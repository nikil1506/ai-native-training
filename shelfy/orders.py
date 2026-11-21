from .inventory import Inventory
from .pricing import total_with_tax


def place_order(inv: Inventory, items: list[tuple[str, int, float]]) -> float:
    """items: (sku, qty, unit_price). Returns total incl. tax."""
    subtotal = 0.0
    for sku, qty, unit_price in items:
        inv.remove(sku, qty)
        subtotal += qty * unit_price
    return total_with_tax(subtotal)
