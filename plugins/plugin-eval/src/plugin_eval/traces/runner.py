"""Run each prompt through an isolated, headless Claude Code session and record the trace.

Each session gets a fresh temporary CLAUDE_CONFIG_DIR and a fresh working directory, so the
maintainer's own skills, plugins, settings, and CLAUDE.md never reach it. Plugins load only
through --plugin-dir. The parser marks a trace contaminated if anything else shows up in the
session's init event. Each session's raw stream is kept next to its trace as
<id>.stream.jsonl, because the trace keeps only summaries (for example, the text a skill
loads is only in the raw stream).
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import re
import subprocess
import tempfile
import threading
from collections.abc import Callable, Iterable
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from pathlib import Path
from typing import Any

from plugin_eval.traces.models import PromptRecord, TraceRecord
from plugin_eval.traces.parse import ALLOWED_TOOLS, NO_RESULT_ERROR, parse_stream
from plugin_eval.traces.prompts import skill_names

logger = logging.getLogger(__name__)

README_TEXT = "Scratch project for a Claude Code session.\n"
# Prompt ids become file names in the output directory, so they must be plain names.
PROMPT_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
# plugins_digest skips hidden entries other than these, and cache directories, so a local
# .venv or .pytest_cache does not count as plugin content.
DIGEST_HIDDEN_KEEP = frozenset({".claude-plugin", ".mcp.json"})
DIGEST_SKIP = frozenset({"__pycache__", "node_modules"})
STREAM_SUFFIX = ".stream.jsonl"  # the raw stream file; it never matches the *.json traces
# Plugin hooks run shell commands on every tool call (protect-mcp's run npx), and the init
# event does not list them. Flag settings keep the config dir empty. A probe on Claude Code
# 2.1.283 showed this stops a plugin's hooks; the parser flags any hook event that still runs.
SESSION_SETTINGS = json.dumps({"disableAllHooks": True})
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

    Distractors are local marketplace plugins with at least one skill, since a plugin with
    no skills competes with nothing: same_category from the target's category and
    random_other from the other categories. A local source is resolved against the
    marketplace root, the directory that holds .claude-plugin/. The order is shuffled so the
    target does not always load first. Pass a seed derived from the prompt id (see
    trace_seed) to get a different but repeatable set for each prompt.
    """
    entries = json.loads(marketplace_json.read_text(encoding="utf-8"))["plugins"]
    local = {
        e["name"]: e.get("category", "uncategorized")
        for e in entries
        if isinstance(e.get("source"), str)
    }
    if target_plugin not in local:
        raise ValueError(f"{target_plugin} is not a local plugin in {marketplace_json}")
    dirs = local_plugin_dirs(marketplace_json)
    candidates = {n: c for n, c in local.items() if n != target_plugin and skill_names(dirs[n])}
    category = local[target_plugin]
    same = sorted(n for n, c in candidates.items() if c == category)
    other = sorted(n for n, c in candidates.items() if c != category)
    rng = random.Random(seed)
    picked = [
        target_plugin,
        *rng.sample(same, min(same_category, len(same))),
        *rng.sample(other, min(random_other, len(other))),
    ]
    rng.shuffle(picked)
    return picked


def local_plugin_dirs(marketplace_json: Path) -> dict[str, Path]:
    """Map each local marketplace plugin to its directory, resolved against the marketplace
    root (the directory that holds .claude-plugin/), as Claude Code resolves it."""
    root = marketplace_json.parent.parent
    entries = json.loads(marketplace_json.read_text(encoding="utf-8"))["plugins"]
    return {
        e["name"]: (root / e["source"]).resolve()
        for e in entries
        if isinstance(e.get("source"), str)
    }


def check_prompt_ids(records: Iterable[PromptRecord]) -> None:
    """Raise ValueError unless every prompt id is a plain file name and appears only once."""
    seen: set[str] = set()
    for record in records:
        if not PROMPT_ID_PATTERN.fullmatch(record.id):
            raise ValueError(
                f"prompt id {record.id!r} is not allowed. Ids must match "
                f"{PROMPT_ID_PATTERN.pattern}, because they become file names."
            )
        # Compare without case, because macOS and Windows file systems usually ignore it,
        # so p001 and P001 would write the same trace file.
        if record.id.casefold() in seen:
            raise ValueError(
                f"prompt id {record.id!r} is a duplicate (ids are compared without case). "
                "Each id must be unique."
            )
        seen.add(record.id.casefold())


def _skipped(name: str) -> bool:
    return (name.startswith(".") and name not in DIGEST_HIDDEN_KEEP) or name in DIGEST_SKIP


def plugins_digest(plugin_dirs: Iterable[Path]) -> str:
    """Return a short digest of the files a session can read from the given plugins.

    The digest covers each file's path and bytes, in a fixed order, so it changes when any
    plugin file changes and not when the load order does.
    """
    digest = hashlib.sha256()
    for plugin in sorted(plugin_dirs, key=lambda d: d.name):
        for root, dirs, files in os.walk(plugin):
            dirs[:] = sorted(d for d in dirs if not _skipped(d))
            for name in sorted(f for f in files if not _skipped(f)):
                path = Path(root) / name
                digest.update(f"{plugin.name}/{path.relative_to(plugin).as_posix()}\n".encode())
                digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()[:16]


def claude_version() -> str:
    """Return the installed Claude Code version, such as "2.1.283", or "" if claude cannot run."""
    with tempfile.TemporaryDirectory(prefix="plugin-eval-cfg-") as config_dir:
        try:
            proc = subprocess.run(
                ["claude", "--version"],
                env=build_env(Path(config_dir)),
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError):
            return ""
    words = proc.stdout.split()
    return words[0] if proc.returncode == 0 and words else ""


def trace_seed(seed: int, prompt_id: str) -> int:
    """Combine the run seed and a prompt id into a stable per-prompt seed."""
    digest = hashlib.sha256(f"{seed}:{prompt_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def build_argv(
    query: str, plugin_dirs: list[Path], model: str, per_trace_usd: float, max_turns: int
) -> list[str]:
    """Build the claude command line for one headless trace session.

    plugin_dirs must be absolute, because the session runs in another directory and the
    read rules use absolute paths. The query comes last, after "--", so a query that starts
    with "-" (a Markdown bullet, for example) is not read as an option.
    """
    return [
        "claude",
        "-p",
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
        "--tools",
        *ALLOWED_TOOLS,
        # Writes land in the fresh temporary cwd. Edits outside the working directories are
        # still denied in -p mode, because no one is there to approve them.
        "--permission-mode",
        "acceptEdits",
        "--settings",
        SESSION_SETTINGS,
        # Hook events go to the stream, so a PreToolUse or PostToolUse hook that still ran
        # marks the trace contaminated. Without this flag only SessionStart hooks show up.
        "--include-hook-events",
        # -p mode also denies reads outside the working directories, which would stop a skill
        # from opening its own references/. These rules allow reads, and only reads, of the
        # loaded plugins. --add-dir would also allow edits there under acceptEdits.
        "--allowedTools",
        *[f"Read(/{d}/**)" for d in plugin_dirs],
        *[arg for d in plugin_dirs for arg in ("--plugin-dir", str(d))],
        "--",
        query,
    ]


def build_env(config_dir: Path) -> dict[str, str]:
    """Return the environment for one session: the allowlist plus an empty config dir."""
    env = {k: v for k, v in os.environ.items() if k in ENV_ALLOWLIST}
    env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    # Keep one Claude Code version for the whole run; a new version can add built-in skills.
    env["DISABLE_AUTOUPDATER"] = "1"
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
    raw_dir: Path | None = None,
) -> TraceRecord:
    """Run one prompt in a headless session and parse its stream into a TraceRecord.

    When raw_dir is given, the session's stdout is saved there as <id>.stream.jsonl. On a
    timeout, the partial stdout is saved and parsed, and the trace's error is "timeout".
    """
    plugins = choose_plugins(record.target_plugin, marketplace_json, trace_seed(seed, record.id))
    plugin_dirs = [(plugins_dir / name).resolve() for name in plugins]
    expected = {f"{d.name}:{skill}" for d in plugin_dirs for skill in skill_names(d)}
    digest = plugins_digest(plugin_dirs)
    (workdir / "README.md").write_text(README_TEXT, encoding="utf-8")
    argv = build_argv(record.query, plugin_dirs, model, per_trace_usd, max_turns)
    timed_out = False
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
        stdout, stderr, returncode = proc.stdout, proc.stderr, proc.returncode
    except subprocess.TimeoutExpired as exc:
        # The partial output arrives as bytes even with text=True.
        timed_out = True
        stdout, stderr, returncode = _decode(exc.stdout), _decode(exc.stderr), None
    if raw_dir is not None:
        raw_dir.mkdir(parents=True, exist_ok=True)
        _write_atomic(raw_dir / f"{record.id}{STREAM_SUFFIX}", stdout)
    # Split on "\n" only: str.splitlines also splits on U+2028 and U+2029, which JSON
    # leaves raw inside strings.
    trace = parse_stream(stdout.split("\n"), record, plugins, expected)
    trace.model = trace.model or model
    trace.requested_model, trace.seed, trace.per_trace_cap_usd = model, seed, per_trace_usd
    trace.max_turns, trace.timeout_s, trace.plugins_digest = max_turns, timeout_s, digest
    if timed_out:
        trace.is_error = True
        trace.error = "timeout"
    elif returncode != 0 or trace.error == NO_RESULT_ERROR:
        details = [trace.error, f"exit code {returncode}", stderr.strip()[-500:]]
        trace.is_error = True
        trace.error = "; ".join(d for d in details if d)
    return trace


def _decode(output: bytes | str | None) -> str:
    if isinstance(output, bytes):
        return output.decode("utf-8", errors="replace")
    return output or ""


def billed_usd(trace: TraceRecord, cap: float) -> float:
    """What a trace counts against the total budget.

    A session that ran always costs more than zero, so a zero cost means the cost is
    unknown (a timeout, a crash, an interrupted run, or a missing cost field). Unknown cost
    is billed at the cap the trace ran under, when the trace records it, and otherwise at
    cap. So a later run with a lower cap cannot under-count an earlier trace.
    """
    if trace.cost_usd > 0:
        return trace.cost_usd
    return trace.per_trace_cap_usd if trace.per_trace_cap_usd > 0 else cap


def _write_atomic(path: Path, text: str) -> None:
    """Write through a temp file in the same directory, so a crash never leaves half a file."""
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


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
    model: str = "",
    seed: int | None = None,
    max_turns: int = 0,
    timeout_s: int = 0,
) -> list[TraceRecord]:
    """Run records that have no out_dir/<id>.json yet, writing one file per trace.

    A trace starts only after the ledger reserves its cap, and at most concurrency run at
    once. When the ledger refuses and nothing is running, scheduling stops. Each trace is
    settled at billed_usd, so unknown cost counts as the cap. If run raises, an error trace
    is written for that record, with the run's model, seed, cap, max_turns, and timeout_s,
    and the batch goes on.
    A trace that costs more than the cap
    is logged and records the overshoot in over_cap_usd. Returns the new traces in input
    order.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pending = [r for r in records if not (out_dir / f"{r.id}.json").exists()]

    cap = ledger.per_trace_usd

    def run_and_save(record: PromptRecord) -> TraceRecord:
        cost = cap
        try:
            try:
                trace = run(record)
            except Exception as exc:
                logger.exception(
                    "Trace %s raised; writing an error trace billed at the cap.", record.id
                )
                trace = TraceRecord(
                    prompt=record,
                    model=model,
                    plugins_loaded=[],
                    is_error=True,
                    error=f"runner raised {type(exc).__name__}: {exc}",
                    requested_model=model,
                    seed=seed,
                    per_trace_cap_usd=cap,
                    max_turns=max_turns,
                    timeout_s=timeout_s,
                )
            cost = billed_usd(trace, cap)
            if trace.cost_usd > cap:
                trace.over_cap_usd = trace.cost_usd - cap
                logger.warning(
                    "Trace %s cost USD %.2f, over the per-trace cap of USD %.2f.",
                    record.id,
                    trace.cost_usd,
                    cap,
                )
            _write_atomic(out_dir / f"{record.id}.json", trace.model_dump_json(indent=2))
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
