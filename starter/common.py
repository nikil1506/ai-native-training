"""Shared helpers for every starter. Labs run from the repo root: python starter/<lab>/<script>.py"""
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from harness import llm  # noqa: E402

# Default every lab to the smaller, cheaper model; use LARGE only where a lab compares sizes.
SMALL = os.environ.get("SMALL_MODEL", "qwen3.5:latest")
LARGE = os.environ.get("LARGE_MODEL", "qwen3.8:27b")
# Illustrative prices in USD per 1M tokens (input, output). Local models are free; these let you practise cost maths.
PRICES = {"small": (0.10, 0.40), "large": (0.60, 2.40)}


def chat(messages, model=None, **kw):
    """Returns (message, usage). usage = {in_tokens, out_tokens, seconds}."""
    t0 = time.time()
    r = llm.chat(messages, model=model or SMALL, **kw)
    return r["message"], {"in_tokens": r.get("prompt_eval_count", 0), "out_tokens": r.get("eval_count", 0),
                          "seconds": round(time.time() - t0, 2)}


def cost_usd(usage, tier="small"):
    pin, pout = PRICES[tier]
    return (usage["in_tokens"] * pin + usage["out_tokens"] * pout) / 1_000_000


def load_jsonl(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def load_module(path, name=None):
    """Import a file whose directory name has a hyphen (e.g. starter/support-agent/tools.py)."""
    spec = importlib.util.spec_from_file_location(name or Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod
