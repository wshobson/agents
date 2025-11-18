---
name: high-load-system-design
description: Comprehensive guide to designing high-load distributed systems. Covers architectural patterns, scalability principles, performance optimization strategies, and trade-off analysis. Use when designing system architecture, evaluating technology choices, or planning infrastructure for high-throughput applications.
---

# High-Load System Design

## When to Use This Skill

- Designing architecture for systems handling millions of requests per second
- Planning infrastructure for high-throughput data processing
- Evaluating trade-offs between consistency, availability, and scalability
- Architecting distributed systems with specific performance targets
- Analyzing system bottlenecks and identifying optimization opportunities
- Building cost-efficient infrastructure for large-scale applications

## Core Concepts

### Scalability Principles

**Horizontal Scaling**
- Design stateless services for easy replication
- Distribute load across multiple servers
- Use consistent hashing or similar for data partitioning
- Trade-offs: Operational complexity, cross-node coordination overhead

**Vertical Scaling**
- Use more powerful hardware (CPU, RAM, storage)
- Less operational complexity but hardware limits exist
- Good for single-point bottlenecks (database, cache layer)
- Trade-offs: Hardware costs, diminishing returns as capacity increases

**Database Scaling**
- Read replicas: Master-slave with asynchronous replication
- Sharding: Partition data by key, route requests to correct shard
- Denormalization: Trade consistency for read performance
- Materialized views: Pre-computed results for common queries

### Load Distribution Patterns

**Round Robin**
- Simple distribution across servers
- Pros: Simple, fair
- Cons: Ignores server load, doesn't consider latency

**Least Connected**
- Route to server with fewest active connections
- Pros: Better load balancing than round robin
- Cons: Requires connection tracking, doesn't account for request size

**Weighted Round Robin**
- Distribute proportionally to server capacity
- Pros: Accounts for different server capabilities
- Cons: Static allocation, doesn't adapt to runtime conditions

**Consistent Hashing**
- Hash-based distribution with minimal remapping on scale
- Pros: Minimal redistribution when adding/removing servers
- Cons: Potential hot keys with skewed data distribution

**Latency-Aware Routing**
- Route based on historical latency to backends
- Pros: Optimal performance, adapts to runtime conditions
- Cons: Requires continuous latency measurement

### Caching Strategy

**Cache-Aside (Lazy Loading)**
```
On read:
  1. Check cache
  2. If miss, fetch from database
  3. Update cache
  4. Return
```
- Simple, flexible
- Can serve stale data
- Cache misses trigger database query

**Write-Through**
```
On write:
  1. Write to cache
  2. Write to database
  3. Return
```
- Guarantees cache is current
- Write latency includes database latency
- Database always consistent

**Write-Behind (Write-Back)**
```
On write:
  1. Write to cache (returns immediately)
  2. Asynchronously write to database
  3. Risk of data loss if cache fails
```
- Fast writes
- Risk of inconsistency
- Complex recovery

**Cache Eviction Policies**
- LRU (Least Recently Used): Good general-purpose
- LFU (Least Frequently Used): Good for varying access patterns
- TTL (Time-To-Live): Good with update frequency expectations
- Write-Behind with overflow to disk

### Consistency Models

**Strong Consistency**
- All clients always see latest committed data
- Simplest to reason about, hardest to scale
- Examples: SQL databases, synchronized storage

**Eventual Consistency**
- Clients may see stale data temporarily
- Scales well, complex application logic
- Examples: Distributed caches, NoSQL databases
- Convergence time from seconds to minutes

**Causal Consistency**
- Related operations preserve causality
- Balance between strong and eventual
- Medium complexity, good scalability
- Examples: DynamoDB with global tables

### Replication Strategies

**Synchronous Replication**
- Data written to all replicas before returning
- Guarantees strong consistency
- Higher write latency
- Fails if any replica unavailable

**Asynchronous Replication**
- Data written to primary only
- Returns quickly
- Risk of data loss if primary fails
- Good for high-write throughput

**Semi-Synchronous**
- Wait for some (not all) replicas to acknowledge
- Balance between durability and latency
- Common in distributed databases

### Partitioning Strategies

**Range-Based Partitioning**
```
Shard 1: User IDs 0-1M
Shard 2: User IDs 1M-2M
Shard 3: User IDs 2M-3M
```
- Simple to understand
- Risk of hot shards if access is uneven
- Rebalancing requires moving large ranges

**Hash-Based Partitioning**
```
Shard = hash(user_id) % num_shards
```
- Even distribution if hash is uniform
- Rebalancing requires rehashing
- Makes range queries complex

**Directory-Based Partitioning**
- Maintain lookup table: key -> partition
- Flexible, can balance load
- Lookup table becomes bottleneck
- Extra round-trip per request

**Geography-Based Partitioning**
```
US East Shard: Users in America
EU Shard: Users in Europe
APAC Shard: Users in Asia-Pacific
```
- Latency optimization through locality
- Can address compliance requirements
- Management complexity increases

## Architecture Patterns

### API Gateway Pattern
```
Client → API Gateway → Service1, Service2, Service3
```
- Single entry point for clients
- Rate limiting, authentication
- Request routing and aggregation
- Operational visibility

### Cache Layer
```
Client → Cache → Database
```
- Reduces database load
- Trade-off: Consistency vs performance
- Cache invalidation strategies critical
- Types: Redis, Memcached, in-process

### Database Read Replicas
```
Write to Primary → Read from Replicas
```
- Separate read and write paths
- Scales read throughput significantly
- Replication lag is challenge
- Good for read-heavy workloads

### Message Queue Pattern
```
Producer → Queue → Consumer
```
- Decouple components
- Handle traffic spikes
- Enable async processing
- Ensures message delivery

### Circuit Breaker Pattern
```
If service fails N times in duration D:
  - Fail fast without calling service
  - After timeout, try again
  - Gradual recovery with half-open state
```
- Prevents cascading failures
- Fast failure detection
- Graceful degradation

## Optimization Techniques

### Database Query Optimization
- Add indexes on frequently filtered columns
- Analyze query execution plans
- Batch operations to reduce round-trips
- Use read replicas for read-heavy queries
- Archive old data to separate storage
- Use connection pooling

### Network Optimization
- Minimize network round-trips (multiplexing, batching)
- Compress data in transit (gzip)
- Use TCP keep-alive for persistent connections
- Optimize packet sizes
- Measure and monitor latency

### Computational Optimization
- Parallel processing (multiple cores)
- Caching computed results
- Precompute when possible
- Use appropriate data structures
- Avoid unnecessary allocations
- Profile to find hot paths

## References

### Design Patterns
- `/references/scaling-patterns.md` - Detailed scaling patterns
- `/references/consistency-models.md` - Consistency models deep-dive
- `/references/replication-strategies.md` - Replication pattern analysis

### Case Studies
- `/assets/case-study-netflix-scaling.md` - Netflix architecture
- `/assets/case-study-facebook-infrastructure.md` - Facebook infrastructure
- `/assets/case-study-google-storage.md` - Google storage systems

### Tools & Frameworks
- `/references/architecture-tools.md` - Architecture planning tools
- `/references/benchmarking-tools.md` - Performance measurement tools
