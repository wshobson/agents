---
name: tarantool-performance
description: Master Tarantool performance optimization, benchmarking, profiling, and tuning techniques for microsecond-latency applications. Use when optimizing Tarantool performance or designing for specific SLAs.
---

# Tarantool Performance Optimization

Complete guide to optimizing Tarantool for high performance.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Optimize Tarantool applications for microsecond latency and extreme throughput.

## When to Use This Skill

- Profile and optimize Tarantool applications
- Benchmark storage engines
- Tune memory and disk usage
- Optimize query patterns
- Design for specific SLA targets
- Identify and fix performance bottlenecks

## Core Concepts

### Profiling with fprofile

**Enable Profiling**
```lua
local fprofile = require('fprofile')
fprofile.enable()

-- Run workload
for i = 1, 1000000 do
    box.space.data:insert({i, 'value'})
end

fprofile.dump()
```

### Index Performance

**Index Selection**
```lua
-- Bad: Full table scan
local users = box.space.users:select({})

-- Good: Index-based lookup
local user = box.space.users.index.primary:get(user_id)

-- Better: Composite index for multi-field filters
local orders = box.space.orders.index.user_date:select({user_id})
```

### Memory Optimization

**Configuration**
```lua
box.cfg {
    memtx_max_tuple_size = 1024 * 1024,
    memtx_memory = 2 * 1024 * 1024 * 1024,  -- 2GB
    wal_max_size = 256 * 1024 * 1024
}
```

### Batch Operations

**Bulk Insert Optimization**
```lua
-- Slow: One-at-a-time
for i = 1, 100000 do
    box.space.users:insert({i, 'user' .. i})
end

-- Fast: In transaction
box.begin()
for i = 1, 100000 do
    box.space.users:insert({i, 'user' .. i})
end
box.commit()
```

### Query Optimization

**Execution Plans**
```lua
-- Check query plan
box.execute("EXPLAIN SELECT * FROM users WHERE id = ?", {1})
```

## Best Practices

1. **Indexing Strategy**
   - Index all filter columns
   - Use composite indexes
   - Monitor index size

2. **Transaction Design**
   - Keep transactions short
   - Batch when appropriate
   - Minimize lock contention

3. **Memory Usage**
   - Monitor memory consumption
   - Use vinyl for large datasets
   - Clean up old data regularly

4. **Benchmarking**
   - Test with realistic workloads
   - Use production-like data volumes
   - Measure latency distribution

## Related Skills

- `tarantool-architecture` - Design for performance
- `lua-development` - Efficient code patterns
- `vshard-sharding` - Distributed performance
