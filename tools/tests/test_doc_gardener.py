"""Tests for tools/doc_gardener.py — verify each check fires on its anti-pattern."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from tools.doc_gardener import (
    Report,
    check_codex_skill_caps,
    check_dead_links,
    check_marketplace_consistency,
    check_oversized_context_files,
    check_stale_artifacts,
)


def _patch_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Redirect the gardener's WORKTREE, PLUGINS_DIR, etc. to tmp_path."""
    import tools.doc_gardener as dg

    monkeypatch.setattr(dg, "WORKTREE", tmp_path)
    monkeypatch.setattr(dg, "PLUGINS_DIR", tmp_path / "plugins")
    monkeypatch.setattr(dg, "DOCS_DIR", tmp_path / "docs")
    monkeypatch.setattr(dg, "MARKETPLACE_JSON", tmp_path / ".claude-plugin" / "marketplace.json")
    # Also patch the base module's WORKTREE / PLUGINS_DIR since list_plugins() uses them
    import tools.adapters.base as base

    monkeypatch.setattr(base, "WORKTREE", tmp_path)
    monkeypatch.setattr(base, "PLUGINS_DIR", tmp_path / "plugins")


# ── Stale artifacts ──────────────────────────────────────────────────────────


class TestStaleArtifacts:
    def test_fresh_artifacts_no_finding(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        # Set up source
        plugin = tmp_path / "plugins" / "demo"
        (plugin / "agents").mkdir(parents=True)
        src = plugin / "agents" / "greeter.md"
        src.write_text("---\nname: greeter\ndescription: Use when greeting.\n---\nBody.\n")
        # Set up generated artifact that's newer
        gen_dir = tmp_path / ".codex" / "agents"
        gen_dir.mkdir(parents=True)
        gen = gen_dir / "demo__greeter.toml"
        gen.write_text('name = "demo__greeter"\ndescription = "x"\ndeveloper_instructions = "y"\n')
        # Force gen mtime to be after source
        future = src.stat().st_mtime + 100
        import os

        os.utime(gen, (future, future))

        report = Report()
        check_stale_artifacts(report)
        assert [f for f in report.findings if f.kind == "STALE_ARTIFACT"] == []

    def test_stale_artifact_warns(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        plugin = tmp_path / "plugins" / "demo"
        (plugin / "agents").mkdir(parents=True)
        src = plugin / "agents" / "greeter.md"
        src.write_text("---\nname: greeter\ndescription: Use when greeting.\n---\nBody.\n")
        gen_dir = tmp_path / ".codex" / "agents"
        gen_dir.mkdir(parents=True)
        gen = gen_dir / "demo__greeter.toml"
        gen.write_text('name = "demo__greeter"\ndescription = "x"\ndeveloper_instructions = "y"\n')
        # Force src to be much newer
        import os

        past = gen.stat().st_mtime - 100
        os.utime(gen, (past, past))

        report = Report()
        check_stale_artifacts(report)
        assert [f for f in report.findings if f.kind == "STALE_ARTIFACT"]

    def test_opencode_skill_id_collision_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        first = tmp_path / "plugins" / "data-analysis" / "skills" / "report"
        second = tmp_path / "plugins" / "data" / "skills" / "analysis-report"
        first.mkdir(parents=True)
        second.mkdir(parents=True)
        for skill in (first, second):
            (skill / "SKILL.md").write_text(
                "---\nname: test\ndescription: Use when testing.\n---\n\nBody.\n"
            )
        (tmp_path / ".opencode" / "skills" / "data-analysis-report").mkdir(parents=True)

        report = Report()
        check_stale_artifacts(report)

        findings = [f for f in report.findings if f.kind == "opencode-skill-id-collision"]
        assert findings
        assert "data-analysis-report" in findings[0].message

    def test_missing_plugins_dir_does_not_crash_for_opencode_skills(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        skill = tmp_path / ".opencode" / "skills" / "demo-greeter"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: demo-greeter\ndescription: Use when greeting.\n---\n\nBody.\n"
        )

        report = Report()
        check_stale_artifacts(report)

        assert [f for f in report.findings if f.kind == "opencode-skill-id-collision"] == []


# ── Context file size ────────────────────────────────────────────────────────


class TestContextFiles:
    def test_within_budget_no_finding(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        (tmp_path / "AGENTS.md").write_text("\n".join(["line"] * 80))
        report = Report()
        check_oversized_context_files(report)
        assert not [f for f in report.findings if f.kind == "CONTEXT_FILE_OVERSIZED"]

    def test_over_budget_warns(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        (tmp_path / "AGENTS.md").write_text("\n".join(["line"] * 200))
        report = Report()
        check_oversized_context_files(report)
        findings = [f for f in report.findings if f.kind == "CONTEXT_FILE_OVERSIZED"]
        assert findings and "200 lines" in findings[0].message


# ── Dead links ───────────────────────────────────────────────────────────────


class TestDeadLinks:
    def test_valid_links_no_finding(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "a.md").write_text("[link to b](b.md)\n")
        (tmp_path / "docs" / "b.md").write_text("# B\n")
        report = Report()
        check_dead_links(report)
        assert not [f for f in report.findings if f.kind == "DEAD_LINK"]

    def test_dead_link_warns(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "a.md").write_text("[missing](does-not-exist.md)\n")
        report = Report()
        check_dead_links(report)
        findings = [f for f in report.findings if f.kind == "DEAD_LINK"]
        assert findings

    def test_external_links_skipped(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        (tmp_path / "docs").mkdir()
        (tmp_path / "docs" / "a.md").write_text(
            "[external](https://example.com)\n[mailto](mailto:x@x)\n[anchor](#top)\n"
        )
        report = Report()
        check_dead_links(report)
        assert not [f for f in report.findings if f.kind == "DEAD_LINK"]


# ── Codex skill cap ──────────────────────────────────────────────────────────


class TestCodexSkillCaps:
    def test_under_cap_no_finding(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        sk = tmp_path / "plugins" / "demo" / "skills" / "small"
        sk.mkdir(parents=True)
        (sk / "SKILL.md").write_text(
            "---\nname: small\ndescription: Use when small.\n---\n\nSmall body.\n"
        )
        report = Report()
        check_codex_skill_caps(report)
        assert not [f for f in report.findings if f.kind == "SKILL_OVER_CODEX_CAP"]

    def test_over_cap_without_references_warns(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        sk = tmp_path / "plugins" / "demo" / "skills" / "big"
        sk.mkdir(parents=True)
        (sk / "SKILL.md").write_text(
            "---\nname: big\ndescription: Use when big.\n---\n\n" + "x" * 9000
        )
        report = Report()
        check_codex_skill_caps(report)
        assert [f for f in report.findings if f.kind == "SKILL_OVER_CODEX_CAP"]

    def test_over_cap_with_references_no_finding(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        sk = tmp_path / "plugins" / "demo" / "skills" / "big"
        sk.mkdir(parents=True)
        (sk / "SKILL.md").write_text(
            "---\nname: big\ndescription: Use when big.\n---\n\n" + "x" * 9000
        )
        (sk / "references").mkdir()
        (sk / "references" / "details.md").write_text("More.\n")
        report = Report()
        check_codex_skill_caps(report)
        assert not [f for f in report.findings if f.kind == "SKILL_OVER_CODEX_CAP"]


# ── Marketplace consistency ──────────────────────────────────────────────────


class TestMarketplaceConsistency:
    def _write_marketplace(self, tmp_path: Path, plugins: list[dict]) -> None:
        mkt_dir = tmp_path / ".claude-plugin"
        mkt_dir.mkdir(parents=True, exist_ok=True)
        (mkt_dir / "marketplace.json").write_text(
            json.dumps({"name": "test", "owner": {"name": "x"}, "plugins": plugins})
        )

    def test_local_orphan_warns(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        (tmp_path / "plugins").mkdir()
        self._write_marketplace(
            tmp_path, [{"name": "missing-plugin", "source": "./plugins/missing-plugin"}]
        )

        report = Report()
        check_marketplace_consistency(report)
        assert [f for f in report.findings if f.kind == "MARKETPLACE_ORPHAN"]

    def test_external_plugin_not_orphaned(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """git-subdir / git source plugins legitimately have no plugins/<name>/."""
        _patch_paths(monkeypatch, tmp_path)
        (tmp_path / "plugins").mkdir()
        self._write_marketplace(
            tmp_path,
            [
                {
                    "name": "external-plug",
                    "source": {
                        "source": "git-subdir",
                        "url": "https://github.com/x/y.git",
                        "path": ".",
                    },
                }
            ],
        )

        report = Report()
        check_marketplace_consistency(report)
        assert not [f for f in report.findings if f.kind == "MARKETPLACE_ORPHAN"]

    def test_unregistered_local_plugin_info(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        plug = tmp_path / "plugins" / "unregistered"
        plug.mkdir(parents=True)
        (plug / ".claude-plugin").mkdir()
        (plug / ".claude-plugin" / "plugin.json").write_text('{"name": "unregistered"}')
        self._write_marketplace(tmp_path, [])  # empty marketplace

        report = Report()
        check_marketplace_consistency(report)
        assert [f for f in report.findings if f.kind == "MARKETPLACE_MISSING"]
