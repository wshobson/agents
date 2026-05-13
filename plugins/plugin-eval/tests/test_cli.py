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

    def test_plugin_eval_at_deep_depth_emits_downgrade_warning(
        self, sample_plugin_dir: Path
    ) -> None:
        """Plugin-level evaluation only runs the static layer; certify-style
        invocations at deep depth must warn the user that the deeper layers
        were skipped, not silently produce a static-only report.
        """
        result = runner.invoke(
            app,
            ["certify", str(sample_plugin_dir), "--output", "markdown"],
        )
        assert result.exit_code == 0
        # Click 8.3+ exposes stdout/stderr as separate attributes by default.
        assert "warning" in result.stderr.lower()
        assert "plugin-level" in result.stderr.lower()
        assert "deep" in result.stderr.lower()

    def test_plugin_eval_at_quick_depth_does_not_warn(
        self, sample_plugin_dir: Path
    ) -> None:
        """No warning when the requested depth is already static-only."""
        result = runner.invoke(
            app,
            ["score", str(sample_plugin_dir), "--depth", "quick"],
        )
        assert result.exit_code == 0
        assert "warning" not in result.stderr.lower()
