Last verified: 2026-07-13

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
normalization or judgment call:

```python
import subprocess
import tempfile
from pathlib import Path

def grade_execution(completion: str, test_code: str) -> bool:
    """Write the completion plus a pytest test file to
    a scratch dir, run pytest, and pass only on a
    clean exit code. Timeouts and non-zero exits are
    both failures — never treat a hung process as a
    pass by default.
    """
    with tempfile.TemporaryDirectory() as tmp:
        solution = Path(tmp) / "solution.py"
        test_file = Path(tmp) / "test_solution.py"
        solution.write_text(completion)
        test_file.write_text(test_code)
        result = subprocess.run(
            ["pytest", str(test_file), "-q"],
            cwd=tmp,
            capture_output=True,
            timeout=30,
        )
        return result.returncode == 0
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
    return verdict == "PASS"
```

Do not treat any output other than exactly `PASS` or
`FAIL` as a pass by default — log it as a parse
failure and re-run or route to human review instead
of defaulting either direction.

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
