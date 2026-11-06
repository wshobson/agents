"""Unit tests for the Qwen Code adapter.

The adapter emits one Qwen extension for every plugin: Qwen installs a single
extension per source URL, so a per-plugin layout would need one URL per plugin.
Names are namespaced per plugin because Qwen reads `agents/` and `skills/` one
level deep, and because Claude tool names do not resolve against Qwen's registry.
"""

from __future__ import annotations

from pathlib import Path

from tools.adapters.base import PluginSource, parse_frontmatter
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model
from tools.adapters.qwen import QwenAdapter, qwen_agent_id, qwen_skill_id

_EXTENSION = Path(".qwen") / "extensions" / "qwen-code-workflows"


class TestQwenAdapter:
    def test_emits_skill_with_namespaced_id(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        adapter = QwenAdapter(output_root=output_root)
        result = adapter.emit_plugin(synthetic_plugin)

        skill_path = output_root / _EXTENSION / "skills" / "demo__hello" / "SKILL.md"
        assert skill_path in result.written
        assert skill_path.is_file()

        fm, _ = parse_frontmatter(skill_path.read_text())
        assert fm["name"] == "demo__hello"
        assert fm["description"]

    def test_agent_name_matches_filename(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        adapter = QwenAdapter(output_root=output_root)
        adapter.emit_plugin(synthetic_plugin)

        agent_path = output_root / _EXTENSION / "agents" / "demo__greeter.md"
        assert agent_path.is_file()

        fm, _ = parse_frontmatter(agent_path.read_text())
        assert fm["name"] == agent_path.stem
        assert fm["description"]

    def test_claude_tool_names_map_to_qwen_canonical(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        adapter = QwenAdapter(output_root=output_root)
        adapter.emit_plugin(synthetic_plugin)

        fm, _ = parse_frontmatter(
            (output_root / _EXTENSION / "agents" / "demo__greeter.md").read_text()
        )
        assert fm["tools"] == ["read_file", "grep_search"]
        assert TOOL_NAME_MAPS["qwen"]["Read"] == "read_file"
        assert TOOL_NAME_MAPS["qwen"]["Bash"] == "run_shell_command"

    def test_color_is_dropped_and_model_inherits(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        adapter = QwenAdapter(output_root=output_root)
        adapter.emit_plugin(synthetic_plugin)

        fm, _ = parse_frontmatter(
            (output_root / _EXTENSION / "agents" / "demo__greeter.md").read_text()
        )
        assert "color" not in fm
        assert "model" not in fm
        assert resolve_model("qwen", "opus") == ("inherit", None)

    def test_command_is_nested_under_the_plugin(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        adapter = QwenAdapter(output_root=output_root)
        adapter.emit_plugin(synthetic_plugin)

        command_path = output_root / _EXTENSION / "commands" / "demo" / "say-hi.md"
        assert command_path.is_file()

        fm, _ = parse_frontmatter(command_path.read_text())
        assert fm["description"] == "Send a greeting"
        assert fm["argument-hint"] == "<name>"

    def test_emit_global_writes_manifest_and_context_index(
        self, synthetic_plugin: PluginSource, output_root: Path
    ):
        adapter = QwenAdapter(output_root=output_root)
        adapter.emit_global([synthetic_plugin])

        manifest_path = output_root / _EXTENSION / "qwen-extension.json"
        assert manifest_path.is_file()
        assert '"name": "qwen-code-workflows"' in manifest_path.read_text()

        context_path = output_root / _EXTENSION / "AGENTS.md"
        assert context_path.is_file()
        # The context file is injected on every request, so it must stay small.
        assert context_path.stat().st_size < 8192

    def test_agent_id_respects_qwen_name_rules(self):
        agent_id = qwen_agent_id("demo", "greeter")
        assert agent_id == "demo__greeter"
        assert len(agent_id) <= 50

        long_id = qwen_agent_id("p" * 40, "a" * 40)
        assert len(long_id) <= 50

        assert qwen_skill_id("demo", "hello") == "demo__hello"
