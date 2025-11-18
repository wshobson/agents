---
name: cpu-steal-time-optimization
description: World-class expert guide to CPU steal time diagnosis, mitigation, and elimination. Covers hypervisor overcommitment, noisy neighbor detection, CPU pinning strategies, scheduler optimization, cloud platform tuning, and real-time monitoring. Use when experiencing CPU steal time issues, diagnosing VM performance degradation, optimizing cloud workload placement, or troubleshooting latency-sensitive applications in virtualized environments.
---

# CPU Steal Time Optimization

## When to Use This Skill

- Diagnosing unexplained application latency in VMs
- Experiencing high CPU steal time (>5%) in production
- Optimizing VM performance in overcommitted environments
- Detecting and mitigating noisy neighbor effects
- Tuning latency-sensitive applications in cloud
- Planning VM placement strategies for predictable performance
- Troubleshooting intermittent performance issues in VMs
- Configuring dedicated CPU resources for critical workloads

## Core Concepts

### What is CPU Steal Time?

**Definition**
- Time that a virtual CPU waits for a physical CPU while the hypervisor services another virtual CPU
- Measured as percentage of total CPU time
- High steal time = VM is starved for CPU resources

**How it Appears**
```bash
# top output showing steal time
%Cpu(s):  2.3 us,  1.2 sy,  0.0 ni, 89.5 id,  0.0 wa,  0.0 hi,  0.5 si, 6.5 st
                                                                              ^^
                                                                         steal time

# mpstat showing per-CPU steal
Linux 5.15.0 (host)     11/18/2025  _x86_64_

11:30:00 AM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
11:30:01 AM    0    5.00    0.00    2.00    0.00    0.00    0.00   12.00    0.00    0.00   81.00
11:30:01 AM    1    3.00    0.00    1.00    0.00    0.00    0.00   15.00    0.00    0.00   81.00
```

**Acceptable Levels**
- **0-2%**: Excellent, negligible impact
- **2-5%**: Good, may affect latency-sensitive apps
- **5-10%**: Warning, noticeable performance degradation
- **10-20%**: Critical, significant performance issues
- **>20%**: Severe, VM severely starved for CPU

### Root Causes of CPU Steal Time

**1. CPU Overcommitment**
```
Physical Host: 8 physical cores
├─ VM1: 4 vCPUs (running CPU-intensive workload)
├─ VM2: 4 vCPUs (running CPU-intensive workload)
├─ VM3: 4 vCPUs (running CPU-intensive workload)
└─ VM4: 4 vCPUs (idle)
Total: 16 vCPUs on 8 physical cores = 2:1 overcommit ratio
```
When VM1, VM2, VM3 compete for CPU, they experience steal time.

**2. Noisy Neighbors**
- Other VMs on same host consuming disproportionate CPU
- Bursty workloads causing periodic contention
- Batch jobs running at unexpected times

**3. Poor vCPU to pCPU Mapping**
```
# Bad: vCPU spread across NUMA nodes
VM with 4 vCPUs mapped to:
pCPU 0 (NUMA node 0)
pCPU 8 (NUMA node 1)
pCPU 4 (NUMA node 0)
pCPU 12 (NUMA node 1)
Result: Cross-NUMA scheduling overhead + steal time

# Good: vCPU aligned to single NUMA node
VM with 4 vCPUs mapped to:
pCPU 0-3 (all on NUMA node 0)
Result: Local memory access + reduced steal time
```

**4. Hypervisor Scheduling Inefficiencies**
- CFS scheduler delays in KVM
- Scheduling quantum too small or too large
- Priority inversions between VMs
- Insufficient time for vCPU to complete work

**5. SMT (Hyper-Threading) Contention**
```
Physical Core 0:
├─ Thread 0 (pCPU 0) ← VM1 vCPU
└─ Thread 1 (pCPU 8) ← VM2 vCPU
Result: Both VMs share execution units, causing steal time
```

## Diagnostic Techniques

### Monitoring CPU Steal Time

**Real-Time Monitoring**
```bash
# Monitor steal time with top
top
# Press '1' to see per-CPU stats
# Look at '%st' column

# Continuous monitoring with vmstat
vmstat 1
# Look at 'st' column under CPU

# Per-CPU steal with mpstat
mpstat -P ALL 1

# Detailed stats with sar
sar -P ALL 1
```

**Historical Analysis**
```bash
# View steal time history (requires sysstat)
sar -u ALL -f /var/log/sa/sa18  # View specific day

# Plot steal time over time
sar -u ALL | grep -E 'Average|steal' | awk '{print $NF}'

# Export to CSV for analysis
sar -u ALL -s 00:00:00 -e 23:59:59 | grep -v '^$' > steal_time.csv
```

**Application-Level Impact**
```bash
# Measure latency during high steal
# Terminal 1: Monitor steal
watch -n 1 'mpstat 1 1 | grep Average'

# Terminal 2: Measure application latency
while true; do
  time curl -s http://localhost:8080/api > /dev/null
  sleep 1
done

# Correlate steal time spikes with latency increases
```

### Hypervisor-Side Diagnostics

**KVM/libvirt Analysis**
```bash
# View VM CPU statistics
virsh vcpuinfo vm-name
# Look at CPU time vs available time ratio

# Monitor vCPU scheduling
virsh vcpupin vm-name --live

# Check vCPU thread states
ps -eLo pid,tid,class,rtprio,ni,pri,psr,pcpu,stat,comm | grep qemu

# Measure vCPU wait time
perf record -e 'kvm:*' -a -g -- sleep 60
perf script | flamegraph.pl > kvm_flamegraph.svg
```

**vCPU Scheduling Latency**
```bash
# Use bpftrace to measure vCPU scheduling delays
bpftrace -e '
kprobe:kvm_vcpu_block {
  @start[tid] = nsecs;
}

kretprobe:kvm_vcpu_block /@start[tid]/ {
  $latency_us = (nsecs - @start[tid]) / 1000;
  @latency_hist = hist($latency_us);
  delete(@start[tid]);
}

interval:s:10 {
  print(@latency_hist);
  clear(@latency_hist);
}
'
```

**Noisy Neighbor Detection**
```bash
# On hypervisor: Identify VMs consuming most CPU
virsh list --all | awk '{print $2}' | while read vm; do
  [ -z "$vm" ] && continue
  echo -n "$vm: "
  virsh domstats $vm | grep 'cpu.time' | awk '{print $2}'
done | sort -t: -k2 -rn

# Correlate with VM names
for vm in $(virsh list --name); do
  echo "=== $vm ==="
  virsh vcpuinfo $vm | grep 'CPU time'
done
```

### Cloud Platform Diagnostics

**AWS (EC2)**
```bash
# CloudWatch metric for CPU steal
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUCreditUsage \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2025-11-18T00:00:00Z \
  --end-time 2025-11-18T23:59:59Z \
  --period 300 \
  --statistics Average

# T-series instances: Monitor CPU credits
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUCreditBalance \
  --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
  --start-time 2025-11-18T00:00:00Z \
  --end-time 2025-11-18T23:59:59Z \
  --period 300 \
  --statistics Average

# Recommended: Use dedicated instances (c5, m5, r5 with dedicated option)
# or bare metal instances (*.metal) to eliminate steal time
```

**GCP (Compute Engine)**
```bash
# Stackdriver monitoring for CPU steal
gcloud compute instances describe INSTANCE_NAME \
  --format="get(metadata.items.cpu-steal-time)"

# Use sole-tenant nodes for predictable performance
gcloud compute sole-tenancy node-groups create GROUP_NAME \
  --node-template=TEMPLATE_NAME \
  --target-size=1

# Recommended: N2 or C2 machine types with sole tenancy
```

**Azure (Virtual Machines)**
```bash
# Azure Monitor metrics
az monitor metrics list \
  --resource /subscriptions/{subscription-id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{vm-name} \
  --metric "Percentage CPU" \
  --start-time 2025-11-18T00:00:00Z \
  --end-time 2025-11-18T23:59:59Z

# Note: Azure doesn't expose steal time directly
# Recommended: Use dedicated host or isolated VMs
az vm host create --host-group myHostGroup --name myHost --sku DSv3-Type1 -g myResourceGroup
```

## Mitigation Strategies

### 1. CPU Pinning (vCPU to pCPU Affinity)

**Basic CPU Pinning**
```xml
<!-- Pin 4 vCPUs to physical CPUs 0-3 -->
<vcpu placement='static'>4</vcpu>
<cputune>
  <vcpupin vcpu='0' cpuset='0'/>
  <vcpupin vcpu='1' cpuset='1'/>
  <vcpupin vcpu='2' cpuset='2'/>
  <vcpupin vcpu='3' cpuset='3'/>
</cputune>
```

**NUMA-Aware Pinning**
```xml
<!-- Pin vCPUs to same NUMA node for memory locality -->
<vcpu placement='static'>4</vcpu>
<cputune>
  <!-- All vCPUs on NUMA node 0 (assume CPUs 0-7 are node 0) -->
  <vcpupin vcpu='0' cpuset='0'/>
  <vcpupin vcpu='1' cpuset='1'/>
  <vcpupin vcpu='2' cpuset='2'/>
  <vcpupin vcpu='3' cpuset='3'/>
</cputune>
<numatune>
  <memory mode='strict' nodeset='0'/>
</numatune>
```

**SMT-Aware Pinning (Avoid Sibling Threads)**
```bash
# Identify SMT siblings
cat /sys/devices/system/cpu/cpu0/topology/thread_siblings_list
# Output: 0,8  (CPU 0 and 8 share physical core)

# Pin vCPUs to avoid SMT siblings
# Option 1: Pin to physical cores only (0-7), avoid hyperthreads (8-15)
<cputune>
  <vcpupin vcpu='0' cpuset='0'/>
  <vcpupin vcpu='1' cpuset='1'/>
  <vcpupin vcpu='2' cpuset='2'/>
  <vcpupin vcpu='3' cpuset='3'/>
</cputune>

# Option 2: Disable SMT on host
echo off > /sys/devices/system/cpu/smt/control
```

**Emulator Thread Pinning**
```xml
<!-- Pin QEMU emulator threads to separate CPUs -->
<cputune>
  <!-- Guest vCPUs -->
  <vcpupin vcpu='0' cpuset='1'/>
  <vcpupin vcpu='1' cpuset='2'/>
  <vcpupin vcpu='2' cpuset='3'/>
  <vcpupin vcpu='3' cpuset='4'/>

  <!-- QEMU emulator threads (I/O, device emulation) -->
  <emulatorpin cpuset='0,5'/>
</cputune>
```

**Dynamic Pinning with virsh**
```bash
# Pin vCPU 0 to physical CPU 2
virsh vcpupin vm-name 0 2 --live

# Verify pinning
virsh vcpuinfo vm-name

# Pin multiple vCPUs at once
virsh vcpupin vm-name 0 0 --live
virsh vcpupin vm-name 1 1 --live
virsh vcpupin vm-name 2 2 --live
virsh vcpupin vm-name 3 3 --live
```

### 2. CPU Isolation on Host

**Isolate CPUs from Kernel Scheduler**
```bash
# Edit /etc/default/grub
GRUB_CMDLINE_LINUX="isolcpus=1-7 nohz_full=1-7 rcu_nocbs=1-7"

# Update grub
grub2-mkconfig -o /boot/grub2/grub.cfg

# Reboot
reboot

# Verify isolation
cat /sys/devices/system/cpu/isolated
# Output: 1-7
```

**Disable IRQ Balancing on Isolated CPUs**
```bash
# Configure irqbalance to avoid isolated CPUs
echo "IRQBALANCE_BANNED_CPUS=fe" > /etc/sysconfig/irqbalance
# fe = binary 11111110 = CPUs 1-7 banned

# Restart irqbalance
systemctl restart irqbalance

# Manually set IRQ affinity
echo "01" > /proc/irq/30/smp_affinity  # Pin IRQ 30 to CPU 0
```

**Taskset for Host Processes**
```bash
# Move all movable processes to CPU 0
for pid in $(ps -eLo pid | grep -v PID); do
  taskset -apc 0 $pid 2>/dev/null
done

# Verify processes on isolated CPUs
ps -eLo psr,pid,comm | awk '$1 > 0' | grep -v qemu
# Should only show QEMU/KVM threads
```

### 3. Scheduler Tuning

**CFS Scheduler Parameters**
```bash
# Increase scheduling latency for less preemption
sysctl kernel.sched_latency_ns=24000000  # 24ms (default: 6ms)

# Increase minimum granularity
sysctl kernel.sched_min_granularity_ns=10000000  # 10ms (default: 3ms)

# Reduce wakeup granularity for better responsiveness
sysctl kernel.sched_wakeup_granularity_ns=4000000  # 4ms (default: 4ms)

# Disable automatic NUMA balancing to reduce overhead
sysctl kernel.numa_balancing=0

# Persist settings
cat >> /etc/sysctl.conf <<EOF
kernel.sched_latency_ns=24000000
kernel.sched_min_granularity_ns=10000000
kernel.sched_wakeup_granularity_ns=4000000
kernel.numa_balancing=0
EOF
```

**Real-Time Priority for vCPU Threads**
```bash
# Identify QEMU vCPU threads
ps -eLo pid,tid,comm | grep qemu

# Set real-time priority (SCHED_FIFO) for vCPU threads
# Example: vCPU thread TID 12345
chrt -f -p 50 12345

# Script to set RT priority for all vCPU threads
for tid in $(ps -eLo tid,comm | grep 'CPU.*KVM' | awk '{print $1}'); do
  chrt -f -p 50 $tid
done
```

**libvirt Scheduler Configuration**
```xml
<domain type='kvm'>
  <cputune>
    <!-- Real-time scheduler for vCPUs -->
    <vcpusched vcpus='0-3' scheduler='fifo' priority='50'/>

    <!-- Emulator threads at lower priority -->
    <emulatorsched scheduler='fifo' priority='40'/>

    <!-- I/O threads at lower priority -->
    <iothreadsched iothreads='0-1' scheduler='fifo' priority='30'/>
  </cputune>
</domain>
```

### 4. Resource Reservation and Quotas

**cgroups CPU Quota**
```bash
# Create cgroup for VM
cgcreate -g cpu:/vms/vm-critical

# Set CPU quota: 400% (4 full CPUs)
echo 400000 > /sys/fs/cgroup/cpu/vms/vm-critical/cpu.cfs_quota_us
echo 100000 > /sys/fs/cgroup/cpu/vms/vm-critical/cpu.cfs_period_us

# Assign QEMU process to cgroup
echo $QEMU_PID > /sys/fs/cgroup/cpu/vms/vm-critical/tasks

# Verify
cat /sys/fs/cgroup/cpu/vms/vm-critical/cpu.stat
```

**CPU Shares (Relative Priority)**
```bash
# High-priority VM gets 2048 shares
echo 2048 > /sys/fs/cgroup/cpu/vms/vm-critical/cpu.shares

# Low-priority VM gets 512 shares
echo 512 > /sys/fs/cgroup/cpu/vms/vm-batch/cpu.shares

# When CPUs are contended, vm-critical gets 4x more CPU time
```

**libvirt Resource Limits**
```xml
<domain type='kvm'>
  <cputune>
    <!-- Reserve 50% of CPU bandwidth for this VM -->
    <period>100000</period>        <!-- 100ms period -->
    <quota>200000</quota>          <!-- 200ms quota = 2 vCPUs worth -->

    <!-- Global shares for scheduling priority -->
    <shares>2048</shares>
  </cputune>
</domain>
```

### 5. Workload-Specific Optimizations

**Latency-Sensitive Workloads**
```xml
<domain type='kvm'>
  <!-- CPU configuration -->
  <vcpu placement='static'>4</vcpu>
  <cpu mode='host-passthrough' check='none'>
    <topology sockets='1' cores='4' threads='1'/>
    <feature policy='require' name='tsc-deadline'/>
    <feature policy='require' name='invtsc'/>
  </cpu>

  <!-- Strict CPU pinning -->
  <cputune>
    <vcpupin vcpu='0' cpuset='1'/>
    <vcpupin vcpu='1' cpuset='2'/>
    <vcpupin vcpu='2' cpuset='3'/>
    <vcpupin vcpu='3' cpuset='4'/>
    <emulatorpin cpuset='0,5'/>

    <!-- Real-time scheduling -->
    <vcpusched vcpus='0-3' scheduler='fifo' priority='80'/>
  </cputune>

  <!-- Memory pinning with huge pages -->
  <memoryBacking>
    <hugepages>
      <page size='1048576' unit='KiB' nodeset='0'/>
    </hugepages>
    <locked/>
  </memoryBacking>

  <numatune>
    <memory mode='strict' nodeset='0'/>
  </numatune>
</domain>
```

**Host Configuration for Latency-Sensitive VMs**
```bash
# 1. CPU isolation
echo "isolcpus=1-4 nohz_full=1-4 rcu_nocbs=1-4" >> /etc/default/grub

# 2. Disable frequency scaling
for cpu in /sys/devices/system/cpu/cpu[1-4]; do
  echo performance > $cpu/cpufreq/scaling_governor
done

# 3. Disable C-states (prevent CPU from sleeping)
for cpu in /sys/devices/system/cpu/cpu[1-4]; do
  for state in $cpu/cpuidle/state*/disable; do
    echo 1 > $state
  done
done

# 4. Disable transparent huge pages (for predictability)
echo never > /sys/kernel/mm/transparent_hugepage/enabled

# 5. Set TSC clocksource
echo tsc > /sys/devices/system/clocksource/clocksource0/current_clocksource
```

**Batch/Throughput Workloads**
```xml
<domain type='kvm'>
  <!-- Allow CPU overcommitment -->
  <vcpu placement='static'>8</vcpu>
  <cpu mode='host-model'/>

  <cputune>
    <!-- No strict pinning, allow flexible scheduling -->
    <!-- Lower CPU shares -->
    <shares>512</shares>
  </cputune>

  <!-- Use balloon driver for dynamic memory -->
  <memballoon model='virtio'>
    <stats period='10'/>
  </memballoon>
</domain>
```

### 6. Cloud Platform Solutions

**AWS**
```bash
# Use dedicated instances (no CPU overcommit)
aws ec2 run-instances \
  --instance-type c5.2xlarge \
  --tenancy dedicated \
  --image-id ami-12345678

# Use bare metal instances (no hypervisor)
aws ec2 run-instances \
  --instance-type c5.metal \
  --image-id ami-12345678

# Use dedicated hosts (full control)
aws ec2 allocate-hosts \
  --instance-type c5.2xlarge \
  --quantity 1 \
  --availability-zone us-east-1a

aws ec2 run-instances \
  --instance-type c5.2xlarge \
  --placement "Tenancy=host,HostId=h-0123456789abcdef0" \
  --image-id ami-12345678

# For T-series: Use unlimited mode
aws ec2 modify-instance-credit-specification \
  --instance-credit-specification "InstanceId=i-1234567890abcdef0,CpuCredits=unlimited"
```

**GCP**
```bash
# Use sole-tenant nodes
gcloud compute instances create INSTANCE_NAME \
  --machine-type n2-standard-4 \
  --node NODE_NAME \
  --node-group NODE_GROUP_NAME

# Create node template with specific CPU platform
gcloud compute sole-tenancy node-templates create TEMPLATE_NAME \
  --node-type n2-node-96-624 \
  --cpu-overcommit-type none

# Use C2 machine type (compute-optimized)
gcloud compute instances create INSTANCE_NAME \
  --machine-type c2-standard-16 \
  --min-cpu-platform "Intel Cascade Lake"
```

**Azure**
```bash
# Use dedicated hosts
az vm host create \
  --host-group myHostGroup \
  --name myHost \
  --sku DSv3-Type1 \
  --resource-group myResourceGroup

az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --host myHost \
  --image UbuntuLTS \
  --size Standard_D4s_v3

# Use isolated VM sizes (no CPU overcommit)
az vm create \
  --resource-group myResourceGroup \
  --name myVM \
  --image UbuntuLTS \
  --size Standard_E64is_v3  # Isolated SKU
```

## Advanced Techniques

### Real-Time KVM Configuration

**Install RT Kernel**
```bash
# Ubuntu/Debian
apt-get install linux-image-rt-amd64

# RHEL/CentOS
yum install kernel-rt

# Reboot into RT kernel
reboot

# Verify RT kernel
uname -a | grep PREEMPT_RT
```

**RT Throttling Configuration**
```bash
# Disable RT throttling (allows 100% CPU for RT tasks)
sysctl kernel.sched_rt_runtime_us=-1

# Or increase RT budget
sysctl kernel.sched_rt_period_us=1000000   # 1 second
sysctl kernel.sched_rt_runtime_us=950000   # 95% of period

# Persist
echo "kernel.sched_rt_runtime_us=-1" >> /etc/sysctl.conf
```

**Tuned Profile for Low Latency**
```bash
# Install tuned
yum install tuned

# Use realtime profile
tuned-adm profile realtime

# Or create custom profile
cat > /etc/tuned/vm-lowlatency/tuned.conf <<EOF
[main]
summary=Low latency tuning for VMs
include=realtime

[cpu]
force_latency=1
governor=performance
energy_perf_bias=performance

[sysctl]
kernel.sched_min_granularity_ns=10000000
kernel.sched_wakeup_granularity_ns=15000000
vm.stat_interval=120
kernel.numa_balancing=0
EOF

tuned-adm profile vm-lowlatency
```

### vCPU Hotplug for Dynamic Scaling

**Enable vCPU Hotplug**
```xml
<domain type='kvm'>
  <vcpu placement='static' current='4'>8</vcpu>  <!-- 4 active, 8 max -->

  <cpu>
    <topology sockets='1' cores='8' threads='1'/>
  </cpu>
</domain>
```

**Hotplug vCPUs at Runtime**
```bash
# Add vCPU
virsh setvcpus vm-name 6 --live

# Monitor steal time after adding vCPUs
watch -n 1 'ssh vm-ip "mpstat 1 1 | grep Average"'

# Remove vCPU (if needed)
virsh setvcpus vm-name 4 --live
```

**Automatic Scaling Based on Steal Time**
```bash
#!/bin/bash
# auto-scale-vcpu.sh - Scale vCPUs based on steal time

VM_NAME="my-vm"
STEAL_THRESHOLD=5  # 5%
MAX_VCPUS=8
MIN_VCPUS=2

while true; do
  # Get current steal time from VM
  STEAL=$(ssh $VM_NAME "mpstat 1 1 | grep Average | awk '{print \$NF}'")
  CURRENT_VCPUS=$(virsh vcpucount $VM_NAME --live)

  if (( $(echo "$STEAL > $STEAL_THRESHOLD" | bc -l) )); then
    # High steal, try to add vCPUs
    if [ $CURRENT_VCPUS -lt $MAX_VCPUS ]; then
      NEW_VCPUS=$((CURRENT_VCPUS + 1))
      virsh setvcpus $VM_NAME $NEW_VCPUS --live
      echo "Increased vCPUs to $NEW_VCPUS due to high steal ($STEAL%)"
    fi
  fi

  sleep 60
done
```

### Performance Monitoring and Alerting

**Comprehensive Monitoring Script**
```bash
#!/bin/bash
# monitor-steal-time.sh

VM_NAME="$1"
ALERT_THRESHOLD=10  # Alert if steal > 10%
LOG_FILE="/var/log/steal-time-monitor.log"

while true; do
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

  # Get steal time
  STEAL=$(ssh $VM_NAME "mpstat 1 1 | grep Average | awk '{print \$NF}'")

  # Get vCPU info
  VCPU_INFO=$(virsh vcpuinfo $VM_NAME | grep '^CPU time:' | awk '{print $3}')

  # Get CPU pinning
  PINNING=$(virsh vcpupin $VM_NAME | grep -v 'VCPU')

  # Log data
  echo "$TIMESTAMP | Steal: ${STEAL}% | vCPU time: $VCPU_INFO" >> $LOG_FILE

  # Alert if high steal
  if (( $(echo "$STEAL > $ALERT_THRESHOLD" | bc -l) )); then
    echo "$TIMESTAMP | ALERT: High steal time ${STEAL}% on $VM_NAME" | tee -a $LOG_FILE

    # Send notification (example with mail)
    echo "High CPU steal time detected: ${STEAL}% on $VM_NAME" | \
      mail -s "CPU Steal Alert: $VM_NAME" admin@example.com
  fi

  sleep 60
done
```

**Prometheus Exporter for Steal Time**
```bash
# Install node_exporter in VM
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.6.1.linux-amd64.tar.gz
cd node_exporter-1.6.1.linux-amd64
./node_exporter &

# Query steal time metric
curl http://localhost:9100/metrics | grep node_cpu_seconds_total | grep steal

# Prometheus query for steal percentage
rate(node_cpu_seconds_total{mode="steal"}[5m]) * 100

# Alert rule in Prometheus
groups:
- name: cpu_steal_alerts
  rules:
  - alert: HighCPUSteal
    expr: rate(node_cpu_seconds_total{mode="steal"}[5m]) * 100 > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU steal time on {{ $labels.instance }}"
      description: "CPU steal time is {{ $value }}% on {{ $labels.instance }}"
```

## Best Practices

### Design Guidelines

**1. Right-Size VMs**
- Don't over-provision vCPUs
- Rule of thumb: 1 vCPU per application thread + 1 for OS
- Example: 4-thread application → 6 vCPUs maximum

**2. Match Workload to VM Type**
```
Latency-sensitive (databases, real-time):
├─ Dedicated instances
├─ CPU pinning
├─ Real-time scheduling
└─ No overcommitment

Throughput-focused (web servers, APIs):
├─ Shared instances OK
├─ Moderate overcommit (1.5:1)
├─ Standard scheduling
└─ Monitor steal time

Batch/background:
├─ Shared instances
├─ High overcommit (2:1 or more)
├─ Lower priority
└─ Steal time acceptable
```

**3. Plan for Peak Load**
- Size for peak + 20% headroom
- Use autoscaling for variable workloads
- Reserve capacity for critical VMs

**4. Implement Monitoring from Day 1**
- Always monitor CPU steal time
- Set alerts at 5% and 10% thresholds
- Correlate with application performance

### Troubleshooting Checklist

```
[ ] Step 1: Confirm steal time is the issue
    - Check mpstat, top, sar for steal time
    - Verify steal time > 5%
    - Rule out other bottlenecks (I/O, memory, network)

[ ] Step 2: Identify the source
    - Check hypervisor CPU utilization
    - Identify noisy neighbors (other VMs)
    - Verify CPU overcommit ratio
    - Check for SMT contention

[ ] Step 3: Quick wins
    - Enable CPU pinning
    - Isolate CPUs on host
    - Increase vCPU count (if under-provisioned)
    - Migrate to less loaded host

[ ] Step 4: Deep optimization
    - Tune scheduler parameters
    - Configure real-time priority
    - Implement NUMA pinning
    - Consider dedicated hardware

[ ] Step 5: Long-term solution
    - Migrate to dedicated instances
    - Use bare metal for critical workloads
    - Implement capacity planning
    - Set up continuous monitoring
```

## References

### Documentation
- `/references/cpu-steal-diagnosis.md` - Detailed diagnostic guide
- `/references/kvm-cpu-scheduling.md` - KVM scheduler internals
- `/references/cfs-tuning-guide.md` - CFS scheduler tuning
- `/references/numa-optimization.md` - NUMA optimization techniques
- `/references/realtime-kvm-setup.md` - Real-time KVM configuration

### Tools & Scripts
- `/assets/steal-time-monitor.sh` - Monitoring script
- `/assets/vcpu-auto-scaler.sh` - Auto-scaling script
- `/assets/prometheus-steal-exporter.yaml` - Prometheus configuration
- `/assets/grafana-steal-dashboard.json` - Grafana dashboard
- `/assets/cpu-pinning-generator.py` - CPU pinning configuration generator

### Cloud Provider Guides
- `/references/aws-dedicated-instances.md` - AWS dedicated instance guide
- `/references/gcp-sole-tenant-nodes.md` - GCP sole-tenant setup
- `/references/azure-dedicated-hosts.md` - Azure dedicated host guide
- `/references/cloud-instance-selection.md` - Cloud instance selection guide

### Performance Analysis
- `/references/perf-vcpu-analysis.md` - perf for vCPU analysis
- `/references/bpftrace-kvm-scripts.md` - BPF tracing for KVM
- `/references/steal-time-case-studies.md` - Real-world case studies
- `/assets/benchmarking-steal-impact.md` - Benchmark methodology
