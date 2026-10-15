---
name: fastapi-templates
description: Create production-ready FastAPI projects with async patterns, dependency injection, and comprehensive error handling. Use when building new FastAPI applications or setting up backend API projects.
---

# FastAPI Project Templates

Production-ready FastAPI project structures with async patterns, dependency injection, middleware, and best practices for building high-performance APIs.

## When to Use This Skill

- Starting new FastAPI projects from scratch
- Implementing async REST APIs with Python
- Building high-performance web services and microservices
- Creating async applications with PostgreSQL, MongoDB
- Setting up API projects with proper structure and testing

## Core Concepts

### 1. Project Structure

**Recommended Layout:**

```
app/
├── api/                    # API routes
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── users.py
│   │   │   ├── auth.py
│   │   │   └── items.py
│   │   └── router.py
│   └── dependencies.py     # Shared dependencies
├── core/                   # Core configuration
│   ├── config.py
│   ├── security.py
│   └── database.py
├── models/                 # Database models
│   ├── user.py
│   └── item.py
├── schemas/                # Pydantic schemas
│   ├── user.py
│   └── item.py
├── services/               # Business logic
│   ├── user_service.py
│   └── auth_service.py
├── repositories/           # Data access
│   ├── user_repository.py
│   └── item_repository.py
└── main.py                 # Application entry
```

### 2. Dependency Injection

FastAPI's built-in DI system using `Depends`:

- Database session management
- Authentication/authorization
- Shared business logic
- Configuration injection

### 3. Async Patterns

Proper async/await usage:

- Async route handlers
- Async database operations
- Async background tasks
- Async middleware

### 4. Dependencies

The packages the examples import:

```text
# requirements.txt
fastapi
uvicorn[standard]
pydantic-settings
sqlalchemy[asyncio]>=2.0  # DeclarativeBase; [asyncio] installs greenlet for the async engine
asyncpg                   # PostgreSQL driver: postgresql+asyncpg://...
PyJWT
pwdlib[argon2]
python-multipart          # only for a login route that uses OAuth2PasswordRequestForm

# requirements-dev.txt
pytest
pytest-asyncio
httpx
aiosqlite                 # test database: sqlite+aiosqlite:///:memory:
```

## Detailed worked examples and patterns

Detailed sections (starting with `## Implementation Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

## Testing

```python
# tests/conftest.py
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import get_db, Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Async fixtures need pytest_asyncio.fixture in pytest-asyncio's default strict mode
@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with AsyncSessionLocal() as session:
        yield session
    await engine.dispose()

@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # httpx 0.28 removed AsyncClient(app=...); use an ASGI transport
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
```
