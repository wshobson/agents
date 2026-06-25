from pathlib import Path
from unittest.mock import patch

import pytest

from plugin_eval.layers._sdk import usage_total_tokens

# claude-agent-sdk lives in the optional `llm` extra; skip these SDK-object tests
# (rather than fail collection) when a dev installed only the `dev` extra.
pytest.importorskip("claude_agent_sdk")

from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock  # noqa: E402

from plugin_eval.layers.monte_carlo import (  # noqa: E402
    MonteCarloAnalyzer,
    MonteCarloConfig,
    SimResult,
    _simresult_from_messages,
)


def _assistant(text: str) -> AssistantMessage:
    return AssistantMessage(content=[TextBlock(text=text)], model="claude-sonnet-4-6")


def _result(
    *, is_error: bool = False, result: str | None = None, usage: dict | None = None
) -> ResultMessage:
    return ResultMessage(
        subtype="success" if not is_error else "error",
        duration_ms=1,
        duration_api_ms=1,
        is_error=is_error,
        num_turns=1,
        session_id="t",
        result=result,
        usage=usage,
    )


class TestSimResultFromMessages:
    def test_activated_when_assistant_text_present(self):
        sim = _simresult_from_messages([_assistant("x" * 250), _result()], "p", 10)
        assert sim.activated is True
        assert sim.quality_score == 0.5
        assert sim.errored is False

    def test_not_activated_when_no_text(self):
        sim = _simresult_from_messages([_result()], "p", 10)
        assert sim.activated is False
        assert sim.quality_score == 0.0

    def test_errored_result_flagged(self):
        sim = _simresult_from_messages([_result(is_error=True)], "p", 10)
        assert sim.errored is True

    def test_activated_via_result_fallback(self):
        # A run that emits only a terminal ResultMessage.result (no AssistantMessage
        # text) must still count as activated, using the shared result fallback.
        sim = _simresult_from_messages([_result(result="x" * 250)], "p", 10)
        assert sim.activated is True
        assert sim.quality_score == 0.5

    def test_tokens_summed_from_usage(self):
        sim = _simresult_from_messages(
            [_assistant("hi"), _result(usage={"input_tokens": 3, "output_tokens": 4})],
            "p",
            10,
        )
        assert sim.tokens == 7


class TestSimResult:
    def test_sim_result(self):
        sr = SimResult(activated=True, quality_score=0.8, tokens=2500, duration_ms=1200)
        assert sr.activated is True
        assert sr.errored is False


class TestMonteCarloAnalyzer:
    @pytest.mark.asyncio
    @patch("plugin_eval.layers.monte_carlo.run_simulation")
    async def test_run_with_mocked_sims(self, mock_sim, sample_skill_dir: Path):
        mock_sim.return_value = SimResult(
            activated=True, quality_score=0.82, tokens=2800, duration_ms=1500
        )
        config = MonteCarloConfig(n_runs=10, concurrency=2)
        analyzer = MonteCarloAnalyzer(config)
        result = await analyzer.analyze_skill(sample_skill_dir)
        assert result.layer == "monte_carlo"
        assert result.score > 0
        assert "triggering" in result.sub_scores
        assert "output_consistency" in result.sub_scores
        assert "failure_rate" in result.sub_scores

    def test_statistical_analysis(self):
        """Test the statistical analysis on pre-computed sim results."""
        analyzer = MonteCarloAnalyzer(MonteCarloConfig(n_runs=50))
        results = [
            SimResult(activated=True, quality_score=0.8 + i * 0.002, tokens=2500, duration_ms=1200)
            for i in range(48)
        ] + [
            SimResult(
                activated=False, quality_score=0.0, tokens=500, duration_ms=200, errored=True
            ),
            SimResult(activated=True, quality_score=0.75, tokens=8000, duration_ms=5000),
        ]
        stats = analyzer._compute_statistics(results)
        assert stats["triggering"]["activation_rate"] == pytest.approx(0.98)
        assert stats["failure_rate"]["p_fail"] == pytest.approx(0.02)
        assert stats["output_consistency"]["cv"] < 0.15


class TestUsageTotalTokens:
    def test_sums_component_token_fields(self):
        assert usage_total_tokens({"input_tokens": 10, "output_tokens": 5}) == 15

    def test_prefers_explicit_total_tokens(self):
        assert usage_total_tokens({"total_tokens": 20, "input_tokens": 1}) == 20

    def test_none_and_empty_are_zero(self):
        assert usage_total_tokens(None) == 0
        assert usage_total_tokens({}) == 0
