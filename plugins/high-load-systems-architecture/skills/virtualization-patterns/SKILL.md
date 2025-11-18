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

## Troubleshooting Virtualization Issues

### VM Performance Problems

**VM Running Slow**:
```bash
# Check host resource usage
top
free -h
iostat -x 1 5

# Check VM resource allocation
virsh dominfo <vm-name>
virsh vcpuinfo <vm-name>

# Monitor VM CPU usage from host
virt-top

# Check CPU steal time (inside VM)
top  # Look at 'st' (steal time) column
vmstat 1 5  # 'st' column

# Solutions:
# 1. Reduce CPU overcommit ratio
# 2. Pin vCPUs to physical CPUs
virsh vcpupin <vm-name> 0 0  # Pin vCPU 0 to physical CPU 0

# 3. Set CPU topology
virsh edit <vm-name>
# Add: <topology sockets='1' cores='2' threads='2'/>
```

**High I/O Latency in VM**:
```bash
# Check I/O scheduler (inside VM)
cat /sys/block/vda/queue/scheduler

# Check virtio-blk vs virtio-scsi
lsblk -o NAME,ROTA,DISC-GRAN,DISC-MAX
virsh domblklist <vm-name>

# Test I/O performance
fio --filename=/dev/vda --direct=1 --rw=randread --bs=4k --ioengine=libaio --iodepth=32

# Solutions:
# 1. Use virtio-scsi for better performance
<disk type='file' device='disk'>
  <driver name='qemu' type='raw' cache='none' io='native'/>
  <target dev='sda' bus='scsi'/>
</disk>

# 2. Enable discard/trim
<disk type='file' device='disk'>
  <driver name='qemu' type='raw' discard='unmap'/>
</disk>

# 3. Use raw format instead of qcow2
qemu-img convert -f qcow2 -O raw source.qcow2 destination.raw
```

**VM Network Performance Issues**:
```bash
# Check network device type
virsh dumpxml <vm-name> | grep -A 5 "interface type"

# Test network throughput
iperf3 -c <server-ip> -t 60

# Check for packet drops
ethtool -S <interface> | grep drop

# Solutions:
# 1. Use virtio-net for best performance
<interface type='bridge'>
  <model type='virtio'/>
</interface>

# 2. Enable multi-queue
<interface type='bridge'>
  <driver queues='4'/>
  <model type='virtio'/>
</interface>

# 3. Use vhost-net kernel acceleration
modprobe vhost_net
# Should be enabled by default with virtio

# 4. For ultimate performance: SR-IOV
# (see SR-IOV section in Advanced Features)
```

### VM Won't Start

**VM Fails to Start**:
```bash
# Check error messages
virsh start <vm-name>
journalctl -u libvirtd -n 50

# Check QEMU logs
tail -50 /var/log/libvirt/qemu/<vm-name>.log

# Common issues:

# 1. Missing disk image
virsh domblklist <vm-name>
ls -lh /var/lib/libvirt/images/<disk.img>

# 2. Permission issues
chown qemu:qemu /var/lib/libvirt/images/<disk.img>
chmod 644 /var/lib/libvirt/images/<disk.img>

# 3. Locked by another process
virsh domblkinfo <vm-name> vda
lsof | grep <disk.img>

# 4. Insufficient resources
free -h  # Check available RAM
virsh dominfo <vm-name>  # Check VM memory requirement
```

**VM in Paused State**:
```bash
# Check VM state
virsh domstate <vm-name>

# Resume paused VM
virsh resume <vm-name>

# Common causes:
# 1. I/O error on disk
virsh domblkerror <vm-name>

# 2. Host out of memory
dmesg | grep -i "out of memory"
free -h

# 3. Storage backend unreachable (e.g., Ceph down)
ceph -s  # If using Ceph
```

### Live Migration Issues

**Migration Fails**:
```bash
# Attempt migration with verbose logging
virsh migrate --live --verbose <vm-name> qemu+ssh://dest-host/system

# Check migration progress
virsh domjobinfo <vm-name>

# Common failures:

# 1. Incompatible CPU models
# Source and destination must have compatible CPUs
virsh domcapabilities
# Solution: Use <cpu mode='host-model'/> or specific model

# 2. Storage not accessible on destination
# For shared storage: ensure both hosts can access
# For non-shared: use --copy-storage-all
virsh migrate --live --copy-storage-all <vm-name> qemu+ssh://dest/system

# 3. Network connectivity issues
ping <dest-host>
ssh <dest-host> hostname

# 4. libvirt version mismatch
virsh version  # Run on both hosts
```

**Migration Too Slow / Never Completes**:
```bash
# Check memory dirtying rate
virsh domstats <vm-name> | grep dirty

# Monitor migration progress
virsh domjobinfo <vm-name>
# Look at "Data remaining" and "Data processed"

# Solutions:
# 1. Reduce workload during migration
# 2. Increase migration bandwidth
virsh migrate-setmaxdowntime <vm-name> 1000  # 1 second

# 3. Use post-copy migration (higher risk)
virsh migrate --live --postcopy <vm-name> qemu+ssh://dest/system

# 4. Suspend and resume instead of live migrate
virsh suspend <vm-name>
virsh migrate <vm-name> qemu+ssh://dest/system
virsh resume <vm-name>
```

### Memory Issues

**VM Memory Ballooning Not Working**:
```bash
# Check balloon driver in VM
lsmod | grep virtio_balloon  # Inside VM

# Check balloon size from host
virsh dommemstat <vm-name>

# Set balloon target
virsh setmem <vm-name> 2048M --live

# Solutions:
# 1. Ensure balloon driver is loaded in guest
modprobe virtio_balloon  # Inside VM

# 2. Check VM XML configuration
virsh edit <vm-name>
# Ensure: <memballoon model='virtio'/>

# 3. Install guest agent
apt-get install qemu-guest-agent  # Debian/Ubuntu
yum install qemu-guest-agent      # RHEL/CentOS
systemctl start qemu-guest-agent
```

**Huge Pages Not Working**:
```bash
# Check huge pages allocation on host
cat /proc/meminfo | grep Huge
hugeadm --pool-list

# Allocate huge pages
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# Verify VM is using huge pages
virsh dumpxml <vm-name> | grep hugepages
grep -i huge /proc/<qemu-pid>/smaps

# Solutions:
# 1. Pre-allocate huge pages
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# 2. Make persistent
echo "vm.nr_hugepages = 1024" >> /etc/sysctl.conf
sysctl -p

# 3. Configure VM to use huge pages
<memoryBacking>
  <hugepages/>
</memoryBacking>
```

### SR-IOV Issues

**VF Not Available**:
```bash
# Check if SR-IOV is enabled
lspci | grep "Virtual Function"

# Check VF count
cat /sys/class/net/<pf-interface>/device/sriov_numvfs

# Enable SR-IOV
echo 8 > /sys/class/net/<pf-interface>/device/sriov_numvfs

# Check for errors
dmesg | tail -20

# Common issues:
# 1. IOMMU not enabled
# Add to kernel cmdline: intel_iommu=on iommu=pt
dmesg | grep -i iommu

# 2. NIC driver doesn't support SR-IOV
ethtool -i <interface> | grep driver
# Check driver documentation for SR-IOV support
```

**VM Can't Use VF**:
```bash
# Verify VF is bound to vfio-pci
lspci -k -s <vf-pci-address>
# Should show: Kernel driver in use: vfio-pci

# Bind VF to vfio-pci
echo <vf-pci-address> > /sys/bus/pci/drivers/<current-driver>/unbind
echo <vendor-id> <device-id> > /sys/bus/pci/drivers/vfio-pci/new_id

# Check VM XML
virsh dumpxml <vm-name> | grep -A 10 hostdev

# Inside VM: verify device
lspci | grep Ethernet
ip link show
```

### GPU Passthrough Issues

**GPU Not Accessible in VM**:
```bash
# Check GPU is bound to vfio-pci
lspci -k | grep -A 3 VGA

# Bind GPU to vfio-pci
echo <gpu-pci-address> > /sys/bus/pci/drivers/nvidia/unbind
echo <vendor-id> <device-id> > /sys/bus/pci/drivers/vfio-pci/new_id

# Check IOMMU groups
find /sys/kernel/iommu_groups/ -type l

# Verify VM configuration
virsh dumpxml <vm-name> | grep -A 10 hostdev

# Inside VM: check GPU
lspci | grep VGA
nvidia-smi  # For NVIDIA GPUs
```

**Error 43 with NVIDIA GPU**:
```bash
# NVIDIA detects it's running in VM and disables
# Solution: Hide VM from NVIDIA driver

virsh edit <vm-name>
# Add inside <features>:
<features>
  <hyperv>
    <vendor_id state='on' value='1234567890ab'/>
  </hyperv>
  <kvm>
    <hidden state='on'/>
  </kvm>
</features>

# Also set CPU to host-passthrough
<cpu mode='host-passthrough'/>
```

### Nested Virtualization Issues

**Nested VMs Won't Start**:
```bash
# Check if nested virtualization is enabled (host)
cat /sys/module/kvm_intel/parameters/nested  # Intel
cat /sys/module/kvm_amd/parameters/nested    # AMD

# Enable nested virtualization
echo "options kvm-intel nested=1" > /etc/modprobe.d/kvm-intel.conf
modprobe -r kvm-intel
modprobe kvm-intel

# Check L1 VM has VMX/SVM flag
virsh dumpxml <vm-name> | grep cpu
# Should have:
<cpu mode='host-passthrough'>
  <feature policy='require' name='vmx'/>  <!-- Intel -->
</cpu>

# Inside L1 VM: verify
egrep -o '(vmx|svm)' /proc/cpuinfo
```

**Poor Performance in Nested VMs**:
```bash
# Expected: 10-30% overhead vs native
# If worse, check:

# 1. CPU mode should be host-passthrough
virsh dumpxml <l1-vm> | grep cpu

# 2. Enable EPT/NPT (should be automatic)
cat /sys/module/kvm_intel/parameters/ept

# 3. Reduce nesting depth (L3+ very slow)
# Consider: containers in L1 VM instead of L2 VMs
```

### Monitoring and Diagnostics

**Collect VM Performance Data**:
```bash
# CPU stats
virsh vcpuinfo <vm-name>
virsh cpu-stats <vm-name>

# Memory stats
virsh dommemstat <vm-name>

# Disk I/O stats
virsh domblkstat <vm-name> vda

# Network stats
virsh domifstat <vm-name> vnet0

# Comprehensive monitoring
virt-top
```

**Enable Debug Logging**:
```bash
# Enable libvirt debug logging
virsh log --level 1  # 1 = debug, 4 = error

# Check logs
journalctl -u libvirtd -f

# QEMU debug
# Edit VM XML:
<domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
  <qemu:commandline>
    <qemu:arg value='-d'/>
    <qemu:arg value='cpu,exec,int'/>
  </qemu:commandline>
</domain>
```

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
