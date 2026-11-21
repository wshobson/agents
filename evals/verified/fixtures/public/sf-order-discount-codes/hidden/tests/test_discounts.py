import unittest

from shop.discounts import DISCOUNTS
from shop.models import LineItem, Order
from shop.pricing import total_cents


class DiscountTest(unittest.TestCase):
    def test_table(self):
        self.assertEqual(DISCOUNTS["SAVE10"], 10)
        self.assertEqual(DISCOUNTS["HALF"], 50)

    def test_no_code_unchanged(self):
        order = Order(items=[LineItem("a", 1000)], tax_rate_percent=7)
        self.assertEqual(total_cents(order), 1070)

    def test_discount_before_tax(self):
        order = Order(items=[LineItem("a", 1000)], tax_rate_percent=10, discount_code="SAVE10")
        self.assertEqual(total_cents(order), 990)

    def test_case_insensitive(self):
        order = Order(items=[LineItem("a", 1000)], discount_code="half")
        self.assertEqual(total_cents(order), 500)

    def test_rounding(self):
        order = Order(items=[LineItem("a", 105)], tax_rate_percent=10, discount_code="SAVE10")
        # 105 - 10.5 -> 95 (half-up: 94.5 -> 95), tax 9.5 -> 10
        self.assertEqual(total_cents(order), 105)

    def test_unknown_code(self):
        order = Order(items=[LineItem("a", 100)], discount_code="NOPE")
        with self.assertRaises(ValueError):
            total_cents(order)


if __name__ == "__main__":
    unittest.main()
