#!/bin/bash
# vm-performance-monitor.sh - Monitor VM performance

VM_NAME="$1"

if [ -z "$VM_NAME" ]; then
    echo "Usage: $0 <vm-name>"
    exit 1
fi

while true; do
    clear
    echo "=== VM Performance Dashboard: $VM_NAME ==="
    echo "Time: $(date)"
    echo ""

    # CPU metrics
    echo "--- CPU ---"
    virsh vcpuinfo "$VM_NAME" | grep -E 'CPU:|CPU time:|State:'
    echo ""

    # Memory metrics
    echo "--- Memory ---"
    virsh domstats "$VM_NAME" --balloon | grep -E 'balloon\.'
    echo ""

    # I/O metrics
    echo "--- Storage ---"
    virsh domblkstat "$VM_NAME" vda
    echo ""

    # Network metrics
    echo "--- Network ---"
    virsh domifstat "$VM_NAME" vnet0
    echo ""

    sleep 5
done
