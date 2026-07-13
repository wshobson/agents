#!/usr/bin/env bash
# Background thermal/power sampler for a long training run.
# Output contract: CSV, one line per sample, matching
# `nvidia-smi --query-gpu` field order — pipe-compatible with
# the training log for later correlation by timestamp.
# Usage: bash thermal-sample.sh [interval_seconds] [logfile]
set -uo pipefail

INTERVAL="${1:-30}"
LOGFILE="${2:-thermal.log}"

echo "timestamp,temperature.gpu,power.draw" > "$LOGFILE"
nvidia-smi --query-gpu=timestamp,temperature.gpu,power.draw \
  --format=csv,noheader -l "$INTERVAL" >> "$LOGFILE" &
echo "Sampling every ${INTERVAL}s into ${LOGFILE} (pid $!)"
echo "A sustained ~100W reading is the platform cap, not a bug — see SKILL.md Thermal Monitoring."
