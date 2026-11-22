from dataclasses import dataclass, field


@dataclass
class LineItem:
    sku: str
    unit_cents: int
    quantity: int = 1


@dataclass
class Order:
    items: list[LineItem] = field(default_factory=list)
    tax_rate_percent: int = 0
