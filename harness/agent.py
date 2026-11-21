"""The agent loop: model -> tool calls -> results -> model ... with budgets, hooks, kill switch."""
import json
import os
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

from . import config, llm
from .trace import Trace


class Killed(Exception):
    pass


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict
    fn: Callable

    def spec(self):
        return {"type": "function", "function": {
            "name": self.name, "description": self.description, "parameters": self.parameters}}


@dataclass
class Hooks:
    # pre(name, args) -> reason string to BLOCK, or None to allow
    pre: list = field(default_factory=list)
    # post(name, args, result) -> extra feedback string appended to the result, or None
    post: list = field(default_factory=list)


@dataclass
class Result:
    final: str
    turns: int
    tokens: int
    seconds: float
    stopped: str  # done | max_turns | timeout


MAX_TOOL_OUTPUT = 6000


class Agent:
    def __init__(self, tools, system, hooks=None, max_turns=12, timeout_s=600, trace=None,
                 kill_file=None, model=None, chat_fn=None, name="agent"):
        self.tools = {t.name: t for t in tools}
        self.system = system
        self.hooks = hooks or Hooks()
        self.max_turns, self.timeout_s = max_turns, timeout_s
        self.trace = trace or Trace()
        self.kill_file = kill_file or config.KILL_FILE
        self.model, self.chat, self.name = model, chat_fn or llm.chat, name

    def _call(self, name, args):
        if name not in self.tools:
            return f"ERROR: unknown tool {name!r}. Available: {', '.join(self.tools)}"
        for hook in self.hooks.pre:
            reason = hook(name, args)
            if reason:
                self.trace.event("blocked", agent=self.name, tool=name, args=args, reason=reason)
                return f"BLOCKED by guardrail: {reason}. Choose a safer approach."
        try:
            out = str(self.tools[name].fn(**args))
        except Exception as e:  # tool errors go back to the model, not up the stack
            out = f"ERROR: {type(e).__name__}: {e}"
        for hook in self.hooks.post:
            extra = hook(name, args, out)
            if extra:
                out += "\n[hook] " + extra
        if len(out) > MAX_TOOL_OUTPUT:
            out = out[:MAX_TOOL_OUTPUT] + "\n...[truncated]"
        return out

    def run(self, task):
        msgs = [{"role": "system", "content": self.system}, {"role": "user", "content": task}]
        specs = [t.spec() for t in self.tools.values()]
        start, tokens, last = time.time(), 0, ""
        for turn in range(1, self.max_turns + 1):
            if os.path.exists(self.kill_file):
                self.trace.event("killed", agent=self.name)
                raise Killed(f"kill switch {self.kill_file} present")
            if time.time() - start > self.timeout_s:
                return self._finish(last, turn - 1, tokens, start, "timeout")
            resp = self.chat(msgs, tools=specs, model=self.model)
            m = resp["message"]
            tokens += resp.get("prompt_eval_count", 0) + resp.get("eval_count", 0)
            last = m.get("content", "") or last
            calls = m.get("tool_calls") or []
            entry = {"role": "assistant", "content": m.get("content", "")}
            if calls:
                entry["tool_calls"] = calls
            msgs.append(entry)
            self.trace.event("model", agent=self.name, turn=turn, content=m.get("content", ""),
                             tool_calls=[c["function"]["name"] for c in calls])
            if not calls:
                return self._finish(m.get("content", ""), turn, tokens, start, "done")
            for c in calls:
                name, args = c["function"]["name"], c["function"].get("arguments", {})
                if isinstance(args, str):
                    args = json.loads(args or "{}")
                out = self._call(name, args)
                self.trace.event("tool", agent=self.name, tool=name, args=args, result=out[:500])
                msgs.append({"role": "tool", "tool_name": name, "content": out})
        return self._finish(last, self.max_turns, tokens, start, "max_turns")

    def _finish(self, final, turns, tokens, start, stopped):
        r = Result(final, turns, tokens, round(time.time() - start, 1), stopped)
        self.trace.event("finish", agent=self.name, turns=turns, tokens=tokens,
                         seconds=r.seconds, stopped=stopped)
        return r
