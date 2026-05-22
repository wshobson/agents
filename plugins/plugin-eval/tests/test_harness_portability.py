"""Tests for the harness_portability layer."""

from pathlib import Path

import pytest

from plugin_eval.layers.harness_portability import (
    detect_agent_findings,
    detect_skill_findings,
    score_agent_portability,
    score_skill_portability,
)
from plugin_eval.parser import parse_agent, parse_skill


def _make_skill(tmp_path: Path, body: str, *, name: str = "test-skill", references: bool = False) -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Use when testing portability.\n---\n\n{body}\n"
    )
    if references:
        (skill_dir / "references").mkdir()
        (skill_dir / "references" / "details.md").write_text("Detail.\n")
    return skill_dir


def _make_agent(tmp_path: Path, frontmatter: str, body: str = "Body.\n") -> Path:
    agent_file = tmp_path / "agent.md"
    agent_file.write_text(f"---\n{frontmatter}\n---\n\n{body}")
    return agent_file


class TestSkillFindings:
    def test_clean_skill_has_no_findings(self, tmp_path: Path):
        skill_dir = _make_skill(tmp_path, "Use action verbs; run a shell command.")
        skill = parse_skill(skill_dir)
        assert detect_skill_findings(skill) == []
        assert score_skill_portability(skill) == 1.0

    def test_skill_over_codex_cap_fires_when_no_references(self, tmp_path: Path):
        skill_dir = _make_skill(tmp_path, "x" * 9000, references=False)
        skill = parse_skill(skill_dir)
        flags = [f.flag for f in detect_skill_findings(skill)]
        assert "SKILL_OVER_CODEX_CAP" in flags

    def test_skill_over_codex_cap_suppressed_when_references_exist(self, tmp_path: Path):
        skill_dir = _make_skill(tmp_path, "x" * 9000, references=True)
        skill = parse_skill(skill_dir)
        flags = [f.flag for f in detect_skill_findings(skill)]
        assert "SKILL_OVER_CODEX_CAP" not in flags

    def test_camel_tool_refs_fire(self, tmp_path: Path):
        # Match a Claude-tool reference in context: "use `Read`", "the `Bash`", or "`Edit` tool"
        skill_dir = _make_skill(
            tmp_path, "Use `Read` to open files. Call `Edit` to modify. The `Bash` tool runs commands."
        )
        skill = parse_skill(skill_dir)
        flags = [f.flag for f in detect_skill_findings(skill)]
        assert "CLAUDE_TOOL_REFS" in flags

    def test_bare_backticked_token_no_false_positive(self, tmp_path: Path):
        """Generic prose backticks like Rust's `Task` type must NOT fire CLAUDE_TOOL_REFS."""
        skill_dir = _make_skill(
            tmp_path,
            "Rust's `Task` is a future. `Read` and `Write` are stdlib traits. Set `LS` for line sep.",
        )
        skill = parse_skill(skill_dir)
        flags = [f.flag for f in detect_skill_findings(skill)]
        assert "CLAUDE_TOOL_REFS" not in flags

    def test_tool_prose_fires(self, tmp_path: Path):
        skill_dir = _make_skill(tmp_path, "First, use the Read tool to open the file.")
        skill = parse_skill(skill_dir)
        flags = [f.flag for f in detect_skill_findings(skill)]
        assert "CLAUDE_TOOL_PROSE" in flags

    def test_tool_prose_no_false_positive_on_lowercase_words(self, tmp_path: Path):
        """`the bash tool` (shell, lowercase) must NOT fire CLAUDE_TOOL_PROSE."""
        skill_dir = _make_skill(
            tmp_path,
            "Configure the bash tool in your Makefile. The read tool target is at line 12.",
        )
        skill = parse_skill(skill_dir)
        flags = [f.flag for f in detect_skill_findings(skill)]
        assert "CLAUDE_TOOL_PROSE" not in flags

    def test_findings_carry_remediation(self, tmp_path: Path):
        skill_dir = _make_skill(tmp_path, "Use the Bash tool.")
        skill = parse_skill(skill_dir)
        findings = detect_skill_findings(skill)
        assert findings
        assert all(f.remediation for f in findings)
        # Remediation appears in the AntiPattern description
        ap = findings[0].to_anti_pattern()
        assert "Fix:" in ap.description


class TestAgentFindings:
    def test_clean_agent_has_no_findings(self, tmp_path: Path):
        agent_file = _make_agent(tmp_path, "name: my-explorer\ndescription: Use when exploring.\nmodel: inherit")
        agent = parse_agent(agent_file)
        assert detect_agent_findings(agent) == []
        assert score_agent_portability(agent) == 1.0

    def test_builtin_name_collision_fires(self, tmp_path: Path):
        agent_file = _make_agent(tmp_path, "name: worker\ndescription: Use when working.\nmodel: inherit")
        agent = parse_agent(agent_file)
        flags = [f.flag for f in detect_agent_findings(agent)]
        assert "AGENT_NAME_COLLISION" in flags

    def test_bare_model_alias_fires(self, tmp_path: Path):
        agent_file = _make_agent(tmp_path, "name: my-agent\ndescription: Use when delegating.\nmodel: opus")
        agent = parse_agent(agent_file)
        flags = [f.flag for f in detect_agent_findings(agent)]
        assert "BARE_MODEL_ALIAS" in flags

    def test_inherit_model_passes(self, tmp_path: Path):
        agent_file = _make_agent(tmp_path, "name: my-agent\ndescription: Use when delegating.\nmodel: inherit")
        agent = parse_agent(agent_file)
        flags = [f.flag for f in detect_agent_findings(agent)]
        assert "BARE_MODEL_ALIAS" not in flags

    def test_camel_tool_refs_in_agent_body(self, tmp_path: Path):
        agent_file = _make_agent(
            tmp_path,
            "name: my-agent\ndescription: Use when delegating.\nmodel: inherit",
            body="Use `Read` and `Glob` to explore the filesystem.",
        )
        agent = parse_agent(agent_file)
        flags = [f.flag for f in detect_agent_findings(agent)]
        assert "CLAUDE_TOOL_REFS" in flags
