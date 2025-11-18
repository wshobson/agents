# CFS Scheduler Tuning Guide

## Key Parameters

### sched_latency_ns
**Default**: 6000000 (6ms)
**Description**: Target latency for all tasks to get CPU time
**Tuning**: Increase for less preemption, lower for better responsiveness

```bash
# Reduce preemption overhead
echo 24000000 > /proc/sys/kernel/sched_latency_ns  # 24ms
```

### sched_min_granularity_ns
**Default**: 3000000 (3ms)
**Description**: Minimum time slice per task
**Tuning**: Increase to reduce context switch overhead

```bash
echo 10000000 > /proc/sys/kernel/sched_min_granularity_ns  # 10ms
```

### sched_wakeup_granularity_ns
**Default**: 4000000 (4ms)
**Description**: Preemption threshold for woken tasks
**Tuning**: Increase to reduce wakeup preemptions

```bash
echo 15000000 > /proc/sys/kernel/sched_wakeup_granularity_ns  # 15ms
```

## NUMA Balancing

```bash
# Disable automatic NUMA balancing (if using pinning)
echo 0 > /proc/sys/kernel/numa_balancing
```

## Monitoring

```bash
# Context switches per second
vmstat 1

# Per-CPU scheduling stats
cat /proc/schedstat

# Task scheduling latency
perf sched latency
```

## Workload-Specific Tuning

### Latency-Sensitive
```bash
sched_latency_ns=6000000        # Lower latency
sched_min_granularity_ns=3000000
sched_wakeup_granularity_ns=2000000
```

### Throughput-Optimized
```bash
sched_latency_ns=24000000       # Higher throughput
sched_min_granularity_ns=10000000
sched_wakeup_granularity_ns=15000000
```
