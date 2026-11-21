def to_csv(stock: dict[str, int]) -> str:
    lines = ["sku,qty"] + [f"{s},{q}" for s, q in sorted(stock.items())]
    return "\n".join(lines) + "\n"
