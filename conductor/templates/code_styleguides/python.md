# Python Style Guide

Python conventions following PEP 8 and modern best practices.

## PEP 8 Fundamentals

### Naming Conventions

```python
# Variables and functions: snake_case
user_name = "John"
def calculate_total(items):
    pass

# Constants: SCREAMING_SNAKE_CASE
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Classes: PascalCase
class UserAccount:
    pass

# Private: single underscore prefix
class User:
    def __init__(self):
        self._internal_state = {}

# Name mangling: double underscore prefix
class Base:
    def __init__(self):
        self.__private = "truly private"

# Module-level "private": single underscore
_module_cache = {}
```

### Indentation and Line Length

```python
# 4 spaces per indentation level
def function():
    if condition:
        do_something()

# Line length: 88 characters (Black) or 79 (PEP 8)
# Break long lines appropriately
result = some_function(
    argument_one,
    argument_two,
    argument_three,
)

# Implicit line continuation in brackets
users = [
    "alice",
    "bob",
    "charlie",
]
```

### Imports

```python
# Standard library
import os
import sys
from pathlib import Path
from typing import Optional, List

# Third-party
import requests
from pydantic import BaseModel

# Local application
from myapp.models import User
from myapp.utils import format_date

# Avoid wildcard imports
# Bad: from module import *
# Good: from module import specific_item
```

## Type Hints

### Basic Type Annotations

```python
from typing import Optional, List, Dict, Tuple, Union, Any

# Variables
name: str = "John"
age: int = 30
active: bool = True
scores: List[int] = [90, 85, 92]

# Functions
def greet(name: str) -> str:
    return f"Hello, {name}!"

def find_user(user_id: int) -> Optional[User]:
    """Returns User or None if not found."""
    pass

def process_items(items: List[str]) -> Dict[str, int]:
    """Returns count of each item."""
    pass
```

### Advanced Type Hints

```python
from typing import (
    TypeVar, Generic, Protocol, Callable,
    Literal, TypedDict, Final
)

# TypeVar for generics
T = TypeVar('T')
def first(items: List[T]) -> Optional[T]:
    return items[0] if items else None

# Protocol for structural typing
class Renderable(Protocol):
    def render(self) -> str: ...

def display(obj: Renderable) -> None:
    print(obj.render())

# Literal for specific values
Status = Literal["pending", "active", "completed"]

def set_status(status: Status) -> None:
    pass

# TypedDict for dictionary shapes
class UserDict(TypedDict):
    id: int
    name: str
    email: Optional[str]

# Final for constants
MAX_SIZE: Final = 100
```

### Type Hints in Classes

```python
from dataclasses import dataclass
from typing import ClassVar, Self

@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True

    # Class variable
    _instances: ClassVar[Dict[int, 'User']] = {}

    def deactivate(self) -> Self:
        self.active = False
        return self

class Builder:
    def __init__(self) -> None:
        self._value: str = ""

    def append(self, text: str) -> Self:
        self._value += text
        return self
```

## Docstrings

### Function Docstrings

```python
def calculate_discount(
    price: float,
    discount_percent: float,
    min_price: float = 0.0
) -> float:
    """Calculate the discounted price.

    Args:
        price: Original price of the item.
        discount_percent: Discount percentage (0-100).
        min_price: Minimum price floor. Defaults to 0.0.

    Returns:
        The discounted price, not less than min_price.

    Raises:
        ValueError: If discount_percent is not between 0 and 100.

    Example:
        >>> calculate_discount(100.0, 20.0)
        80.0
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")

    discounted = price * (1 - discount_percent / 100)
    return max(discounted, min_price)
```

### Class Docstrings

```python
class UserService:
    """Service for managing user operations.

    This service handles user CRUD operations and authentication.
    It requires a database connection and optional cache.

    Attributes:
        db: Database connection instance.
        cache: Optional cache for user lookups.

    Example:
        >>> service = UserService(db_connection)
        >>> user = service.get_user(123)
    """

    def __init__(
        self,
        db: DatabaseConnection,
        cache: Optional[Cache] = None
    ) -> None:
        """Initialize the UserService.

        Args:
            db: Active database connection.
            cache: Optional cache instance for performance.
        """
        self.db = db
        self.cache = cache
```

## Virtual Environments

### Setup Commands

```bash
# Create virtual environment
python -m venv .venv

# Activate (Unix/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt
```

### Modern Tools

```bash
# Using uv (recommended)
uv venv
uv pip install -r requirements.txt

# Using poetry
poetry init
poetry add requests
poetry install

# Using pipenv
pipenv install
pipenv install requests
```

### Project Structure

```
project/
├── .venv/               # Virtual environment (gitignored)
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── pyproject.toml       # Modern project config
├── requirements.txt     # Pinned dependencies
└── README.md
```

## Testing

### pytest Basics

```python
import pytest
from myapp.calculator import add, divide

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-1, -1) == -2

def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

# Parametrized tests
@pytest.mark.parametrize("a,b,expected", [
    (1, 1, 2),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add_parametrized(a, b, expected):
    assert add(a, b) == expected
```

### Fixtures

```python
import pytest
from myapp.database import Database
from myapp.models import User

@pytest.fixture
def db():
    """Provide a clean database for each test."""
    database = Database(":memory:")
    database.create_tables()
    yield database
    database.close()

@pytest.fixture
def sample_user(db):
    """Create a sample user in the database."""
    user = User(name="Test User", email="test@example.com")
    db.save(user)
    return user

def test_user_creation(db, sample_user):
    found = db.find_user(sample_user.id)
    assert found.name == "Test User"
```

### Mocking

```python
from unittest.mock import Mock, patch, MagicMock
import pytest

def test_api_client_with_mock():
    # Create mock
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "Test"}
    mock_response.status_code = 200

    with patch('requests.get', return_value=mock_response) as mock_get:
        result = fetch_user(1)

        mock_get.assert_called_once_with('/users/1')
        assert result['name'] == "Test"

@patch('myapp.service.external_api')
def test_with_patch_decorator(mock_api):
    mock_api.get_data.return_value = {"status": "ok"}
    result = process_data()
    assert result["status"] == "ok"
```

## Error Handling

### Exception Patterns

```python
# Define custom exceptions
class AppError(Exception):
    """Base exception for application errors."""
    pass

class ValidationError(AppError):
    """Raised when validation fails."""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """Raised when a resource is not found."""
    def __init__(self, resource: str, identifier: Any):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} '{identifier}' not found")
```

### Exception Handling

```python
def get_user(user_id: int) -> User:
    try:
        user = db.find_user(user_id)
        if user is None:
            raise NotFoundError("User", user_id)
        return user
    except DatabaseError as e:
        logger.error(f"Database error: {e}")
        raise AppError("Unable to fetch user") from e

# Context managers for cleanup
from contextlib import contextmanager

@contextmanager
def database_transaction(db):
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
```

## Common Patterns

### Dataclasses

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    id: int
    name: str
    email: str
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.email = self.email.lower()

@dataclass(frozen=True)
class Point:
    """Immutable point."""
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5
```

### Context Managers

```python
from contextlib import contextmanager
from typing import Generator

@contextmanager
def timer(name: str) -> Generator[None, None, None]:
    """Time a block of code."""
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{name}: {elapsed:.3f}s")

# Usage
with timer("data processing"):
    process_large_dataset()

# Class-based context manager
class DatabaseConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    def __enter__(self):
        self.connection = connect(self.connection_string)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
        return False  # Don't suppress exceptions
```

### Decorators

```python
from functools import wraps
from typing import Callable, TypeVar, ParamSpec
import time

P = ParamSpec('P')
R = TypeVar('R')

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def fetch_data(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

## Code Quality Tools

### Ruff Configuration

```toml
# pyproject.toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = ["E501"]  # Line too long (handled by formatter)

[tool.ruff.lint.isort]
known-first-party = ["myapp"]
```

### Type Checking with mypy

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true
```
