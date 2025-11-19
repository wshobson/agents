---
name: distributed-systems-design
description: Проектирование distributed systems включая консистентность, доступность, partition tolerance, репликацию, sharding, consensus algorithms. Используйте когда проектируете distributed architectures, выбираете consistency models или решаете CAP theorem trade-offs.
---

# Distributed Systems Design

## Когда использовать этот скилл

- Проектирование distributed database architectures
- Выбор consistency models (strong vs eventual)
- Решение CAP theorem trade-offs
- Проектирование replication strategies
- Implementing consensus algorithms
- Designing для high availability и fault tolerance
- Handling network partitions и failures

## CAP Theorem

```yaml
CAP_Theorem:
  statement: "Можно гарантировать только 2 из 3: Consistency, Availability, Partition Tolerance"

  properties:
    Consistency:
      definition: "Все nodes видят одинаковые данные одновременно"
      example: "Read после write всегда возвращает latest value"

    Availability:
      definition: "Каждый request получает response (success или failure)"
      example: "System отвечает даже если некоторые nodes недоступны"

    Partition_Tolerance:
      definition: "System продолжает работать при network partitions"
      reality: "В distributed systems partitions неизбежны, поэтому P всегда необходим"

  practical_choices:
    CP_Systems:
      description: "Consistency + Partition Tolerance (жертвуем Availability)"
      behavior: "При partition некоторые nodes становятся unavailable"
      examples:
        - "MongoDB (с write concern majority)"
        - "HBase, BigTable"
        - "Redis (с синхронной репликацией)"
        - "Zookeeper, etcd, Consul"
      use_cases: "Financial transactions, inventory management"

    AP_Systems:
      description: "Availability + Partition Tolerance (жертвуем Consistency)"
      behavior: "При partition возвращаем stale data (eventual consistency)"
      examples:
        - "Cassandra"
        - "DynamoDB"
        - "Riak"
        - "CouchDB"
      use_cases: "Social media feeds, shopping carts, user profiles"

  PACELC_Extension:
    statement: "В случае Partition → выбор между A и C; Else → выбор между Latency и Consistency"
    explanation: "Даже без partitions есть trade-off между latency и consistency"
```

## Consistency Models

```yaml
Strong_Consistency:
  definition: "Все reads видят latest write immediately"
  implementation: "Synchronous replication ко всем replicas"
  latency: "Higher latency (wait для всех replicas)"
  examples:
    - "Google Spanner (TrueTime API)"
    - "Azure Cosmos DB (Strong consistency level)"
    - "PostgreSQL synchronous replication"

Eventual_Consistency:
  definition: "Reads могут видеть stale data, но в итоге все replicas converge"
  implementation: "Asynchronous replication"
  latency: "Lower latency (не ждем replicas)"
  conflict_resolution: "Last-write-wins, vector clocks, CRDTs"
  examples:
    - "DynamoDB (default)"
    - "Cassandra (с Quorum < ALL)"
    - "S3 (eventual consistency for overwrites)"

Causal_Consistency:
  definition: "Causally related операции видны в правильном порядке"
  example: |
    User posts comment → Comment appears → Notification sent
    Все nodes видят events в этом порядке
  implementations:
    - "MongoDB (causal consistency sessions)"
    - "Cosmos DB (Session consistency)"

Read_Your_Writes:
  definition: "User всегда видит свои собственные writes"
  implementation: "Sticky sessions, read from primary, version tracking"
  use_case: "User profile updates immediately visible to that user"

Monotonic_Reads:
  definition: "Subsequent reads не возвращают older versions"
  example: "If read v2, next read ≥ v2 (не вернет v1)"

Session_Consistency:
  definition: "Consistency в рамках одной user session"
  implementation: "Combine read-your-writes + monotonic reads"
  default_in:
    - "Azure Cosmos DB"
    - "DynamoDB (если использовать consistent reads)"
```

## Replication Patterns

```yaml
Primary_Replica:
  also_known_as: "Master-Slave, Leader-Follower"

  architecture: |
    Write → Primary → Async Replication → Replicas
    Reads ← [Primary или Replicas]

  write_path:
    - "All writes идут к primary"
    - "Primary applies change локально"
    - "Primary replicates to followers (async или sync)"

  read_path:
    strategy1: "Read from primary (strong consistency)"
    strategy2: "Read from replicas (eventual consistency, lower latency)"
    strategy3: "Read-your-writes (session affinity to primary)"

  failover:
    manual: "Admin promotes replica to primary"
    automatic: "Consensus algorithm выбирает new primary (Raft, Paxos)"
    challenge: "Split-brain (два primaries), решение через fencing"

  examples:
    - "PostgreSQL streaming replication"
    - "MySQL replication"
    - "MongoDB replica sets"

Multi_Primary:
  also_known_as: "Multi-Master"

  architecture: "Multiple primaries accept writes, replicate to each other"

  benefits:
    - "Higher write throughput"
    - "Better geographic distribution"
    - "No single point of failure"

  challenges:
    write_conflicts:
      example: "User A updates name to 'Alice' в US, User B updates to 'Alicia' в EU одновременно"
      resolution_strategies:
        - "Last-write-wins (timestamp-based)"
        - "Application-level conflict resolution"
        - "CRDTs (Conflict-free Replicated Data Types)"
        - "Vector clocks"

  examples:
    - "Cassandra (multi-datacenter)"
    - "Cosmos DB (multi-region writes)"
    - "CouchDB"

Quorum_Replication:
  concept: "Require majority agreement для reads/writes"

  formula: |
    W + R > N
    Где:
      N = total replicas
      W = write quorum
      R = read quorum

  example_configurations:
    strong_consistency:
      N: 3
      W: 2  # Write to 2 nodes
      R: 2  # Read from 2 nodes
      guarantee: "W + R = 4 > N = 3, поэтому overlap гарантирован"

    eventual_consistency:
      N: 3
      W: 1  # Faster writes
      R: 1  # Faster reads
      trade_off: "W + R = 2 < N, possible stale reads"

  tunable_consistency:
    platform: "Cassandra, DynamoDB"
    options:
      - "ONE, TWO, THREE"
      - "QUORUM (N/2 + 1)"
      - "ALL (strongest consistency)"
```

## Partitioning (Sharding)

```yaml
Partitioning_Strategies:
  Hash_Based:
    method: "hash(key) % num_partitions"
    benefits: "Uniform distribution"
    drawbacks: "Range queries inefficient, rebalancing сложный"
    example: "DynamoDB partition key"

  Range_Based:
    method: "Partition по диапазонам (A-M, N-Z)"
    benefits: "Efficient range queries"
    drawbacks: "Hotspots если data skewed"
    example: "BigTable row key ranges"

  Geographic:
    method: "Partition по region/datacenter"
    benefits: "Data locality, compliance (GDPR)"
    example: "EU users → EU shard, US users → US shard"

  Consistent_Hashing:
    purpose: "Minimize data movement при adding/removing nodes"
    concept: "Nodes и keys на hash ring, key принадлежит ближайшему node"
    virtual_nodes: "Каждый physical node → несколько virtual nodes для balance"
    examples: "Cassandra, DynamoDB, Memcached"

Hotspot_Mitigation:
  problem: "Unbalanced load (один shard получает 80% traffic)"

  solutions:
    composite_keys:
      example: "customer_id + timestamp вместо только customer_id"

    salting:
      example: "Add random suffix (user_123_01, user_123_02)"

    splitting:
      action: "Split hot partition на несколько smaller partitions"

Cross_Shard_Queries:
  problem: "Query spans multiple shards"

  solutions:
    scatter_gather:
      method: "Query all shards, merge results"
      cost: "High latency, resource usage"

    secondary_indexes:
      implementation: "Global secondary index для cross-shard queries"
      example: "DynamoDB GSI"

    denormalization:
      method: "Duplicate data в каждом shard"
      trade_off: "Storage cost за query performance"
```

## Consensus Algorithms

```yaml
Raft:
  purpose: "Leader election и log replication"

  components:
    Leader: "Handles все client requests, replicates log"
    Follower: "Passive, accept log entries from leader"
    Candidate: "Follower становится candidate при leader timeout"

  leader_election:
    trigger: "Follower не получает heartbeat от leader (timeout)"
    process: |
      1. Follower → Candidate, increment term, vote for self
      2. Request votes от других nodes
      3. Majority votes → Candidate становится Leader
      4. Leader sends heartbeats to maintain authority

  log_replication:
    process: |
      1. Client sends command to Leader
      2. Leader appends to local log
      3. Leader replicates to Followers
      4. Leader waits для majority acknowledgment
      5. Leader commits entry, applies to state machine
      6. Leader notifies Followers to commit

  safety: "At most one leader per term, committed entries never lost"

  implementations:
    - "etcd (Kubernetes metadata store)"
    - "Consul (service discovery)"
    - "CockroachDB"

Paxos:
  purpose: "Достижение consensus в distributed system"
  reputation: "Notoriously difficult to understand и implement"
  variants: "Multi-Paxos для repeated consensus"

  implementations:
    - "Google Chubby (lock service)"
    - "Apache ZooKeeper (до версии 3.6)"

Two_Phase_Commit:
  purpose: "Atomic commit для distributed transactions"

  phases:
    prepare_phase:
      - "Coordinator → Participants: 'Can you commit?'"
      - "Participants prepare transaction, reply YES или NO"

    commit_phase:
      - "If all YES → Coordinator sends COMMIT"
      - "If any NO → Coordinator sends ABORT"

  problems:
    blocking: "Coordinator failure блокирует participants"
    coordinator_spof: "Single point of failure"

  use_cases: "Limited, чаще используют Saga pattern для microservices"
```

## Справочные материалы

Для примеров см. директорию `references/`:
- CAP theorem case studies
- Consistency models comparisons
- Replication architecture diagrams
- Consensus algorithm visualizations
- Distributed database patterns

---

**Примечание**: Концепции основаны на практиках Google Spanner, Amazon DynamoDB, Azure Cosmos DB, Apache Cassandra и других distributed systems.
