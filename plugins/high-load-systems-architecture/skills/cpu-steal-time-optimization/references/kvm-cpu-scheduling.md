# KVM CPU Scheduling

## Scheduler Architecture

### CFS (Completely Fair Scheduler)
- Default Linux scheduler
- Time-slicing based on nice values
- vCPU threads compete with other processes

### Real-Time Scheduling
- SCHED_FIFO: First-in-first-out
- SCHED_RR: Round-robin with time slices
- Higher priority than normal processes

## vCPU Thread Lifecycle

```
Guest CPU operation
    ↓ (VM-Exit)
KVM module (kernel space)
    ↓ (trap to userspace if needed)
QEMU process (userspace)
    ↓ (VM-Entry)
Guest continues execution
```

## Tuning Parameters

### Scheduler Latency
```bash
# Increase time slice (reduces preemption)
sysctl kernel.sched_latency_ns=24000000  # 24ms
```

### CPU Affinity
```bash
# Pin vCPU threads to specific CPUs
virsh vcpupin vm-name <vcpu> <pcpu>
```

### Real-Time Priority
```bash
# Set RT priority for vCPU threads
chrt -f -p 50 <vcp thread pid>
```

## Best Practices

1. Pin vCPUs to prevent migrations
2. Use real-time priority for latency-sensitive VMs
3. Disable NUMA balancing for pinned VMs
4. Monitor context switches (vmstat)
