"""A small shopping-cart service. It has three bugs (easy, medium, tricky). Failing tests show them."""


class Cart:
    def __init__(self):
        self.items = {}          # sku -> (unit_price_cents, qty)

    def add(self, sku, unit_price_cents, qty=1):
        # BUG 1 (easy): adding the same sku twice replaces the quantity instead of adding to it
        self.items[sku] = (unit_price_cents, qty)

    def subtotal_cents(self):
        return sum(p * q for p, q in self.items.values())


def apply_coupon(subtotal_cents, percent, min_spend_cents=0):
    """percent off, only when subtotal >= min_spend. Returns the new subtotal in cents."""
    # BUG 2 (medium): the minimum-spend rule is checked with > instead of >= and the discount is
    # applied with integer division that truncates toward the wrong side for odd amounts
    if subtotal_cents > min_spend_cents:
        return subtotal_cents - subtotal_cents * percent // 100
    return subtotal_cents


def split_bill(total_cents, people):
    """Split a total between people so the shares add up EXACTLY to the total."""
    # BUG 3 (tricky): every share is rounded down, so cents go missing (e.g. 1000 / 3)
    share = total_cents // people
    return [share] * people
