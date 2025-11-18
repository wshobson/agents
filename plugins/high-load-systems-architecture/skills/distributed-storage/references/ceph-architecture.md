# Ceph Architecture Reference

## Core Components

### MON (Monitor)
- Cluster map management
- Quorum-based consensus
- Minimum 3 MONs for HA

### OSD (Object Storage Daemon)
- Data storage and replication
- Recovery and rebalancing
- One OSD per disk

### MDS (Metadata Server)
- CephFS metadata
- Directory hierarchy
- File attributes

### MGR (Manager)
- Monitoring and metrics
- Dashboard and API
- Module framework

## CRUSH Algorithm

**Controlled Replication Under Scalable Hashing**

```python
def get_osds(object_id, num_replicas=3):
    pg = hash(object_id) % num_pgs
    osds = crush_map.get_osds(pg, num_replicas)
    return osds
```

## Replication

### Replicated Pools
- Full copies of data
- 3x storage overhead (default)
- Fast reads, medium writes

### Erasure Coding
- K+M chunks (e.g., 8+3)
- Lower overhead (1.37x for 8+3)
- Slower writes, rebuild overhead

## Performance Tuning

```ini
[osd]
osd_op_threads = 8
osd_disk_threads = 4
osd_recovery_max_active = 5
```
