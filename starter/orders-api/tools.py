"""L7 task 1-2, 5: design at most FOUR tools over api.call(). Names and descriptions ARE prompts.
Return `TOOLS` (agent Tool objects). Keep outputs short; return helpful errors with a hint.
Decide what to hide or guard (the DELETE endpoint!) and write why in tool-design.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from harness.agent import Tool  # noqa: E402
from starter.common import load_module  # noqa: E402

api = load_module(Path(__file__).parent / "api.py", "orders_api_mod")


def build_tools():
    # TODO: return a list of at most 4 Tool(name, description, parameters_json_schema, fn).
    # Example shape:
    #   Tool("get_order", "Look up one order by its id (e.g. '1001'). Returns status, total, address.",
    #        {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
    #        lambda order_id: ...)
    # Errors: return {"error": "...", "hint": "what to try next"} instead of raising.
    raise NotImplementedError("design your tools")
