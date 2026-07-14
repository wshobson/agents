Last verified: 2026-07-13

# GRPO Reward Function Library

Complete, runnable reward functions for TRL's
`GRPOTrainer`. Every function here follows the
current TRL reward-function signature: it accepts
`completions` plus any extra dataset columns as
keyword arguments, and returns a `list[float]` the
same length as `completions`. Base models are never
named here — `SFT_CHECKPOINT`/`JUDGE_MODEL` are
placeholders; see `finetuning-method-selection`'s
`references/model-catalog.md` for actual
checkpoints.

**These examples assume the standard (string)
completion format** — `completions: list[str]` — and
call `.strip()`, `json.loads()`, `.split()`, etc.
directly on each `completion`. TRL's conversational
dataset format instead passes each completion as
`[{"role": "assistant", "content": "..."}]`; on that
format, extract `completion[0]["content"]` before
applying any of the string operations below, in
every function in this file.

**Before wiring any of these into a training run,
inspect them against 50–100 sampled outputs by
hand** — this is `SKILL.md`'s Inspection Rule, not
optional. A reward function that looks correct in
isolation can still disagree with human judgment
on real model outputs.

## Format Reward

Checks structural compliance — did the completion
follow the required response shape at all — as a
prerequisite to grading correctness:

```python
import re

def format_reward(completions, **kwargs) -> list[float]:
    """1.0 if the completion has a <reasoning>...</reasoning>
    block followed by an <answer>...</answer> block, else 0.0.
    This is a gate, not the correctness signal — a
    well-formed wrong answer still scores 0 on
    correctness_reward below.
    """
    pattern = re.compile(
        r"^<reasoning>.*?</reasoning>\s*<answer>.*?</answer>$",
        re.DOTALL,
    )
    return [1.0 if pattern.match(c.strip()) else 0.0 for c in completions]
```

## Correctness Reward — Exact Match

The baseline verifiable-answer reward, for tasks
with a single ground-truth string (math final
answers, closed-form lookups):

```python
def correctness_reward(completions, answer, **kwargs) -> list[float]:
    """`answer` is the ground-truth column from the
    training dataset, aligned index-for-index with
    `completions`. Extracts the <answer> block from
    format_reward's expected shape and compares.
    """
    rewards = []
    for completion, gold in zip(completions, answer):
        match = re.search(r"<answer>(.*?)</answer>", completion, re.DOTALL)
        predicted = match.group(1).strip() if match else None
        rewards.append(2.0 if predicted == gold.strip() else 0.0)
    return rewards
```

## Correctness Reward — Schema Validation

For structured-output and tool-call tasks, where
"correct" means "conforms to the required JSON
schema," not string equality:

```python
import json
from jsonschema import validate, ValidationError

def schema_reward(completions, output_schema, **kwargs) -> list[float]:
    """`output_schema` is a JSON Schema dict, either a
    single constant schema for the whole batch or a
    per-example list the same length as `completions`.
    Rewards valid, schema-conformant JSON; 0.0 for
    anything that doesn't parse or doesn't validate.
    """
    if isinstance(output_schema, dict):
        # Constant case: one schema dict for every completion —
        # zip()-ing a bare dict would iterate its keys instead,
        # not the schema itself, so normalize first.
        schemas = [output_schema] * len(completions)
    else:
        schemas = list(output_schema)
        if len(schemas) != len(completions):
            raise ValueError(
                f"schema_reward: {len(schemas)} schemas for "
                f"{len(completions)} completions"
            )
    rewards = []
    for completion, schema in zip(completions, schemas):
        try:
            parsed = json.loads(completion)
            validate(instance=parsed, schema=schema)
            rewards.append(1.0)
        except (json.JSONDecodeError, ValidationError):
            rewards.append(0.0)
    return rewards
```

## Correctness Reward — Unit Test Execution

For code-generation tasks, where "correct" means
the generated function passes a held-out test
suite. Execute in a subprocess with a hard
timeout — never `exec()` untrusted completions
in-process.

**WARNING — this function executes model-generated
code and REQUIRES an isolated environment:** a
network-disabled container, gVisor/firejail, or a
dedicated CI sandbox, with **no secrets or
credentials in the environment** — no HF tokens,
experiment-tracker keys, cloud credentials, or SSH
keys. GRPO will, by design, push adversarial
completions through this path as the policy
explores. Never run it directly on a training host
holding credentials. The timeout below protects
training-loop liveness only — **it is NOT a
security boundary**. Likewise, `TemporaryDirectory`
confines where the harness writes its files, not
what the executed code can read or reach. The
function below enforces this: it takes the sandbox
boundary as a required argument and refuses to run
at all — returning reward 0.0 — when the caller
doesn't supply one. It never falls back to host
execution.

```python
import logging
import subprocess
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

def test_execution_reward(
    completions, test_code, sandbox_cmd, timeout_s=10, **kwargs
) -> list[float]:
    """`test_code` is a per-example pytest snippet that
    imports the candidate under a fixed module name
    and asserts expected behavior. Runs each candidate
    in its own subprocess with a wall-clock timeout;
    an infinite loop or crash scores 0.0 instead of
    hanging the training loop.

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
    execute anything and returns 0.0 for every
    completion — it never falls back to running
    pytest on the host. The subprocess environment is
    scrubbed to a minimal PATH (no HF tokens,
    experiment-tracker keys, cloud credentials, or SSH
    keys). The timeout is a liveness guard for the
    training loop, NOT a security boundary — isolation
    comes entirely from `sandbox_cmd`; the temporary
    directory only confines harness writes, not what
    executed code can read or reach.
    """
    if not sandbox_cmd:
        logger.warning(
            "test_execution_reward: no sandbox boundary provided "
            "— refusing to execute model-generated code"
        )
        return [0.0 for _ in completions]

    scrubbed_env = {"PATH": "/usr/bin:/bin"}
    rewards = []
    for completion, tests in zip(completions, test_code):
        with tempfile.TemporaryDirectory() as tmp:
            candidate_path = Path(tmp) / "candidate.py"
            test_path = Path(tmp) / "test_candidate.py"
            candidate_path.write_text(completion)
            test_path.write_text(tests)
            try:
                result = subprocess.run(
                    [*sandbox_cmd, "python", "-m", "pytest",
                     str(test_path), "-q"],
                    cwd=tmp,
                    capture_output=True,
                    timeout=timeout_s,
                    env=scrubbed_env,
                )
                rewards.append(1.0 if result.returncode == 0 else 0.0)
            except subprocess.TimeoutExpired:
                rewards.append(0.0)
    return rewards
```

## Length-Penalty Wrapper

Wraps any reward function above to discourage
runaway completion length without replacing the
underlying correctness signal — use when a
correctness-only reward starts trending toward
longer, padded outputs:

```python
def with_length_penalty(reward_fn, target_len=512, penalty_per_token=0.001):
    """Returns a new reward function that subtracts a
    small per-token penalty for every token past
    `target_len`, applied on top of `reward_fn`'s
    output. Penalty is capped so it can't drive an
    otherwise-correct reward negative — it discourages
    padding without overriding correctness.
    """
    def wrapped(completions, **kwargs) -> list[float]:
        base_rewards = reward_fn(completions, **kwargs)
        adjusted = []
        for reward, completion in zip(base_rewards, completions):
            overflow = max(0, len(completion.split()) - target_len)
            penalty = min(reward, overflow * penalty_per_token)
            adjusted.append(reward - penalty)
        return adjusted
    return wrapped
```

Note that `len(completion.split())` counts words
as a cheap proxy for tokens — use the model's own
tokenizer for true token counts when tuning
`target_len`.

This is a targeted fix for observed length
creep, not a substitute for Dr.GRPO — if length
bias is systemic rather than an occasional
overflow, route to the Dr.GRPO variant in
`SKILL.md`'s Variant Selection instead of stacking
penalty wrappers.

## Rubric-as-Reward Judge Pattern

For tasks where correctness isn't code-checkable
but the pass/fail line is still crisp enough for a
judge to apply consistently — e.g., "did the
response follow the requested format and stay
on-topic" rather than "is this a good essay."
Binary pass/fail, not a Likert score:

TRL calls reward functions with `completions` plus
whatever dataset columns the trainer was given, via
`**kwargs` — it does not inject arbitrary objects
like a judge client. Bind `judge_client` and the
fixed `rubric` in a closure before handing the
result to `GRPOTrainer(reward_funcs=[...])`, rather
than declaring them as parameters TRL is expected to
supply:

```python
def make_rubric_judge_reward(judge_client, rubric):
    """`judge_client` calls JUDGE_MODEL — a model from a
    *different* model family than the model under
    training, never the model being trained or a
    same-family relative of it. `rubric` is a fixed
    pass/fail criterion string, not a free-form
    quality prompt, so both are bound here rather than
    read from TRL-supplied per-example kwargs. Returns a
    reward function matching TRL's actual signature.
    """
    def rubric_judge_reward(completions, prompts, **kwargs) -> list[float]:
        """Returns 1.0/0.0 per completion, never an
        intermediate score."""
        rewards = []
        for prompt, completion in zip(prompts, completions):
            verdict = judge_client.judge(
                rubric=rubric,
                prompt=prompt,
                response=completion,
                output_format="pass_fail",   # binary only — no Likert scale
            )
            rewards.append(1.0 if verdict == "pass" else 0.0)
        return rewards
    return rubric_judge_reward
```

**Calibration is a hard prerequisite, not a
nice-to-have.** An uncalibrated judge is a
noisier, more expensive version of the exact-match
reward above — before wiring `rubric_judge_reward`
into a GRPO run, the judge must be calibrated
against human labels (train/dev/sealed-test
splits, TPR/TNR reported, judge pinned to a fixed
snapshot). That calibration workflow lives in
`eval-harness-first`; do not skip it because the
rubric "looks obviously right" — the same
plugin-wide judge-calibration prerequisite applies
here as everywhere else a judge grades a reward.
