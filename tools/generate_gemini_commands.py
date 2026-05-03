#!/usr/bin/env python3
"""Generate Gemini CLI TOML slash commands from Claude Code command .md files."""

import argparse
import json
import os
import re
import sys
from pathlib import Path

WORKTREE = Path(__file__).resolve().parent.parent
PLUGINS_DIR = WORKTREE / "plugins"
COMMANDS_OUT = WORKTREE / "commands"


# ── Parsing helpers ──────────────────────────────────────────────────────────

def read_file(path: Path) -> str:
    """Read file content as UTF-8 string."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_plugin_json(plugin_dir: Path) -> dict:
    """Read and parse plugin.json from plugin directory."""
    path = plugin_dir / ".claude-plugin" / "plugin.json"
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


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
    """Extract the first H1 heading from Markdown body."""
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


def skill_names(plugin_dir: Path) -> list[str]:
    """Return sorted list of skill names in plugin directory."""
    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        return []
    return sorted(
        d.name for d in skills_dir.iterdir()
        if d.is_dir() and (d / "SKILL.md").is_file()
    )


def agent_names(plugin_dir: Path) -> list[str]:
    """Return sorted list of agent names in plugin directory."""
    agents_dir = plugin_dir / "agents"
    if not agents_dir.is_dir():
        return []
    return [f.name.removesuffix(".md") for f in sorted(agents_dir.iterdir()) if f.name.endswith(".md")]


# ── TOML generation ──────────────────────────────────────────────────────────

def escape_toml_string(s: str) -> str:
    """Escape for TOML basic string (double-quoted)."""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def build_prompt(
    plugin_name: str,
    cmd_name: str,
    cmd_path: str,
    description: str,
    arg_hint: str,
    skills: list[str],
    agents: list[str],
) -> str:
    """Build the Gemini CLI command prompt."""
    parts: list[str] = []

    parts.append(f"You are the Orchestrator for the {description.rstrip('.')}.")
    parts.append("")
    parts.append(f"1. READ the full protocol definition at: `{cmd_path}`")
    parts.append("2. INITIALIZE the session according to the 'Pre-flight Checks' in that file.")
    parts.append("3. EXECUTE the steps sequentially. Use the `executing-plans` skill to manage progress.")
    parts.append("4. STOP at all `PHASE CHECKPOINT` or `GATE` boundaries. Use `ask_user` to get approval.")
    
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


def build_entry_prompt(
    plugin_name: str,
    description: str,
    skills: list[str],
    agents: list[str],
) -> str:
    """Build the top-level plugin entry point prompt."""
    parts: list[str] = []
    parts.append(description.rstrip(".") + ".")
    parts.append("")
    parts.append(f"This is the top-level entry point for the `{plugin_name}` plugin.")
    
    if agents:
        parts.append("")
        parts.append("Available agents: " + ", ".join(f"`{a}`" for a in agents) + ".")

    if skills:
        parts.append("")
        parts.append("Available skills: " + ", ".join(f"`{s}`" for s in skills) + ".")

    parts.append("")
    parts.append("{{args}}")
    return "\n".join(parts)


def escape_toml_prompt(s: str) -> str:
    """Escape for TOML multiline basic string (triple double-quoted)."""
    return s.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')


def generate_toml(description: str, prompt: str) -> str:
    """Generate the full TOML content for a command."""
    lines = ['description = "' + escape_toml_string(description) + '"', 'prompt = """']
    lines.append(escape_toml_prompt(prompt))
    lines.append('"""')
    lines.append("")
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Gemini CLI TOML commands.")
    parser.add_argument("--plugin", help="Only sync commands for the specified plugin.")
    parser.add_argument("--all", action="store_true", help="Generate commands for ALL plugins.")
    parser.add_argument("--prune", action="store_true", help="Delete TOMLs that no longer have a source .md file.")
    args = parser.parse_args()

    created = 0
    deleted = 0
    errors: list[str] = []

    # ── Pruning ─────────────────────────────────────────────────────────────
    if args.prune and COMMANDS_OUT.is_dir():
        for toml_path in COMMANDS_OUT.rglob("*.toml"):
            # Security: Ensure we are only deleting inside COMMANDS_OUT
            if not toml_path.resolve().is_relative_to(COMMANDS_OUT.resolve()):
                continue

            rel_path = toml_path.relative_to(COMMANDS_OUT)
            parts = rel_path.parts
            
            should_delete = False
            if len(parts) == 1:
                # Top-level plugin toml
                plugin_name = toml_path.stem
                if not (PLUGINS_DIR / plugin_name).is_dir():
                    should_delete = True
            elif len(parts) == 2:
                # Sub-command toml
                plugin_name = parts[0]
                cmd_name = toml_path.stem
                source_md = PLUGINS_DIR / plugin_name / "commands" / f"{cmd_name}.md"
                if not source_md.is_file():
                    should_delete = True
            
            if should_delete:
                toml_path.unlink()
                deleted += 1
                print(f"  pruned commands/{rel_path}")

    # ── Identify plugins to sync ────────────────────────────────────────────
    plugins_to_sync = []
    if args.plugin:
        if (PLUGINS_DIR / args.plugin).is_dir():
            plugins_to_sync = [args.plugin]
        else:
            print(f"Error: Plugin directory not found: {args.plugin}", file=sys.stderr)
            sys.exit(1)
    elif args.all:
        plugins_to_sync = sorted(p.name for p in PLUGINS_DIR.iterdir() if p.is_dir())
    elif COMMANDS_OUT.is_dir():
        # Smart Sync: Only update plugins that are already present in commands/
        existing_plugin_configs = set()
        for p in COMMANDS_OUT.iterdir():
            if p.is_file() and p.suffix == ".toml":
                existing_plugin_configs.add(p.stem)
            elif p.is_dir() and any(p.iterdir()):
                existing_plugin_configs.add(p.name)
        
        plugins_to_sync = sorted([p for p in existing_plugin_configs if (PLUGINS_DIR / p).is_dir()])
    
    if not plugins_to_sync and not args.prune:
        print("No plugins to sync. Use --plugin <name> or --all.")
        return

    # ── Generation/Sync ─────────────────────────────────────────────────────
    for plugin_name in plugins_to_sync:
        plugin_dir = PLUGINS_DIR / plugin_name
        
        agents = agent_names(plugin_dir)
        skills = skill_names(plugin_dir)
        
        # ── Generate plugin entry point ──────────────────────────────────────
        meta = read_plugin_json(plugin_dir)
        plugin_desc = meta.get("description") or f"{plugin_name.replace('-', ' ').title()} plugin"
        
        entry_prompt = build_entry_prompt(plugin_name, plugin_desc, skills, agents)
        entry_toml = generate_toml(plugin_desc, entry_prompt)
        
        COMMANDS_OUT.mkdir(exist_ok=True)
        entry_path = COMMANDS_OUT / f"{plugin_name}.toml"
        try:
            entry_path.write_text(entry_toml, encoding="utf-8")
            created += 1
            print(f"  wrote commands/{plugin_name}.toml")
        except OSError as e:
            errors.append(f"{plugin_name} entry: {e}")

        # ── Generate sub-commands ────────────────────────────────────────────
        cmds_dir = plugin_dir / "commands"
        if not cmds_dir.is_dir():
            continue

        cmd_files = sorted(f for f in cmds_dir.iterdir() if f.name.endswith(".md"))
        if not cmd_files:
            continue

        out_dir = COMMANDS_OUT / plugin_name
        out_dir.mkdir(exist_ok=True)

        for cmd_file_path in cmd_files:
            cmd_name = cmd_file_path.stem
            cmd_rel_path = f"plugins/{plugin_name}/commands/{cmd_file_path.name}"
            content = read_file(cmd_file_path)
            fm, body = parse_frontmatter(content)

            description = (
                (fm.get("description") or "").strip()
                or h1_from_body(body)
                or cmd_name.replace("-", " ").title()
            )
            arg_hint = (fm.get("argument-hint") or "").strip()

            prompt = build_prompt(plugin_name, cmd_name, cmd_rel_path, description, arg_hint, skills, agents)
            toml_content = generate_toml(description, prompt)

            out_path = out_dir / f"{cmd_name}.toml"
            try:
                out_path.write_text(toml_content, encoding="utf-8")
                created += 1
                print(f"  wrote commands/{plugin_name}/{cmd_name}.toml")
            except OSError as e:
                errors.append(f"{plugin_name}/{cmd_name}: {e}")
                print(f"  ERROR {plugin_name}/{cmd_name}: {e}", file=sys.stderr)

    print(f"\nDone: {created} TOML commands synced, {deleted} pruned, {len(errors)} errors")
    if errors:
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
