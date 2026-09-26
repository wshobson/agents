## Debugging Tools

### JavaScript/TypeScript Debugging

```typescript
// Chrome DevTools Debugger
function processOrder(order: Order) {
  debugger; // Execution pauses here

  const total = calculateTotal(order);
  console.log("Total:", total);

  // Conditional breakpoint
  if (order.items.length > 10) {
    debugger; // Only breaks if condition true
  }

  return total;
}

// Console debugging techniques
console.log("Value:", value); // Basic
console.table(arrayOfObjects); // Table format
console.time("operation");
/* code */ console.timeEnd("operation"); // Timing
console.trace(); // Stack trace
console.assert(value > 0, "Value must be positive"); // Assertion

// Performance profiling
performance.mark("start-operation");
// ... operation code
performance.mark("end-operation");
performance.measure("operation", "start-operation", "end-operation");
console.log(performance.getEntriesByType("measure"));
```

**VS Code Debugger Configuration:**

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Program",
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "tsc: build - tsconfig.json",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"],
      "skipFiles": ["<node_internals>/**"]
    },
    {
      "type": "node",
      "request": "launch",
      "name": "Debug Tests",
      "program": "${workspaceFolder}/node_modules/jest/bin/jest",
      "args": ["--runInBand", "--no-cache"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Python Debugging

```python
# Built-in debugger (pdb)
import pdb

def calculate_total(items):
    total = 0
    pdb.set_trace()  # Debugger starts here

    for item in items:
        total += item.price * item.quantity

    return total

# Breakpoint (Python 3.7+)
def process_order(order):
    breakpoint()  # More convenient than pdb.set_trace()
    # ... code

# Post-mortem debugging
try:
    risky_operation()
except Exception:
    import pdb
    pdb.post_mortem()  # Debug at exception point

# IPython debugging (ipdb)
from ipdb import set_trace
set_trace()  # Better interface than pdb

# Logging for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_user(user_id):
    logger.debug(f'Fetching user: {user_id}')
    user = db.query(User).get(user_id)
    logger.debug(f'Found user: {user}')
    return user

# Profile performance
import cProfile
import pstats

cProfile.run('slow_function()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest
```

### Go Debugging

```go
// Delve debugger
// Install: go install github.com/go-delve/delve/cmd/dlv@latest
// Run: dlv debug main.go

import (
    "fmt"
    _ "net/http/pprof"
    "os"
    "runtime/debug"
    "runtime/pprof"
)

// Print stack trace
func debugStack() {
    debug.PrintStack()
}

// Panic recovery with debugging
func processRequest() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Panic:", r)
            debug.PrintStack()
        }
    }()

    // ... code that might panic
}

// The blank import above registers profiling handlers on the default mux.
// Serve that mux on a loopback-only endpoint in your application before visiting
// http://localhost:6060/debug/pprof/; importing alone does not start a server.

// CPU profiling: invoke this helper around the workload you want to measure.
func profileCPU() error {
    f, err := os.Create("cpu.prof")
    if err != nil {
        return err
    }
    defer f.Close()
    if err := pprof.StartCPUProfile(f); err != nil {
        return err
    }
    defer pprof.StopCPUProfile()
    // ... code to profile
    return nil
}
```

## Advanced Debugging Techniques

### Technique 1: Binary Search Debugging

```bash
# Git bisect for finding regression
git bisect start
git bisect bad                    # Current commit is bad
git bisect good v1.0.0            # v1.0.0 was good

# Git checks out middle commit
# Test it, then:
git bisect good   # if it works
git bisect bad    # if it's broken

# Continue until bug found
git bisect reset  # when done
```

### Technique 2: Differential Debugging

Compare working vs broken:

```markdown
## What's Different?

| Aspect       | Working     | Broken         |
| ------------ | ----------- | -------------- |
| Environment  | Development | Production     |
| Node version | 18.16.0     | 18.15.0        |
| Data         | Empty DB    | 1M records     |
| User         | Admin       | Regular user   |
| Browser      | Chrome      | Safari         |
| Time         | During day  | After midnight |

Hypothesis: Time-based issue? Check timezone handling.
```

### Technique 3: Trace Debugging

```typescript
// Function call tracing
function trace(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor,
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with args:`, args);
    const result = originalMethod.apply(this, args);
    console.log(`${propertyKey} returned:`, result);
    return result;
  };

  return descriptor;
}

class OrderService {
  @trace
  calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
  }
}
```

### Technique 4: Memory Leak Detection

```typescript
// Chrome DevTools Memory Profiler
// 1. Take heap snapshot
// 2. Perform action
// 3. Take another snapshot
// 4. Compare snapshots

// Node.js memory debugging
if (process.memoryUsage().heapUsed > 500 * 1024 * 1024) {
  console.warn("High memory usage:", process.memoryUsage());

  // Generate heap dump
  require("v8").writeHeapSnapshot();
}

// Find memory leaks in tests
let beforeMemory: number;

beforeEach(() => {
  beforeMemory = process.memoryUsage().heapUsed;
});

afterEach(() => {
  const afterMemory = process.memoryUsage().heapUsed;
  const diff = afterMemory - beforeMemory;

  if (diff > 10 * 1024 * 1024) {
    // 10MB threshold
    console.warn(`Possible memory leak: ${diff / 1024 / 1024}MB`);
  }
});
```
