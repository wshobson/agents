#!/usr/bin/env bash
# Background thermal/power sampler for a long training run.
# Output contract: CSV, one line per sample, matching
# `nvidia-smi --query-gpu` field order — pipe-compatible with
# the training log for later correlation by timestamp.
# Usage: bash thermal-sample.sh [interval_seconds] [logfile]
set -uo pipefail

command -v nvidia-smi >/dev/null || { echo "nvidia-smi not found" >&2; exit 1; }

INTERVAL="${1:-30}"
LOGFILE="${2:-thermal.log}"
PIDFILE="${LOGFILE}.pid"

if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "Stopping existing sampler (pid $(cat "$PIDFILE"))"
  kill "$(cat "$PIDFILE")"
fi

echo "timestamp,temperature.gpu,power.draw" > "$LOGFILE"
nvidia-smi --query-gpu=timestamp,temperature.gpu,power.draw \
  --format=csv,noheader -l "$INTERVAL" >> "$LOGFILE" &
PID=$!
echo "$PID" > "$PIDFILE"
echo "Sampling every ${INTERVAL}s into ${LOGFILE} (pid $PID)"
echo "A sustained ~100W reading is the platform cap, not a bug — see SKILL.md Thermal Monitoring."
