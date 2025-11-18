#!/bin/bash
# steal-time-monitor.sh - Monitor CPU steal time

VM_NAME="$1"
THRESHOLD=5  # Alert if steal > 5%
LOG_FILE="/var/log/steal-time-monitor.log"

if [ -z "$VM_NAME" ]; then
    echo "Usage: $0 <vm-name>"
    exit 1
fi

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

    # Get steal time from VM
    STEAL=$(ssh "$VM_NAME" "mpstat 1 1 | grep Average | awk '{print \$NF}'")

    # Log steal time
    echo "$TIMESTAMP | VM: $VM_NAME | Steal: ${STEAL}%" >> "$LOG_FILE"

    # Alert if high steal
    if (( $(echo "$STEAL > $THRESHOLD" | bc -l) )); then
        echo "$TIMESTAMP | ALERT: High steal time ${STEAL}% on $VM_NAME" | \
            tee -a "$LOG_FILE"

        # Send notification
        curl -X POST https://alerts.example.com/webhook \
            -H "Content-Type: application/json" \
            -d "{\"vm\": \"$VM_NAME\", \"steal\": $STEAL, \"timestamp\": \"$TIMESTAMP\"}"
    fi

    sleep 60
done
