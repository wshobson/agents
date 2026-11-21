from pathlib import Path

Path("shop/discounts.py").write_text('DISCOUNTS = {"SAVE10": 10, "HALF": 50}\n')
m = Path("shop/models.py")
m.write_text(m.read_text() + "    discount_code: str | None = None\n")
p = Path("shop/pricing.py")
s = p.read_text()
s = s.replace(
    "from shop.models import Order",
    "from shop.discounts import DISCOUNTS\nfrom shop.models import Order",
)
s = s.replace(
    "    subtotal = Decimal(subtotal_cents(order))\n",
    """    subtotal = Decimal(subtotal_cents(order))
    if order.discount_code is not None:
        code = order.discount_code.upper()
        if code not in DISCOUNTS:
            raise ValueError(f"unknown discount code {order.discount_code}")
        subtotal = Decimal(_round_cents(subtotal * (100 - DISCOUNTS[code]) / 100))
""",
)
p.write_text(s)
print("Added discount codes.")
