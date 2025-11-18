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

## Troubleshooting Kernel Performance Issues

### High CPU Usage

**Diagnosis**:
```bash
# Identify CPU-intensive processes
top -b -n 1 | head -20
ps aux --sort=-%cpu | head -10

# CPU usage breakdown
mpstat -P ALL 1 5  # Per-CPU statistics

# Check for CPU throttling
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq
cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_cur_freq

# Identify context switches
vmstat 1 5  # Look at 'cs' column

# Profile CPU usage
perf top -g  # Real-time profiling
perf record -ag -- sleep 30
perf report
```

**Common Causes & Solutions**:

1. **CPU Frequency Scaling**
   ```bash
   # Check current governor
   cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

   # Set to performance mode
   echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

   # Make persistent
   cpupower frequency-set -g performance
   ```

2. **Excessive Context Switching**
   ```bash
   # Identify source
   perf sched record -- sleep 10
   perf sched latency

   # Solution: CPU pinning
   taskset -c 0-3 <command>
   ```

3. **IRQ Storm**
   ```bash
   # Check interrupt counts
   cat /proc/interrupts
   watch -n 1 "cat /proc/interrupts | head -20"

   # Distribute IRQs across CPUs
   echo 2 > /proc/irq/<irq-num>/smp_affinity
   # Or use irqbalance
   systemctl start irqbalance
   ```

### Memory Issues

**OOM Killer Triggered**:
```bash
# Check OOM events
dmesg | grep -i "out of memory"
journalctl -k | grep -i "killed process"

# Identify memory hogs
ps aux --sort=-%mem | head -10

# Check memory fragmentation
cat /proc/buddyinfo
cat /proc/pagetypeinfo

# Trigger memory compaction
echo 1 > /proc/sys/vm/compact_memory

# Adjust OOM score
echo -500 > /proc/<pid>/oom_score_adj  # Less likely to be killed
```

**Memory Leak Detection**:
```bash
# Monitor memory usage over time
while true; do
  ps aux | grep <process> | awk '{print $6}'
  sleep 60
done

# Detailed memory analysis
pmap -x <pid>
cat /proc/<pid>/smaps

# Java heap analysis
jmap -heap <pid>
jmap -dump:format=b,file=heap.bin <pid>
```

**Swap Thrashing**:
```bash
# Check swap usage
free -h
swapon -s

# Identify processes using swap
for pid in $(ls /proc | grep -E '^[0-9]+$'); do
  [ -f /proc/$pid/smaps ] && \
  awk '/Swap:/ {sum+=$2} END {print sum}' /proc/$pid/smaps | \
  xargs -I {} echo "$pid: {} KB"
done | sort -t: -k2 -n

# Solutions:
# 1. Reduce swappiness
sysctl vm.swappiness=10

# 2. Add more RAM
# 3. Optimize application memory usage
```

### I/O Performance Problems

**High I/O Wait**:
```bash
# Check I/O wait percentage
iostat -x 1 5  # Look at %iowait

# Identify I/O-heavy processes
iotop -o

# Check disk queue depth
cat /sys/block/sda/queue/nr_requests

# Monitor I/O scheduler performance
cat /sys/block/sda/queue/scheduler
```

**Slow Disk Performance**:
```bash
# Test disk performance
dd if=/dev/zero of=/tmp/test bs=1M count=1024 conv=fdatasync
hdparm -tT /dev/sda

# Check for disk errors
smartctl -a /dev/sda
dmesg | grep -i error

# Optimize I/O scheduler
echo mq-deadline > /sys/block/sda/queue/scheduler  # For SSD
echo none > /sys/block/nvme0n1/queue/scheduler  # For NVMe

# Tune read-ahead
echo 256 > /sys/block/sda/queue/read_ahead_kb

# Check filesystem mount options
mount | grep sda
# Optimize: noatime, nodiratime for performance
mount -o remount,noatime,nodiratime /dev/sda1
```

**io_uring Issues**:
```bash
# Check if io_uring is available
cat /proc/sys/kernel/io_uring_disabled  # Should be 0

# Monitor io_uring usage
# Use bpftrace to trace io_uring calls
bpftrace -e 'kprobe:io_uring_enter { @calls = count(); }'

# Common issues:
# 1. Kernel too old (< 5.1)
uname -r

# 2. Not enough memory locked (for fixed buffers)
ulimit -l unlimited
```

### Network Performance Issues

**High Packet Loss**:
```bash
# Check packet loss
netstat -s | grep -i 'packet receive errors'
ethtool -S eth0 | grep -i drop

# Check ring buffer sizes
ethtool -g eth0

# Increase ring buffer
ethtool -G eth0 rx 4096 tx 4096

# Check for buffer overruns
netstat -i  # Look at RX-OVR and TX-OVR
```

**TCP Retransmissions**:
```bash
# Monitor retransmissions
ss -ti | grep -i retrans
netstat -s | grep -i retrans

# Check TCP buffer sizes
sysctl net.ipv4.tcp_rmem
sysctl net.ipv4.tcp_wmem

# Optimize TCP buffers
sysctl -w net.ipv4.tcp_rmem="4096 87380 134217728"
sysctl -w net.ipv4.tcp_wmem="4096 65536 134217728"
sysctl -w net.core.rmem_max=134217728
sysctl -w net.core.wmem_max=134217728

# Enable TCP BBR congestion control
modprobe tcp_bbr
sysctl -w net.ipv4.tcp_congestion_control=bbr
```

**Network Latency Spikes**:
```bash
# Measure latency
ping -c 100 <destination>
mtr -r -c 100 <destination>

# Check for network interface errors
ethtool -S eth0 | grep -i error

# Disable interrupt coalescing (reduce latency)
ethtool -C eth0 rx-usecs 0 tx-usecs 0

# Enable RPS/RFS for multi-core scaling
echo "ff" > /sys/class/net/eth0/queues/rx-0/rps_cpus
```

### cgroups Issues

**cgroup OOM Kills**:
```bash
# Check cgroup memory limit
cat /sys/fs/cgroup/memory/myapp/memory.limit_in_bytes
cat /sys/fs/cgroup/memory/myapp/memory.usage_in_bytes

# Check OOM events
cat /sys/fs/cgroup/memory/myapp/memory.oom_control

# Monitor memory pressure (cgroups v2)
cat /sys/fs/cgroup/myapp/memory.pressure

# Solutions:
# 1. Increase memory limit
echo 4294967296 > /sys/fs/cgroup/memory/myapp/memory.limit_in_bytes

# 2. Enable memory.high soft limit (cgroups v2)
echo 3221225472 > /sys/fs/cgroup/myapp/memory.high  # 3GB warning
```

**CPU Throttling**:
```bash
# Check CPU usage and throttling (cgroups v2)
cat /sys/fs/cgroup/myapp/cpu.stat
# Look for nr_throttled and throttled_usec

# Check quota vs period
cat /sys/fs/cgroup/myapp/cpu.max

# Increase CPU quota
echo "500000 100000" > /sys/fs/cgroup/myapp/cpu.max  # 5 CPUs

# Monitor with systemctl (for systemd services)
systemctl status myapp.service
# Look for "CPU: <usage>"
```

### eBPF Troubleshooting

**eBPF Program Won't Load**:
```bash
# Check error message
bpftool prog load program.o /sys/fs/bpf/myprog
# Common errors:
# - Kernel version mismatch (BTF CO-RE issue)
# - Invalid instruction
# - Stack size exceeded

# Verify eBPF support
cat /proc/sys/kernel/unprivileged_bpf_disabled

# Check loaded programs
bpftool prog list

# Unload stuck programs
bpftool prog show id <id>
rm /sys/fs/bpf/<prog-name>
```

**XDP Performance Not Improved**:
```bash
# Verify XDP mode (native vs generic)
ip link show dev eth0
# Look for "xdpgeneric" (slow) vs "xdp" (fast)

# Ensure native XDP support
ethtool -i eth0 | grep driver
# Check if driver supports XDP

# Monitor XDP statistics
bpftool prog show id <xdp-id>
cat /sys/class/net/eth0/statistics/rx_xdp_drop
```

### NUMA Issues

**Cross-NUMA Memory Access**:
```bash
# Check NUMA topology
numactl --hardware
lscpu | grep NUMA

# Identify cross-NUMA traffic
numastat
numastat -p <pid>

# Check NUMA misses
perf stat -e node-loads,node-load-misses -- <command>

# Solutions:
# 1. Pin process to NUMA node
numactl --membind=0 --cpunodebind=0 <command>

# 2. Enable automatic NUMA balancing
echo 1 > /proc/sys/kernel/numa_balancing

# 3. Use NUMA-aware allocations in application
```

### Real-Time Latency Issues

**High Latency Spikes**:
```bash
# Measure latency with cyclictest
cyclictest -m -Sp90 -i200 -h400 -q -D 24h

# Check for latency sources
hwlatdetect --duration=60

# Common causes:
# 1. SMI interrupts
# Check BIOS settings, disable SMI if possible

# 2. Timer tick interrupts
# Verify nohz_full is active
cat /sys/devices/system/cpu/nohz_full

# 3. RCU callbacks
# Offload RCU to housekeeping CPUs
# Add to kernel cmdline: rcu_nocbs=2-7

# 4. TLB shootdowns
# Use huge pages to reduce TLB misses
```

**IRQ Affinity Not Working**:
```bash
# Check IRQ affinity
cat /proc/irq/<irq-num>/smp_affinity

# Set IRQ affinity
echo 2 > /proc/irq/<irq-num>/smp_affinity  # CPU 1

# Disable irqbalance if manual control needed
systemctl stop irqbalance
systemctl disable irqbalance
```

## Advanced Technologies

### eBPF Programming

**Basic eBPF Program Structure**
```c
// Count syscalls
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 1024);
    __type(key, u32);
    __type(value, u64);
} syscall_count SEC(".maps");

SEC("tracepoint/raw_syscalls/sys_enter")
int count_syscalls(struct trace_event_raw_sys_enter *ctx) {
    u32 key = ctx->id;
    u64 *count = bpf_map_lookup_elem(&syscall_count, &key);
    if (count) (*count)++;
    else {
        u64 init = 1;
        bpf_map_update_elem(&syscall_count, &key, &init, BPF_ANY);
    }
    return 0;
}
```

**BPF CO-RE (Compile Once Run Everywhere)**
```bash
# Use libbpf and BTF for portable programs
clang -O2 -g -target bpf -c program.bpf.c -o program.bpf.o

# Load with bpftool
bpftool prog load program.bpf.o /sys/fs/bpf/myprog
```

**Common eBPF Use Cases**
- System call tracing and filtering
- Network packet inspection (XDP)
- Performance monitoring (CPU, memory, I/O)
- Security monitoring (LSM hooks)
- Custom metrics collection

### io_uring for Async I/O

**Basic io_uring Setup**
```c
#include <liburing.h>

struct io_uring ring;
io_uring_queue_init(256, &ring, 0);

// Submit read operation
struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd, buf, size, offset);
io_uring_sqe_set_data(sqe, user_data);
io_uring_submit(&ring);

// Wait for completion
struct io_uring_cqe *cqe;
io_uring_wait_cqe(&ring, &cqe);
// Process result: cqe->res
io_uring_cqe_seen(&ring, cqe);
```

**io_uring Features**
- Zero-copy operations (IORING_OP_READ_FIXED)
- Batch submissions (reduce syscall overhead)
- Polling mode (IORING_SETUP_IOPOLL)
- Fixed files (IORING_REGISTER_FILES)
- Network operations (send, recv, accept)

### cgroups v2 Unified Hierarchy

**Migration from v1 to v2**
```bash
# Enable cgroups v2
mount -t cgroup2 none /sys/fs/cgroup

# Create cgroup
mkdir /sys/fs/cgroup/myapp

# Set CPU limit (50% of one CPU)
echo "50000 100000" > /sys/fs/cgroup/myapp/cpu.max

# Set memory limit (2GB)
echo "2147483648" > /sys/fs/cgroup/myapp/memory.max

# Move process to cgroup
echo $PID > /sys/fs/cgroup/myapp/cgroup.procs
```

**Pressure Stall Information (PSI)**
```bash
# Monitor resource pressure
cat /proc/pressure/cpu
cat /proc/pressure/memory
cat /proc/pressure/io

# Output format:
# some avg10=2.00 avg60=1.50 avg300=1.00 total=500000
# full avg10=0.50 avg60=0.30 avg300=0.20 total=100000
```
- **some**: Some processes delayed
- **full**: All processes delayed
- Use for load shedding decisions

### Real-Time Kernel Tuning

**PREEMPT_RT Kernel**
```bash
# Check if kernel is real-time
uname -a | grep PREEMPT_RT

# Install RT kernel (Debian/Ubuntu)
apt-get install linux-image-rt-amd64

# Verify preemption mode
cat /sys/kernel/debug/sched/preempt
```

**Real-Time Scheduling**
```bash
# Set SCHED_FIFO with priority 50
chrt -f 50 my-realtime-app

# CPU isolation for real-time
# Add to kernel cmdline: isolcpus=2-7 nohz_full=2-7

# Disable timer ticks on isolated CPUs
echo 0 > /proc/sys/kernel/timer_migration
```

**Latency Analysis**
```bash
# Measure latency with cyclictest
cyclictest -m -Sp90 -i200 -h400 -q

# Hardware latency detection
hwlatdetect --duration=60
```

## References

### Kernel Documentation
- `/references/kernel-tuning-guide.md` - Comprehensive tuning guide
- `/references/scheduler-tuning.md` - CFS scheduler deep dive
- `/references/network-stack-tuning.md` - Network optimization details
- `/references/ebpf-programming-guide.md` - eBPF development guide
- `/references/io_uring-guide.md` - io_uring usage patterns
- `/references/cgroups-v2-migration.md` - cgroups v2 migration
- `/references/realtime-kernel-guide.md` - Real-time kernel setup

### Profiling Tools
- `/references/perf-guide.md` - Perf profiling guide
- `/references/flamegraph-guide.md` - Flame graph visualization
- `/references/bpftrace-scripts.md` - bpftrace examples
- `/references/ebpf-tools.md` - BCC and libbpf tools
- `/assets/profiling-checklist.md` - Profiling checklist

### Advanced Topics
- `/references/psi-monitoring.md` - PSI-based load management
- `/references/dpdk-setup.md` - DPDK userspace networking
- `/references/xdp-programming.md` - XDP packet processing
