# Dependency Graph Patterns

Visual patterns for task dependency design with trade-offs.

## Pattern 1: Fully Independent (Maximum Parallelism)

```
Task A ─┐
Task B ─┼─→ Final Integration
Task C ─┘
```

- **Parallelism**: Maximum — all tasks run simultaneously
- **Risk**: Integration may reveal incompatibilities late
- **Use when**: Tasks operate on completely separate files/modules
- **TaskCreate**: No blockedBy relationships; integration task blocked by all

## Pattern 2: Sequential Chain (No Parallelism)

```
Task A → Task B → Task C → Task D
```

- **Parallelism**: None — each task waits for the previous
- **Risk**: Bottleneck at each step; one delay cascades
- **Use when**: Each task depends on the output of the previous (avoid if possible)
- **TaskCreate**: Each task blockedBy the previous

## Pattern 3: Diamond (Shared Foundation)

```
           ┌→ Task B ─┐
Task A ──→ ┤          ├→ Task D
           └→ Task C ─┘
```

- **Parallelism**: B and C run in parallel after A completes
- **Risk**: A is a bottleneck; D must wait for both B and C
- **Use when**: B and C both need output from A (e.g., shared types)
- **TaskCreate**: B and C blockedBy A; D blockedBy B and C

## Pattern 4: Fork-Join (Phased Parallelism)

```
Phase 1:  A1, A2, A3  (parallel)
          ────────────
Phase 2:  B1, B2      (parallel, after phase 1)
          ────────────
Phase 3:  C1          (after phase 2)
```

- **Parallelism**: Within each phase, tasks are parallel
- **Risk**: Phase boundaries add synchronization delays
- **Use when**: Natural phases with dependencies (build → test → deploy)
- **TaskCreate**: Phase 2 tasks blockedBy all Phase 1 tasks

## Pattern 5: Pipeline (Streaming)

```
Task A ──→ Task B ──→ Task C
  └──→ Task D ──→ Task E
```

- **Parallelism**: Two parallel chains
- **Risk**: Chains may diverge in approach
- **Use when**: Two independent feature branches from a common starting point
- **TaskCreate**: B blockedBy A; D blockedBy A; C blockedBy B; E blockedBy D

## Anti-Patterns

### Circular Dependency (Deadlock)

```
Task A → Task B → Task C → Task A  ✗ DEADLOCK
```

**Fix**: Extract shared dependency into a separate task that all three depend on.

### Unnecessary Dependencies

```
Task A → Task B → Task C
(where B doesn't actually need A's output)
```

**Fix**: Remove the blockedBy relationship; let B run independently.

### Star Pattern (Single Bottleneck)

```
     ┌→ B
A →  ├→ C  → F
     ├→ D
     └→ E
```

**Fix**: If A is slow, all downstream tasks are delayed. Try to parallelize A's work.
