"""A minimal JSON API over the order store. handle(method, path, body) -> (status, json)."""
import re

from . import orders


def handle(method, path, body=None):
    body = body or {}
    try:
        if method == "POST" and path == "/orders":
            return 201, orders.create_order(body["customer"], body["items"], body["total_cents"])
        if method == "GET" and path == "/orders":
            return 200, orders.list_orders()
        m = re.fullmatch(r"/orders/(\d+)", path)
        if m and method == "GET":
            return 200, orders.get_order(int(m.group(1)))
        m = re.fullmatch(r"/orders/(\d+)/(pay|ship)", path)
        if m and method == "POST":
            return 200, getattr(orders, m.group(2))(int(m.group(1)))
        return 404, {"error": "not found"}
    except KeyError as e:
        return 404, {"error": str(e)}
    except ValueError as e:
        return 409, {"error": str(e)}
