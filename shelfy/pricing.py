def apply_discount(price: float, pct: float) -> float:
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    return round(price * (100 - pct) / 100, 2)


def total_with_tax(subtotal: float, rate: float = 0.08) -> float:
    return round(subtotal * (1 + rate), 2)
