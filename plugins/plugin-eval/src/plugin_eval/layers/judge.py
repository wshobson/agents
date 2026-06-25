"""Layer 2: LLM Judge — semantic evaluation via Claude, model-tiered, async."""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from plugin_eval.layers._sdk import collect_sdk_output
from plugin_eval.models import LayerResult
from plugin_eval.parser import ParsedSkill, parse_skill

# ---------------------------------------------------------------------------
# Anchored rubrics
# ---------------------------------------------------------------------------

ORCHESTRATION_RUBRIC = """
Score 0.0 — Poor: Skill acts as standalone agent; manages its own tool calls and sub-tasks.
Score 0.25 — Below average: Skill has some orchestration logic mixed with worker tasks.
Score 0.5 — Average: Skill delegates some tasks but still coordinates multi-step flows itself.
Score 0.75 — Good: Skill is mostly a worker; inputs/outputs documented, minimal coordination.
Score 1.0 — Excellent: Pure worker role; composable, clear contracts, no orchestration logic.
""".strip()

SCOPE_RUBRIC = """
Score 0.0 — Too thin: Stub or trivial wrapper with near-zero unique value.
Score 0.25 — Under-scoped: Covers only a narrow slice; misses obvious related tasks.
Score 0.5 — Average: Reasonable scope but either too broad or somewhat narrow.
Score 0.75 — Well-scoped: Covers one coherent domain; neither bloated nor sparse.
Score 1.0 — Perfectly calibrated: Minimal surface area, maximum cohesion, ideal composability.
""".strip()

# ---------------------------------------------------------------------------
# Model resolution
# ---------------------------------------------------------------------------

_MODEL_MAP: dict[str, str] = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-8",
}


def _resolve_model(tier: str) -> str:
    """Map a tier name to a full model ID."""
    return _MODEL_MAP.get(tier, _MODEL_MAP["sonnet"])


# ---------------------------------------------------------------------------
# LLM query helper (abstracted for testability)
# ---------------------------------------------------------------------------


def _extract_and_parse(messages: list) -> dict:
    """Pull assistant text from SDK messages and parse JSON.

    Returns the parsed dict on success, or an {"unmeasured": True, ...} marker
    when the run errored, produced no text, or returned non-JSON.
    """
    output = collect_sdk_output(messages)
    text = output.text.strip()
    raw = text or (output.result or "")
    if output.errored:
        return {
            "unmeasured": True,
            "error": "judge LLM call returned an error result",
            **({"raw": raw} if raw else {}),
        }
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


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


def _measured_score(result: Any, key: str) -> float | None:
    """Return the numeric score for an assessment, or None if it was unmeasured.

    Tolerates non-dict JSON (e.g. a list or bare string) by treating it as
    unmeasured rather than raising.
    """
    if not isinstance(result, dict) or result.get("unmeasured"):
        return None
    val = result.get(key)
    return float(val) if isinstance(val, (int, float)) else None


@dataclass
class JudgeConfig:
    judges: int = 1
    concurrency: int = 4


# ---------------------------------------------------------------------------
# Analyzer
# ---------------------------------------------------------------------------


class JudgeAnalyzer:
    """Semantic skill evaluation using Claude as a judge."""

    def __init__(self, config: JudgeConfig) -> None:
        self.config = config
        self._sem = asyncio.Semaphore(config.concurrency)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def analyze_skill(self, skill_or_dir: Path | ParsedSkill) -> LayerResult:
        """Run all 4 assessments concurrently and return a LayerResult."""
        skill = skill_or_dir if isinstance(skill_or_dir, ParsedSkill) else parse_skill(skill_or_dir)
        triggering, orchestration, output_quality, scope = await asyncio.gather(
            self.assess_triggering(skill),
            self.assess_orchestration(skill),
            self.assess_output_quality(skill),
            self.assess_scope(skill),
        )

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

    # ------------------------------------------------------------------
    # Individual assessments
    # ------------------------------------------------------------------

    async def assess_triggering(self, skill: Path | ParsedSkill) -> dict:
        """Generate 10 synthetic prompts and classify triggering accuracy via Haiku."""
        if isinstance(skill, Path):
            skill = parse_skill(skill)
        model = _resolve_model("haiku")

        system = (
            "You are an expert evaluator of Claude Code skills. "
            "Respond ONLY with valid JSON — no explanation, no markdown fences."
        )
        prompt = f"""Given this skill description:

<description>
{skill.description}
</description>

Generate 10 synthetic user prompts: 5 that SHOULD trigger this skill and 5 that should NOT.
For each prompt, also predict whether a typical Claude model would trigger this skill.

Return JSON matching this schema:
{{
  "predictions": [
    {{"prompt": "...", "should_trigger": true, "would_trigger": true}},
    ...
  ],
  "precision": <float 0-1>,
  "recall": <float 0-1>,
  "f1": <float 0-1>
}}"""

        async with self._sem:
            return await query_llm(prompt, system=system, model=model)

    async def assess_orchestration(self, skill: Path | ParsedSkill) -> dict:
        """Rate orchestration fitness using an anchored rubric via Sonnet."""
        if isinstance(skill, Path):
            skill = parse_skill(skill)
        model = _resolve_model("sonnet")

        system = (
            "You are an expert evaluator of Claude Code skills. "
            "Respond ONLY with valid JSON — no explanation, no markdown fences."
        )
        prompt = f"""Evaluate this skill's orchestration fitness.

A skill should be a pure WORKER — it should NOT orchestrate other tools or agents.
It should accept clear inputs and produce clear outputs.

Rubric:
{ORCHESTRATION_RUBRIC}

Skill content:
<skill>
{skill.raw_content[:3000]}
</skill>

Return JSON:
{{
  "score": <float 0.0-1.0 matching rubric>,
  "reasoning": "<one sentence>",
  "evidence": ["<quote or observation>", ...]
}}"""

        async with self._sem:
            return await query_llm(prompt, system=system, model=model)

    async def assess_output_quality(self, skill: Path | ParsedSkill) -> dict:
        """Simulate 3 tasks and judge output quality via Sonnet."""
        if isinstance(skill, Path):
            skill = parse_skill(skill)
        model = _resolve_model("sonnet")

        system = (
            "You are an expert evaluator of Claude Code skills. "
            "Respond ONLY with valid JSON — no explanation, no markdown fences."
        )
        prompt = f"""Simulate 3 realistic tasks this skill would handle, then evaluate the
expected output quality based on the skill's instructions.

Skill content:
<skill>
{skill.raw_content[:3000]}
</skill>

Return JSON:
{{
  "score": <float 0.0-1.0>,
  "simulations": [
    {{"task": "...", "expected_output": "...", "quality_notes": "..."}}
  ]
}}"""

        async with self._sem:
            return await query_llm(prompt, system=system, model=model)

    async def assess_scope(self, skill: Path | ParsedSkill) -> dict:
        """Evaluate scope calibration using an anchored rubric via Sonnet."""
        if isinstance(skill, Path):
            skill = parse_skill(skill)
        model = _resolve_model("sonnet")

        system = (
            "You are an expert evaluator of Claude Code skills. "
            "Respond ONLY with valid JSON — no explanation, no markdown fences."
        )
        prompt = f"""Evaluate this skill's scope calibration.

Rubric:
{SCOPE_RUBRIC}

Skill content:
<skill>
{skill.raw_content[:3000]}
</skill>

Return JSON:
{{
  "score": <float 0.0-1.0 matching rubric>,
  "assessment": "<one sentence>"
}}"""

        async with self._sem:
            return await query_llm(prompt, system=system, model=model)
