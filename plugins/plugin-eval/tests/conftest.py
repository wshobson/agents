from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_skill_dir(tmp_path: Path) -> Path:
    """Create a minimal valid skill directory."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        "---\n"
        "name: test-skill\n"
        'description: "Test skill for evaluation. Use when testing plugin-eval."\n'
        "---\n\n"
        "# Test Skill\n\n"
        "## Overview\n\n"
        "This is a test skill for evaluation purposes.\n\n"
        "## Usage\n\n"
        "```python\nprint('hello')\n```\n\n"
        "## Troubleshooting\n\n"
        "Check the logs.\n"
    )
    refs_dir = skill_dir / "references"
    refs_dir.mkdir()
    (refs_dir / "guide.md").write_text("# Guide\n\nDetailed reference content.\n")
    return skill_dir


@pytest.fixture
def sample_plugin_dir(tmp_path: Path, sample_skill_dir: Path) -> Path:
    """Create a minimal valid plugin directory."""
    plugin_dir = tmp_path / "test-plugin"
    plugin_dir.mkdir()
    claude_dir = plugin_dir / ".claude-plugin"
    claude_dir.mkdir()
    (claude_dir / "plugin.json").write_text('{"name": "test-plugin"}')

    skills_dir = plugin_dir / "skills"
    skills_dir.mkdir()
    import shutil
    dest = skills_dir / "test-skill"
    shutil.copytree(sample_skill_dir, dest)

    agents_dir = plugin_dir / "agents"
    agents_dir.mkdir()
    (agents_dir / "test-agent.md").write_text(
        "---\n"
        "name: test-agent\n"
        'description: "Test agent. Use PROACTIVELY for testing."\n'
        "model: sonnet\n"
        "tools: Read, Grep, Glob\n"
        "---\n\n"
        "You are a test agent.\n"
    )
    return plugin_dir


@pytest.fixture
def poor_skill_dir(tmp_path: Path) -> Path:
    """Create a skill with multiple anti-patterns."""
    skill_dir = tmp_path / "poor-skill"
    skill_dir.mkdir()
    skill_md = skill_dir / "SKILL.md"
    lines = ["---\n", "name: poor-skill\n", 'description: "A skill."\n', "---\n\n"]
    lines.append("# Poor Skill\n\n")
    for i in range(100):
        lines.append(f"You MUST follow rule {i}. You ALWAYS do this. NEVER skip.\n")
    skill_md.write_text("".join(lines))
    refs = skill_dir / "references"
    refs.mkdir()
    (refs / "orphan.md").write_text("# Orphan\n\nNot referenced from SKILL.md.\n")
    return skill_dir
