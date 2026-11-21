"""L3: an agent is a loop. Complete the TODOs. Run: python starter/l3/agent.py [task_id]
The tests in test_agent.py run WITHOUT a model (they use a fake one), so you can check your loop quickly:
    python -m unittest discover starter/l3"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from starter.common import SMALL, chat as real_chat  # noqa: E402

SANDBOX = Path(__file__).parent / "sandbox"
MAX_STEPS = 6

TOOL_SPECS = [
    {"type": "function", "function": {"name": "calculator", "description": "Evaluate an arithmetic expression like '2*(3+4)'.",
     "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "read_file", "description": "Read a text file from the sandbox folder.",
     "parameters": {"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}}},
]


def calculator(expression):
    # TODO 2a: evaluate +, -, *, /, parentheses and numbers ONLY. Never call eval() on raw model text.
    # (Hint: use the ast module and walk the tree, or validate characters first.)
    raise NotImplementedError("TODO 2a")


def read_file(path):
    # TODO 2b: resolve (SANDBOX / path), check the result is inside SANDBOX, then read it.
    # If it escapes (e.g. ../secret.txt) raise PermissionError and print a line starting with "BLOCKED:" (the log).
    raise NotImplementedError("TODO 2b")


TOOLS = {"calculator": calculator, "read_file": read_file}


def run_agent(task, chat_fn=real_chat, max_steps=MAX_STEPS, log=print):
    """Returns the final answer, or 'STOPPED: step limit' if the limit was reached."""
    messages = [{"role": "system", "content": "You are a careful assistant. Use tools when needed."},
                {"role": "user", "content": task}]
    for step in range(1, max_steps + 1):
        # TODO 1: call chat_fn(messages, tools=TOOL_SPECS) -> (message, usage).
        #   - append the assistant message to `messages`
        #   - if it has no tool_calls: return its content (the final answer)
        #   - otherwise run each tool call and append {"role": "tool", "tool_name": name, "content": result}
        # TODO 3: log each step: step number, tool name, and tokens (usage["in_tokens"] + usage["out_tokens"]).
        # TODO 4: if a tool raises, send the error text back as the tool message instead of crashing.
        raise NotImplementedError("TODO 1/3/4")
    return "STOPPED: step limit"


if __name__ == "__main__":
    tasks = json.loads((Path(__file__).parent / "tasks.json").read_text())
    pick = [t for t in tasks if len(sys.argv) < 2 or str(t["id"]) == sys.argv[1]]
    for t in pick:
        print(f"\n=== task {t['id']}: {t['prompt']}")
        print("ANSWER:", run_agent(t["prompt"]))
