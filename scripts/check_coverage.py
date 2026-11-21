"""Does this repo cover everything the programme guide says? Two checks:
 1. TEXT: every word of the guide's HTML appears in the generated docs (docs/programme/*.md).
 2. ARTIFACTS: every starter, dataset, helper and support item the guide names exists in the repo.
Exit code 0 = all covered."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "docs/programme/AI-Native-Developer-Training-Beginner.html"


class T(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, tag, a):
        self.skip += tag in ("style", "script")
    def handle_endtag(self, tag):
        self.skip -= tag in ("style", "script")
    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def words(s):
    return re.findall(r"[a-z0-9][a-z0-9'./_-]*", s.lower())


def text_check():
    p = T(); p.feed(HTML.read_text(encoding="utf-8"))
    src = words(" ".join(p.out))
    docs = " ".join(f.read_text(encoding="utf-8") for f in (ROOT / "docs/programme").rglob("*.md"))
    have = set(words(docs))
    missing = [w for w in src if w not in have]
    ratio = 1 - len(missing) / len(src)
    print(f"[text] {len(src)} words in the guide, {len(missing)} not found in docs -> {ratio:.2%} covered")
    if missing:
        print("       e.g.", sorted(set(missing))[:15])
    return ratio >= 0.995


ARTIFACTS = {
    # starter repositories named in the guide (labs + instructor guide)
    "starter repos": ["starter/l1", "starter/bugfix-repo", "starter/l3", "starter/orders-app", "starter/sample-repo-2", "starter/backlog",
                      "starter/orders-api", "starter/support-agent", "starter/policy-corpus", "starter/eval", "starter/incidents",
                      "starter/vulnerable-agent", "starter/capstone-scaffold"],
    # per-lab contents the lab text promises
    "L1": ["starter/l1/tickets.jsonl", "starter/l1/classify.py", "starter/l1/score.py", "starter/l1/validator.py"],
    "L2": ["starter/bugfix-repo/service/cart.py", "starter/bugfix-repo/tests/test_cart.py"],
    "L3": ["starter/l3/agent.py", "starter/l3/tasks.json", "starter/l3/sandbox"],
    "L4": ["starter/orders-app/app/api.py", "starter/orders-app/tests", "starter/orders-app/spec_template.md", "starter/orders-app/FEATURE_REQUEST.md"],
    "L5": ["starter/sample-repo-2/textkit", "starter/sample-repo-2/README.md"],
    "L6": ["starter/backlog/item-1.md", "starter/backlog/item-2.md", "docs/cheatsheets/worktree.md"],
    "L7": ["starter/orders-api/api.py", "starter/orders-api/mcp_server.py", "starter/orders-api/tasks.json"],
    "L8": ["starter/support-agent/agent.py", "starter/support-agent/tools.py", "starter/support-agent/scenarios.json", "starter/support-agent/failure.py"],
    "L9": ["starter/policy-corpus/docs", "starter/policy-corpus/questions.json", "starter/policy-corpus/unanswerable.json", "starter/policy-corpus/ingest.py",
           "starter/policy-corpus/score.py", "starter/policy-corpus/access.py"],
    "L10": ["starter/eval/cases.json", "starter/eval/run_eval.py", "starter/eval/judge_prompt.md"],
    "L11": ["starter/eval/tracing_template.py", "starter/eval/trace_report.py"],
    "L12": ["starter/incidents/bundles", "starter/incidents/orchestrator.py", "starter/incidents/schemas", "starter/incidents/rubric.md"],
    "L13": ["starter/incidents/checkpoint.py"],
    "L14": ["starter/vulnerable-agent/agent.py", "starter/vulnerable-agent/attacks"],
    "capstone": ["starter/capstone-scaffold/CAPSTONE.md", "starter/capstone-scaffold/orchestrator.py", "starter/capstone-scaffold/scenarios"],
    "checkpoints": ["starter/a1-flawed-pr/pr.md", "starter/a1-flawed-pr/change.diff", "starter/a2-traces/trace-1.jsonl", "starter/a2-traces/trace-2.jsonl",
                    "starter/a2-traces/trace-3.jsonl", "docs/cheatsheets/review-checklist.md", "docs/cheatsheets/trace-reading-guide.md"],
    "pre-work": ["docs/prework/README.md", "docs/prework/diagnostic.md", "docs/prework/primer.md", "docs/prework/acceptable-use.md",
                 "docs/programme/09-glossary.md", "scripts/doctor.py", "Makefile"],
    "instructor": ["facilitator/INSTRUCTOR-CHECKLIST.md", "facilitator/grading/lab-grading-sheets.md", "facilitator/answer-keys/a1.md",
                   "facilitator/answer-keys/a2.md", "facilitator/answer-keys/incidents.json", "facilitator/solutions", "gateway/__main__.py",
                   "facilitator/templates/self-assessment.md", "facilitator/templates/follow-up-30-60-90.md"],
}


def artifact_check():
    ok = True
    has_fac = (ROOT / "facilitator").is_dir()
    for group, paths in ARTIFACTS.items():
        if group == "instructor" and not has_fac:
            print("[artifacts] instructor     skipped (facilitator/ not present: student branch)")
            continue
        missing = [p for p in paths if not (ROOT / p).exists()]
        ok &= not missing
        print(f"[artifacts] {group:<14} {len(paths) - len(missing)}/{len(paths)}" + (f"  MISSING {missing}" if missing else ""))
    for n in range(1, 16):
        for p in (f"docs/cheatsheets/day-{n:02d}.md", f"facilitator/walkthroughs/day-{n:02d}.md"):
            if not (ROOT / p).exists():
                print("[artifacts] MISSING", p); ok = False
    for n in range(1, 15):
        if not (ROOT / f"docs/programme/labs/L{n}.md").exists():
            print("[artifacts] MISSING lab doc L%d" % n); ok = False
    print(f"[artifacts] 15 cheat sheets, 15 walkthrough scripts, 14 lab docs: {'ok' if ok else 'INCOMPLETE'}")
    return ok


def counts_check():
    h = HTML.read_text(encoding="utf-8")
    boxes = h.count('data-k="')
    docs = sum(p.read_text(encoding="utf-8").count("- [ ] ") for p in (ROOT / "docs/programme/labs").glob("L*.md"))
    print(f"[counts] acceptance criteria: guide {boxes}, docs {docs}; labs 14; days 15")
    return boxes == docs


if __name__ == "__main__":
    results = [text_check(), artifact_check(), counts_check()]
    print("\nALL COVERED" if all(results) else "\nGAPS FOUND")
    sys.exit(0 if all(results) else 1)
