# Comprehensive KVM Tuning Guide

## CPU Optimization

### Host-Passthrough Mode
```xml
<cpu mode='host-passthrough' check='none'>
  <topology sockets='1' cores='4' threads='1'/>
  <feature policy='require' name='invtsc'/>  <!-- Invariant TSC -->
  <feature policy='require' name='tsc-deadline'/>
  <cache mode='passthrough'/>
</cpu>
```

### CPU Pinning
```bash
# Pin vCPUs 0-3 to pCPUs 0-3
virsh vcpupin vm-name 0 0
virsh vcpupin vm-name 1 1
virsh vcpupin vm-name 2 2
virsh vcpupin vm-name 3 3

# Pin emulator threads
virsh emulatorpin vm-name 8-9
```

## Memory Optimization

### Huge Pages (1GB)
```bash
# Allocate huge pages
echo 32 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages

# VM configuration
<memoryBacking>
  <hugepages>
    <page size='1048576' unit='KiB' nodeset='0'/>
  </hugepages>
  <locked/>
</memoryBacking>
```

### Disable THP
```bash
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

## Network Optimization

### Multi-Queue virtio-net
```xml
<interface type='bridge'>
  <model type='virtio'/>
  <driver queues='4'>  <!-- Match vCPU count -->
    <host tso4='on' tso6='on'/>
    <guest tso4='on' tso6='on'/>
  </driver>
</interface>
```

### Guest Configuration
```bash
# Enable multi-queue
ethtool -L eth0 combined 4

# Increase ring buffers
ethtool -G eth0 rx 4096 tx 4096
```

## Storage Optimization

### Native AIO with O_DIRECT
```xml
<disk type='block' device='disk'>
  <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'/>
  <source dev='/dev/vg0/vm-disk'/>
  <target dev='vda' bus='virtio'/>
</disk>
```

### I/O Threading
```xml
<iothreads>4</iothreads>
<disk>
  <driver iothread='1' queues='4'/>
</disk>
```

## Quick Wins Checklist

- [ ] CPU pinning enabled
- [ ] Huge pages configured
- [ ] Multi-queue networking
- [ ] Native AIO for storage
- [ ] NUMA alignment correct
- [ ] TSC clocksource
- [ ] Frequency scaling disabled
