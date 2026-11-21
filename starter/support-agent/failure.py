"""Provided failure-injection switch. INJECT_FAILURES=1 makes tools sometimes time out or return bad data (seeded, repeatable)."""
import os
import random

_rng = random.Random(int(os.environ.get("INJECT_SEED", "7")))


def enabled():
    return os.environ.get("INJECT_FAILURES") == "1"


def inject(name, fn):
    def wrapped(**kw):
        if enabled() and name in ("lookup_order", "search_kb"):
            r = _rng.random()
            if r < 0.30:
                raise TimeoutError(f"{name} timed out")
            if r < 0.45:
                return {"garbage": True}  # bad data
        return fn(**kw)
    return wrapped
