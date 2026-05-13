import json
from pathlib import Path

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig
from plugin_eval.reporter import Reporter, _effective_depth


class TestReporter:
    def test_json_output(self, sample_skill_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)

        reporter = Reporter()
        output = reporter.to_json(result)
        parsed = json.loads(output)
        assert "composite" in parsed
        assert "layers" in parsed
        assert parsed["composite"]["confidence_label"] == "Estimated"

    def test_markdown_output(self, sample_skill_dir: Path):
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)

        reporter = Reporter()
        output = reporter.to_markdown(result)
        assert "# PluginEval Report" in output
        assert "Overall Score" in output
        assert "Layer Breakdown" in output
        assert "Dimension Scores" in output


class TestDepthDowngradeWarning:
    """When plugin-level evaluation silently downgrades a deep/standard request
    to static-only, the reporter must surface the downgrade in-band so the
    consumer cannot mistake the score for a deeply-evaluated one.
    """

    def test_effective_depth_matches_layers_run(self, sample_skill_dir: Path) -> None:
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)
        assert _effective_depth(result) is Depth.QUICK

    def test_markdown_shows_no_warning_when_depth_was_honored(
        self, sample_skill_dir: Path
    ) -> None:
        config = EvalConfig(depth=Depth.QUICK)
        engine = EvalEngine(config)
        result = engine.evaluate_skill(sample_skill_dir)

        output = Reporter().to_markdown(result)
        assert "(requested)" not in output
        assert "downgraded" not in output

    def test_markdown_shows_warning_when_plugin_eval_downgrades_depth(
        self, sample_plugin_dir: Path
    ) -> None:
        # Plugin-level eval at deep depth: the engine runs only the static
        # layer regardless. The report must say so clearly.
        config = EvalConfig(depth=Depth.DEEP)
        engine = EvalEngine(config)
        result = engine.evaluate_plugin(sample_plugin_dir)

        output = Reporter().to_markdown(result)
        assert "deep (requested)" in output
        assert "quick (effective)" in output
        assert "downgraded" in output

    def test_markdown_shows_warning_when_standard_depth_is_downgraded(
        self, sample_plugin_dir: Path
    ) -> None:
        config = EvalConfig(depth=Depth.STANDARD)
        engine = EvalEngine(config)
        result = engine.evaluate_plugin(sample_plugin_dir)

        output = Reporter().to_markdown(result)
        assert "standard (requested)" in output
        assert "quick (effective)" in output
