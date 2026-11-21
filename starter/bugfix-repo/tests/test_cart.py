import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from service.cart import Cart, apply_coupon, split_bill


class CartTests(unittest.TestCase):
    def test_adding_same_sku_accumulates_quantity(self):          # bug 1
        c = Cart(); c.add("A", 500, 2); c.add("A", 500, 3)
        self.assertEqual(c.subtotal_cents(), 2500)

    def test_distinct_skus(self):
        c = Cart(); c.add("A", 100); c.add("B", 250, 2)
        self.assertEqual(c.subtotal_cents(), 600)


class CouponTests(unittest.TestCase):
    def test_min_spend_is_inclusive(self):                         # bug 2
        self.assertEqual(apply_coupon(5000, 10, min_spend_cents=5000), 4500)

    def test_discount_rounds_to_nearest_cent(self):                # bug 2
        self.assertEqual(apply_coupon(999, 15), 849)               # 999*0.85 = 849.15 -> 849
        self.assertEqual(apply_coupon(1005, 10), 905)              # 904.5 -> 905 (round half up)

    def test_below_min_spend_unchanged(self):
        self.assertEqual(apply_coupon(4999, 10, min_spend_cents=5000), 4999)


class SplitTests(unittest.TestCase):
    def test_shares_sum_to_total(self):                            # bug 3
        for total, n in [(1000, 3), (1001, 4), (7, 5), (100, 1)]:
            self.assertEqual(sum(split_bill(total, n)), total, (total, n))

    def test_shares_differ_by_at_most_one_cent(self):
        s = split_bill(1000, 3)
        self.assertLessEqual(max(s) - min(s), 1)


if __name__ == "__main__":
    unittest.main()
