---
name: design-high-load-system
description: Interactive system architecture design workflow. Guides through requirements gathering, technology selection, and architecture design for high-load systems. Coordinates with high-load architect, storage architect, and virtualization architect agents.
---

# Design High-Load System

## Overview

This command provides an interactive workflow for designing architecture for high-load systems. It guides you through:

1. **Requirements Gathering** - Understanding your specific needs
2. **Technology Selection** - Choosing appropriate technologies
3. **Architecture Design** - Building the complete system architecture
4. **Performance Projection** - Estimating performance metrics
5. **Implementation Roadmap** - Planning the implementation

## Process

### Phase 1: Requirements Gathering

First, we need to understand your specific requirements:

**Scale Requirements**
- Expected users/requests per second
- Data volume (current and 12-month projection)
- Growth rate
- Geographic distribution

**Performance Requirements**
- Throughput (requests/sec, MB/sec)
- Latency (99th percentile, 99.9th percentile)
- Consistency requirements (strong, eventual, causal)
- Availability requirement (99.9%, 99.99%, etc.)

**Operational Requirements**
- Budget constraints
- Operational complexity tolerance
- Team size and expertise
- Upgrade/scaling frequency
- Disaster recovery requirements

**Workload Profile**
- Read-heavy vs write-heavy
- Random vs sequential access patterns
- Typical request size
- Burstiness and peak-to-average ratio
- Data retention requirements

### Phase 2: Technology Selection

Based on requirements, we evaluate technologies:

**Compute & Virtualization**
- Bare metal vs VMs vs containers
- Kubernetes vs custom orchestration
- Single vs multi-datacenter

**Storage Selection**
- Database technology (SQL, NoSQL, time-series)
- Cache layer (Redis, Memcached)
- Distributed storage (Ceph, S3)
- Replication vs erasure coding

**Networking**
- Load balancing strategy
- Network topology (star, spine-leaf)
- CDN for content delivery
- Message queue selection

### Phase 3: Architecture Design

We design the complete architecture including:

**Service Architecture**
```
Load Balancer
  ├─ API Gateway (horizontal scaling)
  ├─ Service1 (microservice)
  ├─ Service2 (microservice)
  └─ ServiceN
       ↓
Database Cluster (read replicas)
  ↓
Cache Layer (distributed)
  ↓
Object Storage (archive)
```

**Redundancy & Failover**
- Active-passive vs active-active
- Failure domain analysis
- Health checking and recovery

**Data Flow**
- Synchronous vs asynchronous patterns
- Message queues for decoupling
- Event streaming for real-time updates

### Phase 4: Performance Projection

Using the high-load architect, we estimate:

**Throughput Calculations**
```
Compute throughput = (cores per node) × (requests per core/sec) × (number of nodes)

Example:
- 8 cores per node × 10,000 req/core/sec × 10 nodes = 800,000 req/sec
```

**Latency Analysis**
```
Total latency = (service latency) + (network latency) + (queue latency)

Example:
- Service: 50ms (99th percentile)
- Network: 5ms round-trip
- Queue: 10ms
- Total: 65ms
```

**Storage Capacity**
```
Required storage = (data size) × (replication/EC factor) × (growth multiplier)

Example:
- 10TB current data
- 3-way replication = 30TB
- 12-month growth to 50TB = total 150TB (50TB × 3)
- Add 20% headroom = 180TB total
```

### Phase 5: Implementation Roadmap

A phased approach to implementation:

**Phase 1: MVP (Months 1-3)**
- Deploy basic infrastructure
- Test scaling approach
- Validate performance assumptions
- Implement monitoring

**Phase 2: Production Ready (Months 3-6)**
- Add redundancy and failover
- Implement full monitoring
- Disaster recovery testing
- Performance optimization

**Phase 3: Optimization (Months 6+)**
- Fine-tune parameters
- Optimize cost
- Plan 10x scaling
- Team enablement

## Engagement with Agents

### High-Load Architect
- Overall system design
- Technology trade-off analysis
- Scalability strategy
- Performance projections

### Storage Architect
- Database selection
- Replication/erasure coding decisions
- Storage capacity planning
- Storage performance optimization

### Virtualization Architect
- Infrastructure design
- VM sizing and placement
- Live migration strategy
- Cloud platform architecture

### Linux Kernel Specialist
- Kernel parameter tuning
- System-level optimization
- Performance debugging
- Resource allocation

## Expected Outcomes

At the end of this workflow, you should have:

1. **Architecture Document**
   - System overview diagram
   - Component descriptions
   - Data flow diagrams
   - Redundancy and failover strategy

2. **Performance Projections**
   - Throughput capacity
   - Latency estimates
   - Storage requirements
   - Network capacity

3. **Technology Decisions**
   - Compute (hardware, virtualization)
   - Storage (databases, caches)
   - Networking (load balancing, CDN)
   - Monitoring and observability

4. **Implementation Roadmap**
   - Phased approach
   - Team requirements
   - Timeline and milestones
   - Budget estimates

5. **Operational Guidelines**
   - Capacity planning thresholds
   - Scaling procedures
   - Disaster recovery procedures
   - Performance tuning parameters

## Tips for Success

- **Be specific about requirements** - Vague requirements lead to suboptimal architecture
- **Understand your bottlenecks** - Different workloads have different bottlenecks
- **Plan for 10x growth** - Ensure architecture scales without major redesign
- **Measure everything** - Validate assumptions with real metrics
- **Start simple** - Add complexity only when needed
- **Plan for operations** - Simple to operate is worth more than slightly better performance
