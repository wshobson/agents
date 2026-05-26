from pathlib import Path

import pytest

from plugin_eval.parser import ParsedSkill, ParsedAgent, ParsedPlugin, parse_skill, parse_agent, parse_plugin


class TestParseSkill:
    def test_parse_valid_skill(self, sample_skill_dir: Path):
        skill = parse_skill(sample_skill_dir)
        assert skill.name == "test-skill"
        assert "testing plugin-eval" in skill.description
        assert skill.line_count > 0
        assert skill.h2_count >= 2
        assert skill.code_block_count >= 1
        assert skill.has_references is True

    def test_parse_poor_skill(self, poor_skill_dir: Path):
        skill = parse_skill(poor_skill_dir)
        assert skill.name == "poor-skill"
        assert skill.must_never_always_count > 15
        assert skill.has_references is True
        assert len(skill.reference_files) == 1

    def test_missing_skill_md_raises(self, tmp_path: Path):
        empty = tmp_path / "empty-skill"
        empty.mkdir()
        with pytest.raises(FileNotFoundError):
            parse_skill(empty)


class TestParseAgent:
    def test_parse_valid_agent(self, sample_plugin_dir: Path):
        agent_path = sample_plugin_dir / "agents" / "test-agent.md"
        agent = parse_agent(agent_path)
        assert agent.name == "test-agent"
        assert agent.model == "sonnet"
        assert agent.has_tools_restriction is True
        assert agent.has_proactive_trigger is True


class TestParsePlugin:
    def test_parse_valid_plugin(self, sample_plugin_dir: Path):
        plugin = parse_plugin(sample_plugin_dir)
        assert plugin.name == "test-plugin"
        assert len(plugin.skills) == 1
        assert len(plugin.agents) == 1
