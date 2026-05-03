#!/usr/bin/env python3
"""Generate Gemini CLI TOML slash commands from Claude Code command .md files."""

import argparse
import json
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


def read_plugin_json(plugin_dir: str) -> dict:
    path = os.path.join(plugin_dir, ".claude-plugin", "plugin.json")
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
    plugin_name: str,
    cmd_name: str,
    cmd_path: str,
    description: str,
    arg_hint: str,
    skills: list[str],
    agents: list[str],
) -> str:
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
    lines = ['description = "' + escape_toml_string(description) + '"', 'prompt = """']
    lines.append(escape_toml_prompt(prompt))
    lines.append('"""')
    lines.append("")
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Gemini CLI TOML commands.")
    parser.add_argument("--plugin", help="Only sync commands for the specified plugin.")
    parser.add_argument("--prune", action="store_true", help="Delete TOMLs that no longer have a source .md file.")
    args = parser.parse_args()

    created = 0
    deleted = 0
    errors: list[str] = []

    if args.plugin:
        plugins = [args.plugin]
        if not os.path.isdir(os.path.join(PLUGINS_DIR, args.plugin)):
            print(f"Error: Plugin directory not found: {args.plugin}", file=sys.stderr)
            sys.exit(1)
    else:
        plugins = sorted(
            p for p in os.listdir(PLUGINS_DIR)
            if os.path.isdir(os.path.join(PLUGINS_DIR, p))
        )

    # ── Pruning ─────────────────────────────────────────────────────────────
    if args.prune and os.path.isdir(COMMANDS_OUT):
        for root, dirs, files in os.walk(COMMANDS_OUT):
            for f in files:
                if not f.endswith(".toml"):
                    continue
                
                toml_path = os.path.join(root, f)
                rel_to_out = os.path.relpath(toml_path, COMMANDS_OUT)
                
                # Check top-level plugin toml
                if "/" not in rel_to_out:
                    plugin_name = f.removesuffix(".toml")
                    source_dir = os.path.join(PLUGINS_DIR, plugin_name)
                    if not os.path.isdir(source_dir):
                        os.remove(toml_path)
                        deleted += 1
                        print(f"  pruned commands/{f}")
                else:
                    # Check sub-command toml
                    parts = rel_to_out.split("/")
                    plugin_name = parts[0]
                    cmd_name = parts[1].removesuffix(".toml")
                    source_md = os.path.join(PLUGINS_DIR, plugin_name, "commands", f"{cmd_name}.md")
                    if not os.path.isfile(source_md):
                        os.remove(toml_path)
                        deleted += 1
                        print(f"  pruned commands/{rel_to_out}")

    # ── Generation/Sync ─────────────────────────────────────────────────────
    for plugin_name in plugins:
        plugin_dir = os.path.join(PLUGINS_DIR, plugin_name)
        
        agents = agent_names(plugin_dir)
        skills = skill_names(plugin_dir)
        
        # ── Generate plugin entry point ──────────────────────────────────────
        meta = read_plugin_json(plugin_dir)
        plugin_desc = meta.get("description") or f"{plugin_name.replace('-', ' ').title()} plugin"
        
        entry_prompt = build_entry_prompt(plugin_name, plugin_desc, skills, agents)
        entry_toml = generate_toml(plugin_desc, entry_prompt)
        
        os.makedirs(COMMANDS_OUT, exist_ok=True)
        entry_path = os.path.join(COMMANDS_OUT, plugin_name + ".toml")
        try:
            with open(entry_path, "w", encoding="utf-8") as f:
                f.write(entry_toml)
            created += 1
            print(f"  wrote commands/{plugin_name}.toml")
        except OSError as e:
            errors.append(f"{plugin_name} entry: {e}")

        # ── Generate sub-commands ────────────────────────────────────────────
        cmds_dir = os.path.join(plugin_dir, "commands")
        if not os.path.isdir(cmds_dir):
            continue

        cmd_files = sorted(f for f in os.listdir(cmds_dir) if f.endswith(".md"))
        if not cmd_files:
            continue

        out_dir = os.path.join(COMMANDS_OUT, plugin_name)
        os.makedirs(out_dir, exist_ok=True)

        for cmd_file in cmd_files:
            cmd_name = cmd_file.removesuffix(".md")
            cmd_rel_path = f"plugins/{plugin_name}/commands/{cmd_file}"
            content = read_file(os.path.join(cmds_dir, cmd_file))
            fm, body = parse_frontmatter(content)

            description = (
                (fm.get("description") or "").strip()
                or h1_from_body(body)
                or cmd_name.replace("-", " ").title()
            )
            arg_hint = (fm.get("argument-hint") or "").strip()

            prompt = build_prompt(plugin_name, cmd_name, cmd_rel_path, description, arg_hint, skills, agents)
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

    print(f"\nDone: {created} TOML commands synced, {deleted} pruned, {len(errors)} errors")
    if errors:
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
