# python-resilience — detailed worked examples

## Advanced Patterns

### Pattern 5: Logging Retry Attempts

Track retry behavior for debugging and alerting.

```python
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

logger = structlog.get_logger()

def log_retry_attempt(retry_state):
    """Log detailed retry information."""
    exception = retry_state.outcome.exception()
    logger.warning(
        "Retrying operation",
        attempt=retry_state.attempt_number,
        exception_type=type(exception).__name__,
        exception_message=str(exception),
        next_wait_seconds=retry_state.next_action.sleep if retry_state.next_action else None,
    )

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, max=10),
    before_sleep=log_retry_attempt,
)
def call_with_logging(request: dict) -> dict:
    """External call with retry logging."""
    ...
```

### Pattern 6: Timeout Decorator

Create reusable timeout decorators for consistent timeout handling.

```python
import asyncio
from functools import wraps
from typing import TypeVar, Callable

T = TypeVar("T")

def with_timeout(seconds: float):
    """Decorator to add timeout to async functions."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            return await asyncio.wait_for(
                func(*args, **kwargs),
                timeout=seconds,
            )
        return wrapper
    return decorator

@with_timeout(30)
async def fetch_with_timeout(url: str) -> dict:
    """Fetch URL with 30 second timeout."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Pattern 7: Cross-Cutting Concerns via Decorators

Stack decorators to separate infrastructure from business logic.

```python
from functools import wraps
from typing import TypeVar, Callable
import structlog

logger = structlog.get_logger()
T = TypeVar("T")

def traced(name: str | None = None):
    """Add tracing to function calls."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        span_name = name or func.__name__

        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            logger.info("Operation started", operation=span_name)
            try:
                result = await func(*args, **kwargs)
                logger.info("Operation completed", operation=span_name)
                return result
            except Exception as e:
                logger.error("Operation failed", operation=span_name, error=str(e))
                raise
        return wrapper
    return decorator

# Stack multiple concerns
@traced("fetch_user_data")
@with_timeout(30)
@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter())
async def fetch_user_data(user_id: str) -> dict:
    """Fetch user with tracing, timeout, and retry."""
    ...
```

### Pattern 8: Dependency Injection for Testability

Pass infrastructure components through constructors for easy testing.

```python
from dataclasses import dataclass
from typing import Protocol

class Logger(Protocol):
    def info(self, msg: str, **kwargs) -> None: ...
    def error(self, msg: str, **kwargs) -> None: ...

class MetricsClient(Protocol):
    def increment(self, metric: str, tags: dict | None = None) -> None: ...
    def timing(self, metric: str, value: float) -> None: ...

@dataclass
class UserService:
    """Service with injected infrastructure."""

    repository: UserRepository
    logger: Logger
    metrics: MetricsClient

    async def get_user(self, user_id: str) -> User:
        self.logger.info("Fetching user", user_id=user_id)
        start = time.perf_counter()

        try:
            user = await self.repository.get(user_id)
            self.metrics.increment("user.fetch.success")
            return user
        except Exception as e:
            self.metrics.increment("user.fetch.error")
            self.logger.error("Failed to fetch user", user_id=user_id, error=str(e))
            raise
        finally:
            elapsed = time.perf_counter() - start
            self.metrics.timing("user.fetch.duration", elapsed)

# Easy to test with fakes
service = UserService(
    repository=FakeRepository(),
    logger=FakeLogger(),
    metrics=FakeMetrics(),
)
```

### Pattern 9: Fail-Safe Defaults

Degrade gracefully when non-critical operations fail.

```python
from typing import TypeVar
from collections.abc import Callable

T = TypeVar("T")

def fail_safe(default: T, log_failure: bool = True):
    """Return default value on failure instead of raising."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if log_failure:
                    logger.warning(
                        "Operation failed, using default",
                        function=func.__name__,
                        error=str(e),
                    )
                return default
        return wrapper
    return decorator

@fail_safe(default=[])
async def get_recommendations(user_id: str) -> list[str]:
    """Get recommendations, return empty list on failure."""
    ...
```
