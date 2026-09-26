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
stderr_console = Console(stderr=True)

EXPERIMENTAL_NOTE = (
    "note: the judge and Monte Carlo layers are experimental and not validated "
    "against human labels; see evals/README.md"
)


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
    )
    engine = EvalEngine(config)

    target = _detect_target(path)
    if target == "skill":
        if depth != Depth.QUICK:
            typer.echo(EXPERIMENTAL_NOTE, err=True)
        result = engine.evaluate_skill(path)
    elif target == "plugin":
        if depth != Depth.QUICK:
            stderr_console.print(
                f"[yellow]warning:[/yellow] plugin-level evaluation only runs the "
                f"static layer; judge and Monte Carlo layers require per-skill "
                f"evaluation. Requested depth [bold]{depth.value}[/bold] will be "
                f"served from the static layer only — confidence label will be "
                f"[bold]Estimated[/bold] regardless. To use the deeper layers, "
                f"point at an individual skill directory."
            )
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

    judge_layer = next((lr for lr in result.layers if lr.layer == "judge"), None)
    if judge_layer is not None:
        unmeasured = judge_layer.metadata.get("unmeasured") or []
        if unmeasured:
            stderr_console.print(
                f"[yellow]warning:[/yellow] LLM judge could not measure "
                f"{', '.join(unmeasured)}; composite computed from the remaining "
                f"layers. Check that claude-agent-sdk is installed and a model is "
                f"configured (run with --verbose for details)."
            )

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
    threshold: float | None = typer.Option(  # noqa: B008
        None, help="Minimum score threshold; exit code 1 if below"
    ),
) -> None:
    """Evaluate a plugin or skill directory and report its quality score."""
    exit_code = _run_score(path, depth, output, verbose, concurrency, threshold)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)


@app.command()
def certify(
    path: Path = typer.Argument(..., help="Plugin or skill directory to certify"),  # noqa: B008
    output: str = typer.Option("markdown", help="Output format: json|markdown|html"),  # noqa: B008
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),  # noqa: B008
    concurrency: int = typer.Option(4, help="Max concurrent LLM calls"),  # noqa: B008
    threshold: float | None = typer.Option(None, help="Minimum score threshold"),  # noqa: B008
) -> None:
    """Certify a plugin or skill (runs at deep depth)."""
    exit_code = _run_score(path, Depth.DEEP, output, verbose, concurrency, threshold)
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
    if depth != Depth.QUICK:
        typer.echo(EXPERIMENTAL_NOTE, err=True)
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


traces_app = typer.Typer(help="Build prompts and traces for error analysis.")
app.add_typer(traces_app, name="traces")


@traces_app.command("prompts")
def traces_prompts(
    plugins_dir: Path = typer.Option(..., help="The repo's plugins directory"),  # noqa: B008
    marketplace: Path = typer.Option(..., help="Path to .claude-plugin/marketplace.json"),  # noqa: B008
    n_skills: int = typer.Option(30, help="Number of skills to sample"),  # noqa: B008
    seed: int = typer.Option(20260926, help="Seed for sampling and tuple building"),  # noqa: B008
    out: Path = typer.Option(..., help="JSONL file to write"),  # noqa: B008
    max_usd: float = typer.Option(5.0, help="Stop writing before API spend could pass this"),  # noqa: B008
    dry_run: bool = typer.Option(False, "--dry-run", help="Write tuples without queries"),  # noqa: B008
) -> None:
    """Sample skills, build prompt tuples, and write one user message per tuple."""
    from plugin_eval.traces.prompts import (
        AnthropicQueryWriter,
        build_tuples,
        render_queries,
        sample_skills,
    )

    for p in (plugins_dir, marketplace):
        if not p.exists():
            console.print(f"[red]Error: Path does not exist: {p}[/red]")
            raise typer.Exit(code=2)
    skills = sample_skills(plugins_dir, marketplace, n=n_skills, seed=seed)
    if not skills:
        console.print(f"[red]Error: No local skills found under {plugins_dir}[/red]")
        raise typer.Exit(code=2)
    tuples = build_tuples(skills, seed=seed)
    if dry_run:
        rows = tuples
    else:
        rows = render_queries(
            tuples,
            skill_text=lambda plugin, skill: (
                plugins_dir / plugin / "skills" / skill / "SKILL.md"
            ).read_text(encoding="utf-8"),
            client=AnthropicQueryWriter(),
            max_usd=max_usd,
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(row.model_dump_json() + "\n" for row in rows), encoding="utf-8")
    console.print(f"Wrote {len(rows)} rows for {len(tuples)} tuples to {out}")
