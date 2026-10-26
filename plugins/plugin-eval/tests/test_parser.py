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

    def test_parse_cross_references_preserves_nested_paths(self, tmp_path: Path):
        skill_dir = tmp_path / "parent"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: parent\n"
            'description: "Use when testing nested references."\n'
            "---\n\n"
            "See sub-skills/child/SKILL.md and skills/sibling/SKILL.md in prose.\n"
        )

        skill = parse_skill(skill_dir)

        assert skill.cross_references == ["sub-skills/child", "sibling"]

    def test_cross_references_exclude_inline_code_spans(self, tmp_path: Path):
        """Inline code mentions are illustrative (commands, examples), not refs.

        Without this exclusion, any backticked mention of a skills/<slug>
        path whose target does not exist on disk produces a DEAD_CROSS_REF
        false positive (observed in practice: 12 such flags on one
        narrative-heavy skill).
        """
        skill_dir = tmp_path / "commanded"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: commanded\n"
            'description: "Use when testing inline code exclusion."\n'
            "---\n\n"
            "Run `bash skills/self/scripts/run.sh` and read `skills/self/results.json`.\n"
        )

        skill = parse_skill(skill_dir)

        assert skill.cross_references == []

    def test_cross_references_exclude_fenced_blocks(self, tmp_path: Path):
        skill_dir = tmp_path / "fenced"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: fenced\n"
            'description: "Use when testing fenced block exclusion."\n'
            "---\n\n"
            "```\nskills/ghost/does-not-exist\n```\n\n"
            "Real reference: skills/sibling/SKILL.md in prose.\n"
        )

        skill = parse_skill(skill_dir)

        assert skill.cross_references == ["sibling"]

    def test_fence_like_line_inside_a_block_does_not_close_it(self, tmp_path: Path):
        """A closing fence must be a bare marker run: `echo "```"` is content."""
        skill_dir = tmp_path / "fence-like"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: fence-like\n"
            'description: "Use when testing fence-line closing rules."\n'
            "---\n\n"
            "```bash\n"
            'echo "```"\n'
            "skills/ghost/does-not-exist\n"
            "```\n\n"
            "Real reference: skills/sibling/SKILL.md in prose.\n"
        )

        skill = parse_skill(skill_dir)

        assert skill.cross_references == ["sibling"]

    def test_unclosed_fence_extends_to_end_of_body(self, tmp_path: Path):
        skill_dir = tmp_path / "unclosed"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: unclosed\n"
            'description: "Use when testing unclosed fence handling."\n'
            "---\n\n"
            "```bash\n"
            "skills/ghost/does-not-exist\n"
            "and the block never closes\n"
        )

        skill = parse_skill(skill_dir)

        assert skill.cross_references == []

    def test_code_spans_match_by_delimiter_length(self, tmp_path: Path):
        """A double-backtick span closes on a double-backtick run, per CommonMark."""
        skill_dir = tmp_path / "multi-span"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            "name: multi-span\n"
            'description: "Use when testing multi-backtick code spans."\n'
            "---\n\n"
            "``skills/ghost/does-not-exist`` stays illustrative, and a ``nested `tick` span`` too.\n"
        )

        skill = parse_skill(skill_dir)

        assert skill.cross_references == []


class TestCodeBlockCounting:
    def _skill(self, tmp_path: Path, body: str, name: str = "counted") -> Path:
        skill_dir = tmp_path / name
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\n"
            f"name: {name}\n"
            'description: "Use when counting fenced code blocks."\n'
            "---\n\n"
            "# Counted\n\n" + body
        )
        return skill_dir

    def test_each_fenced_block_counts_once(self, tmp_path: Path):
        body = "\n\n".join(["```python\nprint('x')\n```"] * 3)
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 3
        assert skill.code_block_languages == ["python", "python", "python"]

    def test_languages_come_from_opening_fences(self, tmp_path: Path):
        body = "```bash\nls\n```\n\n```yaml\nkey: value\n```\n"
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 2
        assert skill.code_block_languages == ["bash", "yaml"]

    def test_unclosed_fence_still_counts_as_a_block(self, tmp_path: Path):
        body = "```python\nprint('x')\n```\n\n```bash\nls\n"
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 2
        assert skill.code_block_languages == ["python", "bash"]

    def test_shorter_fence_inside_a_longer_one_is_not_a_block(self, tmp_path: Path):
        body = "````markdown\n```python\nprint('x')\n```\n````\n"
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 1
        assert skill.code_block_languages == ["markdown"]

    def test_fence_inside_a_blockquote_counts(self, tmp_path: Path):
        body = "> ```bash\n> ls\n> ```\n"
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 1
        assert skill.code_block_languages == ["bash"]

    def test_prose_without_fences_counts_nothing(self, tmp_path: Path):
        skill = parse_skill(self._skill(tmp_path, "Just prose about ``inline code``.\n"))
        assert skill.code_block_count == 0
        assert skill.code_block_languages == []

    def test_tilde_fenced_block_counts_once_with_its_language(self, tmp_path: Path):
        body = "~~~python\nprint('x')\n~~~\n"
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 1
        assert skill.code_block_languages == ["python"]

    def test_tilde_run_inside_a_backtick_block_does_not_close_it(self, tmp_path: Path):
        body = "```markdown\n~~~\nstill inside\n~~~\n```\n\n```bash\nls\n```\n"
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 2
        assert skill.code_block_languages == ["markdown", "bash"]

    def test_fence_run_with_trailing_text_does_not_close_a_block(self, tmp_path: Path):
        body = "```\n``` text\n```\n"
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 1
        assert skill.code_block_languages == []

    def test_closing_fence_with_trailing_whitespace_still_closes(self, tmp_path: Path):
        body = "```python\nprint('x')\n```   \n\n```bash\nls\n```\n"
        skill = parse_skill(self._skill(tmp_path, body))
        assert skill.code_block_count == 2
        assert skill.code_block_languages == ["python", "bash"]


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
