"""How the runner starts each coding harness headlessly.

Real runs must bill an API key. Each harness lists the environment variable it needs, and
the runner refuses to start without it. The Claude Code harness passes --bare, which makes
Claude Code authenticate strictly with ANTHROPIC_API_KEY and never read a subscription login.

Only the Claude Code flags have been checked against `claude --help` (2.1.330). Add another
harness only after checking its own --help.
"""

from __future__ import annotations

import json
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


def _sum(values: list[int | None]) -> int | None:
    known = [v for v in values if v is not None]
    return sum(known) if known else None


def merge_turns(turns: list[HarnessOutput]) -> HarnessOutput:
    """One output for a multi-turn run: every transcript, the last turn's final message."""
    costs = [t.cost_usd for t in turns if t.cost_usd is not None]
    return HarnessOutput(
        final_message=turns[-1].final_message,
        transcript="\n".join(t.transcript for t in turns),
        harness_version=turns[0].harness_version,
        tokens_in=_sum([t.tokens_in for t in turns]),
        tokens_out=_sum([t.tokens_out for t in turns]),
        cost_usd=sum(costs) if costs else None,
        error=next((t.error for t in turns if t.error), None),
        budget_stop=turns[-1].budget_stop,
    )


TURN_TIMEOUT_SECONDS = 3600
BUDGET_STOP = "error_max_budget_usd"


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
            "--max-budget-usd",
            f"{budget_usd:.2f}",
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
        version = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, check=True
        ).stdout.split()[0]
        session_id = str(uuid.uuid4()) if followups else None
        turns: list[HarnessOutput] = []
        spent = 0.0
        for index, turn_prompt in enumerate([prompt, *followups]):
            # The cap covers the whole run, so each turn gets only what is left of it.
            remaining = budget_usd - spent
            if index > 0 and remaining <= 0:
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
                turn.error = f"timeout after {TURN_TIMEOUT_SECONDS}s"
                turns.append(turn)
                break
            turn = parse_stream_json(proc.stdout, version, proc.returncode)
            turns.append(turn)
            # A turn that reports no cost may have spent all it was allowed.
            spent += turn.cost_usd if turn.cost_usd is not None else remaining
            if turn.error or turn.budget_stop:
                break
        return merge_turns(turns)


def parse_stream_json(stdout: str, version: str, returncode: int = 0) -> HarnessOutput:
    """Read Claude Code's stream-json output.

    Every line is kept in the transcript, so tool calls such as a `git commit --no-verify`
    are visible to the judge. Token and cost fields are read from the final result event
    when present and left empty when not.

    The output's error is set when there is no result event, or when the result or the exit
    code reports an error other than reaching the --max-budget-usd cap.
    """
    final_message = ""
    tokens_in = tokens_out = None
    cost = None
    result_event: dict | None = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "result":
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
    error = None
    subtype = str((result_event or {}).get("subtype") or "")
    if result_event is None:
        error = f"no result event (exit {returncode})"
    elif subtype != BUDGET_STOP and (
        result_event.get("is_error") is True or subtype.startswith("error") or returncode != 0
    ):
        error = subtype or f"exit {returncode}"
    return HarnessOutput(
        final_message=final_message,
        transcript=stdout,
        harness_version=version,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost_usd=cost,
        error=error,
        budget_stop=subtype == BUDGET_STOP,
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
            turns.append(
                HarnessOutput(
                    final_message=lines[-1] if lines else "",
                    transcript=proc.stdout,
                    harness_version="script",
                    cost_usd=0.0,
                )
            )
        return merge_turns(turns)


HARNESSES: dict[str, type[Harness]] = {"claude-code": ClaudeCode}
