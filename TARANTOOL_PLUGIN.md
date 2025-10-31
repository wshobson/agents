# Tarantool Development Plugin

## Overview

Complete Tarantool development plugin with expert architect, comprehensive skills, and orchestration commands for building distributed in-memory database applications.

**Version:** 1.0.0
**Category:** Database
**Language Support:** Russian & English

## What's Included

### 🤖 Agent (1)

**tarantool-architect** - Sonnet Model
- Expert in distributed in-memory database architecture
- Specializes in Lua application development
- Masters Cartridge clustering and vshard sharding
- Handles replication, HA, and production deployments
- Responds in Russian when input is in Russian

### 🎓 Skills (6)

1. **tarantool-architecture** (276 lines)
   - In-memory storage engines (memtx, vinyl)
   - MVCC and transaction processing
   - Replication topologies and WAL
   - Data modeling patterns
   - Architecture patterns for scale

2. **lua-development** (333 lines)
   - Lua programming for Tarantool
   - CRUD operations and transactions
   - Stored procedures and triggers
   - Fiber-based concurrency
   - Module development

3. **vshard-sharding** (311 lines)
   - Distributed sharding framework
   - Bucket management
   - Router and storage configuration
   - Automatic rebalancing
   - Shard topology planning

4. **cartridge-framework** (366 lines)
   - Cluster management with Cartridge
   - Role-based architecture
   - HTTP API development
   - Automatic failover
   - Admin UI features

5. **tarantool-performance** (126 lines)
   - Performance profiling and optimization
   - Index optimization strategies
   - Memory management
   - Query optimization
   - Benchmarking techniques

6. **replication-ha** (133 lines)
   - Replication topologies
   - WAL configuration
   - Failover procedures
   - Backup and recovery strategies
   - Disaster recovery planning

### ⚙️ Commands (3)

1. **tarantool-data-model**
   - Design optimized Tarantool data models
   - Analyze workloads and access patterns
   - Create efficient schemas
   - Plan index strategies
   - Validate performance

2. **tarantool-application-dev**
   - Develop complete Tarantool applications
   - Implement Lua business logic
   - Create stored procedures and triggers
   - Build REST API endpoints
   - Testing and deployment

3. **tarantool-cluster-ops**
   - Setup production clusters
   - Plan cluster capacity
   - Configure replication
   - Setup backup/recovery
   - Implement monitoring
   - Disaster recovery procedures

## Features

✅ **Comprehensive Coverage**
- Single-instance to multi-region clusters
- All aspects from data modeling to operations
- Production-ready patterns and practices

✅ **Russian Language Support**
- Full Russian support on all components
- Automatic language detection
- Russian and English responses

✅ **Production Ready**
- High-availability configurations
- Backup and disaster recovery
- Monitoring and observability
- Operational procedures

✅ **Real-World Patterns**
- Master-slave replication
- Master-master replication
- Distributed sharding with vshard
- Multi-region deployments

## Usage Examples

### Architecture Design (Russian)

```
Запрос: "Спроектируй распределённую базу данных для 10 миллионов пользователей"

Ответ: Полное предложение архитектуры с:
- Выбором хранилища (memtx/vinyl)
- Стратегией шардирования с vshard
- Топологией репликации
- Оценкой производительности
- Рекомендациями Cartridge
```

### Lua Application (English)

```
Request: "Build a Tarantool application with stored procedures and REST API"

Response: Complete implementation including:
- Data model with spaces and indexes
- Lua modules and functions
- Stored procedures with transactions
- REST API with HTTP handlers
- Testing and deployment guide
```

### Cluster Operations (Russian)

```
Запрос: "Настрой production Tarantool кластер с высокой доступностью"

Ответ: Пошаговая инструкция по:
- Планированию емкости
- Конфигурации репликации
- Настройке backup/recovery
- Мониторингу кластера
- Процедурам failover
```

## Architecture Patterns

### Single-Instance (Development)
```
Client → Tarantool Instance
         (All data)
```

### Replicated Cluster (Production)
```
    Master (Write)
    /    |    \
Replica Replica Replica (Read)
```

### Distributed Sharding
```
Routers → vshard → Shards (Master + Replicas)
                   ├─ Shard 1
                   ├─ Shard 2
                   └─ Shard N
```

### Cartridge Cluster
```
Cartridge Cluster
├── Routers (Stateless)
├── Storage (Stateful)
│   ├── Replica Group 1
│   ├── Replica Group 2
│   └── Replica Group N
└── Control Plane (Admin UI)
```

## Topics Covered

**Core Tarantool:**
- In-memory storage engines
- MVCC and transactions
- Replication and WAL
- Indexes and data structures
- Durability guarantees

**Lua Programming:**
- CRUD operations
- Stored procedures
- Triggers and automation
- Fiber-based concurrency
- Module development

**Distributed Systems:**
- vshard sharding
- Cartridge clustering
- Replication topologies
- Multi-region setup
- Automatic failover

**Production Operations:**
- Backup and recovery
- Performance optimization
- Monitoring and observability
- Disaster recovery
- Scaling strategies

## Integration

Works seamlessly with other plugins:
- **kubernetes-operations**: Deploy Tarantool on Kubernetes
- **observability-monitoring**: Monitor Tarantool clusters
- **cicd-automation**: Automate Tarantool deployments
- **documentation-generation**: Generate API docs

## Statistics

| Component | Count | Lines |
|-----------|-------|-------|
| Agents | 1 | 139 |
| Skills | 6 | 1,145 |
| Commands | 3 | 335 |
| **Total** | **10** | **2,019** |

## Quick Start

1. **Use the Agent**
   ```
   Question in Russian or English
   → tarantool-architect analyzes and responds in your language
   ```

2. **Access Skills**
   - `tarantool-architecture` - for architecture guidance
   - `lua-development` - for Lua code patterns
   - `vshard-sharding` - for sharding setup
   - `cartridge-framework` - for cluster management
   - `tarantool-performance` - for optimization
   - `replication-ha` - for HA setup

3. **Use Commands**
   - `tarantool-data-model` - design your schema
   - `tarantool-application-dev` - build your app
   - `tarantool-cluster-ops` - operate production clusters

## Documentation

Each skill includes:
- Core concepts and theory
- Code examples
- Best practices
- Common pitfalls
- Related skills

## Language Support

All components support automatic language detection:

```
Russian Input → Russian Response
English Input → English Response
Mixed Input → Primary Language Response
```

Technical terms, code, and system names maintain their original form.

## Examples

**Design a real-time analytics database**
- Use skill: `tarantool-architecture`
- Use command: `tarantool-data-model`
- Use agent: for architecture advice

**Build a session storage service**
- Use skill: `lua-development`
- Use command: `tarantool-application-dev`
- Use agent: for optimization advice

**Setup multi-region cluster**
- Use skill: `vshard-sharding`, `replication-ha`
- Use command: `tarantool-cluster-ops`
- Use agent: for topology advice

## Best Practices

✓ **Data Modeling**: Design schemas for your access patterns
✓ **Indexing**: Create indexes for all filters and joins
✓ **Transactions**: Keep transactions short and simple
✓ **Replication**: Plan for HA and disaster recovery
✓ **Performance**: Profile before optimizing
✓ **Monitoring**: Setup observability from the start

## Support Resources

- **Official Tarantool Docs**: https://tarantool.io/
- **Cartridge Docs**: https://www.tarantool.io/en/doc/latest/reference/cartridge/
- **vshard Docs**: https://www.tarantool.io/en/doc/latest/reference/reference_lua/vshard/
- **Lua API Docs**: https://www.tarantool.io/en/doc/latest/reference/reference_lua/box/

---

**Created:** October 31, 2025
**Version:** 1.0.0
**Status:** Production Ready

🚀 Ready to build Tarantool applications!
