# Database Patterns

SQLAlchemy 2.0 setup and testing patterns for FastAPI.

## SQLAlchemy 2.0 Models

```python
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author: Mapped["User"] = relationship(back_populates="posts")
```

**SQLAlchemy 2.0 changes:**
- `Mapped[T]` for type hints
- `mapped_column()` instead of `Column()`
- Native Python types, not SQLAlchemy types
- Better IDE support and type checking

## Database Session Setup

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections before use
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Testing with StaticPool

Use in-memory SQLite with StaticPool for fast, isolated tests:

```python
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# Test engine with StaticPool (shares connection across threads)
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create tables and provide test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    """Override get_db dependency with test database."""
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

**Why StaticPool:**
- Single connection shared across all operations
- Required for SQLite in-memory with multiple threads
- Fast test execution (no connection overhead)

## Async Testing with httpx

```python
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_get_users(async_client):
    response = await async_client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_user(async_client):
    response = await async_client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test User"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

## Async SQLAlchemy

For fully async applications:

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

### Async Query Patterns

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_user_with_posts(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(
        select(User)
        .options(selectinload(User.posts))
        .where(User.id == user_id)
    )
    return result.scalar_one_or_none()

async def get_users_paginated(
    db: AsyncSession, skip: int = 0, limit: int = 20
) -> list[User]:
    result = await db.execute(
        select(User)
        .offset(skip)
        .limit(limit)
        .order_by(User.created_at.desc())
    )
    return list(result.scalars().all())
```

## Connection Pooling Best Practices

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Maintained connections
    max_overflow=10,       # Extra connections when needed
    pool_timeout=30,       # Wait time for connection
    pool_recycle=1800,     # Recycle connections after 30 min
    pool_pre_ping=True,    # Verify connection before use
)
```

**Guidelines:**
- `pool_size`: Match expected concurrent requests
- `max_overflow`: Allow burst capacity
- `pool_pre_ping`: Prevents stale connection errors
- `pool_recycle`: Prevents connection timeouts (especially MySQL)
