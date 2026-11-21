"""Offline tests for the harness itself (no Ollama needed)."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from harness import hooks, mcp_server, pipeline
from harness.agent import Agent, Hooks, Killed, Tool
from harness.evals import run_check
from harness.skills import load_skills

REPO = Path(__file__).resolve().parent.parent


def fake_llm(script):
    it = iter(script)
    return lambda messages, tools=None, model=None: next(it)


def call(name, **args):
    return {"message": {"content": "", "tool_calls": [{"function": {"name": name, "arguments": args}}]}}


def say(text):
    return {"message": {"content": text}}


class AgentLoop(unittest.TestCase):
    def setUp(self):
        self.echo = Tool("echo", "echo", {"type": "object", "properties": {}}, lambda text="": text)
        self.kill = Path(tempfile.mkdtemp()) / "KILL"

    def test_tool_roundtrip(self):
        a = Agent([self.echo], "s", chat_fn=fake_llm([call("echo", text="hi"), say("done")]), kill_file=self.kill)
        r = a.run("go")
        self.assertEqual((r.final, r.stopped, r.turns), ("done", "done", 2))

    def test_max_turns(self):
        a = Agent([self.echo], "s", max_turns=2, kill_file=self.kill,
                  chat_fn=fake_llm([call("echo", text="a")] * 5))
        self.assertEqual(a.run("go").stopped, "max_turns")

    def test_pre_hook_blocks(self):
        ran = []
        t = Tool("run_cmd", "", {}, lambda cmd: ran.append(cmd) or "ran")
        a = Agent([t], "s", hooks=Hooks(pre=[hooks.command_blocklist()]), kill_file=self.kill,
                  chat_fn=fake_llm([call("run_cmd", cmd="git push --force origin main"), say("ok")]))
        a.run("go")
        self.assertEqual(ran, [])
        self.assertTrue(any(e["kind"] == "blocked" for e in a.trace.events))

    def test_post_hook_feedback(self):
        a = Agent([self.echo], "s", hooks=Hooks(post=[lambda n, a, r: "FIX ME"]), kill_file=self.kill,
                  chat_fn=fake_llm([call("echo", text="x"), say("k")]))
        a.run("go")
        self.assertIn("[hook] FIX ME", [e for e in a.trace.events if e["kind"] == "tool"][0]["result"])

    def test_kill_switch(self):
        self.kill.write_text("x")
        a = Agent([self.echo], "s", kill_file=self.kill, chat_fn=fake_llm([say("never")]))
        with self.assertRaises(Killed):
            a.run("go")

    def test_unknown_tool_is_reported_not_fatal(self):
        a = Agent([self.echo], "s", kill_file=self.kill, chat_fn=fake_llm([call("nope"), say("k")]))
        self.assertEqual(a.run("go").final, "k")


class Redteam(unittest.TestCase):
    def test_replay(self):
        for c in json.loads((REPO / "fixtures/redteam.json").read_text()):
            with self.subTest(c["name"]):
                d = Path(tempfile.mkdtemp())
                for f, t in c.get("setup", {}).items():
                    (d / f).write_text(t)
                why = next((x for h in (hooks.command_blocklist(d), hooks.secret_scan)
                            if (x := h(c["tool"], c["args"]))), None)
                self.assertEqual(why is not None, c["expect"] == "block", why)


class Skills(unittest.TestCase):
    def test_all_skills_well_formed(self):
        sk = load_skills()
        for n in ("pr-description", "code-review", "changelog", "commit-helper"):
            self.assertIn(n, sk)
        for s in sk.values():
            self.assertLess(len(s.body.splitlines()), 40, f"{s.name} body should stay short")

    def test_trigger_eval_files(self):
        for n, s in load_skills().items():
            f = s.path / "evals" / "trigger.json"
            if f.exists() and n != "commit-helper":
                d = json.loads(f.read_text())
                self.assertEqual((len(d["should_trigger"]), len(d["should_not_trigger"])), (10, 10), n)

    def test_checks(self):
        self.assertTrue(run_check({"type": "contains_all", "values": ["A", "b"]}, "a B"))
        self.assertTrue(run_check({"type": "not_contains_any", "values": ["x"]}, "abc"))
        self.assertFalse(run_check({"type": "max_chars", "n": 2}, "abc"))


class MCP(unittest.TestCase):
    def test_pagination_and_errors(self):
        r = mcp_server.search_tickets(page_size=3)
        self.assertEqual(len(r["items"]), 3)
        self.assertGreater(r["total_pages"], 1)
        with self.assertRaises(mcp_server.ToolError) as e:
            mcp_server.get_ticket("T-999")
        self.assertIn("hint", e.exception.payload["error"])

    def test_blockers(self):
        r = mcp_server.list_blockers("R-1.0")
        for row in r["blocked"]:
            self.assertTrue(all(b["status"] != "done" for b in row["blocked_by"]))

    def test_rpc(self):
        out = mcp_server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                 "params": {"name": "get_ticket", "arguments": {"id": "T-201"}}})
        self.assertFalse(out["result"]["isError"])


class Contract(unittest.TestCase):
    def test_plan(self):
        good = "Ticket: T-201\n## Approach\n## Files to touch\n## Test plan\n## Risks\n"
        self.assertEqual(pipeline.validate_plan(good), [])
        self.assertTrue(pipeline.validate_plan("nothing"))

    def test_branch(self):
        self.assertEqual(pipeline.branch_name("T-201", "validate_sku accepts trailing newline"),
                         "agent/T-201-validate-sku-accepts-trailing")

    def test_report(self):
        self.assertEqual(pipeline.validate_report(
            {"ticket": "T-1", "verdict": "pass", "checks": {}, "findings": [], "pr_description": ""}), [])
        self.assertTrue(pipeline.validate_report({"verdict": "maybe"}))


if __name__ == "__main__":
    unittest.main()
