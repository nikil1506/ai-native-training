import re

SKU_RE = re.compile(r"^[A-Z]{3}-\d{4}$")


def validate_sku(sku: str) -> bool:
    """SKUs look like ABC-1234."""
    return bool(SKU_RE.match(sku))


def validate_quantity(qty) -> bool:
    return isinstance(qty, int) and qty > 0
