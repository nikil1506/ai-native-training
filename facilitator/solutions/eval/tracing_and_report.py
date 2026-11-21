"""Reference for L11: Tracer + report (facilitator)."""
import json
import re
import statistics
import sys
import time
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "harness").is_dir())
sys.path.insert(0, str(ROOT))
from starter.common import PRICES  # noqa: E402

TRACE_DIR = ROOT / "starter/eval/traces"


def redact(text):
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[redacted]", str(text))
    return re.sub(r"\d{7,}", "[redacted]", text)


class Tracer:
    def __init__(self, run_id):
        TRACE_DIR.mkdir(exist_ok=True)
        self.path = TRACE_DIR / f"{run_id}.jsonl"

    def span(self, kind, name, **data):
        e = {"ts": time.time(), "kind": kind, "name": name, **{k: (redact(v) if isinstance(v, str) else v) for k, v in data.items()}}
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(e) + "\n")


def report(paths, tier="small"):
    pin, pout = PRICES[tier]
    tasks, step_cost = [], {}
    for p in paths:
        spans = [json.loads(l) for l in open(p, encoding="utf-8")]
        cost = sum((s.get("in_tokens", 0) * pin + s.get("out_tokens", 0) * pout) / 1e6 for s in spans)
        for s in spans:
            step_cost[s["name"]] = step_cost.get(s["name"], 0) + (s.get("in_tokens", 0) * pin + s.get("out_tokens", 0) * pout) / 1e6
        tasks.append({"seconds": sum(s.get("seconds", 0) for s in spans), "tokens": sum(s.get("in_tokens", 0) + s.get("out_tokens", 0) for s in spans),
                      "cost": cost, "ok": not any(s.get("error") for s in spans)})
    secs = [t["seconds"] for t in tasks]
    return {"success_rate": sum(t["ok"] for t in tasks) / len(tasks), "median_seconds": statistics.median(secs), "slowest_seconds": max(secs),
            "avg_tokens": sum(t["tokens"] for t in tasks) / len(tasks), "avg_cost_usd": sum(t["cost"] for t in tasks) / len(tasks),
            "top3_costs": sorted(step_cost.items(), key=lambda x: -x[1])[:3]}


if __name__ == "__main__":
    print(json.dumps(report(sys.argv[1:]), indent=1))
