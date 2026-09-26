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
    plugins_dir: Path = typer.Option(Path("plugins"), help="The repo's plugins directory"),  # noqa: B008
    marketplace: Path = typer.Option(  # noqa: B008
        Path(".claude-plugin/marketplace.json"), help="Path to the marketplace.json"
    ),
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


@traces_app.command("run")
def traces_run(
    prompts: Path = typer.Option(..., help="JSONL file of prompt records"),  # noqa: B008
    out: Path = typer.Option(..., help="Directory for one <id>.json trace per prompt"),  # noqa: B008
    model: str = typer.Option("claude-opus-5-5", help="Model for the Claude Code sessions"),  # noqa: B008
    total_usd: float = typer.Option(60.0, help="Stop starting traces past this total spend"),  # noqa: B008
    per_trace_usd: float = typer.Option(1.5, help="Spend cap for one trace"),  # noqa: B008
    max_turns: int = typer.Option(12, help="Turn cap for one trace"),  # noqa: B008
    concurrency: int = typer.Option(3, help="Sessions to run at once"),  # noqa: B008
    plugins_dir: Path = typer.Option(Path("plugins"), help="The repo's plugins directory"),  # noqa: B008
    marketplace: Path = typer.Option(  # noqa: B008
        Path(".claude-plugin/marketplace.json"), help="Path to the marketplace.json"
    ),
    seed: int = typer.Option(20260926, help="Seed for choosing distractor plugins"),  # noqa: B008
    limit: int | None = typer.Option(None, help="Run only the first N prompts"),  # noqa: B008
    timeout_s: int = typer.Option(600, help="Seconds before one session is stopped"),  # noqa: B008
    smoke: bool = typer.Option(  # noqa: B008
        False, "--smoke", help="Run the first should_trigger prompt and check its skill fired"
    ),
) -> None:
    """Run prompts through isolated headless Claude Code sessions and save the traces.

    A resumed run keeps every existing trace in the output directory, including error and
    timeout traces that were billed at the cap. To retry a trace, delete its .json and
    .stream.jsonl files.
    """
    import os
    import tempfile
    from functools import partial

    from plugin_eval.traces import runner
    from plugin_eval.traces.models import PromptRecord, TraceRecord
    from plugin_eval.traces.triggering import target_fired

    for p in (prompts, plugins_dir, marketplace):
        if not p.exists():
            console.print(f"[red]Error: Path does not exist: {p}[/red]")
            raise typer.Exit(code=2)
    for name, source_dir in runner.local_plugin_dirs(marketplace).items():
        if source_dir != (plugins_dir / name).resolve():
            console.print(
                f"[red]Error: {marketplace} places {name} at {source_dir}, but --plugins-dir "
                f"gives {(plugins_dir / name).resolve()}. Point both at the same repo.[/red]",
                soft_wrap=True,
            )
            raise typer.Exit(code=2)
    # Split on "\n" only: JSON leaves U+2028 raw inside a query, and splitlines splits there.
    lines = prompts.read_text(encoding="utf-8").split("\n")
    records = [PromptRecord.model_validate_json(line) for line in lines if line.strip()]
    try:
        runner.check_prompt_ids(records)
    except ValueError as exc:
        console.print(f"Error: {exc}", style="red", markup=False, soft_wrap=True)
        raise typer.Exit(code=2) from None
    # Every session needs claude. Check once, before any budget is reserved, so a missing
    # binary cannot turn every prompt into an error trace billed at the cap.
    installed_version = runner.claude_version()
    if not installed_version:
        console.print(
            "[red]Error: claude --version failed, so no session can start. Install Claude "
            "Code or fix PATH, then run again.[/red]",
            soft_wrap=True,
        )
        raise typer.Exit(code=2)
    run = partial(
        runner.run_isolated,
        plugins_dir=plugins_dir.resolve(),
        marketplace_json=marketplace,
        seed=seed,
        model=model,
        per_trace_usd=per_trace_usd,
        max_turns=max_turns,
        timeout_s=timeout_s,
    )
    ledger = runner.BudgetLedger(total_usd=total_usd, per_trace_usd=per_trace_usd)

    if smoke:
        target = next((r for r in records if r.routing == "should_trigger"), None)
        if target is None:
            console.print("[red]Error: No should_trigger prompt to smoke test[/red]")
            raise typer.Exit(code=2)
        # Run into a temporary directory, and replace the previous smoke pair only when a new
        # trace comes back, so a refused reservation or a crash keeps the last result.
        smoke_dir = out / "smoke"
        smoke_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=smoke_dir, prefix=".smoke-run-") as tmp:
            staging = Path(tmp)
            traces = runner.run_batch(
                [target],
                staging,
                1,
                ledger,
                partial(run, raw_dir=staging),
                model=model,
                seed=seed,
                max_turns=max_turns,
                timeout_s=timeout_s,
            )
            trace = traces[0] if traces else None
            if trace is None:
                console.print("[red]Smoke failed: the budget did not allow one trace[/red]")
                raise typer.Exit(code=1)
            stream_name = f"{target.id}{runner.STREAM_SUFFIX}"
            if (staging / stream_name).exists():
                os.replace(staging / stream_name, smoke_dir / stream_name)
            else:
                (smoke_dir / stream_name).unlink(missing_ok=True)
            os.replace(staging / f"{target.id}.json", smoke_dir / f"{target.id}.json")
        console.print(
            f"Smoke {target.id}: invoked {trace.skills_invoked}, "
            f"contaminated {trace.contaminated}, error {trace.error}, "
            f"USD {trace.cost_usd:.2f}. Trace saved to {smoke_dir / (target.id + '.json')}",
            soft_wrap=True,
        )
        problems = []
        if not target_fired(trace):
            problems.append(f"it did not invoke {target.target_skill}")
        if trace.contaminated:
            problems.append(
                f"the session was contaminated ({'; '.join(trace.contamination_reasons)})"
            )
        if problems:
            stream = smoke_dir / f"{target.id}{runner.STREAM_SUFFIX}"
            console.print(
                f"[red]Smoke failed for {target.id}: {' and '.join(problems)}. Fix this "
                f"before a full run. The raw stream is in {stream}.[/red]",
                soft_wrap=True,
            )
            raise typer.Exit(code=1)
        return

    # Traces from earlier runs into the same directory count against the total, so a
    # resumed run cannot spend the whole budget again. Unknown cost counts as the cap.
    earlier = {
        p.stem: TraceRecord.model_validate_json(p.read_text(encoding="utf-8"))
        for p in out.glob("*.json")
    }
    ledger.spent = earlier_usd = sum(runner.billed_usd(t, per_trace_usd) for t in earlier.values())
    selected = records[:limit] if limit is not None else records
    # A resumed run skips ids that already have a trace, so those traces must come from the
    # same prompt and run settings, or one directory would mix traces that saw different
    # plugins or ran under different limits. Check them all before any session starts. A
    # setting that an older trace did not record is empty or zero and is not compared.
    digests: dict[tuple[str, ...], str] = {}

    def mismatches(saved: TraceRecord, record: PromptRecord) -> list[str]:
        found = []
        if saved.prompt != record:
            found.append("prompt")
        if saved.requested_model and saved.requested_model != model:
            found.append("requested_model")
        if saved.seed is not None and saved.seed != seed:
            found.append("seed")
        if saved.per_trace_cap_usd and saved.per_trace_cap_usd != per_trace_usd:
            found.append("per_trace_cap_usd")
        if saved.max_turns and saved.max_turns != max_turns:
            found.append("max_turns")
        if saved.timeout_s and saved.timeout_s != timeout_s:
            found.append("timeout_s")
        if saved.plugins_loaded:
            try:
                expected = runner.choose_plugins(
                    record.target_plugin, marketplace, runner.trace_seed(seed, record.id)
                )
            except ValueError:
                expected = []
            if saved.plugins_loaded != expected:
                found.append("plugins_loaded")
            elif saved.plugins_digest:
                key = tuple(expected)
                if key not in digests:
                    dirs = [(plugins_dir / name).resolve() for name in expected]
                    digests[key] = runner.plugins_digest(dirs)
                if digests[key] != saved.plugins_digest:
                    found.append("plugins_digest")
        if saved.claude_version and saved.claude_version != installed_version:
            found.append("claude_version")
        return found

    for record in selected:
        saved = earlier.get(record.id)
        found = mismatches(saved, record) if saved is not None else []
        if found:
            console.print(
                f"[red]Error: {out / (record.id + '.json')} does not match this run for "
                f"{record.id} ({', '.join(found)} differ). This run uses {prompts}, --model "
                f"{model}, --seed {seed}, --per-trace-usd {per_trace_usd}, --max-turns "
                f"{max_turns}, --timeout-s {timeout_s}, --plugins-dir {plugins_dir}, "
                f"--marketplace {marketplace}, and the installed claude. Pick a new --out "
                "for this run.[/red]",
                soft_wrap=True,
            )
            raise typer.Exit(code=2)
    traces = runner.run_batch(
        selected,
        out,
        concurrency,
        ledger,
        partial(run, raw_dir=out),
        model=model,
        seed=seed,
        max_turns=max_turns,
        timeout_s=timeout_s,
    )
    errors = sum(t.is_error for t in traces)
    contaminated = sum(t.contaminated for t in traces)
    console.print(
        f"{len(traces)} traces written to {out}, {errors} errors, "
        f"{contaminated} contaminated, USD {ledger.spent - earlier_usd:.2f} spent "
        f"(USD {ledger.spent:.2f} including earlier runs)",
        soft_wrap=True,
    )
