import unittest
from shelfy.inventory import Inventory
from shelfy.orders import place_order
class T(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            place_order(Inventory(), [])
