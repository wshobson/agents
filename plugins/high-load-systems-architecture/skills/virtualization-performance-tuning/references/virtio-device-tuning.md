# Virtio Device Tuning

## virtio-net (Network)

### Multi-Queue
```xml
<driver queues='4'/>  <!-- Number of TX/RX queue pairs -->
```

**Guest Setup**:
```bash
ethtool -L eth0 combined 4
```

### Offloading
```xml
<driver>
  <host csum='on' gso='on' tso4='on' tso6='on' ecn='on' ufo='on'/>
  <guest csum='on' gso='on' tso4='on' tso6='on' ecn='on' ufo='on'/>
</driver>
```

### Ring Buffer Size
```bash
# In guest
ethtool -G eth0 rx 4096 tx 4096
```

## virtio-blk (Storage)

### Queue Configuration
```xml
<driver queues='4'/>  <!-- Match vCPU count -->
```

### Native AIO
```xml
<driver io='native'/>  <!-- Use Linux AIO -->
```

### Discard/TRIM
```xml
<driver discard='unmap'/>  <!-- Enable TRIM -->
```

## virtio-scsi

### Multi-Queue Controller
```xml
<controller type='scsi' model='virtio-scsi'>
  <driver queues='4' iothread='1'/>
</controller>
```

## Performance Comparison

| Device | Throughput | Latency | CPU Usage |
|--------|------------|---------|-----------|
| virtio-net (single-queue) | 2 Gbps | 5ms | 60% |
| virtio-net (multi-queue) | 9 Gbps | 2ms | 25% |
| virtio-blk | 80K IOPS | 1ms | 20% |
| virtio-scsi | 75K IOPS | 1.2ms | 22% |
