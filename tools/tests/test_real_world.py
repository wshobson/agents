"""Real-source structural tests — run against the actual `plugins/` tree.

These complement the synthetic-fixture adapter tests (`test_adapters.py`) by catching
issues that only surface on real content: malformed frontmatter in a checked-in skill,
broken `@{path}` injections, stale marketplace entries, etc.

Designed to run in CI without API keys.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

# Make tools.* importable when pytest runs from anywhere.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.adapters.base import (  # noqa: E402
    PLUGINS_DIR,
    WORKTREE,
    list_plugins,
    load_plugin,
    parse_frontmatter,
)

# Real source skips marketplace orphans (qa-orchestra is external git-subdir).
_EXTERNAL_PLUGINS: set[str] = {"qa-orchestra"}

# Trigger phrasing matcher — same regex plugin_eval/layers/static.py uses for MISSING_TRIGGER.
_TRIGGER_PATTERN = re.compile(
    r"\b(?:should\s+be\s+)?used?\s+(?:this\s+skill\s+)?(?:immediately\s+)?"
    r"(?:when|after|before|whenever)\b"
    r"|\buse\s+proactively\b"
    r"|\btrigger(?:s)?\s+(?:when|on)\b"
    r"|\bauto[-\s]?loads?\s+(?:when|on)\b",
    re.IGNORECASE,
)

# Codex built-in agent names that custom agents must NOT collide with.
_CODEX_BUILTIN_AGENTS = {"default", "worker", "explorer"}


# ── Marketplace consistency ─────────────────────────────────────────────────


class TestMarketplaceConsistency:
    def test_every_local_marketplace_entry_resolves_to_plugin_dir(self):
        mp = json.loads((WORKTREE / ".claude-plugin" / "marketplace.json").read_text())
        for entry in mp.get("plugins", []):
            source = entry.get("source")
            if isinstance(source, str) and source.startswith("./plugins/"):
                plugin_path = WORKTREE / source.removeprefix("./")
                assert plugin_path.is_dir(), f"{entry['name']}: source {source} does not exist"
                assert (plugin_path / ".claude-plugin" / "plugin.json").is_file(), (
                    f"{entry['name']}: missing .claude-plugin/plugin.json"
                )

    def test_every_local_plugin_dir_appears_in_marketplace(self):
        mp = json.loads((WORKTREE / ".claude-plugin" / "marketplace.json").read_text())
        listed = {e["name"] for e in mp.get("plugins", []) if isinstance(e.get("source"), str)}
        actual = set(list_plugins())
        missing = actual - listed
        assert not missing, f"plugins/ dirs not in marketplace.json: {sorted(missing)}"

    def test_marketplace_version_matches_per_plugin_json(self):
        """Each marketplace.json entry's version must match plugins/<name>/.claude-plugin/plugin.json."""
        mp = json.loads((WORKTREE / ".claude-plugin" / "marketplace.json").read_text())
        mismatches = []
        for entry in mp.get("plugins", []):
            source = entry.get("source")
            if not (isinstance(source, str) and source.startswith("./plugins/")):
                continue
            name = entry["name"]
            mp_version = entry.get("version", "")
            pj_path = WORKTREE / source.removeprefix("./") / ".claude-plugin" / "plugin.json"
            if not pj_path.is_file():
                continue
            pj_version = json.loads(pj_path.read_text()).get("version", "")
            if mp_version != pj_version:
                mismatches.append(f"{name}: marketplace={mp_version} vs plugin.json={pj_version}")
        assert not mismatches, (
            "Version drift between marketplace.json and per-plugin plugin.json:\n  "
            + "\n  ".join(mismatches)
        )


# ── Plugin source integrity ─────────────────────────────────────────────────


class TestPluginSourceIntegrity:
    @pytest.mark.parametrize("plugin_name", list_plugins())
    def test_plugin_loads_without_error(self, plugin_name: str):
        plugin = load_plugin(plugin_name)
        assert plugin is not None, f"{plugin_name}: load_plugin returned None"

    def test_no_plugin_name_contains_double_underscore(self):
        """Plugin names with __ collide with the adapter namespace separator."""
        bad = [p for p in list_plugins() if "__" in p]
        assert not bad, f"plugin names with `__`: {bad}"

    def test_every_agent_has_name_and_description(self):
        problems = []
        for plugin_name in list_plugins():
            plugin = load_plugin(plugin_name)
            if not plugin:
                continue
            for agent in plugin.agents:
                if not agent.frontmatter.get("name"):
                    problems.append(f"{plugin_name}/agents/{agent.name}: missing name")
                if not agent.description:
                    problems.append(f"{plugin_name}/agents/{agent.name}: missing description")
        assert not problems, "Agents missing required frontmatter:\n  " + "\n  ".join(problems)

    def test_every_skill_has_trigger_phrase(self):
        """Per plugin-eval's MISSING_TRIGGER check: every description must include a recognized phrase."""
        problems = []
        for plugin_name in list_plugins():
            plugin = load_plugin(plugin_name)
            if not plugin:
                continue
            for skill in plugin.skills:
                if not _TRIGGER_PATTERN.search(skill.description):
                    problems.append(
                        f"{plugin_name}/skills/{skill.name}: description has no trigger phrase "
                        f"(saw: {skill.description[:80]!r})"
                    )
        assert not problems, "Skills with missing trigger phrases:\n  " + "\n  ".join(problems[:20])

    def test_no_agent_collides_with_codex_builtin(self):
        """Codex has built-in agents `default`, `worker`, `explorer`. Custom agents must not use these names."""
        collisions = []
        for plugin_name in list_plugins():
            plugin = load_plugin(plugin_name)
            if not plugin:
                continue
            for agent in plugin.agents:
                if agent.name.lower() in _CODEX_BUILTIN_AGENTS:
                    collisions.append(f"{plugin_name}/agents/{agent.name}")
        assert not collisions, (
            f"Agent names colliding with Codex built-ins (default/worker/explorer): {collisions}"
        )


# ── Progressive-disclosure refactor integrity ────────────────────────────────


class TestProgressiveDisclosureIntegrity:
    """Catches regressions in the SKILL.md → references/details.md refactor."""

    def _modified_skills(self) -> list[tuple[str, Path, Path]]:
        """Yield (plugin, SKILL.md, references/details.md) for every refactored skill."""
        out: list[tuple[str, Path, Path]] = []
        for skill_md in PLUGINS_DIR.glob("*/skills/*/SKILL.md"):
            details = skill_md.parent / "references" / "details.md"
            if details.is_file():
                plugin_name = skill_md.parent.parent.parent.name
                out.append((plugin_name, skill_md, details))
        return out

    def test_every_refactored_skill_has_meaningful_details(self):
        """Skills with `references/details.md` should have meaningful content there
        (≥500 bytes) — not an empty stub."""
        too_small = []
        for plugin_name, _, details in self._modified_skills():
            size = len(details.read_text().encode("utf-8"))
            if size < 500:
                too_small.append(f"{plugin_name}/{details.relative_to(PLUGINS_DIR)}: {size}B")
        assert not too_small, (
            "references/details.md files are suspiciously small (<500B), "
            "suggesting failed extraction:\n  " + "\n  ".join(too_small)
        )

    def test_extracted_skills_have_pointer_to_references(self):
        """When a skill has `references/details.md`, the SKILL.md body should mention
        `references/details.md` (or `references/`) so the agent knows where to look."""
        missing_pointer = []
        for plugin_name, skill_md, _ in self._modified_skills():
            body = skill_md.read_text()
            if "references/" not in body:
                missing_pointer.append(f"{plugin_name}/{skill_md.relative_to(PLUGINS_DIR)}")
        assert not missing_pointer, (
            "Refactored skills missing pointer to references/:\n  " + "\n  ".join(missing_pointer)
        )

    def test_extracted_skills_preserve_when_to_use(self):
        """Every refactored skill should still have a "When to Use" or equivalent
        navigation section in the SKILL.md body — losing it strips the model's
        ability to decide when to activate."""
        # Common headings that serve as the nav tier
        nav_markers = [
            "## When to Use",
            "## Overview",
            "## Purpose",
            "## Core Concepts",
            "## Quick Start",
            "## Input",
        ]
        missing = []
        for plugin_name, skill_md, _ in self._modified_skills():
            body = skill_md.read_text()
            if not any(marker in body for marker in nav_markers):
                missing.append(f"{plugin_name}/{skill_md.relative_to(PLUGINS_DIR)}")
        assert not missing, "Refactored skills missing navigation-tier section:\n  " + "\n  ".join(
            missing
        )

    def test_no_refactored_skill_is_stub_only(self):
        """A refactored skill's SKILL.md body should be at least ~600 bytes —
        anything smaller is a stub that's lost the quick-start tier."""
        stubs = []
        for plugin_name, skill_md, _ in self._modified_skills():
            fm, body = parse_frontmatter(skill_md.read_text())
            if len(body.encode("utf-8")) < 600:
                stubs.append(
                    f"{plugin_name}/{skill_md.relative_to(PLUGINS_DIR)}: body {len(body.encode())}B"
                )
        assert not stubs, (
            "Refactored skills with stub-sized bodies (<600B) — quick-start tier likely lost:\n  "
            + "\n  ".join(stubs)
        )


# ── plugin.json integrity ─────────────────────────────────────────────────


class TestPluginJsonIntegrity:
    @pytest.mark.parametrize("plugin_name", list_plugins())
    def test_plugin_json_has_name_and_version(self, plugin_name: str):
        pj_path = PLUGINS_DIR / plugin_name / ".claude-plugin" / "plugin.json"
        data = json.loads(pj_path.read_text())
        assert data.get("name"), f"{plugin_name}: plugin.json missing 'name'"
        assert data.get("version"), f"{plugin_name}: plugin.json missing 'version'"
        # plugin.json `name` should match directory name
        assert data["name"] == plugin_name, (
            f"{plugin_name}: plugin.json name={data['name']!r} doesn't match dir name"
        )
