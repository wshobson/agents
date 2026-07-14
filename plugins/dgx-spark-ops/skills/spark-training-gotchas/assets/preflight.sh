#!/usr/bin/env bash
# Fast, automatable subset of the G1-G10 checks in SKILL.md.
# Output contract: every result line starts with its G-number.
#   G1/G7/G9 emit PASS/FAIL/WARN verdicts; G3/G4 emit INFO lines
#   (raw readings needing judgment — see SKILL.md G3/G4).
# Non-automatable gotchas (G2 avoid-a-library, G6 process survey,
# G8 upstream-issue lookup, G10 config review) are not covered
# here — see references/gotcha-checks.md for those.
# Usage: bash preflight.sh
set -uo pipefail

echo "== G1: CUDA 12/13 ABI =="
g1_cuda_ver=$(python3 -c "import torch; print(torch.version.cuda or '')" 2>/dev/null)
if [ -z "$g1_cuda_ver" ]; then
  echo "G1 SKIP: torch not importable"
elif [[ "$g1_cuda_ver" == 13* ]]; then
  echo "G1 PASS: torch built against CUDA $g1_cuda_ver"
else
  echo "G1 FAIL: torch built against CUDA $g1_cuda_ver (need 13.x — see gotcha G1)"
fi

echo "== G3: UMA headroom (raw reading) =="
free -g | awk 'NR==2 {print "G3 INFO: free/used (GB):", $4, $3}'

echo "== G4: thermal snapshot (raw reading) =="
nvidia-smi --query-gpu=temperature.gpu,power.draw --format=csv,noheader 2>/dev/null \
  | sed 's/^/G4 INFO: /' || echo "G4 SKIP: nvidia-smi not available"

echo "== G7: SM121 + NVFP4 target =="
python3 -c "
import torch
cap = torch.cuda.get_device_capability()
print('G7 PASS: SM121 detected' if cap == (12, 1) else f'G7 WARN: unexpected capability {cap}')
" 2>/dev/null || echo "G7 SKIP: torch not importable"

echo "== G9: container vs bare pip =="
if grep -qi docker /proc/1/cgroup 2>/dev/null; then
  echo "G9 PASS: running inside a container"
else
  echo "G9 WARN: bare host — prefer an NGC or Unsloth container"
fi

echo "Full details and remaining gotchas: references/gotcha-checks.md"
