---
name: spark-training-gotchas
description: Preflight and diagnose the ten known failure modes for ML training on NVIDIA DGX Spark. Use when a training run on DGX Spark fails to start, OOMs below the 128GB limit, slows down mid-run, or before any multi-hour training job on GB10.
---

# Spark Training Gotchas

DGX Spark's GB10 chip (Grace Blackwell, SM121, 128GB unified
memory, aarch64) has ten recurring failure modes across
launch, memory, thermals, bandwidth, and precision. Each is
named G1–G10 so it can be checked by number — the numbering
is load-bearing for tooling that runs these checks. Read this
before a long run, not after hour six.

## When to Use This Skill

- A training run fails to start, with an import error or a
  segfault that doesn't point at the real cause.
- A run OOMs while `nvidia-smi` still shows headroom.
- Throughput degrades partway through a run that started fine.
- Before any multi-hour or multi-epoch job on GB10.
- Wiring two Sparks together, before picking a parallelism
  strategy.
- Choosing between FP8 and NVFP4 for a Spark-hosted run.

## Common Issues Quick Reference

| # | Symptom | Fix |
|---|---|---|
| G1 | undefined symbol / segfault | cu130 wheel or container |
| G2 | flash-attn wrong backend used | skip pip build; monkeypatch on NGC |
| G3 | OOM despite headroom | drop page cache |
| G4 | throughput drop / reboot | expect ~100W sustained cap |
| G5 | memory-bound step slow | budget 180–192 GB/s |
| G6 | cache evicted mid-run | one GPU server at a time |
| G7 | NVFP4 slower than FP8 | stay FP8 unless `sm_121a` |
| G8 | playbook fails outright | check upstream issues |
| G9 | env breaks after install | use a container |
| G10 | 2-Spark TP hangs | DDP/FSDP only, never TP |

## The Ten Gotchas

### G1: CUDA 12/13 ABI Mismatch

- **SYMPTOM:** `ImportError: undefined symbol` naming a CUDA
  function, or a segfault on the first `.cuda()` call.
- **CAUSE:** most PyPI wheels link `libcudart.so.12`; Spark
  ships CUDA 13. pip never checks CUDA ABI, so it surfaces
  only at import or first kernel launch.
- **CHECK:** `references/gotcha-checks.md` G1 — the wheel's
  CUDA build tag.
- **FIX:** reinstall from `download.pytorch.org/whl/cu130` or
  use a matched container.

### G2: flash-attn — Skip the pip Build, Watch Unsloth's Auto-Detect

- **SYMPTOM:** `pip install flash-attn` still fails/hangs.
  Unsloth may also silently train flash-attn over an
  explicitly requested SDPA.
- **CAUSE:** no aarch64/sm_121 wheel for bare pip — but NGC
  containers ship a working SM121 flash-attn, and Unsloth
  auto-prefers it, dropping `attn_implementation="sdpa"`.
- **CHECK:** `references/gotcha-checks.md` G2 — is flash-attn
  already present and working.
- **FIX:** bare pip — skip flash-attn, use SDPA (unchanged). On
  NGC — the only reliable override is the monkeypatch in
  `references/gotcha-checks.md` G2.

### G3: UMA OOM Below 128GB

- **SYMPTOM:** OOM during model load/training while
  `nvidia-smi` still reports free memory under the 128GB cap
  — or, on some setups, `[N/A]` outright instead of a number.
- **CAUSE:** mmap and the CUDA allocator double-count pages
  during safetensors load; QLoRA can OOM *earlier* than bf16
  since dequantization adds transient allocs.
- **CHECK:** `references/gotcha-checks.md` G3 — read `free -g`
  and `/proc/meminfo`, not `nvidia-smi`.
- **FIX:** drop the page cache with
  `sync; echo 3 > /proc/sys/vm/drop_caches` — needs root, a
  between-run reset, not a mid-training step.

### G4: Thermal Throttling

- **SYMPTOM:** throughput drops partway through a multi-hour
  run, or the box spontaneously reboots under sustained load.
- **CAUSE:** sustained power draw caps around 100W versus the
  240W rated figure; long runs push into that ceiling and
  throttle or, sometimes, reboot.
- **CHECK:** `references/gotcha-checks.md` G4 — sample
  `nvidia-smi --query-gpu=temperature.gpu,power.draw`.
- **FIX:** if power plateaus under 240W while temperature
  climbs, treat throttling as the cause; improve cooling or
  cap run length.

### G5: Bandwidth Ceiling

- **SYMPTOM:** memory-bound workloads, decode-heavy RL loops
  especially, plateau well below expected throughput.
- **CAUSE:** 273 GB/s is a spec ceiling, not sustained;
  measured bandwidth runs 180–192 GB/s.
- **CHECK:** `references/gotcha-checks.md` G5 — observed step
  time vs. the measured range, not spec.
- **FIX:** budget throughput from 180–192 GB/s; revise a plan
  built on the 273 GB/s figure.

### G6: Global UMA Resource Contention

- **SYMPTOM:** a process's KV cache/weights get evicted
  mid-run silently, no OOM in its own logs.
- **CAUSE:** unified memory is
  one global pool; an uncapped
  or near-capacity process
  competes with anything else
  and can evict it. A small,
  bounded workload doesn't — a
  <4GB LoRA coexists fine
  alongside vLLM capped at
  `gpu-memory-utilization<=0.5`.
- **CHECK:** `references/gotcha-checks.md`
  G6 — other GPU-resident
  processes and whether
  capped.
- **FIX:** the one-heavy-job
  rule applies to **uncapped or
  near-capacity** workloads —
  cap or stop unrelated servers
  first. A small, capped
  workload need not
  stop.

### G7: NVFP4 Slower Than FP8 on SM121

- **SYMPTOM:** switching an inference workload from FP8 to
  NVFP4 on Spark makes it slower, not faster.
- **CAUSE:** SM121 lacks `cvt.e2m1x2` unless kernels target
  `sm_121a`; NVFP4 runs ~32% slower without it.
- **CHECK:** `references/gotcha-checks.md` G7 — capability
  reports `(12, 1)`; does the build target `sm_121a`?
- **FIX:** stay on FP8 unless the build targets `sm_121a`.

### G8: Stale Official Playbooks

- **SYMPTOM:** following an official DGX Spark playbook still
  fails, with no local misconfiguration explaining it.
- **CAUSE:** official playbooks have shipped broken before;
  the stack moves faster than the docs.
- **CHECK:** `references/gotcha-checks.md` G8 — the playbook
  repo's recent issues.
- **FIX:** check `github.com/NVIDIA/dgx-spark-playbooks` issues
  before trusting a recipe for an expensive run.

### G9: Container-First, Not Bare Pip

- **SYMPTOM:** a bare-pip environment that worked yesterday
  breaks after an unrelated `pip install`, or two "identical"
  environments behave differently.
- **CAUSE:** bare pip lets Triton, xformers, and transformers
  drift independently; nothing pins them to GB10's SM121
  target.
- **CHECK:** `references/gotcha-checks.md`
  G9 — container or bare pip?
- **FIX:** prefer an NGC container (see `spark-environment-setup`
  for tag guidance) or Unsloth's container. If bare pip is
  unavoidable, follow the NVIDIA install order, including
  `--no-deps` on Unsloth.

### G10: Dual-Spark Is DDP/FSDP Only

- **SYMPTOM:** a tensor-parallel launch across two Sparks
  hangs, runs far slower than single-Spark, or errors out.
- **CAUSE:** ConnectX-7 is fast enough for gradient/parameter
  sync (DDP, FSDP) but too thin for TP's fine-grained traffic.
- **CHECK:** `references/gotcha-checks.md` G10 — the
  configured parallelism strategy.
- **FIX:** on a two-Spark setup, choose DDP or FSDP, never
  tensor parallelism — TP is single-node only here.

## Fast Triage

The cheapest checks to run before anything else:

```bash
python3 -c "import torch; print(torch.version.cuda)"  # expect 13.x (G1); NGC builds have no +cu130 tag — that's not a failure
```

```python
import torch; print(torch.cuda.get_device_capability())  # expect (12, 1) (G7)
```

```bash
{ [ -f /.dockerenv -o -f /run/.containerenv ] || grep -qE 'docker|containerd' /proc/1/cgroup; } 2>/dev/null && echo container || echo unknown  # G9
```

`assets/preflight.sh` runs G1, G3, G4, G7, G9 and produces one
output line per gotcha in a fixed format: G-number first, then
PASS/FAIL/WARN where automatable, SKIP when unavailable, or
`INFO:` for a raw reading (G3, G4). Full commands:
`references/gotcha-checks.md`. See also
`spark-environment-setup` for the environment assumed working.
