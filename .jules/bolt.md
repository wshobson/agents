## 2024-05-23 - Thread Pool Overhead in Iterative Tasks
**Learning:** Recreating `ThreadPoolExecutor` inside a frequently called loop (like an optimization loop) introduces significant overhead, especially when the individual tasks are short-lived.
**Action:** Initialize `ThreadPoolExecutor` once in the class `__init__` and reuse it across method calls to amortize the setup cost.

## 2024-05-23 - Heavy Dependencies for Simple Math
**Learning:** Importing huge libraries like `numpy` for simple operations (mean, percentile) adds unnecessary installation complexity and startup latency (100ms+), and can cause crashes in minimal environments.
**Action:** Use native Python math or simple helper functions for basic statistics when dataset size is small (<1M items).
