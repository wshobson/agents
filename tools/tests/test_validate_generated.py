"""Tests for tools/validate_generated.py — verify each validator catches its anti-patterns."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from tools.validate_generated import (
    Report,
    validate_antigravity,
    validate_codex,
    validate_copilot,
    validate_cursor,
    validate_opencode,
)


def _patch_worktree(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Temporarily point WORKTREE at tmp_path so validators look there."""
    import tools.validate_generated as vg

    monkeypatch.setattr(vg, "WORKTREE", tmp_path)


# ── Codex ────────────────────────────────────────────────────────────────────


class TestCodexValidator:
    def test_clean_output_no_findings(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        (tmp_path / ".codex" / "agents").mkdir(parents=True)
        (tmp_path / ".codex" / "agents" / "demo.toml").write_text(
            'name = "demo"\ndescription = "Use when testing."\ndeveloper_instructions = "Do work."\n'
        )
        sk = tmp_path / ".codex" / "skills" / "demo"
        sk.mkdir(parents=True)
        (sk / "SKILL.md").write_text(
            "---\nname: demo\ndescription: Use when testing.\n---\n\nBody.\n"
        )
        (tmp_path / "AGENTS.md").write_text("# Map\n" + "\n".join(["line"] * 50))

        report = Report()
        validate_codex(report)
        errors = report.errors()
        assert errors == [], [e.render() for e in errors]

    def test_malformed_toml_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        (tmp_path / ".codex" / "agents").mkdir(parents=True)
        (tmp_path / ".codex" / "agents" / "bad.toml").write_text("not valid = toml = anywhere")

        report = Report()
        validate_codex(report)
        assert any("TOML parse" in f.message for f in report.errors())

    def test_skill_name_mismatch_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        sk = tmp_path / ".codex" / "skills" / "demo"
        sk.mkdir(parents=True)
        (sk / "SKILL.md").write_text(
            "---\nname: WRONG\ndescription: Use when testing.\n---\n\nBody.\n"
        )

        report = Report()
        validate_codex(report)
        assert any("name" in f.message and "directory" in f.message for f in report.errors())

    def test_oversized_skill_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Codex skill exceeding 8 KB injection cap is an ERROR (was warning before round 4)."""
        _patch_worktree(monkeypatch, tmp_path)
        sk = tmp_path / ".codex" / "skills" / "demo"
        sk.mkdir(parents=True)
        (sk / "SKILL.md").write_text(
            "---\nname: demo\ndescription: Use when testing.\n---\n\n" + "x" * 9000
        )

        report = Report()
        validate_codex(report)
        assert any("8192" in f.message for f in report.errors())

    def test_oversized_agents_md_warns(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        (tmp_path / "AGENTS.md").write_text("\n".join(["line"] * 200))
        # Force the directory check to pass (validate_codex returns early if no .codex/)
        (tmp_path / ".codex").mkdir()

        report = Report()
        validate_codex(report)
        assert any(
            "AGENTS.md" in str(f.path) and "cap: 150" in f.message for f in report.warnings()
        )


# ── Cursor ───────────────────────────────────────────────────────────────────


class TestCursorValidator:
    def test_marketplace_missing_owner_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        (tmp_path / ".cursor-plugin").mkdir()
        (tmp_path / ".cursor-plugin" / "marketplace.json").write_text(
            json.dumps({"name": "x", "plugins": []})
        )

        report = Report()
        validate_cursor(report)
        assert any("owner" in f.message for f in report.errors())

    def test_plugin_entry_using_path_instead_of_source_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        (tmp_path / ".cursor-plugin").mkdir()
        (tmp_path / ".cursor-plugin" / "marketplace.json").write_text(
            json.dumps(
                {
                    "name": "x",
                    "owner": {"name": "me"},
                    "plugins": [{"name": "demo", "path": "./plugins/demo"}],
                }
            )
        )

        report = Report()
        validate_cursor(report)
        assert any("source" in f.message for f in report.errors())

    def test_invalid_mdc_keys_error(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        rules = tmp_path / ".cursor" / "rules"
        rules.mkdir(parents=True)
        (rules / "bad.mdc").write_text(
            "---\ndescription: Use when testing.\nagentRequested: true\nmode: auto\n---\n\nBody.\n"
        )
        # Need .cursor-plugin to exist for validator to proceed
        (tmp_path / ".cursor-plugin").mkdir()

        report = Report()
        validate_cursor(report)
        assert any(
            "agentRequested" in f.message or "invalid MDC keys" in f.message
            for f in report.errors()
        )


# ── Copilot ──────────────────────────────────────────────────────────────────


class TestCopilotValidator:
    def test_non_string_description_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".copilot" / "agents"
        agents.mkdir(parents=True)
        (agents / "bad.agent.md").write_text("---\nname: bad\ndescription: [oops]\n---\n\nBody.\n")

        report = Report()
        validate_copilot(report)
        assert any("description" in f.message and "string" in f.message for f in report.errors())

    def test_missing_name_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".copilot" / "agents"
        agents.mkdir(parents=True)
        (agents / "noname.agent.md").write_text(
            "---\ndescription: Use when testing.\n---\n\nBody.\n"
        )

        report = Report()
        validate_copilot(report)
        assert any("name" in f.message for f in report.errors())

    def test_empty_name_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".copilot" / "agents"
        agents.mkdir(parents=True)
        (agents / "emptyname.agent.md").write_text(
            '---\nname: ""\ndescription: Use when testing.\n---\n\nBody.\n'
        )

        report = Report()
        validate_copilot(report)
        assert any("is empty" in f.message for f in report.errors())

    def test_missing_description_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".copilot" / "agents"
        agents.mkdir(parents=True)
        (agents / "nodesc.agent.md").write_text("---\nname: nodesc\n---\n\nBody.\n")

        report = Report()
        validate_copilot(report)
        assert any("description" in f.message for f in report.errors())

    def test_empty_description_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".copilot" / "agents"
        agents.mkdir(parents=True)
        (agents / "emptydesc.agent.md").write_text(
            '---\nname: emptydesc\ndescription: ""\n---\n\nBody.\n'
        )

        report = Report()
        validate_copilot(report)
        assert any("field is empty" in f.message for f in report.errors())

    def test_valid_agent_passes(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".copilot" / "agents"
        agents.mkdir(parents=True)
        (agents / "good.agent.md").write_text(
            "---\nname: good\ndescription: Use when testing.\nmodel: gpt-5\n---\n\nBody.\n"
        )

        report = Report()
        validate_copilot(report)
        assert not report.errors()

    def test_skill_missing_name_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        skill_dir = tmp_path / ".copilot" / "skills" / "test__skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("---\ndescription: Use when testing.\n---\n\nBody.\n")

        report = Report()
        validate_copilot(report)
        assert any("name" in f.message for f in report.errors())

    def test_skill_missing_description_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        skill_dir = tmp_path / ".copilot" / "skills" / "test__skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("---\nname: test__skill\n---\n\nBody.\n")

        report = Report()
        validate_copilot(report)
        assert any("description" in f.message for f in report.errors())


# ── OpenCode ─────────────────────────────────────────────────────────────────


class TestOpenCodeValidator:
    def test_missing_mode_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".opencode" / "agents"
        agents.mkdir(parents=True)
        (agents / "no_mode.md").write_text(
            "---\nname: no_mode\ndescription: Use when testing.\nmodel: anthropic/claude-sonnet-5\n---\n\nBody.\n"
        )

        report = Report()
        validate_opencode(report)
        assert any("mode" in f.message for f in report.errors())

    def test_bare_model_alias_warns(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".opencode" / "agents"
        agents.mkdir(parents=True)
        (agents / "bare.md").write_text(
            "---\nname: bare\ndescription: Use when testing.\nmode: subagent\nmodel: opus\n---\n\nBody.\n"
        )

        report = Report()
        validate_opencode(report)
        assert any("provider-prefixed" in f.message for f in report.warnings())

    def test_unknown_permission_key_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".opencode" / "agents"
        agents.mkdir(parents=True)
        (agents / "bad_perm.md").write_text(
            "---\nname: bad_perm\ndescription: Use when testing.\nmode: subagent\n"
            "model: anthropic/claude-sonnet-5\npermission:\n  fly_drone: allow\n---\n\nBody.\n"
        )

        report = Report()
        validate_opencode(report)
        assert any(
            "unknown permission keys" in f.message and "fly_drone" in f.message
            for f in report.errors()
        )

    def test_nested_permission_key_not_treated_as_top_level(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A nested `permission:` inside `metadata:` must NOT be picked up as the top-level
        permission block."""
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".opencode" / "agents"
        agents.mkdir(parents=True)
        (agents / "nested.md").write_text(
            "---\nname: nested\ndescription: Use when nested.\nmode: subagent\n"
            "model: anthropic/claude-sonnet-5\n"
            "metadata:\n  permission:\n    fly_drone: allow\n"
            "---\n\nBody.\n"
        )

        report = Report()
        validate_opencode(report)
        # The nested permission's `fly_drone` must NOT show up as an invalid top-level key.
        assert not any("fly_drone" in f.message for f in report.errors())

    def test_invalid_permission_value_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        agents = tmp_path / ".opencode" / "agents"
        agents.mkdir(parents=True)
        (agents / "bad_value.md").write_text(
            "---\nname: bad_value\ndescription: Use when testing.\nmode: subagent\n"
            "model: anthropic/claude-sonnet-5\npermission:\n  read: maybe\n---\n\nBody.\n"
        )

        report = Report()
        validate_opencode(report)
        assert any("permission.read" in f.message and "maybe" in f.message for f in report.errors())

    def test_skill_name_mismatch_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        skill = tmp_path / ".opencode" / "skills" / "demo-hello"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: wrong-name\ndescription: Use when testing.\n---\n\nBody.\n"
        )

        report = Report()
        validate_opencode(report)
        assert any("directory" in f.message for f in report.errors())

    def test_invalid_skill_name_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        skill = tmp_path / ".opencode" / "skills" / "demo__hello"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "---\nname: demo__hello\ndescription: Use when testing.\n---\n\nBody.\n"
        )

        report = Report()
        validate_opencode(report)
        assert any("OpenCode-safe" in f.message for f in report.errors())

    def test_empty_skill_description_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        skill = tmp_path / ".opencode" / "skills" / "demo-hello"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: demo-hello\n---\n\nBody.\n")

        report = Report()
        validate_opencode(report)
        assert any("empty description" in f.message for f in report.errors())

    def test_too_long_skill_name_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        name = "x" * 65
        skill = tmp_path / ".opencode" / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Use when testing.\n---\n\nBody.\n"
        )

        report = Report()
        validate_opencode(report)
        assert any("64" in f.message for f in report.errors())


# ── Antigravity ──────────────────────────────────────────────────────────────


def _write_plugin_json(plugin_dir: Path, content: str) -> None:
    plugin_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "plugin.json").write_text(content)


class TestAntigravityValidator:
    def test_missing_plugin_json_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        plugin_dir.mkdir(parents=True)

        report = Report()
        validate_antigravity(report)
        assert any("missing plugin.json" in f.message for f in report.errors())

    def test_plugin_json_parse_error(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, "{not valid json")

        report = Report()
        validate_antigravity(report)
        assert any("JSON parse error" in f.message for f in report.errors())

    def test_plugin_json_missing_name_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, "{}")

        report = Report()
        validate_antigravity(report)
        assert any("missing or empty required `name`" in f.message for f in report.errors())

    def test_plugin_json_unsafe_name_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo plugin!"}')

        report = Report()
        validate_antigravity(report)
        assert any("not agy-safe" in f.message for f in report.errors())

    def test_plugin_json_name_mismatch_dir_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "other-name"}')

        report = Report()
        validate_antigravity(report)
        assert any("!= directory name" in f.message for f in report.errors())

    def test_skill_name_mismatch_dir_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        skill_dir = plugin_dir / "skills" / "hello"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: not-hello\ndescription: Use when testing.\n---\n\nBody.\n"
        )

        report = Report()
        validate_antigravity(report)
        assert any("frontmatter name" in f.message for f in report.errors())

    def test_agent_missing_name_and_description_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        agents_dir = plugin_dir / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "bad.md").write_text("---\nmodel: pro\n---\n\nBody.\n")

        report = Report()
        validate_antigravity(report)
        errors = [f.message for f in report.errors()]
        assert any("name" in m for m in errors)
        assert any("description" in m for m in errors)

    def test_agent_invalid_model_tier_errors(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        agents_dir = plugin_dir / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "bad.md").write_text(
            "---\nname: bad\ndescription: Use when testing.\nmodel: gemini-2.5-pro\n---\n\nBody.\n"
        )

        report = Report()
        validate_antigravity(report)
        assert any("not in" in f.message for f in report.errors())

    @pytest.mark.parametrize("tier", ["inherit", "flash", "pro"])
    def test_agent_valid_model_tiers_pass(
        self, tier: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        agents_dir = plugin_dir / "agents"
        agents_dir.mkdir(parents=True)
        (agents_dir / "good.md").write_text(
            f"---\nname: good\ndescription: Use when testing.\nmodel: {tier}\n---\n\nBody.\n"
        )

        report = Report()
        validate_antigravity(report)
        assert not report.errors()

    def test_command_toml_missing_keys_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        cmds_dir = plugin_dir / "commands" / "demo"
        cmds_dir.mkdir(parents=True)
        (cmds_dir / "incomplete.toml").write_text('description = "Just a desc, no prompt"\n')

        report = Report()
        validate_antigravity(report)
        assert any("missing required `prompt`" in f.message for f in report.errors())

    def test_plugin_json_array_does_not_crash(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A `plugin.json` containing a JSON array (not an object) must be reported
        as a finding, not raise AttributeError from `.get()` on a list."""
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, "[]")

        report = Report()
        validate_antigravity(report)
        assert any("must be a JSON object" in f.message for f in report.errors())

    def test_command_toml_non_string_prompt_does_not_crash(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A `prompt` that TOML-parses to a non-string (e.g. an integer) must be
        reported as a finding, not raise TypeError from `in` on a non-iterable."""
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        cmds_dir = plugin_dir / "commands" / "demo"
        cmds_dir.mkdir(parents=True)
        (cmds_dir / "bad_prompt.toml").write_text('description = "Test"\nprompt = 1\n')

        report = Report()
        validate_antigravity(report)
        assert any("`prompt` field must be a string" in f.message for f in report.errors())

    def test_command_toml_non_string_description_errors(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        """A non-string `description` must be reported, not silently pass."""
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        cmds_dir = plugin_dir / "commands" / "demo"
        cmds_dir.mkdir(parents=True)
        (cmds_dir / "bad_description.toml").write_text(
            'description = 1\nprompt = """Run this.\n\n{{args}}"""\n'
        )

        report = Report()
        validate_antigravity(report)
        assert any("`description` field must be a string" in f.message for f in report.errors())

    def test_command_toml_parse_error(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        cmds_dir = plugin_dir / "commands" / "demo"
        cmds_dir.mkdir(parents=True)
        (cmds_dir / "broken.toml").write_text("not = valid = toml = at = all")

        report = Report()
        validate_antigravity(report)
        assert any("TOML parse error" in f.message for f in report.errors())

    def test_command_prompt_without_args_warns(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo"}')
        cmds_dir = plugin_dir / "commands" / "demo"
        cmds_dir.mkdir(parents=True)
        (cmds_dir / "no_args.toml").write_text('description = "Test"\nprompt = """Run this."""\n')

        report = Report()
        validate_antigravity(report)
        assert any("{{args}}" in f.message for f in report.warnings())

    def test_valid_plugin_passes_with_no_findings(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        _patch_worktree(monkeypatch, tmp_path)
        plugin_dir = tmp_path / ".antigravity" / "plugins" / "demo"
        _write_plugin_json(plugin_dir, '{"name": "demo", "description": "Demo plugin"}')
        (plugin_dir / "skills" / "hello").mkdir(parents=True)
        (plugin_dir / "skills" / "hello" / "SKILL.md").write_text(
            "---\nname: hello\ndescription: Use when greeting.\n---\n\nBody.\n"
        )
        (plugin_dir / "agents").mkdir(parents=True)
        (plugin_dir / "agents" / "greeter.md").write_text(
            "---\nname: greeter\ndescription: Use when delegating.\nmodel: pro\nsubagent: true\n"
            "---\n\nBody.\n"
        )
        cmds_dir = plugin_dir / "commands" / "demo"
        cmds_dir.mkdir(parents=True)
        (cmds_dir / "say-hi.toml").write_text(
            'description = "Say hi"\nprompt = """Greet the user.\n\n{{args}}"""\n'
        )

        report = Report()
        validate_antigravity(report)
        assert not report.errors()
        assert not report.warnings()
