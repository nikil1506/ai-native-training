"""L10 runner. python starter/eval/run_eval.py [--name baseline] [--runs 1] [--agent module:function]
Code checks + LLM judge; reports overall, per-category and HELD-OUT scores; saves reports/<name>.json."""
import argparse
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parents[1]))
from starter.common import SMALL, chat  # noqa: E402
import os  # noqa: E402

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", SMALL)   # pitfall: the agent's own model as the ONLY judge. Try LARGE.


# ---- code checks: add your own (TODO 2): each returns (ok, why)
def check_tool_called(result, expected):
    return (expected in result["tool_calls"], f"expected tool {expected}, got {result['tool_calls']}")


def check_refund_escalated(result, _=None):
    # TODO 2: a refund request must end in escalation and NEVER in an executed refund.
    return (False, "TODO: implement check_refund_escalated")


CODE_CHECKS = {
    "tool": check_tool_called,
    "contains": lambda r, vals: (all(v.lower() in r["final"].lower() for v in vals), f"missing one of {vals}"),
    "not_contains": lambda r, vals: (not any(v.lower() in r["final"].lower() for v in vals), f"contains forbidden {vals}"),
    "escalated": lambda r, want: (r["escalated"] == want, f"escalated={r['escalated']}"),
    "refunded": lambda r, want: (r["refunded"] == want, f"refunded={r['refunded']}"),
    "asks_question": lambda r, want: (("?" in r["final"]) == want, "no question asked"),
}


def judge(case, result):
    prompt = (HERE / "judge_prompt.md").read_text().replace("{input}", case["input"]).replace("{answer}", result["final"])
    msg, _ = chat([{"role": "user", "content": prompt}], model=JUDGE_MODEL, json_mode=True)
    try:
        j = json.loads(msg["content"])
        return bool(j.get("pass")), j.get("reason", "")
    except ValueError:
        return False, "judge returned invalid JSON"


def run(agent_fn, cases, runs=1):
    rows = []
    for c in cases:
        for i in range(runs):
            r = agent_fn(c["input"])
            code = {k: CODE_CHECKS[k](r, v) for k, v in c["checks"].items()}
            j_ok, j_why = judge(c, r)
            rows.append({"id": c["id"], "category": c["category"], "heldout": c.get("heldout", False), "run": i,
                         "code_ok": all(ok for ok, _ in code.values()),
                         "code_fail": [f"{k}: {why}" for k, (ok, why) in code.items() if not ok],
                         "judge_ok": j_ok, "judge_why": j_why, "answer": r["final"], "tokens": r.get("tokens", 0),
                         "seconds": r.get("seconds", 0)})
            print(f"case {c['id']:>2} [{c['category']:<11}] code={'PASS' if rows[-1]['code_ok'] else 'FAIL'} judge={'PASS' if j_ok else 'FAIL'}", flush=True)
    return rows


def summarize(rows):
    def rate(rs, key="code_ok"):
        return round(sum(r[key] for r in rs) / len(rs), 2) if rs else None
    dev, held = [r for r in rows if not r["heldout"]], [r for r in rows if r["heldout"]]
    return {"overall_code": rate(rows), "overall_judge": rate(rows, "judge_ok"), "dev_code": rate(dev), "heldout_code": rate(held),
            "by_category": {c: rate([r for r in rows if r["category"] == c]) for c in sorted({r["category"] for r in rows})},
            "n_cases": len({r["id"] for r in rows})}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="baseline"); ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--agent", default="agent_under_test:answer")
    a = ap.parse_args()
    mod, fn = a.agent.split(":")
    agent_fn = getattr(importlib.import_module(mod), fn)
    cases = json.loads((HERE / "cases.json").read_text())
    rows = run(agent_fn, cases, a.runs)
    s = summarize(rows)
    (HERE / "reports").mkdir(exist_ok=True)
    (HERE / "reports" / f"{a.name}.json").write_text(json.dumps({"summary": s, "rows": rows}, indent=1))
    print(json.dumps(s, indent=1))
    print("\nIf heldout_code is far below dev_code you have over-fitted.")
