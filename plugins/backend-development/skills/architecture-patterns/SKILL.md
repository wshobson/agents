---
name: architecture-patterns
description: Implement proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design. Use this skill when designing clean architecture for a new microservice, when refactoring a monolith to use bounded contexts, when implementing hexagonal or onion architecture patterns, or when debugging dependency cycles between application layers.
---

# Architecture Patterns

Master proven backend architecture patterns including Clean Architecture, Hexagonal Architecture, and Domain-Driven Design to build maintainable, testable, and scalable systems.

**Given:** a service boundary or module to architect.
**Produces:** layered structure with clear dependency rules, interface definitions, and test boundaries.

## When to Use This Skill

- Designing new backend services or microservices from scratch
- Refactoring monolithic applications where business logic is entangled with ORM models or HTTP concerns
- Establishing bounded contexts before splitting a system into services
- Debugging dependency cycles where infrastructure code bleeds into the domain layer
- Creating testable codebases where use-case tests do not require a running database
- Implementing domain-driven design tactical patterns (aggregates, value objects, domain events)

## Core Concepts

### 1. Clean Architecture (Uncle Bob)

**Layers (dependency flows inward):**

- **Entities**: Core business models, no framework imports
- **Use Cases**: Application business rules, orchestrate entities
- **Interface Adapters**: Controllers, presenters, gateways — translate between use cases and external formats
- **Frameworks & Drivers**: UI, database, external services — all at the outermost ring

**Key Principles:**

- Dependencies point inward only; inner layers know nothing about outer layers
- Business logic is independent of frameworks, databases, and delivery mechanisms
- Every layer boundary is crossed via an abstract interface
- Testable without UI, database, or external services

### 2. Hexagonal Architecture (Ports and Adapters)

**Components:**

- **Domain Core**: Business logic lives here, framework-free
- **Ports**: Abstract interfaces that define how the core interacts with the outside world (driving and driven)
- **Adapters**: Concrete implementations of ports (PostgreSQL adapter, Stripe adapter, REST adapter)

**Benefits:**

- Swap implementations without touching the core (e.g., replace PostgreSQL with DynamoDB)
- Use in-memory adapters in tests — no Docker required
- Technology decisions deferred to the edges

### 3. Domain-Driven Design (DDD)

**Strategic Patterns:**

- **Bounded Contexts**: Isolate a coherent model for one subdomain; avoid sharing a single model across the whole system
- **Context Mapping**: Define how contexts relate (Anti-Corruption Layer, Shared Kernel, Open Host Service)
- **Ubiquitous Language**: Every term in code matches the term used by domain experts

**Tactical Patterns:**

- **Entities**: Objects with stable identity that change over time
- **Value Objects**: Immutable objects identified by their attributes (Email, Money, Address)
- **Aggregates**: Consistency boundaries; only the root is accessible from outside
- **Repositories**: Persist and reconstitute aggregates; abstract over the storage mechanism
- **Domain Events**: Capture things that happened inside the domain; used for cross-aggregate coordination

## Clean Architecture — Directory Structure

```
app/
├── domain/           # Entities, value objects, interfaces
│   ├── entities/
│   │   ├── user.py
│   │   └── order.py
│   ├── value_objects/
│   │   ├── email.py
│   │   └── money.py
│   └── interfaces/   # Abstract ports (no implementations)
│       ├── user_repository.py
│       └── payment_gateway.py
├── use_cases/        # Application business rules
│   ├── create_user.py
│   ├── process_order.py
│   └── send_notification.py
├── adapters/         # Concrete implementations
│   ├── repositories/
│   │   ├── postgres_user_repository.py
│   │   └── redis_cache_repository.py
│   ├── controllers/
│   │   └── user_controller.py
│   └── gateways/
│       ├── stripe_payment_gateway.py
│       └── sendgrid_email_gateway.py
└── infrastructure/   # Framework wiring, config, DI container
    ├── database.py
    ├── config.py
    └── logging.py
```

**Dependency rule in one sentence:** every `import` statement in `domain/` and `use_cases/` must point only toward `domain/`; nothing in those layers may import from `adapters/` or `infrastructure/`.

## Clean Architecture — Core Implementation

```python
# domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    """Core user entity — no framework dependencies."""
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True

    def deactivate(self):
        self.is_active = False

    def can_place_order(self) -> bool:
        return self.is_active


# domain/interfaces/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User

class IUserRepository(ABC):
    """Port: defines contract, no implementation details."""

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, user_id: str) -> bool: ...


# use_cases/create_user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid
from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository

@dataclass
class CreateUserRequest:
    email: str
    name: str

@dataclass
class CreateUserResponse:
    user: Optional[User]
    success: bool
    error: Optional[str] = None

class CreateUserUseCase:
    """Use case: orchestrates business logic, no HTTP or DB details."""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(user=None, success=False, error="Email already exists")

        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            name=request.name,
            created_at=datetime.now(),
        )
        saved_user = await self.user_repository.save(user)
        return CreateUserResponse(user=saved_user, success=True)


# adapters/repositories/postgres_user_repository.py
from domain.interfaces.user_repository import IUserRepository
from domain.entities.user import User
from typing import Optional
import asyncpg

class PostgresUserRepository(IUserRepository):
    """Adapter: PostgreSQL implementation of the user port."""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
            return self._to_entity(row) if row else None

    async def find_by_email(self, email: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM users WHERE email = $1", email)
            return self._to_entity(row) if row else None

    async def save(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (id, email, name, created_at, is_active)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (id) DO UPDATE
                SET email = $2, name = $3, is_active = $5
                """,
                user.id, user.email, user.name, user.created_at, user.is_active,
            )
        return user

    async def delete(self, user_id: str) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute("DELETE FROM users WHERE id = $1", user_id)
            return result == "DELETE 1"

    def _to_entity(self, row) -> User:
        return User(
            id=row["id"], email=row["email"], name=row["name"],
            created_at=row["created_at"], is_active=row["is_active"],
        )


# adapters/controllers/user_controller.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from use_cases.create_user import CreateUserUseCase, CreateUserRequest

router = APIRouter()

class CreateUserDTO(BaseModel):
    email: str
    name: str

@router.post("/users")
async def create_user(
    dto: CreateUserDTO,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
):
    """Controller handles HTTP only — no business logic lives here."""
    response = await use_case.execute(CreateUserRequest(email=dto.email, name=dto.name))
    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)
    return {"user": response.user}
```

## Hexagonal Architecture — Ports and Adapters

```python
# Core domain service — no infrastructure dependencies
class OrderService:
    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        payment_gateway: PaymentGatewayPort,
        notification_service: NotificationPort,
    ):
        self.orders = order_repository
        self.payments = payment_gateway
        self.notifications = notification_service

    async def place_order(self, order: Order) -> OrderResult:
        if not order.is_valid():
            return OrderResult(success=False, error="Invalid order")

        payment = await self.payments.charge(amount=order.total, customer=order.customer_id)
        if not payment.success:
            return OrderResult(success=False, error="Payment failed")

        order.mark_as_paid()
        saved_order = await self.orders.save(order)
        await self.notifications.send(
            to=order.customer_email,
            subject="Order confirmed",
            body=f"Order {order.id} confirmed",
        )
        return OrderResult(success=True, order=saved_order)


# Ports (driving and driven interfaces)
class OrderRepositoryPort(ABC):
    @abstractmethod
    async def save(self, order: Order) -> Order: ...

class PaymentGatewayPort(ABC):
    @abstractmethod
    async def charge(self, amount: Money, customer: str) -> PaymentResult: ...

class NotificationPort(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, body: str): ...


# Production adapter: Stripe
class StripePaymentAdapter(PaymentGatewayPort):
    def __init__(self, api_key: str):
        import stripe
        stripe.api_key = api_key
        self._stripe = stripe

    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        try:
            charge = self._stripe.Charge.create(
                amount=amount.cents, currency=amount.currency, customer=customer
            )
            return PaymentResult(success=True, transaction_id=charge.id)
        except self._stripe.error.CardError as e:
            return PaymentResult(success=False, error=str(e))


# Test adapter: no external dependencies
class MockPaymentAdapter(PaymentGatewayPort):
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        return PaymentResult(success=True, transaction_id="mock-txn-123")
```

## DDD — Value Objects and Aggregates

```python
# Value Objects: immutable, validated at construction
from dataclasses import dataclass

@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if "@" not in self.value or "." not in self.value.split("@")[-1]:
            raise ValueError(f"Invalid email: {self.value}")

@dataclass(frozen=True)
class Money:
    amount: int   # cents
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        if self.currency not in {"USD", "EUR", "GBP"}:
            raise ValueError(f"Unsupported currency: {self.currency}")

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)


# Aggregate root: enforces all invariants for its cluster of entities
class Order:
    def __init__(self, id: str, customer_id: str):
        self.id = id
        self.customer_id = customer_id
        self.items: list[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._events: list[DomainEvent] = []

    def add_item(self, product: Product, quantity: int):
        if self.status != OrderStatus.PENDING:
            raise ValueError("Cannot modify a submitted order")
        item = OrderItem(product=product, quantity=quantity)
        self.items.append(item)
        self._events.append(ItemAddedEvent(order_id=self.id, item=item))

    @property
    def total(self) -> Money:
        totals = [item.subtotal() for item in self.items]
        return sum(totals[1:], totals[0]) if totals else Money(0, "USD")

    def submit(self):
        if not self.items:
            raise ValueError("Cannot submit an empty order")
        if self.status != OrderStatus.PENDING:
            raise ValueError("Order already submitted")
        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(order_id=self.id))

    def pop_events(self) -> list[DomainEvent]:
        events, self._events = self._events, []
        return events


# Repository: persist and reconstitute aggregates
class OrderRepository(ABC):
    @abstractmethod
    async def find_by_id(self, order_id: str) -> Optional[Order]: ...

    @abstractmethod
    async def save(self, order: Order) -> None: ...
    # Implementations persist events via pop_events() after writing state
```

## Testing — In-Memory Adapters

The hallmark of correctly applied Clean Architecture is that every use case can be exercised in a plain unit test with no real database, no Docker, and no network:

```python
# tests/unit/test_create_user.py
import asyncio
from typing import Dict, Optional
from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from use_cases.create_user import CreateUserUseCase, CreateUserRequest


class InMemoryUserRepository(IUserRepository):
    def __init__(self):
        self._store: Dict[str, User] = {}

    async def find_by_id(self, user_id: str) -> Optional[User]:
        return self._store.get(user_id)

    async def find_by_email(self, email: str) -> Optional[User]:
        return next((u for u in self._store.values() if u.email == email), None)

    async def save(self, user: User) -> User:
        self._store[user.id] = user
        return user

    async def delete(self, user_id: str) -> bool:
        return self._store.pop(user_id, None) is not None


async def test_create_user_succeeds():
    repo = InMemoryUserRepository()
    use_case = CreateUserUseCase(user_repository=repo)

    response = await use_case.execute(CreateUserRequest(email="alice@example.com", name="Alice"))

    assert response.success
    assert response.user.email == "alice@example.com"
    assert response.user.id is not None


async def test_duplicate_email_rejected():
    repo = InMemoryUserRepository()
    use_case = CreateUserUseCase(user_repository=repo)

    await use_case.execute(CreateUserRequest(email="alice@example.com", name="Alice"))
    response = await use_case.execute(CreateUserRequest(email="alice@example.com", name="Alice2"))

    assert not response.success
    assert "already exists" in response.error
```

## Troubleshooting

### Use case tests require a running database

Business logic has leaked into the infrastructure layer. Move all database calls behind an `IRepository` interface and inject an in-memory implementation in tests (see Testing section above). The use case constructor must accept the abstract port, not the concrete class.

### Circular imports between layers

A common symptom is `ImportError: cannot import name X` between `use_cases` and `adapters`. This happens when a use case imports a concrete adapter class instead of the abstract port. Enforce the rule: `use_cases/` imports only from `domain/` (entities and interfaces). It must never import from `adapters/` or `infrastructure/`.

### Framework decorators appearing in domain entities

If SQLAlchemy `Column()` or Pydantic `Field()` annotations appear on domain entities, the entity is no longer pure. Create a separate ORM model in `adapters/repositories/` and map to/from the domain entity in the repository's `_to_entity()` method.

### All logic ending up in controllers

When the controller grows beyond HTTP parsing and response formatting, extract the logic into a use case class. A controller method should do three things only: parse the request, call a use case, map the response.

### Value objects raising errors too late

Validate invariants in `__post_init__` (Python) or the constructor so an invalid `Email` or `Money` cannot be constructed at all. This surfaces bad data at the boundary, not deep inside business logic.

### Context bleed across bounded contexts

If the `Order` context is importing `User` entities from the `Identity` context, introduce an Anti-Corruption Layer. The `Order` context should hold its own lightweight `CustomerId` value object and only call the `Identity` context through an explicit interface.

## Advanced Patterns

For detailed DDD bounded context mapping, full multi-service project trees, Anti-Corruption Layer implementations, and Onion Architecture comparisons, see:

- [`references/advanced-patterns.md`](references/advanced-patterns.md)

## Related Skills

- `microservices-patterns` — Apply these architecture patterns when decomposing a monolith into services
- `cqrs-implementation` — Use Clean Architecture as the structural foundation for CQRS command/query separation
- `saga-orchestration` — Sagas require well-defined aggregate boundaries, which DDD tactical patterns provide
- `event-store-design` — Domain events produced by aggregates feed directly into an event store
