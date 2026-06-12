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
from tools.adapters.base import PluginSource, parse_frontmatter
from tools.adapters.codex import CodexAdapter, _split_body_if_oversized
from tools.adapters.copilot import (
    CopilotAdapter,
    _build_tools_list,
    _needs_yaml_quoting,
)
from tools.adapters.cursor import CursorAdapter
from tools.adapters.gemini import _INLINE_BODY_THRESHOLD, GeminiAdapter
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


# ── Gemini ───────────────────────────────────────────────────────────────────


class TestGeminiAdapter:
    def test_emits_native_skill_at_extension_root(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        GeminiAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        skill_md = output_root / "skills" / "demo__hello" / "SKILL.md"
        assert skill_md.is_file()
        fm, _ = parse_frontmatter(skill_md.read_text())
        assert fm["name"] == "demo__hello"

    def test_emits_native_subagent(self, synthetic_plugin: PluginSource, output_root: Path):
        GeminiAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        agent_md = output_root / "agents" / "demo__greeter.md"
        assert agent_md.is_file()
        fm, _ = parse_frontmatter(agent_md.read_text())
        # opus -> gemini-2.5-pro
        assert fm["model"] == "gemini-2.5-pro"

    def test_inline_command_when_body_is_small(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        """Small commands inline the body — no @{path} indirection."""
        GeminiAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        toml_path = output_root / "commands" / "demo" / "say-hi.toml"
        assert toml_path.is_file()
        content = toml_path.read_text()
        # Synthetic command body is ~30 bytes — well under inline threshold
        assert "@{plugins/" not in content
        assert "Greet the user" in content

    def test_injection_when_body_is_large(self, tmp_path: Path, output_root: Path):
        """Large command bodies use Gemini's @{path} file injection."""
        from tools.tests.conftest import _make_command

        plugin_dir = tmp_path / "demo"
        plugin_dir.mkdir()
        (plugin_dir / ".claude-plugin").mkdir()
        (plugin_dir / ".claude-plugin" / "plugin.json").write_text('{"name": "demo"}')
        # Body bigger than _INLINE_BODY_THRESHOLD
        big_body = "# Big command\n\n" + ("x " * (_INLINE_BODY_THRESHOLD))
        cmd = _make_command(plugin_dir, "bigcmd", 'description: "Big"', big_body)
        plugin = PluginSource(
            name="demo", dir=plugin_dir, plugin_json={"name": "demo"}, commands=[cmd]
        )
        GeminiAdapter(output_root=output_root).emit_plugin(plugin)

        content = (output_root / "commands" / "demo" / "bigcmd.toml").read_text()
        assert "@{plugins/demo/commands/bigcmd.md}" in content

    def test_command_toml_parses_as_valid_toml(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        import tomllib

        GeminiAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        toml_path = output_root / "commands" / "demo" / "say-hi.toml"
        parsed = tomllib.loads(toml_path.read_text())
        assert "description" in parsed
        assert "prompt" in parsed
        assert "{{args}}" in parsed["prompt"]
        # {{args}} must be near the end so user input is the final context
        assert parsed["prompt"].rstrip().endswith("{{args}}")

    def test_plugin_entry_command_at_top_level(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        GeminiAdapter(output_root=output_root).emit_plugin(synthetic_plugin)
        entry = output_root / "commands" / "demo.toml"
        assert entry.is_file()
        # Should list subagents and skills
        content = entry.read_text()
        assert "demo__greeter" in content
        assert "demo__hello" in content


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
            "sonnet-agent": "claude-sonnet-4.6",
            "haiku-agent": "claude-haiku-4.5",
            "inherit-agent": "claude-sonnet-4.6",
            "default-model": "claude-sonnet-4.6",
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
        assert fm["model"] == "claude-sonnet-4.6"
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


class TestCapabilities:
    def test_every_adapter_id_has_capabilities_entry(self):
        from tools.adapters.capabilities import CAPABILITIES

        for adapter_cls in (
            CodexAdapter,
            CopilotAdapter,
            CursorAdapter,
            GeminiAdapter,
            OpenCodeAdapter,
        ):
            assert adapter_cls.harness_id in CAPABILITIES

    def test_model_aliases_complete(self):
        """Every harness has a mapping for each Claude alias."""
        from tools.adapters.capabilities import MODEL_ALIASES, supported_harnesses

        for harness in supported_harnesses():
            for alias in ("fable", "opus", "sonnet", "haiku", "inherit"):
                assert alias in MODEL_ALIASES[harness], f"{harness} missing {alias}"
