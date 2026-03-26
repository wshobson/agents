"""Eval Engine — coordinates all layers and produces composite scores."""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime
from pathlib import Path

from plugin_eval.layers.static import StaticAnalyzer, anti_pattern_penalty
from plugin_eval.models import (
    Badge,
    CompositeResult,
    Depth,
    DimensionScore,
    EvalConfig,
    LayerResult,
    PluginEvalResult,
)
from plugin_eval.parser import ParsedSkill, parse_skill

# Top-level dimension weights (must sum to 1.0)
DIMENSION_WEIGHTS: dict[str, float] = {
    "triggering_accuracy": 0.25,
    "orchestration_fitness": 0.20,
    "output_quality": 0.15,
    "scope_calibration": 0.12,
    "progressive_disclosure": 0.10,
    "token_efficiency": 0.06,
    "robustness": 0.05,
    "structural_completeness": 0.03,
    "code_template_quality": 0.02,
    "ecosystem_coherence": 0.02,
}

# Per-dimension blend weights across layers
LAYER_BLENDS: dict[str, dict[str, float]] = {
    "triggering_accuracy": {"static": 0.15, "judge": 0.25, "monte_carlo": 0.60},
    "orchestration_fitness": {"static": 0.10, "judge": 0.70, "monte_carlo": 0.20},
    "output_quality": {"static": 0.00, "judge": 0.40, "monte_carlo": 0.60},
    "scope_calibration": {"static": 0.30, "judge": 0.55, "monte_carlo": 0.15},
    "progressive_disclosure": {"static": 0.80, "judge": 0.20, "monte_carlo": 0.00},
    "token_efficiency": {"static": 0.40, "judge": 0.10, "monte_carlo": 0.50},
    "robustness": {"static": 0.00, "judge": 0.20, "monte_carlo": 0.80},
    "structural_completeness": {"static": 0.90, "judge": 0.10, "monte_carlo": 0.00},
    "code_template_quality": {"static": 0.30, "judge": 0.70, "monte_carlo": 0.00},
    "ecosystem_coherence": {"static": 0.85, "judge": 0.15, "monte_carlo": 0.00},
}

# Maps static sub-score names → dimension names
STATIC_TO_DIMENSION: dict[str, str] = {
    "frontmatter_quality": "triggering_accuracy",
    "orchestration_wiring": "orchestration_fitness",
    "structural_completeness": "structural_completeness",
    "progressive_disclosure": "progressive_disclosure",
    "token_efficiency": "token_efficiency",
    "ecosystem_coherence": "ecosystem_coherence",
}


class EvalEngine:
    """Coordinates evaluation layers and produces composite PluginEvalResult."""

    def __init__(self, config: EvalConfig) -> None:
        self.config = config
        self._static = StaticAnalyzer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def evaluate_skill(self, skill_dir: Path) -> PluginEvalResult:
        """Run evaluation layers on a skill directory and return a result."""
        skill = parse_skill(skill_dir)
        layers: list[LayerResult] = []

        # Layer 1: Static analysis (always runs)
        static_result = self._static.analyze_skill(skill)
        layers.append(static_result)

        # Layer 2: Judge (standard+ depth)
        if self.config.depth in (Depth.STANDARD, Depth.DEEP, Depth.THOROUGH):
            from plugin_eval.layers.judge import JudgeAnalyzer, JudgeConfig

            judge_config = JudgeConfig(
                judges=self.config.judges,
                auth=self.config.auth,
                concurrency=self.config.concurrency,
            )
            judge = JudgeAnalyzer(judge_config)

            # Layer 3: Monte Carlo (deep+ depth) — run together with judge when both active
            if self.config.depth in (Depth.DEEP, Depth.THOROUGH):
                from plugin_eval.layers.monte_carlo import MonteCarloAnalyzer, MonteCarloConfig

                n_runs = self.config.monte_carlo_n or (
                    100 if self.config.depth == Depth.THOROUGH else 50
                )
                mc_config = MonteCarloConfig(
                    n_runs=n_runs,
                    concurrency=self.config.concurrency,
                    auth=self.config.auth,
                )
                mc = MonteCarloAnalyzer(mc_config)

                async def _run_llm_layers(
                    judge: JudgeAnalyzer,
                    mc: MonteCarloAnalyzer,
                    skill: ParsedSkill,
                ) -> tuple[LayerResult, LayerResult]:
                    judge_result = await judge.analyze_skill(skill)
                    mc_result = await mc.analyze_skill(skill)
                    return judge_result, mc_result

                judge_result, mc_result = asyncio.run(_run_llm_layers(judge, mc, skill))
                layers.append(judge_result)
                layers.append(mc_result)
            else:
                judge_result = asyncio.run(judge.analyze_skill(skill))
                layers.append(judge_result)

        composite = self._build_composite(layers)

        return PluginEvalResult(
            plugin_path=str(skill_dir),
            timestamp=datetime.now(UTC).isoformat(),
            config=self.config,
            layers=layers,
            composite=composite,
        )

    def evaluate_plugin(self, plugin_dir: Path) -> PluginEvalResult:
        """Run evaluation on an entire plugin directory (all skills + agents).

        Note: Plugin-level evaluation currently only runs Layer 1 (static).
        Judge and Monte Carlo require per-skill evaluation. The confidence
        label is always "Estimated" regardless of requested depth.
        """
        layers: list[LayerResult] = []

        # Layer 1: Static analysis of whole plugin
        static_result = self._static.analyze_plugin(plugin_dir)
        layers.append(static_result)

        # Plugin-level composite uses overall static score mapped to all
        # static-measurable dimensions (plugin result lacks per-dimension breakdown)
        static_overall = static_result.score
        dimension_scores = {dim: static_overall for dim in STATIC_TO_DIMENSION.values()}
        anti_pattern_count = len(static_result.anti_patterns)
        composite = self._assemble_composite(dimension_scores, anti_pattern_count)

        # Plugin-level eval only has static data — always "Estimated"
        # regardless of requested depth (judge/MC are per-skill only)
        composite.confidence_label = Depth.QUICK.confidence_label

        return PluginEvalResult(
            plugin_path=str(plugin_dir),
            timestamp=datetime.now(UTC).isoformat(),
            config=self.config,
            layers=layers,
            composite=composite,
        )

    # ------------------------------------------------------------------
    # Composite construction
    # ------------------------------------------------------------------

    def _build_composite(self, layers: list[LayerResult]) -> CompositeResult:
        """Build the CompositeResult from available layer results."""
        static_result = next((lr for lr in layers if lr.layer == "static"), None)
        judge_result = next((lr for lr in layers if lr.layer == "judge"), None)
        mc_result = next((lr for lr in layers if lr.layer == "monte_carlo"), None)

        static_scores = self._map_static_to_dimensions(static_result) if static_result else None
        judge_scores = judge_result.sub_scores if judge_result else None
        mc_scores = self._normalize_mc_scores(mc_result.sub_scores) if mc_result else None

        dimension_scores = self._blend_layer_scores(
            static_scores=static_scores,
            judge_scores=judge_scores,
            mc_scores=mc_scores,
        )

        anti_pattern_count = len(static_result.anti_patterns) if static_result else 0
        return self._assemble_composite(dimension_scores, anti_pattern_count)

    def _assemble_composite(
        self, dimension_scores: dict[str, float], anti_pattern_count: int
    ) -> CompositeResult:
        """Build a CompositeResult from blended dimension scores and anti-pattern count."""
        penalty = anti_pattern_penalty(anti_pattern_count)

        # Split into measured vs unmeasured dimensions
        # Dimensions absent from dimension_scores are also treated as unmeasured
        measured = {d: s for d, s in dimension_scores.items() if s >= 0.0}
        unmeasured = {d for d, s in dimension_scores.items() if s < 0.0} | (
            set(DIMENSION_WEIGHTS) - set(dimension_scores)
        )

        # Renormalize weights to only measured dimensions
        measured_weight_sum = sum(DIMENSION_WEIGHTS.get(d, 0.0) for d in measured)
        if measured_weight_sum > 0:
            raw = sum(
                (DIMENSION_WEIGHTS.get(dim, 0.0) / measured_weight_sum) * score
                for dim, score in measured.items()
            )
        else:
            raw = 0.0
        composite_score = min(100.0, max(0.0, raw * 100.0 * penalty))

        # Build DimensionScore objects
        dim_objects: list[DimensionScore] = []
        for dim in DIMENSION_WEIGHTS:
            weight = DIMENSION_WEIGHTS[dim]
            if dim in unmeasured:
                dim_objects.append(
                    DimensionScore(
                        name=dim,
                        weight=weight,
                        score=0.0,
                        grade="—",
                    )
                )
            else:
                score = measured.get(dim, 0.0)
                dim_objects.append(
                    DimensionScore(
                        name=dim,
                        weight=weight,
                        score=score,
                        grade=self._score_to_grade(score * 100.0),
                    )
                )

        badge = Badge.from_scores(composite_score, elo=None)

        return CompositeResult(
            score=composite_score,
            anti_pattern_penalty=penalty,
            dimensions=dim_objects,
            badge=badge,
            confidence_label=self.config.depth.confidence_label,
        )

    # ------------------------------------------------------------------
    # Layer blending
    # ------------------------------------------------------------------

    def _blend_layer_scores(
        self,
        static_scores: dict[str, float] | None,
        judge_scores: dict[str, float] | None,
        mc_scores: dict[str, float] | None,
    ) -> dict[str, float]:
        """Blend dimension scores across available layers, renormalizing weights."""
        blended: dict[str, float] = {}

        for dim in DIMENSION_WEIGHTS:
            blends = LAYER_BLENDS.get(dim, {"static": 1.0, "judge": 0.0, "monte_carlo": 0.0})

            # Determine which layers have a score for this dimension
            available: dict[str, float] = {}
            if static_scores is not None and dim in static_scores:
                available["static"] = static_scores[dim]
            if judge_scores is not None and dim in judge_scores:
                available["judge"] = judge_scores[dim]
            if mc_scores is not None and dim in mc_scores:
                available["monte_carlo"] = mc_scores[dim]

            if not available:
                # No data — mark as unmeasured (negative sentinel)
                blended[dim] = -1.0
                continue

            # Renormalize blend weights to only available layers
            total_weight = sum(blends.get(layer, 0.0) for layer in available)
            if total_weight == 0.0:
                # All available layers have zero blend weight — equal weighting
                blended[dim] = sum(available.values()) / len(available)
            else:
                blended[dim] = sum(
                    available[layer] * blends.get(layer, 0.0) / total_weight for layer in available
                )

        return blended

    def _map_static_to_dimensions(self, static_result: LayerResult) -> dict[str, float]:
        """Map static sub-scores to dimension names."""
        mapped: dict[str, float] = {}
        for sub_name, dim_name in STATIC_TO_DIMENSION.items():
            if sub_name in static_result.sub_scores:
                value = static_result.sub_scores[sub_name]
                if isinstance(value, (int, float)):
                    mapped[dim_name] = float(value)
        return mapped

    @staticmethod
    def _normalize_mc_scores(sub_scores: dict) -> dict[str, float]:
        """Extract numeric dimension scores from Monte Carlo nested sub_scores.

        MC sub_scores contain nested dicts like {"triggering": {"activation_rate": 0.92, ...}}.
        This normalizes them to flat dimension → float for blending.
        """
        normalized: dict[str, float] = {}
        triggering = sub_scores.get("triggering", {})
        if isinstance(triggering, dict):
            normalized["triggering_accuracy"] = triggering.get("activation_rate", 0.0)
        consistency = sub_scores.get("output_consistency", {})
        if isinstance(consistency, dict):
            normalized["output_quality"] = consistency.get("mean_quality", 0.0)
        failure = sub_scores.get("failure_rate", {})
        if isinstance(failure, dict):
            normalized["robustness"] = 1.0 - failure.get("p_fail", 0.0)
        token_eff = sub_scores.get("token_efficiency", {})
        if isinstance(token_eff, dict):
            normalized["token_efficiency"] = token_eff.get("efficiency_norm", 0.0)
        return normalized

    # ------------------------------------------------------------------
    # Grading
    # ------------------------------------------------------------------

    def _score_to_grade(self, score: float) -> str:
        """Convert a 0–100 score to a letter grade."""
        if score >= 97:
            return "A+"
        elif score >= 93:
            return "A"
        elif score >= 90:
            return "A-"
        elif score >= 87:
            return "B+"
        elif score >= 83:
            return "B"
        elif score >= 80:
            return "B-"
        elif score >= 77:
            return "C+"
        elif score >= 73:
            return "C"
        elif score >= 70:
            return "C-"
        elif score >= 67:
            return "D+"
        elif score >= 63:
            return "D"
        elif score >= 60:
            return "D-"
        else:
            return "F"
