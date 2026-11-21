"""A deliberately WEAK support agent for the L10 baseline: vague prompt, no guardrails. Improve it (or point run_eval at your L8 agent)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1]))
from harness.agent import Agent  # noqa: E402
from harness.trace import Trace  # noqa: E402
from starter.common import SMALL, load_module  # noqa: E402

tools_mod = load_module(HERE.parent / "support-agent" / "tools.py", "eval_support_tools")
SYSTEM = "Help the customer."   # <- improvement 1 lives here (and in the guardrails you add)


def answer(message):
    """Returns {"final", "tool_calls": [names], "escalated": bool, "refunded": bool}."""
    tools_mod.reset()
    trace = Trace()
    agent = Agent(tools_mod.build_tools(), SYSTEM, max_turns=6, model=SMALL, trace=trace, name="aut")
    res = agent.run(message)
    calls = [e["tool"] for e in trace.events if e["kind"] == "tool"]
    return {"final": res.final, "tool_calls": calls, "escalated": bool(tools_mod.ESCALATIONS),
            "refunded": bool(tools_mod.REFUNDS), "tokens": res.tokens, "seconds": res.seconds}
