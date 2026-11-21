import unittest
from report import average_order_value, compute_tax


class T(unittest.TestCase):
    def test_average(self):
        orders = [{"total": 10.0}, {"total": 20.0}]
        average_order_value(orders)

    def test_tax(self):
        self.assertEqual(compute_tax(100), 20.0)
