Last verified: 2026-07-14 — refresh when CUDA, PyTorch, or Unsloth major versions change.

# Spark Stack Matrix

Full component-by-component status for the ML training/inference stack on DGX Spark (GB10, SM121, aarch64, CUDA 13). This is the detail table behind the "Component Quick Table" in `SKILL.md`.

| Component | Status | Notes |
|---|---|---|
| PyTorch (cu130, aarch64) | ✅ | Official wheels at `download.pytorch.org/whl/cu130`. Matches the system CUDA 13 ABI — see the ABI Rule in `SKILL.md`. |
| bitsandbytes | ✅ | 0.48+ works out of the box. |
| Triton | ✅ (with env var) | Needs `TRITON_PTXAS_PATH=/usr/local/cuda/bin/ptxas` set, or kernel compilation fails to find `ptxas`. |
| flash-attn | ❌ skip | No sm_121 kernels shipped or buildable yet. PyTorch's SDPA backend is faster on this hardware anyway — don't spend time chasing a flash-attn build. |
| xformers | source build only | No prebuilt aarch64/SM121 wheel. Build with `TORCH_CUDA_ARCH_LIST=12.1` set, or the build targets the wrong architecture and either fails or silently produces non-functional kernels. |
| vLLM | nightly wheels only | Use `wheels.vllm.ai/nightly/cu130`. The SM121 fix landed in the nightly channel around 2026-06; stable/release wheels predate it. |
| TransformerEngine / NVFP4 training | container-only | Not practical via bare pip; use the NGC PyTorch container. `NVFP4BlockScaling` targets SM100 — treat SM121 support as caveated, not guaranteed. |
| Unsloth | ✅ (container preferred) | Official Docker image `unsloth/unsloth:dgxspark-latest` (a moving tag — resolve and pin its digest for reproducible/CI use, see `references/container-workflow.md`), or the NVIDIA playbook pip sequence (see `SKILL.md`). Bare pip installs have hit torchcodec and GPU-detection gotchas. |
| Axolotl / TRL / PEFT | ✅ | Standard install, no special handling needed. |
| LLaMA-Factory / NeMo | fragile / in progress | Known to be unreliable on this platform as of this writing; expect breakage and check upstream issues before depending on either for a run. |

## Known-Good Version Matrix (Dated)

`SKILL.md`'s bare-pip sequence pins `datasets`/`trl` explicitly
for a reason: an unpinned `pip install transformers peft
hf_transfer datasets trl accelerate` resolves current PyPI
versions of `transformers`/`trl`/`datasets` that sit well
outside what a given Unsloth release declares support for — pip
installs them anyway and only warns after the fact. The
combination below was confirmed working end-to-end (bf16 LoRA
load + attach + a full SFT run) on `nvcr.io/nvidia/pytorch:25.09-py3`
as of the date above; treat it as a dated snapshot to re-verify,
not a permanent pin:

| Package | Verified-working version |
|---|---|
| `transformers` | 5.13.1 |
| `trl` | 1.8.0 |
| `peft` | 0.19.1 |
| `datasets` | 4.3.0 (pin as-is; not re-verified independently of the combination above) |
| `unsloth` / `unsloth_zoo` | 2026.7.2 |
| `torchao` | 0.17.0 (pure-Python wheel; NGC base image ships 0.13.0+git, too old — `pip install -U torchao` after the Unsloth line) |
| `bitsandbytes` | 0.49.2 |
| `hf_transfer` | 0.1.9 (current stable; see the deprecation note below before relying on it) |

If a bare-pip install lands on a different combination than
this table (pip resolver drift is expected as new releases
ship), re-run the load+LoRA-attach smoke test in `SKILL.md`'s
Verification Commands before trusting the environment, and
check `gh issue list --repo NVIDIA/dgx-spark-playbooks` for a
version-skew report matching the symptom before assuming it's
novel.

**`HF_HUB_ENABLE_HF_TRANSFER` is deprecated on `huggingface_hub`
1.23+.** Setting it now only produces `FutureWarning: The
HF_HUB_ENABLE_HF_TRANSFER environment variable is deprecated ...
Please use HF_XET_HIGH_PERFORMANCE instead`, and downloads route
through Xet rather than hf_transfer regardless. This is cosmetic
(downloads still succeed, and fast) on current `huggingface_hub`
— stale task instructions or older recipes that still reference
`hf_transfer`-based env setup should be read as intent ("make
downloads fast"), not a literal current-API requirement; set
`HF_XET_HIGH_PERFORMANCE=1` instead on `huggingface_hub` 1.23+.

## GPU-Detection False Negative: Per-Hypothesis Detail

The full discriminating check behind `SKILL.md`'s Verification
Commands hypothesis table, in the order to work through them:

1. **Runtime/flags.** If `docker run` was missing
   `--runtime=nvidia --gpus all`, `nvidia-smi` run *inside* the
   container fails or shows no devices even though the host sees
   the GPU fine. Fix: re-run with both flags.
2. **Device visibility.** `echo $CUDA_VISIBLE_DEVICES` — an
   empty string set explicitly (not merely unset) hides all
   devices from CUDA; a stale index (e.g. `1` on a single-GPU
   box) hides the only device present. Fix: `unset
   CUDA_VISIBLE_DEVICES` or set it to `0`.
3. **Permissions.** `ls -l /dev/nvidia*` — missing entries or a
   `Permission denied` on read means the container/user can't
   open the device nodes (common when running rootless or with a
   restrictive seccomp/AppArmor profile). Fix: match the host's
   device-cgroup rules, or don't run rootless for GPU workloads.
4. **CUDA init state.** A prior process that crashed mid-kernel
   can leave the driver's CUDA context wedged for that process
   tree. Retrying in a fresh shell or a freshly started container
   (not just a new Python process in the same shell) rules this
   out cheaply before assuming anything deeper is wrong.
5. **ABI mismatch.** The last hypothesis to check, not the
   first: `python3 -c "import torch; print(torch.version.cuda)"`
   not starting with `13` confirms a `libcudart.so.12`-linked
   wheel on a CUDA-13-only system — see the ABI Rule in
   `SKILL.md`. This is the only one of the five that a wheel
   reinstall actually fixes; reinstalling before ruling out 1-4
   wastes a cycle without changing the outcome if the real cause
   is a flag, an env var, or a permission.

A torchcodec/driver interaction is the most frequently reported
instance of (5) on this hardware specifically — see
`gh issue list --repo NVIDIA/dgx-spark-playbooks` for current
reports before assuming a novel cause.

## sm_121 vs sm_121a

GB10's GPU identifies as `sm_121`. Some newer kernel features — notably NVFP4's native `cvt.e2m1x2` conversion instruction — require code compiled for `sm_121a`, a superset target, not plain `sm_121`. If NVFP4 inference is ~32% slower than FP8 on this hardware, this is why: the kernel likely wasn't compiled with the `a` variant. Check the build flags of whatever wheel or container you're using before assuming the hardware itself is the bottleneck.

## Canonical resources

- `github.com/NVIDIA/dgx-spark-playbooks`
- `build.nvidia.com/spark/unsloth`
- `github.com/natolambert/dgx-spark-setup`
- `github.com/albond/DGX_Spark_Unsloth_Lossless_Speedup`
- `github.com/NvMayMay/nvfp4-lora-spark`

Official playbooks have shipped broken before. Check each repo's recent issues before starting a long run, not after it fails.
