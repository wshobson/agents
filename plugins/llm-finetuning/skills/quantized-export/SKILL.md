---
name: quantized-export
description: Export a promoted fine-tuned model in the right deployment format — merged safetensors, LoRA-only, GGUF with imatrix, or FP8. Use after a checkpoint passes promotion, when choosing a quantization format for a target device, or when an exported model fails its smoke test.
---

# Quantized Export

The last stop after `checkpoint-promotion`
hands off a `PROMOTE` verdict: a checkpoint
that cleared the four-stage gate still isn't
deployed until it's exported in the right
format for its target runtime and proven to
still work post-export. A `REJECT` verdict
never reaches this skill — export starts only
from a promoted checkpoint.

**Input:** a promoted checkpoint (or LoRA
adapter) plus the target deployment surface —
GPU class, serving stack, and whether
long-context/code/math workloads are in
scope.
**Output format:** an exported artifact in
the chosen format plus a smoke-test diff
report comparing 3–5 golden outputs
pre-export and post-export.

## Format Map

Pick format by hardware and deployment shape,
not by habit — the wrong pick either wastes
throughput headroom or breaks silently on
specific workloads (see Workload Overrides).

- **FP8 is the default on Hopper-class GPUs
  and newer.** It preserves near-bf16 quality
  at roughly half the memory, and it's the
  safe first choice whenever the target GPU
  supports it and no edge-device constraint
  applies.
- **AWQ INT4 targets older GPUs** that predate
  FP8 hardware support. **GPTQ is superseded
  for new deployments** — don't reach for it
  on a fresh export; AWQ has better accuracy
  retention at the same bit width and wider
  current tooling support.
- **GGUF with Q4_K_M quantization, built from
  an imatrix, is the edge/llama.cpp format.**
  Use it for local or CPU-adjacent
  deployment, not for GPU-serving
  throughput — it optimizes for footprint,
  not tokens/sec on a datacenter GPU.
- **NVFP4 is for Blackwell-at-scale
  deployments only — and explicitly NOT on
  GB10.** NVFP4 on SM121 (GB10) runs **~32%
  slower than FP8** because the hardware
  lacks a native `cvt.e2m1x2` path unless the
  kernel is compiled `sm_121a`. Choosing
  NVFP4 on a GB10 target is a regression, not
  an upgrade — pick FP8 there instead.
- **Merged vs. LoRA-only is a separate axis
  from quant format.** A merged export folds
  the adapter into the base weights: larger
  artifact, no base-model dependency at serve
  time. LoRA-only keeps the adapter separate:
  much smaller artifact, but the serving stack
  must load the exact same base model
  alongside it — a mismatched or
  wrong-revision base silently changes
  outputs. Pick merged when artifact
  portability matters more than storage; pick
  LoRA-only when disk footprint or multi-adapter
  serving matters more.

### Worked Picks

The core format-selection tradeoff, read as a
lookup table for common scenarios:

| Target | Workload | Format |
|---|---|---|
| Datacenter GPU | generic chat | FP8 |
| Datacenter GPU | long-context/code/math | FP8 or W8A8 — never INT4 |
| Older GPU generation | generic | AWQ INT4 |
| Edge device / laptop | llama.cpp serving | GGUF Q4_K_M + imatrix |
| GB10 | any workload | FP8 via vLLM nightly, or GGUF via llama.cpp locally — skip NVFP4 |

```yaml
# quick decision snippet — see the table above for the full map
hopper_or_newer: fp8
older_gpu: awq-int4
edge_llama_cpp: gguf-q4_k_m+imatrix
gb10_any_workload: fp8-vllm-nightly   # never nvfp4 on GB10
```

## Workload Overrides

The Format Map above is a default, not a rule
that survives every workload. **Long-context,
code, and math workloads break at INT4** —
quantization error compounds across long
sequences and precise token-level reasoning in
ways that don't show up on short, generic
prompts. For any of these three workload
classes, **stay on FP8 or W8A8** even if the
target hardware would otherwise justify INT4
on cost grounds.

- Don't validate this override with MMLU or
  similar broad-knowledge benchmarks — they
  don't stress the failure mode. **Measure
  with the actual task evals** — the goldens
  and graders from `eval-harness-first`, run
  through the exported artifact — because
  INT4 degradation on long-context, code, or
  math shows up as task-specific failures
  (dropped context, broken syntax, arithmetic
  errors) well before it moves a knowledge
  benchmark.
- If a task eval regresses after an INT4
  export on one of these three workload
  classes, the fix is switching format, not
  re-tuning the quantization recipe — AWQ
  and GPTQ variants at the same bit width
  share the same compounding-error failure
  mode on these workloads.

## The Smoke Test

Export bugs are silent at the file level — a
malformed export still produces a
loadable artifact, so file-existence checks
prove nothing. **The smoke test is
mandatory for every export, with no
exception for a format that "should just
work":**

1. **Load the exported artifact in its actual
   target runtime** — vLLM for FP8/AWQ,
   llama.cpp for GGUF, not a quick
   sanity load in a different framework than
   the one that will serve it in production.
2. **Run 3–5 golden prompts through it** —
   pull these from the same `eval/goldens.jsonl`
   `eval-harness-first` maintains, not a fresh
   ad hoc set.
3. **Compare each output against the
   pre-export generation** for the same
   prompt, same deterministic sampling
   settings — greedy decoding (temperature 0)
   and a fixed seed, persisted and reused
   between the pre- and post-export runs, not
   just nominally identical config. **For a
   lossless export, byte match is the gate —
   any diff is a bug.** For a **lossy**
   (quantized) export, byte match is expected
   to fail; the gate is task-grader verdict
   agreement instead — see
   `references/export-commands.md`'s
   Smoke-Test Script Skeleton.

Run this as a gate, not a manual check:

```bash
python smoke_test.py "$EXPORT_PATH" \
    eval/goldens.jsonl pre-export-outputs.jsonl
# non-zero exit on any pre/post mismatch
```

### Failure Signatures

What export bugs actually look like, not a
clean pass/fail flag:

- **Template mismatch** presents as garbled or
  run-on output — the chat template baked
  into the export doesn't match the one the
  checkpoint was trained and evaluated
  against, so turn boundaries or special
  tokens land in the wrong place.
- **Wrong quantization applied to `lm_head`**
  presents as off-template or semantically
  nonsensical output that still looks
  fluent — the output head lost precision it
  needed even though the rest of the network
  quantized cleanly.

Never ship an export that skipped this step —
a checkpoint's `PROMOTE` verdict says the
un-exported checkpoint is good; it says
nothing about the export pipeline. Re-run on
any quant-method or runtime version bump, not
only after the first export. Runnable command
sequences for every format plus the
smoke-test script skeleton:
`references/export-commands.md`.

## Related Skills

- `checkpoint-promotion` — the only valid
  upstream source for this skill. A checkpoint
  without a `PROMOTE` verdict doesn't reach
  export.
- `eval-harness-first` — owns the
  `eval/goldens.jsonl` this skill's smoke test
  draws its 3–5 prompts from, and the task
  evals the Workload Overrides section
  requires for long-context/code/math
  validation.
- `finetuning-method-selection` — its
  `references/model-catalog.md` is the place
  to check hardware-class assumptions (which
  GPU generations a base model targets) before
  picking a format off the Format Map above.

**Spark users:** on GB10, GGUF via llama.cpp
works well for local serving, and FP8 serving
via vLLM nightly builds is the other proven
path — NVFP4 is the one format to avoid there
(see the Format Map exception above). Once the
`dgx-spark-ops` plugin is installed, defer
Spark-specific serving and thermal questions to
its skills rather than re-deriving them here.
