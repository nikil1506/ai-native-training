import argparse
import json
import sys
import tempfile
from pathlib import Path

from . import config


def main():
    ap = argparse.ArgumentParser(prog="harness", description="Agent harness demo (Ollama)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ap.add_argument("--model", help=f"default {config.MODEL} (env HARNESS_MODEL)")

    p = sub.add_parser("chat", help="run a bare agent with file/shell tools + guardrail hooks")
    p.add_argument("task"); p.add_argument("--max-turns", type=int, default=10)
    p = sub.add_parser("route", help="which skill would load for this prompt?"); p.add_argument("prompt")
    p = sub.add_parser("skill", help="run one skill headless (this is the CI job entrypoint)")
    p.add_argument("name"); p.add_argument("--task", required=True)
    p.add_argument("--max-turns", type=int, default=8); p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--out", help="write final answer here")
    p = sub.add_parser("eval", help="trigger + output evals")
    p.add_argument("--skill"); p.add_argument("--trigger-only", action="store_true")
    p.add_argument("--runs", type=int, default=1); p.add_argument("--limit", type=int)
    p.add_argument("--baseline", action="store_true", help="also run without the skill")
    p = sub.add_parser("redteam", help="replay fixtures/redteam.json against the hooks")
    p = sub.add_parser("mcp", help="ask a question using only the MCP ticket server"); p.add_argument("question")
    p = sub.add_parser("pipeline", help="ticket -> plan -> build -> verify -> PR")
    p.add_argument("ticket"); p.add_argument("--auto-approve", action="store_true")
    p = sub.add_parser("kill", help="create (or --clear) the kill switch"); p.add_argument("--clear", action="store_true")
    a = ap.parse_args()
    m = a.model

    if a.cmd == "chat":
        from .agent import Agent
        from .hooks import default_hooks
        from .tools import make_tools
        from .trace import Trace
        import time
        tr = Trace(config.RUNS / f"chat-{int(time.time())}.jsonl")
        r = Agent(make_tools(config.REPO), "You are a careful engineer in a git repo. Use tools.",
                  hooks=default_hooks(config.REPO), max_turns=a.max_turns, trace=tr, model=m).run(a.task)
        print(r.final); print(f"\n[{r.stopped} turns={r.turns} tokens={r.tokens} {r.seconds}s trace={tr.path}]")
    elif a.cmd == "route":
        from .skills import load_skills, route
        print(route(a.prompt, load_skills(), model=m) or "(no skill)")
    elif a.cmd == "skill":
        from .skills import load_skills, run_skill
        from .trace import Trace
        import time
        sk = load_skills()[a.name]
        tr = Trace(config.RUNS / f"skill-{a.name}-{int(time.time())}.jsonl")
        from .agent import Agent  # noqa
        r = run_skill(sk, a.task, model=m, max_turns=a.max_turns, trace=tr)
        print(r.final)
        if a.out:
            Path(a.out).write_text(r.final, encoding="utf-8")
        print(f"\n[{r.stopped} turns={r.turns} tokens={r.tokens} {r.seconds}s trace={tr.path}]", file=sys.stderr)
        sys.exit(0 if r.stopped == "done" else 1)
    elif a.cmd == "eval":
        from .evals import run_all
        run_all(a.skill, a.trigger_only, a.runs, a.limit, a.baseline, m)
    elif a.cmd == "redteam":
        from .hooks import command_blocklist, secret_scan
        bad = 0
        for c in json.loads((config.REPO / "fixtures/redteam.json").read_text()):
            d = Path(tempfile.mkdtemp())
            for f, t in c.get("setup", {}).items():
                (d / f).write_text(t)
            why = next((x for h in (command_blocklist(d), secret_scan) if (x := h(c["tool"], c["args"]))), None)
            ok = (why is not None) == (c["expect"] == "block")
            bad += not ok
            print(f"{'OK  ' if ok else 'FAIL'} {c['expect']:<6}{c['name']:<28}{why or ''}")
        sys.exit(1 if bad else 0)
    elif a.cmd == "mcp":
        from .agent import Agent
        from .mcp_client import MCPClient, mcp_tools
        c = MCPClient()
        try:
            r = Agent(mcp_tools(c), "Answer using ONLY the ticket tools. Be brief and cite ticket ids.",
                      max_turns=8, model=m, name="mcp").run(a.question)
            print(r.final)
        finally:
            c.close()
    elif a.cmd == "pipeline":
        from .pipeline import run_pipeline
        s = run_pipeline(a.ticket, a.auto_approve, model=m)
        sys.exit(0 if s["outcome"] == "pr_ready" else 1)
    elif a.cmd == "kill":
        if a.clear:
            config.KILL_FILE.unlink(missing_ok=True); print("kill switch cleared")
        else:
            config.RUNS.mkdir(exist_ok=True); config.KILL_FILE.write_text("stop"); print("kill switch SET")


main()
