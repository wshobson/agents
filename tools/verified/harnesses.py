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
    ) -> HarnessOutput:
        raise NotImplementedError


class ClaudeCode(Harness):
    name = "claude-code"
    key_env = "ANTHROPIC_API_KEY"

    def command(
        self, prompt: str, model: str, plugin_dirs: list[Path], budget_usd: float
    ) -> list[str]:
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
            "--no-session-persistence",
            "--max-budget-usd",
            f"{budget_usd:.2f}",
        ]
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
    ) -> HarnessOutput:
        self.require_key()
        version = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, check=True
        ).stdout.split()[0]
        proc = subprocess.run(
            self.command(prompt, model, plugin_dirs, budget_usd),
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=3600,
        )
        return parse_stream_json(proc.stdout, version)


def parse_stream_json(stdout: str, version: str) -> HarnessOutput:
    """Read Claude Code's stream-json output.

    Every line is kept in the transcript, so tool calls such as a `git commit --no-verify`
    are visible to the judge. Token and cost fields are read from the final result event
    when present and left empty when not.
    """
    final_message = ""
    tokens_in = tokens_out = None
    cost = None
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "result":
            continue
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
    return HarnessOutput(
        final_message=final_message,
        transcript=stdout,
        harness_version=version,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost_usd=cost,
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
    ) -> HarnessOutput:
        proc = subprocess.run(
            [sys.executable, str(self.script)],
            input=prompt,
            cwd=workspace,
            capture_output=True,
            text=True,
            timeout=120,
        )
        lines = proc.stdout.strip().splitlines()
        return HarnessOutput(
            final_message=lines[-1] if lines else "",
            transcript=proc.stdout,
            harness_version="script",
            cost_usd=0.0,
        )


HARNESSES: dict[str, type[Harness]] = {"claude-code": ClaudeCode}
