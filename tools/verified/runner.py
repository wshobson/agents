"""Plan and run Verified scorecards.

Dry run is the default. Nothing calls a model unless `run` gets --execute, a --max-usd cap
and the harness's API key. The runner never uses a subscription login.

    uv run --project plugins/plugin-eval python -m tools.verified.runner plan \
        --workflow ship-feature --variant free-ship-mate --model sonnet --reps 5

    uv run --project plugins/plugin-eval python -m tools.verified.runner run \
        --workflow ship-feature --variant free-ship-mate --model sonnet --reps 5 \
        --execute --max-usd 10

    uv run --project plugins/plugin-eval python -m tools.verified.runner report scorecards/
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from tools.verified import RUNNER_VERSION
from tools.verified.harnesses import HARNESSES, Harness
from tools.verified.judge import judge, prepare_workspace
from tools.verified.models import (
    CaseKind,
    RunResult,
    Visibility,
    load_case,
    result_schema_text,
)
from tools.verified.report import HARNESS_ERROR, load_results, render_markdown

REPO_ROOT = Path(__file__).resolve().parents[2]
PUBLIC_CASES = REPO_ROOT / "evals" / "verified" / "fixtures" / "public"
WORKFLOWS = Path(__file__).with_name("workflows.json")
SCHEMA_PATH = REPO_ROOT / "scorecards" / "result.schema.json"

# Rough cost of one agent run on a small fixture, in US dollars. These are planning
# estimates (about 600k input tokens, mostly cache reads, and 20k output tokens), not
# measurements. Replace them with measured medians after the first runs.
ESTIMATED_USD_PER_RUN = {"opus": 0.80, "sonnet": 0.40, "haiku": 0.02}
DEFAULT_PER_RUN_CAP_USD = 2.00

# Some free workflows, such as ship-mate, start from a story file rather than a sentence.
STORY_TEMPLATE = """# Verified task

## Description

{task}

## Acceptance criteria

- The request in the description is met.
- The full test suite passes.

## Tasks

- [ ] {task}
"""


@dataclass
class Variant:
    workflow: str
    name: str
    plugin_dirs: list[Path]
    prompt: str
    version: str
    story_file: str | None = None
    # Later turns of the same session, for workflows that pause for a human (ship-mate
    # stops after its plan until `/ship resume`). They run only on cases that are not
    # stop-and-ask, where answering the pause would hide the question being scored.
    followups: tuple[str, ...] = ()
    # Files the workflow's own pipeline writes before any code change (ship-mate's scan
    # writes AGENTS.md). The stop-and-ask check does not count them as code changes.
    own_writes: tuple[str, ...] = ()

    def setup_files(self, task: str) -> dict[str, str]:
        """Files written into the workspace before the baseline, such as a story file."""
        if self.story_file is None:
            return {}
        return {self.story_file: STORY_TEMPLATE.format(task=task)}


def load_variant(workflow: str, variant: str, plugin_dir: Path | None) -> Variant:
    """A named variant from workflows.json, or a Verified build given by --plugin-dir."""
    if plugin_dir is not None:
        # Resolve now: the harness runs from the temporary workspace, not the launch directory.
        plugin_dir = plugin_dir.resolve()
        manifest = json.loads((plugin_dir / ".claude-plugin" / "plugin.json").read_text())
        return Variant(
            workflow=workflow,
            name=variant,
            plugin_dirs=[plugin_dir],
            prompt=f"/{manifest['name']}:{workflow} {{task}}",
            version=manifest["version"],
        )
    spec = json.loads(WORKFLOWS.read_text())[workflow]["variants"][variant]
    manifest = REPO_ROOT / spec["version_from"] / ".claude-plugin" / "plugin.json"
    return Variant(
        workflow=workflow,
        name=variant,
        plugin_dirs=[REPO_ROOT / p for p in spec["plugins"]],
        prompt=spec["prompt"],
        version=json.loads(manifest.read_text())["version"],
        story_file=spec.get("story_file"),
        followups=tuple(spec.get("followups", ())),
        own_writes=tuple(spec.get("own_writes", ())),
    )


def find_cases(
    workflow: str, roots: list[tuple[Path, Visibility]]
) -> list[tuple[Path, Visibility]]:
    found = []
    for root, visibility in roots:
        if not root.is_dir():
            continue
        for case_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            if load_case(case_dir).workflow == workflow:
                found.append((case_dir, visibility))
    return found


def estimate(models: list[str], cases: int, reps: int) -> tuple[int, float]:
    runs = len(models) * cases * reps
    usd = sum(ESTIMATED_USD_PER_RUN.get(m, max(ESTIMATED_USD_PER_RUN.values())) for m in models)
    return runs, usd * cases * reps


def run_one(
    harness: Harness,
    variant: Variant,
    case_dir: Path,
    visibility: Visibility,
    model: str,
    budget_usd: float,
) -> RunResult:
    case = load_case(case_dir)
    with tempfile.TemporaryDirectory(prefix=f"verified-{case.id}-") as tmp:
        workspace = Path(tmp) / "work"
        workspace.mkdir()
        baseline = prepare_workspace(case_dir, workspace, variant.setup_files(case.task))
        followups = () if case.kind is CaseKind.STOP_AND_ASK else variant.followups
        started = time.monotonic()
        out = harness.run(
            variant.prompt.format(task=case.task),
            workspace,
            model,
            variant.plugin_dirs,
            budget_usd,
            followups,
        )
        wall = time.monotonic() - started
        if out.error:
            # The harness failed, so the run says nothing about the workflow. The report
            # leaves these runs out of the pass rate and counts them separately.
            print(f"{case.id}: harness error: {out.error}", file=sys.stderr)
            failed_checks = [HARNESS_ERROR]
        elif out.timed_out:
            failed_checks = ["timed_out"]
        else:
            failed_checks = judge(
                case,
                case_dir,
                workspace,
                baseline,
                out.transcript,
                out.final_message,
                own_writes=variant.own_writes,
            ).failed_checks
    return RunResult(
        workflow=f"{variant.workflow}/{variant.name}",
        workflow_version=variant.version,
        harness=harness.name,
        harness_version=out.harness_version,
        model=model,
        case_id=case.id,
        case_visibility=visibility,
        passed=not failed_checks,
        failed_checks=failed_checks,
        error=out.error,
        tokens_in=out.tokens_in,
        tokens_out=out.tokens_out,
        cost_usd=out.cost_usd,
        wall_seconds=round(wall, 2),
        run_at=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        runner_version=RUNNER_VERSION,
    )


def _case_roots(args: argparse.Namespace) -> list[tuple[Path, Visibility]]:
    roots = [(PUBLIC_CASES, Visibility.PUBLIC)]
    if args.private_cases:
        roots.append((args.private_cases, Visibility.PRIVATE))
    return roots


def cmd_plan(args: argparse.Namespace) -> int:
    variant = load_variant(args.workflow, args.variant, args.plugin_dir)
    cases = find_cases(args.workflow, _case_roots(args))
    runs, usd = estimate(args.model, len(cases), args.reps)
    print(f"workflow {variant.workflow}/{variant.name} {variant.version}")
    print(f"harness {args.harness}, models {', '.join(args.model)}")
    print(f"{len(cases)} cases x {args.reps} reps x {len(args.model)} models = {runs} runs")
    print(f"estimated cost about ${usd:.2f} (planning estimate, not a measurement)")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    if not args.execute:
        print("Dry run. Nothing was started. Add --execute and --max-usd to run for real.")
        return cmd_plan(args)
    if args.max_usd is None or args.max_usd <= 0:
        print("--execute needs a positive --max-usd cap.", file=sys.stderr)
        return 2
    harness = HARNESSES[args.harness]()
    harness.require_key()
    variant = load_variant(args.workflow, args.variant, args.plugin_dir)
    cases = find_cases(args.workflow, _case_roots(args))
    out_dir: Path = args.out / datetime.now(UTC).strftime("%Y-%m-%d")
    out_dir.mkdir(parents=True, exist_ok=True)
    spent = 0.0
    for model in args.model:
        per_run = ESTIMATED_USD_PER_RUN.get(model, DEFAULT_PER_RUN_CAP_USD)
        for case_dir, visibility in cases:
            for rep in range(args.reps):
                remaining = args.max_usd - spent
                if remaining < per_run:
                    print(f"Stopping: ${spent:.2f} spent, cap ${args.max_usd:.2f}.")
                    return 0
                budget = min(remaining, DEFAULT_PER_RUN_CAP_USD)
                result = run_one(harness, variant, case_dir, visibility, model, budget)
                # With no reported cost, or $0 on a harness error, count the whole budget the
                # run was allowed.
                unknown = result.cost_usd is None or (
                    HARNESS_ERROR in result.failed_checks and result.cost_usd == 0
                )
                spent += budget if unknown else (result.cost_usd or 0.0)
                # The start time keeps a second run on the same day from overwriting the first.
                stamp = result.run_at.replace(":", "")
                name = (
                    f"{variant.workflow}-{variant.name}-{model}-{result.case_id}-{stamp}-{rep}.json"
                )
                (out_dir / name).write_text(result.model_dump_json(indent=2) + "\n")
                outcome = (
                    "harness error"
                    if HARNESS_ERROR in result.failed_checks
                    else ("pass" if result.passed else "fail")
                )
                print(f"{result.case_id} rep {rep}: {outcome}")
    print(f"Done. ${spent:.2f} spent.")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    print(render_markdown(load_results(args.results)), end="")
    return 0


def cmd_schema(args: argparse.Namespace) -> int:
    text = result_schema_text()
    if args.check:
        if SCHEMA_PATH.read_text() != text:
            print(f"{SCHEMA_PATH} is out of date. Run the schema command.", file=sys.stderr)
            return 1
        return 0
    SCHEMA_PATH.write_text(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tools.verified.runner")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("plan", "run"):
        p = sub.add_parser(name)
        p.add_argument("--workflow", required=True)
        p.add_argument("--variant", required=True)
        p.add_argument("--plugin-dir", type=Path, help="A Verified build to test instead.")
        p.add_argument("--harness", default="claude-code", choices=sorted(HARNESSES))
        p.add_argument("--model", action="append", required=True)
        p.add_argument("--reps", type=int, default=5)
        p.add_argument("--private-cases", type=Path, help="Folder of private cases.")
        if name == "run":
            p.add_argument("--execute", action="store_true")
            p.add_argument("--max-usd", type=float)
            p.add_argument("--out", type=Path, default=REPO_ROOT / "scorecards" / "runs")
        p.set_defaults(func=cmd_plan if name == "plan" else cmd_run)

    report = sub.add_parser("report")
    report.add_argument("results", type=Path)
    report.set_defaults(func=cmd_report)

    schema = sub.add_parser("schema")
    schema.add_argument("--check", action="store_true")
    schema.set_defaults(func=cmd_schema)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
