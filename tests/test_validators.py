import unittest
from shelfy.validators import validate_sku, validate_quantity


class T(unittest.TestCase):
    def test_sku_ok(self):
        self.assertTrue(validate_sku("ABC-1234"))

    def test_sku_bad(self):
        self.assertFalse(validate_sku("abc-1234"))

    def test_qty(self):
        self.assertTrue(validate_quantity(3))
        self.assertFalse(validate_quantity(0))
