Last verified: 2026-07-13 — refresh when CUDA, PyTorch, or Unsloth major versions change.

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
| Unsloth | ✅ (container preferred) | Official Docker image `unsloth/unsloth:dgxspark-latest`, or the NVIDIA playbook pip sequence (see `SKILL.md`). Bare pip installs have hit torchcodec and GPU-detection gotchas. |
| Axolotl / TRL / PEFT | ✅ | Standard install, no special handling needed. |
| LLaMA-Factory / NeMo | fragile / in progress | Known to be unreliable on this platform as of this writing; expect breakage and check upstream issues before depending on either for a run. |

## sm_121 vs sm_121a

GB10's GPU identifies as `sm_121`. Some newer kernel features — notably NVFP4's native `cvt.e2m1x2` conversion instruction — require code compiled for `sm_121a`, a superset target, not plain `sm_121`. If NVFP4 inference is ~32% slower than FP8 on this hardware, this is why: the kernel likely wasn't compiled with the `a` variant. Check the build flags of whatever wheel or container you're using before assuming the hardware itself is the bottleneck.

## Canonical resources

- `github.com/NVIDIA/dgx-spark-playbooks`
- `build.nvidia.com/spark/unsloth`
- `github.com/natolambert/dgx-spark-setup`
- `github.com/albond/DGX_Spark_Unsloth_Lossless_Speedup`
- `github.com/NvMayMay/nvfp4-lora-spark`

Official playbooks have shipped broken before. Check each repo's recent issues before starting a long run, not after it fails.
