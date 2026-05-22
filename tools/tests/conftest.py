"""Shared fixtures for adapter tests."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make `tools` package importable when running pytest from the repo root.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from tools.adapters.base import (  # noqa: E402
    AgentSource,
    CommandSource,
    PluginSource,
    SkillSource,
    parse_frontmatter,
)


def _make_skill(plugin_dir: Path, name: str, frontmatter: str, body: str) -> SkillSource:
    """Build a SkillSource on disk under plugin_dir/skills/<name>/SKILL.md."""
    skill_dir = plugin_dir / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    content = f"---\n{frontmatter}\n---\n\n{body}\n"
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
    fm, parsed_body = parse_frontmatter(content)
    return SkillSource(
        plugin=plugin_dir.name,
        name=name,
        dir=skill_dir,
        frontmatter=fm,
        body=parsed_body,
    )


def _make_agent(plugin_dir: Path, name: str, frontmatter: str, body: str) -> AgentSource:
    agents_dir = plugin_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    content = f"---\n{frontmatter}\n---\n\n{body}\n"
    path = agents_dir / f"{name}.md"
    path.write_text(content, encoding="utf-8")
    fm, parsed_body = parse_frontmatter(content)
    return AgentSource(
        plugin=plugin_dir.name,
        name=name,
        path=path,
        frontmatter=fm,
        body=parsed_body,
    )


def _make_command(plugin_dir: Path, name: str, frontmatter: str, body: str) -> CommandSource:
    cmds_dir = plugin_dir / "commands"
    cmds_dir.mkdir(parents=True, exist_ok=True)
    content = f"---\n{frontmatter}\n---\n\n{body}\n"
    path = cmds_dir / f"{name}.md"
    path.write_text(content, encoding="utf-8")
    fm, parsed_body = parse_frontmatter(content)
    return CommandSource(
        plugin=plugin_dir.name,
        name=name,
        path=path,
        frontmatter=fm,
        body=parsed_body,
    )


@pytest.fixture
def synthetic_plugin(tmp_path: Path) -> PluginSource:
    """One-of-each plugin: 1 agent, 1 skill, 1 command. Used by every adapter test."""
    plugin_dir = tmp_path / "demo"
    plugin_dir.mkdir()
    (plugin_dir / ".claude-plugin").mkdir()
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
        '{"name": "demo", "version": "1.0.0", "description": "Demo plugin for tests",'
        ' "author": {"name": "Tester", "email": "t@example.com"},'
        ' "homepage": "https://example.com", "license": "MIT", "category": "test"}'
    )

    skill = _make_skill(
        plugin_dir,
        "hello",
        "name: hello\ndescription: Use when greeting users.",
        "# Hello\n\nUse the `Read` tool to open files. Run `Bash` to greet.\n",
    )
    agent = _make_agent(
        plugin_dir,
        "greeter",
        "name: greeter\ndescription: Use when delegating greetings.\nmodel: opus\ntools: Read, Grep\ncolor: blue",
        "# Greeter agent\n\nDelegate greeting tasks here.\n",
    )
    command = _make_command(
        plugin_dir,
        "say-hi",
        'description: "Send a greeting"\nargument-hint: <name>',
        "# Say Hi\n\nGreet the user named $ARGUMENTS.\n",
    )

    return PluginSource(
        name="demo",
        dir=plugin_dir,
        plugin_json={
            "name": "demo",
            "version": "1.0.0",
            "description": "Demo plugin for tests",
            "author": {"name": "Tester", "email": "t@example.com"},
            "homepage": "https://example.com",
            "license": "MIT",
            "category": "test",
        },
        agents=[agent],
        skills=[skill],
        commands=[command],
    )


@pytest.fixture
def output_root(tmp_path: Path) -> Path:
    """Isolated output dir for each adapter test."""
    out = tmp_path / "out"
    out.mkdir()
    return out
