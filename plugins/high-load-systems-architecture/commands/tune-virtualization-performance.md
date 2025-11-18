---
name: tune-virtualization-performance
description: Comprehensive virtualization performance analysis and optimization. Evaluates CPU, memory, network, and storage configurations, benchmarks current performance, and generates detailed tuning recommendations with implementation guides. Covers KVM/QEMU optimization, device passthrough, vhost tuning, and hardware acceleration. Saves detailed optimization plan to markdown file.
---

# Tune Virtualization Performance

This command performs comprehensive virtualization performance analysis and generates an expert optimization plan with specific tuning recommendations.

## What This Command Does

1. **Performance Baseline Assessment**
   - Benchmarks CPU performance (sysbench, stress-ng)
   - Measures memory latency and throughput
   - Tests network throughput (iperf3, netperf)
   - Evaluates storage IOPS and bandwidth (fio)
   - Identifies bottlenecks and overhead sources

2. **Configuration Analysis**
   - Evaluates vCPU topology and pinning strategy
   - Analyzes memory configuration (huge pages, NUMA)
   - Reviews network device configuration (virtio-net, SR-IOV)
   - Examines storage backend (virtio-blk, virtio-scsi, passthrough)
   - Assesses I/O threading and queue configuration

3. **Hardware Acceleration Assessment**
   - Evaluates SR-IOV capability and configuration
   - Analyzes vDPA device support
   - Reviews GPU passthrough options
   - Assesses vhost-user/vhost-net setup
   - Identifies optimization opportunities

4. **Generates Optimization Plan**
   - Prioritized tuning recommendations
   - Expected performance improvements
   - Implementation guides with scripts
   - Risk assessment for each change
   - Rollback procedures
   - Saves to `virtualization-performance-tuning-YYYY-MM-DD-HHMMSS.md`

## Usage

Simply invoke this command and provide:
- Target VM name or hostname
- Workload type (latency-sensitive/throughput/balanced/batch)
- Performance requirements (target latency, throughput, IOPS)
- Current performance issues (if any)

## Example Interaction

**You:** Tune virtualization performance for database-primary-01 (latency-sensitive workload, target <1ms latency)

**Assistant:** I'll perform comprehensive virtualization performance analysis for database-primary-01.

*[Runs benchmarks, analyzes configuration, identifies optimizations]*

**Report Generated:** `virtualization-performance-tuning-2025-11-18-143530.md`

**Performance Baseline:**
- CPU overhead: 12% (can be reduced to <5%)
- Memory latency: 180ns (can be reduced to 90ns)
- Network throughput: 4.2 Gbps (can be increased to 9.5 Gbps)
- Storage IOPS: 25K (can be increased to 80K)

**Optimization Potential:** 3.5x performance improvement

**Top Recommendations:**
1. Enable huge pages → +45% memory performance
2. Implement CPU pinning → +30% CPU performance
3. Configure SR-IOV networking → +125% network throughput
4. Switch to NVMe passthrough → +220% storage IOPS

## Report Contents

The generated markdown report includes:

```markdown
# Virtualization Performance Tuning Report
*Generated: [timestamp]*
*VM: [name]*
*Workload Type: [type]*
*Hypervisor: [KVM/other]*

## Executive Summary

### Current Performance
- CPU Performance: X% of native
- Memory Latency: Xns (native: Yns)
- Network Throughput: X Gbps
- Storage IOPS: X (read), X (write)

### Optimization Potential
- Expected improvement: X% overall
- Estimated time to implement: [duration]
- Risk level: [assessment]

### Quick Wins (< 1 hour implementation)
1. [Optimization] → +X% improvement
2. [Optimization] → +X% improvement

## Performance Baseline

### CPU Benchmarks
\`\`\`
Test              VM Performance    Native Performance   Overhead
-----------------------------------------------------------------
Integer ops       X MOPS           Y MOPS              Z%
Floating point    X MFLOPS         Y MFLOPS            Z%
Memory copy       X MB/s           Y MB/s              Z%
Context switch    X μs             Y μs                Z%
\`\`\`

### Memory Performance
\`\`\`
Metric                Current    Optimal    Gap
-------------------------------------------------
Latency (sequential)  X ns       Y ns       Z%
Latency (random)      X ns       Y ns       Z%
Bandwidth (read)      X GB/s     Y GB/s     Z%
Bandwidth (write)     X GB/s     Y GB/s     Z%
\`\`\`

### Network Performance
\`\`\`
Test              Current    Potential   Improvement
-----------------------------------------------------
TCP throughput    X Gbps     Y Gbps      +Z%
UDP throughput    X Gbps     Y Gbps      +Z%
Latency (avg)     X μs       Y μs        -Z%
Packets/sec       X Kpps     Y Kpps      +Z%
\`\`\`

### Storage Performance
\`\`\`
Test                 Current    Potential   Improvement
---------------------------------------------------------
Sequential read      X MB/s     Y MB/s      +Z%
Sequential write     X MB/s     Y MB/s      +Z%
Random read IOPS     X          Y           +Z%
Random write IOPS    X          Y           +Z%
Latency (avg)        X ms       Y ms        -Z%
\`\`\`

## Configuration Analysis

### Current vCPU Configuration
\`\`\`xml
<vcpu placement='static'>X</vcpu>
<cpu mode='[mode]'/>
<!-- [Analysis of current config] -->
\`\`\`

**Issues Identified:**
- ❌ [Issue 1]: [Description]
- ❌ [Issue 2]: [Description]
- ⚠️  [Issue 3]: [Description]

**Optimization Opportunities:**
- ✅ [Opportunity 1]: [Expected improvement]
- ✅ [Opportunity 2]: [Expected improvement]

### Current Memory Configuration
[Similar analysis for memory]

### Current Network Configuration
[Similar analysis for network]

### Current Storage Configuration
[Similar analysis for storage]

## Optimization Recommendations

### Priority 1: Critical Performance Improvements

#### 1. Enable Huge Pages (1GB)
**Expected Improvement:** +45% memory performance, -35% TLB misses
**Implementation Time:** 15 minutes
**Risk Level:** Low
**Rollback Procedure:** [Steps]

**Implementation:**
\`\`\`bash
# On host
echo 32 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages

# Verify
cat /proc/meminfo | grep Huge
\`\`\`

**VM Configuration:**
\`\`\`xml
<memoryBacking>
  <hugepages>
    <page size='1048576' unit='KiB' nodeset='0'/>
  </hugepages>
  <locked/>
</memoryBacking>
\`\`\`

**Verification:**
\`\`\`bash
# Run memory benchmark before/after
sysbench memory --memory-total-size=100G run
\`\`\`

#### 2. Implement CPU Pinning with NUMA Awareness
**Expected Improvement:** +30% CPU performance, -70% steal time
**Implementation Time:** 20 minutes
**Risk Level:** Medium
**Rollback Procedure:** [Steps]

[Detailed implementation guide...]

#### 3. Configure SR-IOV for Network
**Expected Improvement:** +125% network throughput, -60% CPU overhead
**Implementation Time:** 45 minutes
**Risk Level:** Medium
**Rollback Procedure:** [Steps]

[Detailed implementation guide...]

### Priority 2: Significant Optimizations

[Additional recommendations...]

### Priority 3: Advanced Tuning

[Advanced optimizations...]

## Workload-Specific Configuration

### Latency-Sensitive Configuration (Current Workload)

**Recommended VM Configuration:**
\`\`\`xml
<domain type='kvm'>
  <name>database-primary-01-optimized</name>

  <!-- CPU: Pinned, real-time priority -->
  <vcpu placement='static'>8</vcpu>
  <cpu mode='host-passthrough' check='none'>
    <topology sockets='1' cores='8' threads='1'/>
    <feature policy='require' name='invtsc'/>
    <feature policy='require' name='tsc-deadline'/>
  </cpu>

  <cputune>
    <!-- Pin to NUMA node 0, CPUs 0-7 -->
    <vcpupin vcpu='0' cpuset='0'/>
    <vcpupin vcpu='1' cpuset='1'/>
    <!-- ... -->
    <emulatorpin cpuset='8,9'/>

    <!-- Real-time scheduling -->
    <vcpusched vcpus='0-7' scheduler='fifo' priority='80'/>
  </cputune>

  <!-- Memory: 1GB huge pages, NUMA pinned -->
  <memory unit='GiB'>64</memory>
  <memoryBacking>
    <hugepages>
      <page size='1048576' unit='KiB' nodeset='0'/>
    </hugepages>
    <locked/>
    <nosharepages/>
  </memoryBacking>

  <numatune>
    <memory mode='strict' nodeset='0'/>
  </numatune>

  <!-- Storage: NVMe passthrough -->
  <disk type='block' device='disk'>
    <driver name='qemu' type='raw' cache='none' io='native'/>
    <source dev='/dev/nvme0n1'/>
    <target dev='vda' bus='virtio'/>
  </disk>

  <!-- Network: SR-IOV VF -->
  <interface type='hostdev' managed='yes'>
    <source>
      <address type='pci' domain='0x0000' bus='0x03' slot='0x10' function='0x0'/>
    </source>
    <mac address='52:54:00:12:34:56'/>
  </interface>
</domain>
\`\`\`

**Host Configuration:**
\`\`\`bash
#!/bin/bash
# host-optimization.sh

# 1. CPU isolation
echo "isolcpus=0-7 nohz_full=0-7 rcu_nocbs=0-7" >> /etc/default/grub
grub-mkconfig -o /boot/grub/grub.cfg

# 2. Disable frequency scaling
for cpu in /sys/devices/system/cpu/cpu[0-7]; do
  echo performance > \$cpu/cpufreq/scaling_governor
done

# 3. Disable C-states
for cpu in /sys/devices/system/cpu/cpu[0-7]; do
  for state in \$cpu/cpuidle/state*/disable; do
    echo 1 > \$state
  done
done

# 4. Configure huge pages
echo 64 > /sys/kernel/mm/hugepages/hugepages-1048576kB/nr_hugepages

# 5. Enable SR-IOV
echo 8 > /sys/class/net/ens2f0/device/sriov_numvfs
\`\`\`

## Implementation Plan

### Phase 1: Quick Wins (Day 1)
- [ ] Enable huge pages
- [ ] Configure CPU pinning
- [ ] Tune scheduler parameters
- [ ] Verify improvements

**Expected Improvement:** +50% overall performance

### Phase 2: Hardware Acceleration (Week 1)
- [ ] Configure SR-IOV networking
- [ ] Implement NVMe passthrough
- [ ] Optimize I/O threading
- [ ] Benchmark and validate

**Expected Improvement:** +120% overall performance

### Phase 3: Advanced Tuning (Week 2)
- [ ] Fine-tune NUMA configuration
- [ ] Optimize memory ballooning
- [ ] Implement vhost-user (if applicable)
- [ ] Final benchmarking

**Expected Improvement:** +150% overall performance

## Monitoring and Validation

### Performance Monitoring Setup
\`\`\`bash
#!/bin/bash
# monitor-vm-performance.sh

while true; do
  echo "=== Performance Metrics ==="
  echo "Date: \$(date)"

  # CPU metrics
  virsh vcpuinfo database-primary-01 | grep "CPU time"

  # Memory stats
  virsh domstats database-primary-01 --balloon

  # I/O stats
  virsh domblkstat database-primary-01 vda

  # Network stats
  virsh domifstat database-primary-01 vnet0

  sleep 60
done
\`\`\`

### Validation Tests

**CPU Performance:**
\`\`\`bash
# Before optimization
sysbench cpu --threads=8 --time=60 run

# After optimization
# Expected: +30% events/sec
\`\`\`

**Memory Performance:**
\`\`\`bash
# Before optimization
sysbench memory --memory-total-size=100G run

# After optimization
# Expected: +45% throughput, -35% latency
\`\`\`

**Network Performance:**
\`\`\`bash
# Before optimization
iperf3 -c server -t 60 -P 4

# After optimization
# Expected: +125% throughput
\`\`\`

**Storage Performance:**
\`\`\`bash
# Before optimization
fio --name=randread --rw=randread --bs=4k --iodepth=32 --runtime=60

# After optimization
# Expected: +220% IOPS
\`\`\`

## Risk Mitigation

### Rollback Procedures

**If huge pages cause issues:**
\`\`\`bash
# Disable huge pages in VM config
virsh edit database-primary-01
# Remove <hugepages> section, restart VM
\`\`\`

**If CPU pinning causes issues:**
\`\`\`bash
# Remove CPU pinning
virsh vcpupin database-primary-01 --live --config --vcpu all --cpulist 0-63
\`\`\`

**If SR-IOV causes issues:**
\`\`\`bash
# Revert to virtio-net
virsh edit database-primary-01
# Change interface type back to bridge
\`\`\`

### Testing Checklist

Before production deployment:
- [ ] Test in staging environment
- [ ] Benchmark all metrics
- [ ] Validate application behavior
- [ ] Test failover scenarios
- [ ] Verify monitoring alerts
- [ ] Document rollback procedures
- [ ] Schedule maintenance window

## Appendix

### Benchmark Raw Data
[Detailed benchmark outputs]

### Configuration Files
[Complete configuration files]

### Reference Documentation
- KVM tuning guide: /usr/share/doc/kvm/tuning.md
- libvirt documentation: https://libvirt.org/formatdomain.html
- CPU steal time optimization: ./skills/cpu-steal-time-optimization
- Virtualization patterns: ./skills/virtualization-patterns

### Performance Comparison Matrix
[Before/after comparison tables]

### Hardware Specifications
[Detailed hardware specs]
```

## When to Use This Command

- Planning VM deployment for production workloads
- Experiencing suboptimal VM performance
- Preparing for capacity planning
- Evaluating virtualization overhead
- Optimizing latency-sensitive applications
- Maximizing throughput for high-load systems
- Before/after migration performance validation

## Skills Used

This command leverages the **virtualization-performance-tuning** skill to provide world-class expertise in:
- KVM/QEMU optimization
- Advanced CPU and memory tuning
- Network performance optimization (virtio-net, SR-IOV, vhost-user)
- Storage performance optimization (virtio-blk, virtio-scsi, passthrough)
- Hardware acceleration configuration
- Performance benchmarking and profiling

## Output Location

Reports are saved to: `./reports/virtualization-performance-tuning-YYYY-MM-DD-HHMMSS.md`

If the `reports` directory doesn't exist, it will be created automatically.

## Related Commands

- `/analyze-cpu-steal-time` - Focus specifically on CPU steal time issues
- `/design-high-load-system` - System architecture design
- `/optimize-linux-system` - Linux kernel optimization
