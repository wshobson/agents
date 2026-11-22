from datetime import date, timedelta

# Refund window from POLICY.md.
REFUND_WINDOW_DAYS = 14


def refundable(purchased: date, today: date) -> bool:
    return today - purchased <= timedelta(days=REFUND_WINDOW_DAYS)
