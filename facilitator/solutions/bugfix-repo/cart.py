"""Reference solution for L2."""


class Cart:
    def __init__(self):
        self.items = {}

    def add(self, sku, unit_price_cents, qty=1):
        _, have = self.items.get(sku, (unit_price_cents, 0))
        self.items[sku] = (unit_price_cents, have + qty)

    def subtotal_cents(self):
        return sum(p * q for p, q in self.items.values())


def apply_coupon(subtotal_cents, percent, min_spend_cents=0):
    if subtotal_cents >= min_spend_cents:
        return (subtotal_cents * (100 - percent) * 2 + 100) // 200   # new price, rounded half up
    return subtotal_cents


def split_bill(total_cents, people):
    base, extra = divmod(total_cents, people)
    return [base + (1 if i < extra else 0) for i in range(people)]
