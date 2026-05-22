---
name: go-concurrency-patterns
description: Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing worker pools, or debugging race conditions.
---

# Go Concurrency Patterns

Production patterns for Go concurrency including goroutines, channels, synchronization primitives, and context management.

## When to Use This Skill

- Building concurrent Go applications
- Implementing worker pools and pipelines
- Managing goroutine lifecycles
- Using channels for communication
- Debugging race conditions
- Implementing graceful shutdown

## Core Concepts

### 1. Go Concurrency Primitives

| Primitive         | Purpose                          |
| ----------------- | -------------------------------- |
| `goroutine`       | Lightweight concurrent execution |
| `channel`         | Communication between goroutines |
| `select`          | Multiplex channel operations     |
| `sync.Mutex`      | Mutual exclusion                 |
| `sync.WaitGroup`  | Wait for goroutines to complete  |
| `context.Context` | Cancellation and deadlines       |

### 2. Go Concurrency Mantra

```
Don't communicate by sharing memory;
share memory by communicating.
```

## Quick Start

```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    results := make(chan string, 10)
    var wg sync.WaitGroup

    // Spawn workers
    for i := 0; i < 3; i++ {
        wg.Add(1)
        go worker(ctx, i, results, &wg)
    }

    // Close results when done
    go func() {
        wg.Wait()
        close(results)
    }()

    // Collect results
    for result := range results {
        fmt.Println(result)
    }
}

func worker(ctx context.Context, id int, results chan<- string, wg *sync.WaitGroup) {
    defer wg.Done()

    select {
    case <-ctx.Done():
        return
    case results <- fmt.Sprintf("Worker %d done", id):
    }
}
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Use context** - For cancellation and deadlines
- **Close channels** - From sender side only
- **Use errgroup** - For concurrent operations with errors
- **Buffer channels** - When you know the count
- **Prefer channels** - Over mutexes when possible

### Don'ts

- **Don't leak goroutines** - Always have exit path
- **Don't close from receiver** - Causes panic
- **Don't use shared memory** - Unless necessary
- **Don't ignore context cancellation** - Check ctx.Done()
- **Don't use time.Sleep for sync** - Use proper primitives
