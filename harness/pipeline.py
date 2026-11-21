"""Sessions 5-6 capstone: ticket -> Plan -> [human gate] -> Build -> Verify -> [human gate] -> PR.
Contract (see docs/CONTRACT.md): plan.md sections, branch name, verify-report.json."""
import json
import re
import subprocess
import time
from pathlib import Path

from . import config
from .agent import Agent, Killed
from .hooks import default_hooks
from .mcp_client import MCPClient, mcp_tools
from .skills import load_skills, run_skill
from . import llm
from .tools import make_tools
from .trace import Trace

PLAN_SECTIONS = ["## Approach", "## Files to touch", "## Test plan", "## Risks"]


# ---- contract ------------------------------------------------------------------------------
def validate_plan(text):
    errs = [f"missing section {s}" for s in PLAN_SECTIONS if s not in text]
    if not re.search(r"^Ticket:\s*T-\d+", text, re.M):
        errs.append("missing first line 'Ticket: T-123'")
    return errs


def branch_name(ticket_id, title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:30].strip("-")
    return f"agent/{ticket_id}-{slug}"


def validate_report(r):
    errs = [f"missing key {k}" for k in ("ticket", "verdict", "checks", "findings", "pr_description") if k not in r]
    if r.get("verdict") not in ("pass", "fail"):
        errs.append("verdict must be pass|fail")
    return errs


def git(*a, cwd=None):
    p = subprocess.run(["git", *a], cwd=cwd or config.REPO, capture_output=True, text=True, encoding="utf-8")
    return p.returncode, (p.stdout + p.stderr).strip()


def run_tests(cwd, module):
    outs = []
    for args in (["-m", "unittest", module], ["-m", "unittest", "discover", "tests"]):
        p = subprocess.run(["python", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", timeout=120)
        outs.append(p.stdout + p.stderr)
        if p.returncode:
            return False, "\n".join(outs)[-1200:]
    return True, "ok"


def stage_stats(res):
    return {"turns": res.turns, "tokens": res.tokens, "seconds": res.seconds, "stopped": res.stopped}


# ---- stages --------------------------------------------------------------------------------
def plan_stage(ticket_id, trace, model=None, tries=2):
    client = MCPClient()
    try:
        tools = mcp_tools(client) + make_tools(config.REPO, read_only=True)
        system = ("You are a planning agent. Read the ticket with get_ticket, inspect the relevant code with "
                  "read_file, then reply with ONLY a plan in markdown. First line: 'Ticket: <id>'. Then exactly "
                  "these sections: " + ", ".join(PLAN_SECTIONS) + ". Be specific and short. Never edit code.")
        agent = Agent(tools, system, hooks=default_hooks(config.REPO, run_tests=False), max_turns=10,
                      trace=trace, model=model, name="plan")
        task, stats = f"Write the plan for ticket {ticket_id}.", None
        for _ in range(tries):
            res = agent.run(task)
            stats = stage_stats(res)
            text = re.sub(r"^```\w*\n|\n```$", "", res.final.strip())
            errs = validate_plan(text)
            if not errs:
                return text, stats
            task = f"Your plan was invalid: {errs}. Write the plan for ticket {ticket_id} again, fixing this."
        raise RuntimeError(f"plan failed the contract: {errs}")
    finally:
        client.close()


def build_stage(wt, ticket, plan, trace, attempts=3, model=None, feedback=""):
    test_mod = ticket["test"].replace("/", ".").removesuffix(".py")
    system = ("You are a build agent. Implement the plan with the smallest possible code change. Edit only files "
              "under shelfy/. Never edit anything under tests/ or capstone_tests/. Use write_file with the FULL "
              "new file content (read the file first). Then run the ticket's test with run_cmd. Stop when it passes.")
    agent = Agent(make_tools(wt), system, hooks=default_hooks(wt), max_turns=14, trace=trace, model=model, name="build")
    stats = {"attempts": 0, "turns": 0, "tokens": 0, "seconds": 0.0}
    note = feedback
    for i in range(1, attempts + 1):
        res = agent.run(f"PLAN:\n{plan}\n\nTICKET: {ticket['title']}\n{ticket['description']}\n"
                        f"Test to make pass: python -m unittest {test_mod}\n{note}")
        for k in ("turns", "tokens", "seconds"):
            stats[k] += getattr(res, k)
        stats["attempts"] = i
        ok, out = run_tests(wt, test_mod)
        trace.event("build_check", attempt=i, ok=ok)
        if ok:
            git("add", "-A", cwd=wt)
            git("commit", "-m", f"{ticket['id']}: {ticket['title']}", cwd=wt)
            return True, stats
        note = f"\nATTEMPT {i} FAILED. Test output:\n{out}\nFix it."
    return False, stats


REVIEW_GATE = ('You decide if a code review blocks a merge. List only findings that are definite violations of '
               'the team standards or bugs in the diff. Reply as JSON: {"blocking": ["<one-line finding>", ...]} '
               '(empty list if none, including when the review says "No violations").')


def verify_stage(wt, ticket, branch, trace, model=None):
    skills = load_skills()
    test_mod = ticket["test"].replace("/", ".").removesuffix(".py")
    tests_ok, test_out = run_tests(wt, test_mod)
    _, changed = git("diff", "--name-only", f"main...{branch}", cwd=wt)
    tampered = any(f.startswith(("tests/", "capstone_tests/")) for f in changed.splitlines())
    review = run_skill(skills["code-review"], f"Review the range main..{branch}.", root=wt, model=model, trace=trace)
    blocking = llm.ask_json(REVIEW_GATE, review.final, model=model).get("blocking", []) if review.final else []
    pr = run_skill(skills["pr-description"], f"Write a PR description for the range main..{branch}.",
                   root=wt, model=model, trace=trace)
    passed = tests_ok and not tampered and not blocking
    report = {"ticket": ticket["id"], "verdict": "pass" if passed else "fail",
              "checks": {"tests_pass": tests_ok, "tests_untouched": not tampered, "review_clean": not blocking},
              "findings": blocking + ([] if tests_ok else [f"tests failing: {test_out[-300:]}"])
              + (["test files were modified"] if tampered else []),
              "pr_description": pr.final}
    assert not validate_report(report)
    return report, {"seconds": round(review.seconds + pr.seconds, 1), "tokens": review.tokens + pr.tokens}


# ---- orchestration -------------------------------------------------------------------------
def gate(question, auto, input_fn=input):
    if auto:
        print(f"[gate] {question} -> auto-approved")
        return True
    return input_fn(f"[gate] {question} [y/N] ").strip().lower() == "y"


def run_pipeline(ticket_id, auto_approve=False, build_attempts=3, model=None, input_fn=input):
    run_dir = config.RUNS / f"{ticket_id}-{time.strftime('%H%M%S')}"
    trace = Trace(run_dir / "trace.jsonl")
    summary = {"ticket": ticket_id, "run_dir": str(run_dir), "stages": {}, "outcome": None}
    t0 = time.time()

    def finish(outcome):
        summary["outcome"], summary["wall_seconds"] = outcome, round(time.time() - t0, 1)
        (run_dir / "summary.json").write_text(json.dumps(summary, indent=2))
        print(f"\n== {outcome} | {summary['wall_seconds']}s | trace: {run_dir / 'trace.jsonl'}")
        return summary

    try:
        ticket = json.loads(Path(config.REPO / "fixtures/tickets.json").read_text())
        ticket = next(t for t in ticket["tickets"] if t["id"] == ticket_id and "test" in t)
        print(f"== PLAN {ticket_id}")
        plan, summary["stages"]["plan"] = plan_stage(ticket_id, trace, model)
        (run_dir / "plan.md").write_text(plan, encoding="utf-8")
        print(plan)
        if not gate(f"Approve plan? (edit {run_dir / 'plan.md'} first if you like)", auto_approve, input_fn):
            return finish("rejected_at_plan_gate")
        plan = (run_dir / "plan.md").read_text(encoding="utf-8")

        branch = branch_name(ticket_id, ticket["title"])
        wt = run_dir / "work"
        code, out = git("worktree", "add", "-b", branch, str(wt), "main")
        if code:
            raise RuntimeError(out)
        feedback, report = "", None
        for loop in range(2):  # build, verify; one send-back allowed
            print(f"== BUILD (round {loop + 1})")
            ok, summary["stages"][f"build{loop + 1}"] = build_stage(wt, ticket, plan, trace, build_attempts, model, feedback)
            if not ok:
                return finish("build_failed_max_attempts")
            print("== VERIFY")
            report, summary["stages"][f"verify{loop + 1}"] = verify_stage(wt, ticket, branch, trace, model)
            (run_dir / "verify-report.json").write_text(json.dumps(report, indent=2))
            if report["verdict"] == "pass":
                break
            feedback = "\nVERIFY FAILED with findings: " + "; ".join(report["findings"])
        if report["verdict"] != "pass":
            return finish("verify_failed_after_retry")
        print(report["pr_description"])
        if not gate("Open the PR?", auto_approve, input_fn):
            return finish("rejected_at_pr_gate")
        (run_dir / "pr.md").write_text(report["pr_description"], encoding="utf-8")
        print(f"(simulated) PR for branch {branch} written to {run_dir / 'pr.md'}")
        return finish("pr_ready")
    except Killed as e:
        return finish(f"killed: {e}")
