#!/usr/bin/env python3
"""
numa-topology-analyzer.py - Analyze NUMA topology and suggest optimal VM placement
"""

import subprocess
import sys

def analyze_numa():
    """Analyze NUMA topology"""
    result = subprocess.run(['numactl', '--hardware'], capture_output=True, text=True)

    print("=== NUMA Topology Analysis ===\n")
    print(result.stdout)

    # Parse available nodes
    lines = result.stdout.split('\n')
    nodes = {}

    for line in lines:
        if line.startswith('node') and 'cpus:' in line:
            parts = line.split()
            node_id = int(parts[0].replace('node', ''))
            cpus = [int(c) for c in parts[3:]]
            nodes[node_id] = cpus

    print("\n=== VM Placement Recommendations ===\n")

    for node_id, cpus in nodes.items():
        print(f"Node {node_id}:")
        print(f"  Available CPUs: {len(cpus)}")
        print(f"  CPU List: {cpus}")
        print(f"  Recommended VM sizes:")
        print(f"    - Small (2 vCPUs):  {cpus[:2]}")
        print(f"    - Medium (4 vCPUs): {cpus[:4]}")
        print(f"    - Large (8 vCPUs):  {cpus[:8]}")
        print()

if __name__ == '__main__':
    analyze_numa()
