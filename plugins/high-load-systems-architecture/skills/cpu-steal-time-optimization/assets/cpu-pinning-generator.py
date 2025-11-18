#!/usr/bin/env python3
"""
cpu-pinning-generator.py - Generate optimal CPU pinning configuration
"""

import subprocess
import sys

def get_numa_topology():
    """Parse NUMA topology from lscpu"""
    result = subprocess.run(['lscpu', '--extended'], capture_output=True, text=True)
    topology = {}

    for line in result.stdout.split('\n')[1:]:
        if not line.strip():
            continue
        parts = line.split()
        cpu = int(parts[0])
        node = int(parts[1])
        socket = int(parts[2])
        core = int(parts[3])

        if node not in topology:
            topology[node] = []
        topology[node].append({'cpu': cpu, 'socket': socket, 'core': core})

    return topology

def generate_pinning_config(vm_name, vcpus, numa_node=0):
    """Generate libvirt CPU pinning XML"""
    topology = get_numa_topology()

    if numa_node not in topology:
        print(f"Error: NUMA node {numa_node} not found")
        sys.exit(1)

    available_cpus = topology[numa_node]
    if len(available_cpus) < vcpus:
        print(f"Error: Not enough CPUs on NUMA node {numa_node}")
        sys.exit(1)

    print(f"<domain type='kvm'>")
    print(f"  <name>{vm_name}</name>")
    print(f"  <vcpu placement='static'>{vcpus}</vcpu>")
    print(f"  <cputune>")

    for i in range(vcpus):
        pcpu = available_cpus[i]['cpu']
        print(f"    <vcpupin vcpu='{i}' cpuset='{pcpu}'/>")

    print(f"  </cputune>")
    print(f"  <numatune>")
    print(f"    <memory mode='strict' nodeset='{numa_node}'/>")
    print(f"  </numatune>")
    print(f"</domain>")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: cpu-pinning-generator.py <vm-name> <vcpus> <numa-node>")
        sys.exit(1)

    vm_name = sys.argv[1]
    vcpus = int(sys.argv[2])
    numa_node = int(sys.argv[3])

    generate_pinning_config(vm_name, vcpus, numa_node)
