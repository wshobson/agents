from decimal import ROUND_HALF_UP, Decimal

from shop.models import Order


def _round_cents(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def subtotal_cents(order: Order) -> int:
    return sum(item.unit_cents * item.quantity for item in order.items)


def total_cents(order: Order) -> int:
    subtotal = Decimal(subtotal_cents(order))
    tax = _round_cents(subtotal * order.tax_rate_percent / 100)
    return int(subtotal) + tax
