import unittest

from shop.models import LineItem, Order
from shop.pricing import subtotal_cents, total_cents


class PricingTest(unittest.TestCase):
    def test_subtotal(self):
        order = Order(items=[LineItem("a", 250, 2), LineItem("b", 99)])
        self.assertEqual(subtotal_cents(order), 599)

    def test_total_with_tax(self):
        order = Order(items=[LineItem("a", 1000)], tax_rate_percent=7)
        self.assertEqual(total_cents(order), 1070)

    def test_tax_rounds_half_up(self):
        order = Order(items=[LineItem("a", 50)], tax_rate_percent=1)
        self.assertEqual(total_cents(order), 51)


if __name__ == "__main__":
    unittest.main()
