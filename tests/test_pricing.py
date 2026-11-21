import unittest
from shelfy.pricing import apply_discount, total_with_tax


class T(unittest.TestCase):
    def test_discount(self):
        self.assertEqual(apply_discount(100, 10), 90.0)

    def test_bad_pct(self):
        with self.assertRaises(ValueError):
            apply_discount(100, 120)

    def test_tax(self):
        self.assertEqual(total_with_tax(100), 108.0)
