---
name: spark-environment-setup
description: Set up a working ML training/inference environment on NVIDIA DGX Spark (GB10, aarch64, CUDA 13). Use when installing PyTorch/Unsloth/TRL/vLLM on DGX Spark, hitting libcudart or wheel-ABI errors on aarch64, or choosing between NGC containers and bare pip installs.
---

# Spark Environment Setup

DGX Spark ships a GB10 Grace Blackwell chip: aarch64 CPU, SM121 GPU, 128GB
unified memory, CUDA 13. This is a narrower and younger platform than a
standard x86 CUDA 12 box, so package selection and ABI matching matter more
than usual — the wheel ecosystem for aarch64 + CUDA 13 is still
filling in, and the fixes below are the ones that keep coming up
in practice.

## When to Use This Skill

- Setting up a fresh Spark box for training or inference for the first time.
- Hitting an import error mentioning `libcudart`, a missing symbol, or a
  wheel that "installed fine but won't load."
- A framework install (PyTorch, Unsloth, TRL, vLLM, xformers) fails, hangs,
  or silently falls back to CPU.
- Deciding whether to use an NGC container or a bare pip environment for a
  given run.
- Restoring a working setup after an OS reinstall or a base-image update,
  and needing to re-verify the stack from scratch.

Each of these accepts the same general fix: match the container/wheel
combination to CUDA 13 and SM121, don't fight the ABI. The rest of this
skill walks through how, section by section, starting with the
container-vs-pip decision below.

## Container-First Rule

Quick decision, before the detail below:

- Standard training/inference work → NGC PyTorch container.
- Unsloth-centric fine-tuning → Unsloth container.
- Neither fits (custom system package, local IDE interpreter) → bare pip,
  following the exact sequence further down.

Default to a container. Use `nvcr.io/nvidia/pytorch:25.11-py3` as the base
for general work, or `unsloth/unsloth:dgxspark-latest` for Unsloth-centric
fine-tuning. Treat bare pip as the exception, reached for only when a
container genuinely can't fit the workflow — a custom system package, an
IDE that expects a local interpreter, and so on.

Minimal invocations for each look like this (full flag rationale and
volume mounts for `finetuning/` run dirs: `references/container-workflow.md`):

```bash
docker run --runtime=nvidia --gpus all -it --rm \
  nvcr.io/nvidia/pytorch:25.11-py3
```

```bash
docker run --runtime=nvidia --gpus all -it --rm \
  unsloth/unsloth:dgxspark-latest
```

Pick the NGC image for general training/inference work, and the Unsloth
image specifically when the run is Unsloth-centric — it ships the pinned
Triton/xformers/transformers combination already validated for that path,
so there's nothing extra to configure.

The reason for the container-first stance is pinning, not convenience.
Triton, xformers, and transformers versions interact narrowly with GB10's
SM121 target and the CUDA 13 toolchain; a container locks all of them
together against a combination that's already been validated on this
hardware. A bare pip environment leaves that resolution to you, one broken
import at a time.

When bare pip is warranted, follow the NVIDIA playbook's install sequence
verbatim and in order:

```bash
pip install transformers peft hf_transfer "datasets==4.3.0" "trl==0.26.1"
pip install --no-deps unsloth unsloth_zoo bitsandbytes
```

The second command's `--no-deps` flag is not optional — letting pip
re-resolve Unsloth's dependency tree on aarch64 is a common way to pull in
an incompatible torch or triton build.

Pull a fresh image tag when a new blessed release is announced. Rebuild
locally from one of the two bases only when a project needs an extra
system package layered in — not to "upgrade" a component the image
already pins. Details on both paths: `references/container-workflow.md`.

## The ABI Rule

The single most common failure on Spark is a CUDA 12/13 ABI mismatch: a
wheel built against `libcudart.so.12` loaded on a system that only has
`libcudart.so.13`. The import usually succeeds; the failure surfaces later
as a missing-symbol error or a segfault that doesn't obviously point at
CUDA.

Fix: pull wheels from `download.pytorch.org/whl/cu130` (the cu130-tagged
aarch64 builds), or use one of the containers above, which already carry a
matched build. Before chasing a stack trace that mentions a CUDA symbol,
check which CUDA tag the installed wheel was built against:

```bash
pip show torch | grep -i version
```

If that output doesn't say `cu130` (or a container-supplied equivalent),
the ABI mismatch is the first thing to fix, not the last.

Typical symptoms of this mismatch, so it's recognizable next time:

- `ImportError: undefined symbol` referencing a CUDA runtime function.
- A segfault on the very first `.cuda()` call, with no Python traceback
  pointing anywhere useful.
- A wheel that installs cleanly with no warnings, then fails at import
  time — pip's dependency resolver doesn't check CUDA ABI compatibility,
  only package version constraints.
- Inconsistent behavior between two otherwise-identical environments —
  usually one has a cu130 wheel and the other a cu121/cu124 leftover from
  an earlier install.

The fix is the same regardless of which symptom shows up: match the
wheel's CUDA tag to the system, or use a container that already does.

## Component Quick Table

Condensed status for the components most likely to come up. Full table
with wheel URLs, build flags, and the sm_121 vs sm_121a distinction: see
`references/stack-matrix.md`.

| Component | Status |
|---|---|
| PyTorch | ✅ official cu130 aarch64 wheels |
| bitsandbytes | ✅ works out of the box |
| Triton | ✅ needs the `TRITON_PTXAS_PATH` parameter set |
| flash-attn | ❌ skip — no sm_121 kernels; use PyTorch SDPA instead |
| xformers | source build only (`TORCH_CUDA_ARCH_LIST=12.1`) |
| vLLM | nightly wheels only |
| TransformerEngine / NVFP4 train | container-only |

Everything not in this table — Unsloth itself, Axolotl, TRL, PEFT —
installs cleanly through the container-first path above. Only the
components listed here need special handling, which is why they're
called out separately instead of buried in a general dependency list.

## Verification Commands

Confirm the environment can actually see the GPU before running anything
expensive:

```python
import torch
print(torch.cuda.is_available(), torch.version.cuda)
```

This call returns two values and produces output in this exact format
(`<bool> <cuda-version>`):

```text
True 13.0
```

If it prints `False` instead, don't assume the GPU is absent — Spark has
known GPU-detection false negatives on bare pip installs (a
torchcodec/driver interaction is the usual culprit). Check with the driver
directly before spending time debugging the Python side:

```bash
nvidia-smi
```

If `nvidia-smi` shows the GPU but PyTorch still reports `False`, the
problem is almost certainly the ABI mismatch above, not a missing driver.

Run this same check right after the container starts, before installing
any project-specific packages on top of it. That way, a failure clearly
points at the base image rather than something layered in afterward —
the two failure modes need different fixes, and conflating them wastes
time.

## Fast Path Recap

For a repeat setup, skip straight to the order of operations:

1. Pull the right container (Container-First Rule).
2. Run it with `--runtime=nvidia --gpus all`, matching the commands above.
3. Run the verification commands before installing anything
   project-specific.
4. If verification fails, check the ABI Rule first.
5. Consult the Component Quick Table before assuming a broken framework
   install is unique to this project.
6. Escalate to the two companion skills linked below once the environment
   itself is confirmed healthy.

## Next Steps

A verified environment is only the starting point — long training runs
surface a different class of problem once the stack itself is working.

See also: `spark-training-gotchas` for failure preflights before a
training run, and `spark-memory-thermal-ops` for unified-memory OOMs and
thermal throttling during long ones.
