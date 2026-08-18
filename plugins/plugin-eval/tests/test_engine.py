from pathlib import Path

import pytest

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig, LayerResult, PluginEvalResult


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

    def test_quick_eval_skill_has_empty_model_usage(self, sample_skill_dir: Path):
        """Static-only (quick) runs never touch the SDK, so model_usage stays empty."""
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)
        assert result.model_usage == {}


class TestMergeModelUsage:
    """EvalEngine._merge_model_usage sums per-model tokens across layers."""

    def test_merges_disjoint_models_across_layers(self):
        layers = [
            LayerResult(layer="static", score=0.9),
            LayerResult(
                layer="judge", score=0.8, metadata={"model_usage": {"claude-haiku-4-5": 10}}
            ),
            LayerResult(
                layer="monte_carlo", score=0.7, metadata={"model_usage": {"claude-sonnet-5": 500}}
            ),
        ]
        merged = EvalEngine._merge_model_usage(layers)
        assert merged == {"claude-haiku-4-5": 10, "claude-sonnet-5": 500}

    def test_sums_the_same_model_name_across_layers(self):
        layers = [
            LayerResult(
                layer="judge", score=0.8, metadata={"model_usage": {"claude-sonnet-5": 300}}
            ),
            LayerResult(
                layer="monte_carlo", score=0.7, metadata={"model_usage": {"claude-sonnet-5": 500}}
            ),
        ]
        merged = EvalEngine._merge_model_usage(layers)
        assert merged == {"claude-sonnet-5": 800}

    def test_static_only_layers_merge_to_empty(self):
        layers = [LayerResult(layer="static", score=0.9)]
        assert EvalEngine._merge_model_usage(layers) == {}
