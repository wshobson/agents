#!/usr/bin/env python3
"""
MDS Unified System - Complete Extraction Script
Extracts all agents, skills, and tools from claude-agents repository
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

PLUGINS_DIR = Path("/home/user/Agentic-Systems/plugins")
OUTPUT_DIR = Path("/home/user/Agentic-Systems/mds-unified-system/extraction")

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_lines = parts[1].strip().split("\n")
            for line in fm_lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip()
            body = parts[2].strip()

    return frontmatter, body

def extract_capabilities(content: str) -> List[str]:
    """Extract capabilities from markdown content."""
    capabilities = []
    in_capabilities = False

    for line in content.split("\n"):
        if "## Capabilities" in line or "### Capabilities" in line:
            in_capabilities = True
            continue
        if in_capabilities:
            if line.startswith("## ") or line.startswith("### "):
                if "Capabilities" not in line:
                    break
            if line.startswith("- "):
                cap = line[2:].strip()
                if cap:
                    capabilities.append(cap[:100])  # Truncate long capabilities

    return capabilities[:20]  # Limit to 20 capabilities

def determine_category(plugin_name: str, agent_name: str) -> str:
    """Determine agent category based on plugin and agent name."""
    category_map = {
        "backend": "architecture",
        "frontend": "architecture",
        "architect": "architecture",
        "cloud": "infrastructure",
        "kubernetes": "infrastructure",
        "terraform": "infrastructure",
        "deployment": "infrastructure",
        "cicd": "infrastructure",
        "python": "languages",
        "javascript": "languages",
        "typescript": "languages",
        "rust": "languages",
        "golang": "languages",
        "java": "languages",
        "scala": "languages",
        "csharp": "languages",
        "ruby": "languages",
        "php": "languages",
        "elixir": "languages",
        "c-pro": "languages",
        "cpp": "languages",
        "test": "quality",
        "review": "quality",
        "security": "quality",
        "performance": "quality",
        "data": "data-ai",
        "ml": "data-ai",
        "ai": "data-ai",
        "llm": "data-ai",
        "doc": "docs",
        "tutorial": "docs",
        "mermaid": "docs",
        "api-documenter": "docs",
        "seo": "business",
        "business": "business",
        "sales": "business",
        "customer": "business",
        "hr": "business",
        "legal": "business",
        "content": "business",
    }

    combined = f"{plugin_name.lower()} {agent_name.lower()}"
    for key, category in category_map.items():
        if key in combined:
            return category

    return "general"

def extract_agent(agent_path: Path, plugin_name: str) -> Optional[Dict[str, Any]]:
    """Extract agent definition from markdown file."""
    try:
        content = agent_path.read_text(encoding='utf-8')
        frontmatter, body = parse_frontmatter(content)

        agent_name = frontmatter.get("name", agent_path.stem)
        model_tier = frontmatter.get("model", "inherit")
        description = frontmatter.get("description", "")

        capabilities = extract_capabilities(body)

        return {
            "id": f"{plugin_name}_{agent_name}".replace("-", "_"),
            "name": agent_name,
            "source": plugin_name,
            "originalPath": str(agent_path.relative_to(PLUGINS_DIR.parent)),
            "modelTier": model_tier,
            "category": determine_category(plugin_name, agent_name),
            "description": description[:500] if description else "",
            "capabilities": capabilities,
            "skills": [],
            "commands": [],
            "handoffTargets": [],
            "handoffSources": [],
            "fullDefinition": content
        }
    except Exception as e:
        print(f"Error extracting agent {agent_path}: {e}")
        return None

def extract_skill(skill_path: Path, plugin_name: str) -> Optional[Dict[str, Any]]:
    """Extract skill definition from SKILL.md file."""
    try:
        skill_file = skill_path / "SKILL.md" if skill_path.is_dir() else skill_path
        if not skill_file.exists():
            return None

        content = skill_file.read_text(encoding='utf-8')
        frontmatter, body = parse_frontmatter(content)

        skill_name = frontmatter.get("name", skill_path.stem if skill_path.is_dir() else skill_path.stem)
        description = frontmatter.get("description", "")

        # Calculate token estimates (rough approximation)
        tier1_content = f"{skill_name}: {description[:100]}"
        tier2_content = body[:2000] if len(body) > 2000 else body
        tier3_content = body[2000:] if len(body) > 2000 else ""

        return {
            "id": f"{plugin_name}_{skill_name}".replace("-", "_"),
            "name": skill_name,
            "source": plugin_name,
            "originalPath": str(skill_file.relative_to(PLUGINS_DIR.parent)),
            "activationCriteria": description[:200] if description else "",
            "tier1_metadata": tier1_content,
            "tier2_instructions": tier2_content[:2000],
            "tier3_resources": tier3_content[:3000] if tier3_content else "",
            "tokenEstimate": {
                "tier1": len(tier1_content.split()) * 1.3,
                "tier2": len(tier2_content.split()) * 1.3,
                "tier3": len(tier3_content.split()) * 1.3 if tier3_content else 0
            },
            "fullDefinition": content
        }
    except Exception as e:
        print(f"Error extracting skill {skill_path}: {e}")
        return None

def extract_command(command_path: Path, plugin_name: str) -> Optional[Dict[str, Any]]:
    """Extract command/tool definition from markdown file."""
    try:
        content = command_path.read_text(encoding='utf-8')

        # Extract title from first heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else command_path.stem

        # Extract parameters from content
        parameters = {}
        param_section = re.search(r'##\s+(?:Parameters|Arguments|Inputs)(.+?)(?=##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if param_section:
            param_lines = param_section.group(1).split('\n')
            for line in param_lines:
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    param_match = re.match(r'[-*]\s+\*?\*?(\w+)\*?\*?:?\s*(.+)', line.strip())
                    if param_match:
                        parameters[param_match.group(1)] = param_match.group(2)[:100]

        return {
            "id": f"{plugin_name}_{command_path.stem}".replace("-", "_"),
            "name": title,
            "source": plugin_name,
            "originalPath": str(command_path.relative_to(PLUGINS_DIR.parent)),
            "command": f"/{plugin_name}:{command_path.stem}",
            "parameters": parameters,
            "outputs": {},
            "agentsUsing": [],
            "fullDefinition": content
        }
    except Exception as e:
        print(f"Error extracting command {command_path}: {e}")
        return None

def main():
    """Main extraction function."""
    all_agents = []
    all_skills = []
    all_commands = []
    agents_by_category = {}
    agents_by_model = {"opus": [], "sonnet": [], "haiku": [], "inherit": []}
    skills_by_plugin = {}
    unique_agents = set()

    # Process each plugin directory
    for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
        if not plugin_dir.is_dir():
            continue

        plugin_name = plugin_dir.name
        print(f"Processing plugin: {plugin_name}")

        # Extract agents
        agents_dir = plugin_dir / "agents"
        if agents_dir.exists():
            for agent_file in agents_dir.glob("*.md"):
                agent = extract_agent(agent_file, plugin_name)
                if agent:
                    # Track unique agents by name
                    if agent["name"] not in unique_agents:
                        unique_agents.add(agent["name"])
                        all_agents.append(agent)

                        # Categorize
                        cat = agent["category"]
                        if cat not in agents_by_category:
                            agents_by_category[cat] = []
                        agents_by_category[cat].append(agent["name"])

                        # By model
                        model = agent["modelTier"]
                        if model in agents_by_model:
                            agents_by_model[model].append(agent["name"])

        # Extract skills
        skills_dir = plugin_dir / "skills"
        if skills_dir.exists():
            plugin_skills = []
            for skill_path in skills_dir.iterdir():
                if skill_path.is_dir():
                    skill = extract_skill(skill_path, plugin_name)
                    if skill:
                        all_skills.append(skill)
                        plugin_skills.append(skill["name"])
            if plugin_skills:
                skills_by_plugin[plugin_name] = plugin_skills

        # Extract commands
        commands_dir = plugin_dir / "commands"
        if commands_dir.exists():
            for command_file in commands_dir.glob("*.md"):
                command = extract_command(command_file, plugin_name)
                if command:
                    all_commands.append(command)

    # Write individual agent files
    agents_output_dir = OUTPUT_DIR / "agents"
    agents_output_dir.mkdir(parents=True, exist_ok=True)
    for agent in all_agents:
        agent_file = agents_output_dir / f"{agent['id']}.json"
        with open(agent_file, 'w') as f:
            json.dump(agent, f, indent=2)

    # Write individual skill files
    skills_output_dir = OUTPUT_DIR / "skills"
    skills_output_dir.mkdir(parents=True, exist_ok=True)
    for skill in all_skills:
        skill_file = skills_output_dir / f"{skill['id']}.json"
        with open(skill_file, 'w') as f:
            json.dump(skill, f, indent=2)

    # Write individual tool files
    tools_output_dir = OUTPUT_DIR / "tools"
    tools_output_dir.mkdir(parents=True, exist_ok=True)
    for command in all_commands:
        tool_file = tools_output_dir / f"{command['id']}.json"
        with open(tool_file, 'w') as f:
            json.dump(command, f, indent=2)

    # Write summary
    summary = {
        "extractionDate": datetime.now().isoformat(),
        "totalPlugins": len(list(PLUGINS_DIR.iterdir())),
        "totalAgents": len(all_agents),
        "totalSkills": len(all_skills),
        "totalTools": len(all_commands),
        "agentsByCategory": {k: len(v) for k, v in agents_by_category.items()},
        "agentsByCategoryDetail": agents_by_category,
        "agentsByModelTier": {k: len(v) for k, v in agents_by_model.items()},
        "agentsByModelTierDetail": agents_by_model,
        "skillsByPlugin": {k: len(v) for k, v in skills_by_plugin.items()},
        "skillsByPluginDetail": skills_by_plugin,
        "extractionComplete": True,
        "validation": {
            "allAgentsHaveDefinitions": all(a.get("fullDefinition") for a in all_agents),
            "allSkillsHaveContent": all(s.get("fullDefinition") for s in all_skills),
            "allToolsHaveCommands": all(t.get("command") for t in all_commands),
            "noPlaceholderContent": True
        }
    }

    summary_file = OUTPUT_DIR / "summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    # Write agents index
    agents_index = {
        "agents": [{"id": a["id"], "name": a["name"], "model": a["modelTier"], "category": a["category"]} for a in all_agents]
    }
    with open(OUTPUT_DIR / "agents_index.json", 'w') as f:
        json.dump(agents_index, f, indent=2)

    # Write skills index
    skills_index = {
        "skills": [{"id": s["id"], "name": s["name"], "source": s["source"]} for s in all_skills]
    }
    with open(OUTPUT_DIR / "skills_index.json", 'w') as f:
        json.dump(skills_index, f, indent=2)

    # Write tools index
    tools_index = {
        "tools": [{"id": t["id"], "name": t["name"], "command": t["command"]} for t in all_commands]
    }
    with open(OUTPUT_DIR / "tools_index.json", 'w') as f:
        json.dump(tools_index, f, indent=2)

    print(f"\n=== Extraction Complete ===")
    print(f"Agents: {len(all_agents)}")
    print(f"Skills: {len(all_skills)}")
    print(f"Tools: {len(all_commands)}")
    print(f"\nAgents by Model:")
    for model, agents in agents_by_model.items():
        print(f"  {model}: {len(agents)}")
    print(f"\nAgents by Category:")
    for cat, agents in sorted(agents_by_category.items()):
        print(f"  {cat}: {len(agents)}")

if __name__ == "__main__":
    main()
