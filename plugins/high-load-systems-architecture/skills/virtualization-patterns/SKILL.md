---
name: virtualization-patterns
description: Comprehensive guide to virtualization patterns, KVM/libvirt optimization, VM performance tuning, and cloud platform design. Covers hypervisor architecture, resource allocation, live migration, and VM sizing. Use when optimizing VM performance, designing cloud infrastructure, planning VM deployment strategies, or evaluating virtualization technologies.
---

# Virtualization Patterns

## When to Use This Skill

- Designing KVM/libvirt infrastructure for cloud platforms
- Optimizing VM performance and resource utilization
- Planning VM deployment strategies and sizing
- Configuring live migration for maintenance
- Selecting VM CPU and memory configurations
- Reducing hypervisor overhead
- Implementing multi-tenant isolation

## Core Concepts

### KVM Architecture

**KVM (Kernel-based Virtual Machine)**
- Linux kernel module for virtualization
- Hardware-based virtualization (Intel VT, AMD-V)
- No standalone hypervisor; runs as kernel module

**QEMU Integration**
- QEMU: User-space emulator and machine model
- KVM: Accelerates QEMU with hardware virtualization
- Together: Full VM with near-native performance

**Boot Process**
```
QEMU process (user space)
  ↓ (system calls)
KVM kernel module
  ↓ (hardware)
CPU with VMX/SVM support (Intel/AMD)
  ↓
VM-Exit → KVM handles → VM-Entry
```

### CPU Configuration

**vCPU Allocation**
```bash
# Simple allocation
<vcpu placement='static'>4</vcpu>

# NUMA-aware allocation (2 vCPUs per NUMA node)
<vcpu placement='static'>4</vcpu>
<numatune>
  <memory mode='strict' nodeset='0-1'/>
</numatune>

# CPU pinning (pinning vCPU 0 to physical CPU 0)
<cputune>
  <vcpupin vcpu='0' cpuset='0'/>
  <vcpupin vcpu='1' cpuset='1'/>
  <vcpupin vcpu='2' cpuset='2'/>
  <vcpupin vcpu='3' cpuset='3'/>
</cputune>
```

**CPU Model Selection**
```bash
# List available CPU models
virsh domcapabilities

# Detailed CPU model
<cpu mode='host-model'/>           # Pass through host CPU
<cpu mode='host-passthrough'/>     # Direct pass-through
<cpu model='Nehalem'/>             # Specific model (migration compatible)
```

**Overcommit vs Pinning**
- **Overcommit**: 8 vCPUs on 4 physical CPUs (2x overcommit)
  - Pros: Higher density, flexibility
  - Cons: Scheduling overhead, variable performance
  - Use for: Bursty, non-critical workloads

- **Pinning**: 4 vCPUs on 4 physical CPUs (1:1)
  - Pros: Predictable performance, low latency
  - Cons: Lower density, hardware utilization
  - Use for: Latency-sensitive, critical workloads

### Memory Configuration

**Memory Allocation**
```bash
# Static memory
<memory unit='GiB'>16</memory>
<currentMemory unit='GiB'>16</currentMemory>

# Ballooning (dynamic adjustment)
<memory unit='GiB'>32</memory>
<currentMemory unit='GiB'>16</currentMemory>
<memballoon model='virtio'/>
```

**Huge Pages**
```bash
# Allocate huge pages to VM
<hugepages>
  <page size='1048576' unit='KiB' nodeset='0'/>  # 1GB pages
</hugepages>

# On host, pre-allocate huge pages
echo 16 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages
```
- Benefits: Better TLB efficiency, reduced page faults
- Overhead: More memory consumed, less flexibility
- Typical: 2MB or 1GB huge pages

**NUMA Configuration**
```bash
# NUMA pinning for memory locality
<numatune>
  <memory mode='strict' nodeset='0'/>  # Use NUMA node 0
  <memnode cellid='0' mode='strict' nodeset='0'/>
  <memnode cellid='1' mode='strict' nodeset='1'/>
</numatune>
```

**Memory Balloon Driver**
- Allow hypervisor to reclaim unused guest memory
- Host can request guest to release pages
- Guest releases least-used pages (like page cache)
- Risk: Guest OOM killer triggered

**Memory Swap (Guest)**
```bash
# Disable swap in guest for predictable performance
swapoff -a

# Or use memory limit to prevent swap
<memtune>
  <hard_limit unit='GiB'>16</hard_limit>  # Maximum memory
</memtune>
```

### Storage Configuration

**Block Device Types**

**QCOW2 (Copy-On-Write)**
- Sparse format, grows as needed
- Snapshots support
- Slower than raw (extra metadata ops)
```bash
<disk type='file' device='disk'>
  <driver name='qemu' type='qcow2'/>
  <source file='/var/lib/libvirt/images/disk.qcow2'/>
</disk>
```

**Raw Format**
- Direct access, no copy-on-write overhead
- Faster performance
- Cannot shrink
```bash
<disk type='file' device='disk'>
  <driver name='qemu' type='raw'/>
  <source file='/dev/vg0/vm-disk'/>
</disk>
```

**RBD (Ceph Block Device)**
- Distributed storage, high availability
- Network latency, good for scale-out
```bash
<disk type='network' device='disk'>
  <driver name='qemu' type='raw'/>
  <source protocol='rbd' name='vms/disk-0'>
    <host name='ceph-mon-1' port='6789'/>
  </source>
</disk>
```

**I/O Cache Settings**
```bash
<driver cache='writethrough'/>  # Write-through (safe, slower)
<driver cache='writeback'/>     # Write-back (faster, risky)
<driver cache='unsafe'/>        # No caching (fastest, very risky)
```

**I/O Tuning**
```bash
<disk>
  <iotune>
    <total_bytes_sec>10485760</total_bytes_sec>  # 10 MB/s limit
    <read_iops_sec>1000</read_iops_sec>
    <write_iops_sec>1000</write_iops_sec>
  </iotune>
</disk>
```

### Network Configuration

**Virtio Network Device**
- Paravirtual network device (better than emulated)
- Lower CPU overhead, higher throughput
```bash
<interface type='bridge'>
  <model type='virtio'/>
  <source bridge='br0'/>
</interface>
```

**Network Tuning**
```bash
<interface>
  <bandwidth>
    <inbound average='10240' peak='10485760'/>  # 10MB/s average
    <outbound average='10240' peak='10485760'/>
  </bandwidth>
</interface>
```

**Multi-Queue Network**
- Multiple TX/RX queues for parallel processing
- Improves throughput
```bash
<interface type='bridge'>
  <driver queues='4'/>
  <model type='virtio'/>
</interface>
```

## VM Performance Optimization

### Low-Latency VMs

**Configuration Template**
```xml
<domain type='kvm'>
  <name>low-latency</name>

  <!-- CPU pinning -->
  <vcpu placement='static'>4</vcpu>
  <cputune>
    <vcpupin vcpu='0' cpuset='0'/>
    <vcpupin vcpu='1' cpuset='1'/>
    <vcpupin vcpu='2' cpuset='2'/>
    <vcpupin vcpu='3' cpuset='3'/>
  </cputune>

  <!-- CPU model -->
  <cpu mode='host-passthrough'>
    <feature policy='require' name='rdtscp'/>
  </cpu>

  <!-- Memory with huge pages -->
  <memory unit='GiB'>16</memory>
  <hugepages>
    <page size='1048576' unit='KiB' nodeset='0'/>
  </hugepages>

  <!-- Storage: raw device -->
  <disk type='block' device='disk'>
    <driver name='qemu' type='raw' cache='writethrough'/>
    <source dev='/dev/vg0/vm-disk'/>
  </disk>

  <!-- Network: virtio -->
  <interface type='bridge'>
    <model type='virtio'/>
    <source bridge='br0'/>
  </interface>
</domain>
```

**Host Configuration**
```bash
# 1. CPU isolation
echo "isolcpus=0-3" >> /etc/default/grub
grub-mkconfig -o /boot/grub/grub.cfg

# 2. Disable frequency scaling
echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# 3. Set realtime VM processes
chrt -f -p 50 <pid>

# 4. Disable transparent huge pages
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

### High-Throughput VMs

**Configuration Template**
```xml
<domain type='kvm'>
  <name>high-throughput</name>

  <!-- CPU overcommit -->
  <vcpu placement='static'>8</vcpu>
  <!-- No CPU pinning for flexibility -->

  <!-- CPU model: wider feature set -->
  <cpu mode='host-model'/>

  <!-- Memory with transparent huge pages -->
  <memory unit='GiB'>32</memory>
  <!-- THP enabled in host -->

  <!-- Storage: raw for throughput -->
  <disk type='block' device='disk'>
    <driver name='qemu' type='raw' cache='writeback'/>
    <source dev='/dev/vg0/vm-disk'/>
  </disk>

  <!-- Network: multi-queue -->
  <interface type='bridge'>
    <driver queues='4'/>
    <model type='virtio'/>
    <source bridge='br0'/>
  </interface>
</domain>
```

### Balanced VMs (Default)

```xml
<domain type='kvm'>
  <name>balanced</name>

  <!-- Standard allocation -->
  <vcpu placement='static'>4</vcpu>
  <memory unit='GiB'>8</memory>

  <!-- Standard devices -->
  <disk type='file'>
    <driver name='qemu' type='qcow2'/>
    <source file='/var/lib/libvirt/images/disk.qcow2'/>
  </disk>

  <interface type='bridge'>
    <model type='virtio'/>
    <source bridge='br0'/>
  </interface>
</domain>
```

## Live Migration

**Pre-Copy Migration**
```
1. Migration starts on source host
2. All memory copied to destination
3. Modified pages tracked and retransmitted
4. Final cutover when remaining pages minimal
5. Brief downtime (usually < 1 sec)
```

**Post-Copy Migration**
```
1. Minimal state copied to destination
2. VM started on destination
3. Missing pages fetched on-demand from source
4. Minimal downtime (usually < 100ms)
5. Risk: Source failure loses data
```

**Live Migration Configuration**
```bash
# Enable live migration
virsh migrate --live vm-name qemu+ssh://dest-host/system

# Monitor progress
virsh domjobinfo vm-name

# Set migration parameters
virsh migrate-setmaxdowntime vm-name 1000  # 1 second
```

## Cloud Platform Design

### Compute Node Architecture
```
Compute Node
├─ 16 Physical CPUs (8 cores each)
├─ 256GB RAM
├─ 10GbE Network (2 NICs)
├─ 2x 1TB NVMe (for OS, VM cache)
├─ 8x 8TB SAS drives (via SAN)
│
└─ VMs running:
   ├─ VM1: 2 vCPU, 4GB RAM (web server)
   ├─ VM2: 4 vCPU, 8GB RAM (app server)
   ├─ VM3: 2 vCPU, 4GB RAM (cache)
   └─ VM4: 4 vCPU, 8GB RAM (database)
```

### VM Placement Strategy
- Spread vCPUs across NUMA nodes for locality
- Pin memory-intensive VMs to closest storage
- Balance network load across NICs
- Leave 20% CPU headroom for system

## References

### KVM & libvirt
- `/references/kvm-architecture.md` - KVM deep dive
- `/references/libvirt-xml-guide.md` - VM XML reference
- `/references/live-migration.md` - Live migration details

### Performance Tuning
- `/references/cpu-tuning.md` - CPU configuration guide
- `/references/memory-tuning.md` - Memory optimization
- `/references/storage-tuning.md` - Storage optimization

### Tools & Monitoring
- `/references/virsh-commands.md` - virsh command reference
- `/references/vm-monitoring.md` - Monitoring VMs
- `/assets/vm-sizing-template.md` - VM sizing worksheet
