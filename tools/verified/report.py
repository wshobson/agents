"""Turn result files into a scorecard table."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from statistics import median

from tools.verified.models import RunResult

from plugin_eval.stats import wilson_score_ci

# A run whose harness failed (crash, timeout, API error). It says nothing about the
# workflow, so it is left out of the pass rate and counted on its own.
HARNESS_ERROR = "harness_error"


def load_results(root: Path) -> list[RunResult]:
    return [
        RunResult.model_validate_json(path.read_text(encoding="utf-8"))
        for path in sorted(root.rglob("*.json"))
        if path.name != "result.schema.json"
    ]


def interval(passes: int, runs: int) -> tuple[float, float]:
    """Wilson 95% interval for passes out of runs (z = 1.96)."""
    return wilson_score_ci(passes, runs, confidence=0.95)


def render_markdown(results: list[RunResult]) -> str:
    header = (
        "| Workflow | Version | Harness | Model | Pass rate (95% interval) | "
        "Median tokens | Median time | Last run |\n"
        "|---|---|---|---|---|---|---|---|\n"
    )
    if not results:
        return header + "| No runs yet | | | | | | | |\n"
    groups: dict[tuple[str, str, str, str, str], list[RunResult]] = defaultdict(list)
    for r in results:
        groups[(r.workflow, r.workflow_version, r.harness, r.harness_version, r.model)].append(r)
    rows = []
    for (workflow, version, harness, harness_version, model), all_runs in sorted(groups.items()):
        runs = [r for r in all_runs if HARNESS_ERROR not in r.failed_checks]
        errors = len(all_runs) - len(runs)
        error_text = f"; {errors} harness errors left out" if errors else ""
        last = max(r.run_at for r in all_runs)[:10]
        if not runs:
            rows.append(
                f"| {workflow} | {version} | {harness} {harness_version} | {model} | "
                f"no scored runs{error_text} | n/a | n/a | {last} |\n"
            )
            continue
        k = sum(r.passed for r in runs)
        n = len(runs)
        low, high = interval(k, n)
        tokens = [
            (r.tokens_in or 0) + (r.tokens_out or 0)
            for r in runs
            if r.tokens_in is not None or r.tokens_out is not None
        ]
        token_text = f"{median(tokens) / 1000:.0f}k" if tokens else "n/a"
        minutes = median(r.wall_seconds for r in runs) / 60
        rows.append(
            f"| {workflow} | {version} | {harness} {harness_version} | {model} | "
            f"{k}/{n}, {k / n:.0%} ({low:.0%} to {high:.0%}){error_text} | {token_text} | "
            f"{minutes:.1f} min | {last} |\n"
        )
    return header + "".join(rows)
