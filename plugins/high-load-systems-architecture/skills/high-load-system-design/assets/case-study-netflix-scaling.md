# Netflix Scaling Case Study

## Overview

**Scale**:
- 230M+ subscribers worldwide (2023)
- 200M+ requests per second
- 15% of global internet bandwidth during peak hours
- Streams to 190+ countries

**Technology Stack**:
- Microservices: 700+ services
- Databases: Cassandra, MySQL, PostgreSQL
- Cache: EVCache (memcached-based)
- Streaming: Apache Kafka
- Compute: AWS (100% cloud since 2016)

---

## Architecture Evolution

### Phase 1: Monolithic (2007-2008)

**Architecture**:
```
Web Tier → Application Server (monolith) → Database (Oracle)
```

**Challenges**:
- Single point of failure
- Difficult to scale individual features
- Deployment complexity
- Long release cycles

---

### Phase 2: Service-Oriented Architecture (2008-2012)

**Architecture**:
```
API Gateway
├─ User Service
├─ Movie Service
├─ Recommendation Service
└─ Playback Service
```

**Migration Strategy**:
1. Identify bounded contexts
2. Extract services incrementally
3. Build API gateway for routing
4. Gradually move traffic from monolith

**Benefits Achieved**:
- Independent deployments
- Team autonomy
- Technology diversity
- Fault isolation

---

### Phase 3: Microservices at Scale (2012-Present)

**Current Architecture**:
```
Client (Web, Mobile, TV)
        ↓
Zuul (API Gateway)
        ↓
┌─────────────────────────────┐
│   700+ Microservices        │
│   - User Profile            │
│   - Recommendation          │
│   - Content Metadata        │
│   - Playback                │
│   - Analytics               │
│   - ...                     │
└─────────────────────────────┘
        ↓
┌─────────────────────────────┐
│   Data Layer                │
│   - Cassandra (metadata)    │
│   - EVCache (caching)       │
│   - S3 (content storage)    │
│   - DynamoDB (config)       │
└─────────────────────────────┘
```

---

## Key Patterns & Solutions

### 1. Content Delivery Network (Open Connect)

**Problem**: Streaming video requires massive bandwidth.

**Solution**: Custom CDN with edge servers in ISP networks.

**Architecture**:
```
Content Origin (S3)
        ↓
  Open Connect CDN
        ↓
┌────────────────────────────────┐
│ Edge Servers (ISPs)            │
│ - 10,000+ servers worldwide    │
│ - Cache popular content        │
│ - 95%+ cache hit rate          │
└────────────────────────────────┘
        ↓
  User Devices
```

**Benefits**:
- Reduced latency (< 50ms)
- Lower bandwidth costs
- Improved reliability
- Better user experience

**Implementation Details**:
- Adaptive bitrate streaming (multiple quality levels)
- Predictive pre-caching (machine learning)
- Intelligent client-side buffering
- Peer-to-peer sharing (experimental)

---

### 2. Zuul API Gateway

**Purpose**: Single entry point for all client requests.

**Responsibilities**:
- **Routing**: Direct requests to appropriate microservices
- **Authentication**: Verify user credentials
- **Rate Limiting**: Prevent API abuse
- **Metrics**: Track request patterns
- **Canary Testing**: Gradual rollout of new features

**Implementation**:
```java
@EnableZuulProxy
public class ZuulConfig {
    @Bean
    public RouteLocator routes(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("user-service", r -> r
                .path("/api/users/**")
                .filters(f -> f
                    .addRequestHeader("X-Request-ID", UUID.randomUUID())
                    .circuitBreaker(config -> config
                        .setFallbackUri("/fallback/user"))
                    .retry(3))
                .uri("lb://USER-SERVICE"))
            .build();
    }
}
```

**Performance**:
- Handles 50K+ requests/second per instance
- Sub-millisecond latency overhead
- Automatic failover to backup regions

---

### 3. Hystrix Circuit Breaker

**Problem**: Cascading failures in distributed systems.

**Solution**: Circuit breaker pattern with automatic recovery.

**States**:
```
        Closed (Normal)
              ↓ (failures exceed threshold)
        Open (Fail Fast)
              ↓ (after timeout)
        Half-Open (Test)
              ↓ (if success)
        Closed (Recovered)
```

**Implementation**:
```java
@HystrixCommand(
    fallbackMethod = "getRecommendationsFallback",
    commandProperties = {
        @HystrixProperty(name = "execution.isolation.thread.timeoutInMilliseconds", value = "1000"),
        @HystrixProperty(name = "circuitBreaker.requestVolumeThreshold", value = "20"),
        @HystrixProperty(name = "circuitBreaker.errorThresholdPercentage", value = "50"),
        @HystrixProperty(name = "circuitBreaker.sleepWindowInMilliseconds", value = "5000")
    }
)
public List<Movie> getRecommendations(String userId) {
    return recommendationService.get(userId);
}

public List<Movie> getRecommendationsFallback(String userId) {
    // Return cached or default recommendations
    return cache.get("recommendations:" + userId, () -> getDefaultRecommendations());
}
```

**Impact**:
- 99.99% uptime despite service failures
- Prevented cascading failures
- Improved user experience with fallbacks

---

### 4. Cassandra for Metadata

**Why Cassandra**:
- Linear scalability (add nodes, increase capacity)
- No single point of failure
- Tunable consistency
- High write throughput

**Data Model**:
```
Table: movie_metadata
Partition Key: movie_id
Clustering Key: version

movie_id | version | title              | release_year | genres
---------|---------|--------------------|--------------|---------
m001     | 1       | "The Irishman"     | 2019         | [crime, drama]
m001     | 2       | "The Irishman"     | 2019         | [crime, drama, history]
```

**Consistency Level**:
- Writes: QUORUM (majority of replicas)
- Reads: LOCAL_QUORUM (majority in local datacenter)
- Trade-off: Eventual consistency for high availability

**Cluster Configuration**:
```
3 AWS Regions (US East, US West, EU West)
├─ Each region: 72+ nodes
├─ Replication Factor: 3
└─ Total: 250+ nodes
```

**Performance**:
- 1M+ writes/second
- Sub-10ms p99 latency
- 99.99% availability

---

### 5. EVCache (Memcached-based Caching)

**Purpose**: Reduce database load, improve latency.

**Architecture**:
```
        Application
              ↓
   ┌──────────────────┐
   │ EVCache Client   │
   │ (with replication)│
   └──────────────────┘
              ↓
   ┌─────────────────────────┐
   │ Cache Tier (100+ nodes) │
   │ - Partitioned by key    │
   │ - Replicated (3 copies) │
   │ - TTL-based expiration  │
   └─────────────────────────┘
```

**Replication Strategy**:
- Primary copy in primary availability zone
- 2 replica copies in other zones
- Read from closest replica
- Write to all replicas (async)

**Usage Patterns**:
```java
// Cache user profile
EVCacheClient cache = new EVCacheClient("user-profiles");

// Write
cache.set("user:123", userProfile, 3600); // 1 hour TTL

// Read
UserProfile profile = cache.get("user:123");
if (profile == null) {
    profile = database.getUser(123);
    cache.set("user:123", profile, 3600);
}
```

**Performance**:
- 30M+ requests/second
- Sub-millisecond latency
- 99.5%+ hit rate

---

### 6. Chaos Engineering (Chaos Monkey)

**Purpose**: Proactively test system resilience.

**Tools**:
- **Chaos Monkey**: Randomly terminates instances
- **Chaos Kong**: Simulates entire region failure
- **Latency Monkey**: Adds artificial latency
- **FIT (Failure Injection Testing)**: Simulates specific failure scenarios

**Implementation**:
```python
# Chaos Monkey configuration
{
    "enabled": true,
    "schedule": "0 10 * * MON-FRI",  # Weekdays, 10 AM
    "target": {
        "apps": ["user-service", "movie-service"],
        "probability": 0.1  # 10% of instances
    },
    "actions": [
        {"type": "terminate", "weight": 70},
        {"type": "block_traffic", "weight": 20},
        {"type": "burn_cpu", "weight": 10}
    ]
}
```

**Benefits**:
- Discovered hidden failure modes
- Improved system resilience
- Increased confidence in disaster recovery
- Culture of resilience

**Results**:
- Survived AWS region failures (2012, 2015)
- Smooth handling of traffic spikes
- 99.99% uptime across all services

---

### 7. A/B Testing at Scale

**Purpose**: Test features with subset of users.

**Architecture**:
```
User Request
    ↓
Feature Flag Service
    ↓
┌────────────────┐
│ Experiment A   │ ← 10% of users
│ (new algorithm)│
└────────────────┘
    ↓
┌────────────────┐
│ Experiment B   │ ← 90% of users
│ (current)      │
└────────────────┘
    ↓
Analytics / Metrics
```

**Implementation**:
```java
@ExperimentFlag(name = "recommendation-algorithm")
public List<Movie> getRecommendations(User user) {
    String experiment = experiments.getAssignment(user.getId(), "recommendation-algorithm");

    if ("new-algorithm".equals(experiment)) {
        return newRecommendationEngine.get(user);
    } else {
        return currentRecommendationEngine.get(user);
    }
}
```

**Metrics Tracked**:
- Watch time (primary metric)
- Retention rate
- Click-through rate
- User satisfaction

**Scale**:
- 1,000+ experiments running concurrently
- 100M+ users in experiments
- Statistical significance in hours

---

## Key Learnings

### 1. Embrace Failure

**Principle**: Systems will fail. Design for resilience.

**Practices**:
- Circuit breakers on all external calls
- Fallback strategies for critical paths
- Chaos engineering in production
- Graceful degradation

---

### 2. Optimize for Change

**Principle**: Requirements change. Optimize for flexibility.

**Practices**:
- Small, focused microservices
- Independent deployments
- Feature flags for gradual rollouts
- Backward-compatible APIs

---

### 3. Data-Driven Decisions

**Principle**: Measure everything. Let data guide decisions.

**Practices**:
- A/B testing for all features
- Real-time metrics and dashboards
- Anomaly detection and alerting
- Post-mortem analysis of incidents

---

### 4. Infrastructure as Code

**Principle**: Automate everything. Treat infrastructure as code.

**Practices**:
- Terraform for infrastructure provisioning
- Immutable deployments (no manual changes)
- Automated rollbacks
- Infrastructure version control

---

## Performance Numbers

| Metric | Value |
|--------|-------|
| Subscribers | 230M+ |
| Requests/second | 200M+ |
| Data processed/day | 2+ petabytes |
| Microservices | 700+ |
| AWS instances | 100,000+ |
| Cassandra writes/sec | 1M+ |
| EVCache requests/sec | 30M+ |
| Deployments/day | 4,000+ |
| Chaos Monkey kills/day | 100+ instances |
| Uptime | 99.99% |

---

## References

- Netflix Tech Blog: https://netflixtechblog.com/
- Chaos Engineering: https://principlesofchaos.org/
- Zuul Gateway: https://github.com/Netflix/zuul
- Hystrix: https://github.com/Netflix/Hystrix
- EVCache: https://github.com/Netflix/EVCache
