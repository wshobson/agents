"""Tests for tools/doc_gardener.py — verify each check fires on its anti-pattern."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from tools.doc_gardener import (
    Report,
    check_agent_divergence,
    check_codex_skill_caps,
    check_dead_links,
    check_doc_counts,
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


# ── Doc counts ───────────────────────────────────────────────────────────────


def _write_counts_fixture(tmp_path: Path, *, plugins: int, agents: int) -> None:
    """Build a tiny repo with `plugins` marketplace entries and `agents` agent files."""
    mp = tmp_path / ".claude-plugin"
    mp.mkdir(parents=True, exist_ok=True)
    (mp / "marketplace.json").write_text(
        json.dumps(
            {"plugins": [{"name": f"p{i}", "source": f"./plugins/p{i}"} for i in range(plugins)]}
        )
    )
    agents_dir = tmp_path / "plugins" / "demo" / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    for i in range(agents):
        (agents_dir / f"a{i}.md").write_text("---\nname: a\n---\nBody.\n")


class TestDocCounts:
    def test_matching_counts_no_finding(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / "README.md").write_text("We ship **12 plugins** and **34 agents** today.\n")

        report = Report()
        check_doc_counts(report)
        assert [f for f in report.findings if f.kind == "STALE_COUNT"] == []

    def test_stale_count_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / "README.md").write_text("We ship **11 plugins** and **34 agents** today.\n")

        report = Report()
        check_doc_counts(report)
        stale = [f for f in report.findings if f.kind == "STALE_COUNT"]
        assert len(stale) == 1
        assert stale[0].severity == "error"
        assert "says 11 plugins, actual is 12" in stale[0].message

    def test_reports_every_stale_mention(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / "README.md").write_text("11 plugins\n\nall 11 plugins by category\n")
        (tmp_path / "AGENTS.md").write_text("11 plugins here too\n")

        report = Report()
        check_doc_counts(report)
        assert len([f for f in report.findings if f.kind == "STALE_COUNT"]) == 3

    def test_single_digit_mismatch_is_caught(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """A count below 10 still has to match."""
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=9, agents=3)
        (tmp_path / "README.md").write_text("We ship 8 plugins and 3 agents today.\n")

        report = Report()
        check_doc_counts(report)
        stale = [f for f in report.findings if f.kind == "STALE_COUNT"]
        assert len(stale) == 1
        assert "says 8 plugins, actual is 9" in stale[0].message

    def test_subagents_is_checked_against_the_agent_total(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """AGENTS.md calls the agent total `subagents` in its cross-harness section."""
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / "AGENTS.md").write_text("33 subagents under `plugins/*/agents/`.\n")

        report = Report()
        check_doc_counts(report)
        stale = [f for f in report.findings if f.kind == "STALE_COUNT"]
        assert len(stale) == 1
        assert "says 33 subagents, actual is 34" in stale[0].message

    def test_matching_subagents_count_no_finding(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / "AGENTS.md").write_text("34 subagents under `plugins/*/agents/`.\n")

        report = Report()
        check_doc_counts(report)
        assert [f for f in report.findings if f.kind == "STALE_COUNT"] == []

    def test_singular_nouns_are_matched(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """A total of one is written in the singular and still has to match."""
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=1, agents=1)
        (tmp_path / "README.md").write_text("We ship 2 plugins and 1 agent today.\n")

        report = Report()
        check_doc_counts(report)
        stale = [f for f in report.findings if f.kind == "STALE_COUNT"]
        assert len(stale) == 1
        assert "says 2 plugins, actual is 1" in stale[0].message

    def test_singular_noun_matching_the_total_is_clean(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=1, agents=1)
        (tmp_path / "README.md").write_text("We ship 1 plugin and 1 agent today.\n")

        report = Report()
        check_doc_counts(report)
        assert [f for f in report.findings if f.kind == "STALE_COUNT"] == []

    def test_unparseable_marketplace_skips_the_plugin_count(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A broken manifest means the plugin total is unknown, not zero."""
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / ".claude-plugin" / "marketplace.json").write_text("{ this is not json")
        (tmp_path / "README.md").write_text("We ship 12 plugins and 30 agents today.\n")

        report = Report()
        check_doc_counts(report)
        stale = [f for f in report.findings if f.kind == "STALE_COUNT"]
        # The agent count is still checked; the plugin count is skipped entirely.
        assert len(stale) == 1
        assert "30 agents" in stale[0].message
        assert not any("plugins" in f.message for f in stale)

    def test_missing_marketplace_skips_the_plugin_count(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / ".claude-plugin" / "marketplace.json").unlink()
        (tmp_path / "README.md").write_text("We ship 99 plugins today.\n")

        report = Report()
        check_doc_counts(report)
        assert [f for f in report.findings if f.kind == "STALE_COUNT"] == []

    def test_manifest_with_wrong_root_type_skips_the_plugin_count(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """Valid JSON of the wrong shape is an unknown count, not a traceback."""
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / ".claude-plugin" / "marketplace.json").write_text("[]")
        (tmp_path / "README.md").write_text("We ship 99 plugins today.\n")

        report = Report()
        check_doc_counts(report)
        assert [f for f in report.findings if f.kind == "STALE_COUNT"] == []

    def test_manifest_with_null_plugins_skips_the_plugin_count(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        (tmp_path / ".claude-plugin" / "marketplace.json").write_text('{"plugins": null}')
        (tmp_path / "README.md").write_text("We ship 99 plugins today.\n")

        report = Report()
        check_doc_counts(report)
        assert [f for f in report.findings if f.kind == "STALE_COUNT"] == []

    def test_docs_subtotals_are_not_scanned(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Per-category subtotals under docs/ legitimately differ from the totals."""
        _patch_paths(monkeypatch, tmp_path)
        _write_counts_fixture(tmp_path, plugins=12, agents=34)
        docs = tmp_path / "docs"
        docs.mkdir(parents=True, exist_ok=True)
        (docs / "plugins.md").write_text("### Development (60 plugins)\n")

        report = Report()
        check_doc_counts(report)
        assert [f for f in report.findings if f.kind == "STALE_COUNT"] == []


# ── Agent divergence ─────────────────────────────────────────────────────────


def _write_agent(tmp_path: Path, plugin: str, filename: str, body: str) -> None:
    agents_dir = tmp_path / "plugins" / plugin / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / filename).write_text(f"---\nname: {plugin}-{filename[:-3]}\n---\n{body}")


class TestAgentDivergence:
    def test_single_copy_no_finding(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        _write_agent(tmp_path, "alpha", "reviewer.md", "Review carefully.\n")

        report = Report()
        check_agent_divergence(report)
        assert report.findings == []

    def test_verbatim_copies_are_not_findings(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """Identical bodies differing only by the namespaced `name:` are not drift."""
        _patch_paths(monkeypatch, tmp_path)
        _write_agent(tmp_path, "alpha", "reviewer.md", "Review carefully.\n")
        _write_agent(tmp_path, "beta", "reviewer.md", "Review carefully.\n")

        report = Report()
        check_agent_divergence(report)
        assert report.findings == []

    def test_diverged_bodies_warn(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_paths(monkeypatch, tmp_path)
        _write_agent(tmp_path, "alpha", "reviewer.md", "Review carefully.\n")
        _write_agent(tmp_path, "beta", "reviewer.md", "Review quickly instead.\n")

        report = Report()
        check_agent_divergence(report)
        assert [f.kind for f in report.findings] == ["AGENT_BODY_DIVERGENT"]
        finding = report.findings[0]
        assert finding.severity == "warning"
        assert "2 copies in 2 different versions" in finding.message

    def test_body_name_lines_still_count_as_content(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """Only the frontmatter name is normalized; a `name:` in the body is real content."""
        _patch_paths(monkeypatch, tmp_path)
        _write_agent(tmp_path, "alpha", "reviewer.md", "Example config:\n\nname: alpha-thing\n")
        _write_agent(tmp_path, "beta", "reviewer.md", "Example config:\n\nname: beta-thing\n")

        report = Report()
        check_agent_divergence(report)
        assert [f.kind for f in report.findings] == ["AGENT_BODY_DIVERGENT"]

    def test_body_name_lines_matching_stay_verbatim(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """Same body `name:` plus differing frontmatter names is still a verbatim copy."""
        _patch_paths(monkeypatch, tmp_path)
        _write_agent(tmp_path, "alpha", "reviewer.md", "Example config:\n\nname: shared\n")
        _write_agent(tmp_path, "beta", "reviewer.md", "Example config:\n\nname: shared\n")

        report = Report()
        check_agent_divergence(report)
        assert report.findings == []

    def test_agent_without_frontmatter_does_not_crash(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_paths(monkeypatch, tmp_path)
        for plugin in ("alpha", "beta"):
            agents_dir = tmp_path / "plugins" / plugin / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            (agents_dir / "bare.md").write_text("No frontmatter here.\n")

        report = Report()
        check_agent_divergence(report)
        assert report.findings == []

    def test_crlf_frontmatter_is_normalized(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """CRLF copies differing only by the namespaced name are not divergent."""
        _patch_paths(monkeypatch, tmp_path)
        for plugin in ("alpha", "beta"):
            agents_dir = tmp_path / "plugins" / plugin / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            (agents_dir / "reviewer.md").write_bytes(
                f"---\r\nname: {plugin}-reviewer\r\nmodel: opus\r\n---\r\nReview.\r\n".encode()
            )

        report = Report()
        check_agent_divergence(report)
        assert report.findings == []

    def test_frontmatter_closing_at_eof_is_normalized(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """An agent with no body after its frontmatter still normalizes."""
        _patch_paths(monkeypatch, tmp_path)
        for plugin in ("alpha", "beta"):
            agents_dir = tmp_path / "plugins" / plugin / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            (agents_dir / "reviewer.md").write_text(f"---\nname: {plugin}-reviewer\n---")

        report = Report()
        check_agent_divergence(report)
        assert report.findings == []

    def test_groups_variants_in_message(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Three copies sharing two bodies report as 3 copies / 2 versions."""
        _patch_paths(monkeypatch, tmp_path)
        _write_agent(tmp_path, "alpha", "reviewer.md", "Review carefully.\n")
        _write_agent(tmp_path, "beta", "reviewer.md", "Review carefully.\n")
        _write_agent(tmp_path, "gamma", "reviewer.md", "Something else entirely.\n")

        report = Report()
        check_agent_divergence(report)
        assert "3 copies in 2 different versions" in report.findings[0].message
        assert "alpha+beta" in report.findings[0].message
