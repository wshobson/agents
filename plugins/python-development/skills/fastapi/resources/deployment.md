# Deployment Patterns

Production deployment, logging, and project structure for FastAPI.

## Production Deployment

### Gunicorn with Uvicorn Workers

```bash
pip install uvloop gunicorn

gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --timeout 120 \
    --keep-alive 5 \
    --access-logfile - \
    --error-logfile -
```

**Worker calculation:**
```
workers = (CPU cores * 2) + 1
```

### Uvicorn Direct (Development/Single Container)

```bash
uvicorn main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --loop uvloop \
    --http httptools
```

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run with Gunicorn
CMD ["gunicorn", "main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"]
```

## Structured Logging

### Setup with structlog

```python
import structlog
import logging
from uuid import uuid4
from fastapi import Request

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()
```

### Request ID Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))

        # Bind to structlog context
        structlog.contextvars.bind_contextvars(request_id=request_id)

        # Add to request state
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response

app.add_middleware(RequestIDMiddleware)
```

### Logging in Routes

```python
@router.get("/users/{id}")
async def get_user(id: int, service: UserServiceDep):
    logger.info("fetching_user", user_id=id)
    try:
        user = service.get_user(id)
        logger.info("user_found", user_id=id, email=user.email)
        return user
    except NotFoundError:
        logger.warning("user_not_found", user_id=id)
        raise
```

**Log output:**
```json
{"event": "fetching_user", "user_id": 123, "request_id": "abc-123", "level": "info", "timestamp": "2024-01-15T10:30:00Z"}
```

## Project Structure

```
src/
├── auth/
│   ├── __init__.py
│   ├── router.py          # Auth endpoints
│   ├── schemas.py         # Pydantic models
│   ├── models.py          # SQLAlchemy models
│   ├── service.py         # Business logic
│   └── dependencies.py    # Auth dependencies
├── users/
│   ├── __init__.py
│   ├── router.py
│   ├── schemas.py
│   ├── models.py
│   └── service.py
├── core/
│   ├── __init__.py
│   ├── config.py          # Settings
│   ├── database.py        # DB setup
│   ├── exceptions.py      # Custom exceptions
│   └── logging.py         # Logging config
├── main.py                # App factory
└── __init__.py

tests/
├── conftest.py            # Fixtures
├── test_auth.py
├── test_users.py
└── __init__.py

alembic/
├── versions/
├── env.py
└── alembic.ini
```

### Module Router Registration

```python
# main.py
from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.users.router import router as users_router
from src.core.config import settings
from src.core.exceptions import register_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(
        title="My API",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
    )

    # Register routers
    app.include_router(auth_router, prefix="/auth", tags=["auth"])
    app.include_router(users_router, prefix="/users", tags=["users"])

    # Register exception handlers
    register_exception_handlers(app)

    return app

app = create_app()
```

## Environment Configuration

### .env file

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
DB_POOL_SIZE=5

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=["http://localhost:3000"]

# App
DEBUG=false
LOG_LEVEL=INFO
```

### Config validation on startup

```python
from src.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Validate settings on startup
    logger.info(
        "starting_app",
        debug=settings.DEBUG,
        db_pool_size=settings.DB_POOL_SIZE,
    )

    # Initialize connections
    yield

    # Cleanup
    logger.info("shutting_down")

app = FastAPI(lifespan=lifespan)
```

## Health Checks

```python
from fastapi import APIRouter
from sqlalchemy import text

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "healthy"}

@router.get("/health/ready")
async def readiness(db: DbDep):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "database": str(e)}
        )
```
