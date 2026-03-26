from pathlib import Path

from typer.testing import CliRunner

from plugin_eval.cli import app

runner = CliRunner()


class TestCLI:
    def test_score_quick(self, sample_skill_dir: Path):
        result = runner.invoke(app, ["score", str(sample_skill_dir), "--depth", "quick"])
        assert result.exit_code == 0

    def test_score_json_output(self, sample_skill_dir: Path):
        result = runner.invoke(
            app, ["score", str(sample_skill_dir), "--depth", "quick", "--output", "json"]
        )
        assert result.exit_code == 0
        assert '"composite"' in result.stdout

    def test_score_markdown_output(self, sample_skill_dir: Path):
        result = runner.invoke(
            app, ["score", str(sample_skill_dir), "--depth", "quick", "--output", "markdown"]
        )
        assert result.exit_code == 0
        assert "PluginEval Report" in result.stdout

    def test_score_nonexistent_path(self, tmp_path: Path):
        result = runner.invoke(app, ["score", str(tmp_path / "nonexistent")])
        assert result.exit_code == 2
