from pathlib import Path

import pytest

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig, PluginEvalResult


class TestEvalEngine:
    def test_quick_eval_skill(self, sample_skill_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)
        assert isinstance(result, PluginEvalResult)
        assert len(result.layers) == 1
        assert result.layers[0].layer == "static"
        assert result.composite is not None
        assert result.composite.confidence_label == "Estimated"

    def test_quick_eval_plugin(self, sample_plugin_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_plugin(sample_plugin_dir)
        assert isinstance(result, PluginEvalResult)
        assert result.composite.score > 0

    def test_composite_score_within_bounds(self, sample_skill_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)
        assert 0 <= result.composite.score <= 100

    def test_layer_blend_renormalization(self):
        """When only L1 is available, L1 weights should renormalize to 1.0."""
        engine = EvalEngine(EvalConfig(depth=Depth.QUICK))
        blended = engine._blend_layer_scores(
            static_scores={"triggering_accuracy": 0.9, "orchestration_fitness": 0.8},
            judge_scores=None,
            mc_scores=None,
        )
        assert blended["triggering_accuracy"] > 0
        assert blended["orchestration_fitness"] > 0
