"""L8: a single agent whose limits are ENFORCED IN CODE. Complete the TODOs, then run:
    python -m unittest discover starter/support-agent      (offline, uses a fake model)
    python starter/support-agent/run_scenarios.py          (real model; add INJECT_FAILURES=1 for chaos)
Rule of thumb: the prompt asks, the code enforces."""
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = next(p for p in Path(__file__).resolve().parents if (p / "harness").is_dir())
HERE = ROOT / "starter/support-agent"
sys.path.insert(0, str(ROOT))
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
    fails = {}
    holder = {}

    def escalate(reason):
        holder["tools"]["escalate_to_human"].fn(reason=reason)
        out.escalated = True
        log(f"escalated: {reason}")

    def wrap(name, fn):
        inner = failure.inject(name, fn)

        def call(**kw):
            if name == "process_refund":                       # never executes: becomes a hand-off
                escalate("refund requested: humans only")
                return {"error": "refunds are handled by a human; you have escalated"}
            try:
                res = inner(**kw)
                bad = isinstance(res, dict) and res.get("garbage")
            except Exception as e:
                res, bad = {"error": f"{type(e).__name__}: {e}"}, True
            if bad:
                fails[name] = fails.get(name, 0) + 1
                if fails[name] >= 2:
                    escalate(f"{name} failed twice")
                    return {"error": "tool failing repeatedly; escalated to a human"}
                return {"error": "tool failed or returned bad data", "hint": "you may retry once"}
            return res
        return call

    tools = {t.name: t for t in tools_mod.build_tools(wrap)}
    holder["tools"] = tools
    specs = [t.spec() for t in tools.values()]

    low = message.lower()
    if re.search(r"refund|money back", low):                   # deterministic rule: not the model's decision
        escalate("customer asked for a refund")
        out.stopped, out.final = "escalated", "I have passed your refund request to a human colleague."
        return out
    if re.search(r"order|package|delivery|tracking", low) and not extract_order_id(message):
        out.asked_question, out.stopped = True, "asked"
        out.final = "Could you share your 5-digit order number so I can check?"
        return out

    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": message}]
    pmsg, u = chat_fn(messages + [{"role": "user", "content": "First write a one-line plan starting with 'Plan:'. Do not act yet."}], model=model)
    out.plan = pmsg.get("content", "")
    out.tokens += u["in_tokens"] + u["out_tokens"]
    log(f"plan: {out.plan}")
    messages.append({"role": "system", "content": out.plan})

    while True:
        if out.steps >= MAX_STEPS or out.tokens >= TOKEN_BUDGET:
            out.stopped = "step_limit" if out.steps >= MAX_STEPS else "token_budget"
            escalate(f"stopped: {out.stopped}")
            out.final = out.final or "I couldn't finish this, so I have asked a human to take over."
            return out
        if out.escalated:
            out.stopped = "escalated"
            out.final = out.final or "I have handed this to a human colleague."
            return out
        msg, usage = chat_fn(messages, tools=specs, model=model)
        out.steps += 1
        out.tokens += usage["in_tokens"] + usage["out_tokens"]
        calls = msg.get("tool_calls") or []
        messages.append({k: v for k, v in msg.items() if k in ("role", "content", "tool_calls") and v})
        if not calls:
            out.final = msg.get("content", "")
            return out
        for c in calls:
            name, args = c["function"]["name"], c["function"].get("arguments", {})
            log(f"step {out.steps}: {name} {args}")
            try:
                res = tools[name].fn(**args)
            except Exception as e:
                res = {"error": f"{type(e).__name__}: {e}"}
            messages.append({"role": "tool", "tool_name": name, "content": str(res)})
