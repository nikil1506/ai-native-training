"""Reference solution for L3."""
import ast
import json
import operator
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from starter.common import chat as real_chat  # noqa: E402

SANDBOX = Path(__file__).resolve().parents[3] / "starter/l3/sandbox"
MAX_STEPS = 6
TOOL_SPECS = [
    {"type": "function", "function": {"name": "calculator", "description": "Evaluate an arithmetic expression like '2*(3+4)'.",
     "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a text file from the sandbox folder.",
     "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
]
OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.USub: operator.neg}


def calculator(expression):
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.operand))
        raise ValueError("only numbers and + - * / ( ) are allowed")
    r = ev(ast.parse(expression, mode="eval").body)
    return str(int(r) if float(r).is_integer() else r)


def read_file(path):
    full = (SANDBOX / path).resolve()
    if SANDBOX.resolve() not in full.parents:
        print(f"BLOCKED: path escapes sandbox: {path}")
        raise PermissionError(f"path escapes sandbox: {path}")
    return full.read_text(encoding="utf-8")


TOOLS = {"calculator": calculator, "read_file": read_file}


def run_agent(task, chat_fn=real_chat, max_steps=MAX_STEPS, log=print):
    messages = [{"role": "system", "content": "You are a careful assistant. Use tools when needed. If a tool is blocked or the task cannot be done with the files given, say so plainly."},
                {"role": "user", "content": task}]
    for step in range(1, max_steps + 1):
        msg, usage = chat_fn(messages, tools=TOOL_SPECS)
        messages.append({k: v for k, v in msg.items() if k in ("role", "content", "tool_calls") and v})
        calls = msg.get("tool_calls") or []
        tokens = usage["in_tokens"] + usage["out_tokens"]
        if not calls:
            log(f"step {step}: final answer, tokens={tokens}")
            return msg.get("content", "")
        for c in calls:
            name, args = c["function"]["name"], c["function"].get("arguments", {})
            if isinstance(args, str):
                args = json.loads(args or "{}")
            log(f"step {step}: tool={name} args={args} tokens={tokens}")
            try:
                result = str(TOOLS[name](**args))
            except Exception as e:
                result = f"ERROR: {type(e).__name__}: {e}"
            messages.append({"role": "tool", "tool_name": name, "content": result})
    return "STOPPED: step limit"


if __name__ == "__main__":
    tasks = json.loads((SANDBOX.parent / "tasks.json").read_text())
    for t in [t for t in tasks if len(sys.argv) < 2 or str(t["id"]) == sys.argv[1]]:
        print(f"\n=== task {t['id']}: {t['prompt']}")
        print("ANSWER:", run_agent(t["prompt"]))
