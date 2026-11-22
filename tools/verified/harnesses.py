"""How the runner starts each coding harness headlessly.

Real runs must bill an API key. Each harness lists the environment variable it needs, and
the runner refuses to start without it. The Claude Code harness passes --bare, which makes
Claude Code authenticate strictly with ANTHROPIC_API_KEY and never read a subscription login.

Only the Claude Code flags have been checked against `claude --help` (2.1.330). Add another
harness only after checking its own --help.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HarnessOutput:
    final_message: str
    transcript: str
    harness_version: str
    tokens_in: int | None = None
    tokens_out: int | None = None
    cost_usd: float | None = None
    # Set when the harness itself failed (crash, timeout, API or auth error), so the run
    # says nothing about the workflow. A stop at the budget cap is not a harness error.
    error: str | None = None
    # The turn stopped because it reached its --max-budget-usd cap.
    budget_stop: bool = False
    # The run's cap ran out before every follow-up was sent, so the workflow never finished.
    budget_exhausted: bool = False
    # The turn ran past TURN_TIMEOUT_SECONDS. Usually the workflow's fault (a loop, a
    # blocking command), so it is scored as a failed run, not left out as a harness error.
    timed_out: bool = False
    # The exact model the harness says it ran, such as claude-haiku-5-5. A model alias like
    # "haiku" can point at a newer model after a harness release, so results keep both.
    model_id: str | None = None


def unknown_cost(out: HarnessOutput) -> bool:
    """True when the reported cost can't be trusted as what the run spent."""
    return out.cost_usd is None or (out.error is not None and out.cost_usd == 0)


def _sum(values: list[int | None]) -> int | None:
    known = [v for v in values if v is not None]
    return sum(known) if known else None


def merge_turns(turns: list[HarnessOutput]) -> HarnessOutput:
    """One output for a multi-turn run: every transcript, the last turn's final message."""
    costs = [t.cost_usd or 0.0 for t in turns]
    return HarnessOutput(
        final_message=turns[-1].final_message,
        transcript="\n".join(t.transcript for t in turns),
        harness_version=turns[0].harness_version,
        tokens_in=_sum([t.tokens_in for t in turns]),
        tokens_out=_sum([t.tokens_out for t in turns]),
        # One turn with an unknown cost makes the whole run's cost unknown.
        cost_usd=None if any(unknown_cost(t) for t in turns) else sum(costs),
        error=next((t.error for t in turns if t.error), None),
        budget_stop=turns[-1].budget_stop,
        budget_exhausted=any(t.budget_exhausted for t in turns),
        timed_out=any(t.timed_out for t in turns),
        model_id=next((t.model_id for t in turns if t.model_id), None),
    )


TURN_TIMEOUT_SECONDS = 3600
BUDGET_STOP = "error_max_budget_usd"
# Every case is an offline fixture repo, so web search and fetch can only add tokens and
# outside content to a run. They are turned off for every variant alike.
DISALLOWED_TOOLS = ("WebSearch", "WebFetch")


class Harness:
    name: str = "base"
    key_env: str | None = None

    def require_key(self) -> None:
        if self.key_env and not os.environ.get(self.key_env):
            raise RuntimeError(
                f"{self.name} runs bill an API key. Set {self.key_env} first. The runner never "
                "falls back to a subscription login."
            )

    def run(
        self,
        prompt: str,
        workspace: Path,
        model: str,
        plugin_dirs: list[Path],
        budget_usd: float,
        followups: Sequence[str] = (),
    ) -> HarnessOutput:
        """Run the prompt, then each follow-up as a later turn of the same session."""
        raise NotImplementedError


class ClaudeCode(Harness):
    name = "claude-code"
    key_env = "ANTHROPIC_API_KEY"

    def command(
        self,
        prompt: str,
        model: str,
        plugin_dirs: list[Path],
        budget_usd: float,
        session_id: str | None = None,
        resume: bool = False,
    ) -> list[str]:
        """One headless turn.

        With a session_id the session is saved to disk, so a later turn can resume it.
        """
        cmd = [
            "claude",
            "--bare",
            "-p",
            prompt,
            "--model",
            model,
            "--output-format",
            "stream-json",
            "--verbose",
            "--permission-mode",
            "bypassPermissions",
            "--disallowedTools",
            *DISALLOWED_TOOLS,
            "--max-budget-usd",
            budget_arg(budget_usd),
        ]
        if session_id is None:
            cmd.append("--no-session-persistence")
        elif resume:
            cmd += ["--resume", session_id]
        else:
            cmd += ["--session-id", session_id]
        for plugin_dir in plugin_dirs:
            cmd += ["--plugin-dir", str(plugin_dir)]
        return cmd

    def run(
        self,
        prompt: str,
        workspace: Path,
        model: str,
        plugin_dirs: list[Path],
        budget_usd: float,
        followups: Sequence[str] = (),
    ) -> HarnessOutput:
        self.require_key()
        if float(budget_arg(budget_usd)) <= 0:
            raise ValueError(f"budget {budget_usd} rounds to $0.0000; it must be at least $0.0001")
        version = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, check=True
        ).stdout.split()[0]
        session_id = str(uuid.uuid4()) if followups else None
        turns: list[HarnessOutput] = []
        spent = 0.0
        prompts = [prompt, *followups]
        for index, turn_prompt in enumerate(prompts):
            # The cap covers the whole run, so each turn gets only what is left of it.
            remaining = budget_usd - spent
            if index > 0 and float(budget_arg(remaining)) <= 0:
                turns[-1].budget_exhausted = True
                break
            try:
                proc = subprocess.run(
                    self.command(
                        turn_prompt, model, plugin_dirs, remaining, session_id, resume=index > 0
                    ),
                    cwd=workspace,
                    capture_output=True,
                    text=True,
                    timeout=TURN_TIMEOUT_SECONDS,
                )
            except subprocess.TimeoutExpired as exc:
                stdout = exc.stdout.decode() if isinstance(exc.stdout, bytes) else exc.stdout
                turn = parse_stream_json(stdout or "", version)
                turn.error = None
                turn.timed_out = True
                turns.append(turn)
                break
            turn = parse_stream_json(proc.stdout, version, proc.returncode)
            if turn.error:
                turn.error = with_stderr(turn.error, proc.stderr)
            turns.append(turn)
            # A turn that reports no cost, or an errored turn that reports zero (a crashed
            # session may), may have spent all it was allowed.
            spent += remaining if unknown_cost(turn) else turn.cost_usd or 0.0
            if turn.error or turn.budget_stop:
                # A turn stopped at the cap with follow-ups still to send was cut short too.
                turn.budget_exhausted = turn.budget_stop and index < len(prompts) - 1
                break
        return merge_turns(turns)


def budget_arg(usd: float) -> str:
    """The --max-budget-usd value, rounded down to a hundredth of a cent so it never exceeds
    the cap the runner was given."""
    return f"{max(math.floor(usd * 10_000), 0) / 10_000:.4f}"


ERROR_DETAIL_CHARS = 500


def with_stderr(error: str, stderr: str | None) -> str:
    """Add the end of the process's stderr to an error, so the result shows the cause."""
    tail = (stderr or "").strip()[-ERROR_DETAIL_CHARS:]
    return f"{error}: {tail}" if tail else error


def _entry_sum(usage: object, *keys: str) -> float | None:
    """Sum the given fields over every model entry in model_usage_since_last_result.

    None when the field is missing or any entry lacks one of the fields as a number, so a
    partial figure is never taken for the whole.
    """
    if not isinstance(usage, dict) or not usage:
        return None
    total = 0.0
    for entry in usage.values():
        if not isinstance(entry, dict):
            return None
        for key in keys:
            value = entry.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return None
            total += value
    return total


def process_cost(usage: object) -> float | None:
    """The cost in model_usage_since_last_result: what this process spent since its last result."""
    return _entry_sum(usage, "costUSD")


def process_tokens(usage: object) -> tuple[int | None, int | None]:
    """Input tokens (cache reads and writes included) and output tokens in
    model_usage_since_last_result, counted the same way as the cost."""
    tokens_in = _entry_sum(usage, "inputTokens", "cacheReadInputTokens", "cacheCreationInputTokens")
    tokens_out = _entry_sum(usage, "outputTokens")
    return (
        None if tokens_in is None else int(tokens_in),
        None if tokens_out is None else int(tokens_out),
    )


def parse_stream_json(stdout: str, version: str, returncode: int = 0) -> HarnessOutput:
    """Read Claude Code's stream-json output.

    Every line is kept in the transcript, so tool calls such as a `git commit --no-verify`
    are visible to the judge. Token and cost fields are read from the final result event
    when present and left empty when not.

    The model id is read from the session's init event.

    The output's error is set when there is no result event, or when the result or the exit
    code reports an error other than reaching the --max-budget-usd cap.
    """
    final_message = ""
    tokens_in = tokens_out = None
    cost = None
    process_spend: float | None = None
    process_in: int | None = None
    process_out: int | None = None
    model_id = None
    result_event: dict | None = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") == "system" and event.get("subtype") == "init":
            if isinstance(event.get("model"), str) and model_id is None:
                model_id = event["model"]
            continue
        if event.get("type") != "result":
            continue
        result_event = event
        final_message = str(event.get("result") or "")
        usage = event.get("usage") or {}
        if isinstance(usage, dict):
            parts = [
                usage.get(k)
                for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens")
            ]
            if any(isinstance(p, int) for p in parts):
                tokens_in = sum(p for p in parts if isinstance(p, int))
            if isinstance(usage.get("output_tokens"), int):
                tokens_out = usage["output_tokens"]
        if isinstance(event.get("total_cost_usd"), (int, float)):
            cost = float(event["total_cost_usd"])
        per_process = event.get("model_usage_since_last_result")
        since_last = process_cost(per_process)
        if since_last is not None:
            process_spend = (process_spend or 0.0) + since_last
        last_in, last_out = process_tokens(per_process)
        if last_in is not None:
            process_in = (process_in or 0) + last_in
        if last_out is not None:
            process_out = (process_out or 0) + last_out
    error = None
    subtype = str((result_event or {}).get("subtype") or "")
    if result_event is None:
        error = f"no result event (exit {returncode})"
    elif subtype != BUDGET_STOP and (
        result_event.get("is_error") is True or subtype.startswith("error") or returncode != 0
    ):
        error = ", ".join(
            part for part in (subtype, f"exit {returncode}" if returncode else "") if part
        )
    return HarnessOutput(
        final_message=final_message,
        transcript=stdout,
        harness_version=version,
        # The result's usage may carry a resumed session's earlier turns, like its cost, so
        # the per-process counts are used when Claude Code reports them.
        tokens_in=process_in if process_in is not None else tokens_in,
        tokens_out=process_out if process_out is not None else tokens_out,
        # A resumed session's total_cost_usd includes the turns before it, so it would count
        # them again. The per-process usage, when Claude Code reports it, is this turn alone.
        # Without it the total is kept: that can stop a multi-turn run early, never late.
        cost_usd=process_spend if process_spend is not None else cost,
        error=error,
        budget_stop=subtype == BUDGET_STOP,
        model_id=model_id,
    )


class ScriptHarness(Harness):
    """Runs a local script in place of an agent. Used by the tests; costs nothing.

    The script gets the prompt on stdin and runs inside the workspace. Its stdout is the
    transcript and its last line is the final message.
    """

    name = "script"

    def __init__(self, script: Path) -> None:
        self.script = script

    def run(
        self,
        prompt: str,
        workspace: Path,
        model: str,
        plugin_dirs: list[Path],
        budget_usd: float,
        followups: Sequence[str] = (),
    ) -> HarnessOutput:
        turns = []
        for turn_prompt in [prompt, *followups]:
            proc = subprocess.run(
                [sys.executable, str(self.script)],
                input=turn_prompt,
                cwd=workspace,
                capture_output=True,
                text=True,
                timeout=120,
            )
            lines = proc.stdout.strip().splitlines()
            error = with_stderr(f"exit {proc.returncode}", proc.stderr) if proc.returncode else None
            turns.append(
                HarnessOutput(
                    final_message=lines[-1] if lines else "",
                    transcript=proc.stdout,
                    harness_version="script",
                    cost_usd=0.0,
                    error=error,
                )
            )
            if error:
                break
        return merge_turns(turns)


HARNESSES: dict[str, type[Harness]] = {"claude-code": ClaudeCode}
