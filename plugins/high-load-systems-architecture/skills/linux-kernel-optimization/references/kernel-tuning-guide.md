# Linux Kernel Tuning Guide

## CPU

### Frequency Scaling
```bash
# Set performance governor
echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

### CPU Isolation
```bash
# Isolate CPUs from scheduler
# Add to kernel cmdline: isolcpus=2-7 nohz_full=2-7
```

## Memory

### Transparent Huge Pages
```bash
# Enable THP
echo always > /sys/kernel/mm/transparent_hugepage/enabled

# Or disable for predictability
echo never > /sys/kernel/mm/transparent_hugepage/enabled
```

### Swappiness
```bash
# Reduce swap tendency
sysctl vm.swappiness=10
```

## Network

### TCP Buffer Sizes
```bash
sysctl net.ipv4.tcp_rmem="4096 87380 6291456"
sysctl net.ipv4.tcp_wmem="4096 65536 4194304"
```

### Congestion Control
```bash
# Use BBR
sysctl net.ipv4.tcp_congestion_control=bbr
```

## I/O

### Scheduler
```bash
# For SSD/NVMe
echo none > /sys/block/sda/queue/scheduler

# For HDD
echo mq-deadline > /sys/block/sda/queue/scheduler
```

## Monitoring

```bash
# CPU stats
mpstat -P ALL 1

# Memory stats
vmstat 1

# I/O stats
iostat -x 1

# Network stats
ss -s
```
