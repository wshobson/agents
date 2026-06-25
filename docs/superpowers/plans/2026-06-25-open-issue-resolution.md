# Open-Issue Resolution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the plugin-eval LLM-judge silent-failure bug (#591), harden the review-agent-governance Cedar policy (#598), and close the four stale/superseded issues (#579, #580, #570, #595).

**Architecture:** Two independent code changes on branch `fix/issues-591-598`. (A) plugin-eval: correct the Agent-SDK message extraction, route genuine measurement failures through the engine's existing "unmeasured" path instead of fabricating 0.5, and drop dead config. (B) review-agent-governance: rewrite `in`-on-String forbid rules to validator-clean `.contains()`, add a `.cedarschema`, and add a graceful-skip round-trip test. Triage closes are outward-facing and happen last, only with maintainer approval.

**Tech Stack:** Python 3.12, `claude-agent-sdk` 0.2.101, pytest + pytest-asyncio, `uv`; Cedar policy language via `protect-mcp@0.5.5` (npx).

## Global Constraints

- Python tooling is **uv / ruff / ty** — never pip/black/mypy. Run commands from `plugins/plugin-eval/` as `uv run --project . pytest ...` or repo-root `make test`.
- Do not change generated harness artifacts by hand; none of these changes affect them, but run `make generate-all` at the end to confirm zero drift.
- `claude-agent-sdk` message types: `AssistantMessage(content: list, model: str, ...)`, `TextBlock(text: str)`, `ResultMessage(subtype, duration_ms, duration_api_ms, is_error, num_turns, session_id, ..., result: str|None, structured_output, ...)`. `ResultMessage` has **no** `content` attribute — that is the bug.
- The composite engine treats a dimension as **unmeasured** when its key is **absent** from a layer's `sub_scores` (see `engine.py:_blend_layer_scores`, the `if dim in judge_scores` guard) or when the blended value is `< 0.0`. "Unmeasured" is therefore expressed by **omitting the key**, not by writing a 0.
- Outward-facing GitHub actions (issue closes, the #598 reply) are posted **only after explicit maintainer approval**.

---

## Phase A — #591: plugin-eval judge silent-failure fix

### Task 1: Correct message extraction + unmeasured signal in `query_llm`

**Files:**
- Modify: `plugins/plugin-eval/src/plugin_eval/layers/judge.py` (`query_llm`, ~L55-98; add a pure helper `_extract_and_parse`)
- Test: `plugins/plugin-eval/tests/test_judge.py`

**Interfaces:**
- Produces: `_extract_and_parse(messages: list) -> dict` — returns the parsed JSON dict on success, or `{"unmeasured": True, "error": str, "raw": str}` when the run errored / produced no text / was not valid JSON. `query_llm(prompt, system="", model=...) -> dict` keeps its signature but now returns an `unmeasured` dict instead of raising on missing SDK / call failure.

- [ ] **Step 1: Write the failing tests** (append to `tests/test_judge.py`)

```python
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
from plugin_eval.layers.judge import _extract_and_parse


def _assistant(text: str) -> AssistantMessage:
    return AssistantMessage(content=[TextBlock(text=text)], model="claude-sonnet-4-6")


def _result(*, is_error: bool = False, result: str | None = None) -> ResultMessage:
    return ResultMessage(
        subtype="success" if not is_error else "error",
        duration_ms=1,
        duration_api_ms=1,
        is_error=is_error,
        num_turns=1,
        session_id="t",
        result=result,
    )


class TestExtractAndParse:
    def test_parses_assistant_text_json(self):
        msgs = [_assistant('{"f1": 1.0}'), _result(result="ignored")]
        assert _extract_and_parse(msgs) == {"f1": 1.0}

    def test_parses_json_in_code_fence(self):
        msgs = [_assistant('```json\n{"score": 0.8}\n```'), _result()]
        assert _extract_and_parse(msgs) == {"score": 0.8}

    def test_falls_back_to_result_field_when_no_assistant_text(self):
        msgs = [_result(result='{"score": 0.7}')]
        assert _extract_and_parse(msgs) == {"score": 0.7}

    def test_errored_result_is_unmeasured(self):
        msgs = [_result(is_error=True)]
        out = _extract_and_parse(msgs)
        assert out["unmeasured"] is True

    def test_empty_output_is_unmeasured(self):
        assert _extract_and_parse([_result()])["unmeasured"] is True

    def test_non_json_is_unmeasured(self):
        out = _extract_and_parse([_assistant("not json at all"), _result()])
        assert out["unmeasured"] is True
        assert out["raw"] == "not json at all"
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_judge.py::TestExtractAndParse -v`
Expected: FAIL with `ImportError: cannot import name '_extract_and_parse'`.

- [ ] **Step 3: Implement the helper and rewrite `query_llm`**

Replace the body of `query_llm` (judge.py ~L55-98) with:

```python
def _extract_and_parse(messages: list) -> dict:
    """Pull assistant text from SDK messages and parse JSON.

    Returns the parsed dict on success, or an {"unmeasured": True, ...} marker
    when the run errored, produced no text, or returned non-JSON.
    """
    from claude_agent_sdk import (  # type: ignore[import-untyped]
        AssistantMessage,
        ResultMessage,
        TextBlock,
    )

    text = ""
    fallback = ""
    errored = False
    for message in messages:
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text += block.text
        elif isinstance(message, ResultMessage):
            if message.is_error:
                errored = True
            if message.result:
                fallback = message.result

    raw = text or fallback
    if errored:
        return {"unmeasured": True, "error": "judge LLM call returned an error result"}
    if not raw.strip():
        return {"unmeasured": True, "error": "judge LLM returned no text"}

    stripped = raw.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", stripped)
    if fence_match:
        stripped = fence_match.group(1).strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return {"unmeasured": True, "error": "judge response was not valid JSON", "raw": raw}


async def query_llm(prompt: str, system: str = "", model: str = "claude-sonnet-4-6") -> dict:
    """Call Claude via the Agent SDK and return a parsed JSON dict.

    Degrades to an {"unmeasured": True, ...} marker (never raises) when the SDK
    is missing or the call fails, so the judge layer can be skipped instead of
    crashing the whole evaluation.
    """
    try:
        from claude_agent_sdk import (  # type: ignore[import-untyped]
            ClaudeAgentOptions,
            query,
        )
    except ImportError:
        return {
            "unmeasured": True,
            "error": "claude-agent-sdk not installed (uv sync --extra llm)",
        }

    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    try:
        messages = [
            message
            async for message in query(
                prompt=full_prompt,
                options=ClaudeAgentOptions(model=model, allowed_tools=[]),
            )
        ]
    except Exception as exc:  # noqa: BLE001 — judge is best-effort; degrade to unmeasured
        return {"unmeasured": True, "error": f"judge LLM call failed: {exc}"}

    return _extract_and_parse(messages)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_judge.py::TestExtractAndParse -v`
Expected: PASS (6 passed).

- [ ] **Step 5: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/layers/judge.py plugins/plugin-eval/tests/test_judge.py
git commit -m "fix(plugin-eval): read judge LLM text from AssistantMessage/ResultMessage (#591)

ResultMessage has no .content attribute, so the judge always read empty
text and silently fell back to 0.5. Extract from AssistantMessage TextBlocks
with ResultMessage.result fallback; mark errored/empty/non-JSON as unmeasured."
```

---

### Task 2: Propagate "unmeasured" through `JudgeAnalyzer.analyze_skill`

**Files:**
- Modify: `plugins/plugin-eval/src/plugin_eval/layers/judge.py` (`analyze_skill`, ~L130-168; add helper `_measured_score`)
- Test: `plugins/plugin-eval/tests/test_judge.py`

**Interfaces:**
- Consumes: assessment dicts from `assess_*` (each is `query_llm`'s return — either real JSON or `{"unmeasured": True}`).
- Produces: `LayerResult(layer="judge", score, sub_scores, metadata)` where `sub_scores` contains **only measured** dimensions (unmeasured keys omitted), and `metadata["unmeasured"]` is a sorted list of the dimension names that could not be measured.

- [ ] **Step 1: Write the failing tests** (append to `tests/test_judge.py`)

```python
class TestUnmeasuredPropagation:
    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    async def test_all_unmeasured_yields_empty_sub_scores(self, mock_query, sample_skill_dir: Path):
        mock_query.return_value = {"unmeasured": True, "error": "no text"}
        analyzer = JudgeAnalyzer(JudgeConfig())
        result = await analyzer.analyze_skill(sample_skill_dir)
        assert result.sub_scores == {}
        assert result.score == 0.0
        assert set(result.metadata["unmeasured"]) == {
            "triggering_accuracy",
            "orchestration_fitness",
            "output_quality",
            "scope_calibration",
        }

    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    async def test_partial_measurement_omits_only_failed(self, mock_query, sample_skill_dir: Path):
        mock_query.side_effect = [
            {"f1": 0.9, "predictions": []},          # triggering measured
            {"unmeasured": True, "error": "x"},       # orchestration failed
            {"score": 0.8, "simulations": []},        # output measured
            {"unmeasured": True, "error": "x"},       # scope failed
        ]
        analyzer = JudgeAnalyzer(JudgeConfig())
        result = await analyzer.analyze_skill(sample_skill_dir)
        assert set(result.sub_scores) == {"triggering_accuracy", "output_quality"}
        assert result.sub_scores["triggering_accuracy"] == 0.9
        assert set(result.metadata["unmeasured"]) == {"orchestration_fitness", "scope_calibration"}
```

- [ ] **Step 2: Run to verify they fail**

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_judge.py::TestUnmeasuredPropagation -v`
Expected: FAIL (current code defaults missing scores to 0.5, so `sub_scores` is never empty and there is no `metadata["unmeasured"]`).

- [ ] **Step 3: Implement** — replace the composite/sub_scores/return block in `analyze_skill` (judge.py ~L140-168) with:

```python
        raw_scores: dict[str, float | None] = {
            "triggering_accuracy": _measured_score(triggering, "f1"),
            "orchestration_fitness": _measured_score(orchestration, "score"),
            "output_quality": _measured_score(output_quality, "score"),
            "scope_calibration": _measured_score(scope, "score"),
        }
        sub_scores: dict[str, float] = {k: v for k, v in raw_scores.items() if v is not None}
        unmeasured = sorted(k for k, v in raw_scores.items() if v is None)

        # Layer score is display-only; the composite engine blends per-dimension
        # sub_scores (omitted keys are excluded). Use the mean of measured dims.
        score = sum(sub_scores.values()) / len(sub_scores) if sub_scores else 0.0

        metadata: dict = {
            "triggering": triggering,
            "orchestration": orchestration,
            "output_quality": output_quality,
            "scope": scope,
            "unmeasured": unmeasured,
        }

        return LayerResult(
            layer="judge",
            score=score,
            sub_scores=sub_scores,
            metadata=metadata,
        )
```

Add this helper just above the `JudgeAnalyzer` class (after `query_llm` / `_extract_and_parse`):

```python
def _measured_score(result: dict, key: str) -> float | None:
    """Return the numeric score for an assessment, or None if it was unmeasured."""
    if result.get("unmeasured"):
        return None
    val = result.get(key)
    return float(val) if isinstance(val, (int, float)) else None
```

- [ ] **Step 4: Run to verify they pass** (and the existing judge tests still pass)

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_judge.py -v`
Expected: PASS. Note: the existing `test_full_analysis` asserts `result.score > 0` — still true (all four measured).

- [ ] **Step 5: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/layers/judge.py plugins/plugin-eval/tests/test_judge.py
git commit -m "fix(plugin-eval): omit unmeasured judge dimensions instead of scoring 0.5 (#591)"
```

---

### Task 3: Fix the same extraction bug in Monte Carlo `run_simulation`

**Files:**
- Modify: `plugins/plugin-eval/src/plugin_eval/layers/monte_carlo.py` (`run_simulation`, ~L53-111; add helper `_simresult_from_messages`)
- Test: `plugins/plugin-eval/tests/test_monte_carlo.py`

**Interfaces:**
- Produces: `_simresult_from_messages(messages: list, prompt: str, duration_ms: int) -> SimResult` — `activated` is True iff assistant text was produced; `quality_score = min(1.0, len(text)/500)`; `errored` True iff a `ResultMessage.is_error`.

- [ ] **Step 1: Write the failing test** (append to `tests/test_monte_carlo.py`)

```python
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
from plugin_eval.layers.monte_carlo import _simresult_from_messages


def _assistant(text: str) -> AssistantMessage:
    return AssistantMessage(content=[TextBlock(text=text)], model="claude-sonnet-4-6")


def _result(*, is_error: bool = False) -> ResultMessage:
    return ResultMessage(
        subtype="success" if not is_error else "error",
        duration_ms=1, duration_api_ms=1, is_error=is_error, num_turns=1, session_id="t",
    )


class TestSimResultFromMessages:
    def test_activated_when_assistant_text_present(self):
        sim = _simresult_from_messages([_assistant("x" * 250), _result()], "p", 10)
        assert sim.activated is True
        assert sim.quality_score == 0.5
        assert sim.errored is False

    def test_not_activated_when_no_text(self):
        sim = _simresult_from_messages([_result()], "p", 10)
        assert sim.activated is False
        assert sim.quality_score == 0.0

    def test_errored_result_flagged(self):
        sim = _simresult_from_messages([_result(is_error=True)], "p", 10)
        assert sim.errored is True
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_monte_carlo.py::TestSimResultFromMessages -v`
Expected: FAIL with `ImportError: cannot import name '_simresult_from_messages'`.

- [ ] **Step 3: Implement** — add the helper above `run_simulation` and rewrite the message loop. Replace `run_simulation` body (monte_carlo.py ~L53-111) with:

```python
def _simresult_from_messages(messages: list, prompt: str, duration_ms: int) -> SimResult:
    """Build a SimResult from SDK messages (assistant text => activation + quality)."""
    from claude_agent_sdk import (  # type: ignore[import-untyped]
        AssistantMessage,
        ResultMessage,
        TextBlock,
    )

    text = ""
    tokens = 0
    errored = False
    for message in messages:
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    text += block.text
        elif isinstance(message, ResultMessage):
            if message.is_error:
                errored = True
            if isinstance(message.usage, dict):
                tokens = message.usage.get("total_tokens", tokens)

    activated = bool(text)
    quality_score = min(1.0, len(text) / 500) if activated else 0.0
    return SimResult(
        activated=activated,
        quality_score=quality_score,
        tokens=tokens,
        duration_ms=duration_ms,
        errored=errored,
        prompt=prompt,
    )


async def run_simulation(skill_content: str, prompt: str) -> SimResult:
    """Run a single simulation via Agent SDK. Returns SimResult. On error, errored=True."""
    try:
        import time

        from claude_agent_sdk import (  # type: ignore[import-untyped]
            ClaudeAgentOptions,
            query,
        )

        full_prompt = (
            f"You are evaluating a skill. Apply the skill if appropriate.\n\n"
            f"{skill_content}\n\n{prompt}"
        )
        start = time.monotonic()
        messages = [
            message
            async for message in query(
                prompt=full_prompt,
                options=ClaudeAgentOptions(allowed_tools=[]),
            )
        ]
        duration_ms = int((time.monotonic() - start) * 1000)
        return _simresult_from_messages(messages, prompt, duration_ms)
    except Exception:  # noqa: BLE001 — a failed run is recorded as errored, not fatal
        return SimResult(
            activated=False,
            quality_score=0.0,
            tokens=0,
            duration_ms=0,
            errored=True,
            prompt=prompt,
        )
```

Note the signature change: `run_simulation(skill_content, prompt)` — the `auth` parameter is removed (Task 4 removes its only call-site argument).

- [ ] **Step 4: Update the call site** — `monte_carlo.py:248`, change `run_simulation(skill_content, prompt, self.config.auth)` to `run_simulation(skill_content, prompt)`.

- [ ] **Step 5: Run to verify it passes** (and existing MC tests still pass)

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_monte_carlo.py -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/layers/monte_carlo.py plugins/plugin-eval/tests/test_monte_carlo.py
git commit -m "fix(plugin-eval): fix Monte Carlo SDK message extraction (#591)"
```

---

### Task 4: Remove dead `auth` / `model_tier` config

**Files:**
- Modify: `plugins/plugin-eval/src/plugin_eval/models.py` (`EvalConfig`, L39 + L43)
- Modify: `plugins/plugin-eval/src/plugin_eval/layers/judge.py` (`JudgeConfig`, L109 + L111)
- Modify: `plugins/plugin-eval/src/plugin_eval/layers/monte_carlo.py` (`MonteCarloConfig`, L43)
- Modify: `plugins/plugin-eval/src/plugin_eval/engine.py` (L86, L101 — drop `auth=` args)
- Modify: `plugins/plugin-eval/src/plugin_eval/cli.py` (remove `--auth` from `score`/`certify`, `_run_score` param, and `EvalConfig(...)`)
- Modify: `plugins/plugin-eval/tests/test_judge.py` (L13) and `tests/test_models.py` (L24) — drop the `auth` assertions
- Modify: `docs/plugin-eval.md` (L94 — remove the `--auth` row)

**Interfaces:**
- Produces: `EvalConfig`, `JudgeConfig`, `MonteCarloConfig` without `auth`/`model_tier`; `_run_score(path, depth, output, verbose, concurrency, threshold)` (no `auth` param); `score`/`certify` commands without `--auth`.

- [ ] **Step 1: Update the failing-config tests first** (they currently assert removed fields)

In `tests/test_judge.py`, the `test_default_config` body becomes:
```python
    def test_default_config(self):
        config = JudgeConfig()
        assert config.judges == 1
        assert config.concurrency == 4
```
In `tests/test_models.py:24`, remove the line `assert config.auth == "max"` (keep the rest of that test).

- [ ] **Step 2: Run to verify the suite fails on the new expectation**

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_judge.py::TestJudgeConfig tests/test_models.py -v`
Expected: PASS for the edited asserts is not yet possible — they still reference `auth` in source via defaults; run to confirm current state, then proceed. (If green already, that's fine — these asserts just stop checking `auth`.)

- [ ] **Step 3: Remove the fields and arguments**

- `models.py`: delete `model_tier: str = "auto"` (L39) and `auth: str = "max"` (L43) from `EvalConfig`.
- `judge.py` `JudgeConfig`: delete `auth: str = "max"` and `model_tier: str = "auto"`, leaving:
  ```python
  @dataclass
  class JudgeConfig:
      judges: int = 1
      concurrency: int = 4
  ```
- `monte_carlo.py` `MonteCarloConfig`: delete `auth: str = "max"`.
- `engine.py`: `JudgeConfig(judges=self.config.judges, auth=self.config.auth, concurrency=self.config.concurrency)` → drop `auth=` (L86). `MonteCarloConfig(n_runs=n_runs, concurrency=self.config.concurrency, auth=self.config.auth)` → drop `auth=` (L101).
- `cli.py`: in `_run_score` remove the `auth: str` parameter (L38) and remove `auth=auth` from `EvalConfig(...)` (L51). In `score` (L99) and `certify` (L116) remove the `auth` typer.Option; update the calls (L105, L120) to `_run_score(path, depth, output, verbose, concurrency, threshold)` / `_run_score(path, Depth.DEEP, output, verbose, concurrency, threshold)`.
- `docs/plugin-eval.md`: delete the `| `--auth` | ... |` table row (L94).

- [ ] **Step 4: Run the full plugin-eval suite + lint + type check**

Run: `cd plugins/plugin-eval && uv run --project . pytest -q && uv run --project . ruff check src tests && uv run --project . ruff format --check src tests`
Expected: all pass, no ruff findings.

- [ ] **Step 5: Commit**

```bash
git add plugins/plugin-eval/src docs/plugin-eval.md plugins/plugin-eval/tests
git commit -m "refactor(plugin-eval): remove dead auth/model_tier config (#591)"
```

---

### Task 5: Surface a stderr warning when the judge is unmeasured

**Files:**
- Modify: `plugins/plugin-eval/src/plugin_eval/cli.py` (`_run_score`, after the report is produced, before the threshold check)
- Test: `plugins/plugin-eval/tests/test_cli.py`

**Interfaces:**
- Consumes: `result.layers` (the judge `LayerResult` with `metadata["unmeasured"]` from Task 2).

- [ ] **Step 1: Write the failing test** (append to `tests/test_cli.py`)

```python
from typer.testing import CliRunner
from unittest.mock import patch
from plugin_eval.cli import app
from plugin_eval.models import (
    CompositeResult, Depth, EvalConfig, LayerResult, PluginEvalResult,
)


def test_score_warns_when_judge_unmeasured(sample_skill_dir, tmp_path):
    fake = PluginEvalResult(
        plugin_path=str(sample_skill_dir),
        timestamp="t",
        config=EvalConfig(depth=Depth.STANDARD),
        layers=[
            LayerResult(layer="static", score=0.8, sub_scores={}),
            LayerResult(layer="judge", score=0.0, sub_scores={},
                        metadata={"unmeasured": ["triggering_accuracy", "output_quality"]}),
        ],
        composite=CompositeResult(score=60.0),
    )
    with patch("plugin_eval.cli.EvalEngine") as Eng:
        Eng.return_value.evaluate_skill.return_value = fake
        result = CliRunner(mix_stderr=False).invoke(
            app, ["score", str(sample_skill_dir), "--output", "json"]
        )
    assert result.exit_code == 0
    assert "judge" in result.stderr.lower()
    assert "unmeasured" in result.stderr.lower() or "could not" in result.stderr.lower()
```

- [ ] **Step 2: Run to verify it fails**

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_cli.py::test_score_warns_when_judge_unmeasured -v`
Expected: FAIL (no warning emitted).

- [ ] **Step 3: Implement** — in `cli.py` `_run_score`, immediately after the `reporter`/`typer.echo` output block (after L80, before the threshold check at L82) add:

```python
    judge_layer = next((lr for lr in result.layers if lr.layer == "judge"), None)
    if judge_layer is not None:
        unmeasured = judge_layer.metadata.get("unmeasured") or []
        if unmeasured:
            stderr_console.print(
                f"[yellow]warning:[/yellow] LLM judge could not measure "
                f"{', '.join(unmeasured)}; composite computed from the remaining "
                f"layers. Check that claude-agent-sdk is installed and a model is "
                f"configured (run with --verbose for details)."
            )
```

- [ ] **Step 4: Run to verify it passes**

Run: `cd plugins/plugin-eval && uv run --project . pytest tests/test_cli.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add plugins/plugin-eval/src/plugin_eval/cli.py plugins/plugin-eval/tests/test_cli.py
git commit -m "feat(plugin-eval): warn on stderr when the LLM judge is unmeasured (#591)"
```

---

## Phase B — #598: review-agent-governance Cedar hardening

### Task 6: Live-verify the real engine's behavior

**Files:** none (investigation; records the result that gates Task 10's reply wording).

- [ ] **Step 1: Run a deny-case and a permit-case through the real evaluator**

```bash
cd plugins/review-agent-governance/policies
# Deny case — should exit 2 if the gate fires:
npx --yes protect-mcp@0.5.5 evaluate \
  --policy review-agent-governance.cedar \
  --tool Bash \
  --input '{"command":"gh pr merge 123 --squash"}' \
  --fail-on-missing-policy false; echo "exit=$?"
# Permit case — should exit 0:
npx --yes protect-mcp@0.5.5 evaluate \
  --policy review-agent-governance.cedar \
  --tool Bash \
  --input '{"command":"ls -la"}' \
  --fail-on-missing-policy false; echo "exit=$?"
```

- [ ] **Step 2: Record the outcome and decide severity**

- If deny→`exit=2` and permit→`exit=0`: gates work → #598 is a **false positive** for the shipped engine. Severity: informational. Proceed; the rewrite is still adopted as hardening.
- If deny→`exit=0`: the disclosure is **correct** → severity **HIGH**. The rewrite (Task 7) becomes the priority fix and the reply credits a real vulnerability.
- If `npx`/network unavailable in this environment: do not guess — surface the exact two commands above for the maintainer to run via `!`, and hold Task 10's reply until the result is known.

- [ ] **Step 3: No commit** (record the result in the PR description / Task 10 draft).

---

### Task 7: Rewrite the 5 forbid rules to `.contains()`

**Files:**
- Modify: `plugins/review-agent-governance/policies/review-agent-governance.cedar`

- [ ] **Step 1: Rewrite each `context.<attr> in [ ... ]` to `[ ... ].contains(context.<attr>)`.** The five edits:

```cedar
// Rule 1
} when {
    ["gh pr review", "gh pr comment", "gh pr close", "gh pr merge", "gh pr edit",
     "gh issue comment", "gh issue close", "gh issue edit", "gh release create",
     "gh release edit", "gh api repos"].contains(context.command_pattern)
};

// Rule 2
} when {
    ["glab mr comment", "glab mr approve", "glab mr merge",
     "glab issue comment"].contains(context.command_pattern)
};

// Rule 3
} when {
    ["git push", "git push --force", "git push -f"].contains(context.command_pattern) &&
    ["main", "master", "release", "production"].contains(context.target_branch)
};

// Rule 4
} when {
    [".github/workflows/", ".github/CODEOWNERS", ".gitlab-ci.yml",
     ".circleci/config.yml", "buildkite/pipeline.yml"].contains(context.path_starts_with)
};

// Rule 5
} when {
    context.method == "POST" &&
    ["api.github.com", "api.gitlab.com", "api.bitbucket.org",
     "hooks.slack.com", "discord.com"].contains(context.url_host)
};
```

Keep all comments and the terminal `permit (principal, action, resource);` unchanged.

- [ ] **Step 2: Re-run the Task 6 deny/permit commands to confirm behavior is unchanged-or-fixed**

Run the two `npx ... evaluate` commands from Task 6 against the rewritten policy.
Expected: deny→`exit=2`, permit→`exit=0`. (If Task 6 showed the gates were already working, this confirms no regression; if it showed them broken, this confirms the fix.)

- [ ] **Step 3: Commit**

```bash
git add plugins/review-agent-governance/policies/review-agent-governance.cedar
git commit -m "fix(review-agent-governance): use set .contains() instead of in-on-String in forbid rules (#598)

context.<attr> in [strings] is a type error under standard Cedar (in expects
an entity LHS) and is silently discarded, which would disable the gate. Rewrite
to [strings].contains(context.<attr>), which validates and is portable."
```

---

### Task 8: Add a `.cedarschema` typing the context attributes

**Files:**
- Create: `plugins/review-agent-governance/policies/review-agent-governance.cedarschema`

- [ ] **Step 1: Write the schema** declaring the actions and their String context attributes, so `cedar validate` flags any future `in`-on-String mistake at load time.

```cedarschema
entity User;
entity Resource;

action "Bash" appliesTo {
  principal: [User],
  resource: [Resource],
  context: { command_pattern: String, target_branch: String }
};

action "Write" appliesTo {
  principal: [User],
  resource: [Resource],
  context: { path_starts_with: String }
};

action "Edit" appliesTo {
  principal: [User],
  resource: [Resource],
  context: { path_starts_with: String }
};

action "WebFetch" appliesTo {
  principal: [User],
  resource: [Resource],
  context: { method: String, url_host: String }
};
```

- [ ] **Step 2: Validate the policy against the schema if the `cedar` CLI is available** (best-effort; document the command in the policy folder README later)

```bash
cd plugins/review-agent-governance/policies
command -v cedar >/dev/null 2>&1 && \
  cedar validate --policies review-agent-governance.cedar --schema review-agent-governance.cedarschema || \
  echo "cedar CLI not present — schema is documentation/validation-only"
```
Expected: `cedar validate` reports success (no validation errors), or the skip message. Note: the shipped hook uses `protect-mcp`, which may not consume this schema — its value is `cedar validate` + documentation.

- [ ] **Step 3: Commit**

```bash
git add plugins/review-agent-governance/policies/review-agent-governance.cedarschema
git commit -m "feat(review-agent-governance): add cedarschema typing context attrs as String (#598)"
```

---

### Task 9: Add a graceful-skip deny/permit round-trip test

**Files:**
- Create: `plugins/review-agent-governance/test/run-tests.sh` (executable)
- Create: `plugins/review-agent-governance/test/fixtures/deny-gh-pr-merge.json`
- Create: `plugins/review-agent-governance/test/fixtures/permit-ls.json`
- Create: `plugins/review-agent-governance/test/README.md`

**Interfaces:** mirrors `plugins/protect-mcp/test/run-tests.sh` conventions — exit `0` all pass, `1` a failure, `77` tools missing (treated as skipped).

- [ ] **Step 1: Create the fixtures**

`fixtures/deny-gh-pr-merge.json`:
```json
{ "tool_name": "Bash", "tool_input": { "command": "gh pr merge 123 --squash" } }
```
`fixtures/permit-ls.json`:
```json
{ "tool_name": "Bash", "tool_input": { "command": "ls -la" } }
```

- [ ] **Step 2: Create `test/run-tests.sh`** (mirrors protect-mcp's preflight + check_exit)

```bash
#!/usr/bin/env bash
# run-tests.sh — exercise review-agent-governance.cedar against protect-mcp.
# Exit codes: 0 pass, 1 fail, 77 required tools missing (skipped).
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
POLICY="../policies/review-agent-governance.cedar"

need() { command -v "$1" >/dev/null 2>&1 || { echo "SKIP: '$1' not found."; exit 77; }; }
need node; need npx; need python3

PASS=0; FAIL=0
pass() { echo "PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }
check_exit() { if [ "$1" -eq "$2" ]; then pass "$3"; else fail "$3 (exit $1, expected $2)"; fi; }
tool() { python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["tool_name"])' "$1"; }
inp() { python3 -c 'import json,sys;print(json.dumps(json.load(open(sys.argv[1]))["tool_input"]))' "$1"; }

run() {
  npx --yes protect-mcp@0.5.5 evaluate --policy "$POLICY" \
    --tool "$(tool "$1")" --input "$(inp "$1")" --fail-on-missing-policy false >/dev/null 2>&1
}

echo "=== Deny: gh pr merge ==="
run fixtures/deny-gh-pr-merge.json; check_exit $? 2 "gh pr merge is denied (exit 2)"

echo "=== Permit: ls ==="
run fixtures/permit-ls.json; check_exit $? 0 "ls is permitted (exit 0)"

echo ""; echo "Passed: $PASS, Failed: $FAIL"
[ "$FAIL" -eq 0 ] || exit 1
```

- [ ] **Step 3: Create `test/README.md`** documenting that the test requires node/npx/network and skips (exit 77) otherwise, mirroring `plugins/protect-mcp/test/README.md`.

```markdown
# review-agent-governance policy tests

Round-trip deny/permit checks for `policies/review-agent-governance.cedar`,
evaluated with `protect-mcp@0.5.5` (the engine the plugin's hook uses).

```bash
./run-tests.sh   # exit 0 pass · 1 fail · 77 tools missing (skipped)
```

Requires `node` (>=18), `npx`, and network access on first run.
```

- [ ] **Step 4: Make executable and run**

```bash
chmod +x plugins/review-agent-governance/test/run-tests.sh
plugins/review-agent-governance/test/run-tests.sh; echo "suite exit=$?"
```
Expected: `exit=0` (both checks pass) where npx/network are available, or `exit=77` (skipped) otherwise. A `1` means the gate is not firing — escalate per Task 6.

- [ ] **Step 5: Commit**

```bash
git add plugins/review-agent-governance/test
git commit -m "test(review-agent-governance): add deny/permit round-trip test (skips without npx) (#598)"
```

---

## Phase C — Integration + triage closes

### Task 10: Final gates, PR, and the outward-facing closes/reply

**Files:** none (verification + GitHub actions).

- [ ] **Step 1: Full repo gates**

```bash
cd /Users/wshobson/workspace/agents
make test            # plugin-eval + tools — must pass
make validate STRICT=1
make garden
make generate-all && git status --porcelain   # expect: empty (no harness drift)
```
Expected: all pass; drift check prints nothing.

- [ ] **Step 2: Open the PR** for `fix/issues-591-598` summarizing both fixes; reference issues #591 and #598. Do not merge without maintainer approval.

- [ ] **Step 3: Draft the outward-facing actions (post only after explicit maintainer approval).**

- **#591** — comment that the fix landed in the PR (judge now reads `AssistantMessage`/`ResultMessage` correctly, surfaces "unmeasured" instead of fake 0.5, removed dead config); thank lkjie; close when the PR merges.
- **#598** — reply using the Task 6 result. If false positive: thank matiaszabal, explain the shipped engine is `protect-mcp@0.5.5` (their test used vanilla `cedar-policy 4.8.2`), note we adopted `.contains()` + a schema + a round-trip test as hardening, and reference `cedar-policy/cedar#2428`. If confirmed: credit a real high-severity finding and point to the fix PR. Close when the PR merges.
- **#579** — close: fixed by the format-modernization commit (`4820385`); current marketplace carries no `strict`/component arrays. Ask the reporter to update the marketplace / unpin from 1.0.1/1.2.x.
- **#580** — close: same modernization; `shell-scripting` is now 1.2.3 with auto-discovery and the skills load. Ask them to update.
- **#570** — close as converted to PR #577 (trimmed 3-skill version); tracking moves there.
- **#595** — close as converted to PR #596; tracking moves there.

- [ ] **Step 4: No commit** (GitHub state only).

---

## Self-Review

**Spec coverage:** #591 extraction fix (Tasks 1, 3) ✓; unmeasured-not-0.5 (Tasks 2, 5) ✓; remove dead config (Task 4) ✓; non-mocked extraction tests (Tasks 1, 3) ✓. #598 live-verify (Task 6) ✓; `.contains()` rewrite (Task 7) ✓; `.cedarschema` (Task 8) ✓; round-trip test (Task 9) ✓; severity-gated reply (Task 10) ✓. Triage closes #579/#580/#570/#595 (Task 10) ✓.

**Placeholder scan:** none — every code/test/command step contains concrete content.

**Type consistency:** `_extract_and_parse(list) -> dict`, `_measured_score(dict, str) -> float|None`, `_simresult_from_messages(list, str, int) -> SimResult`, `run_simulation(skill_content, prompt)` (auth removed, call-site updated in Task 3 Step 4) — consistent across tasks. `metadata["unmeasured"]` produced in Task 2, consumed in Tasks 5 and the Task 5 test.
