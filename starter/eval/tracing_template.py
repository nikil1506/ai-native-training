"""L11: add tracing. One entry per model call and per tool call with tokens and time. NO personal data in traces.
Wire it in: wrap the agent's chat function and each tool with the helpers below, then run the eval again."""
import json
import time
from pathlib import Path

TRACE_DIR = Path(__file__).parent / "traces"


class Tracer:
    def __init__(self, run_id):
        self.path = TRACE_DIR / f"{run_id}.jsonl"
        TRACE_DIR.mkdir(exist_ok=True)

    def span(self, kind, name, **data):
        # TODO 1: append one JSON line: {"ts", "kind" ("model"|"tool"), "name", "seconds", "in_tokens", "out_tokens", ...data}
        # Redact emails/phone numbers from any text you store (see redact()).
        raise NotImplementedError("TODO 1")


def redact(text):
    # TODO: replace emails and long digit runs with [redacted]
    return text


def traced_chat(chat_fn, tracer, tier="small"):
    def wrapper(messages, **kw):
        t0 = time.time()
        out = chat_fn(messages, **kw)
        # TODO 1: tracer.span("model", ..., seconds=time.time()-t0, in_tokens=..., out_tokens=...)
        return out
    return wrapper
