# Service Layer Patterns

Business logic encapsulation and error handling patterns for FastAPI.

## Service Class Pattern

```python
class UserService:
    def __init__(self, session: Session):
        self._db = session

    def get_user(self, user_id: int) -> User:
        user = self._db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundError(user_id)
        return user

    def create_user(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user(user_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self._db.commit()
        self._db.refresh(user)
        return user
```

**Key principles:**
- Services receive dependencies via constructor (testable)
- Raise domain exceptions, not HTTPException
- Use Pydantic's `model_dump()` for data conversion
- `exclude_unset=True` for partial updates

## Custom Exception Handlers

### Define Domain Exceptions

```python
# exceptions.py
class AppException(Exception):
    """Base exception for application errors."""
    pass

class NotFoundError(AppException):
    def __init__(self, resource: str, id: int | str):
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} {id} not found")

class ValidationError(AppException):
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class ConflictError(AppException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
```

### Register Exception Handlers

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.resource} {exc.id} not found"}
    )

@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.message, "field": exc.field}
    )

@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content={"detail": exc.message}
    )
```

**Why this pattern:**
- Services stay HTTP-agnostic (reusable in CLI, background tasks)
- Centralized error formatting
- Consistent API responses
- Easy to test service logic

## Pydantic Settings

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # App
    DEBUG: bool = False
    SECRET_KEY: str
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # External APIs
    STRIPE_API_KEY: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### Hide Docs in Production

```python
app = FastAPI(
    title="My API",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url=None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)
```

## Standardized Error Responses

```python
from pydantic import BaseModel
from typing import Any

class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None
    field: str | None = None
    context: dict[str, Any] | None = None

class ErrorDetail(BaseModel):
    loc: list[str | int]
    msg: str
    type: str

class ValidationErrorResponse(BaseModel):
    detail: list[ErrorDetail]
```

### OpenAPI Error Documentation

```python
from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/users/{id}",
    responses={
        404: {"model": ErrorResponse, "description": "User not found"},
        422: {"model": ValidationErrorResponse, "description": "Validation error"},
    }
)
def get_user(id: int, service: UserServiceDep):
    return service.get_user(id)
```
