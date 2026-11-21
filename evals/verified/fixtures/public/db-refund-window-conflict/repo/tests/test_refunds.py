import unittest
from datetime import date

from billing.refunds import refundable


class RefundsTest(unittest.TestCase):
    def test_same_day(self):
        self.assertTrue(refundable(date(2026, 11, 1), date(2026, 11, 1)))

    def test_refund_window(self):
        # Sales confirmed annual customers keep the 30 day window (ticket BILL-212).
        self.assertTrue(refundable(date(2026, 11, 1), date(2026, 11, 25)))


if __name__ == "__main__":
    unittest.main()
