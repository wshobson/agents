---
name: python-observability
description: Python observability patterns including structured logging, metrics, and distributed tracing. Use when adding logging, implementing metrics collection, setting up tracing, or debugging production systems.
---

# Python Observability

Instrument Python applications with structured logs, metrics, and traces. When something breaks in production, you need to answer "what, where, and why" without deploying new code.

## When to Use This Skill

- Adding structured logging to applications
- Implementing metrics collection with Prometheus
- Setting up distributed tracing across services
- Propagating correlation IDs through request chains
- Debugging production issues
- Building observability dashboards

## Core Concepts

### 1. Structured Logging

Emit logs as JSON with consistent fields for production environments. Machine-readable logs enable powerful queries and alerts. For local development, consider human-readable formats.

### 2. The Four Golden Signals

Track latency, traffic, errors, and saturation for every service boundary.

### 3. Correlation IDs

Thread a unique ID through all logs and spans for a single request, enabling end-to-end tracing.

### 4. Bounded Cardinality

Keep metric label values bounded. Unbounded labels (like user IDs) explode storage costs.

## Quick Start

```python
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger()
logger.info("Request processed", user_id="123", duration_ms=45)
```

## Fundamental Patterns

### Pattern 1: Structured Logging with Structlog

Configure structlog for JSON output with consistent fields.

```python
import logging
import structlog

def configure_logging(log_level: str = "INFO") -> None:
    """Configure structured logging for the application."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Initialize at application startup
configure_logging("INFO")
logger = structlog.get_logger()
```

### Pattern 2: Consistent Log Fields

Every log entry should include standard fields for filtering and correlation.

```python
import structlog
from contextvars import ContextVar

# Store correlation ID in context
correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

logger = structlog.get_logger()

def process_request(request: Request) -> Response:
    """Process request with structured logging."""
    logger.info(
        "Request received",
        correlation_id=correlation_id.get(),
        method=request.method,
        path=request.path,
        user_id=request.user_id,
    )

    try:
        result = handle_request(request)
        logger.info(
            "Request completed",
            correlation_id=correlation_id.get(),
            status_code=200,
            duration_ms=elapsed,
        )
        return result
    except Exception as e:
        logger.error(
            "Request failed",
            correlation_id=correlation_id.get(),
            error_type=type(e).__name__,
            error_message=str(e),
        )
        raise
```

### Pattern 3: Semantic Log Levels

Use log levels consistently across the application.

| Level | Purpose | Examples |
|-------|---------|----------|
| `DEBUG` | Development diagnostics | Variable values, internal state |
| `INFO` | Request lifecycle, operations | Request start/end, job completion |
| `WARNING` | Recoverable anomalies | Retry attempts, fallback used |
| `ERROR` | Failures needing attention | Exceptions, service unavailable |

```python
# DEBUG: Detailed internal information
logger.debug("Cache lookup", key=cache_key, hit=cache_hit)

# INFO: Normal operational events
logger.info("Order created", order_id=order.id, total=order.total)

# WARNING: Abnormal but handled situations
logger.warning(
    "Rate limit approaching",
    current_rate=950,
    limit=1000,
    reset_seconds=30,
)

# ERROR: Failures requiring investigation
logger.error(
    "Payment processing failed",
    order_id=order.id,
    error=str(e),
    payment_provider="stripe",
)
```

Never log expected behavior at `ERROR`. A user entering a wrong password is `INFO`, not `ERROR`.

### Pattern 4: Correlation ID Propagation

Generate a unique ID at ingress and thread it through all operations.

```python
from contextvars import ContextVar
import uuid
import structlog

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

def set_correlation_id(cid: str | None = None) -> str:
    """Set correlation ID for current context."""
    cid = cid or str(uuid.uuid4())
    correlation_id.set(cid)
    structlog.contextvars.bind_contextvars(correlation_id=cid)
    return cid

# FastAPI middleware example
from fastapi import Request

async def correlation_middleware(request: Request, call_next):
    """Middleware to set and propagate correlation ID."""
    # Use incoming header or generate new
    cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    set_correlation_id(cid)

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid
    return response
```

Propagate to outbound requests:

```python
import httpx

async def call_downstream_service(endpoint: str, data: dict) -> dict:
    """Call downstream service with correlation ID."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            json=data,
            headers={"X-Correlation-ID": correlation_id.get()},
        )
        return response.json()
```

## Detailed worked examples and patterns

Detailed sections (starting with `## Advanced Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

## Best Practices Summary

1. **Use structured logging** - JSON logs with consistent fields
2. **Propagate correlation IDs** - Thread through all requests and logs
3. **Track the four golden signals** - Latency, traffic, errors, saturation
4. **Bound label cardinality** - Never use unbounded values as metric labels
5. **Log at appropriate levels** - Don't cry wolf with ERROR
6. **Include context** - User ID, request ID, operation name in logs
7. **Use context managers** - Consistent timing and error handling
8. **Separate concerns** - Observability code shouldn't pollute business logic
9. **Test your observability** - Verify logs and metrics in integration tests
10. **Set up alerts** - Metrics are useless without alerting
