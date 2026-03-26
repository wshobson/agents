from pathlib import Path

import pytest

from plugin_eval.layers.static import StaticAnalyzer
from plugin_eval.models import LayerResult


class TestStaticAnalyzer:
    def test_analyze_valid_skill(self, sample_skill_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(sample_skill_dir)
        assert isinstance(result, LayerResult)
        assert result.layer == "static"
        assert result.score > 0.5
        assert len(result.anti_patterns) == 0

    def test_analyze_poor_skill(self, poor_skill_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(poor_skill_dir)
        assert result.score < 0.7
        flags = [ap.flag for ap in result.anti_patterns]
        assert "OVER_CONSTRAINED" in flags
        assert "MISSING_TRIGGER" in flags

    def test_analyze_plugin(self, sample_plugin_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_plugin(sample_plugin_dir)
        assert result.layer == "static"
        assert result.score > 0.5
        assert "skill_scores" in result.sub_scores
        assert "agent_scores" in result.sub_scores

    def test_anti_pattern_penalty(self):
        analyzer = StaticAnalyzer()
        assert analyzer._anti_pattern_penalty(0) == 1.0
        assert analyzer._anti_pattern_penalty(2) == pytest.approx(0.9)
        assert analyzer._anti_pattern_penalty(10) == 0.5
        assert analyzer._anti_pattern_penalty(20) == 0.5

    def test_description_pushiness_score(self):
        analyzer = StaticAnalyzer()
        good = "Test skill for evaluation. Use when testing plugin-eval. Use PROACTIVELY for quality checks."
        weak = "A skill."
        assert analyzer._description_pushiness(good) > analyzer._description_pushiness(weak)
