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
    return AssistantMessage(content=[TextBlock(text=text)], model="claude-sonnet-5")


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

    def test_errored_result_text_does_not_activate(self):
        # An errored SDK run whose result carries diagnostic text used to come
        # back activated=True *and* errored=True, so the same run was counted in
        # both n_activated and n_errored.
        sim = _simresult_from_messages([_result(is_error=True, result="API error")], "p", 10)
        assert sim.errored is True
        assert sim.activated is False
        assert sim.quality_score == 0.0

    def test_errored_run_with_assistant_text_does_not_activate(self):
        # Same rule when the error arrives after some assistant text: the run
        # failed, so it cannot count towards the activation rate.
        sim = _simresult_from_messages(
            [_assistant("x" * 250), _result(is_error=True, result="API error")], "p", 10
        )
        assert sim.errored is True
        assert sim.activated is False
        assert sim.quality_score == 0.0

    def test_errored_run_matches_the_exception_path(self):
        # run_simulation's except branch reports a failed run as
        # activated=False/quality 0.0; an SDK-reported error must look the same.
        sim = _simresult_from_messages([_result(is_error=True, result="boom")], "p", 10)
        assert (sim.activated, sim.quality_score, sim.errored) == (False, 0.0, True)

    def test_tokens_summed_from_usage(self):
        sim = _simresult_from_messages(
            [_assistant("hi"), _result(usage={"input_tokens": 3, "output_tokens": 4})],
            "p",
            10,
        )
        assert sim.tokens == 7

    def test_model_captured_from_assistant_message(self):
        sim = _simresult_from_messages([_assistant("hi"), _result()], "p", 10)
        assert sim.model == "claude-sonnet-5"

    def test_model_is_none_without_an_assistant_message(self):
        sim = _simresult_from_messages([_result(result="x" * 250)], "p", 10)
        assert sim.model is None


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

    def test_errored_runs_do_not_inflate_the_activation_rate(self):
        """An errored run counts once, against the failure rate -- not twice."""
        analyzer = MonteCarloAnalyzer(MonteCarloConfig(n_runs=4))
        results = [
            _simresult_from_messages([_assistant("x" * 250), _result()], "p", 10),
            _simresult_from_messages([_assistant("x" * 250), _result()], "p", 10),
            _simresult_from_messages([_result(is_error=True, result="API error")], "p", 10),
            _simresult_from_messages([_result(is_error=True, result="API error")], "p", 10),
        ]

        stats = analyzer._compute_statistics(results)

        assert stats["triggering"]["n_activated"] == 2
        assert stats["triggering"]["activation_rate"] == pytest.approx(0.5)
        assert stats["failure_rate"]["p_fail"] == pytest.approx(0.5)


class TestMonteCarloModelUsage:
    """Per-sim token usage aggregates by the model the SDK actually reported."""

    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    @patch("plugin_eval.layers.monte_carlo.run_simulation")
    async def test_analyze_skill_records_model_usage(
        self, mock_sim, mock_query_llm, sample_skill_dir: Path
    ):
        # Prompt generation also calls query_llm (Haiku); force the fallback
        # path so this test's usage total reflects only the sims below.
        mock_query_llm.return_value = {"unmeasured": True}
        mock_sim.return_value = SimResult(
            activated=True,
            quality_score=0.82,
            tokens=2800,
            duration_ms=1500,
            model="claude-sonnet-5",
        )
        config = MonteCarloConfig(n_runs=10, concurrency=2)
        analyzer = MonteCarloAnalyzer(config)
        result = await analyzer.analyze_skill(sample_skill_dir)

        assert result.metadata["model_usage"] == {"claude-sonnet-5": 28000}

    @pytest.mark.asyncio
    @patch("plugin_eval.layers.judge.query_llm")
    @patch("plugin_eval.layers.monte_carlo.run_simulation")
    async def test_sims_without_a_reported_model_are_not_attributed(
        self, mock_sim, mock_query_llm, sample_skill_dir: Path
    ):
        # run_simulation's exception path (and any stream lacking an
        # AssistantMessage) leaves model=None -- those tokens can't be
        # attributed to a model and must be skipped, not mis-keyed under "None".
        mock_query_llm.return_value = {"unmeasured": True}
        mock_sim.return_value = SimResult(
            activated=False, quality_score=0.0, tokens=0, duration_ms=0, errored=True, model=None
        )
        config = MonteCarloConfig(n_runs=5, concurrency=2)
        analyzer = MonteCarloAnalyzer(config)
        result = await analyzer.analyze_skill(sample_skill_dir)

        assert result.metadata["model_usage"] == {}


class TestUsageTotalTokens:
    def test_sums_component_token_fields(self):
        assert usage_total_tokens({"input_tokens": 10, "output_tokens": 5}) == 15

    def test_prefers_explicit_total_tokens(self):
        assert usage_total_tokens({"total_tokens": 20, "input_tokens": 1}) == 20

    def test_none_and_empty_are_zero(self):
        assert usage_total_tokens(None) == 0
        assert usage_total_tokens({}) == 0
