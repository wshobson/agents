# Advanced Architecture Patterns — Reference

Deep-dive implementation examples for DDD bounded contexts, Onion Architecture, Anti-Corruption Layers, and full project structures. Referenced from SKILL.md.

---

## Full Multi-Service Project Structure

A realistic e-commerce system organised by bounded context, each context is a deployable service:

```
ecommerce/
├── services/
│   ├── identity/                    # Bounded context: users & auth
│   │   ├── identity/
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   │   └── user.py
│   │   │   │   ├── value_objects/
│   │   │   │   │   ├── email.py
│   │   │   │   │   └── password_hash.py
│   │   │   │   └── interfaces/
│   │   │   │       └── user_repository.py
│   │   │   ├── use_cases/
│   │   │   │   ├── register_user.py
│   │   │   │   └── authenticate_user.py
│   │   │   ├── adapters/
│   │   │   │   ├── repositories/
│   │   │   │   │   └── postgres_user_repository.py
│   │   │   │   └── controllers/
│   │   │   │       └── auth_controller.py
│   │   │   └── infrastructure/
│   │   │       └── jwt_service.py
│   │   └── tests/
│   │       ├── unit/
│   │       └── integration/
│   │
│   ├── catalog/                     # Bounded context: products
│   │   ├── catalog/
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   │   └── product.py
│   │   │   │   └── value_objects/
│   │   │   │       ├── sku.py
│   │   │   │       └── price.py
│   │   │   └── use_cases/
│   │   │       ├── create_product.py
│   │   │       └── update_inventory.py
│   │   └── tests/
│   │
│   └── ordering/                    # Bounded context: orders
│       ├── ordering/
│       │   ├── domain/
│       │   │   ├── entities/
│       │   │   │   └── order.py
│       │   │   ├── value_objects/
│       │   │   │   ├── customer_id.py   # NOT imported from identity!
│       │   │   │   └── money.py
│       │   │   └── interfaces/
│       │   │       ├── order_repository.py
│       │   │       └── catalog_client.py  # ACL port to catalog context
│       │   ├── use_cases/
│       │   │   ├── place_order.py
│       │   │   └── cancel_order.py
│       │   └── adapters/
│       │       ├── acl/
│       │       │   └── catalog_http_client.py  # ACL adapter
│       │       └── repositories/
│       │           └── postgres_order_repository.py
│       └── tests/
│
├── shared/                          # Shared kernel (use sparingly)
│   └── domain_events/
│       └── base_event.py
└── docker-compose.yml
```

---

## Onion Architecture vs. Clean Architecture

Both enforce inward-pointing dependencies. The difference is terminology and layering granularity:

| Concern | Clean Architecture | Onion Architecture |
|---|---|---|
| Innermost ring | Entities | Domain Model |
| Second ring | Use Cases | Domain Services |
| Third ring | Interface Adapters | Application Services |
| Outermost ring | Frameworks & Drivers | Infrastructure / UI / Tests |
| Key insight | Controller is an adapter | Application Services = Use Cases |

Onion Architecture makes the Domain Services layer explicit — it hosts pure domain logic that spans multiple entities but has no I/O:

```python
# onion/domain/services/pricing_service.py
from domain.entities.product import Product
from domain.value_objects.money import Money
from domain.value_objects.discount import Discount

class PricingService:
    """
    Domain service: logic that doesn't belong to a single entity.
    No ports or adapters here — purely domain computation.
    """

    def apply_bulk_discount(self, product: Product, quantity: int) -> Money:
        if quantity >= 100:
            discount = Discount(percentage=20)
        elif quantity >= 50:
            discount = Discount(percentage=10)
        else:
            discount = Discount(percentage=0)
        return product.price.apply_discount(discount)

    def calculate_order_total(self, items: list[tuple[Product, int]]) -> Money:
        subtotals = [self.apply_bulk_discount(p, q) for p, q in items]
        return sum(subtotals[1:], subtotals[0]) if subtotals else Money(0, "USD")
```

---

## Anti-Corruption Layer (ACL)

When the `Ordering` context must fetch product data from the `Catalog` context, it should never use `Catalog`'s domain model directly. An ACL translates between the two models:

```python
# ordering/domain/interfaces/catalog_client.py
from abc import ABC, abstractmethod
from ordering.domain.value_objects.product_snapshot import ProductSnapshot

class CatalogClientPort(ABC):
    """
    Ordering's view of product data. Uses Ordering's own value object,
    not Catalog's Product entity.
    """

    @abstractmethod
    async def get_product_snapshot(self, sku: str) -> ProductSnapshot: ...


# ordering/domain/value_objects/product_snapshot.py
from dataclasses import dataclass
from ordering.domain.value_objects.money import Money

@dataclass(frozen=True)
class ProductSnapshot:
    """Ordering's local representation of a product at order time."""
    sku: str
    name: str
    unit_price: Money
    available: bool


# ordering/adapters/acl/catalog_http_client.py
import httpx
from ordering.domain.interfaces.catalog_client import CatalogClientPort
from ordering.domain.value_objects.product_snapshot import ProductSnapshot
from ordering.domain.value_objects.money import Money

class CatalogHttpClient(CatalogClientPort):
    """
    ACL adapter: calls Catalog's HTTP API and translates
    Catalog's response schema into Ordering's ProductSnapshot.
    """

    def __init__(self, base_url: str, http_client: httpx.AsyncClient):
        self._base_url = base_url
        self._http = http_client

    async def get_product_snapshot(self, sku: str) -> ProductSnapshot:
        response = await self._http.get(f"{self._base_url}/products/{sku}")
        response.raise_for_status()
        data = response.json()

        # Translation: Catalog speaks "price_cents" + "currency_code";
        # Ordering speaks Money(amount, currency).
        return ProductSnapshot(
            sku=data["sku"],
            name=data["title"],              # field name differs between contexts
            unit_price=Money(
                amount=data["price_cents"],
                currency=data["currency_code"],
            ),
            available=data["stock_count"] > 0,
        )


# Test ACL with a stub — no HTTP required
class StubCatalogClient(CatalogClientPort):
    def __init__(self, products: dict[str, ProductSnapshot]):
        self._products = products

    async def get_product_snapshot(self, sku: str) -> ProductSnapshot:
        if sku not in self._products:
            raise ValueError(f"Unknown SKU: {sku}")
        return self._products[sku]
```

---

## Context Map — Relationships Between Bounded Contexts

```
┌─────────────────────────────────────────────────────────────────┐
│                        E-Commerce System                         │
│                                                                  │
│   ┌─────────────┐   Open Host   ┌─────────────────────────┐    │
│   │  Identity   │──────────────▶│        Ordering          │    │
│   │  Context    │               │  (uses CustomerId VO,    │    │
│   │             │               │   not User entity)       │    │
│   └─────────────┘               └─────────────────────────┘    │
│                                          │ ACL                   │
│                                          ▼                       │
│                                 ┌─────────────────┐             │
│   ┌─────────────┐  Shared       │    Catalog      │             │
│   │  Payments   │  Kernel       │    Context      │             │
│   │  Context    │◀─────────────▶│                 │             │
│   │             │  (Money VO)   └─────────────────┘             │
│   └─────────────┘                                               │
└─────────────────────────────────────────────────────────────────┘

Relationship types:
  Open Host Service  — upstream provides a stable API for many downstream contexts
  ACL (Anti-Corruption Layer) — downstream translates upstream model to its own
  Shared Kernel     — two contexts share a small, explicitly governed sub-model
  Conformist        — downstream adopts upstream model as-is (last resort)
```

---

## Dependency Injection Wiring — Infrastructure Layer

All the abstract interfaces are wired to concrete implementations in the infrastructure layer (or a DI container). Nothing else in the codebase knows which concrete class is used:

```python
# infrastructure/container.py
from functools import lru_cache
import asyncpg
from adapters.repositories.postgres_user_repository import PostgresUserRepository
from adapters.gateways.stripe_payment_gateway import StripePaymentAdapter
from use_cases.create_user import CreateUserUseCase
from infrastructure.config import Settings

@lru_cache
def get_settings() -> Settings:
    return Settings()

async def get_db_pool() -> asyncpg.Pool:
    settings = get_settings()
    return await asyncpg.create_pool(settings.database_url)

async def get_create_user_use_case() -> CreateUserUseCase:
    pool = await get_db_pool()
    repo = PostgresUserRepository(pool=pool)
    return CreateUserUseCase(user_repository=repo)

# In tests, replace get_create_user_use_case with a version
# that injects InMemoryUserRepository — no other code changes needed.
```

---

## Aggregate Design Heuristics

Use these rules when deciding aggregate boundaries:

| Question | Guidance |
|---|---|
| Should these two objects always be consistent together? | Put them in the same aggregate. |
| Can they be eventually consistent? | Put them in separate aggregates; use domain events to sync. |
| Is one object the "owner" that controls access? | That object is the aggregate root. |
| Does removing the root make the child meaningless? | Child belongs inside the aggregate. |
| Are you loading thousands of objects to change one? | Aggregate is too large — split it. |

**Practical example — Order vs. Customer:**

```python
# Bad: Customer aggregate holds full Order objects
class Customer:
    def __init__(self):
        self._orders: list[Order] = []   # loads all orders every time

# Good: Customer holds Order IDs only; Order is its own aggregate
class Customer:
    def __init__(self):
        self._order_ids: list[str] = []  # lightweight reference

class Order:
    def __init__(self, id: str, customer_id: str):
        self.id = id
        self.customer_id = customer_id   # reference back, not the full object
```

---

## Domain Events — Publishing and Handling

Domain events decouple aggregates that need to react to each other's state changes:

```python
# domain/events/order_events.py
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class DomainEvent:
    occurred_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class OrderSubmittedEvent(DomainEvent):
    order_id: str = ""
    customer_id: str = ""
    total_cents: int = 0
    currency: str = "USD"


# adapters/event_publisher/postgres_outbox.py
# Transactional outbox pattern: write events to the same DB transaction as state
import json

class PostgresOutboxPublisher:
    """
    Writes domain events to an outbox table in the same transaction
    as the aggregate state. A separate relay process reads and publishes
    to the message broker. Guarantees at-least-once delivery.
    """

    async def publish(self, conn, events: list[DomainEvent]):
        for event in events:
            await conn.execute(
                """
                INSERT INTO outbox (event_type, payload, published_at)
                VALUES ($1, $2, NULL)
                """,
                type(event).__name__,
                json.dumps(event.__dict__, default=str),
            )


# use_cases/place_order.py — aggregate saves, events are extracted and stored
class PlaceOrderUseCase:
    def __init__(self, order_repo: OrderRepository, event_publisher: PostgresOutboxPublisher):
        self.orders = order_repo
        self.publisher = event_publisher

    async def execute(self, request: PlaceOrderRequest) -> PlaceOrderResponse:
        order = Order(id=str(uuid.uuid4()), customer_id=request.customer_id)
        for item in request.items:
            order.add_item(product=item.product, quantity=item.quantity)
        order.submit()

        async with self.db.transaction() as conn:
            await self.orders.save(order, conn)
            await self.publisher.publish(conn, order.pop_events())

        return PlaceOrderResponse(order_id=order.id, success=True)
```

---

## Detecting and Breaking Dependency Cycles

Common symptoms and their structural fixes:

```
Symptom: use_cases/create_order.py imports from adapters/email_sender.py
Fix:     Create domain/interfaces/notification_service.py (abstract port).
         use_cases imports the port. adapters implements it.
         DI container wires them together.

Symptom: domain/entities/user.py imports from infrastructure/config.py
Fix:     Pass config values as constructor arguments or environment at
         the infrastructure boundary. Domain entities must not read config.

Symptom: Two aggregates import each other
Fix:     Introduce a domain event. Aggregate A emits OrderPlaced.
         Aggregate B's use case subscribes and reacts. They never import
         each other.

Symptom: Repository imports a use case to "do extra work" after saving
Fix:     Extract the extra work into a separate domain service or use case.
         Repositories persist state only; they do not orchestrate behaviour.
```

Visual dependency check — run this and look for any arrow pointing outward:

```bash
# Install: pip install pydeps
pydeps app --max-bacon=4 --cluster --rankdir=BT
# Expected: domain has no outgoing edges to adapters or infrastructure
```
