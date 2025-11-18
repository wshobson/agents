# CPU Steal Time Diagnosis Guide

## Detection Methods

### 1. Top Command
```bash
top
# Look at %st column
%Cpu(s): 2.0 us, 1.0 sy, 0.0 ni, 90.0 id, 0.0 wa, 0.0 hi, 0.5 si, 6.5 st
```

### 2. mpstat (Per-CPU Stats)
```bash
mpstat -P ALL 1 10
# Shows steal time per CPU
```

### 3. sar (Historical Data)
```bash
sar -u ALL -s 00:00:00 -e 23:59:59
# View historical CPU steal time
```

## Root Cause Analysis

### CPU Overcommitment
- vCPU to pCPU ratio > 1.5:1
- Multiple VMs competing for same physical CPUs

### Noisy Neighbors
- Other VMs consuming disproportionate CPU
- Bursty workloads causing contention

### SMT Contention
- Sibling hardware threads competing
- Hyper-Threading overhead

### NUMA Misalignment
- Memory access across NUMA nodes
- Cross-NUMA scheduling overhead

## Diagnostic Commands

```bash
# View vCPU mapping
virsh vcpuinfo vm-name

# Check CPU affinity
taskset -p <pid>

# Monitor steal time continuously
watch -n 1 'mpstat 1 1 | grep Average'

# Check NUMA topology
numactl --hardware
```

## Quick Diagnosis Checklist

- [ ] Steal time > 5%?
- [ ] vCPU overcommitted?
- [ ] CPU pinning configured?
- [ ] NUMA alignment correct?
- [ ] SMT enabled?
- [ ] Other VMs on same host?
