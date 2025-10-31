---
name: vshard-sharding
description: Master vshard distributed sharding framework for Tarantool clusters. Design sharded architectures, implement data partitioning, handle rebalancing, and optimize distributed queries. Use when designing large-scale distributed Tarantool systems.
---

# vshard Distributed Sharding

Complete guide to implementing distributed sharding with vshard in Tarantool.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Design and implement horizontally scalable Tarantool clusters using vshard distributed sharding.

## When to Use This Skill

- Design sharding strategy for large datasets
- Implement distributed key-value stores
- Build highly scalable databases
- Plan shard topology and replica groups
- Implement cross-shard queries
- Handle shard rebalancing

## Core Concepts

### Sharding Fundamentals

**Sharding Strategy**
```
Data Set -> Hash Function -> Bucket -> Shard -> Replica Group
```

**vshard Components**
- **Router**: Routes requests to correct shard
- **Storage**: Holds sharded data
- **Bucket**: Unit of data distribution (usually 64K buckets)

### Cluster Configuration

**Basic vshard Configuration**
```lua
-- config.yaml
sharding:
  - server_1:
      master: localhost:3301
      replicas:
        - localhost:3302
  - server_2:
      master: localhost:3303
      replicas:
        - localhost:3304

bucket_count: 65536  -- Total buckets (typically power of 2)
```

**Lua Configuration**
```lua
local vshard = require('vshard')

vshard.storage.cfg({
    sharding = {
        {
            replicas = {
                {uri = 'localhost:3301', name = 'storage_1_a'},
                {uri = 'localhost:3302', name = 'storage_1_b'}
            }
        },
        {
            replicas = {
                {uri = 'localhost:3303', name = 'storage_2_a'},
                {uri = 'localhost:3304', name = 'storage_2_b'}
            }
        }
    },
    bucket_count = 65536
})
```

### Bucket Management

**Bucket ID Calculation**
```lua
local vshard = require('vshard')

-- Get bucket ID for a key
local bucket_id = vshard.router.bucket_id(key)

-- Bucket ID from user_id
local bucket_id = vshard.router.bucket_id(user_id)
```

**Data Distribution**
```lua
-- Data is distributed based on bucket_id
-- bucket_id = hash(key) % bucket_count
-- Each shard owns a range of buckets (usually bucket_count / shard_count)
```

### Router Operations

**Router Initialization**
```lua
local vshard = require('vshard')

vshard.router.cfg({
    sharding = {...},
    bucket_count = 65536
})

-- Wait for router to be ready
vshard.router.bootstrap()
```

**Executing Distributed Queries**
```lua
-- Simple key-value get
local bucket_id = vshard.router.bucket_id(user_id)
local user = vshard.router:call(bucket_id, 'read', 'get_user', {user_id})

-- Insert with bucket routing
vshard.router:call(bucket_id, 'write', 'insert_user', {
    user_id, name, email
})
```

**Multi-Shard Queries**
```lua
local vshard = require('vshard')
local fiber = require('fiber')

local function parallel_query(callback)
    local replicas = {}
    local results = {}

    for bucket_id = 0, vshard.router.bucket_count() - 1 do
        local replica = vshard.router:route(bucket_id)
        if replica and not replicas[replica] then
            replicas[replica] = true
        end
    end

    local futures = {}
    for replica, _ in pairs(replicas) do
        table.insert(futures, replica:call('execute_query', {callback}))
    end

    for _, future in pairs(futures) do
        table.insert(results, future:wait_result())
    end

    return results
end
```

### Rebalancing

**Automatic Rebalancing**
```lua
local vshard = require('vshard')

-- Trigger rebalancing
vshard.storage.rebalancer_request_state(vshard.consts.REBALANCER_STATE_TRANSFER)

-- Monitor rebalancing progress
local info = vshard.storage.info()
if info.rebalancer.status == 'ok' then
    print("Rebalancing completed")
end
```

**Bucket Movement**
```lua
-- When adding new shard, buckets migrate automatically
-- vshard coordinator distributes bucket reassignment
-- Data is copied, then old copy is deleted
-- No downtime during rebalancing
```

### Storage Implementation

**Storage Node Setup**
```lua
-- init.lua for storage node
local vshard = require('vshard')

-- Create spaces for sharded data
box.schema.space.create('users', {
    format = {
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'bucket_id', type = 'unsigned'}
    }
})

box.space.users:create_index('primary', {
    parts = {'id'}
})

box.space.users:create_index('bucket_id', {
    parts = {'bucket_id'}
})

-- Configure vshard
vshard.storage.cfg({...})
```

**Bucket-Aware Functions**
```lua
local function get_user(user_id)
    local bucket_id = vshard.router.bucket_id(user_id)

    if bucket_id == nil then
        return nil, 'Invalid key'
    end

    if not vshard.storage.bucket_is_accessible(bucket_id) then
        return nil, 'Bucket is not accessible'
    end

    return box.space.users:get(user_id)
end
```

### Shard Topology Planning

**Single-Region Cluster**
```
Router Layer
    |
    ├─-> Storage Shard 1 (Master + Replica)
    ├─-> Storage Shard 2 (Master + Replica)
    └─-> Storage Shard N (Master + Replica)
```

**Multi-Region Cluster**
```
Region 1                    Region 2
Router -> Shards 1-N    Router -> Shards 1-N
(Write to local shard)   (Write to local shard)
    |_________________________|
    (Replicate across regions)
```

**Replica Groups Per Shard**
```lua
{
    replicas = {
        {
            uri = 'storage_1_a:3301',
            name = 'storage_1_a',
            master = true
        },
        {
            uri = 'storage_1_b:3302',
            name = 'storage_1_b',
            master = false
        }
    }
}
```

## Best Practices

1. **Shard Key Selection**
   - Choose key that distributes evenly
   - Use user_id, customer_id, or similar for analytics
   - Avoid time-based sharding

2. **Bucket Count**
   - Use 64K or 128K buckets as standard
   - More buckets = finer granularity
   - Affects rebalancing time

3. **Query Patterns**
   - Single-key lookups are optimal
   - Minimize multi-shard queries
   - Denormalize to avoid joins

4. **Adding Shards**
   - Plan capacity growth
   - Add shards in groups (maintain replica redundancy)
   - Monitor rebalancing progress

5. **Failover**
   - Use replica groups for HA
   - Router automatically fails over
   - Monitor master status

## Common Pitfalls

- **Hot Shards**: Uneven key distribution
- **Too Many Buckets**: Slow rebalancing
- **Complex Queries**: Avoid cross-shard transactions
- **Shard Explosion**: Too many shards for dataset size
- **Inconsistent Keys**: Different sharding logic in different places

## Related Skills

- `tarantool-architecture` - Overall cluster design
- `lua-development` - Implementing distributed logic
- `replication-ha` - Replica group configuration
- `tarantool-performance` - Distributed performance tuning
