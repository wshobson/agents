#!/usr/bin/env python3
"""Doc-gardener — recurring drift detection across the repo.

Per the OpenAI harness engineering pattern, a recurring task scans for:
1. Generated artifacts whose source file is newer (regenerate needed)
2. Context files (AGENTS.md, GEMINI.md, CLAUDE.md) above ~150 lines
3. Dead links from docs/ into plugins/ or other docs/
4. Skills above 8 KB body without `references/` (Codex hard cap)
5. Plugin entries in marketplace.json without a corresponding plugins/<name>/ directory
6. Plugins missing from marketplace.json

Each finding ships with a `Fix:` remediation line.

Usage:
    python tools/doc_gardener.py
    python tools/doc_gardener.py --strict   # exit nonzero on any finding
    python tools/doc_gardener.py --check <kind>   # only run one check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.adapters.base import WORKTREE, list_plugins, parse_frontmatter

PLUGINS_DIR = WORKTREE / "plugins"
DOCS_DIR = WORKTREE / "docs"
MARKETPLACE_JSON = WORKTREE / ".claude-plugin" / "marketplace.json"

CONTEXT_FILES = {
    "AGENTS.md": 150,
    "GEMINI.md": 150,
    "CLAUDE.md": 200,  # slightly larger since it documents the source-of-truth
}

CODEX_SKILL_CAP_BYTES = 8 * 1024


# ── Findings ─────────────────────────────────────────────────────────────────


@dataclass
class Finding:
    kind: str
    severity: str  # 'info' | 'warning' | 'error'
    path: Path
    message: str
    fix: str

    def render(self) -> str:
        try:
            rel = self.path.relative_to(WORKTREE)
        except ValueError:
            rel = self.path
        return (
            f"[{self.severity:7}] {self.kind:24} {rel}: {self.message}\n           Fix: {self.fix}"
        )


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, **kwargs) -> None:
        self.findings.append(Finding(**kwargs))

    def by_severity(self, severity: str) -> list[Finding]:
        return [f for f in self.findings if f.severity == severity]


# ── Checks ───────────────────────────────────────────────────────────────────


def check_stale_artifacts(report: Report) -> None:
    """Detect generated artifacts whose source mtime > artifact mtime.

    For each adapter output directory, walk and check.
    """
    # Map of (source path resolver, generated path glob)
    pairs: list[tuple[Path, Path]] = []

    # Codex agent TOMLs map to plugins/<plugin>/agents/<name>.md
    codex_agents = WORKTREE / ".codex" / "agents"
    if codex_agents.is_dir():
        for toml_path in codex_agents.glob("*.toml"):
            name = toml_path.stem  # "<plugin>__<agent>"
            if "__" in name:
                plugin, agent = name.split("__", 1)
                src = PLUGINS_DIR / plugin / "agents" / f"{agent}.md"
                if src.is_file():
                    pairs.append((src, toml_path))

    # Codex skills (only the head SKILL.md; if source changed, references/ would
    # also be stale, but the head is the canonical indicator).
    # The Codex adapter synthesizes a skill from each command (codex.py
    # _emit_command_as_skill), so the source can be EITHER:
    #   plugins/<plugin>/skills/<leaf>/SKILL.md   (real skill)
    #   plugins/<plugin>/commands/<leaf>.md       (command-as-skill)
    # When the two collide, the command-skill is suffixed with __command.
    codex_skills = WORKTREE / ".codex" / "skills"
    if codex_skills.is_dir():
        for skill_md in codex_skills.glob("*/SKILL.md"):
            name = skill_md.parent.name
            if "__" not in name:
                continue
            plugin, leaf = name.split("__", 1)
            # Preference order:
            # 1. Real skill at plugins/<p>/skills/<leaf>/SKILL.md (handles the case where
            #    leaf is literally `<x>__command` — a legitimately-named skill).
            # 2. If leaf ends with `__command` AND no real skill exists, treat as the
            #    command-collision suffix and look in commands/.
            # 3. Otherwise fall through to commands/<leaf>.md (basic command-as-skill).
            real_skill_src = PLUGINS_DIR / plugin / "skills" / leaf / "SKILL.md"
            if real_skill_src.is_file():
                pairs.append((real_skill_src, skill_md))
                continue
            if leaf.endswith("__command"):
                src = PLUGINS_DIR / plugin / "commands" / f"{leaf[: -len('__command')]}.md"
            elif leaf.endswith("__cmd"):
                # Second-order collision suffix
                src = PLUGINS_DIR / plugin / "commands" / f"{leaf[: -len('__cmd')]}.md"
            else:
                src = PLUGINS_DIR / plugin / "commands" / f"{leaf}.md"
            if src.is_file():
                pairs.append((src, skill_md))

    # OpenCode agents
    opencode_agents = WORKTREE / ".opencode" / "agents"
    if opencode_agents.is_dir():
        for md in opencode_agents.glob("*.md"):
            name = md.stem
            if "__" in name:
                plugin, agent = name.split("__", 1)
                src = PLUGINS_DIR / plugin / "agents" / f"{agent}.md"
                if src.is_file():
                    pairs.append((src, md))

    # OpenCode commands (.opencode/commands/<plugin>__<cmd>.md -> plugins/<p>/commands/<cmd>.md)
    opencode_commands = WORKTREE / ".opencode" / "commands"
    if opencode_commands.is_dir():
        for md in opencode_commands.glob("*.md"):
            name = md.stem
            if "__" in name:
                plugin, cmd = name.split("__", 1)
                src = PLUGINS_DIR / plugin / "commands" / f"{cmd}.md"
                if src.is_file():
                    pairs.append((src, md))

    # OpenCode skills (.opencode/skills/<plugin>-<skill>/SKILL.md)
    opencode_skills = WORKTREE / ".opencode" / "skills"
    if opencode_skills.is_dir():
        skill_sources: dict[str, Path] = {}
        if PLUGINS_DIR.is_dir():
            for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
                if not plugin_dir.is_dir():
                    continue
                for skill_file in sorted((plugin_dir / "skills").glob("*/SKILL.md")):
                    skill_id = f"{plugin_dir.name}-{skill_file.parent.name}"
                    existing = skill_sources.get(skill_id)
                    if existing and existing != skill_file:
                        report.add(
                            kind="opencode-skill-id-collision",
                            severity="error",
                            path=skill_file,
                            message=(
                                f"OpenCode skill id `{skill_id}` also maps to "
                                f"{existing.relative_to(WORKTREE)}"
                            ),
                            fix="Rename the plugin or skill so OpenCode's hyphenated skill id is unique.",
                        )
                        continue
                    skill_sources[skill_id] = skill_file
        for skill_md in opencode_skills.glob("*/SKILL.md"):
            src = skill_sources.get(skill_md.parent.name)
            if src and src.is_file():
                pairs.append((src, skill_md))

    # Gemini skills and agents at root
    for top_dir in ("skills", "agents"):
        root = WORKTREE / top_dir
        if root.is_dir():
            pattern = "*/SKILL.md" if top_dir == "skills" else "*.md"
            for gen in root.glob(pattern):
                name = gen.parent.name if top_dir == "skills" else gen.stem
                if "__" in name:
                    plugin, leaf = name.split("__", 1)
                    if top_dir == "skills":
                        src = PLUGINS_DIR / plugin / "skills" / leaf / "SKILL.md"
                    else:
                        src = PLUGINS_DIR / plugin / "agents" / f"{leaf}.md"
                    if src.is_file():
                        pairs.append((src, gen))

    # Gemini commands at commands/<plugin>/<cmd>.toml -> plugins/<plugin>/commands/<cmd>.md
    gemini_commands = WORKTREE / "commands"
    if gemini_commands.is_dir():
        for toml_path in gemini_commands.rglob("*.toml"):
            # Top-level commands/<plugin>.toml maps to the plugin's plugin.json
            if toml_path.parent == gemini_commands:
                plugin = toml_path.stem
                src = PLUGINS_DIR / plugin / ".claude-plugin" / "plugin.json"
                if src.is_file():
                    pairs.append((src, toml_path))
            else:
                plugin = toml_path.parent.name
                cmd = toml_path.stem
                src = PLUGINS_DIR / plugin / "commands" / f"{cmd}.md"
                if src.is_file():
                    pairs.append((src, toml_path))

    # Copilot agents (.agent.md) and skills (SKILL.md) at .copilot/
    copilot_root = WORKTREE / ".copilot"
    copilot_agents = copilot_root / "agents"
    if copilot_agents.is_dir():
        for agent_md in copilot_agents.glob("*.agent.md"):
            name = agent_md.stem
            if name.endswith(".agent"):
                name = name[: -len(".agent")]
            if "__" in name:
                plugin, agent = name.split("__", 1)
                src = PLUGINS_DIR / plugin / "agents" / f"{agent}.md"
                if src.is_file():
                    pairs.append((src, agent_md))

    copilot_skills = copilot_root / "skills"
    if copilot_skills.is_dir():
        for skill_md in copilot_skills.glob("*/SKILL.md"):
            name = skill_md.parent.name
            if "__" in name:
                plugin, leaf = name.split("__", 1)
                src = PLUGINS_DIR / plugin / "skills" / leaf / "SKILL.md"
                if src.is_file():
                    pairs.append((src, skill_md))

    for src, gen in pairs:
        if src.stat().st_mtime > gen.stat().st_mtime + 1:  # 1s grace
            # Derive the plugin name correctly regardless of source layout.
            # All adapter sources live under `plugins/<plugin>/...` — index 1 of parts
            # relative to PLUGINS_DIR is always the plugin name.
            try:
                plugin_name = src.relative_to(PLUGINS_DIR).parts[0]
            except (ValueError, IndexError):
                plugin_name = "<plugin>"
            report.add(
                kind="STALE_ARTIFACT",
                severity="info",
                path=gen,
                message=f"source {src.relative_to(WORKTREE)} is newer",
                fix=f"Run `make generate HARNESS=<harness> PLUGIN={plugin_name}`.",
            )


def check_oversized_context_files(report: Report) -> None:
    for name, cap in CONTEXT_FILES.items():
        path = WORKTREE / name
        if not path.is_file():
            continue
        line_count = len(path.read_text().splitlines())
        if line_count > cap:
            report.add(
                kind="CONTEXT_FILE_OVERSIZED",
                severity="warning",
                path=path,
                message=f"{line_count} lines (cap: {cap})",
                fix="Move detail into docs/ — context files should be table-of-contents only.",
            )


def check_dead_links(report: Report) -> None:
    """Find markdown links from docs/ and top-level guides that point at missing files."""
    targets = [DOCS_DIR] if DOCS_DIR.is_dir() else []
    for top_file in (
        "README.md",
        "CLAUDE.md",
        "AGENTS.md",
        "GEMINI.md",
    ):
        p = WORKTREE / top_file
        if p.is_file():
            targets.append(p)

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)#]+)\)")

    for target in targets:
        files = list(target.rglob("*.md")) if target.is_dir() else [target]
        for md in files:
            try:
                content = md.read_text()
            except OSError:
                continue
            for link in link_pattern.findall(content):
                # Skip external links and anchors
                if link.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                link_path = (md.parent / link).resolve()
                if not link_path.exists():
                    report.add(
                        kind="DEAD_LINK",
                        severity="error",
                        path=md,
                        message=f"link to `{link}` does not resolve",
                        fix="Update the link target, or create the missing file. If the link points into generated output (`.codex/`, `.opencode/`, etc.), the generated tree may need to be regenerated.",
                    )


def check_codex_skill_caps(report: Report) -> None:
    """Skills whose source body exceeds Codex's 8 KB cap and have no references/."""
    if not PLUGINS_DIR.is_dir():
        return
    for skill_md in PLUGINS_DIR.glob("*/skills/*/SKILL.md"):
        content = skill_md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        body_bytes = len(body.encode("utf-8"))
        if body_bytes > CODEX_SKILL_CAP_BYTES:
            refs = skill_md.parent / "references"
            if not refs.is_dir():
                report.add(
                    kind="SKILL_OVER_CODEX_CAP",
                    severity="warning",
                    path=skill_md,
                    message=f"body is {body_bytes} bytes (Codex hard cap: {CODEX_SKILL_CAP_BYTES})",
                    fix="Move detail sections into `references/details.md` and leave SKILL.md as navigation.",
                )


def check_marketplace_consistency(report: Report) -> None:
    if not MARKETPLACE_JSON.is_file():
        return
    try:
        data = json.loads(MARKETPLACE_JSON.read_text())
    except json.JSONDecodeError as e:
        report.add(
            kind="MARKETPLACE_PARSE",
            severity="error",
            path=MARKETPLACE_JSON,
            message=f"JSON parse error: {e}",
            fix="Fix the JSON syntax — likely an unterminated string or missing comma.",
        )
        return

    # Distinguish local entries from external (git-subdir, git, etc.). Only flag
    # missing LOCAL entries as orphans — externals legitimately don't have a plugins/<name>/.
    local_entries: dict[str, dict] = {}
    external_names: set[str] = set()
    for entry in data.get("plugins", []):
        name = entry.get("name")
        if not name:
            continue
        source = entry.get("source")
        if isinstance(source, dict):
            # git-subdir, git, etc. — external
            external_names.add(name)
        elif isinstance(source, str) and source.startswith("./plugins/"):
            local_entries[name] = entry

    listed_local = set(local_entries.keys())
    actual = set(list_plugins())

    for name in sorted(listed_local - actual):
        report.add(
            kind="MARKETPLACE_ORPHAN",
            severity="error",
            path=MARKETPLACE_JSON,
            message=f"plugin `{name}` listed in marketplace.json with local source but plugins/{name}/ missing",
            fix=f"Either remove the entry or create plugins/{name}/.",
        )
    listed_all = listed_local | external_names
    for name in sorted(actual - listed_all):
        # External git-subdir plugins (like the existing `codex` external plugin) may
        # not be in our marketplace.json — that's expected. Only flag if it has a
        # local .claude-plugin/plugin.json.
        if (PLUGINS_DIR / name / ".claude-plugin" / "plugin.json").is_file():
            report.add(
                kind="MARKETPLACE_MISSING",
                severity="info",
                path=MARKETPLACE_JSON,
                message=f"plugins/{name}/ exists but is not in marketplace.json",
                fix=f"Add a plugins[] entry for `{name}` (or leave it as draft / external).",
            )


CHECKS = {
    "stale": check_stale_artifacts,
    "context": check_oversized_context_files,
    "links": check_dead_links,
    "codex-cap": check_codex_skill_caps,
    "marketplace": check_marketplace_consistency,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Recurring drift detection (doc-gardener).")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero on any finding.")
    parser.add_argument(
        "--check",
        choices=list(CHECKS.keys()),
        action="append",
        help="Run only the named check (repeat for multiple). Default: all.",
    )
    parser.add_argument("--quiet", action="store_true", help="Only print findings, no summary.")
    args = parser.parse_args()

    selected = args.check or list(CHECKS.keys())
    report = Report()
    for name in selected:
        CHECKS[name](report)

    if not report.findings:
        if not args.quiet:
            print(f"OK: garden is clean ({len(selected)} check(s) ran).")
        return 0

    # Sort by (severity priority, kind, path) so errors lead and similar findings group.
    severity_order = {"error": 0, "warning": 1, "info": 2}
    sorted_findings = sorted(
        report.findings,
        key=lambda f: (severity_order.get(f.severity, 9), f.kind, str(f.path)),
    )

    # Print a per-kind summary up front so triage is one scroll.
    if not args.quiet:
        from collections import Counter

        kind_counts = Counter((f.severity, f.kind) for f in report.findings)
        if kind_counts:
            print("Summary:")
            for (severity, kind), count in sorted(
                kind_counts.items(),
                key=lambda x: (severity_order.get(x[0][0], 9), -x[1]),
            ):
                print(f"  [{severity:7}] {kind:24} {count}")
            print()

    for f in sorted_findings:
        print(f.render())

    if not args.quiet:
        errors = report.by_severity("error")
        warnings = report.by_severity("warning")
        infos = report.by_severity("info")
        print()
        print(f"Totals: {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info.")

    if report.by_severity("error"):
        return 1
    if args.strict and (report.by_severity("warning") or report.by_severity("info")):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
