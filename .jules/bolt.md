## 2024-05-23 - Thread Pool Overhead in Iterative Tasks
**Learning:** Recreating `ThreadPoolExecutor` inside a frequently called loop (like an optimization loop) introduces significant overhead, especially when the individual tasks are short-lived.
**Action:** Initialize `ThreadPoolExecutor` once in the class `__init__` and reuse it across method calls to amortize the setup cost.
