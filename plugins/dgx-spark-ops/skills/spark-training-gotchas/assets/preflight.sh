#!/usr/bin/env bash
# Fast, automatable subset of the G1-G10 checks in SKILL.md.
# Non-automatable gotchas (G2 avoid-a-library, G6 process survey,
# G8 upstream-issue lookup, G10 config review) are not covered
# here — see references/gotcha-checks.md for those.
# Usage: bash preflight.sh
set -uo pipefail

echo "== G1: CUDA 12/13 ABI =="
if pip show torch 2>/dev/null | grep -qi cu130; then
  echo "PASS: torch reports a cu130 build"
else
  echo "FAIL: torch is not a cu130 build (check libcudart version)"
fi

echo "== G3: UMA headroom =="
free -g | awk 'NR==2 {print "free/used (GB):", $4, $3}'

echo "== G4: thermal snapshot =="
nvidia-smi --query-gpu=temperature.gpu,power.draw --format=csv,noheader 2>/dev/null \
  || echo "SKIP: nvidia-smi not available"

echo "== G7: SM121 + NVFP4 target =="
python3 -c "
import torch
cap = torch.cuda.get_device_capability()
print('PASS: SM121 detected' if cap == (12, 1) else f'WARN: unexpected capability {cap}')
" 2>/dev/null || echo "SKIP: torch not importable"

echo "== G9: container vs bare pip =="
if grep -qi docker /proc/1/cgroup 2>/dev/null; then
  echo "PASS: running inside a container"
else
  echo "WARN: bare host — prefer an NGC or Unsloth container"
fi

echo "Full details and remaining gotchas: references/gotcha-checks.md"
