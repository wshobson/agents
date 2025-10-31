---
name: tarantool-architecture
description: Master Tarantool database architecture, in-memory storage engine design, MVCC transactions, replication topologies, and distributed system patterns. Use when designing Tarantool databases, planning cluster architecture, or optimizing data models.
---

# Tarantool Architecture

Complete guide to designing and implementing Tarantool database architectures from single-instance to distributed clusters.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Design and implement scalable, high-performance Tarantool database architectures that meet throughput, latency, and availability requirements.

## When to Use This Skill

- Design Tarantool database schema and space structure
- Plan single-instance, replicated, or clustered deployments
- Optimize data models for specific workloads
- Select appropriate replication topologies
- Plan high-availability and disaster recovery strategies
- Design index strategies for performance
- Plan vshard sharding architecture

## Core Concepts

### In-Memory Storage Engine

**Memtx (Memory Storage Engine)**
- Ultra-fast access with microsecond latency
- B-tree and hash indexes
- Full ACID transaction support
- Limited by available RAM
- Best for: cache, session storage, real-time analytics

```lua
box.cfg {
    memtx_max_tuple_size = 1024 * 1024,  -- 1MB max tuple
    memtx_allocator = 'malloc'            -- Memory allocator
}
```

**Vinyl (Persistent Storage Engine)**
- LSM-tree based persistent storage
- Designed for high write throughput
- Automatic data compression
- Slower than memtx but persistent
- Best for: long-term storage, large datasets

```lua
box.cfg {
    vinyl_memory = 256 * 1024 * 1024,  -- 256MB vinyl cache
    vinyl_max_tuple_size = 10 * 1024 * 1024
}
```

### MVCC & Transactions

**Multi-Version Concurrency Control (MVCC)**
- Multiple versions of data coexist
- Readers don't block writers and vice versa
- Snapshot isolation by default
- Serializable isolation available

```lua
-- Start transaction with snapshot isolation
local fiber = require('fiber')
box.begin()
-- Perform reads/writes
box.commit()
```

**Isolation Levels**
- `read-committed`: Lowest isolation, best performance
- `read-confirmed`: Default, snapshot isolation
- `serializable`: Highest isolation, strict serialization

### Data Structures & Spaces

**Space Definition**
```lua
box.schema.space.create('users', {
    engine = 'memtx',
    if_not_exists = true,
    format = {
        {name = 'id', type = 'unsigned'},
        {name = 'name', type = 'string'},
        {name = 'email', type = 'string'},
        {name = 'created_at', type = 'integer'}
    }
})
```

**Index Creation**
```lua
box.space.users:create_index('primary', {
    parts = {'id'},
    if_not_exists = true
})

box.space.users:create_index('email', {
    parts = {'email'},
    unique = true,
    if_not_exists = true
})
```

### Replication Fundamentals

**Master-Slave Replication**
```lua
-- Master configuration
box.cfg {
    listen = '3301',
    replication_timeout = 1,
    wal_mode = 'write'
}

-- Slave connects to master
box.cfg {
    listen = '3302',
    replication = 'username:password@master:3301'
}
```

**Master-Master Replication**
- Multiple masters accept writes
- Automatic conflict resolution
- All nodes replicate to all others
- Requires careful transaction design

**Replication Topologies**
1. **Single Master**: Simple, writes to one node
2. **Master-Slave**: HA read replicas
3. **Master-Master**: Active-active, write distribution
4. **Multi-Master Chain**: Cascading replication

### WAL & Durability

**Write-Ahead Logging (WAL)**
```lua
box.cfg {
    wal_mode = 'write',        -- Fsync after each write
    wal_dir = './wal',
    wal_max_size = 268435456   -- 256MB WAL files
}
```

**Durability Guarantees**
- `off`: No persistence (memtx only)
- `write`: Fsync on every transaction
- `fsync`: Synchronous fsync (slowest, safest)

## Architecture Patterns

### Single-Instance Architecture
```
Client -> Tarantool Instance
         (All data)
```

**Use Cases**
- Development environment
- Single-machine deployments
- Bounded data sets
- Non-critical applications

**Advantages**
- Simple deployment
- No replication overhead
- Lowest latency

**Disadvantages**
- No HA or redundancy
- Single point of failure
- Limited by single machine resources

### Replicated Architecture
```
       Master Node
      /    |    \
Slave1  Slave2  Slave3
(Read-only replicas)
```

**Use Cases**
- Production deployments
- High-availability requirements
- Read scaling

**Configuration**
```lua
-- Master (write node)
box.cfg {
    listen = '3301',
    replication_timeout = 1,
    wal_mode = 'write'
}

-- Slaves (read replicas)
box.cfg {
    listen = '330X',
    read_only = true,
    replication = 'username:password@master:3301'
}
```

### Clustered Architecture (Cartridge)

```
Cartridge Cluster
├── Router 1 (Client entry points)
├── Router 2
└── Storage Group
    ├── Shard 1 (Master + Replicas)
    ├── Shard 2 (Master + Replicas)
    └── Shard N (Master + Replicas)
```

**Cartridge Features**
- Automatic failover
- Cluster topology management
- Health checks
- Role-based configuration

## Best Practices

1. **Data Modeling**
   - Design for your queries, not the data
   - Denormalize when needed for performance
   - Use appropriate data types

2. **Indexing**
   - Create indexes for all filters and joins
   - Use composite indexes for multi-column filters
   - Monitor index performance with `box.stat.vinyl()`

3. **Transaction Design**
   - Keep transactions short
   - Avoid nested transactions
   - Design for optimistic locking

4. **Replication**
   - Monitor replication lag
   - Plan failover procedures
   - Test recovery regularly

5. **Performance**
   - Profile before optimizing
   - Use `require('metrics')` for observability
   - Batch operations when possible

## Common Pitfalls

- **Memory Overflow**: Memtx limited by RAM, no spill to disk
- **Replication Lag**: High load can lag replicas
- **Index Bloat**: Too many indexes slows writes
- **Tuple Size**: Tarantool has limits on tuple sizes
- **Long Transactions**: Block other transactions

## Related Skills

- `lua-development` - Lua programming for Tarantool
- `vshard-sharding` - Distributed sharding with vshard
- `cartridge-framework` - Cluster management with Cartridge
- `tarantool-performance` - Performance optimization techniques
- `replication-ha` - High-availability configurations
