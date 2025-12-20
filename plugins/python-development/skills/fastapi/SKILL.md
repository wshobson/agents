---
name: fastapi
description: Production-ready FastAPI patterns with progressive disclosure. Start with essential async rules and architecture, load advanced patterns as needed. Use when building, reviewing, or architecting FastAPI applications.
triggers:
  - fastapi
  - fast api
  - async api
  - python api
  - pydantic api
---

# FastAPI Production Patterns

Production-ready patterns for FastAPI applications with progressive disclosure resources.

## When to Use This Skill

- Building new FastAPI applications
- Reviewing FastAPI code for anti-patterns
- Setting up service layer architecture
- Configuring testing infrastructure
- Deploying to production

## Essential Patterns (Always Apply)

### The Async Golden Rule

**NEVER use `async def` for blocking operations.**

```python
# BAD - Blocks entire event loop
@router.get("/bad")
async def bad():
    time.sleep(10)  # FREEZES YOUR APP

# GOOD - Sync function runs in thread pool
@router.get("/good")
def good():
    time.sleep(10)  # Safe - FastAPI handles threading

# BEST - Truly async
@router.get("/best")
async def best():
    await asyncio.sleep(10)  # Non-blocking
```

**Quick Decision:**
- Blocking library (requests, psycopg2, file I/O) → use `def`
- Async library (httpx, asyncpg, motor) → use `async def`

### Nested Dependency Injection

**Chain: db → service → route** (not db → route)

```python
# Layer 1: DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Layer 2: Service depends on DB
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

# Layer 3: Route depends on Service
@router.get("/users/{id}")
def get_user(id: int, service: UserService = Depends(get_user_service)):
    return service.get_user(id)
```

**Why:** Testing requires only `app.dependency_overrides[get_db]` - services auto-get test DB.

### Annotated Dependencies

```python
from typing import Annotated

DbDep = Annotated[Session, Depends(get_db)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

@router.get("/users/{id}")
def get_user(id: int, service: UserServiceDep):
    return service.get_user(id)
```

### Pydantic Validation (Not Manual)

```python
# BAD
@router.post("/users")
async def create(data: dict):
    if len(data.get("username", "")) < 3:
        raise HTTPException(400, "Too short")

# GOOD
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr

@router.post("/users")
async def create(data: UserCreate):
    return await service.create(data)
```

### Lifespan Events (Not on_event)

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)
    yield
    # Shutdown (guaranteed)
    await app.state.pool.close()

app = FastAPI(lifespan=lifespan)
```

## Available Resources

Load specific resources based on your needs:

### Service Layer Patterns
**File**: `resources/service-layer.md`
**When to load**: Implementing business logic, exception handling, settings
**Contains**:
- Service class pattern
- Custom exception handlers
- Pydantic settings configuration
- Error response standardization

### Database Patterns
**File**: `resources/database-patterns.md`
**When to load**: SQLAlchemy setup, testing database operations
**Contains**:
- SQLAlchemy 2.0 Mapped types
- Testing with StaticPool (in-memory SQLite)
- Async testing with httpx
- Connection pooling patterns

### Deployment Patterns
**File**: `resources/deployment.md`
**When to load**: Production deployment, logging, project structure
**Contains**:
- Production Uvicorn/Gunicorn configuration
- Structured logging with structlog
- Recommended project structure
- Environment-based configuration

### Async Patterns
**File**: `resources/async-patterns.md`
**When to load**: Async library selection, circular import issues
**Contains**:
- Blocking vs async library alternatives table
- Circular import solutions
- Forward references with TYPE_CHECKING

## Quick Reference

| Do | Don't |
|----|-------|
| `def` for blocking I/O | `async def` with blocking calls |
| Nested DI (db→service→route) | DB directly in routes |
| `Annotated[T, Depends()]` | Inline `Depends()` everywhere |
| Pydantic validation | Manual if-checks |
| `lifespan` context | `@app.on_event` (deprecated) |
| Custom exceptions + handler | HTTPException in services |
| Alembic migrations | `create_all()` in prod |

## How to Use Resources

**Load specific resource when needed**:
- "Implement service layer" → Load `resources/service-layer.md`
- "Setup SQLAlchemy testing" → Load `resources/database-patterns.md`
- "Deploy to production" → Load `resources/deployment.md`
- "Fix circular imports" → Load `resources/async-patterns.md`
