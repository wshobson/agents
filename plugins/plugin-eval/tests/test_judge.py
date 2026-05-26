from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from plugin_eval.layers.judge import JudgeAnalyzer, JudgeConfig


class TestJudgeConfig:
    def test_default_config(self):
        config = JudgeConfig()
        assert config.judges == 1
        assert config.auth == "max"


class TestJudgeAnalyzer:
    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    async def test_assess_triggering(self, mock_query, sample_skill_dir: Path):
        mock_query.return_value = {
            "predictions": [
                {"prompt": "test logging", "should_trigger": True, "would_trigger": True},
                {"prompt": "make coffee", "should_trigger": False, "would_trigger": False},
            ],
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        }
        analyzer = JudgeAnalyzer(JudgeConfig())
        result = await analyzer.assess_triggering(sample_skill_dir)
        assert result["f1"] == 1.0
        mock_query.assert_called()

    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    async def test_assess_orchestration(self, mock_query, sample_skill_dir: Path):
        mock_query.return_value = {
            "score": 0.82,
            "reasoning": "Clean worker role with structured outputs.",
            "evidence": ["Output format documented", "No orchestration logic"],
        }
        analyzer = JudgeAnalyzer(JudgeConfig())
        result = await analyzer.assess_orchestration(sample_skill_dir)
        assert result["score"] == 0.82

    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    async def test_full_analysis(self, mock_query, sample_skill_dir: Path):
        mock_query.side_effect = [
            {"f1": 0.85, "precision": 0.90, "recall": 0.80, "predictions": []},
            {"score": 0.82, "reasoning": "Good", "evidence": []},
            {"score": 0.79, "simulations": []},
            {"score": 0.88, "assessment": "well-scoped"},
        ]
        analyzer = JudgeAnalyzer(JudgeConfig())
        result = await analyzer.analyze_skill(sample_skill_dir)
        assert result.layer == "judge"
        assert result.score > 0
