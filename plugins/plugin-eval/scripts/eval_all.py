"""Batch-evaluate every local plugin and write per-plugin JSON + a summary report.

Runs `plugin-eval score` (via the library, not the CLI subprocess) on every
plugin directory under `plugins/`. External git-subdir plugins are skipped
since their source does not exist locally. Outputs:

  reports/<plugin>.json          — raw result per plugin
  reports/summary.md             — aggregated markdown report
  reports/summary.json           — machine-readable aggregate

Intended for CI usage but works locally too:

  uv run python scripts/eval_all.py --depth quick
  uv run python scripts/eval_all.py --depth standard --output-dir /tmp/reports
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from plugin_eval.engine import EvalEngine
from plugin_eval.models import Depth, EvalConfig, PluginEvalResult

REPO_ROOT = Path(__file__).resolve().parents[3]
PLUGINS_DIR = REPO_ROOT / "plugins"

DEPTH_MAP = {
    "quick": Depth.QUICK,
    "standard": Depth.STANDARD,
    "deep": Depth.DEEP,
    "thorough": Depth.THOROUGH,
}


@dataclass
class PluginRow:
    name: str
    score: float | None
    badge: str | None
    confidence: str | None
    ci_lower: float | None
    ci_upper: float | None
    anti_patterns: list[str]
    weakest_dimensions: list[tuple[str, float]]
    duration_ms: int | None
    errored: bool
    error: str | None = None


def discover_plugins() -> list[Path]:
    return sorted(
        p
        for p in PLUGINS_DIR.iterdir()
        if p.is_dir() and (p / ".claude-plugin" / "plugin.json").exists()
    )


def row_from_result(name: str, result: PluginEvalResult, duration_ms: int) -> PluginRow:
    comp = result.composite
    if comp is None:
        return PluginRow(
            name=name,
            score=None,
            badge=None,
            confidence=None,
            ci_lower=None,
            ci_upper=None,
            anti_patterns=[],
            weakest_dimensions=[],
            duration_ms=duration_ms,
            errored=True,
            error="No composite score produced",
        )

    # Collect unique anti-pattern flags across layers
    seen: set[str] = set()
    anti_patterns: list[str] = []
    for layer in result.layers:
        for ap in getattr(layer, "anti_patterns", []) or []:
            flag = getattr(ap, "flag", None) or str(ap)
            if flag and flag not in seen:
                seen.add(flag)
                anti_patterns.append(flag)

    # Weakest 3 dimensions (by weighted_score)
    dims = sorted(
        comp.dimensions,
        key=lambda d: (d.weighted_score if d.weight > 0 else 1.0),
    )[:3]
    weakest = [(d.name, d.score) for d in dims if d.weight > 0]

    badge_val = comp.badge.value if hasattr(comp.badge, "value") else str(comp.badge)
    return PluginRow(
        name=name,
        score=comp.score,
        badge=badge_val,
        confidence=comp.confidence_label,
        ci_lower=comp.ci_lower,
        ci_upper=comp.ci_upper,
        anti_patterns=anti_patterns,
        weakest_dimensions=weakest,
        duration_ms=duration_ms,
        errored=False,
    )


def evaluate_one(
    plugin_dir: Path, config: EvalConfig, output_dir: Path
) -> PluginRow:
    start = time.monotonic()
    name = plugin_dir.name
    engine = EvalEngine(config)
    try:
        result = engine.evaluate_plugin(plugin_dir)
    except Exception as exc:
        return PluginRow(
            name=name,
            score=None,
            badge=None,
            confidence=None,
            ci_lower=None,
            ci_upper=None,
            anti_patterns=[],
            weakest_dimensions=[],
            duration_ms=int((time.monotonic() - start) * 1000),
            errored=True,
            error=f"{type(exc).__name__}: {exc}",
        )

    duration_ms = int((time.monotonic() - start) * 1000)
    (output_dir / f"{name}.json").write_text(result.model_dump_json(indent=2))
    return row_from_result(name, result, duration_ms)


def format_score(v: float | None) -> str:
    """Composite scores are 0-100."""
    return f"{v:.1f}" if v is not None else "—"


def format_ci(lo: float | None, hi: float | None) -> str:
    if lo is None or hi is None:
        return "—"
    return f"[{lo:.1f}–{hi:.1f}]"


def format_dim_score(v: float) -> str:
    """Dimension scores are 0-1, expressed as 0-100 for readability."""
    return f"{v * 100:.0f}"


def build_summary_md(rows: list[PluginRow], depth: str, started_at: str) -> str:
    total = len(rows)
    errored = sum(1 for r in rows if r.errored)
    scored = [r for r in rows if not r.errored and r.score is not None]
    scored.sort(key=lambda r: r.score or 0.0)

    badges: dict[str, int] = {}
    for r in scored:
        key = r.badge or "none"
        badges[key] = badges.get(key, 0) + 1

    mean_score = (
        sum((r.score or 0.0) for r in scored) / len(scored) if scored else 0.0
    )

    lines: list[str] = []
    lines.append(f"# Plugin Eval Report — depth: `{depth}`")
    lines.append("")
    lines.append(f"_Generated: {started_at}_")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Plugins evaluated: **{total}** ({errored} errored)")
    lines.append(f"- Mean score: **{mean_score:.1f}** / 100")
    badge_line = ", ".join(f"{k}: {v}" for k, v in badges.items() if v > 0)
    lines.append(f"- Badges: {badge_line or 'none'}")
    lines.append("")

    # Highlight anything scoring below 60 or with anti-patterns
    concerning = [
        r for r in scored if (r.score or 0.0) < 60.0 or r.anti_patterns
    ]
    if concerning:
        lines.append(f"## Issues requiring attention ({len(concerning)})")
        lines.append("")
        lines.append("| Plugin | Score | Badge | Anti-patterns | Weakest dimensions |")
        lines.append("|---|---|---|---|---|")
        for r in concerning:
            ap = ", ".join(r.anti_patterns) if r.anti_patterns else "—"
            weak = (
                ", ".join(f"{n} ({format_dim_score(s)})" for n, s in r.weakest_dimensions)
                or "—"
            )
            lines.append(
                f"| `{r.name}` | {format_score(r.score)} | {r.badge or '—'} | {ap} | {weak} |"
            )
        lines.append("")

    if errored:
        lines.append(f"## Errors ({errored})")
        lines.append("")
        lines.append("| Plugin | Error |")
        lines.append("|---|---|")
        for r in rows:
            if r.errored:
                lines.append(f"| `{r.name}` | {r.error or '—'} |")
        lines.append("")

    # Full ranked table
    lines.append("## All plugins (ranked by score ascending)")
    lines.append("")
    lines.append("| Plugin | Score | 95% CI | Badge | Confidence | Duration |")
    lines.append("|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (r.score or 0.0)):
        dur = f"{(r.duration_ms or 0) / 1000:.1f}s" if r.duration_ms else "—"
        lines.append(
            f"| `{r.name}` | {format_score(r.score)} | "
            f"{format_ci(r.ci_lower, r.ci_upper)} | "
            f"{r.badge or '—'} | {r.confidence or '—'} | {dur} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--depth", default="quick", choices=list(DEPTH_MAP.keys())
    )
    parser.add_argument("--output-dir", default="eval-reports")
    parser.add_argument(
        "--concurrency",
        type=int,
        default=4,
        help="Max concurrent LLM calls for Layer 2/3",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Exit 1 if mean score below this (0-100)",
    )
    parser.add_argument(
        "--only-changed",
        default=None,
        help="Comma-separated plugin names to limit evaluation to",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    plugins = discover_plugins()
    if args.only_changed:
        wanted = {n.strip() for n in args.only_changed.split(",") if n.strip()}
        plugins = [p for p in plugins if p.name in wanted]

    config = EvalConfig(
        depth=DEPTH_MAP[args.depth],
        concurrency=args.concurrency,
    )

    started_at = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    print(
        f"[eval_all] evaluating {len(plugins)} plugins at depth={args.depth} "
        f"concurrency={args.concurrency}",
        file=sys.stderr,
    )

    rows: list[PluginRow] = []
    for i, plugin_dir in enumerate(plugins, 1):
        print(
            f"[eval_all] ({i}/{len(plugins)}) {plugin_dir.name}…",
            file=sys.stderr,
        )
        row = evaluate_one(plugin_dir, config, output_dir)
        rows.append(row)

    summary_md = build_summary_md(rows, args.depth, started_at)
    (output_dir / "summary.md").write_text(summary_md)
    (output_dir / "summary.json").write_text(
        json.dumps([asdict(r) for r in rows], indent=2)
    )

    # Echo to stdout so CI can redirect to $GITHUB_STEP_SUMMARY
    sys.stdout.write(summary_md)

    scored = [r for r in rows if not r.errored and r.score is not None]
    if args.threshold is not None and scored:
        mean = sum(r.score or 0.0 for r in scored) / len(scored)
        if mean < args.threshold:
            print(
                f"[eval_all] mean {mean:.1f} below threshold {args.threshold}",
                file=sys.stderr,
            )
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
