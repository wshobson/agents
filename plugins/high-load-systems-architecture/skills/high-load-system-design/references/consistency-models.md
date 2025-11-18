# Consistency Models Reference

## Strong Consistency

**Definition**: All clients see the same data at the same time.

**Guarantees**:
- Linearizability: Operations appear atomic
- Read-your-writes: Clients see their own writes immediately
- Monotonic reads: Successive reads never return older data

**Implementation**: 
- Consensus protocols (Praft, Paxos)
- Synchronous replication
- Single-leader architecture

**Trade-offs**:
- High write latency (wait for quorum)
- Lower availability (CAP theorem)
- Limited scalability

**Use Cases**:
- Financial transactions
- Inventory management
- Reservation systems

---

## Eventual Consistency

**Definition**: Given enough time without updates, all replicas converge to the same value.

**Guarantees**:
- No immediate consistency
- Eventually consistent (seconds to minutes)
- High availability

**Implementation**:
- Asynchronous replication
- Anti-entropy (gossip protocols)
- Conflict resolution (last-write-wins, CRDTs)

**Trade-offs**:
- Read-after-write inconsistency
- Complex application logic
- Potential for conflicts

**Use Cases**:
- Social media feeds
- Product catalogs
- Cache layers

---

## Causal Consistency

**Definition**: Operations that are causally related are seen in the same order.

**Example**:
```
User A posts message: "Hello"
User B replies: "Hi there"

All users see:
1. "Hello" (User A)
2. "Hi there" (User B)

Never reversed (would violate causality).
```

**Implementation**:
- Version vectors
- Logical clocks (Lamport timestamps)
- Happens-before relationships

**Use Cases**:
- Collaborative editing
- Chat applications
- Comment threads

---

## Comparison Table

| Model | Consistency | Availability | Performance | Complexity |
|-------|-------------|--------------|-------------|------------|
| Strong | Highest | Low | Slow | Low |
| Causal | Medium | Medium | Medium | Medium |
| Eventual | Lowest | Highest | Fast | High |
