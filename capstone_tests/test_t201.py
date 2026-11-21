import unittest
from shelfy.validators import validate_sku
class T(unittest.TestCase):
    def test_trailing_newline(self):
        self.assertFalse(validate_sku("ABC-1234\n"))
