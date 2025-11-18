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

## Troubleshooting Distributed Storage

### Ceph Cluster Issues

**Cluster Health Problems**:
```bash
# Check cluster status
ceph -s
ceph health detail

# Common states:
# HEALTH_WARN: Warning state (degraded, slow ops)
# HEALTH_ERR: Error state (data loss risk)

# Check OSD status
ceph osd tree
ceph osd stat
ceph osd df  # OSD utilization

# Check placement group states
ceph pg stat
ceph pg dump | grep -v "active+clean"
```

**Common Health Issues & Solutions**:

1. **OSDs Down**
   ```bash
   # Identify down OSDs
   ceph osd tree | grep down

   # Check OSD logs
   journalctl -u ceph-osd@<id> -n 100

   # Restart OSD
   systemctl restart ceph-osd@<id>

   # If OSD won't start, check disk health
   smartctl -a /dev/sdb
   ```

2. **Slow Requests / Blocked Ops**
   ```bash
   # Identify slow ops
   ceph health detail | grep slow

   # Check OSD performance
   ceph osd perf
   ceph daemon osd.<id> dump_historic_ops

   # Common causes:
   # - Disk latency (check iostat, disk queue depth)
   # - Network latency (check network bandwidth)
   # - CPU saturation on OSD node

   # Solutions:
   # - Add more OSDs to distribute load
   # - Upgrade to faster disks (NVMe)
   # - Tune BlueStore cache size
   ceph config set osd bluestore_cache_size 4294967296  # 4GB
   ```

3. **PG Inconsistencies**
   ```bash
   # Identify inconsistent PGs
   ceph pg dump | grep inconsistent

   # Repair PG
   ceph pg repair <pg-id>

   # Deep scrub to verify
   ceph pg deep-scrub <pg-id>

   # Check scrub errors
   rados list-inconsistent-obj <pg-id>
   ```

4. **Unbalanced Data Distribution**
   ```bash
   # Check OSD utilization variance
   ceph osd df tree

   # Rebalance data with CRUSH tuning
   ceph osd crush reweight osd.<id> <weight>

   # Enable balancer module
   ceph balancer on
   ceph balancer mode upmap

   # Monitor rebalancing
   ceph balancer status
   ```

### Performance Troubleshooting

**Slow RBD Performance**:
```bash
# Test RBD performance
rbd bench --io-type write <pool>/<image>
rbd bench --io-type read <pool>/<image>

# Check RBD cache settings
rbd config image get <pool>/<image> rbd_cache

# Optimize RBD striping
rbd info <pool>/<image>  # Check current stripe settings
rbd create --stripe-unit 65536 --stripe-count 16 <pool>/<new-image>

# Check client-side I/O patterns
# Ensure queue depth is appropriate
fio --filename=/dev/rbd0 --iodepth=32 --ioengine=libaio --bs=4k --rw=randread
```

**CephFS Slow Metadata Operations**:
```bash
# Check MDS status
ceph fs status
ceph mds stat

# MDS performance metrics
ceph daemon mds.<name> perf dump

# Common issues:
# 1. MDS cache exhaustion
ceph config set mds mds_cache_memory_limit 8589934592  # 8GB

# 2. Hot metadata (single directory with millions of files)
# Solution: Distribute files across multiple directories
# Use hashing: /data/ab/cd/abcd1234.dat

# 3. MDS failover/recovery
ceph fs set <fs-name> max_mds 2  # Active-active MDS
```

**Object Storage (RGW) Slowness**:
```bash
# Check RGW logs
journalctl -u ceph-radosgw@rgw.$(hostname) -n 100

# Monitor RGW performance
radosgw-admin usage show

# Bucket index sharding (for buckets with many objects)
radosgw-admin bucket stats --bucket=<bucket-name>
radosgw-admin bucket reshard --bucket=<bucket-name> --num-shards=64

# Check RGW cache
# Enable RGW cache tier for frequently accessed objects
```

### Network Issues

**High Latency Between OSDs**:
```bash
# Test network latency
ping -c 10 <osd-host>
iperf3 -c <osd-host> -t 30

# Check for packet loss
mtr <osd-host>

# Verify network configuration
# Ensure cluster network is separate from public network
ceph config get osd cluster_network
ceph config get osd public_network

# Check for network saturation
iftop -i eth1  # Monitor bandwidth usage
```

**Split Brain / Network Partition**:
```bash
# Identify monitor quorum issues
ceph mon stat
ceph quorum_status -f json-pretty

# If monitors can't form quorum:
# 1. Check network connectivity between monitors
# 2. Verify time synchronization (NTP)
timedatectl status

# Emergency: Inject monmap to recover
# (DANGEROUS - use only as last resort)
ceph-mon -i <mon-id> --extract-monmap /tmp/monmap
ceph-mon -i <mon-id> --inject-monmap /tmp/monmap
```

### Capacity and Space Issues

**Near-Full OSDs**:
```bash
# Check OSD fullness
ceph osd df tree

# Full ratio configuration
ceph osd dump | grep full_ratio

# Temporarily increase full ratio (emergency)
ceph osd set-full-ratio 0.90
ceph osd set-nearfull-ratio 0.85

# Permanent solutions:
# 1. Add more OSDs
# 2. Delete unused data
# 3. Rebalance data across OSDs
ceph osd reweight <osd-id> <weight>
```

**RBD Thin Provisioning Issues**:
```bash
# Check actual vs provisioned space
rbd du <pool>/<image>

# Reclaim deleted space
rbd sparsify <pool>/<image>

# Prevent over-provisioning
# Implement quota management
ceph osd pool set-quota <pool> max_bytes <bytes>
```

### Recovery and Rebalancing

**Slow Recovery**:
```bash
# Check recovery progress
ceph -w  # Watch cluster events

# Tune recovery parameters (increase recovery speed)
ceph config set osd osd_max_backfills 4  # Default: 1
ceph config set osd osd_recovery_max_active 5  # Default: 3
ceph config set osd osd_recovery_sleep_hdd 0  # Disable sleep

# Throttle recovery (reduce impact on client I/O)
ceph config set osd osd_max_backfills 1
ceph config set osd osd_recovery_max_active 1
ceph config set osd osd_recovery_sleep_hdd 0.1
```

**Stuck PGs**:
```bash
# Identify stuck PGs
ceph pg dump_stuck stale
ceph pg dump_stuck inactive
ceph pg dump_stuck unclean

# Query specific PG
ceph pg <pg-id> query

# Force PG creation/recovery (use carefully)
ceph pg force_create_pg <pg-id>
ceph osd lost <osd-id> --yes-i-really-mean-it  # Mark OSD as permanently lost
```

### MinIO Specific Issues

**MinIO Performance Degradation**:
```bash
# Check MinIO server logs
journalctl -u minio -n 100

# MinIO metrics
curl http://localhost:9000/minio/v2/metrics/cluster

# Common issues:
# 1. Disk I/O bottleneck
iostat -x 1  # Check disk utilization

# 2. Network bandwidth saturation
iftop

# 3. Healing in progress (after disk replacement)
mc admin heal -r myminio
```

**MinIO Distributed Setup Issues**:
```bash
# Check cluster status
mc admin info myminio

# Verify erasure code configuration
# Ensure drive count matches EC:parity ratio
# Example: 16 drives with EC:8 (8 data + 8 parity)

# Drive offline issues
mc admin heal myminio

# Rebalance after adding drives
# MinIO automatically rebalances on new drive addition
```

### General Storage Troubleshooting

**Identifying Storage Hotspots**:
```bash
# Ceph: Check OSD IOPS distribution
ceph osd perf | sort -k2 -n

# System-level: I/O monitoring
iostat -x 1 5  # Extended stats, 1 sec interval, 5 iterations
iotop -o  # Show only processes doing I/O

# Identify heavy I/O processes
pidstat -d 1
```

**Data Corruption Detection**:
```bash
# Ceph: Deep scrub all PGs
ceph pg deep-scrub <pg-id>

# Enable automatic scrubbing
ceph config set osd osd_scrub_auto_repair true

# Check for silent data corruption
# Verify checksums (BlueStore does this automatically)
ceph daemon osd.<id> dump_mempools

# For critical data: periodic verification
md5sum /path/to/file > checksums.txt
md5sum -c checksums.txt
```

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
