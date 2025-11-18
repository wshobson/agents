---
name: distributed-storage
description: Comprehensive guide to distributed storage systems including Ceph, software-defined storage (SDS), replication strategies, erasure coding, and storage performance optimization. Use when designing storage infrastructure, tuning storage performance, planning capacity, or evaluating storage technologies.
---

# Distributed Storage

## When to Use This Skill

- Designing Ceph clusters for specific workloads
- Selecting between replication and erasure coding
- Optimizing storage performance for read-heavy or write-heavy workloads
- Planning storage capacity and hardware selection
- Implementing tiered storage systems (hot/warm/cold data)
- Analyzing storage costs and efficiency
- Troubleshooting storage performance issues

## Core Concepts

### Ceph Architecture

**RADOS (Reliable Autonomic Distributed Object Store)**
- Foundation of Ceph
- Data stored as objects in pools
- Automatic data replication/erasure coding
- Placement Groups (PGs) distribute objects

**Storage Interfaces**
- **RBD (RADOS Block Device)**: Block storage for VMs, databases
- **CephFS**: Distributed filesystem with POSIX semantics
- **Object Gateway (S3/Swift)**: S3-compatible object storage API

**Key Components**
- **OSDs (Object Storage Daemons)**: Store data on individual drives
- **Monitors**: Track cluster state and configuration
- **MDS (Metadata Servers)**: Manage CephFS metadata (only for CephFS)
- **Managers**: Cluster management and monitoring

### Data Placement: CRUSH Algorithm

CRUSH (Controlled Replication Under Scalable Hashing)
- Maps objects to OSDs deterministically
- Allows rebalancing when topology changes
- Minimizes data movement on failure

**Failure Domains**
```
Datacenter
  ├─ Rack1
  │   ├─ Host1 [OSD0, OSD1]
  │   └─ Host2 [OSD2, OSD3]
  └─ Rack2
      ├─ Host3 [OSD4, OSD5]
      └─ Host4 [OSD6, OSD7]
```
- Ensures replicas spread across failure domains
- Prevents data loss if rack/host fails

**CRUSH Tuning**
```bash
# View CRUSH map
ceph osd getcrushmap -o crushmap.bin
crushtool -d crushmap.bin -o crushmap.txt

# Modify crush map
vi crushmap.txt
crushtool -c crushmap.txt -o crushmap.bin
ceph osd setcrushmap -i crushmap.bin
```

### Replication vs Erasure Coding

**Replication (e.g., 3-way replication)**
- 3 copies of each object
- Storage overhead: 3x original data
- Failure tolerance: 2 OSD failures
- Read performance: Good (3x read bandwidth)
- Write latency: Moderate (all replicas must acknowledge)
- Recovery speed: Fast
- Use case: Small to medium deployments, latency-sensitive

**Erasure Coding (e.g., 4+2 RS coding)**
- Divide object into 4 data chunks, 2 parity chunks
- Storage overhead: 1.5x original data (saves 33% vs 3-way)
- Failure tolerance: 2 OSD failures (2 chunks can be lost)
- Read performance: Complex (reconstruct from 4+ chunks)
- Write latency: Higher (recalculate parity)
- Recovery speed: Slower (reconstruct from multiple OSDs)
- Use case: Large deployments, cost-sensitive, archival data

**Selection Matrix**
| Requirement | Replication | Erasure Coding |
|---|---|---|
| Cost per TB | High | Low |
| Read latency | Low | Higher |
| Write latency | Medium | High |
| Recovery speed | Fast | Slow |
| Operational complexity | Simple | Complex |
| Failure tolerance | Limited | Good |

### Placement Groups (PGs)

PGs distribute objects within pools:
```
Pool → Placement Groups → Objects
```

**PG Calculation**
```
num_pgs = (total_osds * 100) / replica_count
Round to nearest power of 2
Minimum: 100 per OSD, maximum: 500 per OSD
```

**Common Issues**
- Too few PGs: Uneven distribution, hot spots
- Too many PGs: Memory overhead, OSD resource usage
- Uneven distribution: Hot PGs causing performance issues

```bash
# View PG distribution
ceph pg stat

# Change PG number (careful with large clusters)
ceph osd pool set pool_name pg_num 256
ceph osd pool set pool_name pgp_num 256
```

### RBD (Block Storage) Tuning

**Stripe Configuration**
```bash
# Stripe unit: 4KB (default), 8KB (better for sequential)
# Stripe count: 4 (spread data across 4 OSDs)
# Total stripe object size: 4KB * 4 = 16KB objects

rbd create --stripe-unit 8192 --stripe-count 4 volume-name
```
- Larger stripe unit: Better sequential performance
- Larger stripe count: Better parallel I/O performance
- Trade-off: More OSDs involved, more latency

**RBD Cache**
```bash
# Enable writeback cache (faster, riskier)
rbd config set global rbd_cache true
rbd config set global rbd_cache_size 33554432  # 32MB

# Set cache flush interval
rbd config set global rbd_cache_max_dirty 16777216  # 16MB
rbd config set global rbd_cache_target_dirty 8388608  # 8MB
```
- Writeback: Fast writes, risk of data loss on crash
- Writethrough: Slower writes, guaranteed durability

### CephFS (Distributed Filesystem)

**Metadata Server (MDS) Pool**
- Stores filesystem metadata (inodes, dentries)
- Critical performance bottleneck for metadata operations
- Use fast storage (SSD) for MDS pool

**Data Distribution**
- Files striped across multiple OSDs (like RBD)
- Automatic striping for files > 4MB
- Configure with file layouts

**CephFS Performance**
```bash
# Check MDS load
ceph mds stat

# Show cache sizes
ceph daemon mds.0 dump cache

# Tune MDS parameters
ceph config set mds cache_size 100000000  # 100M inodes
```

### Object Storage (S3-compatible)

**Bucket Layout**
- Objects distributed across OSDs
- Bucket is logical container
- No hierarchy, flat namespace

**Multipart Upload**
```
Client → RGW → Multiple OSDs
```
- Upload large objects in parts
- Each part 5MB to 5GB
- More efficient for large objects

**Sharding**
- Distribute bucket index across multiple objects
- Improves performance for buckets with many objects
- Configure: `rgw_override_bucket_index_max_shards`

## Storage Performance Optimization

### Read-Heavy Workloads
```
Strategy: Replication + RBD cache
- Use 3-way replication for fast reads
- Enable RBD writeback cache
- Use SSD for cache tier
- Tune stripe parameters for sequential reads
```

### Write-Heavy Workloads
```
Strategy: Erasure coding + journal tuning
- Use 4+2 erasure coding (lower storage cost)
- Use fast journal storage (NVMe)
- Tune OSD client message sizes
- Consider write-back cache
```

### Mixed Workloads
```
Strategy: Tiered storage + erasure coding
- Hot data: Replication on SSD (RBD cache tier)
- Warm data: Erasure coding on SSD
- Cold data: Erasure coding on HDD
- Automatic tiering based on access patterns
```

### Network Optimization
```bash
# Monitor network usage
ceph mon stat
ceph osd perf

# Separate replication network from client network
# Configure in ceph.conf:
[global]
public network = 10.0.0.0/24     # Client network
cluster network = 10.1.0.0/24    # OSD replication network
```

## Capacity Planning

### Storage Sizing
```
Required capacity = (data size) × (replication/EC factor)

Example: 100TB data with 3-way replication
  Required: 100TB × 3 = 300TB

Example: 100TB data with 4+2 erasure coding
  Required: 100TB × (6/4) = 150TB
```

### OSD Sizing
```
Disk space per OSD = (total required) / (number of OSDs)

Example: 300TB with 10 OSDs
  Space per OSD: 300TB / 10 = 30TB

Keep 10-20% free space for recovery
```

### Hardware Selection

**For Performance (Random I/O, databases)**
- NVMe SSDs for OSDs
- Fast CPUs (8+ cores per OSD)
- High-speed network (10GbE+)
- Journals on separate NVMe

**For Capacity (Archive, object storage)**
- 7.2k RPM SAS drives
- Standard CPUs (4+ cores)
- Sufficient network (1-10GbE)
- Shared journal in fast storage

**For Balance (General purpose)**
- SAS SSDs or 10k RPM SAS drives
- Mid-range CPUs (6+ cores)
- 10GbE network
- Separate journal storage

## Advanced Storage Concepts

### LSM Tree vs B-Tree Storage Engines

**B-Tree (PostgreSQL, MySQL InnoDB)**
```
Structure: Balanced tree with sorted keys
Reads: O(log n) - direct lookup
Writes: In-place updates (slower, causes fragmentation)
```
- Pros: Fast point reads, range scans
- Cons: Slow writes (random I/O), write amplification
- Use case: Read-heavy workloads, transactional databases

**LSM Tree (RocksDB, Cassandra, LevelDB)**
```
Structure: Multiple sorted levels (memtable → SST files)
Reads: O(log n * levels) - check multiple levels
Writes: Sequential append to memtable (faster)
Compaction: Background merge of levels
```
- Pros: Fast writes (sequential I/O), good compression
- Cons: Read amplification, compaction overhead
- Use case: Write-heavy workloads, time-series data

**Bloom Filters**
- Probabilistic data structure to test set membership
- Used in LSM trees to skip checking SSTables
- False positives possible, no false negatives
- Space-efficient (1-2 bytes per key)

### Distributed Storage Comparison

**Ceph**
- Architecture: RADOS (object storage), RBD/CephFS/RGW interfaces
- Pros: Unified storage (block, file, object), self-healing, CRUSH placement
- Cons: Complex setup, resource-intensive (3+ MONs, many OSDs)
- Use case: Enterprise, multi-protocol storage

**MinIO**
- Architecture: S3-compatible object storage, erasure coding
- Pros: Simple setup, high performance, S3 API, Kubernetes-native
- Cons: Object storage only, less mature than Ceph
- Use case: Cloud-native object storage, backups, data lakes

**GlusterFS**
- Architecture: Distributed file system, no metadata server
- Pros: Easy to deploy, scales horizontally, POSIX compliant
- Cons: Performance issues at scale, metadata bottlenecks
- Use case: File sharing, legacy applications needing POSIX

**Longhorn (Kubernetes)**
- Architecture: Cloud-native block storage for Kubernetes
- Pros: Kubernetes-native, snapshot support, easy management
- Cons: Kubernetes-only, newer project
- Use case: Persistent volumes in Kubernetes

### Multi-Region Replication

**Active-Active Replication**
```
Region A ←→ Region B
(bidirectional sync)
```
- Pros: Low latency for all regions, fault tolerance
- Cons: Conflict resolution complexity, consistency challenges
- Use case: Global applications, disaster recovery

**Active-Passive Replication**
```
Region A (primary) → Region B (standby)
```
- Pros: Simpler consistency, lower cost
- Cons: Higher latency for passive region, RTO delay
- Use case: Disaster recovery, compliance

**Disaster Recovery Strategies**
- RTO (Recovery Time Objective): Maximum acceptable downtime
- RPO (Recovery Point Objective): Maximum acceptable data loss
- Strategies: Snapshots, replication, backups (3-2-1 rule)
- Testing: Regular DR drills to validate procedures

## References

### Ceph Documentation
- `/references/ceph-architecture.md` - Deep dive into Ceph architecture
- `/references/crush-tuning.md` - CRUSH algorithm and tuning
- `/references/performance-tuning.md` - Ceph performance optimization
- `/references/bluestore-tuning.md` - BlueStore backend optimization
- `/references/ceph-spdk-integration.md` - SPDK integration for NVMe

### Storage Strategy
- `/references/replication-erasure-coding.md` - Detailed comparison
- `/references/tiered-storage.md` - Tiered storage patterns
- `/references/lsm-vs-btree.md` - Storage engine comparison
- `/references/multi-region-replication.md` - Cross-region patterns
- `/assets/capacity-planning-worksheet.md` - Capacity planning template

### Storage Comparison
- `/references/ceph-vs-minio.md` - Ceph vs MinIO comparison
- `/references/distributed-storage-comparison.md` - Full comparison matrix
- `/references/object-storage-protocols.md` - S3 vs Swift protocols

### Tools & Benchmarking
- `/references/benchmarking-tools.md` - Storage benchmarking tools (fio, rados bench, COSBench)
- `/references/monitoring-tools.md` - Storage monitoring (Prometheus, Grafana)
- `/assets/performance-tuning-checklist.md` - Tuning checklist
- `/assets/disaster-recovery-playbook.md` - DR procedures
