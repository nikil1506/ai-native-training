import unittest
from shelfy.inventory import Inventory
class T(unittest.TestCase):
    def test_inclusive(self):
        inv = Inventory(); inv.add("ABC-1234", 5)
        self.assertEqual(inv.low_stock(5), ["ABC-1234"])
