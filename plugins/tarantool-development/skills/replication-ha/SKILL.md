---
name: replication-ha
description: Master Tarantool replication topologies, high-availability configurations, failover automation, and disaster recovery procedures. Use when designing resilient Tarantool systems.
---

# Tarantool Replication & High Availability

Complete guide to building highly available Tarantool systems.

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

## Purpose

Design and implement highly available Tarantool systems with automatic failover and disaster recovery.

## When to Use This Skill

- Design replication topologies
- Configure master-slave or master-master setups
- Plan disaster recovery
- Implement automatic failover
- Monitor replication health
- Perform point-in-time recovery

## Core Concepts

### Replication Topologies

**Master-Slave (Primary-Replica)**
```
Master (Write)
    |
    +---> Replica 1 (Read)
    +---> Replica 2 (Read)
    +---> Replica 3 (Read)
```

Configuration:
```lua
-- Master
box.cfg {
    listen = '3301',
    replication_timeout = 1,
    wal_mode = 'write'
}

-- Replica
box.cfg {
    listen = '330X',
    read_only = true,
    replication = 'master:3301'
}
```

**Master-Master (Active-Active)**
```
Master 1 <--replication--> Master 2
   |                            |
   +--> Replica 1         +--> Replica 3
   +--> Replica 2         +--> Replica 4
```

**Multi-Master Chain**
```
Master 1 --> Master 2 --> Master 3
```

### WAL & Durability

**Write-Ahead Log Configuration**
```lua
box.cfg {
    wal_mode = 'write',      -- Fsync on each write
    wal_dir = './wal',
    wal_max_size = 256 * 1024 * 1024,
    checkpoint_interval = 3600
}
```

### Failover Procedures

**Promoting a Replica**
```lua
-- On replica that should become master
box.cfg { read_only = false }

-- Update other replicas to point to new master
box.cfg {
    replication = 'newmaster:3301'
}
```

**Automatic Failover with Cartridge**
- Automatic health monitoring
- Leader election
- Replica promotion
- No manual intervention

## Best Practices

1. **Replication Design**
   - Use odd number of replicas
   - Separate replicas geographically
   - Monitor replication lag

2. **Backup Strategy**
   - Regular snapshots (RDB)
   - WAL archival
   - Test recovery procedures

3. **Monitoring**
   - Track replication lag
   - Monitor master health
   - Alert on failover events

4. **Disaster Recovery**
   - Document RTO/RPO targets
   - Test recovery procedures
   - Plan for total data center failure

## Related Skills

- `tarantool-architecture` - Overall cluster design
- `cartridge-framework` - Automatic failover with Cartridge
- `lua-development` - Implementing recovery logic
