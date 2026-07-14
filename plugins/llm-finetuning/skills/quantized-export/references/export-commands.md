Last verified: 2026-07-14

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

## llama.cpp: Build, Convert, imatrix + Quantize

Verified against llama.cpp commit `b1-6e52db5`,
built from source on aarch64/GB10. Three corrections
against older guidance floating around for this
tool, found the hard way:

**Build with the default configuration — do not
try to build "just the tools you need."**
`cmake --build --target llama-cli llama-quantize`
fails ("No rule to make target"), and configuring
with `-DLLAMA_BUILD_EXAMPLES=OFF
-DLLAMA_BUILD_SERVER=OFF` breaks the default build
outright — the unified `llama` app links against
`llama-cli-impl`/`llama-server-impl` libraries those
flags disable. Full default build is cheap enough
(~2 min at `-j20` on a 20-core aarch64 box) that a
minimal-target build isn't worth the breakage risk:

```bash
cmake -B build
cmake --build build --config Release -j"$(nproc)"
```

**Converter prerequisites — neither is optional:**

```bash
pip install ./gguf-py
pip install sentencepiece
```

`convert_hf_to_gguf.py` needs the repo's own
`gguf-py` package installed, and imports
`sentencepiece` unconditionally on the tokenizer
path — even for a BPE-tokenizer model that the
converter otherwise handles natively.

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

**Raw-prompt smoke testing: use `llama-completion`,
not `llama-cli`.** Current `llama-cli` is a
chat-first UI — it re-templates `-p` text as a
conversation turn and, at the end of generation,
drops into an interactive `> ` prompt loop
regardless of `-no-cnv` (the flag still parses and
appears in `--help`, but does nothing the newer
`--single-turn` flag doesn't already own; with
stdin closed, a script invoking `llama-cli -no-cnv`
hangs indefinitely instead of exiting). The raw,
non-chat completion behavior a smoke test needs
lives in a separate binary:

```bash
./llama-completion \
    -m "$GGUF_DIR/model-Q4_K_M.gguf" \
    -p "$(cat prompt.txt)" \
    -n 512 --temp 0 --seed 0
```

`llama-completion` exits after generating, does not
re-template the prompt, and does not require a
`-no-cnv`/`--single-turn` flag at all — it never
enters chat mode in the first place.

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
    --port 8000 > vllm-fp8-load.log 2>&1 &
VLLM_PID=$!

# Bounded wait for readiness — up to 60s, not a blind sleep.
ready=0
for _ in $(seq 1 30); do
    if curl -sf http://localhost:8000/v1/models | grep -q checkpoint-fp8; then
        ready=1
        break
    fi
    sleep 2
done

if [ "$ready" -ne 1 ]; then
    echo "FAILED: endpoint did not come up within 60s"
    kill "$VLLM_PID" 2>/dev/null
    exit 1
fi

# Endpoint liveness alone does not prove FP8 loaded — vLLM can
# silently fall back to bf16. Confirm the actual dtype from the
# startup log before trusting the deployment.
if grep -qi 'fp8' vllm-fp8-load.log; then
    echo "FP8 endpoint up and confirmed FP8 in startup log"
else
    echo "FAILED: endpoint up but startup log does not confirm FP8 (possible silent bf16 fallback)"
    kill "$VLLM_PID" 2>/dev/null
    exit 1
fi
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
structure.

**The comparison mode depends on whether the export
is lossless or lossy — pick before running:**

- **Lossless exports** (fp16/bf16 merge, no
  quantization) — byte/string match
  (`pre.strip() == post.strip()`) is the correct
  gate. Any divergence here is a bug, full stop.
- **Lossy exports** (any quantized format — Q4_K_M,
  AWQ INT4, FP8) — byte match is **unmeetable by
  design**, not a signal of a bug. A quantized
  checkpoint legitimately perturbs logits, so
  0/5 exact matches with 5/5 schema-valid,
  on-template outputs is the *expected healthy*
  result for a lossy export. **The gate for a lossy
  export is the task grader's verdict**, per
  `SKILL.md`'s Workload Overrides section — run
  each golden's actual grader (from
  `eval-harness-first`) against both the pre- and
  post-export output, and diff verdicts, not text.
  A byte-match diff is still worth logging for
  triage (it tells you *how much* the output
  changed), but it must never gate a lossy export by
  itself.

```python
import json
import sys

# Deterministic decoding, persisted and reused for both the
# pre-export run (that produced pre-export-outputs.jsonl) and the
# post-export run below — greedy (temperature 0) with a fixed seed.
# Any drift in these settings between the two runs can flip an
# otherwise-valid export into a spurious mismatch.
SMOKE_TEST_GENERATION_KWARGS = {"temperature": 0, "seed": 0, "max_new_tokens": 512}

def load_pre_export_outputs(path: str) -> dict:
    """goldens.jsonl-keyed pre-export generations,
    produced from the promoted checkpoint before any
    quantization/export step, using
    SMOKE_TEST_GENERATION_KWARGS."""
    with open(path) as f:
        return {row["task_id"]: row["output"] for row in map(json.loads, f)}

def load_goldens(path: str, n: int = 5) -> list:
    with open(path) as f:
        rows = [json.loads(line) for line in f]
    return rows[:n]

def load_exported_model(export_path: str):
    """Load in the ACTUAL target runtime — vLLM,
    llama.cpp, or the AWQ loader. Never substitute
    a different framework than production here."""
    raise NotImplementedError("wire to target runtime")

def generate(model, prompt: str, **generation_kwargs) -> str:
    raise NotImplementedError("wire to target runtime")

def grade(task_id: str, output: str) -> bool:
    """Run the golden's actual task grader (from
    eval-harness-first) against a single output.
    Wire to the real grader module — never stub this
    with a byte-match; that defeats the point of the
    lossy-export path below."""
    raise NotImplementedError("wire to eval-harness-first's grader for this golden")

def diff_report(golden_id: str, pre: str, post: str, *, lossless: bool) -> dict:
    """lossless=True: gate on byte/string match.
    lossless=False (any quantized format): gate on
    grader verdict agreement — byte match is expected
    to fail for a healthy lossy export, so it is
    recorded for triage only, never as `match`."""
    byte_match = pre.strip() == post.strip()
    if lossless:
        match = byte_match
    else:
        match = grade(golden_id, pre) == grade(golden_id, post)
    return {
        "task_id": golden_id,
        "match": match,
        "byte_match": byte_match,
        "pre_export": pre,
        "post_export": post,
    }

def main(export_path: str, goldens_path: str, pre_export_path: str, *, lossless: bool):
    goldens = load_goldens(goldens_path, n=5)
    pre_outputs = load_pre_export_outputs(pre_export_path)
    model = load_exported_model(export_path)

    reports = []
    for row in goldens:
        post = generate(model, row["prompt"], **SMOKE_TEST_GENERATION_KWARGS)
        pre = pre_outputs[row["task_id"]]
        reports.append(diff_report(row["task_id"], pre, post, lossless=lossless))

    failures = [r for r in reports if not r["match"]]
    print(json.dumps({"total": len(reports), "failures": len(failures),
                       "mode": "byte-match" if lossless else "graded-verdict"}, indent=2))
    for r in failures:
        print(f"MISMATCH {r['task_id']} (byte_match={r['byte_match']}):")
        print(f"  pre : {r['pre_export'][:200]}")
        print(f"  post: {r['post_export'][:200]}")

    # non-zero exit on any mismatch — this script
    # gates the export, it does not just report on it
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    # lossless=True only for an unquantized fp16/bf16 merge;
    # every quantized format (Q4_K_M, AWQ, FP8, ...) is lossless=False
    main(*sys.argv[1:4], lossless=False)
```

A failing run's mismatches are the diagnostic
signal — read the `pre`/`post` pair before
re-exporting: garbled or run-on text points to
a template mismatch, fluent-but-wrong-answer
text points to a quantized `lm_head`, per the
failure signatures in `SKILL.md`'s Smoke Test
section. For a lossy export, `byte_match=False`
on a passing (`match=True`) row is expected and
not itself a failure signature — only a grader
verdict flip is.
