import json
from pathlib import Path

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig
from plugin_eval.reporter import Reporter


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
