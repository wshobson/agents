"""Typer CLI for plugin-eval."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig
from plugin_eval.reporter import Reporter

app = typer.Typer(
    name="plugin-eval",
    help="Evaluate Claude Code plugins and skills.",
    add_completion=False,
)
console = Console()


def _detect_target(path: Path) -> str:
    """Return 'skill' if SKILL.md exists, 'plugin' if .claude-plugin/ exists, else 'unknown'."""
    if (path / "SKILL.md").exists():
        return "skill"
    if (path / ".claude-plugin").exists():
        return "plugin"
    return "unknown"


def _run_score(
    path: Path,
    depth: Depth,
    output: str,
    verbose: bool,
    concurrency: int,
    auth: str,
    threshold: float | None,
) -> int:
    """Core scoring logic; returns exit code."""
    if not path.exists():
        console.print(f"[red]Error: Path does not exist: {path}[/red]")
        raise typer.Exit(code=2)

    config = EvalConfig(
        depth=depth,
        output_format=output,
        verbose=verbose,
        concurrency=concurrency,
        auth=auth,
    )
    engine = EvalEngine(config)

    target = _detect_target(path)
    if target == "skill":
        result = engine.evaluate_skill(path)
    elif target == "plugin":
        result = engine.evaluate_plugin(path)
    else:
        # Attempt skill evaluation as fallback
        result = engine.evaluate_skill(path)

    reporter = Reporter()
    if output == "json":
        typer.echo(reporter.to_json(result))
    elif output == "html":
        typer.echo(reporter.to_html(result))
    else:
        # Default: markdown
        typer.echo(reporter.to_markdown(result))

    if (
        threshold is not None
        and result.composite is not None
        and result.composite.score < threshold
    ):
        return 1

    return 0


@app.command()
def score(
    path: Path = typer.Argument(..., help="Plugin or skill directory to evaluate"),  # noqa: B008
    depth: Depth = typer.Option(Depth.STANDARD, help="Evaluation depth"),  # noqa: B008
    output: str = typer.Option("markdown", help="Output format: json|markdown|html"),  # noqa: B008
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),  # noqa: B008
    concurrency: int = typer.Option(4, help="Max concurrent LLM calls"),  # noqa: B008
    auth: str = typer.Option("max", help="Auth mode: max|api-key"),  # noqa: B008
    threshold: float | None = typer.Option(  # noqa: B008
        None, help="Minimum score threshold; exit code 1 if below"
    ),
) -> None:
    """Evaluate a plugin or skill directory and report its quality score."""
    exit_code = _run_score(path, depth, output, verbose, concurrency, auth, threshold)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command()
def certify(
    path: Path = typer.Argument(..., help="Plugin or skill directory to certify"),  # noqa: B008
    output: str = typer.Option("markdown", help="Output format: json|markdown|html"),  # noqa: B008
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),  # noqa: B008
    concurrency: int = typer.Option(4, help="Max concurrent LLM calls"),  # noqa: B008
    auth: str = typer.Option("max", help="Auth mode: max|api-key"),  # noqa: B008
    threshold: float | None = typer.Option(None, help="Minimum score threshold"),  # noqa: B008
) -> None:
    """Certify a plugin or skill (runs at deep depth)."""
    exit_code = _run_score(path, Depth.DEEP, output, verbose, concurrency, auth, threshold)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command()
def init(
    corpus_source: Path = typer.Argument(..., help="Path to plugins directory to index as corpus"),  # noqa: B008
    corpus_dir: Path = typer.Option(  # noqa: B008
        Path.home() / ".plugineval" / "corpus",  # noqa: B008
        help="Where to store corpus index",  # noqa: B008
    ),
) -> None:
    """Initialize corpus from a plugin directory."""
    if not corpus_source.exists():
        console.print(f"[red]Error: Source path does not exist: {corpus_source}[/red]")
        raise typer.Exit(code=2)
    from plugin_eval.corpus import Corpus  # lazy import — Task 10

    corpus = Corpus.init_from_source(corpus_source, corpus_dir)
    console.print(f"[green]Corpus initialized with {corpus.size} skills at {corpus_dir}[/green]")


@app.command()
def compare(
    skill_a: Path = typer.Argument(..., help="First skill directory"),  # noqa: B008
    skill_b: Path = typer.Argument(..., help="Second skill directory"),  # noqa: B008
    depth: Depth = typer.Option(Depth.QUICK, help="Evaluation depth"),  # noqa: B008
    output: str = typer.Option("markdown", help="Output format"),  # noqa: B008
) -> None:
    """Head-to-head comparison of two skills."""
    for p in (skill_a, skill_b):
        if not p.exists():
            console.print(f"[red]Error: Path does not exist: {p}[/red]")
            raise typer.Exit(code=2)
    config = EvalConfig(depth=depth, output_format=output)
    engine = EvalEngine(config)
    result_a = engine.evaluate_skill(skill_a)
    result_b = engine.evaluate_skill(skill_b)
    score_a = result_a.composite.score if result_a.composite else 0
    score_b = result_b.composite.score if result_b.composite else 0
    lines = [
        f"# Head-to-Head: {skill_a.name} vs {skill_b.name}",
        "",
        f"| | {skill_a.name} | {skill_b.name} | Winner |",
        "|---|---|---|---|",
        f"| **Overall** | {score_a:.0f}/100 | {score_b:.0f}/100 | {'A' if score_a > score_b else 'B' if score_b > score_a else 'Tie'} |",
    ]
    if result_a.composite and result_b.composite:
        for da, db in zip(
            result_a.composite.dimensions, result_b.composite.dimensions, strict=False
        ):
            winner = "A" if da.score > db.score else "B" if db.score > da.score else "Tie"
            name = da.name.replace("_", " ").title()
            lines.append(f"| {name} | {da.score:.2f} | {db.score:.2f} | {winner} |")
    console.print("\n".join(lines))
