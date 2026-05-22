# python-error-handling — detailed worked examples

## Advanced Patterns

### Pattern 5: Custom Exceptions with Context

Create domain-specific exceptions that carry structured information.

```python
class ApiError(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_body: str | None = None,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)

class RateLimitError(ApiError):
    """Raised when rate limit is exceeded."""

    def __init__(self, retry_after: int) -> None:
        self.retry_after = retry_after
        super().__init__(
            f"Rate limit exceeded. Retry after {retry_after}s",
            status_code=429,
        )

# Usage
def handle_response(response: Response) -> dict:
    match response.status_code:
        case 200:
            return response.json()
        case 401:
            raise ApiError("Invalid credentials", 401)
        case 404:
            raise ApiError(f"Resource not found: {response.url}", 404)
        case 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            raise RateLimitError(retry_after)
        case code if 400 <= code < 500:
            raise ApiError(f"Client error: {response.text}", code)
        case code if code >= 500:
            raise ApiError(f"Server error: {response.text}", code)
```

### Pattern 6: Exception Chaining

Preserve the original exception when re-raising to maintain the debug trail.

```python
import httpx

class ServiceError(Exception):
    """High-level service operation failed."""
    pass

def upload_file(path: str) -> str:
    """Upload file and return URL."""
    try:
        with open(path, "rb") as f:
            response = httpx.post("https://upload.example.com", files={"file": f})
            response.raise_for_status()
            return response.json()["url"]
    except FileNotFoundError as e:
        raise ServiceError(f"Upload failed: file not found at '{path}'") from e
    except httpx.HTTPStatusError as e:
        raise ServiceError(
            f"Upload failed: server returned {e.response.status_code}"
        ) from e
    except httpx.RequestError as e:
        raise ServiceError(f"Upload failed: network error") from e
```

### Pattern 7: Batch Processing with Partial Failures

Never let one bad item abort an entire batch. Track results per item.

```python
from dataclasses import dataclass

@dataclass
class BatchResult[T]:
    """Results from batch processing."""

    succeeded: dict[int, T]  # index -> result
    failed: dict[int, Exception]  # index -> error

    @property
    def success_count(self) -> int:
        return len(self.succeeded)

    @property
    def failure_count(self) -> int:
        return len(self.failed)

    @property
    def all_succeeded(self) -> bool:
        return len(self.failed) == 0

def process_batch(items: list[Item]) -> BatchResult[ProcessedItem]:
    """Process items, capturing individual failures.

    Args:
        items: Items to process.

    Returns:
        BatchResult with succeeded and failed items by index.
    """
    succeeded: dict[int, ProcessedItem] = {}
    failed: dict[int, Exception] = {}

    for idx, item in enumerate(items):
        try:
            result = process_single_item(item)
            succeeded[idx] = result
        except Exception as e:
            failed[idx] = e

    return BatchResult(succeeded=succeeded, failed=failed)

# Caller handles partial results
result = process_batch(items)
if not result.all_succeeded:
    logger.warning(
        f"Batch completed with {result.failure_count} failures",
        failed_indices=list(result.failed.keys()),
    )
```

### Pattern 8: Progress Reporting for Long Operations

Provide visibility into batch progress without coupling business logic to UI.

```python
from collections.abc import Callable

ProgressCallback = Callable[[int, int, str], None]  # current, total, status

def process_large_batch(
    items: list[Item],
    on_progress: ProgressCallback | None = None,
) -> BatchResult:
    """Process batch with optional progress reporting.

    Args:
        items: Items to process.
        on_progress: Optional callback receiving (current, total, status).
    """
    total = len(items)
    succeeded = {}
    failed = {}

    for idx, item in enumerate(items):
        if on_progress:
            on_progress(idx, total, f"Processing {item.id}")

        try:
            succeeded[idx] = process_single_item(item)
        except Exception as e:
            failed[idx] = e

    if on_progress:
        on_progress(total, total, "Complete")

    return BatchResult(succeeded=succeeded, failed=failed)
```
