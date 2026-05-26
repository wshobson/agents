import pytest
from pydantic import ValidationError

from plugin_eval.models import (
    AntiPattern,
    Badge,
    CompositeResult,
    Depth,
    DimensionScore,
    EloMatchup,
    EloResult,
    EvalConfig,
    LayerResult,
    PluginEvalResult,
    StaticSubScore,
)


class TestEvalConfig:
    def test_default_config(self):
        config = EvalConfig()
        assert config.depth == Depth.STANDARD
        assert config.concurrency == 4
        assert config.auth == "max"

    def test_custom_config(self):
        config = EvalConfig(depth=Depth.DEEP, concurrency=8)
        assert config.depth == Depth.DEEP
        assert config.concurrency == 8

    def test_concurrency_bounds(self):
        with pytest.raises(ValidationError):
            EvalConfig(concurrency=0)
        with pytest.raises(ValidationError):
            EvalConfig(concurrency=21)


class TestDimensionScore:
    def test_valid_score(self):
        ds = DimensionScore(name="triggering_accuracy", weight=0.25, score=0.85)
        assert ds.weighted_score == pytest.approx(0.2125)

    def test_score_bounds(self):
        with pytest.raises(ValidationError):
            DimensionScore(name="x", weight=0.1, score=1.5)
        with pytest.raises(ValidationError):
            DimensionScore(name="x", weight=0.1, score=-0.1)

    def test_optional_ci(self):
        ds = DimensionScore(
            name="triggering_accuracy",
            weight=0.25,
            score=0.85,
            ci_lower=0.80,
            ci_upper=0.90,
        )
        assert ds.ci_lower == 0.80


class TestAntiPattern:
    def test_anti_pattern(self):
        ap = AntiPattern(flag="OVER_CONSTRAINED", description="Too many MUSTs", severity=0.05)
        assert ap.flag == "OVER_CONSTRAINED"


class TestLayerResult:
    def test_layer_result(self):
        lr = LayerResult(layer="static", score=0.91)
        assert lr.score == 0.91


class TestEloMatchup:
    def test_matchup(self):
        m = EloMatchup(
            opponent="distributed-tracing",
            opponent_elo=1540,
            result="loss",
            score=0.44,
        )
        assert m.result in ("win", "loss", "draw")

    def test_invalid_result(self):
        with pytest.raises(ValidationError):
            EloMatchup(opponent="x", opponent_elo=1500, result="tie", score=0.5)


class TestBadge:
    def test_badge_from_scores_gold(self):
        badge = Badge.from_scores(composite=85, elo=1520)
        assert badge == Badge.GOLD

    def test_badge_from_scores_platinum(self):
        badge = Badge.from_scores(composite=92, elo=1650)
        assert badge == Badge.PLATINUM

    def test_badge_requires_both(self):
        badge = Badge.from_scores(composite=95, elo=1200)
        assert badge == Badge.NO_BADGE

    def test_badge_no_elo(self):
        badge = Badge.from_scores(composite=85, elo=None)
        assert badge == Badge.GOLD
