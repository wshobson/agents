---
name: async-python-patterns
description: Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations.
---

# Async Python Patterns

Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.

## When to Use This Skill

- Building async web APIs (FastAPI, aiohttp, Sanic)
- Implementing concurrent I/O operations (database, file, network)
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSocket servers, chat systems)
- Processing multiple independent tasks simultaneously
- Building microservices with async communication
- Optimizing I/O-bound workloads
- Implementing async background tasks and queues

## Sync vs Async Decision Guide

Before adopting async, consider whether it's the right choice for your use case.

| Use Case | Recommended Approach |
|----------|---------------------|
| Many concurrent network/DB calls | `asyncio` |
| CPU-bound computation | `multiprocessing` or thread pool |
| Mixed I/O + CPU | Offload CPU work with `asyncio.to_thread()` |
| Simple scripts, few connections | Sync (simpler, easier to debug) |
| Web APIs with high concurrency | Async frameworks (FastAPI, aiohttp) |

**Key Rule:** Stay fully sync or fully async within a call path. Mixing creates hidden blocking and complexity.

## Core Concepts

### 1. Event Loop

The event loop is the heart of asyncio, managing and scheduling asynchronous tasks.

**Key characteristics:**

- Single-threaded cooperative multitasking
- Schedules coroutines for execution
- Handles I/O operations without blocking
- Manages callbacks and futures

### 2. Coroutines

Functions defined with `async def` that can be paused and resumed.

**Syntax:**

```python
async def my_coroutine():
    result = await some_async_operation()
    return result
```

### 3. Tasks

Scheduled coroutines that run concurrently on the event loop.

### 4. Futures

Low-level objects representing eventual results of async operations.

### 5. Async Context Managers

Resources that support `async with` for proper cleanup.

### 6. Async Iterators

Objects that support `async for` for iterating over async data sources.

## Quick Start

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Python 3.7+
asyncio.run(main())
```

## Fundamental Patterns

### Pattern 1: Basic Async/Await

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Fetch data from URL asynchronously."""
    await asyncio.sleep(1)  # Simulate I/O
    return {"url": url, "data": "result"}

async def main():
    result = await fetch_data("https://api.example.com")
    print(result)

asyncio.run(main())
```

### Pattern 2: Concurrent Execution with gather()

```python
import asyncio
from typing import List

async def fetch_user(user_id: int) -> dict:
    """Fetch user data."""
    await asyncio.sleep(0.5)
    return {"id": user_id, "name": f"User {user_id}"}

async def fetch_all_users(user_ids: List[int]) -> List[dict]:
    """Fetch multiple users concurrently."""
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    user_ids = [1, 2, 3, 4, 5]
    users = await fetch_all_users(user_ids)
    print(f"Fetched {len(users)} users")

asyncio.run(main())
```

### Pattern 3: Task Creation and Management

```python
import asyncio

async def background_task(name: str, delay: int):
    """Long-running background task."""
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} completed")
    return f"Result from {name}"

async def main():
    # Create tasks
    task1 = asyncio.create_task(background_task("Task 1", 2))
    task2 = asyncio.create_task(background_task("Task 2", 1))

    # Do other work
    print("Main: doing other work")
    await asyncio.sleep(0.5)

    # Wait for tasks
    result1 = await task1
    result2 = await task2

    print(f"Results: {result1}, {result2}")

asyncio.run(main())
```

### Pattern 4: Error Handling in Async Code

```python
import asyncio
from typing import List, Optional

async def risky_operation(item_id: int) -> dict:
    """Operation that might fail."""
    await asyncio.sleep(0.1)
    if item_id % 3 == 0:
        raise ValueError(f"Item {item_id} failed")
    return {"id": item_id, "status": "success"}

async def safe_operation(item_id: int) -> Optional[dict]:
    """Wrapper with error handling."""
    try:
        return await risky_operation(item_id)
    except ValueError as e:
        print(f"Error: {e}")
        return None

async def process_items(item_ids: List[int]):
    """Process multiple items with error handling."""
    tasks = [safe_operation(iid) for iid in item_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out failures
    successful = [r for r in results if r is not None and not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]

    print(f"Success: {len(successful)}, Failed: {len(failed)}")
    return successful

asyncio.run(process_items([1, 2, 3, 4, 5, 6]))
```

### Pattern 5: Timeout Handling

```python
import asyncio

async def slow_operation(delay: int) -> str:
    """Operation that takes time."""
    await asyncio.sleep(delay)
    return f"Completed after {delay}s"

async def with_timeout():
    """Execute operation with timeout."""
    try:
        result = await asyncio.wait_for(slow_operation(5), timeout=2.0)
        print(result)
    except asyncio.TimeoutError:
        print("Operation timed out")

asyncio.run(with_timeout())
```

## Detailed worked examples and patterns

Detailed sections (starting with `## Advanced Patterns`) live in `references/details.md`. Read that file when the navigation summary above is insufficient.

## Common Pitfalls

### 1. Forgetting await

```python
# Wrong - returns coroutine object, doesn't execute
result = async_function()

# Correct
result = await async_function()
```

### 2. Blocking the Event Loop

```python
# Wrong - blocks event loop
import time
async def bad():
    time.sleep(1)  # Blocks!

# Correct
async def good():
    await asyncio.sleep(1)  # Non-blocking
```

### 3. Not Handling Cancellation

```python
async def cancelable_task():
    """Task that handles cancellation."""
    try:
        while True:
            await asyncio.sleep(1)
            print("Working...")
    except asyncio.CancelledError:
        print("Task cancelled, cleaning up...")
        # Perform cleanup
        raise  # Re-raise to propagate cancellation
```

### 4. Mixing Sync and Async Code

```python
# Wrong - can't call async from sync directly
def sync_function():
    result = await async_function()  # SyntaxError!

# Correct
def sync_function():
    result = asyncio.run(async_function())
```

## Testing Async Code

```python
import asyncio
import pytest

# Using pytest-asyncio
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await fetch_data("https://api.example.com")
    assert result is not None

@pytest.mark.asyncio
async def test_with_timeout():
    """Test with timeout."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_operation(5), timeout=1.0)
```
