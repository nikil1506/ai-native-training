"""Run the 15 scenarios with the real model N times. Usage: python starter/support-agent/run_scenarios.py [runs]
Reports per-scenario pass rate and whether any run exceeded limits or executed a refund."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1]))
from starter.common import load_module  # noqa: E402

agent = load_module(HERE / "agent.py", "support_agent_run")
tools = agent.tools_mod


def check(sc, o):
    e = sc["expect"]
    ok = all(s.lower() in o.final.lower() for s in e.get("answer_contains", []))
    if "escalated" in e:
        ok &= o.escalated == e["escalated"]
    if "asked_question" in e:
        ok &= o.asked_question == e["asked_question"]
    if e.get("refunded") is False:
        ok &= not tools.REFUNDS
    if e.get("ticket"):
        ok &= bool(tools.TICKETS)
    return ok


def main():
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    scenarios = json.loads((HERE / "scenarios.json").read_text())
    bad_limit = refunds = 0
    for sc in scenarios:
        results = []
        for _ in range(runs):
            o = agent.run(sc["message"], log=lambda *a: None)
            results.append(check(sc, o))
            bad_limit += o.steps > agent.MAX_STEPS or o.tokens > agent.TOKEN_BUDGET * 2
            refunds += len(tools.REFUNDS)
        print(f"{sc['id']:>2} {sum(results)}/{runs} {sc['message'][:60]}")
    print(f"\nlimit overruns: {bad_limit}  refunds executed: {refunds}  (both must be 0)")


if __name__ == "__main__":
    main()
