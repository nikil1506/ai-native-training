import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import api, orders


class T(unittest.TestCase):
    def setUp(self):
        orders.reset()

    def test_create_and_get(self):
        s, o = api.handle("POST", "/orders", {"customer": "ana", "items": ["A"], "total_cents": 500})
        self.assertEqual(s, 201)
        self.assertEqual(api.handle("GET", f"/orders/{o['id']}")[1]["status"], "pending")

    def test_pay_then_ship(self):
        _, o = api.handle("POST", "/orders", {"customer": "ana", "items": ["A"], "total_cents": 500})
        api.handle("POST", f"/orders/{o['id']}/pay")
        self.assertEqual(api.handle("POST", f"/orders/{o['id']}/ship")[1]["status"], "shipped")

    def test_cannot_ship_unpaid(self):
        _, o = api.handle("POST", "/orders", {"customer": "ana", "items": ["A"], "total_cents": 500})
        self.assertEqual(api.handle("POST", f"/orders/{o['id']}/ship")[0], 409)

    def test_missing(self):
        self.assertEqual(api.handle("GET", "/orders/99")[0], 404)


if __name__ == "__main__":
    unittest.main()
