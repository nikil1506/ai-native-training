"""Tiny order store (in memory). Statuses: pending -> paid -> shipped -> delivered."""
import itertools

_ids = itertools.count(1)
ORDERS = {}


def reset():
    ORDERS.clear()


def create_order(customer, items, total_cents):
    oid = next(_ids)
    ORDERS[oid] = {"id": oid, "customer": customer, "items": items, "total_cents": total_cents, "status": "pending"}
    return ORDERS[oid]


def get_order(oid):
    if oid not in ORDERS:
        raise KeyError(f"no order {oid}")
    return ORDERS[oid]


def pay(oid):
    o = get_order(oid)
    if o["status"] != "pending":
        raise ValueError("only pending orders can be paid")
    o["status"] = "paid"
    return o


def ship(oid):
    o = get_order(oid)
    if o["status"] != "paid":
        raise ValueError("only paid orders can be shipped")
    o["status"] = "shipped"
    return o


def list_orders():
    return sorted(ORDERS.values(), key=lambda o: o["id"])
