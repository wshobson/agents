"""Layer 2: LLM Judge — semantic evaluation via Claude, model-tiered, async."""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass
from pathlib import Path

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
    "opus": "claude-opus-4-7",
}


def _resolve_model(tier: str) -> str:
    """Map a tier name to a full model ID."""
    return _MODEL_MAP.get(tier, _MODEL_MAP["sonnet"])


# ---------------------------------------------------------------------------
# LLM query helper (abstracted for testability)
# ---------------------------------------------------------------------------


async def query_llm(prompt: str, system: str = "", model: str = "claude-sonnet-4-6") -> dict:
    """Call Claude via the Agent SDK and return a parsed JSON dict.

    Raises RuntimeError if claude-agent-sdk is not installed.
    """
    try:
        from claude_agent_sdk import (  # type: ignore[import-untyped]
            ClaudeAgentOptions,
            ResultMessage,
            query,
        )
    except ImportError as exc:
        raise RuntimeError(
            "claude-agent-sdk is required for LLM judge. Install with: pip install plugin-eval[llm]"
        ) from exc

    full_prompt = prompt
    if system:
        full_prompt = f"{system}\n\n{prompt}"

    result_text = ""
    async for message in query(
        prompt=full_prompt,
        options=ClaudeAgentOptions(
            model=model,
            allowed_tools=[],
        ),
    ):
        if isinstance(message, ResultMessage):
            # ResultMessage contains the final text
            for block in getattr(message, "content", []):
                if hasattr(block, "text"):
                    result_text += block.text

    # Try to parse JSON — handles raw JSON or JSON inside a markdown code block
    stripped = result_text.strip()
    fence_match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", stripped)
    if fence_match:
        stripped = fence_match.group(1).strip()

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return {"raw": result_text, "score": 0.5}


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


@dataclass
class JudgeConfig:
    judges: int = 1
    auth: str = "max"
    concurrency: int = 4
    model_tier: str = "auto"


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

        # Weighted composite: triggering 0.30, orchestration 0.30, output 0.25, scope 0.15
        score = (
            triggering.get("f1", 0.5) * 0.30
            + orchestration.get("score", 0.5) * 0.30
            + output_quality.get("score", 0.5) * 0.25
            + scope.get("score", 0.5) * 0.15
        )
        score = max(0.0, min(1.0, score))

        sub_scores: dict[str, float] = {
            "triggering_accuracy": triggering.get("f1", 0.5),
            "orchestration_fitness": orchestration.get("score", 0.5),
            "output_quality": output_quality.get("score", 0.5),
            "scope_calibration": scope.get("score", 0.5),
        }

        metadata: dict = {
            "triggering": triggering,
            "orchestration": orchestration,
            "output_quality": output_quality,
            "scope": scope,
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
