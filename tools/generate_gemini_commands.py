#!/usr/bin/env python3
"""Generate Gemini CLI TOML slash commands from Claude Code command .md files."""

import os
import re
import sys

WORKTREE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(WORKTREE, "plugins")
COMMANDS_OUT = os.path.join(WORKTREE, "commands")


# ── Parsing helpers ──────────────────────────────────────────────────────────

def read_file(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (fields, body). Fields are plain strings; no yaml dep needed."""
    fields: dict = {}
    if not content.startswith("---"):
        return fields, content

    end = content.find("\n---", 3)
    if end == -1:
        return fields, content

    block = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")

    current_key = None
    in_list = False
    for line in block.splitlines():
        m = re.match(r'^(\w[\w-]*):\s*(.*)', line)
        if m:
            current_key = m.group(1)
            val = m.group(2).strip().strip('"')
            if val in ("", "["):
                fields[current_key] = []
                in_list = val == "["
            else:
                fields[current_key] = val
                in_list = False
        elif in_list and isinstance(fields.get(current_key), list):
            item = line.strip().strip('",[] ')
            if item and item != "]":
                fields[current_key].append(item)
        elif current_key and isinstance(fields.get(current_key), str) and line.startswith("  "):
            fields[current_key] += " " + line.strip().strip('"')

    return fields, body


def h1_from_body(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def context_paragraph(body: str) -> str:
    """Extract the first substantive paragraph after the H1 heading."""
    lines = body.splitlines()
    past_h1 = False
    collecting = False
    paras: list[str] = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and not past_h1:
            past_h1 = True
            continue
        if not past_h1:
            continue
        # Skip section headings and rule lists
        if stripped.startswith("#") or stripped.startswith("##"):
            if collecting:
                break
            continue
        if stripped.startswith("You MUST") or stripped.startswith("## CRITICAL"):
            break
        if stripped:
            collecting = True
            paras.append(stripped)
        elif collecting and paras:
            break

    text = " ".join(paras).strip()
    # Cap at ~300 chars for prompt brevity
    if len(text) > 300:
        text = text[:297] + "..."
    return text


def skill_names(plugin_dir: str) -> list[str]:
    skills_dir = os.path.join(plugin_dir, "skills")
    if not os.path.isdir(skills_dir):
        return []
    return sorted(
        d for d in os.listdir(skills_dir)
        if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md"))
    )


def agent_names(plugin_dir: str) -> list[str]:
    agents_dir = os.path.join(plugin_dir, "agents")
    if not os.path.isdir(agents_dir):
        return []
    return [f.removesuffix(".md") for f in sorted(os.listdir(agents_dir)) if f.endswith(".md")]


# ── TOML generation ──────────────────────────────────────────────────────────

def escape_toml_string(s: str) -> str:
    """Escape for TOML basic string (double-quoted)."""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def _similar(a: str, b: str) -> bool:
    """True if strings share more than half their words (dedup check)."""
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return False
    return len(wa & wb) / min(len(wa), len(wb)) > 0.55


def build_prompt(
    description: str,
    arg_hint: str,
    context: str,
    keywords: list[str],
    skills: list[str],
    agents: list[str],
) -> str:
    parts: list[str] = []

    parts.append(description.rstrip(".") + ".")

    if context and not _similar(context, description):
        parts.append("")
        parts.append(context)

    if keywords:
        parts.append("")
        kw_line = "Relevant tools and techniques: " + ", ".join(keywords[:8]) + "."
        parts.append(kw_line)

    if agents:
        parts.append("")
        parts.append("Available agents: " + ", ".join(f"`{a}`" for a in agents) + ".")

    if skills:
        parts.append("")
        parts.append("Available skills: " + ", ".join(f"`{s}`" for s in skills) + ".")

    if arg_hint:
        parts.append("")
        parts.append(f"Arguments: {arg_hint}")

    parts.append("")
    parts.append("{{args}}")

    return "\n".join(parts)


def generate_toml(description: str, prompt: str) -> str:
    lines = ['description = "' + escape_toml_string(description) + '"', "prompt = '''"]
    lines.append(prompt)
    lines.append("'''")
    lines.append("")
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    created = 0
    errors: list[str] = []

    plugins = sorted(
        p for p in os.listdir(PLUGINS_DIR)
        if os.path.isdir(os.path.join(PLUGINS_DIR, p))
    )

    for plugin_name in plugins:
        plugin_dir = os.path.join(PLUGINS_DIR, plugin_name)
        cmds_dir = os.path.join(plugin_dir, "commands")
        if not os.path.isdir(cmds_dir):
            continue

        cmd_files = sorted(f for f in os.listdir(cmds_dir) if f.endswith(".md"))
        if not cmd_files:
            continue

        agents = agent_names(plugin_dir)
        skills = skill_names(plugin_dir)
        out_dir = os.path.join(COMMANDS_OUT, plugin_name)
        os.makedirs(out_dir, exist_ok=True)

        for cmd_file in cmd_files:
            cmd_name = cmd_file.removesuffix(".md")
            content = read_file(os.path.join(cmds_dir, cmd_file))
            fm, body = parse_frontmatter(content)

            description = (
                (fm.get("description") or "").strip()
                or h1_from_body(body)
                or cmd_name.replace("-", " ").title()
            )
            arg_hint = (fm.get("argument-hint") or "").strip()
            keywords = fm.get("keywords") or []
            if isinstance(keywords, str):
                keywords = [k.strip() for k in keywords.split(",")]
            context = context_paragraph(body)

            prompt = build_prompt(description, arg_hint, context, keywords, skills, agents)
            toml_content = generate_toml(description, prompt)

            out_path = os.path.join(out_dir, cmd_name + ".toml")
            try:
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(toml_content)
                created += 1
                print(f"  wrote commands/{plugin_name}/{cmd_name}.toml")
            except OSError as e:
                errors.append(f"{plugin_name}/{cmd_name}: {e}")
                print(f"  ERROR {plugin_name}/{cmd_name}: {e}", file=sys.stderr)

    print(f"\nDone: {created} TOML commands created, {len(errors)} errors")
    if errors:
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
