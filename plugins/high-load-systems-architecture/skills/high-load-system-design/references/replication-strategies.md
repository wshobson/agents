# Replication Strategies

## Synchronous Replication
- Write to all replicas before ACK
- Strong consistency
- High latency, lower availability

## Asynchronous Replication  
- Write to primary only, replicate async
- Low latency, high availability
- Eventual consistency, data loss risk

## Semi-Synchronous
- Wait for N replicas (quorum)
- Balance consistency/performance
- Configurable N value

## Multi-Master
- Multiple writable replicas
- Conflict resolution required
- High availability
