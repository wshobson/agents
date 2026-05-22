# async-python-patterns — detailed worked examples

## Advanced Patterns

### Pattern 6: Async Context Managers

```python
import asyncio
from typing import Optional

class AsyncDatabaseConnection:
    """Async database connection context manager."""

    def __init__(self, dsn: str):
        self.dsn = dsn
        self.connection: Optional[object] = None

    async def __aenter__(self):
        print("Opening connection")
        await asyncio.sleep(0.1)  # Simulate connection
        self.connection = {"dsn": self.dsn, "connected": True}
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing connection")
        await asyncio.sleep(0.1)  # Simulate cleanup
        self.connection = None

async def query_database():
    """Use async context manager."""
    async with AsyncDatabaseConnection("postgresql://localhost") as conn:
        print(f"Using connection: {conn}")
        await asyncio.sleep(0.2)  # Simulate query
        return {"rows": 10}

asyncio.run(query_database())
```

### Pattern 7: Async Iterators and Generators

```python
import asyncio
from typing import AsyncIterator

async def async_range(start: int, end: int, delay: float = 0.1) -> AsyncIterator[int]:
    """Async generator that yields numbers with delay."""
    for i in range(start, end):
        await asyncio.sleep(delay)
        yield i

async def fetch_pages(url: str, max_pages: int) -> AsyncIterator[dict]:
    """Fetch paginated data asynchronously."""
    for page in range(1, max_pages + 1):
        await asyncio.sleep(0.2)  # Simulate API call
        yield {
            "page": page,
            "url": f"{url}?page={page}",
            "data": [f"item_{page}_{i}" for i in range(5)]
        }

async def consume_async_iterator():
    """Consume async iterator."""
    async for number in async_range(1, 5):
        print(f"Number: {number}")

    print("\nFetching pages:")
    async for page_data in fetch_pages("https://api.example.com/items", 3):
        print(f"Page {page_data['page']}: {len(page_data['data'])} items")

asyncio.run(consume_async_iterator())
```

### Pattern 8: Producer-Consumer Pattern

```python
import asyncio
from asyncio import Queue
from typing import Optional

async def producer(queue: Queue, producer_id: int, num_items: int):
    """Produce items and put them in queue."""
    for i in range(num_items):
        item = f"Item-{producer_id}-{i}"
        await queue.put(item)
        print(f"Producer {producer_id} produced: {item}")
        await asyncio.sleep(0.1)
    await queue.put(None)  # Signal completion

async def consumer(queue: Queue, consumer_id: int):
    """Consume items from queue."""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break

        print(f"Consumer {consumer_id} processing: {item}")
        await asyncio.sleep(0.2)  # Simulate work
        queue.task_done()

async def producer_consumer_example():
    """Run producer-consumer pattern."""
    queue = Queue(maxsize=10)

    # Create tasks
    producers = [
        asyncio.create_task(producer(queue, i, 5))
        for i in range(2)
    ]

    consumers = [
        asyncio.create_task(consumer(queue, i))
        for i in range(3)
    ]

    # Wait for producers
    await asyncio.gather(*producers)

    # Wait for queue to be empty
    await queue.join()

    # Cancel consumers
    for c in consumers:
        c.cancel()

asyncio.run(producer_consumer_example())
```

### Pattern 9: Semaphore for Rate Limiting

```python
import asyncio
from typing import List

async def api_call(url: str, semaphore: asyncio.Semaphore) -> dict:
    """Make API call with rate limiting."""
    async with semaphore:
        print(f"Calling {url}")
        await asyncio.sleep(0.5)  # Simulate API call
        return {"url": url, "status": 200}

async def rate_limited_requests(urls: List[str], max_concurrent: int = 5):
    """Make multiple requests with rate limiting."""
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [api_call(url, semaphore) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    urls = [f"https://api.example.com/item/{i}" for i in range(20)]
    results = await rate_limited_requests(urls, max_concurrent=3)
    print(f"Completed {len(results)} requests")

asyncio.run(main())
```

### Pattern 10: Async Locks and Synchronization

```python
import asyncio

class AsyncCounter:
    """Thread-safe async counter."""

    def __init__(self):
        self.value = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        """Safely increment counter."""
        async with self.lock:
            current = self.value
            await asyncio.sleep(0.01)  # Simulate work
            self.value = current + 1

    async def get_value(self) -> int:
        """Get current value."""
        async with self.lock:
            return self.value

async def worker(counter: AsyncCounter, worker_id: int):
    """Worker that increments counter."""
    for _ in range(10):
        await counter.increment()
        print(f"Worker {worker_id} incremented")

async def test_counter():
    """Test concurrent counter."""
    counter = AsyncCounter()

    workers = [asyncio.create_task(worker(counter, i)) for i in range(5)]
    await asyncio.gather(*workers)

    final_value = await counter.get_value()
    print(f"Final counter value: {final_value}")

asyncio.run(test_counter())
```

## Real-World Applications

### Web Scraping with aiohttp

```python
import asyncio
import aiohttp
from typing import List, Dict

async def fetch_url(session: aiohttp.ClientSession, url: str) -> Dict:
    """Fetch single URL."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
            text = await response.text()
            return {
                "url": url,
                "status": response.status,
                "length": len(text)
            }
    except Exception as e:
        return {"url": url, "error": str(e)}

async def scrape_urls(urls: List[str]) -> List[Dict]:
    """Scrape multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

async def main():
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2",
        "https://httpbin.org/status/404",
    ]

    results = await scrape_urls(urls)
    for result in results:
        print(result)

asyncio.run(main())
```

### Async Database Operations

```python
import asyncio
from typing import List, Optional

# Simulated async database client
class AsyncDB:
    """Simulated async database."""

    async def execute(self, query: str) -> List[dict]:
        """Execute query."""
        await asyncio.sleep(0.1)
        return [{"id": 1, "name": "Example"}]

    async def fetch_one(self, query: str) -> Optional[dict]:
        """Fetch single row."""
        await asyncio.sleep(0.1)
        return {"id": 1, "name": "Example"}

async def get_user_data(db: AsyncDB, user_id: int) -> dict:
    """Fetch user and related data concurrently."""
    user_task = db.fetch_one(f"SELECT * FROM users WHERE id = {user_id}")
    orders_task = db.execute(f"SELECT * FROM orders WHERE user_id = {user_id}")
    profile_task = db.fetch_one(f"SELECT * FROM profiles WHERE user_id = {user_id}")

    user, orders, profile = await asyncio.gather(user_task, orders_task, profile_task)

    return {
        "user": user,
        "orders": orders,
        "profile": profile
    }

async def main():
    db = AsyncDB()
    user_data = await get_user_data(db, 1)
    print(user_data)

asyncio.run(main())
```

### WebSocket Server

```python
import asyncio
from typing import Set

# Simulated WebSocket connection
class WebSocket:
    """Simulated WebSocket."""

    def __init__(self, client_id: str):
        self.client_id = client_id

    async def send(self, message: str):
        """Send message."""
        print(f"Sending to {self.client_id}: {message}")
        await asyncio.sleep(0.01)

    async def recv(self) -> str:
        """Receive message."""
        await asyncio.sleep(1)
        return f"Message from {self.client_id}"

class WebSocketServer:
    """Simple WebSocket server."""

    def __init__(self):
        self.clients: Set[WebSocket] = set()

    async def register(self, websocket: WebSocket):
        """Register new client."""
        self.clients.add(websocket)
        print(f"Client {websocket.client_id} connected")

    async def unregister(self, websocket: WebSocket):
        """Unregister client."""
        self.clients.remove(websocket)
        print(f"Client {websocket.client_id} disconnected")

    async def broadcast(self, message: str):
        """Broadcast message to all clients."""
        if self.clients:
            tasks = [client.send(message) for client in self.clients]
            await asyncio.gather(*tasks)

    async def handle_client(self, websocket: WebSocket):
        """Handle individual client connection."""
        await self.register(websocket)
        try:
            async for message in self.message_iterator(websocket):
                await self.broadcast(f"{websocket.client_id}: {message}")
        finally:
            await self.unregister(websocket)

    async def message_iterator(self, websocket: WebSocket):
        """Iterate over messages from client."""
        for _ in range(3):  # Simulate 3 messages
            yield await websocket.recv()
```

## Performance Best Practices

### 1. Use Connection Pools

```python
import asyncio
import aiohttp

async def with_connection_pool():
    """Use connection pool for efficiency."""
    connector = aiohttp.TCPConnector(limit=100, limit_per_host=10)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [session.get(f"https://api.example.com/item/{i}") for i in range(50)]
        responses = await asyncio.gather(*tasks)
        return responses
```

### 2. Batch Operations

```python
async def batch_process(items: List[str], batch_size: int = 10):
    """Process items in batches."""
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        tasks = [process_item(item) for item in batch]
        await asyncio.gather(*tasks)
        print(f"Processed batch {i // batch_size + 1}")

async def process_item(item: str):
    """Process single item."""
    await asyncio.sleep(0.1)
    return f"Processed: {item}"
```

### 3. Avoid Blocking Operations

Never block the event loop with synchronous operations. A single blocking call stalls all concurrent tasks.

```python
# BAD - blocks the entire event loop
async def fetch_data_bad():
    import time
    import requests
    time.sleep(1)  # Blocks!
    response = requests.get(url)  # Also blocks!

# GOOD - use async-native libraries (e.g., httpx for async HTTP)
import httpx

async def fetch_data_good(url: str):
    await asyncio.sleep(1)
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
```

**Wrapping Blocking Code with `asyncio.to_thread()` (Python 3.9+):**

When you must use synchronous libraries, offload to a thread pool:

```python
import asyncio
from pathlib import Path

async def read_file_async(path: str) -> str:
    """Read file without blocking event loop."""
    # asyncio.to_thread() runs sync code in a thread pool
    return await asyncio.to_thread(Path(path).read_text)

async def call_sync_library(data: dict) -> dict:
    """Wrap a synchronous library call."""
    # Useful for sync database drivers, file I/O, CPU work
    return await asyncio.to_thread(sync_library.process, data)
```

**Lower-level approach with `run_in_executor()`:**

```python
import asyncio
import concurrent.futures
from typing import Any

def blocking_operation(data: Any) -> Any:
    """CPU-intensive blocking operation."""
    import time
    time.sleep(1)
    return data * 2

async def run_in_executor(data: Any) -> Any:
    """Run blocking operation in thread pool."""
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, blocking_operation, data)
        return result

async def main():
    results = await asyncio.gather(*[run_in_executor(i) for i in range(5)])
    print(results)

asyncio.run(main())
```
