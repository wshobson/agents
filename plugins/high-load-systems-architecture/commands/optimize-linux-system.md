---
name: optimize-linux-system
description: Interactive Linux system optimization workflow. Profiles system performance, identifies bottlenecks, applies kernel and application tuning, and validates improvements. Coordinates with linux-kernel-specialist agent for detailed optimization.
---

# Optimize Linux System

## Overview

This command provides an interactive workflow for optimizing Linux system performance. It guides you through:

1. **System Profiling** - Understanding current performance
2. **Bottleneck Analysis** - Identifying the limiting factor
3. **Targeted Optimization** - Applying specific tuning
4. **Performance Validation** - Measuring improvements
5. **Production Deployment** - Safe rollout of changes

## Process

### Phase 1: System Profiling

We start by understanding your current system:

**System Information**
```bash
# CPU info
lscpu                          # CPU model, cores, flags
cat /proc/cpuinfo             # Detailed CPU information

# Memory info
free -h                        # Total, used, free memory
numactl --hardware            # NUMA topology

# Storage info
lsblk                         # Block devices and sizes
df -h                         # Filesystem usage

# Network info
ethtool eth0                  # NIC capabilities
ip addr                       # IP configuration
```

**Current Performance Metrics**
- **CPU Usage**: User, system, I/O wait, idle
- **Memory**: Used, cache, swap, fragmentation
- **I/O**: Disk throughput, latency, IOPS
- **Network**: Throughput, latency, packet loss

**Application-Specific Metrics**
- Request latency (p50, p99, p99.9)
- Throughput (requests/sec, MB/sec)
- Error rates
- Resource utilization

### Phase 2: Bottleneck Analysis

We identify what's limiting performance:

**Common Bottlenecks**

**CPU-Limited**
- Symptoms: High CPU usage (>80%), consistent latency
- Root cause: Insufficient compute capacity
- Solutions:
  - Add more CPUs/cores
  - Optimize hot code paths
  - Reduce context switching
  - Pin to specific CPUs

**I/O-Limited**
- Symptoms: High disk/network latency, low CPU usage
- Root cause: Slow storage/network
- Solutions:
  - Use faster storage (SSD vs HDD)
  - Increase I/O parallelism
  - Optimize query patterns
  - Add caching

**Memory-Limited**
- Symptoms: High page fault rate, OOM killer active
- Root cause: Insufficient RAM or memory leaks
- Solutions:
  - Add more RAM
  - Reduce memory footprint
  - Tune cache sizes
  - Enable swap monitoring

**Network-Limited**
- Symptoms: High network latency, packet loss
- Root cause: Network congestion or topology
- Solutions:
  - Optimize packet sizes
  - Reduce network hops
  - Upgrade network hardware
  - Tune TCP parameters

### Phase 3: Targeted Optimization

Based on the bottleneck, we apply specific tuning:

**For CPU-Limited Workloads**

```bash
# 1. CPU Affinity
taskset -c 0-3 my-app        # Pin to CPUs 0-3

# 2. Priority Setting
nice -n -10 my-app           # Higher priority

# 3. Real-time Scheduling (if appropriate)
chrt -f 50 my-app            # FIFO real-time at priority 50

# 4. Disable Frequency Scaling
echo performance > /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# 5. Check Scheduler Parameters
cat /proc/sys/kernel/sched_min_granularity_ns
cat /proc/sys/kernel/sched_latency_ns
```

**For I/O-Limited Workloads**

```bash
# 1. Change I/O Scheduler (for spinning disks)
echo mq-deadline > /sys/block/sda/queue/scheduler

# Or for SSDs:
echo none > /sys/block/sda/queue/scheduler

# 2. Increase Read-Ahead
echo 256 > /sys/block/sda/queue/read_ahead_kb

# 3. Tune Block Device Queue
echo 256 > /sys/block/sda/queue/nr_requests

# 4. Optimize for rotational devices
echo 0 > /sys/block/sda/queue/rotational  # 0 for SSD, 1 for HDD

# 5. Tune VM writeback
sysctl vm.dirty_ratio=20
sysctl vm.dirty_background_ratio=5
```

**For Memory-Limited Workloads**

```bash
# 1. Tune Swappiness
sysctl vm.swappiness=10        # Prefer evicting cache

# 2. Enable Huge Pages
echo always > /sys/kernel/mm/transparent_hugepage/enabled
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# 3. Tune Page Cache
sysctl vm.dirty_ratio=15
sysctl vm.dirty_background_ratio=5

# 4. Monitor Memory
cat /proc/numa_maps
cat /proc/buddyinfo
```

**For Network-Limited Workloads**

```bash
# 1. Tune TCP Buffers
sysctl net.ipv4.tcp_rmem="4096 87380 134217728"
sysctl net.ipv4.tcp_wmem="4096 65536 134217728"

# 2. Increase Backlog Queues
sysctl net.core.somaxconn=4096
sysctl net.ipv4.tcp_max_syn_backlog=4096

# 3. Set Congestion Control
sysctl net.ipv4.tcp_congestion_control=bbr

# 4. Enable RPS for NIC
echo "f" > /sys/class/net/eth0/queues/rx-0/rps_cpus

# 5. Interrupt Coalescing
ethtool -C eth0 rx-usecs 100
```

### Phase 4: Performance Validation

We measure the impact of optimizations:

**Baseline vs Optimized Comparison**
```
Metric              Before      After      Improvement
─────────────────────────────────────────────────────
Throughput (req/s)  10,000      15,000     +50%
Latency p99 (ms)    50          35         -30%
CPU Usage           80%         60%        -20%
Memory Usage        8GB         8GB        0%
```

**Profiling Tools**

**perf (CPU profiling)**
```bash
# Record CPU profile
perf record -F 99 -p $PID
perf report

# Flame graph
perf record -F 99 -g -p $PID
perf script | flamegraph.pl > out.svg
```

**vmstat (System metrics)**
```bash
vmstat 1              # Update every 1 second
# Look at: r (run queue), cs (context switches), us/sy (user/system)
```

**iostat (I/O metrics)**
```bash
iostat -x 1 sda       # Extended stats every 1 second
# Look at: await (latency), %util (utilization)
```

**netstat/ss (Network)**
```bash
ss -s                 # Socket statistics
netstat -s           # Protocol statistics
```

**Load Testing**
- Use appropriate load testing tool for your application
- Generate realistic load patterns
- Measure latency percentiles (p50, p99, p99.9)
- Monitor resource utilization during test

### Phase 5: Production Deployment

Safe rollout of optimizations:

**Staged Rollout**
1. **Development**: Validate in dev environment
2. **Staging**: Test with production-like load
3. **Canary**: Deploy to 10% of production
4. **Monitor**: Watch metrics for 24 hours
5. **Full Rollout**: Gradually increase to 100%

**Measurement & Monitoring**
```bash
# Create monitoring dashboard
- Throughput (requests/sec)
- Latency (p50, p99, p99.9)
- CPU usage (user, system, idle)
- Memory usage (used, cache, swap)
- Disk I/O (IOPS, throughput, latency)
- Network (throughput, latency)
```

**Rollback Plan**
- Keep old configuration documented
- Have rollback procedure ready
- Alert on performance regressions
- Define SLO thresholds

## Engagement with Linux Kernel Specialist

### When to Engage
- Complex kernel tuning needed
- Performance debugging
- Understanding why optimizations work
- Evaluating trade-offs

### What They Provide
- Kernel parameter tuning recommendations
- Profiling and analysis guidance
- Performance bottleneck identification
- Trade-off analysis (latency vs throughput)

## Optimization Checklists

### Low-Latency Application Checklist
```
☐ CPU pinning configured
☐ Frequency scaling disabled
☐ Real-time priority enabled
☐ Swap disabled
☐ THP disabled
☐ Huge pages allocated
☐ Network interrupt coalescing tuned
☐ TCP buffers optimized
☐ Load testing completed
☐ Monitoring in place
```

### High-Throughput Workload Checklist
```
☐ CPU overcommit optimized
☐ I/O scheduler tuned (none or mq-deadline)
☐ Read-ahead optimized
☐ Buffer sizes increased
☐ THP enabled
☐ TCP congestion control optimized (BBR)
☐ RPS/RFS enabled
☐ Network interrupt coalescing optimized
☐ Load testing completed
☐ Monitoring in place
```

### Storage-Heavy Workload Checklist
```
☐ I/O scheduler configured
☐ Block queue depth optimized
☐ Read-ahead tuned
☐ Page cache tuning
☐ Writeback parameters optimized
☐ Filesystem optimizations applied
☐ NUMA locality considered
☐ Disk health monitoring enabled
☐ Load testing completed
☐ Monitoring in place
```

## Tips for Success

- **Measure first** - Establish baseline before optimizing
- **Change one thing at a time** - Makes impact clear
- **Document changes** - Important for reproducibility
- **Test under load** - Development performance may not reflect production
- **Monitor long-term** - Optimizations may have long-term effects
- **Plan for growth** - Ensure optimizations scale
- **Keep it simple** - Simplest solution is usually best
- **Be cautious with production** - Staged rollout reduces risk

## Common Pitfalls to Avoid

- ❌ Tuning without measuring impact
- ❌ Making multiple changes simultaneously
- ❌ Optimizing wrong bottleneck
- ❌ Trading consistency for performance
- ❌ Ignoring long-term performance trends
- ❌ Over-optimizing for micro-benchmarks
- ❌ Forgetting to document changes
- ❌ Testing only happy path scenarios
