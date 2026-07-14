Last verified: 2026-07-13 — refresh when CUDA, PyTorch, or the
DGX Spark stack ships a new major version.

Runnable check commands for each gotcha in `SKILL.md`, keyed by
G-number. Run the check before assuming the gotcha is the cause;
each command is safe to run read-only unless noted.

## G1: CUDA 12/13 ABI Mismatch

```bash
python3 -c "import torch; print(torch.version.cuda)"
python -c "import ctypes; ctypes.CDLL('libcudart.so.13')"
ldconfig -p | grep libcudart
```

`torch.version.cuda` is the authoritative signal: it should
report `13.x`. Don't rely on `pip show torch | grep cu130` — NGC
container builds (e.g. `nvcr.io/nvidia/pytorch:25.11-py3`) build
torch internally against CUDA 13 with no `+cu130` wheel tag, so
the absence of a `cu130` tag in `pip show` output is NOT a
failure by itself on those containers. The `ctypes` load
confirms `libcudart.so.13` is actually present on the system; if
it raises `OSError`, the driver/runtime install is the problem,
not the wheel. `ldconfig -p` lists every CUDA runtime version
currently registered — a `libcudart.so.12` entry alongside
`libcudart.so.13` is a common leftover from an earlier install
and a likely ABI-mismatch source.

## G2: flash-attn Absent

```bash
python -c "import flash_attn" 2>&1 | tail -5
python -c "import torch; print(torch.backends.cuda.flash_sdp_enabled())"
```

The first command is expected to fail on Spark — that's the
point of this check, confirming no training code path silently
depends on flash-attn. The second confirms PyTorch's SDPA
backend has flash-style kernels enabled as the fallback.

## G3: UMA OOM Below 128GB

```bash
free -g
cat /proc/meminfo | grep -i huge
```

Read real memory pressure from `free -g`, not `nvidia-smi` —
unified memory means CUDA allocations and host RAM share one
pool, and `nvidia-smi` only reports the CUDA side. If `free -g`
shows most of the 128GB consumed while a load is failing,
reclaim it:

```bash
sync
echo 3 > /proc/sys/vm/drop_caches
```

This needs root and flushes the page cache system-wide — every
process on the box loses cached file reads, not just the
training job. Run it between runs when memory looks pinned by
stale mmap'd pages, not as a routine step during training.

## G4: Thermal Throttling

```bash
nvidia-smi --query-gpu=temperature.gpu,power.draw --format=csv -l 5
```

Sampling loop (`-l 5` = every 5 seconds); let it run for at
least 10–15 minutes on a representative workload before judging.
Rated power is 240W; if draw plateaus around 100W while
temperature keeps climbing or has already plateaued high, the
box is throttling. A rising temperature with power still near
peak is not yet a throttle event — keep watching. Interrupt with
Ctrl-C when done; this does not need root.

## G5: Bandwidth Ceiling

**Intrusive, unlike the other checks in this file — do not run
against an active workload.** It allocates ~4GB on a UMA system
where GPU and host memory share one pool, and repeatedly clones
that tensor. Run only on an idle host; a box with another job
already using most of its 128GB headroom can OOM that job.

```bash
python -c "
import torch, time
x = torch.randn(1_000_000_000, device='cuda', dtype=torch.float32)
torch.cuda.synchronize()
t0 = time.time()
for _ in range(20):
    y = x.clone()
torch.cuda.synchronize()
dt = time.time() - t0
gbps = (x.numel() * 4 * 2 * 20) / dt / 1e9
print(f'{gbps:.1f} GB/s')
del x, y
torch.cuda.empty_cache()
"
```

Expect roughly 180–192 GB/s, not the 273 GB/s spec figure. If a
throughput plan assumed the spec number, revise it against this
measured range before committing to a schedule.

## G6: Global UMA Resource Contention

```bash
nvidia-smi
ps aux | grep -E "vllm|ollama|python.*train" | grep -v grep
```

List every GPU-resident process before starting a long run.
`nvidia-smi` shows per-process memory; the `ps` filter catches
inference servers (vLLM, Ollama) that may not show up clearly in
`nvidia-smi` output on unified memory. Stop unrelated servers
before a run that needs the full 128GB pool.

## G7: NVFP4 Slower Than FP8 on SM121

```bash
python -c "import torch; print(torch.cuda.get_device_capability())"
```

Expect `(12, 1)` on GB10 — this confirms SM121. SM121 lacks a
native `cvt.e2m1x2` conversion path, so NVFP4 kernels not
compiled for the `sm_121a` target fall back to a slower path,
roughly 32% behind FP8. Check the kernel build's target arch
(often `TORCH_CUDA_ARCH_LIST` or a similar build flag) before
assuming NVFP4 is the faster choice on this hardware.

## G8: Stale Official Playbooks

```bash
gh issue list --repo NVIDIA/dgx-spark-playbooks --state open --limit 20
```

Requires the `gh` CLI authenticated, or substitute a browser
visit to the same URL. Scan open issues for the specific
playbook and command being followed before trusting it verbatim
for a long or expensive run.

## G9: Container-First, Not Bare Pip

```bash
if [ -f /.dockerenv ] || [ -f /run/.containerenv ]; then
  echo "in container (marker file)"
elif grep -qE '(docker|containerd|kubepods)' /proc/1/cgroup 2>/dev/null; then
  echo "in container (cgroup marker)"
else
  echo "unknown — no container marker matched, this does not prove a bare host"
fi
pip list 2>/dev/null | grep -E "^(torch|triton|xformers|transformers) "
```

The first block checks Docker's `/.dockerenv` and Podman's
`/run/.containerenv` marker files, then falls back to a
cgroup-string check — a single `grep docker /proc/1/cgroup` alone
is not reliable: cgroup v2 layouts and some runtimes/namespaces
hide the runtime name, so a failed match is "unknown," never proof
of a bare host. The second command lists the versions actually
installed — compare against the pinned set in an NGC or Unsloth
image if running bare pip, to catch drift early rather than at
import time.

## G10: Dual-Spark Is DDP/FSDP Only

```bash
python -c "
import os
print('WORLD_SIZE:', os.environ.get('WORLD_SIZE'))
print('parallelism strategy check: confirm config uses DDP or FSDP, not TP/tensor_parallel')
"
rg -l --iglob '*.yaml' --iglob '*.yml' -e 'tensor_parallel|tp_size|tensor-parallel' . \
  || grep -rlE "tensor_parallel|tp_size|tensor-parallel" --include='*.yaml' --include='*.yml' .
```

Search recursively, not just the current directory — a
non-recursive `*.yaml *.yml` glob misses nested configs, and a
redirected/suppressed error there reads as "no TP configuration"
when it may just be "wrong directory." If the workload's config
path is already known, pass it explicitly instead of searching.
Any match on a two-Spark job is a configuration error — switch to
DDP or FSDP before launching; TP is not viable across the
ConnectX-7 link on this hardware.
