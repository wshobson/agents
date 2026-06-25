from pathlib import Path
from unittest.mock import patch

import pytest
from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock

from plugin_eval.layers.judge import JudgeAnalyzer, JudgeConfig, _extract_and_parse


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

    def test_errored_result_with_partial_text_includes_raw(self):
        out = _extract_and_parse([_assistant('{"f1": 0.9}'), _result(is_error=True)])
        assert out["unmeasured"] is True
        assert out["raw"] == '{"f1": 0.9}'


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
