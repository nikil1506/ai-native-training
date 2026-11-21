"""L8: a single agent whose limits are ENFORCED IN CODE. Complete the TODOs, then run:
    python -m unittest discover starter/support-agent      (offline, uses a fake model)
    python starter/support-agent/run_scenarios.py          (real model; add INJECT_FAILURES=1 for chaos)
Rule of thumb: the prompt asks, the code enforces."""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1]))
from starter.common import SMALL, chat as real_chat, load_module  # noqa: E402

tools_mod = load_module(HERE / "tools.py", "support_tools")
failure = load_module(HERE / "failure.py", "support_failure")

MAX_STEPS = 6
TOKEN_BUDGET = 6000
SYSTEM = ("You are a customer support agent. Tools: lookup_order, search_kb, create_ticket, escalate_to_human. "
          "Be brief. Use only tool results for facts.")


@dataclass
class Outcome:
    final: str = ""
    steps: int = 0
    tokens: int = 0
    escalated: bool = False
    asked_question: bool = False
    stopped: str = "done"           # done | step_limit | token_budget | escalated | asked
    plan: str = ""
    log: list = field(default_factory=list)


def extract_order_id(text):
    m = re.search(r"\b(\d{5})\b", text)
    return m.group(1) if m else None


def run(message, chat_fn=real_chat, model=SMALL, log=print):
    tools_mod.reset()
    out = Outcome()
    fails = {}                                              # tool name -> consecutive failures

    def wrap(name, fn):
        inner = failure.inject(name, fn)
        def call(**kw):
            # TODO 4: if the tool raises or returns bad data (a dict with no useful fields / "garbage"),
            # count it in `fails`; on the SECOND failure of the same tool call escalate_to_human (don't retry forever).
            return inner(**kw)
        return call

    tools = {t.name: t for t in tools_mod.build_tools(wrap)}
    specs = [t.spec() for t in tools.values()]

    # TODO 5: if the message is about an order (order/package/delivery/tracking) but has no order number
    # (extract_order_id), do NOT call the model: set out.asked_question=True, out.stopped="asked",
    # out.final = a question asking for the order number, and return out.
    # TODO 2: refunds ALWAYS go to a human. If the message asks for a refund/money back, call
    # tools['escalate_to_human'] in CODE (not via the model) and return. Also never let process_refund run.
    # TODO 3: ask the model for a short plan BEFORE acting (a call with no tools), store it in out.plan and log it.

    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": message}]
    while True:
        # TODO 1: enforce limits INSIDE the loop, BEFORE each model call:
        #   steps >= MAX_STEPS -> out.stopped = "step_limit"; tokens >= TOKEN_BUDGET -> "token_budget".
        #   On a limit, escalate to a human and return (never loop on).
        # Then: msg, usage = chat_fn(messages, tools=specs, model=model); count tokens and steps;
        # run tool calls and append tool results; return when the model answers without tool calls.
        raise NotImplementedError("TODO 1")
