"""Connect an agent to YOUR tools and run the eight task prompts. Prints a pass/fail line per task.
Usage: python starter/orders-api/run_tasks.py [--bad]   (--bad uses tools.py as-is; swap in worse descriptions for the before/after table)"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1]))
from harness.agent import Agent  # noqa: E402
from starter.common import SMALL, load_module  # noqa: E402

tools_mod = load_module(HERE / "tools.py", "orders_tools")
api = tools_mod.api


def state_ok(expr):
    if expr.endswith("exists"):
        return expr.split()[0] in api.DB
    key, _, rhs = expr.partition(" == ")
    oid, field = key.split(".")
    return repr(api.DB[oid][field]) == rhs


def main():
    tasks = json.loads((HERE / "tasks.json").read_text())
    passed = 0
    for t in tasks:
        api.reset()
        agent = Agent(tools_mod.build_tools(), "You help support staff with orders. Use the tools. Be brief.",
                      max_turns=6, model=SMALL, name="orders")
        res = agent.run(t["prompt"])
        ok = all(s.lower() in res.final.lower() for s in t.get("answer_contains", []))
        if "state_check" in t:
            ok = ok and state_ok(t["state_check"])
        passed += ok
        print(f"task {t['id']}: {'PASS' if ok else 'FAIL'} ({res.turns} turns) - {t['prompt']}")
    print(f"\n{passed}/{len(tasks)} tasks passed (acceptance: at least 5 of 8)")


if __name__ == "__main__":
    main()
