Last verified: 2026-07-13

# Export Commands

Complete command sequences for every format on
the `SKILL.md` Format Map, plus the smoke-test
script skeleton. `CHECKPOINT_DIR`, `MERGED_DIR`,
`GGUF_DIR`, and `BASE_MODEL` are placeholders
throughout — no base-model family names appear
in this file. Fill each with the promoted
checkpoint's actual path/repo before running.

## Unsloth: Merged Safetensors

Merged export folds the LoRA adapter into the
base weights — use this path when the serving
stack needs a single self-contained artifact
(see `SKILL.md`'s merged-vs-LoRA-only tradeoff).

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=CHECKPOINT_DIR,
    max_seq_length=4096,
    load_in_4bit=False,  # load full precision before merge
)

# fp16/bf16 merged export — safe default, no quant loss at this step
model.save_pretrained_merged(
    MERGED_DIR,
    tokenizer,
    save_method="merged_16bit",
)

# 4-bit merged export — only if the serving stack
# consumes bitsandbytes 4-bit directly (rare; most
# deployments quantize downstream instead — see the
# AWQ and GGUF sections below)
model.save_pretrained_merged(
    MERGED_DIR + "-4bit",
    tokenizer,
    save_method="merged_4bit",
)
```

## Unsloth: GGUF with Quant Method

Unsloth can drive llama.cpp's converter and
quantizer directly. The `quantization_method`
argument accepts a list — pass every quant
level needed for target devices in one call to
avoid re-converting from safetensors each time:

```python
model.save_pretrained_gguf(
    GGUF_DIR,
    tokenizer,
    quantization_method=["q4_k_m", "q8_0"],
)
```

`q4_k_m` is the edge default from the Format
Map; `q8_0` is a higher-fidelity fallback for
validating that a quality regression traces to
the quant level rather than the conversion
itself — export both when in doubt, compare
smoke-test diffs, then ship only the one
actually deployed.

## llama.cpp: Manual imatrix + quantize

Use this path when converting outside Unsloth
(a merged safetensors export from another
framework) or when a custom calibration set is
required for the imatrix:

```bash
# 1. Convert HF safetensors to GGUF (f16, no quant yet)
python convert_hf_to_gguf.py \
    "$MERGED_DIR" \
    --outfile "$GGUF_DIR/model-f16.gguf" \
    --outtype f16

# 2. Generate the importance matrix from a calibration
#    corpus — domain-representative text, several
#    hundred KB minimum; a generic corpus (e.g. the
#    llama.cpp wikitext sample) works if no
#    domain corpus is available
./llama-imatrix \
    -m "$GGUF_DIR/model-f16.gguf" \
    -f calibration-corpus.txt \
    -o "$GGUF_DIR/imatrix.dat" \
    --chunks 200

# 3. Quantize using the imatrix — Q4_K_M is the
#    edge/llama.cpp default from the Format Map
./llama-quantize \
    --imatrix "$GGUF_DIR/imatrix.dat" \
    "$GGUF_DIR/model-f16.gguf" \
    "$GGUF_DIR/model-Q4_K_M.gguf" \
    Q4_K_M
```

Skipping the imatrix step (quantizing straight
from f16) works but leaves accuracy on the
table at Q4_K_M — the imatrix step is cheap
relative to the training run that produced the
checkpoint and should not be skipped for a
production export.

## AWQ Export Sketch

AWQ targets older GPU generations per the
Format Map. Sketch using the `autoawq` package
against the merged safetensors directory:

```python
from awq import AutoAWQForCausalLM
from transformers import AutoTokenizer

quant_config = {
    "zero_point": True,
    "q_group_size": 128,
    "w_bit": 4,
    "version": "GEMM",
}

model = AutoAWQForCausalLM.from_pretrained(MERGED_DIR)
tokenizer = AutoTokenizer.from_pretrained(MERGED_DIR)

# calibration data: a few hundred domain-representative
# samples; reuses the same calibration-corpus concept
# as the llama.cpp imatrix step above
model.quantize(tokenizer, quant_config=quant_config)
model.save_quantized(MERGED_DIR + "-awq")
tokenizer.save_pretrained(MERGED_DIR + "-awq")
```

Do not run this path on a checkpoint destined
for a long-context, code, or math workload —
per `SKILL.md`'s Workload Overrides, stay on
FP8/W8A8 for those regardless of target GPU
generation.

## vLLM: FP8 Load Check

FP8 is the Format Map default on Hopper-class
GPUs and newer. Confirm the serving stack
actually loads the export in FP8 before
treating the export as done — a silent
fallback to bf16 defeats the memory savings
without erroring:

```bash
vllm serve "$MERGED_DIR" \
    --quantization fp8 \
    --served-model-name checkpoint-fp8 \
    --port 8000 &

sleep 20
curl -s http://localhost:8000/v1/models | grep -q checkpoint-fp8 \
    && echo "FP8 endpoint up" \
    || echo "FAILED: endpoint did not come up"

# confirm the loaded dtype in the server startup log,
# not just endpoint liveness — grep for "fp8" near the
# model-loading lines before trusting the deployment
```

Use a nightly vLLM build for GB10/SM121
targets per `SKILL.md`'s Spark note — the
SM121 fix for FP8 serving landed in the
nightly channel, not yet in a stable release
as of the date at the top of this file.

## Smoke-Test Script Skeleton

Load → generate on goldens → diff report, per
`SKILL.md`'s mandatory Smoke Test section. This
skeleton is runtime-agnostic — swap the `load()`
and `generate()` bodies for the target stack
(vLLM client, llama.cpp Python bindings, AWQ
loader) without changing the surrounding
structure:

```python
import json
import sys

def load_pre_export_outputs(path: str) -> dict:
    """goldens.jsonl-keyed pre-export generations,
    produced from the promoted checkpoint before
    any quantization/export step."""
    with open(path) as f:
        return {row["id"]: row["output"] for row in map(json.loads, f)}

def load_goldens(path: str, n: int = 5) -> list:
    with open(path) as f:
        rows = [json.loads(line) for line in f]
    return rows[:n]

def load_exported_model(export_path: str):
    """Load in the ACTUAL target runtime — vLLM,
    llama.cpp, or the AWQ loader. Never substitute
    a different framework than production here."""
    raise NotImplementedError("wire to target runtime")

def generate(model, prompt: str) -> str:
    raise NotImplementedError("wire to target runtime")

def diff_report(golden_id: str, pre: str, post: str) -> dict:
    return {
        "id": golden_id,
        "match": pre.strip() == post.strip(),
        "pre_export": pre,
        "post_export": post,
    }

def main(export_path: str, goldens_path: str, pre_export_path: str):
    goldens = load_goldens(goldens_path, n=5)
    pre_outputs = load_pre_export_outputs(pre_export_path)
    model = load_exported_model(export_path)

    reports = []
    for row in goldens:
        post = generate(model, row["prompt"])
        pre = pre_outputs[row["id"]]
        reports.append(diff_report(row["id"], pre, post))

    failures = [r for r in reports if not r["match"]]
    print(json.dumps({"total": len(reports), "failures": len(failures)}, indent=2))
    for r in failures:
        print(f"MISMATCH {r['id']}:")
        print(f"  pre : {r['pre_export'][:200]}")
        print(f"  post: {r['post_export'][:200]}")

    # non-zero exit on any mismatch — this script
    # gates the export, it does not just report on it
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main(*sys.argv[1:4])
```

A failing run's mismatches are the diagnostic
signal — read the `pre`/`post` pair before
re-exporting: garbled or run-on text points to
a template mismatch, fluent-but-wrong-answer
text points to a quantized `lm_head`, per the
failure signatures in `SKILL.md`'s Smoke Test
section.
