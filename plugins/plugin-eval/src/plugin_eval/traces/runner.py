"""Run each prompt through an isolated, headless Claude Code session and record the trace.

Each session gets a fresh temporary CLAUDE_CONFIG_DIR and a fresh working directory, so the
maintainer's own skills, plugins, settings, and CLAUDE.md never reach it. Plugins load only
through --plugin-dir. The parser marks a trace contaminated if anything else shows up in the
session's init event.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import subprocess
import tempfile
import threading
from collections.abc import Callable, Iterable
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Any

from plugin_eval.traces.models import PromptRecord, TraceRecord
from plugin_eval.traces.parse import parse_stream
from plugin_eval.traces.prompts import _skill_names

logger = logging.getLogger(__name__)

DISALLOWED_TOOLS = ("Bash", "WebFetch", "WebSearch", "Task", "Agent")
README_TEXT = "Scratch project for a Claude Code session.\n"
# The only variables a trace session inherits. Anything else in the caller's environment
# can carry the maintainer's Claude Code configuration: a parent Claude Code session exports
# its settings.json "env" block (for example ENABLE_TOOL_SEARCH) and its own CLAUDE_* values
# (for example CLAUDE_EFFORT), and a child session would read them.
ENV_ALLOWLIST = (
    "PATH",
    "HOME",
    "USER",
    "LOGNAME",
    "SHELL",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "LC_CTYPE",
    "TERM",
    "ANTHROPIC_API_KEY",
)


def choose_plugins(
    target_plugin: str,
    marketplace_json: Path,
    seed: int,
    same_category: int = 2,
    random_other: int = 2,
) -> list[str]:
    """Return the target plugin plus distractors, in a seeded random order.

    Distractors are local marketplace plugins: same_category from the target's category and
    random_other from the other categories. The order is shuffled so the target does not
    always load first. Pass a seed derived from the prompt id (see trace_seed) to get a
    different but repeatable set for each prompt.
    """
    entries = json.loads(marketplace_json.read_text(encoding="utf-8"))["plugins"]
    local = {
        e["name"]: e.get("category", "uncategorized")
        for e in entries
        if isinstance(e.get("source"), str)
    }
    if target_plugin not in local:
        raise ValueError(f"{target_plugin} is not a local plugin in {marketplace_json}")
    category = local[target_plugin]
    same = sorted(n for n, c in local.items() if c == category and n != target_plugin)
    other = sorted(n for n, c in local.items() if c != category)
    rng = random.Random(seed)
    picked = [
        target_plugin,
        *rng.sample(same, min(same_category, len(same))),
        *rng.sample(other, min(random_other, len(other))),
    ]
    rng.shuffle(picked)
    return picked


def trace_seed(seed: int, prompt_id: str) -> int:
    """Combine the run seed and a prompt id into a stable per-prompt seed."""
    digest = hashlib.sha256(f"{seed}:{prompt_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def build_argv(
    query: str, plugin_dirs: list[Path], model: str, per_trace_usd: float, max_turns: int
) -> list[str]:
    """Build the claude command line for one headless trace session."""
    return [
        "claude",
        "-p",
        query,
        "--output-format",
        "stream-json",
        "--verbose",
        "--model",
        model,
        "--max-budget-usd",
        f"{per_trace_usd:.2f}",
        "--max-turns",
        str(max_turns),
        "--no-session-persistence",
        "--disallowedTools",
        *DISALLOWED_TOOLS,
        *[arg for d in plugin_dirs for arg in ("--plugin-dir", str(d))],
    ]


def build_env(config_dir: Path) -> dict[str, str]:
    """Return the environment for one session: the allowlist plus an empty config dir."""
    env = {k: v for k, v in os.environ.items() if k in ENV_ALLOWLIST}
    env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    return env


class BudgetLedger:
    """Thread-safe spend tracking that reserves the per-trace cap before a trace starts.

    try_reserve refuses when spent + reserved + per_trace_usd would pass total_usd, so
    concurrent traces can never start more work than the budget covers. settle releases
    one reservation and records what the trace actually cost.
    """

    def __init__(self, total_usd: float, per_trace_usd: float) -> None:
        self.total_usd = total_usd
        self.per_trace_usd = per_trace_usd
        self.spent = 0.0
        self.reserved = 0.0
        self._lock = threading.Lock()

    def try_reserve(self) -> bool:
        with self._lock:
            if self.spent + self.reserved + self.per_trace_usd > self.total_usd + 1e-9:
                return False
            self.reserved += self.per_trace_usd
            return True

    def settle(self, actual_usd: float) -> None:
        with self._lock:
            self.reserved = max(0.0, self.reserved - self.per_trace_usd)
            self.spent += actual_usd


def run_one(
    record: PromptRecord,
    *,
    plugins_dir: Path,
    marketplace_json: Path,
    seed: int,
    model: str,
    per_trace_usd: float,
    max_turns: int,
    workdir: Path,
    config_dir: Path,
    timeout_s: int = 600,
) -> TraceRecord:
    """Run one prompt in a headless session and parse its stream into a TraceRecord."""
    plugins = choose_plugins(record.target_plugin, marketplace_json, trace_seed(seed, record.id))
    plugin_dirs = [plugins_dir / name for name in plugins]
    expected = {f"{d.name}:{skill}" for d in plugin_dirs for skill in _skill_names(d)}
    (workdir / "README.md").write_text(README_TEXT, encoding="utf-8")
    argv = build_argv(record.query, plugin_dirs, model, per_trace_usd, max_turns)
    try:
        proc = subprocess.run(
            argv,
            env=build_env(config_dir),
            cwd=workdir,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired:
        return TraceRecord(
            prompt=record, model=model, plugins_loaded=plugins, is_error=True, error="timeout"
        )
    trace = parse_stream(proc.stdout.splitlines(), record, plugins, expected)
    if proc.returncode != 0 or trace.error == "no result event":
        details = [trace.error, f"exit code {proc.returncode}", proc.stderr.strip()[-500:]]
        trace.is_error = True
        trace.error = "; ".join(d for d in details if d)
    return trace


def run_isolated(record: PromptRecord, **kwargs: Any) -> TraceRecord:
    """Call run_one with a fresh temporary working directory and config dir, then remove both."""
    with (
        tempfile.TemporaryDirectory(prefix="plugin-eval-work-", ignore_cleanup_errors=True) as w,
        tempfile.TemporaryDirectory(prefix="plugin-eval-cfg-", ignore_cleanup_errors=True) as c,
    ):
        return run_one(record, workdir=Path(w), config_dir=Path(c), **kwargs)


def run_batch(
    records: Iterable[PromptRecord],
    out_dir: Path,
    concurrency: int,
    ledger: BudgetLedger,
    run: Callable[[PromptRecord], TraceRecord],
) -> list[TraceRecord]:
    """Run records that have no out_dir/<id>.json yet, writing one file per trace.

    A trace starts only after the ledger reserves its cap, and at most concurrency run at
    once. When the ledger refuses and nothing is running, scheduling stops. A trace that
    failed without reporting a cost is settled at the cap, since its real spend is unknown.
    Returns the new traces in input order.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pending = [r for r in records if not (out_dir / f"{r.id}.json").exists()]

    def run_and_save(record: PromptRecord) -> TraceRecord:
        cost = ledger.per_trace_usd
        try:
            trace = run(record)
            if trace.cost_usd > 0 or not trace.is_error:
                cost = trace.cost_usd
            (out_dir / f"{record.id}.json").write_text(
                trace.model_dump_json(indent=2), encoding="utf-8"
            )
            return trace
        finally:
            ledger.settle(cost)

    done: dict[str, TraceRecord] = {}
    in_flight: set[Future[TraceRecord]] = set()

    def collect(futures: set[Future[TraceRecord]]) -> None:
        for future in futures:
            trace = future.result()
            done[trace.prompt.id] = trace

    def wait_for_slot() -> bool:
        """Block until a worker is free and the ledger reserves a cap; False if it never will."""
        nonlocal in_flight
        while len(in_flight) >= concurrency or not ledger.try_reserve():
            if not in_flight:
                return False
            finished, in_flight = wait(in_flight, return_when=FIRST_COMPLETED)
            collect(finished)
        return True

    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        for index, record in enumerate(pending):
            if not wait_for_slot():
                logger.warning(
                    "Budget of USD %.2f reached; %d traces were not started.",
                    ledger.total_usd,
                    len(pending) - index,
                )
                break
            in_flight.add(pool.submit(run_and_save, record))
        collect(wait(in_flight).done)
    return [done[r.id] for r in pending if r.id in done]
