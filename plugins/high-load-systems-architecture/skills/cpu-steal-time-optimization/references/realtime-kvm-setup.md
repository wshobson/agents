# Real-Time KVM Setup

## Install RT Kernel

### Ubuntu/Debian
```bash
apt-get install linux-image-rt-amd64
reboot
```

### RHEL/CentOS
```bash
yum install kernel-rt
reboot
```

### Verify
```bash
uname -a | grep PREEMPT_RT
```

## RT Throttling Configuration

```bash
# Disable RT throttling (allow 100% CPU for RT tasks)
sysctl kernel.sched_rt_runtime_us=-1

# Or increase budget
sysctl kernel.sched_rt_period_us=1000000   # 1 second
sysctl kernel.sched_rt_runtime_us=950000   # 95%
```

## VM RT Configuration

```xml
<domain type='kvm'>
  <cputune>
    <!-- RT scheduling for vCPUs -->
    <vcpusched vcpus='0-3' scheduler='fifo' priority='80'/>
    
    <!-- Emulator threads at lower priority -->
    <emulatorsched scheduler='fifo' priority='40'/>
  </cputune>
</domain>
```

## Host Optimization

```bash
# CPU isolation
echo "isolcpus=1-7 nohz_full=1-7 rcu_nocbs=1-7" >> /etc/default/grub
grub-mkconfig -o /boot/grub/grub.cfg

# Disable IRQ balancing
echo "IRQBALANCE_BANNED_CPUS=fe" > /etc/sysconfig/irqbalance

# Latency measurement
cyclictest -m -Sp90 -i200 -h400 -q
```
