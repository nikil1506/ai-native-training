"""Scores a postmortem draft (JSON from orchestrator.py) with the rubric. The answer keys live in facilitator/answer-keys/ (the facilitator runs this,
or shares it after the lab).   python starter/incidents/score.py inc-1 draft.json"""
import json
import sys
from pathlib import Path

KEY = Path(__file__).resolve().parents[2] / "facilitator/answer-keys/incidents.json"


def score(inc, draft):
    k = json.loads(KEY.read_text())[inc]
    text = json.dumps({k: v for k, v in draft.items() if not k.startswith("_")}).lower()   # ignore metadata (_review, _usage)
    return {"accuracy_root_cause": any(w.lower() in text for w in k["root_cause_keywords"]),
            "accuracy_no_planted_errors": [m for m in k["must_not_claim"] if m in text] == [],
            "planted_errors_repeated": [m for m in k["must_not_claim"] if m in text],
            "completeness": all(len(draft.get(f) or "") > 0 for f in ("title", "summary", "root_cause", "impact")) and bool(draft.get("timeline")) and bool(draft.get("action_items"))}


if __name__ == "__main__":
    print(json.dumps(score(sys.argv[1], json.loads(Path(sys.argv[2]).read_text())), indent=1))
