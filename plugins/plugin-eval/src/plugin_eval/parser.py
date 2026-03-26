"""Parse Claude Code plugin structure: skills, agents, plugin.json."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class ParsedSkill:
    path: Path
    name: str
    description: str
    line_count: int
    h2_count: int
    h3_count: int
    code_block_count: int
    code_block_languages: list[str]
    has_examples: bool
    has_troubleshooting: bool
    has_references: bool
    has_assets: bool
    reference_files: list[str]
    asset_files: list[str]
    total_content_lines: int
    must_never_always_count: int
    cross_references: list[str]
    raw_content: str
    frontmatter: dict


@dataclass
class ParsedAgent:
    path: Path
    name: str
    description: str
    model: str | None
    has_tools_restriction: bool
    tools: list[str]
    has_proactive_trigger: bool
    skill_references: list[str]
    raw_content: str
    frontmatter: dict


@dataclass
class ParsedPlugin:
    path: Path
    name: str
    skills: list[ParsedSkill] = field(default_factory=list)
    agents: list[ParsedAgent] = field(default_factory=list)
    plugin_json: dict = field(default_factory=dict)


def parse_skill(skill_dir: Path) -> ParsedSkill:
    """Parse a skill directory into structured data."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"No SKILL.md found in {skill_dir}")

    content = skill_md.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(content)
    lines = body.strip().split("\n")

    h2_count = sum(1 for line in lines if re.match(r"^## ", line))
    h3_count = sum(1 for line in lines if re.match(r"^### ", line))

    code_blocks = re.findall(r"```(\w*)", content)
    code_block_languages = [lang for lang in code_blocks if lang]

    lower_body = body.lower()
    has_examples = bool(re.search(r"(## example|### example|## usage)", lower_body))
    has_troubleshooting = bool(re.search(r"(## troubleshoot|## common issue|## faq)", lower_body))

    refs_dir = skill_dir / "references"
    assets_dir = skill_dir / "assets"
    reference_files = (
        [f.name for f in refs_dir.iterdir() if f.is_file()] if refs_dir.exists() else []
    )
    asset_files = (
        [f.name for f in assets_dir.iterdir() if f.is_file()] if assets_dir.exists() else []
    )

    total_lines = len(content.split("\n"))
    for ref_file in reference_files:
        ref_path = refs_dir / ref_file
        total_lines += len(ref_path.read_text(encoding="utf-8").split("\n"))

    must_pattern = re.compile(r"\b(MUST|NEVER|ALWAYS)\b")
    must_count = len(must_pattern.findall(content))

    cross_refs = re.findall(r"(?:skill|skills)/([a-z0-9-]+)", body)

    return ParsedSkill(
        path=skill_dir,
        name=frontmatter.get("name", skill_dir.name),
        description=frontmatter.get("description", ""),
        line_count=len(content.split("\n")),
        h2_count=h2_count,
        h3_count=h3_count,
        code_block_count=len(code_blocks),
        code_block_languages=code_block_languages,
        has_examples=has_examples,
        has_troubleshooting=has_troubleshooting,
        has_references=refs_dir.exists(),
        has_assets=assets_dir.exists(),
        reference_files=reference_files,
        asset_files=asset_files,
        total_content_lines=total_lines,
        must_never_always_count=must_count,
        cross_references=cross_refs,
        raw_content=content,
        frontmatter=frontmatter,
    )


def parse_agent(agent_path: Path) -> ParsedAgent:
    """Parse an agent markdown file."""
    content = agent_path.read_text(encoding="utf-8")
    frontmatter, body = _split_frontmatter(content)

    tools_raw = frontmatter.get("tools", "")
    if isinstance(tools_raw, list):
        tools = [str(t).strip() for t in tools_raw]
    elif isinstance(tools_raw, str) and tools_raw:
        tools = [t.strip() for t in tools_raw.split(",")]
    else:
        tools = []

    description = frontmatter.get("description", "")
    has_proactive = bool(re.search(r"use proactively", description, re.IGNORECASE))

    skill_refs = re.findall(r"(?:skill|skills)/([a-z0-9-]+)", body)

    return ParsedAgent(
        path=agent_path,
        name=frontmatter.get("name", agent_path.stem),
        description=description,
        model=frontmatter.get("model"),
        has_tools_restriction=bool(tools),
        tools=tools,
        has_proactive_trigger=has_proactive,
        skill_references=skill_refs,
        raw_content=content,
        frontmatter=frontmatter,
    )


def parse_plugin(plugin_dir: Path) -> ParsedPlugin:
    """Parse an entire plugin directory."""
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    plugin_json = {}
    if plugin_json_path.exists():
        plugin_json = json.loads(plugin_json_path.read_text(encoding="utf-8"))

    name = plugin_json.get("name", plugin_dir.name)

    skills = []
    skills_dir = plugin_dir / "skills"
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                skills.append(parse_skill(skill_dir))

    agents = []
    agents_dir = plugin_dir / "agents"
    if agents_dir.exists():
        for agent_file in sorted(agents_dir.glob("*.md")):
            agents.append(parse_agent(agent_file))

    return ParsedPlugin(
        path=plugin_dir,
        name=name,
        skills=skills,
        agents=agents,
        plugin_json=plugin_json,
    )


def _split_frontmatter(content: str) -> tuple[dict, str]:
    """Split YAML frontmatter from markdown body."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    try:
        frontmatter = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        frontmatter = {}

    return frontmatter, parts[2]
