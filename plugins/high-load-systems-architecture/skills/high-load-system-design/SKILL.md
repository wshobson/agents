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

### Event-Driven Architecture
```
Service A → Event Bus (Kafka/RabbitMQ) → Service B, Service C
```
- Loose coupling between services
- Asynchronous processing
- Event sourcing for audit trails
- Eventual consistency trade-offs
- Use cases: Real-time analytics, notifications, workflow orchestration

### CQRS (Command Query Responsibility Segregation)
```
Write Side: Commands → Write Model → Event Store
Read Side: Events → Read Model(s) → Queries
```
- Separate models for reads and writes
- Optimized read models (denormalized, cached)
- Scalable read path independent of write path
- Event sourcing often paired with CQRS
- Trade-off: Complexity, eventual consistency

### Saga Pattern (Distributed Transactions)
**Choreography-Based Saga**
```
Order Service → Payment Service → Inventory Service
     ↓ (events)      ↓ (events)        ↓ (events)
Compensating transactions if any step fails
```
- Each service listens to events and triggers next step
- No central coordinator
- Decentralized decision-making

**Orchestration-Based Saga**
```
Saga Orchestrator
  ↓ coordinates
Order Service, Payment Service, Inventory Service
```
- Central coordinator manages workflow
- Easier to reason about flow
- Single point of failure risk

### API Gateway Pattern
```
Client → API Gateway → Service1, Service2, Service3
```
- Single entry point for clients
- Rate limiting, authentication, authorization
- Request routing and aggregation
- Protocol translation (REST to gRPC)
- Operational visibility (metrics, tracing)

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

### Service Mesh Pattern
```
Service A → Sidecar Proxy (Envoy) → Sidecar Proxy → Service B
```
- Observability (distributed tracing, metrics)
- Traffic management (canary deployments, A/B testing)
- Security (mTLS, authorization policies)
- Resilience (retries, timeouts, circuit breakers)
- Examples: Istio, Linkerd, Consul Connect

### Rate Limiting Strategies

**Token Bucket Algorithm**
```
Bucket capacity: N tokens
Refill rate: R tokens per second
Request: consumes 1 token
If bucket empty → reject request
```
- Burst handling: allows bursts up to bucket capacity
- Smooth refill: gradual token replenishment
- Use case: API rate limiting

**Leaky Bucket Algorithm**
```
Queue capacity: N requests
Process rate: R requests per second
Incoming request → queue
If queue full → reject request
```
- Smooths traffic: processes at constant rate
- No bursts: strict rate enforcement
- Use case: Traffic shaping

**Sliding Window Counter**
```
Track requests in time windows (e.g., 1 minute)
Window slides continuously (not fixed intervals)
Limit: X requests per window
```
- Accurate rate limiting
- Prevents window boundary gaming
- Use case: User quotas

### Backpressure Mechanisms
- Reject requests when overloaded (fail fast)
- Queue with bounded capacity (shed load when full)
- Throttle upstream producers (reactive streams)
- Exponential backoff for retries
- Circuit breaker to prevent cascading failures

## Optimization Techniques

### Database Query Optimization
- Add indexes on frequently filtered columns (B-tree, hash, GiST)
- Analyze query execution plans (EXPLAIN ANALYZE)
- Batch operations to reduce round-trips
- Use read replicas for read-heavy queries
- Archive old data to separate storage (partitioning, cold storage)
- Use connection pooling (PgBouncer, HikariCP)
- Query result caching (Redis, application-level)
- Denormalization for read-heavy workloads

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

### Observability Patterns

**Distributed Tracing**
```
Request ID propagated across services
Service A (span) → Service B (span) → Service C (span)
Trace: collection of all spans for a request
```
- Tools: OpenTelemetry, Jaeger, Zipkin
- Visualize latency breakdown across services
- Identify bottlenecks in request flow

**Metrics Collection**
```
Application → Metrics Exporter → Prometheus → Grafana
```
- RED metrics: Rate, Errors, Duration
- USE metrics: Utilization, Saturation, Errors
- SLI/SLO/SLA tracking

**Log Aggregation**
```
Services → Log Shipper → Central Store → Search/Analysis
```
- Structured logging (JSON format)
- Correlation IDs for tracing
- Tools: ELK stack, Loki, ClickHouse

## Troubleshooting High-Load Systems

### Performance Degradation

**Symptoms**: Increased latency, reduced throughput, timeouts

**Diagnosis Steps**:
```bash
# 1. Check system resources
top -b -n 1 | head -20
free -h
df -h

# 2. Check application metrics
# CPU usage, memory consumption, thread count
ps aux | grep java | awk '{print $3, $4, $11}'

# 3. Network connectivity
netstat -an | grep ESTABLISHED | wc -l  # Connection count
ss -s  # Socket statistics

# 4. Database connections
# Check connection pool exhaustion
SHOW PROCESSLIST;  # MySQL
SELECT * FROM pg_stat_activity;  # PostgreSQL

# 5. Application logs
tail -n 1000 /var/log/app.log | grep -i error
journalctl -u myapp.service -n 100
```

**Common Causes & Solutions**:

1. **Database Connection Pool Exhaustion**
   - Symptom: "Too many connections" errors
   - Solution: Increase pool size, add connection pooling (PgBouncer, HikariCP)
   - Verify: Check pool metrics, active vs idle connections

2. **Memory Leak**
   - Symptom: Gradually increasing memory usage, OOM kills
   - Diagnosis: `jmap -heap <pid>` (Java), `pmap -x <pid>`, memory profiling
   - Solution: Analyze heap dumps, fix memory leaks, tune GC

3. **Thread Pool Exhaustion**
   - Symptom: Requests queuing, worker threads maxed out
   - Solution: Increase thread pool size, optimize blocking operations
   - Verify: Thread dump analysis `jstack <pid>` or `kill -3 <pid>`

4. **Network Saturation**
   - Symptom: High packet loss, retransmissions
   - Diagnosis: `iftop`, `nethogs`, `tcpdump`
   - Solution: Scale out, optimize payload size, enable compression

### Database Performance Issues

**Slow Queries**:
```bash
# MySQL slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;  # Log queries > 2 seconds

# PostgreSQL
ALTER SYSTEM SET log_min_duration_statement = 2000;  # milliseconds
SELECT pg_reload_conf();

# Analyze query execution plan
EXPLAIN ANALYZE SELECT ...;

# Check for missing indexes
SELECT * FROM sys.schema_unused_indexes;  # MySQL
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;  # PostgreSQL
```

**Solutions**:
- Add indexes on frequently queried columns
- Optimize JOIN operations (use INNER JOIN over subqueries)
- Denormalize for read-heavy workloads
- Use read replicas for reporting queries
- Implement query result caching

**Lock Contention**:
```bash
# MySQL
SHOW ENGINE INNODB STATUS;
SELECT * FROM information_schema.INNODB_LOCKS;

# PostgreSQL
SELECT * FROM pg_locks WHERE NOT granted;
SELECT * FROM pg_stat_activity WHERE wait_event IS NOT NULL;
```

**Solutions**:
- Reduce transaction scope (smaller, shorter transactions)
- Use optimistic locking where possible
- Implement row-level locking instead of table-level
- Consider MVCC-friendly patterns

### Cache-Related Issues

**Cache Stampede (Thundering Herd)**:
- **Problem**: Multiple requests simultaneously fetch same expired cache key
- **Solution**: Probabilistic early expiration, cache warming, locking

```python
# Probabilistic early expiration
import random
def get_with_early_expiration(key, ttl=3600):
    remaining_ttl = cache.ttl(key)
    if remaining_ttl < ttl * 0.1 * random.random():
        # Refresh cache early with probability
        refresh_cache(key)
    return cache.get(key)

# Lock-based approach
def get_with_lock(key):
    value = cache.get(key)
    if value is None:
        lock_key = f"lock:{key}"
        if cache.set(lock_key, "1", nx=True, ex=10):  # 10 sec lock
            try:
                value = fetch_from_db(key)
                cache.set(key, value, ex=3600)
            finally:
                cache.delete(lock_key)
        else:
            # Wait for other thread to populate
            time.sleep(0.1)
            return get_with_lock(key)
    return value
```

**Cache Hotspots**:
- **Problem**: Single key accessed very frequently, overwhelming cache node
- **Diagnosis**: Redis `MONITOR` command, slow log
- **Solutions**:
  - Local in-process cache (L1 cache) + distributed cache (L2)
  - Key replication across multiple cache nodes
  - Request coalescing at application layer

### Service Mesh / Microservices Issues

**Circuit Breaker Not Triggering**:
```bash
# Check circuit breaker metrics
curl http://localhost:9090/actuator/metrics/resilience4j.circuitbreaker.state

# Verify configuration
# Ensure thresholds are appropriate
resilience4j.circuitbreaker:
  instances:
    backendA:
      failure-rate-threshold: 50  # Open circuit at 50% failure rate
      wait-duration-in-open-state: 10s
      sliding-window-size: 100
```

**Service Discovery Stale Entries**:
- **Problem**: Load balancer routing to dead instances
- **Diagnosis**: Check service registry (Consul, Eureka)
- **Solution**: Reduce TTL, implement active health checks

```bash
# Consul health check
curl http://localhost:8500/v1/health/service/myservice
# Remove unhealthy instances manually if needed
curl -X PUT http://localhost:8500/v1/agent/service/deregister/myservice-1
```

**Distributed Tracing Gaps**:
- **Problem**: Missing spans, incomplete traces
- **Solution**: Ensure trace context propagation across all services

```python
# Propagate trace context in HTTP headers
from opentelemetry import trace
from opentelemetry.propagate import inject

headers = {}
inject(headers)  # Inject trace context
response = requests.get(url, headers=headers)
```

### Load Balancing Issues

**Uneven Load Distribution**:
```bash
# Check backend server request counts
# NGINX
curl http://localhost/nginx_status

# HAProxy
echo "show stat" | socat stdio /var/run/haproxy.sock

# Verify consistent hashing is working
# For cache/database sharding
```

**Solutions**:
- Switch from round-robin to least-connections algorithm
- Implement weighted load balancing based on server capacity
- Use power-of-two-choices for better distribution
- Monitor server health and adjust weights dynamically

### Message Queue Backlogs

**Kafka Consumer Lag**:
```bash
# Check consumer group lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-group --describe

# Topic partition distribution
kafka-topics.sh --describe --topic my-topic --bootstrap-server localhost:9092
```

**Solutions**:
- Increase consumer parallelism (more partitions, more consumers)
- Optimize message processing (reduce per-message overhead)
- Batch message consumption
- Scale out consumer groups

**RabbitMQ Queue Buildup**:
```bash
# Check queue depth
rabbitmqctl list_queues name messages consumers

# Monitor memory usage
rabbitmqctl status | grep memory
```

**Solutions**:
- Add more consumers
- Implement message TTL and dead-letter queues
- Increase prefetch count for better throughput
- Enable lazy queues for large backlogs

### API Gateway Bottlenecks

**Rate Limiting False Positives**:
- **Problem**: Legitimate users getting rate limited
- **Solution**: Implement sliding window counters, per-user quotas
- **Better approach**: Adaptive rate limiting based on backend capacity

**Authentication Overhead**:
```bash
# Profile JWT validation time
# If slow, consider:
# 1. Cache decoded tokens (with short TTL)
# 2. Use symmetric signing (HS256) instead of RSA
# 3. Implement token blacklist with bloom filters
```

## Real-World Case Studies

### Netflix Architecture
- **Scale**: 220M+ subscribers, 200M+ requests/sec
- **Patterns**: Microservices, event-driven, chaos engineering
- **Storage**: Cassandra for distributed database, S3 for content
- **CDN**: Open Connect for content delivery
- **Resilience**: Hystrix circuit breakers, Chaos Monkey

### Amazon Architecture
- **Scale**: 300M+ customers, 1.6M transactions/sec (Prime Day)
- **Patterns**: Service-oriented architecture, two-pizza teams
- **Storage**: DynamoDB for NoSQL, Aurora for relational
- **Caching**: ElastiCache (Redis/Memcached)
- **Queuing**: SQS for async processing, Kinesis for streaming

### LinkedIn Architecture
- **Scale**: 900M+ members, 100K+ events/sec
- **Patterns**: Event-driven with Kafka, microservices
- **Storage**: Espresso (distributed database), Venice (derived data)
- **Real-time**: Samza for stream processing
- **Analytics**: Pinot for real-time analytics

### Twitter Architecture
- **Scale**: 400M+ users, 6K tweets/sec average (70K peak)
- **Patterns**: Timeline fanout (push vs pull), caching
- **Storage**: Manhattan (distributed database), sharded MySQL
- **Caching**: Multi-tier cache (L1: in-process, L2: Redis)
- **Real-time**: Firehose for event streaming

## References

### Design Patterns
- `/references/scaling-patterns.md` - Detailed scaling patterns
- `/references/consistency-models.md` - Consistency models deep-dive
- `/references/replication-strategies.md` - Replication pattern analysis
- `/references/event-driven-architecture.md` - Event-driven patterns
- `/references/saga-patterns.md` - Distributed transaction patterns

### Case Studies
- `/assets/case-study-netflix-scaling.md` - Netflix architecture
- `/assets/case-study-amazon-infrastructure.md` - Amazon infrastructure
- `/assets/case-study-linkedin-kafka.md` - LinkedIn event streaming
- `/assets/case-study-twitter-timeline.md` - Twitter timeline architecture

### Tools & Frameworks
- `/references/architecture-tools.md` - Architecture planning tools
- `/references/benchmarking-tools.md` - Performance measurement tools
- `/references/observability-stack.md` - Monitoring and tracing tools
