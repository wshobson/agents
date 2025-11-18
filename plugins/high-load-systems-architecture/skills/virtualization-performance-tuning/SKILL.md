---
name: virtualization-performance-tuning
description: World-class expert guide to advanced virtualization performance optimization. Covers KVM/QEMU tuning, device passthrough, vhost optimization, virtio-net/blk tuning, memory ballooning, huge pages, NUMA optimization, nested virtualization, and hardware acceleration. Use when optimizing VM I/O performance, reducing virtualization overhead, tuning network/storage throughput, implementing advanced device passthrough, or achieving near-native performance in virtualized environments.
---

# Virtualization Performance Tuning

## When to Use This Skill

- Optimizing I/O performance (network, storage) in VMs
- Reducing virtualization overhead for critical workloads
- Tuning KVM/QEMU for maximum throughput
- Implementing hardware acceleration (SR-IOV, vDPA)
- Optimizing memory performance with huge pages
- Configuring NUMA-aware VM placement
- Troubleshooting VM performance bottlenecks
- Achieving near-native performance in virtualized environments
- Planning high-performance cloud infrastructure

## Core Concepts

### Virtualization Overhead Sources

**1. CPU Virtualization Overhead**
```
Overhead Sources:
├─ VM-Exit/VM-Entry transitions (1-5% overhead)
├─ Instruction emulation (0-10% overhead)
├─ Interrupt handling (1-3% overhead)
├─ Timer emulation (1-2% overhead)
└─ vCPU scheduling (1-5% overhead)

Total: 4-25% CPU overhead depending on workload
```

**2. Memory Virtualization Overhead**
```
Overhead Sources:
├─ Extended Page Tables (EPT/NPT): 2-5% overhead
├─ TLB misses: 5-10% overhead without huge pages
├─ Memory balloon driver: 1-2% overhead
├─ Page sharing (KSM): 3-8% overhead
└─ NUMA remote access: 10-50% latency penalty

Total: 10-30% memory overhead without optimization
```

**3. I/O Virtualization Overhead**
```
Overhead Sources:
├─ Emulated devices: 50-80% overhead
├─ Paravirtualized (virtio): 5-15% overhead
├─ Device passthrough (SR-IOV): <5% overhead
├─ Interrupt coalescing: 2-5% overhead
└─ I/O thread scheduling: 3-7% overhead

Total: 5-80% I/O overhead depending on method
```

### Performance Tuning Philosophy

**Performance Hierarchy (Best to Worst)**
```
1. Hardware Passthrough (PCI passthrough, SR-IOV)
   ├─ ~95-99% native performance
   └─ No hypervisor involvement

2. Hardware-Accelerated Paravirtualization (vDPA, vhost-user)
   ├─ ~85-95% native performance
   └─ Minimal hypervisor overhead

3. Kernel-Space Paravirtualization (vhost-net, vhost-blk)
   ├─ ~75-90% native performance
   └─ Reduced context switches

4. User-Space Paravirtualization (virtio)
   ├─ ~60-80% native performance
   └─ QEMU-mediated I/O

5. Full Emulation
   ├─ ~20-50% native performance
   └─ High CPU overhead
```

## Advanced CPU Optimization

### CPU Model Selection Strategy

**CPU Model Hierarchy**
```
host-passthrough
├─ Best performance (all features)
├─ No migration compatibility
└─ Use for: Dedicated hosts, non-migratable VMs

host-model
├─ Good performance (filtered features)
├─ Some migration compatibility
└─ Use for: Private cloud, controlled environments

custom (e.g., Skylake-Server)
├─ Good compatibility
├─ May miss some features
└─ Use for: Public cloud, wide migration

qemu64 / kvm64
├─ Maximum compatibility
├─ Lowest performance
└─ Use for: Legacy OS, maximum portability
```

**Optimal CPU Configuration**
```xml
<cpu mode='host-passthrough' check='none' migratable='off'>
  <!-- Expose host CPU topology -->
  <topology sockets='1' dies='1' cores='4' threads='1'/>

  <!-- Performance features -->
  <feature policy='require' name='pdpe1gb'/>      <!-- 1GB pages -->
  <feature policy='require' name='invtsc'/>        <!-- Invariant TSC -->
  <feature policy='require' name='tsc-deadline'/>  <!-- TSC deadline timer -->
  <feature policy='require' name='rdtscp'/>        <!-- Fast timestamp -->
  <feature policy='require' name='mpx'/>           <!-- Memory protection -->

  <!-- Disable unnecessary features for performance -->
  <feature policy='disable' name='hypervisor'/>    <!-- Hide hypervisor -->
  <feature policy='disable' name='smep'/>          <!-- If not needed -->

  <!-- Cache configuration -->
  <cache mode='passthrough'/>
</cpu>
```

### Advanced vCPU Pinning Strategies

**Topology-Aware Pinning**
```bash
# Analyze host topology
lscpu --extended
# Output shows: CPU NODE SOCKET CORE L1d:L1i:L2:L3

# Example output:
# CPU  NODE  SOCKET  CORE  L1d:L1i:L2:L3
# 0    0     0       0     0:0:0:0
# 1    0     0       1     1:1:1:0
# 2    0     0       2     2:2:2:0
# 3    0     0       3     3:3:3:0
# 4    1     1       4     4:4:4:1
# 5    1     1       5     5:5:5:1

# Pin VM to single L3 cache domain (CPUs 0-3 share L3 cache 0)
```

**Pinning Configuration**
```xml
<vcpu placement='static'>4</vcpu>

<cputune>
  <!-- Pin to CPUs sharing L3 cache -->
  <vcpupin vcpu='0' cpuset='0'/>
  <vcpupin vcpu='1' cpuset='1'/>
  <vcpupin vcpu='2' cpuset='2'/>
  <vcpupin vcpu='3' cpuset='3'/>

  <!-- Separate I/O threads -->
  <emulatorpin cpuset='8'/>
  <iothreadpin iothread='1' cpuset='9'/>
  <iothreadpin iothread='2' cpuset='10'/>
</cputune>

<numatune>
  <!-- Pin memory to same NUMA node -->
  <memory mode='strict' nodeset='0'/>
  <memnode cellid='0' mode='strict' nodeset='0'/>
</numatune>
```

**Dynamic vCPU Scaling with Performance Awareness**
```bash
#!/bin/bash
# intelligent-vcpu-scaler.sh

VM_NAME="$1"
TARGET_CPU_UTIL=70  # Target 70% CPU utilization

while true; do
  # Get VM CPU utilization
  VM_CPU=$(ssh $VM_NAME "mpstat 1 1 | grep Average | awk '{print 100 - \$NF}'")

  # Get current vCPUs
  CURRENT_VCPUS=$(virsh vcpucount $VM_NAME --live)

  if (( $(echo "$VM_CPU > 90" | bc -l) )); then
    # Scale up
    NEW_VCPUS=$((CURRENT_VCPUS + 1))
    virsh setvcpus $VM_NAME $NEW_VCPUS --live

    # Pin new vCPU to optimal pCPU
    NEXT_PCPU=$(find_optimal_pcpu $VM_NAME)
    virsh vcpupin $VM_NAME $((NEW_VCPUS - 1)) $NEXT_PCPU --live

  elif (( $(echo "$VM_CPU < 50" | bc -l) )) && [ $CURRENT_VCPUS -gt 2 ]; then
    # Scale down
    NEW_VCPUS=$((CURRENT_VCPUS - 1))
    virsh setvcpus $VM_NAME $NEW_VCPUS --live
  fi

  sleep 30
done
```

## Advanced Memory Optimization

### Huge Pages Optimization

**Huge Page Sizing Strategy**
```
Page Size Trade-offs:

4KB (default):
├─ Pros: Flexible, no waste
├─ Cons: High TLB miss rate, many page table entries
└─ Use for: General workloads, memory-constrained

2MB (huge pages):
├─ Pros: 512x fewer TLB entries, faster lookup
├─ Cons: Some memory waste, requires pre-allocation
└─ Use for: Most production VMs, databases

1GB (gigantic pages):
├─ Pros: 512x fewer TLB entries than 2MB
├─ Cons: Significant waste potential, must pre-allocate
└─ Use for: Large memory VMs (>64GB), HPC workloads
```

**Optimal Huge Pages Configuration**
```bash
# Calculate required huge pages
# VM memory: 32GB
# Huge page size: 2MB
# Pages needed: 32768 MB / 2 MB = 16384 pages

# Reserve 2MB huge pages
echo 16384 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# Or reserve 1GB huge pages (for 32GB VM)
echo 32 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages

# Verify allocation
cat /proc/meminfo | grep Huge

# Make persistent
cat >> /etc/sysctl.conf <<EOF
vm.nr_hugepages=16384
vm.hugetlb_shm_group=36  # kvm group ID
EOF

# Create hugepages mount
mkdir -p /dev/hugepages
mount -t hugetlbfs hugetlbfs /dev/hugepages
echo "hugetlbfs /dev/hugepages hugetlbfs defaults 0 0" >> /etc/fstab
```

**VM Configuration with Huge Pages**
```xml
<domain type='kvm'>
  <memory unit='GiB'>32</memory>
  <currentMemory unit='GiB'>32</currentMemory>

  <memoryBacking>
    <!-- Use 1GB huge pages -->
    <hugepages>
      <page size='1048576' unit='KiB' nodeset='0'/>
    </hugepages>

    <!-- Lock pages in RAM (prevent swapping) -->
    <locked/>

    <!-- Disable THP (we use static huge pages) -->
    <nosharepages/>

    <!-- Pre-allocate all memory -->
    <allocation mode='immediate'/>
  </memoryBacking>

  <numatune>
    <memory mode='strict' nodeset='0'/>
  </numatune>
</domain>
```

### NUMA Optimization

**NUMA Topology Analysis**
```bash
# Show NUMA topology
numactl --hardware
# Output:
# available: 2 nodes (0-1)
# node 0 cpus: 0 1 2 3 4 5 6 7
# node 0 size: 128GB
# node 0 free: 64GB
# node 1 cpus: 8 9 10 11 12 13 14 15
# node 1 size: 128GB
# node 1 free: 96GB
# node distances:
# node   0   1
#   0:  10  21    # Local access=10, remote=21 (2.1x slower)
#   1:  21  10

# Verify VM NUMA configuration
virsh numatune vm-name
```

**NUMA-Aware VM Configuration**
```xml
<domain type='kvm'>
  <vcpu placement='static'>8</vcpu>

  <!-- Define virtual NUMA topology matching physical -->
  <cpu>
    <numa>
      <cell id='0' cpus='0-3' memory='16' unit='GiB' memAccess='shared'/>
      <cell id='1' cpus='4-7' memory='16' unit='GiB' memAccess='shared'/>
    </numa>
  </cpu>

  <!-- Pin virtual NUMA to physical NUMA -->
  <numatune>
    <memory mode='strict' nodeset='0-1'/>
    <memnode cellid='0' mode='strict' nodeset='0'/>
    <memnode cellid='1' mode='strict' nodeset='1'/>
  </numatune>

  <!-- Pin vCPUs to corresponding NUMA node -->
  <cputune>
    <!-- vCPUs 0-3 on NUMA node 0 (pCPUs 0-3) -->
    <vcpupin vcpu='0' cpuset='0'/>
    <vcpupin vcpu='1' cpuset='1'/>
    <vcpupin vcpu='2' cpuset='2'/>
    <vcpupin vcpu='3' cpuset='3'/>

    <!-- vCPUs 4-7 on NUMA node 1 (pCPUs 8-11) -->
    <vcpupin vcpu='4' cpuset='8'/>
    <vcpupin vcpu='5' cpuset='9'/>
    <vcpupin vcpu='6' cpuset='10'/>
    <vcpupin vcpu='7' cpuset='11'/>
  </cputune>
</domain>
```

**NUMA Monitoring**
```bash
# Monitor NUMA memory allocation
numastat -c qemu

# Show per-node memory stats for VM
cat /proc/$(pgrep qemu)/numa_maps | grep dirty | \
  awk '{node[$1]++; mem[$1]+=$2} END {for (n in node) print n, node[n], mem[n]}'

# Identify remote NUMA access
perf stat -e node-load-misses,node-store-misses -p $(pgrep qemu) sleep 10
```

### Memory Ballooning and Overcommitment

**Intelligent Ballooning Strategy**
```xml
<domain type='kvm'>
  <memory unit='GiB'>32</memory>        <!-- Maximum -->
  <currentMemory unit='GiB'>24</currentMemory>  <!-- Current -->

  <memballoon model='virtio'>
    <!-- Enable statistics collection -->
    <stats period='10'/>

    <!-- Automatic deflation on memory pressure -->
    <autodeflate>on</autodeflate>
  </memballoon>
</domain>
```

**Dynamic Memory Management**
```bash
# Monitor balloon stats
virsh domstats vm-name --balloon

# Set current memory (balloon adjusts)
virsh setmem vm-name 20G --live

# View guest memory pressure
virsh dommemstat vm-name

# Automatic balloon adjustment based on host pressure
#!/bin/bash
# auto-balloon.sh

HOST_FREE_THRESHOLD=10  # GB
VM_NAME="my-vm"

while true; do
  # Get host free memory
  HOST_FREE=$(free -g | awk '/Mem:/ {print $4}')

  if [ $HOST_FREE -lt $HOST_FREE_THRESHOLD ]; then
    # Host under pressure, deflate VM balloon (reduce VM memory)
    CURRENT_MEM=$(virsh dommemstat $VM_NAME | grep actual | awk '{print $2/1024/1024}')
    NEW_MEM=$(echo "$CURRENT_MEM * 0.9" | bc)  # Reduce by 10%
    virsh setmem $VM_NAME ${NEW_MEM}G --live
    echo "Deflated $VM_NAME to ${NEW_MEM}G due to host pressure"
  fi

  sleep 30
done
```

## Advanced Network Optimization

### Multi-Queue virtio-net

**Multi-Queue Configuration**
```xml
<domain type='kvm'>
  <!-- Create dedicated I/O threads -->
  <iothreads>4</iothreads>

  <devices>
    <interface type='bridge'>
      <source bridge='br0'/>
      <model type='virtio'/>

      <!-- Enable multi-queue (match vCPU count) -->
      <driver name='vhost' queues='4' tx='timer'>
        <host tso4='on' tso6='on' ecn='on' ufo='on'/>
        <guest tso4='on' tso6='on' ecn='on' ufo='on'/>
      </driver>

      <!-- Assign to specific I/O thread -->
      <driver iothread='1'/>
    </interface>
  </devices>
</domain>
```

**Guest Configuration for Multi-Queue**
```bash
# In guest: Enable multi-queue for interface
ethtool -L eth0 combined 4

# Verify queues
ethtool -l eth0

# Configure RPS/RFS for queue affinity
#!/bin/bash
# setup-multiqueue.sh

IFACE="eth0"
QUEUES=4

# Set CPU affinity for each RX queue
for i in $(seq 0 $((QUEUES-1))); do
  CPU_MASK=$((1 << i))
  echo $CPU_MASK > /sys/class/net/$IFACE/queues/rx-$i/rps_cpus
done

# Enable RFS (Receive Flow Steering)
echo 32768 > /proc/sys/net/core/rps_sock_flow_entries
for i in $(seq 0 $((QUEUES-1))); do
  echo 8192 > /sys/class/net/$IFACE/queues/rx-$i/rps_flow_cnt
done

# Increase ring buffer size
ethtool -G $IFACE rx 4096 tx 4096
```

### vhost-user with DPDK

**vhost-user Architecture**
```
Guest (virtio-net)
      ↓ virtqueue
vhost-user (userspace process, e.g., OVS-DPDK)
      ↓ poll mode
Physical NIC (DPDK driver)
```

**vhost-user Configuration**
```xml
<domain type='kvm'>
  <memoryBacking>
    <!-- Required for vhost-user -->
    <hugepages>
      <page size='2048' unit='KiB'/>
    </hugepages>
    <access mode='shared'/>
  </memoryBacking>

  <devices>
    <interface type='vhostuser'>
      <source type='unix' path='/var/run/openvswitch/vhost-user1' mode='client'/>
      <model type='virtio'/>

      <!-- Multi-queue for performance -->
      <driver queues='4'>
        <host mrg_rxbuf='on'/>
      </driver>
    </interface>
  </devices>
</domain>
```

**OVS-DPDK Setup**
```bash
# Install OVS with DPDK
yum install openvswitch dpdk

# Configure huge pages (8GB)
echo 4096 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages

# Initialize OVS-DPDK
ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true
ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-socket-mem="4096,4096"
systemctl restart openvswitch

# Create DPDK bridge
ovs-vsctl add-br br0 -- set bridge br0 datapath_type=netdev

# Add physical port with DPDK
ovs-vsctl add-port br0 dpdk0 -- \
  set Interface dpdk0 type=dpdk options:dpdk-devargs=0000:01:00.0

# Add vhost-user port
ovs-vsctl add-port br0 vhost-user1 -- \
  set Interface vhost-user1 type=dpdkvhostuserclient \
  options:vhost-server-path=/var/run/openvswitch/vhost-user1

# Set PMD CPU affinity
ovs-vsctl set Open_vSwitch . other_config:pmd-cpu-mask=0x6  # CPUs 1,2
```

### SR-IOV for Maximum Performance

**SR-IOV Setup**
```bash
# Enable IOMMU in kernel
# Edit /etc/default/grub
GRUB_CMDLINE_LINUX="intel_iommu=on iommu=pt"
grub2-mkconfig -o /boot/grub2/grub.cfg
reboot

# Create virtual functions
echo 8 > /sys/class/net/ens2f0/device/sriov_numvfs

# Verify VFs created
lspci | grep "Virtual Function"

# Persist VF creation
cat > /etc/systemd/system/sriov-vfs.service <<EOF
[Unit]
Description=Create SR-IOV Virtual Functions
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c 'echo 8 > /sys/class/net/ens2f0/device/sriov_numvfs'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF

systemctl enable sriov-vfs
```

**VM Configuration with SR-IOV**
```xml
<domain type='kvm'>
  <devices>
    <!-- SR-IOV VF passthrough -->
    <interface type='hostdev' managed='yes'>
      <source>
        <address type='pci' domain='0x0000' bus='0x03' slot='0x10' function='0x0'/>
      </source>

      <!-- MAC address for VF -->
      <mac address='52:54:00:12:34:56'/>

      <!-- Trust VF for better performance -->
      <driver name='vfio'/>

      <!-- Boot protocol -->
      <boot order='1'/>
    </interface>
  </devices>
</domain>
```

**Advanced SR-IOV Tuning**
```bash
# Set VF trust mode (allows MAC/VLAN changes)
ip link set ens2f0 vf 0 trust on

# Set VF MAC address
ip link set ens2f0 vf 0 mac 52:54:00:12:34:56

# Set VF VLAN
ip link set ens2f0 vf 0 vlan 100

# Set VF rate limit (Mbps)
ip link set ens2f0 vf 0 max_tx_rate 10000

# Set VF spoof checking
ip link set ens2f0 vf 0 spoofchk off

# Set VF link state
ip link set ens2f0 vf 0 state auto

# Enable VF QoS
ip link set ens2f0 vf 0 qos 7  # Priority 7
```

## Advanced Storage Optimization

### I/O Threading and Native AIO

**Optimal Storage Configuration**
```xml
<domain type='kvm'>
  <!-- Create dedicated I/O threads -->
  <iothreads>4</iothreads>

  <devices>
    <!-- Optimal virtio-blk configuration -->
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'
              detect_zeroes='unmap' iothread='1' queues='4'/>
      <source dev='/dev/vg0/vm-disk'/>
      <target dev='vda' bus='virtio'/>

      <!-- I/O tuning -->
      <iotune>
        <total_iops_sec>50000</total_iops_sec>
        <read_iops_sec>30000</read_iops_sec>
        <write_iops_sec>20000</write_iops_sec>
      </iotune>
    </disk>

    <!-- NVMe passthrough for best performance -->
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native'/>
      <source dev='/dev/nvme0n1'/>
      <target dev='vdb' bus='virtio'/>
    </disk>
  </devices>
</domain>
```

**Cache Mode Selection**
```
cache='none'
├─ Best: Native AIO, O_DIRECT
├─ Pros: No double buffering, consistent performance
├─ Cons: No host cache benefit
└─ Use for: Production, SSD/NVMe, databases

cache='writethrough'
├─ Safe: Write to host cache + disk
├─ Pros: Read caching, safe writes
├─ Cons: Write latency
└─ Use for: General purpose, safety first

cache='writeback'
├─ Fast: Writes to host cache only
├─ Pros: Low write latency
├─ Cons: Data loss risk on host crash
└─ Use for: Non-critical, temporary data

cache='directsync'
├─ Safest: Bypass host cache, sync writes
├─ Pros: Maximum safety, no cache
├─ Cons: Highest latency
└─ Use for: Financial, critical data
```

### virtio-blk vs virtio-scsi

**Performance Comparison**
```
virtio-blk:
├─ Simpler, lower overhead
├─ Best for single disk VMs
├─ ~5-10% better throughput
├─ No SCSI features (no TRIM in old kernels)
└─ Recommended for most workloads

virtio-scsi:
├─ More features (SCSI commands, hot-plug)
├─ Better for multiple disks
├─ ~5-10% lower throughput than virtio-blk
├─ Supports TRIM, persistent reservations
└─ Recommended for complex storage setups
```

**virtio-scsi Configuration**
```xml
<domain type='kvm'>
  <devices>
    <!-- virtio-scsi controller -->
    <controller type='scsi' index='0' model='virtio-scsi'>
      <!-- Multi-queue support -->
      <driver queues='4' iothread='1'/>
    </controller>

    <!-- Disks attached to virtio-scsi -->
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'/>
      <source dev='/dev/vg0/vm-disk1'/>
      <target dev='sda' bus='scsi'/>
    </disk>

    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'/>
      <source dev='/dev/vg0/vm-disk2'/>
      <target dev='sdb' bus='scsi'/>
    </disk>
  </devices>
</domain>
```

### vhost-blk and vhost-user-blk

**vhost-blk Configuration (Kernel)**
```xml
<disk type='block' device='disk'>
  <driver name='qemu' type='raw' cache='none'>
    <!-- Use vhost-blk for kernel-space acceleration -->
    <vhost type='vhost-kernel'/>
  </driver>
  <source dev='/dev/vg0/vm-disk'/>
  <target dev='vda' bus='virtio'/>
</disk>
```

**vhost-user-blk with SPDK**
```bash
# Install SPDK
git clone https://github.com/spdk/spdk
cd spdk
./scripts/pkgdep.sh
./configure --with-vhost
make

# Setup huge pages
./scripts/setup.sh

# Start SPDK vhost target
./build/bin/vhost -S /var/tmp -m 0x3  # CPUs 0,1

# Create vhost-blk device
./scripts/rpc.py bdev_malloc_create 4096 512 -b Malloc0
./scripts/rpc.py vhost_create_blk_controller --cpumask 0x1 vhost.0 Malloc0
```

**VM Configuration with SPDK vhost-user-blk**
```xml
<domain type='kvm'>
  <memoryBacking>
    <hugepages/>
    <access mode='shared'/>
  </memoryBacking>

  <devices>
    <disk type='vhostuser' device='disk'>
      <source type='unix' path='/var/tmp/vhost.0'>
        <reconnect enabled='yes' timeout='10'/>
      </source>
      <target dev='vda' bus='virtio'/>
    </disk>
  </devices>
</domain>
```

## Advanced Device Passthrough

### PCI Passthrough Optimization

**VFIO Configuration**
```bash
# Enable IOMMU
# /etc/default/grub
GRUB_CMDLINE_LINUX="intel_iommu=on iommu=pt vfio_iommu_type1.allow_unsafe_interrupts=1"
grub2-mkconfig -o /boot/grub2/grub.cfg

# Find device
lspci -nn | grep -i nvidia
# Output: 01:00.0 VGA compatible controller [0300]: NVIDIA Corporation [10de:1b80]

# Bind to vfio-pci
echo "10de 1b80" > /sys/bus/pci/drivers/vfio-pci/new_id
echo "0000:01:00.0" > /sys/bus/pci/devices/0000:01:00.0/driver/unbind
echo "0000:01:00.0" > /sys/bus/pci/drivers/vfio-pci/bind

# Or use vfio-pci boot parameter
# /etc/modprobe.d/vfio.conf
options vfio-pci ids=10de:1b80
```

**VM Configuration with PCI Passthrough**
```xml
<domain type='kvm'>
  <features>
    <!-- Required for PCI passthrough -->
    <ioapic driver='kvm'/>
  </features>

  <devices>
    <!-- PCI device passthrough -->
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <source>
        <address domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
      </source>

      <!-- Guest address -->
      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
    </hostdev>
  </devices>
</domain>
```

### GPU Optimization

**Multi-GPU Passthrough**
```xml
<domain type='kvm'>
  <devices>
    <!-- GPU 1 -->
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <source>
        <address domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
      </source>
    </hostdev>

    <!-- GPU 1 Audio -->
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <source>
        <address domain='0x0000' bus='0x01' slot='0x00' function='0x1'/>
      </source>
    </hostdev>

    <!-- GPU 2 -->
    <hostdev mode='subsystem' type='pci' managed='yes'>
      <source>
        <address domain='0x0000' bus='0x02' slot='0x00' function='0x0'/>
      </source>
    </hostdev>
  </devices>
</domain>
```

## Performance Monitoring and Profiling

### Comprehensive Performance Monitoring

**VM Performance Dashboard Script**
```bash
#!/bin/bash
# vm-performance-monitor.sh

VM_NAME="$1"

while true; do
  clear
  echo "=== VM Performance Dashboard: $VM_NAME ==="
  echo ""

  # CPU metrics
  echo "--- CPU ---"
  virsh vcpuinfo $VM_NAME | grep -E 'CPU:|CPU time:|State:'

  # Steal time (from guest)
  echo ""
  STEAL=$(ssh $VM_NAME "mpstat 1 1 | grep Average | awk '{print \$NF}'")
  echo "CPU Steal: ${STEAL}%"

  # Memory metrics
  echo ""
  echo "--- Memory ---"
  virsh domstats $VM_NAME --balloon

  # I/O metrics
  echo ""
  echo "--- I/O ---"
  virsh domblklist $VM_NAME --details
  virsh domblkstat $VM_NAME vda

  # Network metrics
  echo ""
  echo "--- Network ---"
  virsh domiflist $VM_NAME
  virsh domifstat $VM_NAME vnet0

  sleep 5
done
```

**Latency Profiling**
```bash
# Profile VM exit reasons
perf kvm stat record -p $(pgrep qemu) -- sleep 10
perf kvm stat report

# Profile I/O latency
bpftrace -e '
kprobe:blk_account_io_start {
  @start[arg0] = nsecs;
}

kprobe:blk_account_io_done /@start[arg0]/ {
  $latency = nsecs - @start[arg0];
  @io_latency = hist($latency / 1000);  # microseconds
  delete(@start[arg0]);
}
' -- sleep 30
```

## References

### Tuning Guides
- `/references/kvm-tuning-comprehensive.md` - Complete KVM tuning guide
- `/references/qemu-performance-optimization.md` - QEMU optimization
- `/references/virtio-device-tuning.md` - virtio device optimization
- `/references/vhost-optimization.md` - vhost tuning guide
- `/references/dpdk-vhost-user-guide.md` - DPDK vhost-user setup
- `/references/spdk-integration.md` - SPDK integration guide

### Hardware Acceleration
- `/references/sriov-advanced-config.md` - Advanced SR-IOV
- `/references/vdpa-setup-guide.md` - vDPA configuration
- `/references/gpu-passthrough-optimization.md` - GPU passthrough
- `/references/nvme-passthrough.md` - NVMe passthrough
- `/references/pci-passthrough-best-practices.md` - PCI passthrough

### Memory Optimization
- `/references/hugepages-sizing-guide.md` - Huge pages sizing
- `/references/numa-optimization-advanced.md` - Advanced NUMA
- `/references/memory-ballooning-strategies.md` - Ballooning strategies
- `/references/ksm-tuning.md` - KSM optimization

### Network Performance
- `/references/multiqueue-virtio-net.md` - Multi-queue setup
- `/references/ovs-dpdk-tuning.md` - OVS-DPDK optimization
- `/references/network-latency-optimization.md` - Network latency

### Storage Performance
- `/references/virtio-blk-scsi-comparison.md` - Block device comparison
- `/references/io-threading-guide.md` - I/O threading
- `/references/storage-cache-modes.md` - Cache mode selection
- `/references/nvme-optimization.md` - NVMe optimization

### Tools & Scripts
- `/assets/vm-performance-monitor.sh` - Monitoring script
- `/assets/latency-profiler.sh` - Latency profiling
- `/assets/vcpu-optimizer.py` - vCPU optimization tool
- `/assets/numa-topology-analyzer.py` - NUMA analysis
- `/assets/grafana-vm-performance-dashboard.json` - Grafana dashboard
