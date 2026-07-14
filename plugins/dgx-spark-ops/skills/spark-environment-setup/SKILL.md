---
name: spark-environment-setup
description: Set up a working ML training/inference environment on NVIDIA DGX Spark (GB10, aarch64, CUDA 13). Use when installing PyTorch/Unsloth/TRL/vLLM on DGX Spark, hitting libcudart or wheel-ABI errors on aarch64, or choosing between NGC containers and bare pip installs.
---

# Spark Environment Setup

DGX Spark ships a GB10 Grace Blackwell chip: aarch64 CPU, SM121
GPU, 128GB unified memory, CUDA 13. This is a narrower and
younger platform than a standard x86 CUDA 12 box, so package
selection and ABI matching matter more than usual — the wheel
ecosystem for aarch64 + CUDA 13 is still filling in.

## When to Use This Skill

- Setting up a fresh Spark box for training or inference.
- Hitting an import error mentioning `libcudart`, a missing
  symbol, or a wheel that "installed fine but won't load."
- A framework install (PyTorch, Unsloth, TRL, vLLM, xformers)
  fails, hangs, or silently falls back to CPU.
- Deciding whether to use an NGC container or bare pip.
- Restoring a working setup after an OS reinstall or a
  base-image update, needing to re-verify from scratch.

Each of these accepts the same general fix: match the
container/wheel combination to CUDA 13 and SM121, don't fight
the ABI.

## Container-First Rule

Quick decision, before the detail below:

- Standard training/inference work → NGC PyTorch container.
- Unsloth-centric fine-tuning → Unsloth container (it ships
  the pinned Triton/xformers/transformers combination already
  validated for that path).
- Neither fits (custom system package, local IDE interpreter)
  → bare pip, following the exact sequence further down.

Default to a container. Use `nvcr.io/nvidia/pytorch:25.09-py3`
as the base for general work — the newest tag confirmed
working on this hardware; pull a newer blessed tag if one is
locally available and note any delta rather than hard-blocking
on `25.11-py3` specifically — or `unsloth/unsloth:dgxspark-latest`
for Unsloth-centric fine-tuning. Treat bare pip as the exception.

Minimal invocations (full flag rationale and volume mounts for
`finetuning/` run dirs: `references/container-workflow.md`):

```bash
docker run --runtime=nvidia --gpus all -it --rm \
  nvcr.io/nvidia/pytorch:25.09-py3
```

```bash
docker run --runtime=nvidia --gpus all -it --rm \
  unsloth/unsloth:dgxspark-latest
```

`dgxspark-latest` is a moving tag — pin it once resolved:
`docker inspect --format='{{index .RepoDigests 0}}' unsloth/unsloth:dgxspark-latest`,
then use that `@sha256:...` digest in place of the tag.

The reason for the container-first stance is pinning, not
convenience. Triton, xformers, and transformers versions
interact narrowly with GB10's SM121 target and CUDA 13; a
container locks all of them together against a combination
already validated on this hardware. Bare pip leaves that
resolution to you, one broken import at a time.

When bare pip is warranted, follow the NVIDIA playbook's
install sequence verbatim and in order:

```bash
pip install transformers peft hf_transfer "datasets==4.3.0" "trl==0.26.1"
pip install --no-deps unsloth unsloth_zoo bitsandbytes
pip install -U torchao
```

The second command's `--no-deps` flag is not optional —
letting pip re-resolve Unsloth's dependency tree on aarch64 is
a common way to pull in an incompatible torch or triton build.
The third line is not optional either: the NGC base image's
bundled `torchao` is too old for current `peft`'s LoRA-attach
path (`ImportError: ... torchao ... only versions above 0.16.0
are supported`) — a hard blocker, not a warning. The `==` pins
shown above are load-bearing, not illustrative: an unpinned
`pip install transformers peft hf_transfer datasets trl
accelerate` resolves current PyPI versions well outside what
this Unsloth release supports. Dated known-good version matrix:
`references/stack-matrix.md`.

Pull a fresh tag when a new blessed release is announced.
Rebuild locally from one of the two bases only when a project
needs an extra system package layered in — not to "upgrade" a
component the image already pins. Details on both paths:
`references/container-workflow.md`.

One more preflight: official DGX Spark playbooks have shipped
broken before. Check recent issues on
`github.com/NVIDIA/dgx-spark-playbooks` (and the other
resources in `references/stack-matrix.md`) before trusting a
recipe verbatim for a long run.

## The ABI Rule

The single most common failure on Spark is a CUDA 12/13 ABI
mismatch: a wheel built against `libcudart.so.12` loaded on a
system that only has `libcudart.so.13`. The install usually
succeeds; the failure surfaces later as a missing-symbol error
or a segfault that doesn't obviously point at CUDA.

Fix: pull wheels from `download.pytorch.org/whl/cu130` (the
cu130-tagged aarch64 builds), or use one of the containers
above, which already carry a matched build. Before chasing a
stack trace that mentions a CUDA symbol, check which CUDA tag
the installed wheel was built against:

```bash
python3 -c "import torch; print(torch.version.cuda)"
```

If that output doesn't start with `13`, the ABI mismatch is the
first thing to fix. NGC container builds (e.g.
`nvcr.io/nvidia/pytorch:25.09-py3`) build torch internally
against CUDA 13 with no `+cu130` wheel tag — `pip show torch`
won't say `cu130` there, and that absence alone is not a failure.

Typical symptoms:

- `ImportError: undefined symbol` referencing a CUDA runtime
  function.
- A segfault on the first `.cuda()` call, no useful traceback.
- A wheel that installs cleanly, then fails at import time —
  pip's resolver doesn't check CUDA ABI, only version constraints.
- Two "identical" environments behaving differently — usually one
  has a cu130 wheel, the other a cu121/cu124 leftover.

The fix is the same regardless of symptom: match the wheel's
CUDA tag to the system, or use a container that already does.

## Component Quick Table

Condensed status for the components most likely to come up.
Full table with wheel URLs, build flags, the sm_121 vs sm_121a
distinction, and the dated known-good version matrix:
`references/stack-matrix.md`.

| Component | Status |
|---|---|
| PyTorch | ✅ official cu130 aarch64 wheels |
| bitsandbytes | ✅ works out of the box |
| Triton | ✅ needs the `TRITON_PTXAS_PATH` parameter set |
| flash-attn | ❌ skip pip build; NGC bundles a working one — see `spark-training-gotchas` G2 |
| xformers | source build only (`TORCH_CUDA_ARCH_LIST=12.1`) |
| vLLM | nightly wheels only |
| TransformerEngine / NVFP4 train | container-only |

Everything else — Unsloth, Axolotl, TRL, PEFT — installs
cleanly through the container-first path above. LLaMA-Factory
and NeMo are fragile on Spark; check upstream issues first.

## Verification Commands

Confirm the environment can actually see the GPU before
running anything expensive:

```python
import torch
print(torch.cuda.is_available(), torch.version.cuda)
```

This call returns two values; the exact output format is one
line, `<bool> <cuda-version>`:

```text
True 13.0
```

If it prints `False` instead, don't assume the GPU is absent —
Spark has known GPU-detection false negatives on bare pip
installs (a torchcodec/driver interaction is the usual
culprit). Check with the driver directly first:

```bash
nvidia-smi
```

If `nvidia-smi` shows the GPU but PyTorch still reports
`False`, the problem is almost certainly the ABI mismatch
above, not a missing driver. Run this check right after the
container starts, before installing anything project-specific.

One more check: if Triton kernel compilation fails once
training starts, set
`TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas` and retry — see
`references/stack-matrix.md` for the full workaround list.

## Next Steps

A verified environment is only the starting point. See also:
`spark-training-gotchas` for failure preflights before a
training run, and `spark-memory-thermal-ops` for unified-memory
OOMs and thermal throttling during long ones.
