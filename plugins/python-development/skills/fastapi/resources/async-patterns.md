# Async Patterns

Async library selection and common async issues in FastAPI.

## Async Library Alternatives

When using `async def` endpoints, use async-compatible libraries:

| Blocking Library | Async Alternative | Notes |
|------------------|-------------------|-------|
| `time.sleep()` | `asyncio.sleep()` | Built-in |
| `requests` | `httpx.AsyncClient` | Drop-in replacement |
| `urllib3` | `aiohttp` | Lower-level HTTP |
| `psycopg2` | `asyncpg` | PostgreSQL |
| `pymysql` | `aiomysql` | MySQL |
| `pymongo` | `motor` | MongoDB |
| `redis-py` | `aioredis` / `redis.asyncio` | Redis (redis-py 4.2+ has async) |
| `boto3` | `aioboto3` | AWS SDK |
| `paramiko` | `asyncssh` | SSH |
| `smtplib` | `aiosmtplib` | Email |

### httpx Example

```python
import httpx
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create shared client with connection pooling
    app.state.http_client = httpx.AsyncClient(
        timeout=30.0,
        limits=httpx.Limits(max_connections=100),
    )
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

@router.get("/external-data")
async def get_external_data(request: Request):
    client: httpx.AsyncClient = request.app.state.http_client
    response = await client.get("https://api.example.com/data")
    return response.json()
```

## Circular Import Solutions

### Problem

```python
# models/user.py
from models.post import Post  # Circular!

class User(Base):
    posts: Mapped[list["Post"]] = relationship()

# models/post.py
from models.user import User  # Circular!

class Post(Base):
    author: Mapped["User"] = relationship()
```

### Solution 1: Forward References with TYPE_CHECKING

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.post import Post

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
```

### Solution 2: String References in Relationships

```python
# No imports needed - use string class names
class User(Base):
    __tablename__ = "users"
    posts: Mapped[list["Post"]] = relationship(
        "Post",  # String reference
        back_populates="author"
    )

class Post(Base):
    __tablename__ = "posts"
    author: Mapped["User"] = relationship(
        "User",  # String reference
        back_populates="posts"
    )
```

### Solution 3: Pydantic model_rebuild()

For Pydantic schemas with circular references:

```python
from __future__ import annotations
from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from schemas.post import PostRead

class UserRead(BaseModel):
    id: int
    name: str
    posts: list["PostRead"] = []

# After all models are defined (e.g., in __init__.py)
from schemas.user import UserRead
from schemas.post import PostRead

UserRead.model_rebuild()
PostRead.model_rebuild()
```

### Solution 4: Centralized Models File

For smaller projects, define all models in one file:

```python
# models.py
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
```

## Running Blocking Code in Async Context

When you must use blocking code in an async endpoint:

```python
import asyncio
from functools import partial

def blocking_operation(data: str) -> str:
    # Simulating blocking I/O
    import time
    time.sleep(1)
    return f"processed: {data}"

@router.post("/process")
async def process_data(data: str):
    # Run blocking code in thread pool
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,  # Default executor
        partial(blocking_operation, data)
    )
    return {"result": result}
```

**Better approach:** Use `def` instead of `async def`:

```python
@router.post("/process")
def process_data(data: str):
    # FastAPI automatically runs in thread pool
    result = blocking_operation(data)
    return {"result": result}
```

## Async Context Managers

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_async_resource():
    resource = await create_resource()
    try:
        yield resource
    finally:
        await resource.cleanup()

@router.get("/data")
async def get_data():
    async with get_async_resource() as resource:
        return await resource.fetch_data()
```

## Concurrent Requests

```python
import asyncio

@router.get("/aggregate")
async def aggregate_data(request: Request):
    client: httpx.AsyncClient = request.app.state.http_client

    # Run multiple requests concurrently
    users, posts, comments = await asyncio.gather(
        client.get("https://api.example.com/users"),
        client.get("https://api.example.com/posts"),
        client.get("https://api.example.com/comments"),
    )

    return {
        "users": users.json(),
        "posts": posts.json(),
        "comments": comments.json(),
    }
```

### With Error Handling

```python
results = await asyncio.gather(
    fetch_users(),
    fetch_posts(),
    fetch_comments(),
    return_exceptions=True,  # Don't fail if one fails
)

users, posts, comments = [
    r if not isinstance(r, Exception) else None
    for r in results
]
```
