# Scaling Patterns Reference

## Horizontal Scaling Patterns

### Pattern 1: Stateless Service Scaling

**Description**: Design services without server-side state to enable unlimited replication.

**Architecture**:
```
Load Balancer
├─ App Server 1 (stateless)
├─ App Server 2 (stateless)
├─ App Server 3 (stateless)
└─ App Server N (stateless)
     ↓
Shared State Store (Redis, Database)
```

**Implementation**:
- Store session data in external cache (Redis)
- Use JWT tokens for authentication (avoid server-side sessions)
- Design APIs to be idempotent
- Use distributed caching for shared data

**Benefits**:
- Easy to add/remove instances
- Perfect for containerized deployments
- Auto-scaling friendly
- Fault tolerance through redundancy

**Trade-offs**:
- Network overhead for external state access
- Complexity in managing distributed state
- Cache consistency challenges

**Use Cases**:
- Web applications
- API services
- Microservices architectures

---

### Pattern 2: Database Read Scaling

**Description**: Separate read and write operations to scale reads independently.

**Architecture**:
```
Application Layer
├─ Writes → Primary Database
└─ Reads → Read Replicas (1-N)
```

**Implementation**:
```python
# Write to primary
def create_user(data):
    return primary_db.insert(users, data)

# Read from replica
def get_user(user_id):
    return read_replica.query(users, user_id)
```

**Replication Strategies**:
1. **Asynchronous Replication** (most common)
   - Low write latency
   - Eventual consistency on reads
   - Risk of replication lag

2. **Semi-Synchronous Replication**
   - Wait for at least one replica
   - Balance between consistency and performance
   - Used in MySQL semi-sync replication

**Benefits**:
- Scales read throughput linearly
- Read replicas can be geographically distributed
- Minimal impact on write performance

**Trade-offs**:
- Replication lag (seconds to minutes)
- Read-after-write consistency challenges
- Complexity in failover procedures

**Use Cases**:
- Read-heavy applications (90%+ reads)
- Analytics and reporting
- Geographic distribution

---

### Pattern 3: Database Sharding

**Description**: Partition data across multiple database instances.

**Sharding Strategies**:

#### A. Hash-Based Sharding
```python
shard_id = hash(user_id) % num_shards
database = get_shard(shard_id)
```

**Benefits**:
- Even distribution
- Simple implementation

**Trade-offs**:
- Rebalancing requires rehashing
- Cross-shard queries expensive

#### B. Range-Based Sharding
```python
if user_id < 1_000_000:
    database = shard_1
elif user_id < 2_000_000:
    database = shard_2
else:
    database = shard_3
```

**Benefits**:
- Range queries efficient
- Easy to understand

**Trade-offs**:
- Risk of hot shards
- Manual rebalancing

#### C. Geographic Sharding
```python
if user.region == 'US':
    database = us_shard
elif user.region == 'EU':
    database = eu_shard
else:
    database = apac_shard
```

**Benefits**:
- Low latency (data locality)
- Compliance with data residency laws

**Trade-offs**:
- Complex cross-region queries
- Uneven load distribution

**Implementation Considerations**:
- Shard key selection (immutable, high cardinality)
- Handling cross-shard transactions
- Rebalancing strategy
- Backup and recovery per shard

---

### Pattern 4: Cache-Aside (Lazy Loading)

**Description**: Application manages cache explicitly.

**Flow**:
```
1. Check cache
2. If cache miss:
   a. Fetch from database
   b. Store in cache
   c. Return data
3. If cache hit:
   Return cached data
```

**Implementation**:
```python
def get_user(user_id):
    # Try cache first
    user = cache.get(f"user:{user_id}")
    if user:
        return user

    # Cache miss - fetch from database
    user = database.get(user_id)

    # Store in cache
    cache.set(f"user:{user_id}", user, ttl=3600)

    return user
```

**Benefits**:
- Simple to implement
- Flexible (application controls caching logic)
- Works with any storage backend

**Trade-offs**:
- Cache stampede risk (many requests for same key)
- Stale data possible
- Application complexity

**Optimization: Probabilistic Early Expiration**
```python
def get_user(user_id):
    cached = cache.get(f"user:{user_id}")
    if cached:
        # Refresh cache probabilistically before expiration
        if random.random() < 0.1 * (time.now() - cached.timestamp) / cached.ttl:
            asyncio.create_task(refresh_cache(user_id))
        return cached.data

    return fetch_and_cache(user_id)
```

---

### Pattern 5: Write-Through Cache

**Description**: Cache is updated synchronously with database writes.

**Flow**:
```
1. Write to cache
2. Write to database
3. Return success
```

**Implementation**:
```python
def update_user(user_id, data):
    # Update cache
    cache.set(f"user:{user_id}", data, ttl=3600)

    # Update database
    database.update(user_id, data)

    return True
```

**Benefits**:
- Cache always consistent with database
- No cache stampede
- Simple read path

**Trade-offs**:
- Higher write latency
- Wasted cache space (infrequently read data)
- Database failure affects cache

---

### Pattern 6: Event-Driven Scaling

**Description**: Decouple components using event streams.

**Architecture**:
```
Producer Services
    ↓ (publish events)
Event Bus (Kafka, RabbitMQ)
    ↓ (subscribe to events)
Consumer Services (multiple instances)
```

**Implementation with Kafka**:
```python
# Producer
def create_order(order_data):
    order = database.insert(orders, order_data)
    kafka.publish('orders.created', {
        'order_id': order.id,
        'user_id': order.user_id,
        'amount': order.amount
    })

# Consumer (scales independently)
def handle_order_created(event):
    send_email(event.user_id, event.order_id)
    update_inventory(event.items)
    log_analytics(event)
```

**Benefits**:
- Loose coupling
- Independent scaling of consumers
- Event replay capability
- Async processing

**Trade-offs**:
- Eventual consistency
- Event ordering challenges
- Increased operational complexity

---

### Pattern 7: CQRS (Command Query Responsibility Segregation)

**Description**: Separate read and write data models.

**Architecture**:
```
Commands (Writes)
    ↓
Write Model (normalized, ACID)
    ↓ (events)
Event Store
    ↓ (projections)
Read Models (denormalized, optimized)
    ↑
Queries (Reads)
```

**Implementation**:
```python
# Write side (commands)
def create_order(command):
    order = Order(
        id=command.order_id,
        user_id=command.user_id,
        items=command.items
    )
    event_store.append('orders', [
        OrderCreated(order.id, order.user_id),
        ItemsAdded(order.id, order.items)
    ])

# Read side (queries)
def get_order_summary(order_id):
    # Read from optimized view
    return read_db.get('order_summaries', order_id)

# Projection (event handler)
def project_order_summary(event):
    if isinstance(event, OrderCreated):
        read_db.create('order_summaries', {
            'id': event.order_id,
            'user_id': event.user_id,
            'status': 'created'
        })
```

**Benefits**:
- Optimized read and write models
- Independent scaling
- Event sourcing integration
- Complex query support

**Trade-offs**:
- High complexity
- Eventual consistency
- Duplicate data storage

---

## Vertical Scaling Patterns

### Pattern 8: Resource Optimization

**Techniques**:

#### CPU Optimization
- Use efficient algorithms (O(n log n) vs O(n²))
- Profile and optimize hot paths
- Parallelize workloads across cores
- Use CPU-efficient data structures

#### Memory Optimization
- Object pooling (reduce GC pressure)
- Memory-mapped files for large datasets
- Compression (trade CPU for memory)
- Efficient serialization (Protobuf vs JSON)

#### I/O Optimization
- Batch operations
- Async I/O (non-blocking)
- Buffering and prefetching
- SSD over HDD

**Example: Connection Pooling**
```python
# Without pooling (creates new connection each time)
def query_database():
    conn = create_connection()  # Expensive
    result = conn.execute(query)
    conn.close()
    return result

# With pooling (reuses connections)
pool = ConnectionPool(size=10)

def query_database():
    with pool.get_connection() as conn:
        return conn.execute(query)
```

---

## Auto-Scaling Patterns

### Pattern 9: Metric-Based Auto-Scaling

**Metrics**:
1. **CPU Utilization** (target: 70%)
2. **Memory Usage** (target: 80%)
3. **Request Queue Depth** (target: < 100)
4. **Response Time** (target: < 200ms p99)

**Implementation (Kubernetes HPA)**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-autoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: http_requests_per_second
      target:
        type: AverageValue
        averageValue: "1000"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100  # Double capacity
        periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50  # Reduce by 50%
        periodSeconds: 60
```

---

### Pattern 10: Predictive Scaling

**Description**: Scale based on predicted load patterns.

**Implementation**:
```python
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_load():
    # Historical data: hour of day → request count
    X = np.array([[0], [1], [2], ..., [23]])
    y = np.array([100, 80, 60, ..., 120])

    model = LinearRegression()
    model.fit(X, y)

    # Predict next hour
    next_hour = datetime.now().hour + 1
    predicted_load = model.predict([[next_hour]])[0]

    # Scale accordingly
    desired_capacity = predicted_load / 1000  # 1000 RPS per instance
    update_autoscaler(desired_capacity)
```

**Benefits**:
- Proactive scaling (no cold start delay)
- Handles predictable traffic patterns
- Cost optimization

**Trade-offs**:
- Complex implementation
- Requires historical data
- May overscale for unpredictable traffic

---

## Geographic Scaling Patterns

### Pattern 11: Multi-Region Active-Active

**Architecture**:
```
          Global Load Balancer (DNS-based)
                 /              \
     US Region (Primary)    EU Region (Primary)
          |                        |
    [App Servers]            [App Servers]
          |                        |
  [Regional Database]      [Regional Database]
          |                        |
    Cross-Region Replication (bi-directional)
```

**Implementation**:
- GeoDNS routing (Route 53, Cloudflare)
- Active-active database replication (CockroachDB, DynamoDB Global Tables)
- Conflict resolution strategy (last-write-wins, CRDTs)

**Benefits**:
- Low latency worldwide
- High availability (no single point of failure)
- Disaster recovery

**Trade-offs**:
- High cost (duplicate infrastructure)
- Complex conflict resolution
- Consistency challenges

---

### Pattern 12: Multi-Region Active-Passive

**Architecture**:
```
         Global Load Balancer
                 ↓
         US Region (Active)
               |
         [App Servers]
               |
         [Primary Database] ─┐
                             │ (async replication)
         EU Region (Passive) │
               |              ↓
         [Standby Servers] [Replica Database]
```

**Failover Process**:
1. Detect primary region failure (health checks)
2. Promote EU replica to primary
3. Update DNS to route traffic to EU
4. Redirect all traffic to EU region

**Benefits**:
- Lower cost than active-active
- Disaster recovery
- Regional compliance

**Trade-offs**:
- Higher latency for some users
- Manual or semi-automatic failover
- Data loss possible (replication lag)

---

## Cost Optimization Patterns

### Pattern 13: Serverless Scaling

**Use Cases**:
- Sporadic workloads
- Event-driven processing
- Low traffic APIs

**Implementation (AWS Lambda)**:
```python
def lambda_handler(event, context):
    # Automatically scales from 0 to 10,000+ concurrent executions
    user_id = event['user_id']
    data = process_user(user_id)
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
```

**Benefits**:
- Pay-per-use (no idle costs)
- Automatic scaling
- Zero infrastructure management

**Trade-offs**:
- Cold start latency
- Execution time limits
- Vendor lock-in

---

## Summary Table

| Pattern | Scalability | Complexity | Cost | Use Case |
|---------|-------------|------------|------|----------|
| Stateless Services | Unlimited horizontal | Low | Medium | Web apps, APIs |
| Read Replicas | High read throughput | Medium | Medium | Read-heavy workloads |
| Database Sharding | Very high | High | High | Multi-tenant, global scale |
| Cache-Aside | Reduces DB load | Low | Low | General purpose |
| Event-Driven | High decoupling | Medium | Medium | Async processing |
| CQRS | Independent read/write | Very High | High | Complex domains |
| Auto-Scaling | Elastic capacity | Medium | Variable | Variable traffic |
| Multi-Region | Global reach | Very High | Very High | Global apps |
| Serverless | Infinite burst | Low | Very Low | Sporadic loads |
