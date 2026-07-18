Last verified: 2026-07-14

# Grader Templates

Runnable examples for the four grader shapes named
in `SKILL.md`'s Graders section: schema-compliance,
exact-match with normalization, execution-based, and
LLM-judge. Every grader returns a binary pass/fail —
never a Likert score — per the plugin-wide rule.
Wire each one to exactly one failure bucket from
error analysis; don't blend buckets into one grader.

## Schema Compliance

For buckets where the failure mode is "the output
isn't shaped right" — tool calls, structured
extraction, JSON responses:

```python
import json
from jsonschema import validate, ValidationError

RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["action", "arguments"],
    "properties": {
        "action": {"type": "string"},
        "arguments": {"type": "object"},
    },
    "additionalProperties": False,
}

def grade_schema_compliance(completion: str) -> bool:
    """Binary pass/fail: does the completion parse as
    JSON and match RESPONSE_SCHEMA? Malformed JSON is
    an automatic fail, not an exception to handle
    upstream — the grader owns that decision.
    """
    try:
        payload = json.loads(completion)
    except json.JSONDecodeError:
        return False
    try:
        validate(instance=payload, schema=RESPONSE_SCHEMA)
    except ValidationError:
        return False
    return True
```

## Exact Match with Normalization

For buckets with a single ground-truth string (math
final answers, extracted entities, classification
labels) where naive `==` fails on formatting noise:

```python
import re

def normalize(text: str) -> str:
    """Lowercase, collapse whitespace, strip
    punctuation and surrounding markup — apply the
    identical normalization to both prediction and
    ground truth so neither side gets an unfair pass.
    """
    text = text.strip().lower()
    text = re.sub(r"[^\w\s.]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

def grade_exact_match(completion: str, ground_truth: str) -> bool:
    return normalize(completion) == normalize(ground_truth)
```

## Execution-Based

For buckets where correctness means "the code runs
and does the right thing" — the strongest signal
available when applicable, since it needs no
normalization or judgment call.

**WARNING — this grader executes model-generated
code and REQUIRES an isolated environment:** a
network-disabled container, gVisor/firejail, or a
dedicated CI sandbox, with **no secrets or
credentials in the environment** — no HF tokens,
experiment-tracker keys, cloud credentials, or SSH
keys. Never run it directly on a host holding
credentials. The timeout below protects grading-loop
liveness only — **it is NOT a security boundary**;
isolation comes entirely from `sandbox_cmd`.

```python
import logging
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

def grade_execution(completion: str, test_code: str, sandbox_cmd: list[str]) -> bool:
    """Write the completion plus a pytest test file to
    a scratch dir, run pytest via `sandbox_cmd`, and
    pass only on a clean exit code. Timeouts and
    non-zero exits are both failures — never treat a
    hung process as a pass by default.

    SECURITY: executes model-generated code. This
    function REQUIRES an isolation boundary — it does
    not run anything on the host by itself.

    `sandbox_cmd` (list[str], required) is a command
    prefix that wraps pytest in that boundary, e.g. a
    network-disabled, resource-capped Docker container:

        # sandbox_cmd = [
        #     "docker", "run", "--rm", "--network=none",
        #     "--memory=1g", "--cpus=1",
        #     "-v", f"{workdir}:/work:ro", "-w", "/work",
        #     "python:3.12-slim",
        # ]

    If `sandbox_cmd` is falsy, this function refuses to
    execute anything and returns False — it never falls
    back to running pytest on the host. The subprocess
    environment is scrubbed to a minimal PATH.
    """
    if not sandbox_cmd:
        logger.warning(
            "grade_execution: no sandbox boundary provided "
            "— refusing to execute model-generated code"
        )
        return False

    scrubbed_env = {"PATH": "/usr/bin:/bin"}
    with tempfile.TemporaryDirectory() as tmp:
        solution = Path(tmp) / "solution.py"
        test_file = Path(tmp) / "test_solution.py"
        solution.write_text(completion)
        test_file.write_text(test_code)
        try:
            result = subprocess.run(
                [*sandbox_cmd, "python", "-m", "pytest",
                 str(test_file), "-q"],
                cwd=tmp,
                capture_output=True,
                timeout=30,
                env=scrubbed_env,
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
```

## LLM-Judge Template

Only for buckets that failed the deterministic-first
check in `SKILL.md` — genuinely subjective criteria.
Few-shot slots and a binary output contract are both
mandatory; a judge without few-shot anchors drifts
toward its own prior instead of the calibrated
labels.

```python
JUDGE_PROMPT = """You are grading whether a response
meets the following criterion: {criterion}

Examples of PASS:
{few_shot_pass_examples}

Examples of FAIL:
{few_shot_fail_examples}

Now grade this response. Output exactly one word,
PASS or FAIL, with no other text.

Task: {task}
Response: {response}
Verdict:"""

class JudgeParseError(Exception):
    """Raised when the judge returns anything other than
    exactly PASS or FAIL — a transport or format failure,
    not a grading verdict. Never caught and coerced to
    False; the caller retries the judge call or routes the
    item to human review."""

def grade_llm_judge(task: str, response: str, criterion: str,
                     few_shot_pass: str, few_shot_fail: str,
                     judge_client) -> bool:
    prompt = JUDGE_PROMPT.format(
        criterion=criterion,
        few_shot_pass_examples=few_shot_pass,
        few_shot_fail_examples=few_shot_fail,
        task=task,
        response=response,
    )
    # judge_client is pinned to a fixed snapshot per
    # SKILL.md's Judge Calibration section — never an
    # unpinned "latest" alias.
    verdict = judge_client.complete(prompt, temperature=0).strip().upper()
    if verdict not in ("PASS", "FAIL"):
        raise JudgeParseError(f"unparseable judge verdict: {verdict!r}")
    return verdict == "PASS"
```

The grader's return value stays binary pass/fail per this
file's plugin-wide rule — `JudgeParseError` is not a third
grading state, it's an operational failure. Never catch it
and coerce to `False`; log it and re-run the judge call or
route the item to human review instead.

## drift-suite.yaml Example

Frozen general-capability benchmarks plus a
domain-adjacent slice, per `SKILL.md`'s Directory
Contract. Benchmark subsets are frozen at a fixed
seed/split so re-runs are comparable run over run:

```yaml
# eval/drift-suite.yaml
frozen_benchmarks:
  - name: mmlu-subset
    source: mmlu
    split: test
    n_items: 500
    seed: 42
  - name: gsm8k-subset
    source: gsm8k
    split: test
    n_items: 250
    seed: 42
  - name: ifeval
    source: ifeval
    split: test
    n_items: 300
    seed: 42

domain_adjacent:
  path: eval/goldens.jsonl
  filter: "tag == 'drift-suite'"
  n_items_range: [200, 500]

drift_budget:
  noise_tolerance_pts: 1
  rerun_seed_variation_pts: [2, 5]
  hard_fail_threshold_pts: 5   # >5pt drop is a hard fail regardless of task-metric gains
```

**Minimum viable drift suite for a small/dogfood run:** the
500/250/300 general-benchmark sizes and the 200-500
`domain_adjacent` range above are scoped for production-scale
runs and can be hours of wall-clock at greedy single-stream
decode on modest hardware. Scope down deliberately rather than
silently truncating — pick n per benchmark using
`checkpoint-promotion`'s item-count-from-budget rule (95% CI
half-width comfortably under half the hard-fail threshold), and
document the scoped-down suite inline in `drift-suite.yaml`
(a comment naming the budget it was sized against). The
`domain_adjacent` block itself is **optional when the golden
set is small and already fully consumed by the task harness** —
if `eval/goldens.jsonl` has no separate drift-suite-tagged
holdout because every golden is already spoken for by the task
grader, omit the block rather than fabricating a slice with
nothing behind it; the frozen general benchmarks alone still
provide a capability-drift signal.

## Drift-Suite MMLU-Style Scoring: Logprob Over Generate-and-Extract

"Letter-choice logprob or generate-and-extract" are not
equivalent scoring methods, though earlier guidance in this
plugin implied they were interchangeable:

- **Generate-and-extract** (sample a completion, extract the
  first A–D letter from a tight token budget) is **parse-brittle**
  for models that preamble before answering. Observed on a real
  drift run: a near-base checkpoint hit 9/100 unparsed-scored-
  as-wrong items (all prose restarts like "The energy levels
  of...") on a `max_new_tokens=8` budget, versus 0–1 unparsed
  for other checkpoints in the same series — this conflates
  answer-format compliance with the knowledge MMLU is supposed
  to measure, and can hard-fail a checkpoint on formatting alone.
- **Logprob scoring** (compare the model's log-probability on
  each of the four answer-letter tokens directly, no generation
  or parsing involved) is robust to this failure mode entirely —
  there is nothing to parse, so a verbose or preambling model
  scores on its actual answer distribution.

**Prefer logprob scoring whenever the harness has logit access**
(local inference, not a hosted API that only returns text). When
logit access isn't available and generate-and-extract is the
only option, use a generous token budget and retry with a longer
budget on any unparsed output before scoring it as wrong — don't
let a tight budget silently convert "the model reasoned before
answering" into "the model failed the benchmark."
