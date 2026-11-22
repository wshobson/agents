"""Write docs/verified/static-scores.md from plugin-eval's static layer.

The static layer reads files only and makes no model calls, so this costs nothing to run:

    uv run --project plugins/plugin-eval python -m tools.verified.static_scores
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT = REPO_ROOT / "docs" / "verified" / "static-scores.md"

# The free plugins that the first Verified workflows are built from.
SOURCE_PLUGINS = {
    "ship-feature": ["ship-mate", "block-no-verify"],
    "debug": ["incident-response", "error-debugging", "debugging-toolkit"],
}


def score_plugin(name: str) -> tuple[float, str]:
    engine = EvalEngine(EvalConfig(depth=Depth.QUICK, output_format="json"))
    composite = engine.evaluate_plugin(REPO_ROOT / "plugins" / name).composite
    if composite is None:
        raise RuntimeError(f"plugin-eval returned no composite score for {name}")
    return composite.score, composite.badge.value


def render(date: str) -> str:
    lines = [
        "# Static scores for the Verified source plugins",
        "",
        "These scores come from the plugin-eval static layer at quick depth. The static layer",
        "reads the plugin's files and checks structure, frontmatter and portability. It makes no",
        "model calls, so it says nothing about whether a workflow finishes a task. Measured pass",
        "rates will appear in [the scorecards](README.md) once runs start.",
        "",
        f"Generated on {date} with:",
        "",
        "```bash",
        "uv run --project plugins/plugin-eval python -m tools.verified.static_scores",
        "```",
        "",
        "| Verified workflow | Source plugin | Version | Static score | Badge |",
        "|---|---|---|---|---|",
    ]
    for workflow, plugins in SOURCE_PLUGINS.items():
        for name in plugins:
            score, badge = score_plugin(name)
            version = _version(name)
            lines.append(
                f"| {workflow} | [{name}](../../plugins/{name}/) | {version} | {score:.1f} | {badge} |"
            )
    return "\n".join(lines) + "\n"


def _version(name: str) -> str:
    manifest = REPO_ROOT / "plugins" / name / ".claude-plugin" / "plugin.json"
    return json.loads(manifest.read_text())["version"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="tools.verified.static_scores")
    parser.add_argument("--date", help="Date to print, YYYY-MM-DD. Defaults to today (UTC).")
    parser.add_argument("--stdout", action="store_true", help="Print instead of writing.")
    args = parser.parse_args(argv)
    text = render(args.date or datetime.now(UTC).strftime("%Y-%m-%d"))
    if args.stdout:
        sys.stdout.write(text)
    else:
        OUTPUT.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
