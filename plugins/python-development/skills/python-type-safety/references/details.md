# python-type-safety — detailed worked examples

## Advanced Patterns

### Pattern 5: Generic Repository

Create type-safe data access patterns.

```python
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")
ID = TypeVar("ID")

class Repository(ABC, Generic[T, ID]):
    """Generic repository interface."""

    @abstractmethod
    async def get(self, id: ID) -> T | None:
        """Get entity by ID."""
        ...

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save and return entity."""
        ...

    @abstractmethod
    async def delete(self, id: ID) -> bool:
        """Delete entity, return True if existed."""
        ...

class UserRepository(Repository[User, str]):
    """Concrete repository for Users with string IDs."""

    async def get(self, id: str) -> User | None:
        row = await self._db.fetchrow(
            "SELECT * FROM users WHERE id = $1", id
        )
        return User(**row) if row else None

    async def save(self, entity: User) -> User:
        ...

    async def delete(self, id: str) -> bool:
        ...
```

### Pattern 6: TypeVar with Bounds

Restrict generic parameters to specific types.

```python
from typing import TypeVar
from pydantic import BaseModel

ModelT = TypeVar("ModelT", bound=BaseModel)

def validate_and_create(model_cls: type[ModelT], data: dict) -> ModelT:
    """Create a validated Pydantic model from dict."""
    return model_cls.model_validate(data)

# Works with any BaseModel subclass
class User(BaseModel):
    name: str
    email: str

user = validate_and_create(User, {"name": "Alice", "email": "a@b.com"})
# user is typed as User

# Type error: str is not a BaseModel subclass
result = validate_and_create(str, {"name": "Alice"})  # Error!
```

### Pattern 7: Protocols for Structural Typing

Define interfaces without requiring inheritance.

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Serializable(Protocol):
    """Any class that can be serialized to/from dict."""

    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_dict(cls, data: dict) -> "Serializable":
        ...

# User satisfies Serializable without inheriting from it
class User:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(id=data["id"], name=data["name"])

def serialize(obj: Serializable) -> str:
    """Works with any Serializable object."""
    return json.dumps(obj.to_dict())

# Works - User matches the protocol
serialize(User("1", "Alice"))

# Runtime checking with @runtime_checkable
isinstance(User("1", "Alice"), Serializable)  # True
```

### Pattern 8: Common Protocol Patterns

Define reusable structural interfaces.

```python
from typing import Protocol

class Closeable(Protocol):
    """Resource that can be closed."""
    def close(self) -> None: ...

class AsyncCloseable(Protocol):
    """Async resource that can be closed."""
    async def close(self) -> None: ...

class Readable(Protocol):
    """Object that can be read from."""
    def read(self, n: int = -1) -> bytes: ...

class HasId(Protocol):
    """Object with an ID property."""
    @property
    def id(self) -> str: ...

class Comparable(Protocol):
    """Object that supports comparison."""
    def __lt__(self, other: "Comparable") -> bool: ...
    def __le__(self, other: "Comparable") -> bool: ...
```

### Pattern 9: Type Aliases

Create meaningful type names.

**Note:** The `type Alias = ...` statement syntax (PEP 695) was introduced in **Python 3.12**, not 3.10. For projects targeting earlier versions (including 3.10/3.11), use the `TypeAlias` annotation (PEP 613, available since Python 3.10).

```python
# Python 3.12+ type statement (PEP 695)
type UserId = str
type UserDict = dict[str, Any]

# Python 3.12+ type statement with generics (PEP 695)
type Handler[T] = Callable[[Request], T]
type AsyncHandler[T] = Callable[[Request], Awaitable[T]]
```

```python
# Python 3.10-3.11 style (needed for broader compatibility)
from typing import TypeAlias
from collections.abc import Callable, Awaitable

UserId: TypeAlias = str
Handler: TypeAlias = Callable[[Request], Response]
```

```python
# Usage
def register_handler(path: str, handler: Handler[Response]) -> None:
    ...
```

### Pattern 10: Callable Types

Type function parameters and callbacks.

```python
from collections.abc import Callable, Awaitable

# Sync callback
ProgressCallback = Callable[[int, int], None]  # (current, total)

# Async callback
AsyncHandler = Callable[[Request], Awaitable[Response]]

# With named parameters (using Protocol)
class OnProgress(Protocol):
    def __call__(
        self,
        current: int,
        total: int,
        *,
        message: str = "",
    ) -> None: ...

def process_items(
    items: list[Item],
    on_progress: ProgressCallback | None = None,
) -> list[Result]:
    for i, item in enumerate(items):
        if on_progress:
            on_progress(i, len(items))
        ...
```

## Configuration

### Strict Mode Checklist

For `mypy --strict` compliance:

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
no_implicit_optional = true
```

Incremental adoption goals:
- All function parameters annotated
- All return types annotated
- Class attributes annotated
- Minimize `Any` usage (acceptable for truly dynamic data)
- Generic collections use type parameters (`list[str]` not `list`)

For existing codebases, enable strict mode per-module using `# mypy: strict` or configure per-module overrides in `pyproject.toml`.
