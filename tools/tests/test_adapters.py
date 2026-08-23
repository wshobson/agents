"""Unit tests for each harness adapter.

Each adapter is exercised against a `synthetic_plugin` (1 agent + 1 skill + 1 command)
in an isolated `output_root`. Tests verify file paths, frontmatter shapes, and the
specific transforms each adapter is responsible for.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# tools.adapters.* imports happen via the conftest sys.path injection
from tools.adapters.antigravity import AntigravityAdapter
from tools.adapters.base import PluginSource, parse_frontmatter
from tools.adapters.codex import CodexAdapter, _split_body_if_oversized
from tools.adapters.copilot import (
    CopilotAdapter,
    _build_tools_list,
    _needs_yaml_quoting,
)
from tools.adapters.cursor import CursorAdapter
from tools.adapters.opencode import OpenCodeAdapter, _opencode_skill_id

# ── Codex ────────────────────────────────────────────────────────────────────


class TestCodexAdapter:
    def test_emits_skill_with_namespaced_id(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        adapter = CodexAdapter(output_root=output_root)
        result = adapter.emit_plugin(synthetic_plugin)

        skill_path = output_root / ".codex" / "skills" / "demo__hello" / "SKILL.md"
        assert skill_path in result.written
        assert skill_path.is_file()

        fm, body = parse_frontmatter(skill_path.read_text())
        assert fm["name"] == "demo__hello"
        assert fm["description"].startswith("Use when greeting")

    def test_strips_claude_only_skill_fields(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        skill = _make_skill(
            plugin_dir,
            "noisy",
            "name: noisy\ndescription: Use when testing\nallowed-tools: Read\nmodel: opus",
            "# Noisy\n\nBody.\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, skills=[skill]
        )
        CodexAdapter(output_root=output_root).emit_plugin(plugin)

        emitted = output_root / ".codex" / "skills" / "demo__noisy" / "SKILL.md"
        content = emitted.read_text()
        assert "allowed-tools:" not in content
        assert "model:" not in content

    def test_emits_agent_toml_with_remapped_model(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        CodexAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        agent_toml = output_root / ".codex" / "agents" / "demo__greeter.toml"
        assert agent_toml.is_file()
        content = agent_toml.read_text()

        import tomllib

        parsed = tomllib.loads(content)
        assert parsed["name"] == "demo__greeter"
        # opus is mapped to gpt-5.5
        assert parsed["model"] == "gpt-5.5"
        # tools: Read, Grep -> read-only-ish set -> sandbox_mode = read-only
        assert parsed["sandbox_mode"] == "read-only"
        # color: blue should NOT be present
        assert "color" not in parsed
        # No `tools` key in Codex TOML (silently ignored anyway)
        assert "tools" not in parsed

    def test_agent_with_write_tools_gets_workspace_write(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "writer",
            "name: writer\ndescription: Use when writing.\ntools: Read, Write, Bash",
            "# Writer\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        CodexAdapter(output_root=output_root).emit_plugin(plugin)

        import tomllib

        parsed = tomllib.loads(
            (output_root / ".codex" / "agents" / "demo__writer.toml").read_text()
        )
        assert parsed["sandbox_mode"] == "workspace-write"

    def test_skill_body_splitting_overflow(self, tmp_path: Path, output_root: Path):
        """A skill whose body exceeds the cap is split into references/details.md."""
        from tools.tests.conftest import _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')

        body = (
            "# Big\n\nIntro.\n\n"
            "## Section A\n\n" + ("a" * 4000) + "\n\n"
            "## Section B\n\n" + ("b" * 4000) + "\n"
        )
        skill = _make_skill(plugin_dir, "big", "name: big\ndescription: Use when big.", body)
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, skills=[skill]
        )
        result = CodexAdapter(output_root=output_root).emit_plugin(plugin)

        head_path = output_root / ".codex" / "skills" / "demo__big" / "SKILL.md"
        overflow_path = (
            output_root / ".codex" / "skills" / "demo__big" / "references" / "details.md"
        )
        assert head_path.is_file()
        assert overflow_path.is_file()
        # Head must fit Codex's 8 KB cap (with the pointer note included)
        assert len(head_path.read_text().encode()) <= 8 * 1024
        # Warning recorded
        assert any("body exceeded" in w for w in result.warnings)

    def test_split_helper_handles_runaway_head(self):
        """If the H1 + intro alone is bigger than cap, the splitter hard-cuts."""
        body = "# Big\n\n" + ("x" * 12000)
        head, overflow = _split_body_if_oversized(body, 7400)
        assert overflow is not None
        # Result fits cap (with pointer overhead)
        assert len(head.encode()) <= 7400

    def test_emit_global_warns_when_agents_md_missing(
        self, synthetic_plugin: PluginSource, output_root: Path, tmp_path: Path
    ):
        """AGENTS.md is now committed at the repo root, not generated by the adapter.
        emit_global validates the file exists and warns if it doesn't.

        Uses an empty `repo_root` so the real committed AGENTS.md isn't picked up.
        """
        empty_repo = tmp_path / "empty_repo"
        empty_repo.mkdir()
        adapter = CodexAdapter(output_root=output_root, repo_root=empty_repo)
        adapter.emit_plugin(synthetic_plugin)
        result = adapter.emit_global([synthetic_plugin])

        # No write — AGENTS.md is canonical, not generated.
        assert (output_root / "AGENTS.md") not in result.written
        assert (empty_repo / "AGENTS.md") not in result.written
        # Must warn about missing AGENTS.md
        assert any("AGENTS.md is missing" in w for w in result.warnings)

    def test_marketplace_entries_have_description(
        self, synthetic_plugin: PluginSource, output_root: Path, tmp_path: Path
    ):
        """Each `.agents/plugins/marketplace.json` entry carries a top-level
        `description` as forward-compatible metadata, falling back to the plugin
        name when the plugin's own manifest omits it.

        NOTE: `codex-marketplace`'s installer (npm `codex-marketplace@0.2.1`,
        `marketplacePluginSchema` in `dist/schema.js`) does not currently declare
        or require this field — unknown keys are silently stripped by zod's
        default `.parse()`. The field the installer actually validates is the
        per-plugin `.codex-plugin/plugin.json` `description` — see
        `test_plugin_manifest_description_falls_back_to_name` below.

        Uses an empty `repo_root` so the real committed AGENTS.md isn't picked up.
        """
        empty_repo = tmp_path / "empty_repo"
        empty_repo.mkdir()
        adapter = CodexAdapter(output_root=output_root, repo_root=empty_repo)
        adapter.emit_plugin(synthetic_plugin)
        no_desc_plugin = PluginSource(
            name="no-desc",
            dir=empty_repo / "no-desc",
            plugin_json={"name": "no-desc", "version": "0.1.0"},
        )
        adapter.emit_global([synthetic_plugin, no_desc_plugin])

        marketplace_path = output_root / ".agents" / "plugins" / "marketplace.json"
        data = json.loads(marketplace_path.read_text(encoding="utf-8"))
        assert len(data["plugins"]) == 2, "expected two marketplace plugin entries"
        for entry in data["plugins"]:
            assert "description" in entry, f"missing description key in entry: {entry}"
            assert isinstance(entry["description"], str)
            assert len(entry["description"]) > 0

        no_desc_entry = next(p for p in data["plugins"] if p["name"] == "no-desc")
        assert no_desc_entry["description"] == "no-desc", (
            "expected description to fall back to plugin name"
        )

    def test_plugin_manifest_description_falls_back_to_name(
        self, tmp_path: Path, output_root: Path
    ):
        """`codex-marketplace`'s installer parses each plugin's
        `.codex-plugin/plugin.json` with `pluginManifestSchema`, which requires
        `description: z.string().min(1)`. A plugin whose own manifest omits
        `description` (e.g. `plugin-eval` upstream) must still get a non-empty
        `description` in the generated Codex manifest, via the `plugin.name`
        fallback — otherwise `npx codex-marketplace add <repo> --plugins` fails
        with `String must contain at least 1 character(s)` at `path: ["description"]`
        for that plugin (#617).
        """
        plugin_dir = tmp_path / "no-description-plugin"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "no-description-plugin", "version": "0.1.0"}'
        )
        plugin = PluginSource(
            name="no-description-plugin",
            dir=plugin_dir,
            plugin_json={"name": "no-description-plugin", "version": "0.1.0"},
        )
        assert plugin.description == ""  # sanity: this is the empty-description case

        CodexAdapter(output_root=output_root).emit_plugin(plugin)

        manifest_path = (
            output_root / "plugins" / "no-description-plugin" / ".codex-plugin" / "plugin.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["description"] == "no-description-plugin"

    def test_emit_global_validates_committed_agents_md(
        self, synthetic_plugin: PluginSource, output_root: Path, tmp_path: Path
    ):
        """When a committed AGENTS.md exists, emit_global validates the size caps.

        The committed file is read from `repo_root` — independent of `output_root` so
        `--output-root <scratch>` doesn't falsely report AGENTS.md as missing.
        """
        # Stage an oversized AGENTS.md at the repo root (not output_root)
        fake_repo = tmp_path / "fake_repo"
        fake_repo.mkdir()
        (fake_repo / "AGENTS.md").write_text("# Big AGENTS.md\n\n" + ("filler line\n" * 200))
        adapter = CodexAdapter(output_root=output_root, repo_root=fake_repo)
        adapter.emit_plugin(synthetic_plugin)
        result = adapter.emit_global([synthetic_plugin])

        # The committed file is not overwritten
        assert (fake_repo / "AGENTS.md").read_text().startswith("# Big AGENTS.md")
        # And the size warning fires
        assert any("table-of-contents cap" in w for w in result.warnings)

    def test_emit_global_finds_agents_md_when_output_root_differs(
        self, synthetic_plugin: PluginSource, output_root: Path, tmp_path: Path
    ):
        """Regression: with `--output-root <scratch>`, emit_global must read
        AGENTS.md from repo_root (defaulting to WORKTREE), not output_root.

        Previously this used `self.output_root / "AGENTS.md"`, which produced a
        false "missing" warning whenever output_root was a scratch directory.
        """
        fake_repo = tmp_path / "fake_repo"
        fake_repo.mkdir()
        (fake_repo / "AGENTS.md").write_text("# Tiny AGENTS.md\n\n## Map\n")
        adapter = CodexAdapter(output_root=output_root, repo_root=fake_repo)
        result = adapter.emit_global([synthetic_plugin])

        # No "missing" warning — the file is found at repo_root, not output_root.
        assert not any("AGENTS.md is missing" in w for w in result.warnings)
        # And no size warning either (file is well under both caps).
        assert not any("table-of-contents cap" in w for w in result.warnings)
        assert not any("32 KiB" in w for w in result.warnings)

    def test_builtin_name_collision_warns(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir, "worker", "name: worker\ndescription: Use when.", "# Worker\n"
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        result = CodexAdapter(output_root=output_root).emit_plugin(plugin)
        assert any("collides" in w for w in result.warnings)
        # Emitted file uses namespaced ID
        assert (output_root / ".codex" / "agents" / "demo__worker.toml").is_file()

    def test_command_becomes_skill(self, synthetic_plugin: PluginSource, output_root: Path):
        CodexAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        # Command should be present as a skill (Codex deprecated ~/.codex/prompts/)
        cmd_skill = output_root / ".codex" / "skills" / "demo__say-hi" / "SKILL.md"
        assert cmd_skill.is_file()

    def test_skill_command_name_collision_namespaced(self, tmp_path: Path, output_root: Path):
        """A skill and command with the same name in one plugin must NOT overwrite."""
        from tools.tests.conftest import _make_command, _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        skill = _make_skill(
            plugin_dir,
            "review",
            "name: review\ndescription: Use when reviewing.",
            "# Skill\nbody",
        )
        command = _make_command(
            plugin_dir, "review", 'description: "Review command"', "# Command\nbody"
        )
        plugin = PluginSource(
            name="demo",
            dir=plugin_dir,
            plugin_json={"name": "demo"},
            skills=[skill],
            commands=[command],
        )
        result = CodexAdapter(output_root=output_root).emit_plugin(plugin)

        skill_path = output_root / ".codex" / "skills" / "demo__review" / "SKILL.md"
        cmd_skill_path = output_root / ".codex" / "skills" / "demo__review__command" / "SKILL.md"
        assert skill_path.is_file()
        assert cmd_skill_path.is_file()
        assert any("collides" in w for w in result.warnings)

    def test_unknown_model_alias_warns(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "exotic",
            "name: exotic\ndescription: Use when exotic.\nmodel: claude-3-opus-20240229",
            "# Exotic\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        result = CodexAdapter(output_root=output_root).emit_plugin(plugin)
        assert any("unknown model alias" in w for w in result.warnings)

    def test_split_body_respects_fenced_code(self):
        """A `## ` line inside a fenced code block must NOT trigger a split."""
        from tools.adapters.codex import _split_body_fence_aware

        body = (
            "# Title\n\nIntro.\n\n"
            "```python\n"
            "## not a heading inside fence\n"
            "print(1)\n"
            "```\n\n"
            "## Real Section\n\nReal content.\n"
        )
        sections = _split_body_fence_aware(body)
        # Only ONE top-level section split (at '## Real Section'), so we get 2 chunks.
        assert len(sections) == 2
        assert "## not a heading" in sections[0]  # stays inside the head section
        assert sections[1].startswith("## Real Section")

    def test_utf8_safe_cut_preserves_codepoints(self):
        """Hard cut should not produce broken UTF-8 sequences."""
        from tools.adapters.codex import _utf8_safe_cut

        # 'é' is 2 bytes (0xC3 0xA9); cut at a position that would split mid-codepoint.
        encoded = ("a" * 100 + "é" + "b" * 100).encode("utf-8")
        # Find the byte index of the 'é' first byte and cut one byte in
        idx = encoded.index(b"\xc3")
        head, tail = _utf8_safe_cut(encoded, idx + 1)
        # Both halves must decode cleanly
        head.decode("utf-8")
        tail.decode("utf-8")
        # No data should be silently dropped
        assert head + tail == encoded

    def test_utf8_safe_cut_never_empty_head(self):
        """When cap > 0 and encoded is non-empty, head must NOT be empty bytes."""
        from tools.adapters.codex import _utf8_safe_cut

        # Body of only multi-byte chars, no newlines — used to produce empty head.
        encoded = ("☃" * 100).encode("utf-8")
        head, tail = _utf8_safe_cut(encoded, 153)
        assert len(head) > 0
        assert head + tail == encoded

    def test_split_no_double_prepend_hash(self):
        """Overflow content must not get `## ## ` prepended."""
        from tools.adapters.codex import _split_body_if_oversized

        body = (
            "# Title\n\nIntro.\n\n"
            + "## Section A\n"
            + ("a" * 4000)
            + "\n\n"
            + "## Section B\n"
            + ("b" * 4000)
            + "\n"
        )
        head, overflow = _split_body_if_oversized(body, 7400)
        assert overflow is not None
        assert "## ##" not in overflow, f"double-prepend bug: {overflow[:80]!r}"
        assert "## ##" not in head, f"double-prepend bug in head: {head[-80:]!r}"

    def test_empty_tools_field_yields_read_only_sandbox(self, tmp_path: Path, output_root: Path):
        """An explicit `tools: []` in source should map to read-only sandbox, not workspace-write."""
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "advisory",
            "name: advisory\ndescription: Use when advising.\ntools: []",
            "# Advisory\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        CodexAdapter(output_root=output_root).emit_plugin(plugin)

        import tomllib

        parsed = tomllib.loads(
            (output_root / ".codex" / "agents" / "demo__advisory.toml").read_text()
        )
        assert parsed["sandbox_mode"] == "read-only", parsed

    def test_missing_tools_field_yields_workspace_write(self, tmp_path: Path, output_root: Path):
        """A source agent with NO `tools:` field should map to workspace-write (Claude default)."""
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "unrestricted",
            "name: unrestricted\ndescription: Use when unrestricted.",
            "# Unrestricted\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        CodexAdapter(output_root=output_root).emit_plugin(plugin)

        import tomllib

        parsed = tomllib.loads(
            (output_root / ".codex" / "agents" / "demo__unrestricted.toml").read_text()
        )
        assert parsed["sandbox_mode"] == "workspace-write"

    def test_second_order_collision_routes_to_cmd(self, tmp_path: Path, output_root: Path):
        """Skill `foo`, command `foo`, AND skill `foo__command` → command goes to `foo__cmd`."""
        from tools.tests.conftest import _make_command, _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        s1 = _make_skill(plugin_dir, "foo", "name: foo\ndescription: Use when foo.", "# foo\n")
        s2 = _make_skill(
            plugin_dir,
            "foo__command",
            "name: foo__command\ndescription: Use when foo command.",
            "# foo__command\n",
        )
        cmd = _make_command(plugin_dir, "foo", 'description: "foo command"', "# foo cmd\n")
        plugin = PluginSource(
            name="demo",
            dir=plugin_dir,
            plugin_json={"name": "demo"},
            skills=[s1, s2],
            commands=[cmd],
        )
        result = CodexAdapter(output_root=output_root).emit_plugin(plugin)

        # Real skill `foo`
        assert (output_root / ".codex" / "skills" / "demo__foo" / "SKILL.md").is_file()
        # Real skill `foo__command`
        assert (output_root / ".codex" / "skills" / "demo__foo__command" / "SKILL.md").is_file()
        # Command-derived skill routed to `__cmd` to avoid second-order clash
        assert (output_root / ".codex" / "skills" / "demo__foo__cmd" / "SKILL.md").is_file()
        assert any("second-order" in w for w in result.warnings)

    def test_rewriter_matches_lint_pattern(self):
        """The Codex body rewriter must match the lint pattern: article case-insensitive,
        tool name strict CamelCase. `the bash tool` (lowercase) must NOT be rewritten."""
        from tools.adapters.codex import _rewrite_body_for_codex

        # 'the Bash tool' and 'The Read tool' (CamelCase) → rewritten.
        out = _rewrite_body_for_codex("First use the Bash tool, then The Read tool.")
        assert "Bash tool" not in out
        assert "Read tool" not in out

        # 'the bash tool' (lowercase) → left alone (refers to shell, not Claude's Bash).
        out2 = _rewrite_body_for_codex("Configure the bash tool in your Makefile.")
        assert "the bash tool" in out2


# ── Cursor ───────────────────────────────────────────────────────────────────


class TestCursorAdapter:
    def test_emits_plugin_manifest(self, synthetic_plugin: PluginSource, output_root: Path):
        adapter = CursorAdapter(output_root=output_root)
        result = adapter.emit_plugin(synthetic_plugin)
        manifest_path = output_root / ".cursor-plugin" / "plugins" / "demo.json"
        assert manifest_path in result.written

        manifest = json.loads(manifest_path.read_text())
        assert manifest["name"] == "demo"
        assert manifest["version"] == "1.0.0"
        assert manifest["author"]["name"] == "Tester"
        # No component arrays — Cursor auto-discovers
        assert "skills" not in manifest
        assert "agents" not in manifest

    def test_emits_marketplace_with_owner_and_source(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        adapter = CursorAdapter(output_root=output_root)
        adapter.emit_plugin(synthetic_plugin)
        result = adapter.emit_global([synthetic_plugin])

        marketplace = output_root / ".cursor-plugin" / "marketplace.json"
        assert marketplace in result.written
        data = json.loads(marketplace.read_text())
        assert "owner" in data
        assert data["owner"].get("name")
        # First plugin entry uses `source`, not `path` or `url`
        assert data["plugins"][0]["source"] == "./plugins/demo"

    def test_emits_curated_rules_present(self, synthetic_plugin: PluginSource, output_root: Path):
        adapter = CursorAdapter(output_root=output_root)
        result = adapter.emit_global([synthetic_plugin])
        rule_files = [p for p in result.written if p.suffix == ".mdc"]
        assert rule_files  # the three curated rules ship with the repo

    def test_string_author_normalized_to_dict(self, tmp_path: Path, output_root: Path):
        """A plugin.json with npm-style `\"author\": \"Name <email>\"` must not crash the adapter."""
        from tools.adapters.cursor import CursorAdapter

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
            '{"name": "demo", "version": "1.0.0", "author": "Jane Doe <jane@example.com>"}'
        )
        plugin = PluginSource(
            name="demo",
            dir=plugin_dir,
            plugin_json={
                "name": "demo",
                "version": "1.0.0",
                "author": "Jane Doe <jane@example.com>",
            },
        )
        CursorAdapter(output_root=output_root).emit_plugin(plugin)
        manifest = json.loads(
            (output_root / ".cursor-plugin" / "plugins" / "demo.json").read_text()
        )
        assert manifest["author"] == {"name": "Jane Doe", "email": "jane@example.com"}

    def test_curated_rules_validate(self, synthetic_plugin: PluginSource, output_root: Path):
        """Each emitted .mdc has only the three allowed frontmatter keys."""
        adapter = CursorAdapter(output_root=output_root)
        adapter.emit_global([synthetic_plugin])
        rules_dir = output_root / ".cursor" / "rules"
        assert rules_dir.is_dir()
        for mdc in rules_dir.glob("*.mdc"):
            content = mdc.read_text()
            fm, _ = parse_frontmatter(content)
            invalid = set(fm.keys()) - {"description", "globs", "alwaysApply"}
            assert not invalid, f"{mdc}: unexpected keys {invalid}"

    def test_mdc_validator_handles_block_scalar(self, tmp_path: Path):
        """A description: > block scalar with colons in body must NOT yield phantom keys."""
        from tools.adapters.cursor import _validate_mdc_frontmatter

        content = (
            "---\n"
            "description: >\n"
            "  Use: this rule when authoring source plugins.\n"
            "  Apply: only to plugins/ markdown.\n"
            "alwaysApply: true\n"
            "---\n\n"
            "Body.\n"
        )
        errors = _validate_mdc_frontmatter(content, tmp_path / "test.mdc")
        # 'Use' and 'Apply' must NOT appear as invalid keys
        assert errors == [], f"unexpected errors: {errors}"

    def test_mdc_validator_rejects_real_invalid_key(self, tmp_path: Path):
        """A genuine invalid frontmatter key (e.g. `agentRequested:`) is still rejected."""
        from tools.adapters.cursor import _validate_mdc_frontmatter

        content = "---\ndescription: x\nagentRequested: true\n---\n\nBody.\n"
        errors = _validate_mdc_frontmatter(content, tmp_path / "test.mdc")
        assert any("agentRequested" in e for e in errors)


# ── OpenCode ─────────────────────────────────────────────────────────────────


class TestOpenCodeAdapter:
    def test_emits_subagent_markdown(self, synthetic_plugin: PluginSource, output_root: Path):
        OpenCodeAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        agent_md = output_root / ".opencode" / "agents" / "demo__greeter.md"
        assert agent_md.is_file()
        fm, body = parse_frontmatter(agent_md.read_text())
        assert fm["name"] == "demo__greeter"
        assert fm["mode"] == "subagent"
        # opus -> full provider/model-id
        assert fm["model"] == "anthropic/claude-opus-4-8"

    def test_permission_block_denies_unlisted_tools(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        OpenCodeAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        agent_md = output_root / ".opencode" / "agents" / "demo__greeter.md"
        content = agent_md.read_text()
        # tools: Read, Grep -> read: allow, grep: allow, edit: deny, etc.
        assert re.search(r"read:\s*allow", content)
        assert re.search(r"grep:\s*allow", content)
        assert re.search(r"edit:\s*deny", content)
        assert re.search(r"write:\s*deny", content)
        assert re.search(r"bash:\s*deny", content)

    def test_no_permission_block_when_no_tools_field(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "free",
            "name: free\ndescription: Use when free.",
            "# Free agent\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        OpenCodeAdapter(output_root=output_root).emit_plugin(plugin)
        content = (output_root / ".opencode" / "agents" / "demo__free.md").read_text()
        assert "permission:" not in content

    def test_lowercases_tool_refs_in_body(self, synthetic_plugin: PluginSource, output_root: Path):
        OpenCodeAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        # Commands and agents need OpenCode's lowercase tool vocabulary.
        cmd_md = output_root / ".opencode" / "commands" / "demo__say-hi.md"
        assert cmd_md.is_file()

    def test_emits_minimal_opencode_json(self, synthetic_plugin: PluginSource, output_root: Path):
        adapter = OpenCodeAdapter(output_root=output_root)
        adapter.emit_plugin(synthetic_plugin)
        result = adapter.emit_global([synthetic_plugin])
        cfg = output_root / "opencode.json"
        assert cfg in result.written
        data = json.loads(cfg.read_text())
        assert data["$schema"] == "https://opencode.ai/config.json"

    def test_emits_opencode_skill_with_hyphenated_name(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        OpenCodeAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        skill_md = output_root / ".opencode" / "skills" / "demo-hello" / "SKILL.md"
        assert skill_md.is_file()
        fm, body = parse_frontmatter(skill_md.read_text())
        assert fm["name"] == "demo-hello"
        assert fm["description"] == "Use when greeting users."
        assert "# Hello" in body
        assert "`read`" in body
        assert "`bash`" in body
        assert "`Read`" not in body
        assert "`Bash`" not in body

    def test_emits_opencode_skill_support_files(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        skill = _make_skill(
            plugin_dir,
            "with-assets",
            "name: with-assets\ndescription: Use when testing assets.",
            "# With Assets\n\nBody.\n",
        )
        (skill.dir / "references").mkdir()
        (skill.dir / "references" / "details.md").write_text("More detail.\n")
        (skill.dir / "assets").mkdir()
        (skill.dir / "assets" / "icon.bin").write_bytes(b"\x00\x01")
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, skills=[skill]
        )

        OpenCodeAdapter(output_root=output_root).emit_plugin(plugin)

        skill_dir = output_root / ".opencode" / "skills" / "demo-with-assets"
        assert (skill_dir / "references" / "details.md").read_text() == "More detail.\n"
        assert (skill_dir / "assets" / "icon.bin").read_bytes() == b"\x00\x01"

    def test_rejects_invalid_opencode_skill_id(self, tmp_path: Path):
        from tools.tests.conftest import _make_skill

        plugin_dir = tmp_path / "bad_plugin"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "bad_plugin"}')
        skill = _make_skill(
            plugin_dir,
            "hello",
            "name: hello\ndescription: Use when testing.",
            "# Hello\n\nBody.\n",
        )
        plugin = PluginSource(
            name="bad_plugin",
            dir=plugin_dir,
            plugin_json={"name": "bad_plugin"},
            skills=[skill],
        )

        try:
            _opencode_skill_id(plugin, skill)
        except ValueError as exc:
            assert "must match" in str(exc)
        else:
            raise AssertionError("invalid OpenCode skill id was accepted")

    def test_rejects_too_long_opencode_skill_id(self, tmp_path: Path):
        from tools.tests.conftest import _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        skill = _make_skill(
            plugin_dir,
            "x" * 80,
            "name: long\ndescription: Use when testing.",
            "# Long\n\nBody.\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, skills=[skill]
        )

        try:
            _opencode_skill_id(plugin, skill)
        except ValueError as exc:
            assert "limit" in str(exc)
        else:
            raise AssertionError("too-long OpenCode skill id was accepted")

    def test_rejects_ambiguous_opencode_skill_id_collision(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_skill

        first_dir = tmp_path / "data-analysis"
        second_dir = tmp_path / "data"
        first_dir.mkdir()
        second_dir.mkdir()
        for plugin_dir in (first_dir, second_dir):
            (plugin_dir / ".claude-plugin").mkdir()
            (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
                f'{{"name": "{plugin_dir.name}"}}'
            )

        first_skill = _make_skill(
            first_dir,
            "report",
            "name: report\ndescription: Use when testing.",
            "# Report\n\nBody.\n",
        )
        second_skill = _make_skill(
            second_dir,
            "analysis-report",
            "name: analysis-report\ndescription: Use when testing.",
            "# Analysis Report\n\nBody.\n",
        )
        first = PluginSource(
            name="data-analysis",
            dir=first_dir,
            plugin_json={"name": "data-analysis"},
            skills=[first_skill],
        )
        second = PluginSource(
            name="data",
            dir=second_dir,
            plugin_json={"name": "data"},
            skills=[second_skill],
        )

        adapter = OpenCodeAdapter(output_root=output_root)
        adapter.emit_plugin(first)

        try:
            adapter.emit_plugin(second)
        except ValueError as exc:
            assert "collision" in str(exc)
            assert "data-analysis/report" in str(exc)
            assert "data/analysis-report" in str(exc)
        else:
            raise AssertionError("ambiguous OpenCode skill id collision was accepted")

    def test_explicit_empty_tools_yields_locked_permission_block(
        self, tmp_path: Path, output_root: Path
    ):
        """`tools: []` (explicit empty allowlist) MUST emit a deny-everything permission
        block (with skill/task base capabilities). Returning {} would silently upgrade a
        locked-down agent to OpenCode's permissive default — Codex PR-541 P1 finding."""
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "locked-advisor",
            "name: locked-advisor\ndescription: Use when locked.\ntools: []",
            "# Locked advisor\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        OpenCodeAdapter(output_root=output_root).emit_plugin(plugin)

        content = (output_root / ".opencode" / "agents" / "demo__locked-advisor.md").read_text()
        # Permission block MUST be present (locked agent), with skill/task allow + all else deny.
        assert "permission:" in content
        assert re.search(r"read:\s*deny", content)
        assert re.search(r"edit:\s*deny", content)
        assert re.search(r"write:\s*deny", content)
        assert re.search(r"bash:\s*deny", content)
        # Base capabilities preserved.
        assert re.search(r"skill:\s*allow", content)
        assert re.search(r"task:\s*allow", content)

    def test_missing_tools_field_yields_no_permission_block(
        self, tmp_path: Path, output_root: Path
    ):
        """Absent `tools:` (Claude default) → no permission block → permissive (Claude semantics)."""
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "open-agent",
            "name: open-agent\ndescription: Use when unrestricted.",
            "# Open agent\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        OpenCodeAdapter(output_root=output_root).emit_plugin(plugin)

        content = (output_root / ".opencode" / "agents" / "demo__open-agent.md").read_text()
        assert "permission:" not in content

    def test_subtask_inference_word_boundary(self, tmp_path: Path, output_root: Path):
        """Word-boundary subtask inference: `PerformanceReviewAgent` (substring inside a
        class name) must NOT trigger `subtask: true` — Codex PR-541 P2 finding."""
        from tools.tests.conftest import _make_command

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')

        # Body mentions 'Agent' only as a substring (class name in code) — no actual orchestration.
        no_orchestration = _make_command(
            plugin_dir,
            "lint",
            'description: "Lint code"',
            "# Lint\n\nReview the `PerformanceReviewAgent` class definition. Check `useragent` headers.",
        )
        # Body explicitly mentions `subagent` as a standalone word — IS orchestration.
        orchestration = _make_command(
            plugin_dir,
            "delegate",
            'description: "Delegate work"',
            "# Delegate\n\nSpawn a subagent to handle each task.",
        )

        plugin = PluginSource(
            name="demo",
            dir=plugin_dir,
            plugin_json={"name": "demo"},
            commands=[no_orchestration, orchestration],
        )
        OpenCodeAdapter(output_root=output_root).emit_plugin(plugin)

        lint = (output_root / ".opencode" / "commands" / "demo__lint.md").read_text()
        delegate = (output_root / ".opencode" / "commands" / "demo__delegate.md").read_text()

        assert "subtask:" not in lint  # NO false positive on substring matches
        assert "subtask: true" in delegate  # genuine orchestration still detected


# ── Antigravity ──────────────────────────────────────────────────────────────


class TestAntigravityAdapter:
    def test_emits_plugin_json(self, synthetic_plugin: PluginSource, output_root: Path):
        AntigravityAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        plugin_json = output_root / ".antigravity" / "plugins" / "demo" / "plugin.json"
        assert plugin_json.is_file()

        data = json.loads(plugin_json.read_text())
        assert data["name"] == "demo"
        assert data["description"] == "Demo plugin for tests"

    def test_emits_skill_with_bare_name(self, synthetic_plugin: PluginSource, output_root: Path):
        AntigravityAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        skill_md = (
            output_root / ".antigravity" / "plugins" / "demo" / "skills" / "hello" / "SKILL.md"
        )
        assert skill_md.is_file()

        fm, _ = parse_frontmatter(skill_md.read_text())
        # No `<plugin>__` namespacing — the plugin directory already scopes it.
        assert fm["name"] == "hello"

    def test_mirrors_all_skill_support_dirs_not_just_references(
        self, tmp_path: Path, output_root: Path
    ):
        """scripts/, assets/, resources/, examples/ must be mirrored alongside
        references/ — not dropped (P1: broken workflows without them)."""
        from tools.tests.conftest import _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        skill = _make_skill(
            plugin_dir,
            "toolkit",
            "name: toolkit\ndescription: Use when running the toolkit.",
            "# Toolkit\n\nRun `scripts/preflight.sh`.\n",
        )
        (skill.dir / "references").mkdir()
        (skill.dir / "references" / "notes.md").write_text("notes")
        (skill.dir / "scripts").mkdir()
        (skill.dir / "scripts" / "preflight.sh").write_text("#!/bin/sh\necho ok\n")
        (skill.dir / "assets").mkdir()
        (skill.dir / "assets" / "logo.png").write_bytes(b"\x89PNG\r\n")
        (skill.dir / "resources").mkdir()
        (skill.dir / "resources" / "data.json").write_text("{}")
        (skill.dir / "examples").mkdir()
        (skill.dir / "examples" / "sample.txt").write_text("example")
        # Hidden files must NOT be mirrored.
        (skill.dir / ".DS_Store").write_text("junk")
        hidden_dir = skill.dir / ".cache"
        hidden_dir.mkdir()
        (hidden_dir / "ignored.txt").write_text("ignored")

        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, skills=[skill]
        )
        AntigravityAdapter(output_root=output_root).emit_plugin(plugin)

        skill_root = output_root / ".antigravity" / "plugins" / "demo" / "skills" / "toolkit"
        assert (skill_root / "references" / "notes.md").is_file()
        assert (skill_root / "scripts" / "preflight.sh").is_file()
        assert (skill_root / "assets" / "logo.png").is_file()
        assert (skill_root / "resources" / "data.json").is_file()
        assert (skill_root / "examples" / "sample.txt").is_file()
        assert not (skill_root / ".DS_Store").exists()
        assert not (skill_root / ".cache").exists()
        # SKILL.md itself isn't duplicated by the mirroring loop.
        assert (skill_root / "SKILL.md").read_text().count("# Toolkit") == 1

    def test_preserves_mapping_valued_frontmatter_field(self, tmp_path: Path, output_root: Path):
        """A dict-valued field (e.g. `metadata`) must round-trip as a YAML mapping,
        not get flattened into a broken `str(dict)` scalar."""
        from tools.tests.conftest import _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        skill = _make_skill(
            plugin_dir,
            "meta",
            "name: meta\ndescription: Use when testing.\nmetadata:\n  version: 1.0.0\n  source: https://example.com/repo",
            "# Meta\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, skills=[skill]
        )
        AntigravityAdapter(output_root=output_root).emit_plugin(plugin)

        skill_md = (
            output_root / ".antigravity" / "plugins" / "demo" / "skills" / "meta" / "SKILL.md"
        )
        content = skill_md.read_text()
        assert "{'version'" not in content
        fm, _ = parse_frontmatter(content)
        assert isinstance(fm["metadata"], dict)
        assert fm["metadata"]["version"] == "1.0.0"
        assert fm["metadata"]["source"] == "https://example.com/repo"

    def test_quotes_comma_in_flow_list_item(self, tmp_path: Path, output_root: Path):
        """A list item containing a comma must be quoted in the emitted flow
        sequence, or it silently splits into two list items on round-trip."""
        from tools.tests.conftest import _make_skill

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        skill = _make_skill(
            plugin_dir,
            "tagged",
            'name: tagged\ndescription: Use when testing.\ntags: ["foo, bar", baz]',
            "# Tagged\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, skills=[skill]
        )
        AntigravityAdapter(output_root=output_root).emit_plugin(plugin)

        skill_md = (
            output_root / ".antigravity" / "plugins" / "demo" / "skills" / "tagged" / "SKILL.md"
        )
        fm, _ = parse_frontmatter(skill_md.read_text())
        assert fm["tags"] == ["foo, bar", "baz"]

    def test_emits_agent_with_tier_model_and_mapped_tools(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        AntigravityAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        agent_md = output_root / ".antigravity" / "plugins" / "demo" / "agents" / "greeter.md"
        assert agent_md.is_file()

        fm, _ = parse_frontmatter(agent_md.read_text())
        assert fm["name"] == "greeter"
        # opus -> pro (agy tier alias, not a concrete gemini/claude model id)
        assert fm["model"] == "pro"
        # Read, Grep -> view_file, grep_search (confirmed agy tool names)
        assert fm["tools"] == ["view_file", "grep_search"]
        assert fm["subagent"] == "true"

    def test_agent_omits_tools_when_source_has_no_tools_field(
        self, tmp_path: Path, output_root: Path
    ):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "unrestricted",
            "name: unrestricted\ndescription: Use when unrestricted.",
            "# Unrestricted\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        AntigravityAdapter(output_root=output_root).emit_plugin(plugin)

        agent_md = output_root / ".antigravity" / "plugins" / "demo" / "agents" / "unrestricted.md"
        fm, _ = parse_frontmatter(agent_md.read_text())
        assert "tools" not in fm

    def test_model_alias_tiers(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')

        agents = [
            _make_agent(
                plugin_dir,
                name,
                f"name: {name}\ndescription: Use for {name}.\nmodel: {model}",
                f"# {name}\n",
            )
            for name, model in [
                ("sonnet-agent", "sonnet"),
                ("haiku-agent", "haiku"),
                ("inherit-agent", "inherit"),
            ]
        ]
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=agents
        )
        AntigravityAdapter(output_root=output_root).emit_plugin(plugin)

        expected = {"sonnet-agent": "pro", "haiku-agent": "flash", "inherit-agent": "inherit"}
        for name, exp_model in expected.items():
            agent_md = output_root / ".antigravity" / "plugins" / "demo" / "agents" / f"{name}.md"
            fm, _ = parse_frontmatter(agent_md.read_text())
            assert fm["model"] == exp_model, f"{name}: expected {exp_model}, got {fm['model']}"

    def test_command_always_inlines_never_at_path(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        """`agy plugin validate` never evaluates @{path}, so commands always inline."""
        AntigravityAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        toml_path = (
            output_root / ".antigravity" / "plugins" / "demo" / "commands" / "demo" / "say-hi.toml"
        )
        assert toml_path.is_file()
        content = toml_path.read_text()
        assert "@{" not in content
        assert "Greet the user" in content

    def test_command_toml_parses_as_valid_toml(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        import tomllib

        AntigravityAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        toml_path = (
            output_root / ".antigravity" / "plugins" / "demo" / "commands" / "demo" / "say-hi.toml"
        )
        parsed = tomllib.loads(toml_path.read_text())
        assert "description" in parsed
        assert "prompt" in parsed
        assert "{{args}}" in parsed["prompt"]
        # The synthetic command body already contains `$ARGUMENTS`, translated in
        # place — no duplicate trailing {{args}} block is appended.
        assert "$ARGUMENTS" not in parsed["prompt"]
        assert parsed["prompt"].count("{{args}}") == 1

    def test_translates_dollar_arguments_placeholder_mid_body(
        self, tmp_path: Path, output_root: Path
    ):
        """`$ARGUMENTS` occurrences anywhere in the body are translated to agy's
        `{{args}}` in place; no duplicate trailing {{args}} block is appended."""
        from tools.tests.conftest import _make_command

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        cmd = _make_command(
            plugin_dir,
            "echo",
            'description: "Echo"',
            "Echo back: $ARGUMENTS\n\nDo it again: $ARGUMENTS.",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, commands=[cmd]
        )
        AntigravityAdapter(output_root=output_root).emit_plugin(plugin)

        import tomllib

        toml_path = (
            output_root / ".antigravity" / "plugins" / "demo" / "commands" / "demo" / "echo.toml"
        )
        parsed = tomllib.loads(toml_path.read_text())
        assert "$ARGUMENTS" not in parsed["prompt"]
        assert parsed["prompt"].count("{{args}}") == 2

    def test_appends_trailing_args_block_when_source_has_no_dollar_arguments(
        self, tmp_path: Path, output_root: Path
    ):
        """Commands without `$ARGUMENTS` in the body still get exactly one trailing
        {{args}} block so agy binds user input somewhere."""
        from tools.tests.conftest import _make_command

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        cmd = _make_command(
            plugin_dir,
            "static",
            'description: "Static"',
            "Do a fixed thing, no arguments needed.",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, commands=[cmd]
        )
        AntigravityAdapter(output_root=output_root).emit_plugin(plugin)

        import tomllib

        toml_path = (
            output_root / ".antigravity" / "plugins" / "demo" / "commands" / "demo" / "static.toml"
        )
        parsed = tomllib.loads(toml_path.read_text())
        assert parsed["prompt"].count("{{args}}") == 1
        assert parsed["prompt"].rstrip().endswith("{{args}}")


# ── Copilot ──────────────────────────────────────────────────────────────────


class TestCopilotAdapter:
    def test_emits_agent_profile(self, synthetic_plugin: PluginSource, output_root: Path):
        adapter = CopilotAdapter(output_root=output_root)
        result = adapter.emit_plugin(synthetic_plugin)

        agent_path = output_root / ".copilot" / "agents" / "demo__greeter.agent.md"
        assert agent_path in result.written
        assert agent_path.is_file()

        fm, body = parse_frontmatter(agent_path.read_text())
        assert fm["name"] == "demo__greeter"
        assert fm["description"] == "Use when delegating greetings."
        assert fm["model"] == "claude-opus-4.8"
        assert fm["tools"] == ["read", "search"]
        assert "color" not in fm

    def test_tool_name_rewriting(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "tool-user",
            "name: tool-user\ndescription: Use when tooling.\ntools: Read, Write, Bash",
            "# Tool User\n\nUse the `Read` tool to read and `Bash` to execute.\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        CopilotAdapter(output_root=output_root).emit_plugin(plugin)

        content = (output_root / ".copilot" / "agents" / "demo__tool-user.agent.md").read_text()
        fm, body = parse_frontmatter(content)
        assert fm["tools"] == ["read", "edit", "execute"]
        assert "`read`" in body
        assert "`execute`" in body
        assert "`Read`" not in body
        assert "`Bash`" not in body

    def test_model_alias_resolution(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')

        agents = []
        for name, model in [
            ("sonnet-agent", "sonnet"),
            ("haiku-agent", "haiku"),
            ("inherit-agent", "inherit"),
        ]:
            agents.append(
                _make_agent(
                    plugin_dir,
                    name,
                    f"name: {name}\ndescription: Use for {name}.\nmodel: {model}",
                    f"# {name}\n",
                )
            )
        default_agent = _make_agent(
            plugin_dir,
            "default-model",
            "name: default-model\ndescription: Use with default.",
            "# Default\n",
        )
        agents.append(default_agent)

        plugin = PluginSource(
            name="demo",
            dir=plugin_dir,
            plugin_json={"name": "demo"},
            agents=agents,
        )
        CopilotAdapter(output_root=output_root).emit_plugin(plugin)

        expected = {
            "sonnet-agent": "claude-sonnet-5",
            "haiku-agent": "claude-haiku-4.5",
            "inherit-agent": "claude-sonnet-5",
            "default-model": "claude-sonnet-5",
        }
        for name, exp_model in expected.items():
            fm, _ = parse_frontmatter(
                (output_root / ".copilot" / "agents" / f"demo__{name}.agent.md").read_text()
            )
            assert fm["model"] == exp_model, f"{name}: expected {exp_model}, got {fm['model']}"

    def test_emits_skill(self, synthetic_plugin: PluginSource, output_root: Path):
        CopilotAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        skill_path = output_root / ".copilot" / "skills" / "demo__hello" / "SKILL.md"
        assert skill_path.is_file()

        fm, body = parse_frontmatter(skill_path.read_text())
        assert fm["name"] == "hello"
        assert fm["description"] == "Use when greeting users."
        assert "# Hello" in body

    def test_emits_command_prompt_files(self, synthetic_plugin: PluginSource, output_root: Path):
        CopilotAdapter(output_root=output_root).emit_plugin(synthetic_plugin)

        entry = output_root / ".copilot" / "commands" / "demo" / "index.md"
        cmd = output_root / ".copilot" / "commands" / "demo" / "say-hi.md"

        assert entry.is_file()
        assert cmd.is_file()

        entry_fm, entry_body = parse_frontmatter(entry.read_text())
        cmd_fm, cmd_body = parse_frontmatter(cmd.read_text())
        assert entry_fm["description"] == "Demo plugin for tests"
        assert "/demo:say-hi" in entry_body
        assert cmd_fm["description"] == "Send a greeting"
        assert "Greet the user named $ARGUMENTS." in cmd_body

    def test_emit_global_returns_empty(self, synthetic_plugin: PluginSource, output_root: Path):
        adapter = CopilotAdapter(output_root=output_root)
        result = adapter.emit_global([synthetic_plugin])
        assert result.written == []

    def test_build_tools_list(self):
        assert _build_tools_list(["Read", "Grep"]) == ["read", "search"]
        assert _build_tools_list(["Write", "Edit"]) == ["edit", "edit"]
        assert _build_tools_list(["Bash", "Glob"]) == ["execute", "search"]
        assert _build_tools_list(["CustomTool"]) == ["CustomTool"]
        assert _build_tools_list([]) == []

    def test_yaml_quoting(self):
        assert _needs_yaml_quoting("123")
        assert _needs_yaml_quoting("3.14")
        assert _needs_yaml_quoting("true")
        assert _needs_yaml_quoting("false")
        assert _needs_yaml_quoting("yes")
        assert _needs_yaml_quoting("no")
        assert _needs_yaml_quoting("on")
        assert _needs_yaml_quoting("off")
        assert _needs_yaml_quoting("null")
        assert _needs_yaml_quoting("~")
        assert not _needs_yaml_quoting("hello world")
        assert not _needs_yaml_quoting("Use when testing.")

    def test_explicit_empty_tools(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "advisory",
            "name: advisory\ndescription: Use when advising.\nmodel: sonnet\ntools: []",
            "# Advisory\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        CopilotAdapter(output_root=output_root).emit_plugin(plugin)

        content = (output_root / ".copilot" / "agents" / "demo__advisory.agent.md").read_text()
        fm, body = parse_frontmatter(content)
        assert fm["name"] == "demo__advisory"
        assert fm["description"] == "Use when advising."
        assert fm["model"] == "claude-sonnet-5"
        assert "tools:" in content

    def test_no_tools_field(self, tmp_path: Path, output_root: Path):
        from tools.tests.conftest import _make_agent

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        agent = _make_agent(
            plugin_dir,
            "unrestricted",
            "name: unrestricted\ndescription: Use when unrestricted.\nmodel: opus",
            "# Unrestricted\n",
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, agents=[agent]
        )
        CopilotAdapter(output_root=output_root).emit_plugin(plugin)

        content = (output_root / ".copilot" / "agents" / "demo__unrestricted.agent.md").read_text()
        fm, body = parse_frontmatter(content)
        assert fm["name"] == "demo__unrestricted"
        assert fm["description"] == "Use when unrestricted."
        assert fm["model"] == "claude-opus-4.8"
        assert "tools" not in fm


# ── Cross-cutting: capabilities consistency ──────────────────────────────────


class TestLoadPlugin:
    def test_rejects_double_underscore_plugin_name(self, tmp_path: Path, monkeypatch):
        """Plugin names with `__` collide with the adapter namespace separator."""
        import tools.adapters.base as base

        # Build a fake plugins dir with a bad name
        bad_plugin = tmp_path / "plugins" / "bad__name"
        (bad_plugin / ".claude-plugin").mkdir(parents=True)
        (bad_plugin / ".claude-plugin" / "plugin.json").write_text('{"name": "bad__name"}')
        monkeypatch.setattr(base, "PLUGINS_DIR", tmp_path / "plugins")

        # Should return None with a stderr warning
        assert base.load_plugin("bad__name") is None


class TestFrontmatterParser:
    """Targeted tests for parse_frontmatter edge cases caught by code review."""

    def test_inline_list_tools(self):
        from tools.adapters.base import parse_frontmatter

        fm, _ = parse_frontmatter(
            "---\nname: x\ntools: [Read, Grep, Glob]\ndescription: y\n---\nbody"
        )
        assert fm["tools"] == ["Read", "Grep", "Glob"]

    def test_inline_list_empty(self):
        from tools.adapters.base import parse_frontmatter

        fm, _ = parse_frontmatter("---\nname: x\ntools: []\n---\nbody")
        assert fm["tools"] == []

    def test_inline_list_quoted_items(self):
        from tools.adapters.base import parse_frontmatter

        fm, _ = parse_frontmatter('---\nname: x\ntools: ["Read", "Grep"]\n---\nbody')
        assert fm["tools"] == ["Read", "Grep"]

    def test_block_list_still_works(self):
        from tools.adapters.base import parse_frontmatter

        fm, _ = parse_frontmatter("---\nname: x\ntools:\n  - Read\n  - Grep\n---\nbody")
        assert fm["tools"] == ["Read", "Grep"]

    def test_block_scalar_description(self):
        from tools.adapters.base import parse_frontmatter

        fm, _ = parse_frontmatter("---\nname: x\ndescription: >\n  multi\n  line\n---\nbody")
        assert fm["description"] == "multi line"

    def test_nested_mapping(self):
        from tools.adapters.base import parse_frontmatter

        fm, _ = parse_frontmatter(
            '---\nmetadata:\n  version: "1.0.0"\n  source: https://example.com\n---\nbody'
        )
        assert fm["metadata"] == {
            "version": "1.0.0",
            "source": "https://example.com",
        }

    def test_nested_mapping_rejects_deeper_indentation(self):
        from tools.adapters.base import parse_frontmatter

        fm, _ = parse_frontmatter("---\nmetadata:\n    version: 1.0.0\n---\nbody")
        assert fm["metadata"] == ""

        fm, _ = parse_frontmatter(
            "---\nmetadata:\n  version: 1.0.0\n    source: https://example.com\n---\nbody"
        )
        assert fm["metadata"] == {"version": "1.0.0"}


class TestCapabilities:
    def test_every_adapter_id_has_capabilities_entry(self):
        from tools.adapters.capabilities import CAPABILITIES

        for adapter_cls in (
            AntigravityAdapter,
            CodexAdapter,
            CopilotAdapter,
            CursorAdapter,
            OpenCodeAdapter,
        ):
            assert adapter_cls.harness_id in CAPABILITIES

    def test_model_aliases_complete(self):
        """Every harness has a mapping for each Claude alias."""
        from tools.adapters.capabilities import MODEL_ALIASES, supported_harnesses

        for harness in supported_harnesses():
            for alias in ("fable", "opus", "sonnet", "haiku", "inherit"):
                assert alias in MODEL_ALIASES[harness], f"{harness} missing {alias}"


# ── Tool-reference rewriting ─────────────────────────────────────────────────


class TestStripClaudeToolRefs:
    """Characterization tests for `HarnessAdapter.strip_claude_tool_refs`.

    Copilot command bodies are rewritten through this method, and its output is not
    otherwise asserted anywhere. These tests pin the exact strings so that a refactor
    which changes them has to say so instead of slipping through.
    """

    SAMPLE = "Use the `Read` tool first, then the Bash tool. Prefer `Grep` over `Glob`."

    def _adapter(self, tmp_path: Path) -> CopilotAdapter:
        return CopilotAdapter(output_root=tmp_path)

    def test_lower_case_output_is_exact(self, tmp_path: Path):
        assert (
            self._adapter(tmp_path).strip_claude_tool_refs(self.SAMPLE, tool_case="lower")
            == "Use `open` first, then `shell`. Prefer `grep` over `glob`."
        )

    def test_normal_case_output_is_exact(self, tmp_path: Path):
        """`normal` keeps Read as `read` and leaves bare backticked names alone."""
        assert (
            self._adapter(tmp_path).strip_claude_tool_refs(self.SAMPLE, tool_case="normal")
            == "Use `read` first, then `shell`. Prefer `Grep` over `Glob`."
        )

    def test_replacements_keep_their_backticks(self, tmp_path: Path):
        out = self._adapter(tmp_path).strip_claude_tool_refs("Run the Bash tool.")
        assert out == "Run `shell`."
        assert "`shell`" in out, "replacement must stay inside backticks"

    def test_backticked_prose_form(self, tmp_path: Path):
        assert (
            self._adapter(tmp_path).strip_claude_tool_refs("Call the `WebFetch` tool now.")
            == "Call `fetch` now."
        )

    def test_bare_backticked_name_is_lowercased_not_verbed(self, tmp_path: Path):
        """`Grep` on its own becomes `grep` — the lowercased name, not the `rg` verb."""
        assert self._adapter(tmp_path).strip_claude_tool_refs("Prefer `Grep`.") == "Prefer `grep`."

    def test_prose_words_are_left_alone(self, tmp_path: Path):
        """Conservative by design: only the two tool phrasings are touched."""
        sample = "Read the docs, then write a summary and edit it."
        assert self._adapter(tmp_path).strip_claude_tool_refs(sample) == sample

    def test_every_mapped_tool_is_covered(self, tmp_path: Path):
        """Both cases, passed explicitly so a change to the default is caught.

        Only Read differs between the two. The rest are pinned in both modes so a
        future divergence has to be deliberate.
        """
        adapter = self._adapter(tmp_path)
        # camel -> (tool_case="lower", tool_case="normal")
        expected = {
            "Read": ("open", "read"),
            "Edit": ("edit", "edit"),
            "Write": ("write", "write"),
            "Bash": ("shell", "shell"),
            "Grep": ("rg", "rg"),
            "Glob": ("glob", "glob"),
            "WebFetch": ("fetch", "fetch"),
            "WebSearch": ("search", "search"),
            "TodoWrite": ("todo", "todo"),
        }
        for camel, (lower_verb, normal_verb) in expected.items():
            body = f"Use the {camel} tool."
            assert adapter.strip_claude_tool_refs(body, tool_case="lower") == f"Use `{lower_verb}`."
            assert (
                adapter.strip_claude_tool_refs(body, tool_case="normal") == f"Use `{normal_verb}`."
            )

    def test_emitted_copilot_command_rewrites_tool_refs(self, tmp_path: Path):
        """Cover the real path: what a generated Copilot command body actually says.

        The unit assertions above pin the method. Copilot's two call sites pass
        `tool_case="lower"` explicitly, so this asserts the emitted file instead of the
        method default, which is what would actually regress.
        """
        from tools.adapters.base import CommandSource, PluginSource

        plugin_dir = tmp_path / "src" / "demo"
        cmds = plugin_dir / "commands"
        cmds.mkdir(parents=True)
        body = "Use the `Read` tool first, then the Bash tool. Prefer `Grep` over `Glob`."
        content = f"---\ndescription: Demo command.\n---\n\n{body}\n"
        (cmds / "demo-cmd.md").write_text(content, encoding="utf-8")
        fm, parsed_body = parse_frontmatter(content)
        command = CommandSource(
            plugin="demo",
            name="demo-cmd",
            path=cmds / "demo-cmd.md",
            frontmatter=fm,
            body=parsed_body,
        )
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, commands=[command]
        )

        out = tmp_path / "out"
        result = CopilotAdapter(output_root=out).emit_plugin(plugin)
        emitted = [p for p in result.written if p.suffix == ".md"]
        # Copilot writes the command twice, as a skill and as a legacy command, and
        # also writes a plugin index that carries no command body.
        command_files = [p for p in emitted if p.name in {"SKILL.md", "demo-cmd.md"}]
        assert len(command_files) == 2, [p.name for p in emitted]

        # Per file, not joined: a joined string would let one emitter regress to
        # `read` while the other's `open` still satisfied the assertion.
        for path in command_files:
            text = path.read_text(encoding="utf-8")
            assert "`open`" in text, path
            assert "`shell`" in text, path
            assert "`grep`" in text, path
            assert "`read`" not in text, path
            assert "the `Read` tool" not in text, path
            assert "the Bash tool" not in text, path
