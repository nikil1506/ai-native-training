import unittest
from shelfy.inventory import Inventory
from shelfy.orders import place_order


class T(unittest.TestCase):
    def test_add_remove(self):
        inv = Inventory(); inv.add("ABC-1234", 10); inv.remove("ABC-1234", 4)
        self.assertEqual(inv.get("ABC-1234"), 6)

    def test_oversell(self):
        inv = Inventory(); inv.add("ABC-1234", 1)
        with self.assertRaises(ValueError):
            inv.remove("ABC-1234", 2)

    def test_order(self):
        inv = Inventory(); inv.add("ABC-1234", 5)
        self.assertEqual(place_order(inv, [("ABC-1234", 2, 10.0)]), 21.6)
