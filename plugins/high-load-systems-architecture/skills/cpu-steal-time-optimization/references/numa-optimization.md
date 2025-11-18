# NUMA Optimization Guide

## Understanding NUMA

### Topology
```
Node 0:
├─ CPUs: 0-7
├─ Memory: 64GB
└─ Local access: 100ns

Node 1:
├─ CPUs: 8-15
├─ Memory: 64GB
└─ Remote access (from Node 0): 200ns (2x slower)
```

## VM NUMA Configuration

### Single-Node VM
```xml
<vcpu placement='static'>8</vcpu>
<cputune>
  <vcpupin vcpu='0' cpuset='0'/>
  ...
  <vcpupin vcpu='7' cpuset='7'/>
</cputune>
<numatune>
  <memory mode='strict' nodeset='0'/>
</numatune>
```

### Multi-Node VM
```xml
<cpu>
  <numa>
    <cell id='0' cpus='0-3' memory='32' unit='GiB' memAccess='shared'/>
    <cell id='1' cpus='4-7' memory='32' unit='GiB' memAccess='shared'/>
  </numa>
</cpu>

<numatune>
  <memnode cellid='0' mode='strict' nodeset='0'/>
  <memnode cellid='1' mode='strict' nodeset='1'/>
</numatune>
```

## Monitoring

```bash
# Show NUMA topology
numactl --hardware

# Per-node memory stats
numastat

# Process NUMA maps
cat /proc/<pid>/numa_maps
```

## Best Practices

1. Align vCPUs to single NUMA node when possible
2. Use strict memory binding
3. Disable automatic NUMA balancing for pinned VMs
4. Monitor remote memory access
