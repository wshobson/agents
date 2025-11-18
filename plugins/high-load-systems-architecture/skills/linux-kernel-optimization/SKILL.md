---
name: linux-kernel-optimization
description: Expert guide to Linux kernel tuning and performance optimization. Covers CPU scheduling, memory management, I/O optimization, network stack tuning, and profiling techniques. Use when optimizing system performance, debugging performance issues, tuning kernel parameters, or analyzing system behavior.
---

# Linux Kernel Optimization

## When to Use This Skill

- Optimizing kernel parameters for specific workloads
- Debugging performance issues at the system level
- Reducing latency or increasing throughput
- Tuning CPU scheduling for low-latency applications
- Optimizing I/O performance for storage-heavy workloads
- Analyzing system behavior with profiling and tracing
- Configuring resource limits and isolation

## Core Concepts

### CPU Scheduling

**CFS (Completely Fair Scheduler)**
- Default Linux scheduler since 2.6.23
- Fair distribution of CPU time across processes
- Tracks virtual runtime (weighted by priority)
- Quantum (time slice) adapts based on load

Key parameters:
- `sched_min_granularity_ns`: Minimum time slice
- `sched_latency_ns`: Target latency for all tasks to get CPU time
- `sched_wakeup_granularity_ns`: Wakeup preemption threshold

**Kernel Thread Scheduling**
```bash
# Increase priority (lower nice value, higher priority)
nice -n -20 my-app

# Set real-time priority
chrt -f 50 my-app

# Pin to CPU
taskset -c 0-3 my-app
```

**NUMA Load Balancing**
- Automatic memory placement for NUMA systems
- Trade-off: Better locality vs scheduling overhead
- Tune with `kernel.numa_balancing` parameter

**Context Switch Overhead**
- More context switches = lower latency but higher overhead
- Monitor with `vmstat` or `perf`
- Reduce with CPU pinning and real-time priority

### Memory Management

**Virtual Memory Zones**
- DMA: Memory directly accessible by DMA hardware (< 16MB)
- DMA32: 32-bit DMA capable (< 4GB)
- Normal: Normal memory (typically 1GB+ up to RAM size)
- High: Memory > 4GB on 32-bit systems

**Page Cache**
- Caches filesystem blocks for fast access
- Reduces I/O operations
- Automatic, but can be tuned:
  - `vm.swappiness`: Tendency to swap vs evict cache (0-100)
  - `vm.dirty_ratio`: Dirty pages threshold for writeback
  - `vm.dirty_background_ratio`: Background writeback threshold

**Memory Compaction**
```bash
# Trigger memory compaction
echo 1 > /proc/sys/vm/compact_memory

# Monitor fragmentation
cat /proc/buddyinfo
```

**Transparent Huge Pages (THP)**
```bash
# Enable THP
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# Disable THP (for some workloads)
echo never > /sys/kernel/mm/transparent_hugepage/enabled

# Madvise: Only for madvise() calls
echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
```
Trade-off: Better TLB efficiency vs memory overhead

**NUMA Locality**
```bash
# Bind process to NUMA node 0
numactl --membind=0 my-app

# Show NUMA topology
numactl --hardware

# Monitor memory locality
cat /proc/numa_maps
```

**OOM Killer**
```bash
# Set OOM score (lower = less likely to kill)
echo -500 > /proc/$PID/oom_score_adj

# Disable OOM killer
echo -17 > /proc/$PID/oom_score_adj
```

### I/O Optimization

**I/O Schedulers**

- **none**: Simple FIFO, good for high-speed storage (SSD, NVMe)
```bash
echo none > /sys/block/sda/queue/scheduler
```

- **mq-deadline**: Deadline guarantees, good balance
```bash
echo mq-deadline > /sys/block/sda/queue/scheduler
```

- **kyber**: Latency targeting, good for low-latency requirements
```bash
echo kyber > /sys/block/sda/queue/scheduler
```

- **bfq**: Fairness between I/O requests
```bash
echo bfq > /sys/block/sda/queue/scheduler
```

**Block Device Tuning**
```bash
# Read-ahead size (in sectors)
echo 256 > /sys/block/sda/queue/read_ahead_kb

# Request queue depth
echo 256 > /sys/block/sda/queue/nr_requests

# Rotational device (0 for SSD, 1 for HDD)
echo 0 > /sys/block/sda/queue/rotational
```

**NVMe-Specific Tuning**
```bash
# Set appropriate queue depth
echo 256 > /sys/block/nvme0n1/queue/nr_requests

# Use none scheduler for NVMe
echo none > /sys/block/nvme0n1/queue/scheduler
```

### Network Stack Tuning

**TCP Window Size**
```bash
# Read buffer (socket receive buffer)
sysctl net.ipv4.tcp_rmem="4096 87380 6291456"

# Write buffer (socket send buffer)
sysctl net.ipv4.tcp_wmem="4096 65536 4194304"
```
- Larger window = higher throughput but more memory

**TCP Backlog**
```bash
# Listen socket backlog
sysctl net.core.somaxconn=4096

# SYN queue size
sysctl net.ipv4.tcp_max_syn_backlog=4096
```

**Congestion Control**
```bash
# View available algorithms
cat /proc/sys/net/ipv4/tcp_available_congestion_control

# Set default (BBR is modern high-performance choice)
sysctl net.ipv4.tcp_congestion_control=bbr
```

**Receive Packet Steering (RPS)**
```bash
# Enable RPS for NIC queue 0
echo "f" > /sys/class/net/eth0/queues/rx-0/rps_cpus
```
- Distribute packet processing across CPUs
- Improves cache locality

**Interrupt Coalescing**
```bash
# Reduce interrupt frequency (usecs)
ethtool -C eth0 rx-usecs 100

# Maximum packets per interrupt
ethtool -C eth0 rx-max-coalesced-frames 64
```
- Trade-off: Latency vs throughput

### cgroups Resource Control

**CPU Bandwidth Control**
```bash
# Limit CPU to 50% of system (500000 us per 1000000 us period)
echo 500000 > /sys/fs/cgroup/cpu/myapp/cpu.cfs_quota_us
echo 1000000 > /sys/fs/cgroup/cpu/myapp/cpu.cfs_period_us
```

**Memory Limits**
```bash
# Set memory limit to 2GB
echo 2147483648 > /sys/fs/cgroup/memory/myapp/memory.limit_in_bytes

# View memory stats
cat /sys/fs/cgroup/memory/myapp/memory.stat
```

**I/O Bandwidth Control (blkio)**
```bash
# Limit write IOPS
echo "8:0 1000" > /sys/fs/cgroup/blkio/myapp/blkio.throttle.write_iops_device

# Monitor I/O usage
cat /sys/fs/cgroup/blkio/myapp/blkio.throttle.io_service_bytes
```

## Profiling & Analysis

### Tools for Performance Analysis

**perf (Performance Events)**
```bash
# CPU profiling
perf record -F 99 -p $PID
perf report

# Trace system calls
perf trace -p $PID

# Record events for flame graph
perf record -F 99 -g -p $PID
perf script | flamegraph.pl > out.svg
```

**vmstat (Virtual Memory Statistics)**
```bash
# Show memory and CPU stats every second
vmstat 1
# Columns: procs, memory (swpd,free,buff,cache), I/O, system, CPU
```

**iostat (I/O Statistics)**
```bash
# Show disk I/O stats every second
iostat -x 1 sda
# Look for: await (avg wait), svctm (service time), %util (utilization)
```

**netstat/ss (Network Statistics)**
```bash
# Show TCP connections
ss -s
ss -tan

# View socket statistics
netstat -s
```

**ftrace (Function Tracing)**
```bash
# Enable specific function tracing
echo "function" > /sys/kernel/debug/tracing/current_tracer
echo "schedule" > /sys/kernel/debug/tracing/set_ftrace_filter
echo 1 > /sys/kernel/debug/tracing/tracing_on

# Read trace output
cat /sys/kernel/debug/tracing/trace
```

## Optimization Patterns

### Low-Latency Applications
```bash
# 1. CPU Pinning
taskset -c 0-3 my-app

# 2. Disable frequency scaling
echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# 3. Real-time scheduling
chrt -f 50 my-app

# 4. Network tuning
sysctl net.core.rmem_max=134217728
sysctl net.core.wmem_max=134217728
sysctl net.ipv4.tcp_rmem="4096 87380 134217728"
sysctl net.ipv4.tcp_wmem="4096 65536 134217728"

# 5. Disable THP
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

### High-Throughput Workloads
```bash
# 1. Increase buffer sizes
sysctl net.core.rmem_max=134217728
sysctl net.core.wmem_max=134217728

# 2. Enable jumbo frames (if network supports)
ip link set dev eth0 mtu 9000

# 3. NIC optimization
ethtool -L eth0 combined 8
ethtool -C eth0 rx-usecs 100

# 4. Enable THP for memory efficiency
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# 5. Tune I/O scheduler
echo mq-deadline > /sys/block/sda/queue/scheduler
```

## References

### Kernel Documentation
- `/references/kernel-tuning-guide.md` - Comprehensive tuning guide
- `/references/scheduler-tuning.md` - CFS scheduler deep dive
- `/references/network-stack-tuning.md` - Network optimization details

### Profiling Tools
- `/references/perf-guide.md` - Perf profiling guide
- `/references/flamegraph-guide.md` - Flame graph visualization
- `/assets/profiling-checklist.md` - Profiling checklist
