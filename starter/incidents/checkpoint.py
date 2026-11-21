"""Provided checkpoint helper for L13. save(run_id, state) writes atomically; load(run_id) returns state or None.
mark_sent / was_sent make side effects idempotent: record that something was sent BEFORE moving on."""
import json
import os
from pathlib import Path

DIR = Path(__file__).parent / "runs"


def _p(run_id):
    DIR.mkdir(exist_ok=True)
    return DIR / f"{run_id}.json"


def save(run_id, state):
    tmp = _p(run_id).with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1), encoding="utf-8")
    os.replace(tmp, _p(run_id))       # atomic: a crash never leaves half a file


def load(run_id):
    return json.loads(_p(run_id).read_text(encoding="utf-8")) if _p(run_id).exists() else None


def mark_sent(state, key):
    state.setdefault("sent", []).append(key)


def was_sent(state, key):
    return key in state.get("sent", [])
