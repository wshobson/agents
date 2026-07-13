---
name: spark-training-gotchas
description: Preflight and diagnose the ten known failure modes for ML training on NVIDIA DGX Spark. Use when a training run on DGX Spark fails to start, OOMs below the 128GB limit, slows down mid-run, or before launching any multi-hour training job on GB10 hardware.
---

# Spark Training Gotchas

DGX Spark's GB10 chip (Grace Blackwell, SM121, 128GB unified
memory, aarch64) has ten recurring failure modes across
launch, memory, thermals, bandwidth, and precision. Each is
named G1–G10 so it can be checked by number — the numbering
is load-bearing for tooling that runs these checks. Read this
before a long run, not after it fails at hour six.

## When to Use This Skill

- A training run fails to start, with an import error or a
  segfault that doesn't point at the real cause.
- A run OOMs while `nvidia-smi` still shows headroom under
  the 128GB unified-memory ceiling.
- Throughput degrades partway through a run that started
  fine.
- Before any multi-hour or multi-epoch job on GB10 — a
  five-minute preflight beats hour six.
- Wiring two Sparks together, before the parallelism
  strategy is chosen.
- Choosing between FP8 and NVFP4 for a Spark-hosted run.

## Common Issues Quick Reference

| # | Symptom | Fix |
|---|---|---|
| G1 | undefined symbol / segfault | cu130 wheel or container |
| G2 | flash-attn build fails | skip it; use SDPA |
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
  function, or a segfault on the first `.cuda()`
  call with no useful traceback.
- **CAUSE:** most wheels on PyPI link against
  `libcudart.so.12`; Spark ships CUDA 13. pip
  never checks CUDA ABI, so it surfaces only at
  import or first kernel launch.
- **CHECK:** `references/gotcha-checks.md` G1 — the wheel's
  CUDA build tag.
- **FIX:** reinstall from
  `download.pytorch.org/whl/cu130` or use a
  matched container.

### G2: flash-attn Absent

- **SYMPTOM:** `flash-attn` fails to build, or builds but
  hangs or crashes on the first attention call.
- **CAUSE:** no published sm_121 kernels for flash-attn on
  GB10 as of this writing.
- **CHECK:** `references/gotcha-checks.md` G2 — no flash-attn
  import in the training path.
- **FIX:** skip flash-attn; use PyTorch's built-in SDPA
  backend — faster here anyway.

### G3: UMA OOM Below 128GB

- **SYMPTOM:** OOM during model load or training while
  `nvidia-smi` still reports free memory under
  the 128GB unified-memory cap.
- **CAUSE:** mmap and the CUDA allocator double-count pages
  during safetensors load, understating true
  pressure; QLoRA can OOM *earlier* than bf16
  since dequantization adds transient allocations.
- **CHECK:** `references/gotcha-checks.md` G3 — read `free -g`
  and `/proc/meminfo`, not `nvidia-smi`.
- **FIX:** drop the page cache with
  `sync; echo 3 > /proc/sys/vm/drop_caches`. Needs
  root and flushes cache system-wide — a
  between-run reset, not a mid-training step.

### G4: Thermal Throttling

- **SYMPTOM:** throughput drops partway through a multi-hour
  run, or the box spontaneously reboots under
  sustained load.
- **CAUSE:** sustained power draw caps around 100W versus
  the 240W rated figure; multi-hour runs push
  into that ceiling and throttle or, sometimes,
  reboot.
- **CHECK:** `references/gotcha-checks.md` G4 — sample
  `nvidia-smi --query-gpu=temperature.gpu,power.draw`
  over a long run.
- **FIX:** if power plateaus under 240W while temperature
  climbs, treat throttling as the cause; improve
  cooling or cap run length.

### G5: Bandwidth Ceiling

- **SYMPTOM:** memory-bound workloads, decode-heavy RL loops
  especially, plateau well below expected
  throughput.
- **CAUSE:** the 273 GB/s figure is a spec ceiling, not
  sustained; measured bandwidth runs 180–192 GB/s.
- **CHECK:** `references/gotcha-checks.md` G5 — observed step
  time vs. the measured range, not spec.
- **FIX:** budget throughput from 180–192 GB/s; revise a
  plan built on the 273 GB/s figure.

### G6: Global UMA Resource Contention

- **SYMPTOM:** a training or inference process's KV cache or
  weights get silently evicted mid-run, with no
  OOM in that process's own logs.
- **CAUSE:** unified memory is one global pool; concurrent
  processes (e.g. vLLM and Ollama side by side)
  compete for it and can evict each other.
- **CHECK:** `references/gotcha-checks.md` G6 — other
  GPU-resident processes before a long run.
- **FIX:** run one GPU-resident server at a time; stop
  unrelated servers before a full-pool run.

### G7: NVFP4 Slower Than FP8 on SM121

- **SYMPTOM:** switching an inference workload from FP8 to
  NVFP4 on Spark makes it slower, not faster.
- **CAUSE:** SM121 lacks a native `cvt.e2m1x2` path unless
  kernels target `sm_121a`; without that, NVFP4
  runs ~32% slower than FP8 here.
- **CHECK:** `references/gotcha-checks.md` G7 — capability
  reports `(12, 1)`; does the build target `sm_121a`?
- **FIX:** stay on FP8 unless the build explicitly targets
  `sm_121a`.

### G8: Stale Official Playbooks

- **SYMPTOM:** following an official DGX Spark playbook step
  by step still fails, with no local
  misconfiguration explaining it.
- **CAUSE:** official playbooks have shipped broken before;
  the stack moves faster than the docs.
- **CHECK:** `references/gotcha-checks.md` G8 — the playbook
  repo's recent issues.
- **FIX:** check `github.com/NVIDIA/dgx-spark-playbooks`
  issues before trusting a recipe for an
  expensive run.

### G9: Container-First, Not Bare Pip

- **SYMPTOM:** a bare-pip environment that worked yesterday
  breaks after an unrelated `pip install`, or
  two "identical" environments behave
  differently.
- **CAUSE:** bare pip lets Triton, xformers, and
  transformers versions drift independently;
  nothing pins them to GB10's SM121 target the
  way a container does.
- **CHECK:** `references/gotcha-checks.md` G9 — is the
  environment container-based or bare pip?
- **FIX:** prefer an NGC
  (`nvcr.io/nvidia/pytorch:25.11-py3`) or Unsloth
  container. If bare pip is unavoidable, follow
  the NVIDIA install order, including `--no-deps`
  on the Unsloth line.

### G10: Dual-Spark Is DDP/FSDP Only

- **SYMPTOM:** a tensor-parallel launch across two Sparks
  hangs, runs far slower than single-Spark, or
  errors out.
- **CAUSE:** the ConnectX-7 link is fast enough for
  gradient/parameter sync (DDP, FSDP) but too
  thin for the fine-grained traffic tensor
  parallelism requires.
- **CHECK:** `references/gotcha-checks.md` G10 — the
  configured parallelism strategy.
- **FIX:** on a two-Spark setup, choose DDP or FSDP and
  never tensor parallelism — TP is single-node
  only here.

## Fast Triage

The cheapest checks to run before anything else:

```bash
pip show torch | grep -i version  # expect cu130 (G1)
```

```python
import torch; print(torch.cuda.get_device_capability())  # expect (12, 1) (G7)
```

```bash
grep -qi docker /proc/1/cgroup && echo container || echo bare-host  # G9
```

`assets/preflight.sh` runs G1, G3, G4, G7, G9. Every result
line starts with its G-number — the output format
`/spark-preflight` will parse: PASS/FAIL where automatable
(G1, G7, G9), `INFO:` raw readings for judgment (G3, G4).
Full commands and interpretation notes per gotcha:
`references/gotcha-checks.md`. See also
`plugins/dgx-spark-ops/skills/spark-environment-setup/SKILL.md`
for the environment these gotchas assume is already working.
