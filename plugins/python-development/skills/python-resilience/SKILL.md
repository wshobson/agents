---
name: python-resilience
description: Python resilience patterns including automatic retries, exponential backoff, timeouts, and fault-tolerant decorators. Use when adding retry logic, implementing timeouts, building fault-tolerant services, or handling transient failures.
---

# Python Resilience Patterns

Build fault-tolerant Python applications that gracefully handle transient failures, network issues, and service outages. Resilience patterns keep systems running when dependencies are unreliable.

## When to Use This Skill

- Adding retry logic to external service calls
- Implementing timeouts for network operations
- Building fault-tolerant microservices
- Handling rate limiting and backpressure
- Creating infrastructure decorators
- Designing circuit breakers

## Core Concepts

### 1. Transient vs Permanent Failures

Retry transient errors (network timeouts, temporary service issues). Don't retry permanent errors (invalid credentials, bad requests).

### 2. Exponential Backoff

Increase wait time between retries to avoid overwhelming recovering services.

### 3. Jitter

Add randomness to backoff to prevent thundering herd when many clients retry simultaneously.

### 4. Bounded Retries

Cap both attempt count and total duration to prevent infinite retry loops.

## Quick Start

```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def call_external_service(request: dict) -> dict:
    return httpx.post("https://api.example.com", json=request).json()
```

## Fundamental Patterns

### Pattern 1: Basic Retry with Tenacity

Use the `tenacity` library for production-grade retry logic. For simpler cases, consider built-in retry functionality or a lightweight custom implementation.

```python
from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential_jitter,
    retry_if_exception_type,
)

TRANSIENT_ERRORS = (ConnectionError, TimeoutError, OSError)

@retry(
    retry=retry_if_exception_type(TRANSIENT_ERRORS),
    stop=stop_after_attempt(5) | stop_after_delay(60),
    wait=wait_exponential_jitter(initial=1, max=30),
)
def fetch_data(url: str) -> dict:
    """Fetch data with automatic retry on transient failures."""
    response = httpx.get(url, timeout=30)
    response.raise_for_status()
    return response.json()
```

### Pattern 2: Retry Only Appropriate Errors

Whitelist specific transient exceptions. Never retry:

- `ValueError`, `TypeError` - These are bugs, not transient issues
- `AuthenticationError` - Invalid credentials won't become valid
- HTTP 4xx errors (except 429) - Client errors are permanent

```python
from tenacity import retry, retry_if_exception_type
import httpx

# Define what's retryable
RETRYABLE_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
)

@retry(
    retry=retry_if_exception_type(RETRYABLE_EXCEPTIONS),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def resilient_api_call(endpoint: str) -> dict:
    """Make API call with retry on network issues."""
    return httpx.get(endpoint, timeout=10).json()
```

### Pattern 3: HTTP Status Code Retries

Retry specific HTTP status codes that indicate transient issues.

```python
from tenacity import retry, retry_if_result, stop_after_attempt
import httpx

RETRY_STATUS_CODES = {429, 502, 503, 504}

def should_retry_response(response: httpx.Response) -> bool:
    """Check if response indicates a retryable error."""
    return response.status_code in RETRY_STATUS_CODES

@retry(
    retry=retry_if_result(should_retry_response),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
)
def http_request(method: str, url: str, **kwargs) -> httpx.Response:
    """Make HTTP request with retry on transient status codes."""
    return httpx.request(method, url, timeout=30, **kwargs)
```

### Pattern 4: Combined Exception and Status Retry

Handle both network exceptions and HTTP status codes.

```python
from tenacity import (
    retry,
    retry_if_exception_type,
    retry_if_result,
    stop_after_attempt,
    wait_exponential_jitter,
    before_sleep_log,
)
import logging
import httpx

logger = logging.getLogger(__name__)

TRANSIENT_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
    httpx.ConnectError,
    httpx.ReadTimeout,
)
RETRY_STATUS_CODES = {429, 500, 502, 503, 504}

def is_retryable_response(response: httpx.Response) -> bool:
    return response.status_code in RETRY_STATUS_CODES

@retry(
    retry=(
        retry_if_exception_type(TRANSIENT_EXCEPTIONS) |
        retry_if_result(is_retryable_response)
    ),
    stop=stop_after_attempt(5),
    wait=wait_exponential_jitter(initial=1, max=30),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def robust_http_call(
    method: str,
    url: str,
    **kwargs,
) -> httpx.Response:
    """HTTP call with comprehensive retry handling."""
    return httpx.request(method, url, timeout=30, **kwargs)
```

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

## Best Practices Summary

1. **Retry only transient errors** - Don't retry bugs or authentication failures
2. **Use exponential backoff** - Give services time to recover
3. **Add jitter** - Prevent thundering herd from synchronized retries
4. **Cap total duration** - `stop_after_attempt(5) | stop_after_delay(60)`
5. **Log every retry** - Silent retries hide systemic problems
6. **Use decorators** - Keep retry logic separate from business logic
7. **Inject dependencies** - Make infrastructure testable
8. **Set timeouts everywhere** - Every network call needs a timeout
9. **Fail gracefully** - Return cached/default values for non-critical paths
10. **Monitor retry rates** - High retry rates indicate underlying issues
