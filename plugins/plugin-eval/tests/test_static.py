from pathlib import Path

import pytest

from plugin_eval.layers.static import _TRIGGER_PATTERN, StaticAnalyzer
from plugin_eval.models import LayerResult


def _make_skill(tmp_path: Path, description: str, name: str = "test-skill") -> Path:
    skill_dir = tmp_path / name
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: \"{description}\"\n---\n\n"
        "# Skill\n\n## Overview\n\nBody.\n"
    )
    return skill_dir


class TestStaticAnalyzer:
    def test_analyze_valid_skill(self, sample_skill_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(sample_skill_dir)
        assert isinstance(result, LayerResult)
        assert result.layer == "static"
        assert result.score > 0.5
        assert len(result.anti_patterns) == 0

    def test_analyze_poor_skill(self, poor_skill_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(poor_skill_dir)
        assert result.score < 0.7
        flags = [ap.flag for ap in result.anti_patterns]
        assert "OVER_CONSTRAINED" in flags
        assert "MISSING_TRIGGER" in flags

    def test_analyze_plugin(self, sample_plugin_dir: Path):
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_plugin(sample_plugin_dir)
        assert result.layer == "static"
        assert result.score > 0.5
        assert "skill_scores" in result.sub_scores
        assert "agent_scores" in result.sub_scores

    def test_anti_pattern_penalty(self):
        analyzer = StaticAnalyzer()
        assert analyzer._anti_pattern_penalty(0) == 1.0
        assert analyzer._anti_pattern_penalty(2) == pytest.approx(0.9)
        assert analyzer._anti_pattern_penalty(10) == 0.5
        assert analyzer._anti_pattern_penalty(20) == 0.5

    def test_description_pushiness_score(self):
        analyzer = StaticAnalyzer()
        good = "Test skill for evaluation. Use when testing plugin-eval. Use PROACTIVELY for quality checks."
        weak = "A skill."
        assert analyzer._description_pushiness(good) > analyzer._description_pushiness(weak)


class TestTriggerPattern:
    """Regression coverage for the broadened trigger-phrase matcher.

    plugin-dev's canonical recommendation is third-person ("This skill should be
    used when …"), and several real-world plugins use prepositional triggers
    ("Use after …", "Use before …"). The pre-2026 regex only matched the
    imperative "Use when …" form, which produced false-positive MISSING_TRIGGER
    flags against Anthropic's own examples.
    """

    @pytest.mark.parametrize(
        "description",
        [
            "Use when testing plugin-eval.",
            "Use this skill when scaffolding plugins.",
            "This skill should be used when the user asks to 'create a hook'.",
            "Used when several attempts have failed in a row.",
            "Use after editing the source-of-truth files, before committing.",
            "Use before declaring a task complete after a hard debugging session.",
            "Use immediately before a commit, push, or edit-after-failure.",
            "Use whenever you are asked to plan inside a Paperclip company.",
            "Auto-loads when working on test files.",
            "Trigger when a Bash command fails three times in a row.",
            "Use PROACTIVELY before merging.",
        ],
    )
    def test_pattern_matches_canonical_forms(self, description: str) -> None:
        assert _TRIGGER_PATTERN.search(description), (
            f"Expected trigger phrase to match in: {description!r}"
        )

    @pytest.mark.parametrize(
        "description",
        [
            "A skill.",
            "Provides hook guidance.",
            "Returns the current timestamp.",
            "Performs static analysis on plugin directories.",
        ],
    )
    def test_pattern_rejects_descriptions_without_trigger(self, description: str) -> None:
        assert not _TRIGGER_PATTERN.search(description), (
            f"Did not expect trigger match in: {description!r}"
        )

    def test_third_person_skill_does_not_flag_missing_trigger(self, tmp_path: Path) -> None:
        """Anthropic plugin-dev's canonical phrasing must not be flagged."""
        skill_dir = _make_skill(
            tmp_path,
            "This skill should be used when the user asks to 'create a hook', "
            "'add a PreToolUse hook', or 'validate tool use'.",
        )
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(skill_dir)
        flags = [ap.flag for ap in result.anti_patterns]
        assert "MISSING_TRIGGER" not in flags

    def test_prepositional_trigger_does_not_flag_missing_trigger(self, tmp_path: Path) -> None:
        skill_dir = _make_skill(
            tmp_path,
            "Self-check before a single risky action. Use immediately before a "
            "commit, push, edit-after-failure, or skip-a-verification step.",
        )
        analyzer = StaticAnalyzer()
        result = analyzer.analyze_skill(skill_dir)
        flags = [ap.flag for ap in result.anti_patterns]
        assert "MISSING_TRIGGER" not in flags
