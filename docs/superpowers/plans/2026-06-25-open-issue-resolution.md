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

- [x] **Step 2: OUTCOME (2026-06-25) — premise invalid; `evaluate` subcommand does not exist**

The live run revealed `protect-mcp@0.5.5` has **no `evaluate` or `sign` subcommand** (the invocation above falls through to "wrapper" mode). Its real CLI is `serve` (HTTP hook server), `simulate`, `init-hooks`, and Cedar-via-WASM (`--cedar <dir>`). Consequences:
- The plugin's `hooks/hooks.json` (PreToolUse `… evaluate …`, PostToolUse `… sign …`) targets non-existent subcommands → **the gate does not run at all** against the pinned version. This is a separate, larger defect than #598 as filed.
- protect-mcp's own `test/run-tests.sh` also uses `evaluate …`, so the earlier "its test expects deny → gates work" inference was unfounded.
- protect-mcp evaluates Cedar "locally via WASM" = the real Cedar engine, which genuinely discards `in`-on-String forbid rules. So the disclosure (#598) is **essentially correct**, not a false positive. The `.contains()` rewrite (Task 7) is the right fix regardless.

Decision (maintainer-approved): proceed with the Cedar correctness fix (Tasks 7-8), retarget Task 9 to a `cedar validate`-based test that needs no `evaluate`, and in Task 10 reply to #598 acknowledging the reporter is right AND surface the broken-hook finding as its own issue (do NOT blind-fix the hook integration here).

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

- [ ] **Step 2: Confirm the rewritten policy is syntactically well-formed**

`protect-mcp evaluate` does not exist (Task 6), so semantic validation moves to Task 9 (`cedar validate` against the schema). Here, just confirm the rewrite parses: every `forbid` block still ends with a valid `when { … }`, the terminal `permit (principal, action, resource);` is intact, and brackets/quotes balance. If a local `cedar` CLI is present you may pre-check `cedar validate --policies review-agent-governance.cedar` (without schema it checks syntax only); otherwise rely on Task 9.

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
if command -v cedar >/dev/null 2>&1; then
  cedar validate --policies review-agent-governance.cedar --schema review-agent-governance.cedarschema
else
  echo "cedar CLI not present — schema is documentation/validation-only"
fi
```
Expected: `cedar validate` reports success (no validation errors), or the skip message. Note: the shipped hook uses `protect-mcp`, which may not consume this schema — its value is `cedar validate` + documentation.

- [ ] **Step 3: Commit**

```bash
git add plugins/review-agent-governance/policies/review-agent-governance.cedarschema
git commit -m "feat(review-agent-governance): add cedarschema typing context attrs as String (#598)"
```

---

### Task 9: Add a `cedar validate` + textual regression test (no `evaluate` dependency)

Retargeted after Task 6: `protect-mcp evaluate` does not exist, so the test cannot route through protect-mcp. Instead it (a) always-on: greps the policy to ensure no `in`-on-String forbid pattern regresses; (b) when the `cedar` CLI is present: `cedar validate` the policy against the schema, which fails on `in`-on-String and passes on `.contains()`.

**Files:**
- Create: `plugins/review-agent-governance/test/run-tests.sh` (executable)
- Create: `plugins/review-agent-governance/test/README.md`

**Interfaces:** exit `0` all pass, `1` a failure. Part A always runs (needs only grep); Part B prints a SKIP line (does not fail) when `cedar` is absent.

- [ ] **Step 1: Create `test/run-tests.sh`**

```bash
#!/usr/bin/env bash
# run-tests.sh — guard review-agent-governance.cedar against the in-on-String
# forbid bug (#598). Part A (grep) always runs; Part B (cedar validate) runs
# only if the `cedar` CLI is installed, else SKIPs without failing.
# Exit codes: 0 pass, 1 fail.
set -uo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
POLICY="../policies/review-agent-governance.cedar"
SCHEMA="../policies/review-agent-governance.cedarschema"

PASS=0; FAIL=0
pass() { echo "PASS: $1"; PASS=$((PASS+1)); }
fail() { echo "FAIL: $1"; FAIL=$((FAIL+1)); }

echo "=== Part A: no in-on-String forbid pattern (always runs) ==="
# The bug pattern is `context.<attr> in [` inside a forbid rule. The fixed form
# is `[ ... ].contains(context.<attr>)`. Assert the bad pattern is absent.
if grep -nE 'context\.[a-z_]+[[:space:]]+in[[:space:]]*\[' "$POLICY" >/dev/null; then
  fail "policy still uses 'context.<attr> in [ ... ]' (the discarded-forbid bug)"
  grep -nE 'context\.[a-z_]+[[:space:]]+in[[:space:]]*\[' "$POLICY"
else
  pass "no in-on-String forbid pattern present"
fi
# And assert the fixed idiom is actually used.
if grep -qE '\]\.contains\(context\.' "$POLICY"; then
  pass "policy uses [ ... ].contains(context.<attr>)"
else
  fail "policy does not use the expected .contains() idiom"
fi

echo "=== Part B: cedar validate against schema (if cedar CLI present) ==="
if command -v cedar >/dev/null 2>&1; then
  if cedar validate --policies "$POLICY" --schema "$SCHEMA"; then
    pass "cedar validate succeeds (policy is well-typed)"
  else
    fail "cedar validate failed"
  fi
else
  echo "SKIP: 'cedar' CLI not found — Part B skipped (Part A still gates)."
fi

echo ""; echo "Passed: $PASS, Failed: $FAIL"
[ "$FAIL" -eq 0 ] || exit 1
```

- [ ] **Step 2: Create `test/README.md`**

```markdown
# review-agent-governance policy tests

Guards `policies/review-agent-governance.cedar` against the #598 `in`-on-String
forbid bug.

```bash
./run-tests.sh   # exit 0 pass · 1 fail
```

- **Part A** (always runs, needs only `grep`): asserts the policy contains no
  `context.<attr> in [ ... ]` forbid pattern (which Cedar silently discards) and
  uses `[ ... ].contains(context.<attr>)` instead.
- **Part B** (runs only if the `cedar` CLI is installed): `cedar validate` the
  policy against `review-agent-governance.cedarschema`. With the context
  attributes typed as `String`, `cedar validate` rejects the `in`-on-String form
  at load time and accepts `.contains()`.

Note: the shipped runtime is `protect-mcp serve` (Cedar-via-WASM); this test
validates the policy source directly and does not depend on protect-mcp.
```

- [ ] **Step 3: Make executable and run**

```bash
chmod +x plugins/review-agent-governance/test/run-tests.sh
plugins/review-agent-governance/test/run-tests.sh; echo "suite exit=$?"
```
Expected: `exit=0`. Part A passes (policy uses `.contains()` after Task 7); Part B passes if `cedar` is installed, else prints SKIP. A non-zero exit means Part A's regression guard caught the bad pattern — fix the policy.

- [ ] **Step 4: Commit**

```bash
git add plugins/review-agent-governance/test
git commit -m "test(review-agent-governance): guard against in-on-String forbid bug (#598)"
```

---

## Phase C — Integration + triage closes

### Task 10: Final gates, PR, and the outward-facing closes/reply

**Files:** none (verification + GitHub actions).

- [ ] **Step 1: Full repo gates**

```bash
cd "$(git rev-parse --show-toplevel)"   # run from the repo root
make test            # plugin-eval + tools — must pass
make validate STRICT=1
make garden
make generate-all && git status --porcelain   # expect: empty (no harness drift)
```
Expected: all pass; drift check prints nothing.

- [ ] **Step 2: Open the PR** for `fix/issues-591-598` summarizing both fixes; reference issues #591 and #598. Do not merge without maintainer approval.

- [ ] **Step 3: Draft the outward-facing actions (post only after explicit maintainer approval).**

- **#591** — comment that the fix landed in the PR (judge now reads `AssistantMessage`/`ResultMessage` correctly, surfaces "unmeasured" instead of fake 0.5, removed dead config); thank lkjie; close when the PR merges.
- **#598** — reply crediting matiaszabal: the finding is **essentially correct**, not a false positive. protect-mcp evaluates Cedar via the real engine (WASM), which discards `in`-on-String forbid rules. We adopted `[ ... ].contains(context.<attr>)` + a `.cedarschema` + a regression test (PR). Reference `cedar-policy/cedar#2428`. ALSO disclose the adjacent finding we hit while verifying: the plugin's `hooks/hooks.json` targets `protect-mcp evaluate`/`sign` subcommands that don't exist in the pinned `@0.5.5` (it now uses `serve`/`init-hooks`), so the gate doesn't run as shipped — tracked separately (see new issue below). Close #598 when the PR merges.
- **NEW ISSUE (file it)** — open a bug for the broken protect-mcp integration: `review-agent-governance/hooks/hooks.json` (and `protect-mcp/test/run-tests.sh`) invoke non-existent `evaluate`/`sign` subcommands of `protect-mcp@0.5.5`; the current CLI is `serve`/`init-hooks`/`--cedar`. Enforcement does not run as shipped. Recommend regenerating hooks via `protect-mcp init-hooks` (serve-based) and updating the pin/tests. This is the larger defect surfaced by #598's verification.
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
