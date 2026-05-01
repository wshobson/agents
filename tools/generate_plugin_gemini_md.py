#!/usr/bin/env python3
"""Generate per-plugin GEMINI.md files for all plugins in the Gemini CLI extension."""

import os
import re
import sys


WORKTREE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(WORKTREE, "plugins")


def parse_frontmatter(filepath: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body. Returns (fields_dict, body_text)."""
    fields: dict = {}
    body = ""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except OSError:
        return fields, body

    if not content.startswith("---"):
        return fields, content

    end = content.find("\n---", 3)
    if end == -1:
        return fields, content

    block = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")

    current_key = None
    for line in block.splitlines():
        m = re.match(r'^(\w[\w-]*):\s*(.*)', line)
        if m:
            current_key = m.group(1)
            fields[current_key] = m.group(2).strip().strip('"')
        elif current_key and line.startswith(' '):
            fields[current_key] = fields[current_key] + ' ' + line.strip().strip('"')
    return fields, body


def h1_from_body(body: str) -> str:
    """Extract the first H1 heading from markdown body text."""
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def first_sentence(text: str) -> str:
    """Return a natural first sentence, avoiding splits on decimal points."""
    # Split on '. ' or '.\n' but not on digits followed by period (e.g. '5.x')
    m = re.search(r'(?<!\d)\.(?!\d)\s', text)
    if m:
        return text[:m.start()].strip()
    return text[:80].strip()


def plugin_title(plugin_name: str) -> str:
    return plugin_name.replace('-', ' ').title()


def collect_agents(plugin_dir: str) -> list[dict]:
    agents_dir = os.path.join(plugin_dir, "agents")
    if not os.path.isdir(agents_dir):
        return []
    items = []
    for fname in sorted(os.listdir(agents_dir)):
        if not fname.endswith(".md"):
            continue
        fm, body = parse_frontmatter(os.path.join(agents_dir, fname))
        name = fm.get("name") or fname.removesuffix(".md")
        desc = fm.get("description", "").strip() or h1_from_body(body)
        model = fm.get("model", "inherit")
        items.append({"name": name, "description": desc, "model": model})
    return items


def collect_commands(plugin_dir: str, plugin_name: str) -> list[dict]:
    cmds_dir = os.path.join(plugin_dir, "commands")
    if not os.path.isdir(cmds_dir):
        return []
    items = []
    for fname in sorted(os.listdir(cmds_dir)):
        if not fname.endswith(".md"):
            continue
        fm, body = parse_frontmatter(os.path.join(cmds_dir, fname))
        cmd_name = fname.removesuffix(".md")
        desc = fm.get("description", "").strip() or h1_from_body(body)
        hint = fm.get("argument-hint", "").strip()
        items.append({
            "name": cmd_name,
            "slug": f"/{plugin_name}:{cmd_name}",
            "description": desc,
            "hint": hint,
        })
    return items


def collect_skills(plugin_dir: str) -> list[dict]:
    skills_dir = os.path.join(plugin_dir, "skills")
    if not os.path.isdir(skills_dir):
        return []
    items = []
    for skill_name in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, skill_name, "SKILL.md")
        if not os.path.isfile(skill_path):
            continue
        fm, body = parse_frontmatter(skill_path)
        name = fm.get("name") or skill_name
        desc = fm.get("description", "").strip() or h1_from_body(body)
        items.append({"name": name, "description": desc})
    return items


def generate_gemini_md(plugin_name: str, agents: list, commands: list, skills: list) -> str:
    title = plugin_title(plugin_name)
    lines = [f"# {title}", ""]

    # Agents section
    if agents:
        lines += ["## Agents", ""]
        lines.append("In Gemini CLI, invoke agents by describing your task naturally. "
                     "The model activates the appropriate expertise.")
        lines.append("")
        lines.append("| Agent | Model | When to use |")
        lines.append("|---|---|---|")
        for a in agents:
            desc = a["description"].replace("|", "\\|")
            # Truncate very long descriptions for table readability
            if len(desc) > 120:
                desc = desc[:117] + "..."
            lines.append(f"| `{a['name']}` | {a['model']} | {desc} |")
        lines.append("")

    # Commands section
    if commands:
        lines += ["## Commands", ""]
        lines.append("These commands are available in Claude Code via slash command. "
                     "In Gemini CLI, describe the equivalent task in natural language.")
        lines.append("")
        lines.append("| Claude Code Command | Description |")
        lines.append("|---|---|")
        for c in commands:
            desc = c["description"].replace("|", "\\|")
            if len(desc) > 120:
                desc = desc[:117] + "..."
            hint = f" `{c['hint']}`" if c["hint"] else ""
            lines.append(f"| `{c['slug']}`{hint} | {desc} |")
        lines.append("")

    # Skills section
    if skills:
        lines += ["## Skills", ""]
        lines.append("Skills activate automatically when Gemini identifies a matching task.")
        lines.append("")
        lines.append("| Skill | Activates when |")
        lines.append("|---|---|")
        for s in skills:
            desc = s["description"].replace("|", "\\|")
            if len(desc) > 140:
                desc = desc[:137] + "..."
            lines.append(f"| `{s['name']}` | {desc} |")
        lines.append("")

    # Gemini usage note
    lines += ["## Gemini CLI Usage", ""]
    examples = []
    if agents:
        a = agents[0]
        short = first_sentence(a["description"])
        examples.append(f'- "{short}" → activates `{a["name"]}`')
    if skills:
        s = skills[0]
        short = first_sentence(s["description"])
        examples.append(f'- "{short}" → activates `{s["name"]}` skill')
    if commands:
        c = commands[0]
        examples.append(
            f'- In Claude Code: `{c["slug"]}` — in Gemini: describe the task in natural language'
        )

    if examples:
        lines.append("**Example natural language triggers:**")
        lines.append("")
        lines.extend(examples)
        lines.append("")

    lines.append(
        "See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and "
        "[docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences."
    )
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    created = 0
    skipped = 0
    errors = []

    plugins = sorted(
        p for p in os.listdir(PLUGINS_DIR)
        if os.path.isdir(os.path.join(PLUGINS_DIR, p))
    )

    for plugin_name in plugins:
        plugin_dir = os.path.join(PLUGINS_DIR, plugin_name)
        out_path = os.path.join(plugin_dir, "GEMINI.md")

        agents = collect_agents(plugin_dir)
        commands = collect_commands(plugin_dir, plugin_name)
        skills = collect_skills(plugin_dir)

        if not agents and not commands and not skills:
            skipped += 1
            print(f"  skip  {plugin_name} (no components)")
            continue

        content = generate_gemini_md(plugin_name, agents, commands, skills)
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(content)
            created += 1
            print(f"  wrote {plugin_name}/GEMINI.md "
                  f"(agents={len(agents)} cmds={len(commands)} skills={len(skills)})")
        except OSError as e:
            errors.append(f"{plugin_name}: {e}")
            print(f"  ERROR {plugin_name}: {e}", file=sys.stderr)

    print(f"\nDone: {created} created, {skipped} skipped, {len(errors)} errors")
    if errors:
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
