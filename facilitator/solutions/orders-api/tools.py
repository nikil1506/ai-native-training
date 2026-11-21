"""Reference solution for L7: three tools, destructive endpoint hidden, helpful errors."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from harness.agent import Tool  # noqa: E402
from starter.common import load_module  # noqa: E402

api = load_module(Path(__file__).resolve().parents[3] / "starter/orders-api/api.py", "orders_api_mod")


def _get(order_id):
    s, o = api.call("GET", f"/orders/{order_id}")
    return o if s == 200 else {"error": f"order {order_id} not found", "hint": "use find_orders to list valid ids"}


def _find(customer="", status=""):
    q = "&".join(f"{k}={v}" for k, v in (("customer", customer), ("status", status)) if v)
    s, rows = api.call("GET", "/orders" + ("?" + q if q else ""))
    return [{"id": o["id"], "customer": o["customer"], "status": o["status"], "total": o["total"]} for o in rows][:20]


def _set_address(order_id, address):
    s, o = api.call("PUT", f"/orders/{order_id}/address", {"address": address})
    if s == 200:
        return {"ok": True, "id": order_id, "address": address}
    return {"error": o["error"] if isinstance(o, dict) else str(o), "hint": "orders that have shipped cannot change address; tell the user"}


def build_tools():
    S = lambda **p: {"type": "object", "properties": {k: {"type": "string", "description": d} for k, d in p.items()}, "required": [k for k in p]}
    return [
        Tool("get_order", "Look up ONE order by its id (e.g. '1001'): status, total, address, items.", S(order_id="order id"), _get),
        Tool("find_orders", "List orders, optionally filtered by customer email and/or status (pending, paid, shipped, delivered). Returns short rows; use get_order for details.",
             {"type": "object", "properties": {"customer": {"type": "string", "description": "customer email"}, "status": {"type": "string"}}}, _find),
        Tool("set_delivery_address", "Change the delivery address of an order that has NOT shipped yet.", S(order_id="order id", address="new full address"), _set_address),
        # delete_order is deliberately NOT exposed: destructive, support never needs it (see tool-design.md)
    ]
