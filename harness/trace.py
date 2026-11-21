"""Session 5: every run leaves a trace you can read afterwards."""
import json
import time
from pathlib import Path


class Trace:
    def __init__(self, path=None):
        self.path = Path(path) if path else None
        self.events = []
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def event(self, kind, **data):
        e = {"ts": round(time.time(), 3), "kind": kind, **data}
        self.events.append(e)
        if self.path:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(e, default=str) + "\n")
        return e
