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

## Advanced Virtualization Features

### SR-IOV (Single Root I/O Virtualization)

**Enabling SR-IOV**
```bash
# Enable SR-IOV on physical function (PF)
echo 8 > /sys/class/net/eth0/device/sriov_numvfs

# Verify virtual functions (VFs) created
lspci | grep "Virtual Function"

# Bind VF to vfio-pci driver
echo "8086 154c" > /sys/bus/pci/drivers/vfio-pci/new_id
```

**VM Configuration with SR-IOV**
```xml
<interface type='hostdev' managed='yes'>
  <source>
    <address type='pci' domain='0x0000' bus='0x03' slot='0x10' function='0x0'/>
  </source>
  <mac address='52:54:00:12:34:56'/>
  <model type='virtio'/>
</interface>
```
- Pros: Near-native network performance, low CPU overhead
- Cons: Live migration not supported, VF management complexity
- Use case: High-throughput networking, low-latency applications

### GPU Passthrough & vGPU

**Full GPU Passthrough**
```bash
# Enable IOMMU in kernel cmdline
# intel_iommu=on iommu=pt (Intel)
# amd_iommu=on iommu=pt (AMD)

# Bind GPU to vfio-pci
echo "10de 1b80" > /sys/bus/pci/drivers/vfio-pci/new_id

# VM configuration
<hostdev mode='subsystem' type='pci' managed='yes'>
  <source>
    <address domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
  </source>
</hostdev>
```
- Pros: Full GPU performance, native drivers
- Cons: No sharing, live migration not supported
- Use case: GPU-intensive workloads, ML training

**vGPU (GPU Virtualization)**
```xml
<!-- NVIDIA vGPU configuration -->
<hostdev mode='subsystem' type='mdev' managed='no' model='vfio-pci'>
  <source>
    <address uuid='b0123456-7890-abcd-ef12-3456789abcde'/>
  </source>
</hostdev>
```
- Pros: GPU sharing among VMs, live migration possible
- Cons: Reduced performance vs passthrough, licensing costs
- Use case: VDI, multi-tenant GPU sharing

### vDPA (virtio Data Path Acceleration)

**vDPA Architecture**
```
VM (virtio driver) → vDPA device → Hardware (NIC/vDPA capable)
```
- Hardware-accelerated virtio
- Combines virtio compatibility with hardware performance
- Use case: High-performance I/O with live migration support

**vDPA Configuration**
```bash
# Load vdpa modules
modprobe vdpa
modprobe vhost_vdpa

# Create vDPA device
vdpa dev add name vdpa0 mgmtdev pci/0000:03:00.0

# VM uses vhost-vdpa backend
<interface type='vdpa'>
  <source dev='/dev/vhost-vdpa-0'/>
  <model type='virtio'/>
</interface>
```

### Confidential Computing

**AMD SEV (Secure Encrypted Virtualization)**
```xml
<domain type='kvm'>
  <launchSecurity type='sev'>
    <policy>0x0003</policy>
    <cbitpos>47</cbitpos>
    <reducedPhysBits>1</reducedPhysBits>
  </launchSecurity>
</domain>
```
- VM memory encrypted with per-VM key
- Protects against hypervisor/physical attacks
- Use case: Sensitive workloads, compliance

**Intel TDX (Trust Domain Extensions)**
```xml
<domain type='kvm'>
  <features>
    <tdx/>
  </features>
</domain>
```
- Hardware-isolated trusted execution environment
- Protection from compromised hypervisor
- Use case: Confidential cloud computing

### MicroVM Patterns

**Firecracker (AWS Lambda)**
```bash
# Start Firecracker microVM
firecracker --api-sock /tmp/firecracker.socket

# Configure via API
curl -X PUT 'http://localhost/boot-source' \
  -H 'Content-Type: application/json' \
  -d '{"kernel_image_path": "/path/to/kernel", "boot_args": "console=ttyS0"}'

# Start VM
curl -X PUT 'http://localhost/actions' \
  -d '{"action_type": "InstanceStart"}'
```
- Minimal device model (virtio-block, virtio-net only)
- Fast boot (<125ms)
- Low memory overhead (<5MB)
- Use case: Serverless, FaaS platforms

**Cloud Hypervisor**
```bash
# Start Cloud Hypervisor VM
cloud-hypervisor \
  --kernel /path/to/vmlinux \
  --disk path=/path/to/disk.raw \
  --cpus boot=2 \
  --memory size=1G
```
- Rust-based, KVM-optimized
- Modern VMM with minimal attack surface
- Use case: Cloud-native workloads, Kubernetes

### Nested Virtualization

**Enable Nested Virtualization**
```bash
# Intel
echo "options kvm-intel nested=1" > /etc/modprobe.d/kvm-intel.conf
modprobe -r kvm-intel
modprobe kvm-intel

# AMD
echo "options kvm-amd nested=1" > /etc/modprobe.d/kvm-amd.conf
modprobe -r kvm-amd
modprobe kvm-amd

# Verify
cat /sys/module/kvm_intel/parameters/nested  # Y = enabled
```

**L1 VM Configuration for Nested Virtualization**
```xml
<cpu mode='host-passthrough'>
  <feature policy='require' name='vmx'/>  <!-- Intel -->
  <!-- OR -->
  <feature policy='require' name='svm'/>  <!-- AMD -->
</cpu>
```
- Use case: Development, testing, cloud provider infrastructure
- Performance: 10-30% overhead vs native virtualization

## Performance Benchmarking

### Storage Benchmarking
```bash
# fio sequential read
fio --name=seqread --rw=read --bs=1M --size=10G --runtime=60

# fio random IOPS
fio --name=randread --rw=randread --bs=4k --iodepth=32 --runtime=60

# Compare raw vs qcow2 vs rbd
```

### Network Benchmarking
```bash
# iperf3 throughput test
iperf3 -c server_ip -t 60 -P 4

# netperf latency test
netperf -H server_ip -t TCP_RR

# Compare virtio-net vs SR-IOV
```

### CPU Benchmarking
```bash
# sysbench CPU test
sysbench cpu --threads=4 --time=60 run

# Measure vCPU overhead
# Compare pinned vs unpinned vCPUs
```

## References

### KVM & libvirt
- `/references/kvm-architecture.md` - KVM deep dive
- `/references/libvirt-xml-guide.md` - VM XML reference
- `/references/live-migration.md` - Live migration details
- `/references/nested-virtualization.md` - Nested virt setup

### Advanced Features
- `/references/sriov-setup.md` - SR-IOV configuration guide
- `/references/gpu-passthrough.md` - GPU passthrough guide
- `/references/vgpu-setup.md` - vGPU configuration
- `/references/vdpa-guide.md` - vDPA setup and tuning
- `/references/confidential-computing.md` - SEV/TDX setup

### MicroVMs
- `/references/firecracker-guide.md` - Firecracker setup
- `/references/cloud-hypervisor.md` - Cloud Hypervisor guide
- `/references/kata-containers.md` - Kata Containers integration

### Performance Tuning
- `/references/cpu-tuning.md` - CPU configuration guide
- `/references/memory-tuning.md` - Memory optimization
- `/references/storage-tuning.md` - Storage optimization
- `/references/benchmarking-vms.md` - VM benchmarking guide

### Tools & Monitoring
- `/references/virsh-commands.md` - virsh command reference
- `/references/vm-monitoring.md` - Monitoring VMs
- `/references/performance-profiling.md` - VM performance analysis
- `/assets/vm-sizing-template.md` - VM sizing worksheet
- `/assets/benchmark-results.md` - Benchmark comparison data
