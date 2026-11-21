"""Generate per-day cheat sheets, per-lab grading sheets and facilitator walkthrough scripts from docs/programme/*.md.
Run after scripts/html_to_docs.py:  python scripts/gen_programme_assets.py"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROG = ROOT / "docs/programme"
RUN = {  # lab -> (starter dir, how to run / check)
    "L1": ("starter/l1", ["python starter/l1/classify.py 1   # then 2, 4, 5 as you complete each TODO"]),
    "L2": ("starter/bugfix-repo", ["cd starter/bugfix-repo", "python -m unittest discover tests"]),
    "L3": ("starter/l3", ["python -m unittest discover starter/l3    # offline, fake model", "python starter/l3/agent.py        # real model, 5 tasks"]),
    "L4": ("starter/orders-app", ["cd starter/orders-app", "python -m unittest discover tests"]),
    "L5": ("starter/sample-repo-2", ["cd starter/sample-repo-2", "python -m unittest discover tests   # then run YOUR review skill here"]),
    "L6": ("starter/backlog", ["see docs/cheatsheets/worktree.md", "build in starter/orders-app; artifacts/ holds one markdown file per stage"]),
    "L7": ("starter/orders-api", ["python starter/orders-api/run_tasks.py", "python starter/orders-api/mcp_server.py   # your MCP server"]),
    "L8": ("starter/support-agent", ["python -m unittest discover starter/support-agent", "python starter/support-agent/run_scenarios.py 3   (INJECT_FAILURES=1 for chaos)"]),
    "L9": ("starter/policy-corpus", ["python starter/policy-corpus/ingest.py 40", "python starter/policy-corpus/score.py   # hit@5 / hit@1 + access test"]),
    "L10": ("starter/eval", ["python starter/eval/run_eval.py --name baseline", "python starter/eval/check_threshold.py starter/eval/reports/after.json 0.7"]),
    "L11": ("starter/eval", ["python starter/eval/trace_report.py starter/eval/traces/*.jsonl", "re-run the L10 eval and compare quality + cost"]),
    "L12": ("starter/incidents", ["python starter/incidents/orchestrator.py inc-1 single", "python starter/incidents/orchestrator.py inc-1 team"]),
    "L13": ("starter/incidents", ["use starter/incidents/checkpoint.py", "kill the run part-way, rerun with the same run id: finished steps must not repeat"]),
    "L14": ("starter/vulnerable-agent", ["python starter/vulnerable-agent/run_attack.py 1   # 1-5", "python -m unittest starter/vulnerable-agent/test_hardening.py   # AGENT=path/to/your/agent.py"]),
}


def days():
    text = (PROG / "04-daily-syllabus.md").read_text(encoding="utf-8")
    parts = re.split(r"^Day (\d+)\s*$", text, flags=re.M)
    out = {}
    for i in range(1, len(parts), 2):
        out[int(parts[i])] = parts[i + 1]
    return out


def section(md, heading):
    m = re.search(rf"^#+ {re.escape(heading)}.*?\n(.*?)(?=^#+ |\Z)", md, re.M | re.S)
    return m.group(1).strip() if m else ""


def labs():
    return {p.stem: p.read_text(encoding="utf-8") for p in (PROG / "labs").glob("L*.md")}


def main():
    D, L = days(), labs()
    (ROOT / "docs/cheatsheets").mkdir(exist_ok=True)
    for n, md in D.items():
        title = re.search(r"^### (.+)$", md, re.M).group(1)
        outcomes = section(md, "By the end of the day you can")
        morning = section(md, "Morning session")
        lab_ids = re.findall(r"- (L\d+) ·", md)
        cp = re.search(r"> \*\*Checkpoint:\*\* (.+)", md)
        lines = [f"# Day {n} cheat sheet: {title}\n", "## By the end of the day you can\n", outcomes + "\n",
                 "## Key concepts (this morning)\n", morning + "\n"]
        for lid in lab_ids:
            lab = L[lid]
            starter, cmds = RUN[lid]
            lines += [f"## Today's lab: {lid}\n", f"Lab text: `docs/programme/labs/{lid}.md` · starter: `{starter}`\n", "```", *cmds, "```\n",
                      "### Hint cards\n", section(lab, "Hint cards") + "\n"]
        if cp:
            lines += [f"## Checkpoint\n\n{cp.group(1)}\n"]
        lines += ["## The stuck ladder\n", "1. Re-read the task and the hint card (5 min).", "2. Ask your coding assistant to **explain** the error, not to fix it.",
                  "3. Check this cheat sheet.", "4. Ask a facilitator.", "5. Skip to the next task, mark it, and catch up in office hours.\n",
                  "## Explain it back\n\nAt the debrief you will explain one thing you built in your own words.\n"]
        (ROOT / f"docs/cheatsheets/day-{n:02d}.md").write_text("\n".join(lines), encoding="utf-8")
    # grading sheets
    g = ["# Lab grading sheets\n", "A lab counts when **all** acceptance criteria are met; facilitators may accept a documented, reasoned exception. "
         "Labs are 40% of the final result (14 labs).\n"]
    for lid in sorted(L, key=lambda x: int(x[1:])):
        lab = L[lid]
        title = re.search(r"\*\*L\d+\*\*\s*(.*?)\s*\*\[", lab).group(1)
        g += [f"## {lid} · {title}\n", "**Deliverables**\n", section(lab, "Deliverables") + "\n", "**Acceptance criteria**\n",
              section(lab, "Acceptance criteria").replace("- [ ]", "- [ ]") + "\n", "Exception accepted? ☐ yes (reason: ______________)   Result: ☐ met  ☐ not met\n"]
    (ROOT / "facilitator/grading").mkdir(exist_ok=True)
    (ROOT / "facilitator/grading/lab-grading-sheets.md").write_text("\n".join(g), encoding="utf-8")
    # walkthrough scripts (what the facilitator live-codes, and what to record)
    (ROOT / "facilitator/walkthroughs").mkdir(exist_ok=True)
    for n, md in D.items():
        title = re.search(r"^### (.+)$", md, re.M).group(1)
        lab_ids = re.findall(r"- (L\d+) ·", md)
        w = [f"# Day {n} guided walkthrough script: {title}\n", "45 minutes, live-coded; **record it** so a participant who falls behind can replay it.\n"]
        for lid in lab_ids:
            lab = L[lid]
            w += [f"## {lid}\n", "**Guided start (from the lab):**\n", section(lab, "Guided start").replace("**Guided start.**", "") or re.search(r"\*\*Guided start\.\*\*(.*)", lab).group(1).strip(), "",
                  "**Live-code, in order:** the first one or two Tasks of the lab:\n", "\n".join(section(lab, "Tasks").splitlines()[:6]) + "\n",
                  f"**Run it:** `{RUN[lid][1][0]}`\n", "**Stop when:** the first TODO is done and the participants can continue alone. Show where the hint cards are.\n"]
        (ROOT / f"facilitator/walkthroughs/day-{n:02d}.md").write_text("\n".join(w), encoding="utf-8")
    print("cheat sheets:", len(D), "walkthroughs:", len(D), "labs graded:", len(L))


main()
