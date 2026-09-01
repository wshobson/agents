"""Real-CLI subprocess smoke tests.

Invokes the actual harness CLIs against our generated artifacts to catch issues
that pure-Python parsing can't see (CLI version drift, schema validation surprises,
plugin loader behavior).

Each test class skips gracefully when its CLI isn't installed — so local devs and
CI runners only exercise the tools they have. CI installs OpenCode + Antigravity CLI
(both are quick) and the corresponding test classes become required gates.

No API keys needed: every command exercised here is local-only (`agent list`,
`extensions validate`, `doctor`, `--version`).
"""

from __future__ import annotations

import json
import os
import re
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
    args: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int = _TIMEOUT,
) -> subprocess.CompletedProcess:
    """Run a subprocess with a tight timeout and capture stdout/stderr."""
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(cwd) if cwd else None,
        env=env,
    )


def _run_stdout_to_file(args: list[str], cwd: Path, sink_dir: Path) -> subprocess.CompletedProcess:
    """Like `_run`, but stdout is written to a file instead of a pipe.

    `opencode agent list` prints every agent's expanded permission array (about
    330k lines for this catalog) and exits before a pipe is drained, so pipe
    capture intermittently drops the tail and the alphabetically last agents go
    missing. A file sink is written synchronously, so the output is complete.
    """
    sink = sink_dir / "stdout.txt"
    with sink.open("w") as fh:
        proc = subprocess.run(
            args,
            stdout=fh,
            stderr=subprocess.PIPE,
            text=True,
            timeout=_TIMEOUT,
            cwd=str(cwd),
        )
    return subprocess.CompletedProcess(args, proc.returncode, sink.read_text(), proc.stderr)


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

    def test_opencode_agent_list_succeeds(self, opencode_workdir: Path, tmp_path: Path):
        """`opencode agent list` must exit 0 — failure indicates an agent frontmatter
        bug, mode/model schema violation, or permission-block parse error."""
        proc = _run_stdout_to_file(["opencode", "agent", "list"], opencode_workdir, tmp_path)
        assert proc.returncode == 0, (
            f"opencode agent list failed (rc={proc.returncode}):\n"
            f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
        )

    def test_opencode_discovers_every_source_agent(self, opencode_workdir: Path, tmp_path: Path):
        """Every source agent in plugins/*/agents/ must show up in `opencode agent list`."""
        proc = _run_stdout_to_file(["opencode", "agent", "list"], opencode_workdir, tmp_path)
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


# ── Antigravity CLI ──────────────────────────────────────────────────────────


@pytest.mark.skipif(not _has("agy"), reason="agy CLI not installed")
@pytest.mark.skipif(
    not (WORKTREE / ".antigravity" / "plugins").is_dir(),
    reason="Antigravity artifacts not generated — run `make generate HARNESS=antigravity`",
)
class TestAntigravitySmoke:
    def test_agy_plugin_validate_passes_for_every_plugin(self):
        """`agy plugin validate <dir>` must exit 0 for every generated plugin —
        failure indicates a plugin.json, SKILL.md, agent, or command TOML schema
        violation against the real agy binary."""
        root = WORKTREE / ".antigravity" / "plugins"
        failures = []
        for plugin_dir in sorted(p for p in root.iterdir() if p.is_dir()):
            proc = _run(["agy", "plugin", "validate", str(plugin_dir)])
            if proc.returncode != 0:
                failures.append(
                    f"{plugin_dir.name}: rc={proc.returncode}\n"
                    f"--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}"
                )
        assert not failures, "agy plugin validate failures:\n" + "\n".join(failures[:10])


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


# ── Agent Skills installers: gh skill + npx skills ───────────────────────────
#
# Neither is a harness. Both are distribution channels that read the source tree
# directly and discover skills through the `plugins/<plugin>/skills/<skill>/`
# layout. A layout change, or a SKILL.md that breaks the agentskills.io spec,
# silently drops skills from `gh skill install` and `npx skills add`, so these
# tests run the real CLIs against this checkout.

_ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def _source_skill_dirs() -> list[tuple[str, str]]:
    """(plugin, skill directory name) for every source skill under plugins/.

    The directory name is what both installers key on: the agentskills.io spec
    requires frontmatter `name` to equal it, and `gh skill publish` enforces that.
    """
    pairs: list[tuple[str, str]] = []
    for plugin_name in list_plugins():
        plugin = load_plugin(plugin_name)
        if plugin:
            pairs.extend((plugin.name, s.dir.name) for s in plugin.skills)
    return pairs


def test_source_skill_names_are_unique_across_plugins():
    """`npx skills` installs by bare skill name, so two plugins shipping the same
    skill directory name would overwrite each other on install."""
    names = [skill for _, skill in _source_skill_dirs()]
    dupes = sorted({n for n in names if names.count(n) > 1})
    assert not dupes, f"Skill directory names shared across plugins: {dupes}"


def _gh_has_skill_command() -> bool:
    """`gh skill` shipped in GitHub CLI 2.90 (April 2026); older builds lack it."""
    return _has("gh") and _run(["gh", "skill", "--help"]).returncode == 0


@pytest.mark.skipif(
    not _gh_has_skill_command(), reason="gh CLI with `gh skill` (>= 2.90) not installed"
)
class TestGitHubSkillSmoke:
    def test_gh_skill_discovers_every_source_skill(self):
        """`gh skill install <dir> --from-local` lists skills found through the
        `plugins/{scope}/skills/*/SKILL.md` convention as `[plugins] <plugin>/<skill>`
        (TSV when piped). Every source skill directory must appear. gh prints the
        frontmatter name, so a name/directory mismatch also surfaces here."""
        proc = _run(["gh", "skill", "install", ".", "--from-local"], cwd=WORKTREE)
        assert proc.returncode == 0, (
            f"gh skill install --from-local failed (rc={proc.returncode}):\n"
            f"--- stdout ---\n{proc.stdout[:2000]}\n--- stderr ---\n{proc.stderr}"
        )
        listed = set()
        for line in proc.stdout.splitlines():
            head = line.split("\t", 1)[0].strip()
            if head.startswith("[plugins] "):
                listed.add(head.removeprefix("[plugins] "))

        expected = {f"{plugin}/{skill}" for plugin, skill in _source_skill_dirs()}
        missing = expected - listed
        assert not missing, (
            f"gh skill failed to discover {len(missing)} source skills. "
            f"Missing: {sorted(missing)[:10]}{'...' if len(missing) > 10 else ''}"
        )

    def test_gh_skill_publish_dry_run_validates_every_skill(self):
        """`gh skill publish --dry-run` validates every discovered SKILL.md against
        the agentskills.io spec: name pattern, name == directory, required
        frontmatter, `allowed-tools` shape. Errors fail the run; warnings
        (recommended `license`, body length) are advisory and stay visible in -v."""
        proc = _run(["gh", "skill", "publish", "--dry-run"], cwd=WORKTREE)
        output = proc.stdout + proc.stderr
        errors = [line for line in output.splitlines() if line.startswith("error")]
        assert proc.returncode == 0 and not errors, (
            f"gh skill publish --dry-run failed (rc={proc.returncode}):\n"
            + "\n".join(errors or [output[-2000:]])
        )


@pytest.mark.skipif(not _has("npx"), reason="npx (Node.js) not installed")
class TestVercelSkillsSmoke:
    def test_npx_skills_discovers_every_source_skill(self):
        """`npx skills add <dir> --list` (vercel-labs/skills) walks the tree and lists
        skills by bare frontmatter name, with no plugin prefix. Every source skill must
        appear. On a generated checkout the listing is a superset: the gitignored
        `.codex/`, `.opencode/` and `.copilot/` trees are walked too, so only
        containment is asserted."""
        env = {**os.environ, "DISABLE_TELEMETRY": "1", "NO_COLOR": "1"}
        proc = _run(
            ["npx", "--yes", "skills@latest", "add", ".", "--list", "-y"],
            cwd=WORKTREE,
            env=env,
            timeout=180,  # first run downloads the package
        )
        assert proc.returncode == 0, (
            f"npx skills add --list failed (rc={proc.returncode}):\n"
            f"--- stdout ---\n{proc.stdout[-2000:]}\n--- stderr ---\n{proc.stderr[-2000:]}"
        )
        text = _ANSI.sub("", proc.stdout + proc.stderr)
        # Each skill name is its own box-drawing line, `│` plus exactly four spaces;
        # descriptions are indented six, so they never match.
        listed = set(re.findall(r"^│ {4}([a-z0-9][a-z0-9_.-]*)$", text, flags=re.M))

        expected = {skill for _, skill in _source_skill_dirs()}
        missing = expected - listed
        assert not missing, (
            f"npx skills failed to discover {len(missing)} source skills. "
            f"Missing: {sorted(missing)[:10]}{'...' if len(missing) > 10 else ''}"
        )


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
