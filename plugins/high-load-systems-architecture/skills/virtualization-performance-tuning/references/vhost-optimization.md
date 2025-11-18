# vhost Optimization

## vhost-net (Kernel-Space)

### Enable vhost-net
```xml
<interface type='bridge'>
  <model type='virtio'/>
  <driver name='vhost'/>  <!-- Use vhost-net -->
</interface>
```

**Benefits**:
- Reduces VM-exits
- Lower CPU overhead
- Better throughput

## vhost-user (Userspace)

### With DPDK
```bash
# Start OVS-DPDK
ovs-vsctl add-br br0 -- set bridge br0 datapath_type=netdev
ovs-vsctl add-port br0 vhost-user1 -- \
  set Interface vhost-user1 type=dpdkvhostuserclient \
  options:vhost-server-path=/var/run/openvswitch/vhost-user1
```

### VM Configuration
```xml
<memoryBacking>
  <hugepages/>
  <access mode='shared'/>  <!-- Required for vhost-user -->
</memoryBacking>

<interface type='vhostuser'>
  <source type='unix' path='/var/run/openvswitch/vhost-user1' mode='client'/>
  <model type='virtio'/>
  <driver queues='4'/>
</interface>
```

## vhost-blk

### SPDK Integration
```bash
# Start SPDK vhost target
./build/bin/vhost -S /var/tmp -m 0x3

# Create vhost-blk device
./scripts/rpc.py bdev_malloc_create 4096 512 -b Malloc0
./scripts/rpc.py vhost_create_blk_controller --cpumask 0x1 vhost.0 Malloc0
```

### VM Configuration
```xml
<disk type='vhostuser' device='disk'>
  <source type='unix' path='/var/tmp/vhost.0'/>
  <target dev='vda' bus='virtio'/>
</disk>
```

## Performance Impact

| Backend | Throughput | CPU Overhead | Latency |
|---------|------------|--------------|---------|
| QEMU (userspace) | Baseline | 100% | Baseline |
| vhost-net | +30% | -40% | -20% |
| vhost-user (DPDK) | +120% | -60% | -50% |
| vhost-blk (SPDK) | +150% | -70% | -60% |
