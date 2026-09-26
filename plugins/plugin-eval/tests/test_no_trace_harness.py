"""Guards for the removal of the trace harness and the Anthropic prompt writer."""

import tomllib
from pathlib import Path

from typer.testing import CliRunner

from plugin_eval.cli import app

SRC = Path(__file__).resolve().parents[1] / "src" / "plugin_eval"


def test_cli_has_no_traces_command() -> None:
    result = CliRunner().invoke(app, ["traces", "--help"])
    assert result.exit_code != 0


def test_package_does_not_import_the_anthropic_sdk() -> None:
    hits = [p for p in SRC.rglob("*.py") if "import anthropic" in p.read_text(encoding="utf-8")]
    assert hits == []


def test_pyproject_has_no_api_extra() -> None:
    data = tomllib.loads((SRC.parents[1] / "pyproject.toml").read_text(encoding="utf-8"))
    assert "api" not in data["project"]["optional-dependencies"]
