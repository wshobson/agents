"""Eval Engine — coordinates all layers and produces composite scores."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from plugin_eval.layers.static import StaticAnalyzer
from plugin_eval.models import (
    Badge,
    CompositeResult,
    DimensionScore,
    EvalConfig,
    LayerResult,
    PluginEvalResult,
)

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
        layers: list[LayerResult] = []

        # Layer 1: Static analysis (always runs)
        static_result = self._static.analyze_skill(skill_dir)
        layers.append(static_result)

        # Layer 2: LLM Judge — will be implemented in Task 8
        if "judge" in self.config.depth.layers:
            pass  # placeholder

        # Layer 3: Monte Carlo — will be implemented in Task 9
        if "monte_carlo" in self.config.depth.layers:
            pass  # placeholder

        composite = self._build_composite(layers)

        return PluginEvalResult(
            plugin_path=str(skill_dir),
            timestamp=datetime.now(UTC).isoformat(),
            config=self.config,
            layers=layers,
            composite=composite,
        )

    def evaluate_plugin(self, plugin_dir: Path) -> PluginEvalResult:
        """Run evaluation on an entire plugin directory (all skills + agents)."""
        layers: list[LayerResult] = []

        # Layer 1: Static analysis of whole plugin
        static_result = self._static.analyze_plugin(plugin_dir)
        layers.append(static_result)

        # Layer 2: LLM Judge — will be implemented in Task 8
        if "judge" in self.config.depth.layers:
            pass  # placeholder

        # Layer 3: Monte Carlo — will be implemented in Task 9
        if "monte_carlo" in self.config.depth.layers:
            pass  # placeholder

        composite = self._build_composite(layers)

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
        mc_scores = mc_result.sub_scores if mc_result else None

        dimension_scores = self._blend_layer_scores(
            static_scores=static_scores,
            judge_scores=judge_scores,
            mc_scores=mc_scores,
        )

        # Compute anti-pattern penalty from static layer
        anti_pattern_count = len(static_result.anti_patterns) if static_result else 0
        penalty = max(0.5, 1.0 - 0.05 * anti_pattern_count)

        # Compute weighted composite score
        raw = sum(
            DIMENSION_WEIGHTS.get(dim, 0.0) * score for dim, score in dimension_scores.items()
        )
        composite_score = min(100.0, max(0.0, raw * 100.0 * penalty))

        # Build DimensionScore objects
        dim_objects: list[DimensionScore] = []
        for dim, score in dimension_scores.items():
            weight = DIMENSION_WEIGHTS.get(dim, 0.0)
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
                # No data — default to 0.5 neutral
                blended[dim] = 0.5
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
