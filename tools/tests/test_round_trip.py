"""Cross-harness round-trip integrity tests.

These run AFTER `make generate-all` (CI runs this). They:
1. Verify counts match between source and generated artifacts (catches silent skips/dupes).
2. Re-parse generated TOMLs/JSONs/MDCs to confirm structural correctness.
3. Verify reference resolution (e.g. Gemini's `@{path}` injections point at real files).
4. Spot-check that the same plugin's artifacts look reasonable across harnesses.

CI runs `make generate-all` before this; if you're running locally first do the same.
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.adapters.base import (  # noqa: E402
    WORKTREE,
    list_plugins,
    load_plugin,
    parse_frontmatter,
)


def _source_agent_count() -> int:
    """Count agents across all local plugins."""
    n = 0
    for name in list_plugins():
        plugin = load_plugin(name)
        if plugin:
            n += len(plugin.agents)
    return n


def _source_skill_count() -> int:
    n = 0
    for name in list_plugins():
        plugin = load_plugin(name)
        if plugin:
            n += len(plugin.skills)
    return n


def _source_command_count() -> int:
    n = 0
    for name in list_plugins():
        plugin = load_plugin(name)
        if plugin:
            n += len(plugin.commands)
    return n


# ── Per-harness output checks ────────────────────────────────────────────────


@pytest.mark.skipif(
    not (WORKTREE / ".codex").is_dir(),
    reason="Codex artifacts not generated (run `make generate HARNESS=codex` first)",
)
class TestCodexRoundTrip:
    def test_codex_agent_count_matches_source(self):
        codex_agents = list((WORKTREE / ".codex" / "agents").glob("*.toml"))
        assert len(codex_agents) == _source_agent_count(), (
            f"agent count mismatch: source={_source_agent_count()} codex={len(codex_agents)}"
        )

    def test_every_codex_skill_under_8kb(self):
        """Codex hard-truncates skills past 8 KB — any over-sized file is a runtime defect."""
        oversized = []
        for skill_md in (WORKTREE / ".codex" / "skills").glob("*/SKILL.md"):
            size = len(skill_md.read_text().encode("utf-8"))
            if size > 8 * 1024:
                oversized.append(f"{skill_md.relative_to(WORKTREE)}: {size}B")
        assert not oversized, "Codex skills over 8 KB injection cap:\n  " + "\n  ".join(oversized)

    def test_every_codex_agent_toml_parses_and_has_required_fields(self):
        required = {"name", "description", "developer_instructions"}
        invalid = []
        for toml_path in (WORKTREE / ".codex" / "agents").glob("*.toml"):
            try:
                data = tomllib.loads(toml_path.read_text())
            except tomllib.TOMLDecodeError as e:
                invalid.append(f"{toml_path.name}: {e}")
                continue
            missing = required - set(data.keys())
            if missing:
                invalid.append(f"{toml_path.name}: missing {sorted(missing)}")
            sandbox = data.get("sandbox_mode")
            if sandbox and sandbox not in {
                "read-only",
                "workspace-write",
                "danger-full-access",
            }:
                invalid.append(f"{toml_path.name}: invalid sandbox_mode {sandbox!r}")
        assert not invalid, "Invalid Codex agent TOMLs:\n  " + "\n  ".join(invalid[:20])

    def test_agents_md_within_cap(self):
        agents_md = WORKTREE / "AGENTS.md"
        if not agents_md.is_file():
            pytest.skip("AGENTS.md not generated")
        lines = agents_md.read_text().splitlines()
        assert len(lines) <= 150, f"AGENTS.md is {len(lines)} lines (cap: 150)"


@pytest.mark.skipif(
    not (WORKTREE / ".opencode").is_dir(),
    reason="OpenCode artifacts not generated (run `make generate HARNESS=opencode` first)",
)
class TestOpenCodeRoundTrip:
    def test_opencode_agent_count_matches_source(self):
        n = len(list((WORKTREE / ".opencode" / "agents").glob("*.md")))
        assert n == _source_agent_count(), (
            f"agent count mismatch: source={_source_agent_count()} opencode={n}"
        )

    def test_opencode_command_count_matches_source(self):
        n = len(list((WORKTREE / ".opencode" / "commands").glob("*.md")))
        assert n == _source_command_count(), (
            f"command count mismatch: source={_source_command_count()} opencode={n}"
        )

    def test_opencode_skill_count_matches_source(self):
        n = len(list((WORKTREE / ".opencode" / "skills").glob("*/SKILL.md")))
        assert n == _source_skill_count(), (
            f"skill count mismatch: source={_source_skill_count()} opencode={n}"
        )

    def test_every_opencode_agent_has_required_frontmatter(self):
        modes = {"primary", "subagent", "all"}
        problems = []
        for agent_md in (WORKTREE / ".opencode" / "agents").glob("*.md"):
            fm, _ = parse_frontmatter(agent_md.read_text())
            if not fm:
                problems.append(f"{agent_md.name}: no frontmatter")
                continue
            if fm.get("mode") not in modes:
                problems.append(f"{agent_md.name}: invalid mode {fm.get('mode')!r}")
            model = fm.get("model", "")
            if model and "/" not in model:
                problems.append(f"{agent_md.name}: model {model!r} not provider-prefixed")
        assert not problems, "OpenCode agent issues:\n  " + "\n  ".join(problems[:20])

    def test_locked_agents_have_proper_permission_block(self):
        """Source agents with `tools: []` MUST emit a deny-everything permission block
        (with skill/task base capabilities allowed). Regression guard for PR #541 P1."""
        problems = []
        for plugin_name in list_plugins():
            plugin = load_plugin(plugin_name)
            if not plugin:
                continue
            for agent in plugin.agents:
                if "tools" not in agent.frontmatter or agent.tools:
                    continue
                # source has `tools: []` — generated must lock it down.
                agent_id = f"{plugin.name}__{agent.name}"
                gen = WORKTREE / ".opencode" / "agents" / f"{agent_id}.md"
                if not gen.is_file():
                    continue
                content = gen.read_text()
                if "permission:" not in content:
                    problems.append(
                        f"{agent_id}: source has `tools: []` but generated has no permission block "
                        "(privilege escalation — Codex PR-541 P1)"
                    )
                    continue
                # Must allow skill + task (base capabilities), deny others.
                if not re.search(r"skill:\s*allow", content):
                    problems.append(f"{agent_id}: skill not allowed in permission block")
                if not re.search(r"task:\s*allow", content):
                    problems.append(f"{agent_id}: task not allowed in permission block")
                if not re.search(r"read:\s*deny", content):
                    problems.append(f"{agent_id}: read should be denied for locked agent")
        assert not problems, "Locked-agent permission regressions:\n  " + "\n  ".join(problems)

    def test_every_opencode_skill_has_valid_frontmatter(self):
        name_re = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
        problems = []
        for skill_md in (WORKTREE / ".opencode" / "skills").glob("*/SKILL.md"):
            fm, _ = parse_frontmatter(skill_md.read_text())
            name = str(fm.get("name") or "")
            if name != skill_md.parent.name:
                problems.append(f"{skill_md}: name {name!r} != directory {skill_md.parent.name!r}")
            if not name_re.fullmatch(name):
                problems.append(f"{skill_md}: invalid OpenCode skill name {name!r}")
            if len(name) > 64:
                problems.append(f"{skill_md}: OpenCode skill name exceeds 64 chars")
            if not str(fm.get("description") or "").strip():
                problems.append(f"{skill_md}: missing description")
        assert not problems, "OpenCode skill issues:\n  " + "\n  ".join(problems[:20])


@pytest.mark.skipif(
    not (WORKTREE / ".cursor-plugin").is_dir(),
    reason="Cursor artifacts not generated (run `make generate HARNESS=cursor` first)",
)
class TestCursorRoundTrip:
    def test_cursor_marketplace_lists_all_local_plugins(self):
        marketplace = WORKTREE / ".cursor-plugin" / "marketplace.json"
        data = json.loads(marketplace.read_text())
        cursor_names = {p["name"] for p in data["plugins"]}
        local_plugins = set(list_plugins())
        # Cursor marketplace mirrors the Claude marketplace, so it should include the
        # external git-subdir plugin (qa-orchestra) too.
        assert local_plugins.issubset(cursor_names), (
            f"Cursor marketplace missing plugins: {local_plugins - cursor_names}"
        )

    def test_cursor_per_plugin_manifests_exist(self):
        per_plugin = WORKTREE / ".cursor-plugin" / "plugins"
        if not per_plugin.is_dir():
            pytest.skip("per-plugin manifests not generated")
        manifest_names = {p.stem for p in per_plugin.glob("*.json")}
        local_plugins = set(list_plugins())
        missing = local_plugins - manifest_names
        assert not missing, f"Cursor per-plugin manifests missing for: {sorted(missing)}"

    def test_cursor_rules_only_use_allowed_keys(self):
        rules_dir = WORKTREE / ".cursor" / "rules"
        if not rules_dir.is_dir():
            pytest.skip(".cursor/rules/ not generated")
        allowed = {"description", "globs", "alwaysApply"}
        problems = []
        for mdc in rules_dir.glob("*.mdc"):
            fm, _ = parse_frontmatter(mdc.read_text())
            invalid_keys = set(fm.keys()) - allowed
            if invalid_keys:
                problems.append(f"{mdc.name}: invalid MDC keys {sorted(invalid_keys)}")
        assert not problems, "MDC frontmatter violations:\n  " + "\n  ".join(problems)


@pytest.mark.skipif(
    not (WORKTREE / "commands").is_dir(),
    reason="Gemini commands not generated (run `make generate HARNESS=gemini` first)",
)
class TestGeminiRoundTrip:
    def test_gemini_command_at_path_injections_resolve(self):
        """Every `@{plugins/foo/commands/bar.md}` in a generated Gemini TOML must
        point at a real source file."""
        broken = []
        at_pattern = re.compile(r"@\{(plugins/[^}]+)\}")
        for toml_path in (WORKTREE / "commands").rglob("*.toml"):
            try:
                data = tomllib.loads(toml_path.read_text())
            except tomllib.TOMLDecodeError:
                continue
            prompt = data.get("prompt", "")
            for match in at_pattern.findall(prompt):
                target = WORKTREE / match
                if not target.is_file():
                    broken.append(f"{toml_path.relative_to(WORKTREE)}: @{{{match}}} -> missing")
        assert not broken, "Broken Gemini @{path} injections:\n  " + "\n  ".join(broken[:20])

    def test_every_gemini_command_has_prompt_and_args(self):
        problems = []
        for toml_path in (WORKTREE / "commands").rglob("*.toml"):
            try:
                data = tomllib.loads(toml_path.read_text())
            except tomllib.TOMLDecodeError as e:
                problems.append(f"{toml_path.relative_to(WORKTREE)}: parse error {e}")
                continue
            if "description" not in data:
                problems.append(f"{toml_path.relative_to(WORKTREE)}: missing description")
            if "prompt" not in data:
                problems.append(f"{toml_path.relative_to(WORKTREE)}: missing prompt")
            elif "{{args}}" not in data["prompt"]:
                problems.append(f"{toml_path.relative_to(WORKTREE)}: prompt missing {{{{args}}}}")
        assert not problems, "Gemini TOML issues:\n  " + "\n  ".join(problems[:20])

    def test_gemini_md_within_cap(self):
        gemini_md = WORKTREE / "GEMINI.md"
        if not gemini_md.is_file():
            pytest.skip("GEMINI.md missing")
        lines = gemini_md.read_text().splitlines()
        assert len(lines) <= 150, f"GEMINI.md is {len(lines)} lines (cap: 150)"


@pytest.mark.skipif(
    not (WORKTREE / ".copilot").is_dir(),
    reason="Copilot artifacts not generated (run `make generate HARNESS=copilot` first)",
)
class TestCopilotRoundTrip:
    def test_copilot_agent_count_matches_source(self):
        n = len(list((WORKTREE / ".copilot" / "agents").glob("*.agent.md")))
        assert n == _source_agent_count(), (
            f"agent count mismatch: source={_source_agent_count()} copilot={n}"
        )

    def test_copilot_skill_count_matches_source(self):
        n = len(list((WORKTREE / ".copilot" / "skills").glob("*/SKILL.md")))
        expected = _source_skill_count() + _source_command_count()
        assert n == expected, (
            f"skill count mismatch: source_skills={_source_skill_count()} "
            f"source_commands={_source_command_count()} expected={expected} copilot={n}"
        )

    def test_copilot_command_count_matches_source(self):
        n = len(
            [p for p in (WORKTREE / ".copilot" / "commands").rglob("*.md") if p.name != "index.md"]
        )
        assert n == _source_command_count(), (
            f"command count mismatch: source={_source_command_count()} copilot={n}"
        )

    def test_copilot_command_entrypoints_exist_for_every_plugin(self):
        missing = []
        for plugin_name in list_plugins():
            entry = WORKTREE / ".copilot" / "commands" / plugin_name / "index.md"
            if not entry.is_file():
                missing.append(plugin_name)
        assert not missing, f"missing Copilot command entrypoints for: {sorted(missing)}"

    def test_every_copilot_agent_has_required_frontmatter(self):
        required = {"name", "description"}
        problems = []
        for agent_md in (WORKTREE / ".copilot" / "agents").glob("*.agent.md"):
            fm, _ = parse_frontmatter(agent_md.read_text())
            if not fm:
                problems.append(f"{agent_md.name}: no frontmatter")
                continue
            missing = required - set(fm.keys())
            if missing:
                problems.append(f"{agent_md.name}: missing {sorted(missing)}")
        assert not problems, "Copilot agent frontmatter issues:\n  " + "\n  ".join(problems[:20])


# ── Native-install manifests (always run; these are committed source) ─────────


class TestNativeInstallManifests:
    """Committed registries each harness's native plugin manager installs from.

    These are committed (not gitignored) so Codex + Cursor install straight from a clone;
    they point at the source `plugins/` dirs (no duplicated skill/agent trees).
    """

    def test_gemini_extension_manifest(self):
        path = WORKTREE / "gemini-extension.json"
        assert path.is_file(), "gemini-extension.json missing"
        data = json.loads(path.read_text())
        assert data.get("contextFileName") == "AGENTS.md", (
            "Gemini contextFileName must be AGENTS.md"
        )
        assert data.get("name"), "gemini-extension.json needs a name"
        assert data.get("version"), "gemini-extension.json needs a version"

    def test_codex_marketplace_lists_all_local_plugins(self):
        marketplace = WORKTREE / ".agents" / "plugins" / "marketplace.json"
        assert marketplace.is_file(), ".agents/plugins/marketplace.json missing"
        data = json.loads(marketplace.read_text())
        names = {p["name"] for p in data["plugins"]}
        local = set(list_plugins())
        assert local.issubset(names), f"Codex marketplace missing plugins: {local - names}"
        for p in data["plugins"]:
            assert p["source"]["path"] == f"./plugins/{p['name']}", (
                f"{p['name']}: marketplace source.path must point at the source plugin dir"
            )

    def test_codex_per_plugin_manifests_valid(self):
        problems = []
        for name in list_plugins():
            manifest = WORKTREE / "plugins" / name / ".codex-plugin" / "plugin.json"
            if not manifest.is_file():
                problems.append(f"{name}: plugins/{name}/.codex-plugin/plugin.json missing")
                continue
            try:
                data = json.loads(manifest.read_text())
            except json.JSONDecodeError as e:
                problems.append(f"{name}: {e}")
                continue
            if data.get("name") != name:
                problems.append(f"{name}: manifest name is {data.get('name')!r}")
            if data.get("skills") != "./skills/":
                problems.append(f"{name}: manifest skills is {data.get('skills')!r}")
        assert not problems, "Codex per-plugin manifest issues:\n  " + "\n  ".join(problems[:20])

    def test_claude_md_is_symlink_to_agents_md(self):
        claude = WORKTREE / "CLAUDE.md"
        assert claude.is_symlink(), "CLAUDE.md should be a symlink to AGENTS.md"
        assert claude.readlink() == Path("AGENTS.md"), (
            f"CLAUDE.md should point at AGENTS.md, points at {claude.readlink()}"
        )
        assert claude.read_text() == (WORKTREE / "AGENTS.md").read_text()


# ── Context file size budgets (always run) ───────────────────────────────────


class TestContextFileBudgets:
    """Every harness context file must be within its ~150-line / ~500-token budget."""

    @pytest.mark.parametrize(
        "name,cap",
        [
            ("CLAUDE.md", 200),  # slightly looser; project source-of-truth
            ("CONTRIBUTING.md", 150),
            ("GEMINI.md", 150),
            ("AGENTS.md", 150),
        ],
    )
    def test_context_file_within_cap(self, name: str, cap: int):
        path = WORKTREE / name
        if not path.is_file():
            pytest.skip(f"{name} not present")
        lines = path.read_text().splitlines()
        assert len(lines) <= cap, f"{name} is {len(lines)} lines (cap: {cap})"
