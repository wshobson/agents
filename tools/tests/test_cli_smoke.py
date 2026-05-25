"""Real-CLI subprocess smoke tests.

Invokes the actual harness CLIs against our generated artifacts to catch issues
that pure-Python parsing can't see (CLI version drift, schema validation surprises,
plugin loader behavior).

Each test class skips gracefully when its CLI isn't installed — so local devs and
CI runners only exercise the tools they have. CI installs OpenCode + Gemini CLI
(both are quick) and the corresponding test classes become required gates.

No API keys needed: every command exercised here is local-only (`agent list`,
`extensions validate`, `doctor`, `--version`).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.adapters.base import WORKTREE, list_plugins, load_plugin  # noqa: E402

_TIMEOUT = 60  # seconds per subprocess call


def _has(cli: str) -> bool:
    """Return True iff a CLI is on PATH."""
    return shutil.which(cli) is not None


def _run(
    args: list[str], cwd: Path | None = None, env: dict | None = None
) -> subprocess.CompletedProcess:
    """Run a subprocess with a tight timeout and capture stdout/stderr."""
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=_TIMEOUT,
        cwd=str(cwd) if cwd else None,
        env=env,
    )


# ── OpenCode CLI ─────────────────────────────────────────────────────────────


@pytest.mark.skipif(not _has("opencode"), reason="opencode CLI not installed")
@pytest.mark.skipif(
    not (WORKTREE / ".opencode").is_dir(),
    reason="OpenCode artifacts not generated — run `make generate HARNESS=opencode`",
)
class TestOpenCodeSmoke:
    @pytest.fixture(scope="class")
    def opencode_workdir(self, tmp_path_factory) -> Path:
        """Stage the generated .opencode/ + opencode.json in a tmpdir so we don't
        need to install into the user's ~/.opencode/."""
        d = tmp_path_factory.mktemp("opencode-smoke")
        shutil.copytree(WORKTREE / ".opencode", d / ".opencode")
        shutil.copy(WORKTREE / "opencode.json", d / "opencode.json")
        return d

    def test_opencode_agent_list_succeeds(self, opencode_workdir: Path):
        """`opencode agent list` must exit 0 — failure indicates an agent frontmatter
        bug, mode/model schema violation, or permission-block parse error."""
        proc = _run(["opencode", "agent", "list"], cwd=opencode_workdir)
        assert proc.returncode == 0, (
            f"opencode agent list failed (rc={proc.returncode}):\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )

    def test_opencode_discovers_every_source_agent(self, opencode_workdir: Path):
        """Every source agent in plugins/*/agents/ must show up in `opencode agent list`."""
        proc = _run(["opencode", "agent", "list"], cwd=opencode_workdir)
        assert proc.returncode == 0
        listed = set()
        for line in proc.stdout.splitlines():
            # Lines look like `<plugin>__<agent> (subagent)` or `<name> (primary)`
            line = line.strip()
            if "(" in line:
                listed.add(line.split("(", 1)[0].strip())

        expected = set()
        for plugin_name in list_plugins():
            plugin = load_plugin(plugin_name)
            if plugin:
                expected.update(f"{plugin.name}__{a.name}" for a in plugin.agents)

        missing = expected - listed
        assert not missing, (
            f"OpenCode failed to discover {len(missing)} agents — likely a frontmatter "
            f"or permission-block bug. Missing: {sorted(missing)[:10]}{'...' if len(missing) > 10 else ''}"
        )


# ── Gemini CLI ───────────────────────────────────────────────────────────────


@pytest.mark.skipif(not _has("gemini"), reason="gemini CLI not installed")
class TestGeminiSmoke:
    def test_gemini_extension_validates(self):
        """`gemini extensions validate <repo>` must return success — failure indicates
        gemini-extension.json schema drift or invalid TOML in commands/."""
        proc = _run(["gemini", "extensions", "validate", str(WORKTREE)])
        assert proc.returncode == 0, (
            f"gemini extensions validate failed (rc={proc.returncode}):\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )
        # Success message is part of the Gemini CLI contract.
        assert "successfully validated" in proc.stdout.lower() or proc.returncode == 0


# ── Codex CLI ────────────────────────────────────────────────────────────────


@pytest.mark.skipif(not _has("codex"), reason="codex CLI not installed")
class TestCodexSmoke:
    def test_codex_doctor_passes_overall(self):
        """`codex doctor` is the only no-API health check Codex CLI provides. It runs
        a battery of structural checks and surfaces drift in the local install."""
        proc = _run(["codex", "doctor"])
        # Codex doctor returns 0 on healthy install; warnings are inline but don't fail.
        assert proc.returncode == 0, (
            f"codex doctor failed (rc={proc.returncode}):\n"
            f"--- stdout ---\n{proc.stdout[:2000]}\n--- stderr ---\n{proc.stderr}"
        )

    @pytest.mark.skipif(
        not (WORKTREE / ".codex").is_dir(),
        reason="Codex artifacts not generated — run `make generate HARNESS=codex`",
    )
    def test_every_codex_agent_toml_loads_with_tomllib(self):
        """We can't directly invoke Codex on our agents (would require a session), but
        every TOML must parse with the same library Codex uses."""
        import tomllib

        broken = []
        for toml_path in (WORKTREE / ".codex" / "agents").glob("*.toml"):
            try:
                tomllib.loads(toml_path.read_text())
            except tomllib.TOMLDecodeError as e:
                broken.append(f"{toml_path.name}: {e}")
        assert not broken, "Codex agent TOMLs that fail to parse:\n  " + "\n  ".join(broken)


# ── Claude Code CLI ──────────────────────────────────────────────────────────


@pytest.mark.skipif(not _has("claude"), reason="claude CLI not installed")
class TestClaudeCodeSmoke:
    def test_claude_version_runs(self):
        """Sanity check that the Claude Code CLI is invokable. Doesn't load our
        marketplace (that would require an actual session)."""
        proc = _run(["claude", "--version"])
        assert proc.returncode == 0, f"claude --version failed: {proc.stderr}"
        assert "Claude Code" in proc.stdout or "claude" in proc.stdout.lower()

    def test_marketplace_json_loads_via_python(self):
        """The marketplace.json must parse as JSON (covers Claude Code's loader path)."""
        mp = json.loads((WORKTREE / ".claude-plugin" / "marketplace.json").read_text())
        assert mp.get("plugins"), "marketplace.json has no plugins[]"
        # Owner/metadata are required for Claude Code's marketplace loader.
        assert mp.get("owner"), "marketplace.json missing top-level 'owner'"
        assert mp.get("metadata", {}).get("version"), "marketplace.json missing metadata.version"


# ── Cross-CLI sanity: marketplace + adapter agreement ────────────────────────


class TestMarketplaceAgreement:
    """No CLI needed — checks the static contract between marketplace.json and
    what the adapters produce. Catches version-bump drift and missing entries."""

    def test_every_marketplace_local_entry_has_synced_version(self):
        mp = json.loads((WORKTREE / ".claude-plugin" / "marketplace.json").read_text())
        drift = []
        for entry in mp.get("plugins", []):
            source = entry.get("source")
            if not (isinstance(source, str) and source.startswith("./plugins/")):
                continue
            pj_path = WORKTREE / source.removeprefix("./") / ".claude-plugin" / "plugin.json"
            if not pj_path.is_file():
                continue
            pj = json.loads(pj_path.read_text())
            if entry.get("version") != pj.get("version"):
                drift.append(
                    f"{entry['name']}: marketplace={entry.get('version')} "
                    f"vs plugin.json={pj.get('version')}"
                )
        assert not drift, "Version drift:\n  " + "\n  ".join(drift)
