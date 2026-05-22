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

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

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
