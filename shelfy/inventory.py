from .validators import validate_sku, validate_quantity


class Inventory:
    def __init__(self):
        self._stock: dict[str, int] = {}

    def add(self, sku: str, qty: int) -> None:
        if not validate_sku(sku):
            raise ValueError(f"invalid sku: {sku!r}")
        if not validate_quantity(qty):
            raise ValueError("quantity must be a positive int")
        self._stock[sku] = self._stock.get(sku, 0) + qty

    def remove(self, sku: str, qty: int) -> None:
        self._stock[sku] -= qty

    def get(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def low_stock(self, threshold: int = 5) -> list[str]:
        return sorted(s for s, q in self._stock.items() if q < threshold)

    def bulk_add(self, rows: list[tuple[str, int]]) -> None:
        for sku, qty in rows:
            self.add(sku, qty)
