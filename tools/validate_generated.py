#!/usr/bin/env python3
"""Structural validation of generated harness artifacts.

Approximates harness round-trip without installing each CLI. For every adapter output,
parse and validate against documented schemas. Surface issues with file paths and
remediation hints (OpenAI harness-engineering: lint errors carry their fix).

Usage:
    python tools/validate_generated.py                # validate all four
    python tools/validate_generated.py --harness codex
    python tools/validate_generated.py --strict       # exit nonzero if any warning
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

# Allow `python tools/validate_generated.py` from repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.adapters.base import WORKTREE, parse_frontmatter
from tools.adapters.capabilities import supported_harnesses

# ── Findings ─────────────────────────────────────────────────────────────────


@dataclass
class Finding:
    severity: str  # 'error' | 'warning' | 'info'
    harness: str
    path: Path
    message: str
    remediation: str = ""

    def render(self) -> str:
        rel = self.path.relative_to(WORKTREE) if self.path.is_relative_to(WORKTREE) else self.path
        tail = f"\n    fix: {self.remediation}" if self.remediation else ""
        return f"[{self.severity}] {self.harness}: {rel}: {self.message}{tail}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, **kwargs) -> None:
        self.findings.append(Finding(**kwargs))

    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]

    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "info"]


# ── Helpers ──────────────────────────────────────────────────────────────────


def _check_nonempty_str_field(
    report: Report,
    fm: dict,
    field: str,
    harness: str,
    path: Path,
    label: str = "",
) -> bool:
    """Validate that `field` exists in `fm`, is a str, and is non-empty.

    Adds one Finding per violation. Returns True if the field passes all checks.
    ``label`` is only used in remediation hints (defaults to ``field``).
    """
    label = label or field
    if field not in fm:
        report.add(
            severity="error",
            harness=harness,
            path=path,
            message=f"missing required `{field}` field in frontmatter",
            remediation=f"Each {harness} {label} needs a `{field}`.",
        )
        return False
    if not isinstance(fm[field], str):
        report.add(
            severity="error",
            harness=harness,
            path=path,
            message=f"`{field}` field must be a string",
            remediation=f"Set `{field}` to a plain string in the {label} frontmatter.",
        )
        return False
    if not fm[field].strip():
        report.add(
            severity="error",
            harness=harness,
            path=path,
            message=f"`{field}` field is empty",
            remediation=f"Provide a non-empty `{field}` in the {label} frontmatter.",
        )
        return False
    return True


# ── Codex validators ─────────────────────────────────────────────────────────


def validate_codex(report: Report) -> None:
    root = WORKTREE / ".codex"
    if not root.is_dir():
        return  # nothing generated yet

    # 1. Every agent .toml parses and has required fields.
    required_agent_fields = {"name", "description", "developer_instructions"}
    for toml_path in (root / "agents").glob("*.toml") if (root / "agents").is_dir() else []:
        try:
            data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as e:
            report.add(
                severity="error",
                harness="codex",
                path=toml_path,
                message=f"TOML parse error: {e}",
                remediation="Regenerate via `make generate HARNESS=codex PLUGIN=<name>`.",
            )
            continue
        missing = required_agent_fields - set(data.keys())
        if missing:
            report.add(
                severity="error",
                harness="codex",
                path=toml_path,
                message=f"missing required TOML fields: {sorted(missing)}",
                remediation="The source agent markdown is missing fields. Check `description:` in frontmatter.",
            )
        if "sandbox_mode" in data and data["sandbox_mode"] not in {
            "read-only",
            "workspace-write",
            "danger-full-access",
        }:
            report.add(
                severity="error",
                harness="codex",
                path=toml_path,
                message=f"invalid sandbox_mode: {data['sandbox_mode']!r}",
                remediation="Must be one of: read-only, workspace-write, danger-full-access.",
            )

    # 2. Every skill SKILL.md has valid frontmatter + name matches directory.
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        for skill_md in skills_dir.glob("*/SKILL.md"):
            content = skill_md.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(content)
            if not fm:
                report.add(
                    severity="error",
                    harness="codex",
                    path=skill_md,
                    message="missing or invalid frontmatter",
                    remediation="SKILL.md must start with `---\\nname: ...\\ndescription: ...\\n---`.",
                )
                continue
            if fm.get("name") != skill_md.parent.name:
                report.add(
                    severity="error",
                    harness="codex",
                    path=skill_md,
                    message=f"frontmatter name {fm.get('name')!r} != directory name {skill_md.parent.name!r}",
                    remediation="Codex requires the name field to match the skill directory exactly.",
                )
            if not fm.get("description"):
                report.add(
                    severity="error",
                    harness="codex",
                    path=skill_md,
                    message="empty description in frontmatter",
                    remediation="Add a description with a trigger phrase (e.g. 'Use when ...').",
                )
            # Body cap — entire file ≤ 8 KB (the cap Codex hardcodes).
            # Promoted to error: at runtime Codex hard-truncates anything past the cap,
            # silently breaking the skill. The fix is mechanical (extract sections to
            # references/) and the false-positive risk is zero.
            file_bytes = len(content.encode("utf-8"))
            if file_bytes > 8 * 1024:
                report.add(
                    severity="error",
                    harness="codex",
                    path=skill_md,
                    message=f"file size {file_bytes} B exceeds Codex 8192 B injection cap",
                    remediation="Push detail into references/details.md and shorten the SKILL.md body or description.",
                )

    # 3. AGENTS.md exists and is ≤ 150 lines.
    agents_md = WORKTREE / "AGENTS.md"
    if not agents_md.is_file():
        report.add(
            severity="warning",
            harness="codex",
            path=agents_md,
            message="AGENTS.md not generated",
            remediation="Run `make generate HARNESS=codex --all` (or include a global pass).",
        )
    else:
        line_count = len(agents_md.read_text().splitlines())
        if line_count > 150:
            report.add(
                severity="warning",
                harness="codex",
                path=agents_md,
                message=f"AGENTS.md is {line_count} lines (cap: 150 — table-of-contents pattern)",
                remediation="Move detail into docs/; keep AGENTS.md as a navigation index.",
            )


# ── Cursor validators ────────────────────────────────────────────────────────


_ALLOWED_MDC_KEYS = {"description", "globs", "alwaysApply"}


def validate_cursor(report: Report) -> None:
    root = WORKTREE / ".cursor-plugin"
    if not root.is_dir():
        return

    # 1. marketplace.json shape
    marketplace = root / "marketplace.json"
    if marketplace.is_file():
        try:
            data = json.loads(marketplace.read_text())
        except json.JSONDecodeError as e:
            report.add(
                severity="error",
                harness="cursor",
                path=marketplace,
                message=f"JSON parse error: {e}",
                remediation="Regenerate via `make generate HARNESS=cursor --all`.",
            )
            return
        if "owner" not in data:
            report.add(
                severity="error",
                harness="cursor",
                path=marketplace,
                message="marketplace.json missing required `owner` field",
                remediation="Cursor 2.5+ requires owner.name in marketplace.json.",
            )
        for entry in data.get("plugins", []):
            if "source" not in entry:
                report.add(
                    severity="error",
                    harness="cursor",
                    path=marketplace,
                    message=f"plugin entry {entry.get('name', '<unnamed>')} missing `source`",
                    remediation="Cursor uses `source` (not `path` or `url`) per plugin entry.",
                )

    # 2. Each per-plugin manifest parses
    plugins_dir = root / "plugins"
    if plugins_dir.is_dir():
        for manifest in plugins_dir.glob("*.json"):
            try:
                data = json.loads(manifest.read_text())
            except json.JSONDecodeError as e:
                report.add(
                    severity="error",
                    harness="cursor",
                    path=manifest,
                    message=f"JSON parse error: {e}",
                    remediation="Regenerate via `make generate HARNESS=cursor`.",
                )
                continue
            if "name" not in data:
                report.add(
                    severity="error",
                    harness="cursor",
                    path=manifest,
                    message="missing required `name` field",
                    remediation="Every Cursor plugin.json needs a name.",
                )

    # 3. .cursor/rules/*.mdc — only the three allowed frontmatter keys
    rules_dir = WORKTREE / ".cursor" / "rules"
    if rules_dir.is_dir():
        for mdc in rules_dir.glob("*.mdc"):
            content = mdc.read_text()
            fm, _ = parse_frontmatter(content)
            if not fm:
                report.add(
                    severity="error",
                    harness="cursor",
                    path=mdc,
                    message="missing or invalid frontmatter",
                    remediation="MDC files need YAML frontmatter with at least `description:`.",
                )
                continue
            invalid = set(fm.keys()) - _ALLOWED_MDC_KEYS
            if invalid:
                report.add(
                    severity="error",
                    harness="cursor",
                    path=mdc,
                    message=f"invalid MDC keys: {sorted(invalid)}",
                    remediation=(
                        "Cursor only supports description/globs/alwaysApply. "
                        "Keys like agentRequested:, mode:, tags: are folklore."
                    ),
                )


# ── OpenCode validators ──────────────────────────────────────────────────────


_OPENCODE_PERMISSION_KEYS = {
    "read",
    "edit",
    "write",
    "bash",
    "grep",
    "glob",
    "list",
    "task",
    "skill",
    "lsp",
    "webfetch",
    "websearch",
    "external_directory",
    "todowrite",
    "question",
    "doom_loop",
}
_OPENCODE_PERMISSION_VALUES = {"allow", "ask", "deny"}
_OPENCODE_MODES = {"primary", "subagent", "all"}
_OPENCODE_SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_OPENCODE_SKILL_NAME_MAX = 64


def _extract_permission_block(raw: str) -> dict | None:
    """Pull the top-level `permission:` block out of raw frontmatter text and return its
    key→value mapping. Returns None if no top-level `permission:` block is found.

    We hand-roll this because `parse_frontmatter` collapses nested mappings into a list
    of strings, losing key→value structure. Validating from raw text catches the
    real-shape permission blocks the OpenCode adapter emits.

    Only matches `permission:` at column 0 — a nested `  permission:` (e.g. inside a
    `metadata:` block) is correctly ignored.
    """
    if not raw.startswith("---"):
        return None
    end = raw.find("\n---", 3)
    if end == -1:
        return None
    fm_text = raw[3:end]
    lines = fm_text.splitlines()
    block: dict[str, str] = {}
    in_perm = False
    for line in lines:
        # Top-level (column-0) `permission:` is the only one we recognize.
        if line.rstrip() == "permission:" and not line.startswith((" ", "\t")):
            in_perm = True
            continue
        if in_perm:
            # Continuation if line is indented; otherwise we've left the block.
            if line.startswith(("  ", "\t")) and ":" in line:
                k, _, v = line.strip().partition(":")
                block[k.strip()] = v.strip()
            elif line.strip() == "":
                continue
            else:
                in_perm = False
    return block if block else None


def validate_opencode(report: Report) -> None:
    root = WORKTREE / ".opencode"
    if not root.is_dir():
        return

    # 1. opencode.json
    cfg = WORKTREE / "opencode.json"
    if cfg.is_file():
        try:
            data = json.loads(cfg.read_text())
        except json.JSONDecodeError as e:
            report.add(
                severity="error",
                harness="opencode",
                path=cfg,
                message=f"JSON parse error: {e}",
                remediation="Regenerate via `make generate HARNESS=opencode`.",
            )
        else:
            if "$schema" not in data:
                report.add(
                    severity="info",
                    harness="opencode",
                    path=cfg,
                    message="missing $schema reference",
                    remediation='Add "$schema": "https://opencode.ai/config.json" for editor tooling.',
                )

    # 2. Every agent .md has required frontmatter
    agents_dir = root / "agents"
    if agents_dir.is_dir():
        for agent_md in agents_dir.glob("*.md"):
            content = agent_md.read_text()
            fm, _ = parse_frontmatter(content)
            if not fm:
                report.add(
                    severity="error",
                    harness="opencode",
                    path=agent_md,
                    message="missing or invalid frontmatter",
                    remediation="Regenerate via `make generate HARNESS=opencode`.",
                )
                continue
            if fm.get("mode") not in _OPENCODE_MODES:
                report.add(
                    severity="error",
                    harness="opencode",
                    path=agent_md,
                    message=f"mode {fm.get('mode')!r} not in {sorted(_OPENCODE_MODES)}",
                    remediation="Set mode: subagent on transpiled agents.",
                )
            model = fm.get("model", "")
            if model and "/" not in model:
                report.add(
                    severity="warning",
                    harness="opencode",
                    path=agent_md,
                    message=f"model {model!r} is not provider-prefixed (e.g. 'anthropic/claude-...')",
                    remediation="OpenCode requires `provider/model-id`; check MODEL_ALIASES in capabilities.py.",
                )

            # Validate the permission block by re-parsing raw frontmatter — `fm` from
            # parse_frontmatter flattens nested mappings into lists, losing structure.
            perm = _extract_permission_block(content)
            if perm:
                unknown_keys = set(perm.keys()) - _OPENCODE_PERMISSION_KEYS
                if unknown_keys:
                    report.add(
                        severity="error",
                        harness="opencode",
                        path=agent_md,
                        message=f"unknown permission keys: {sorted(unknown_keys)}",
                        remediation=(
                            f"Valid keys: {sorted(_OPENCODE_PERMISSION_KEYS)}. "
                            "Update _OPENCODE_PERMISSIONS in tools/adapters/opencode.py if a new key was added."
                        ),
                    )
                for k, v in perm.items():
                    if v not in _OPENCODE_PERMISSION_VALUES:
                        report.add(
                            severity="error",
                            harness="opencode",
                            path=agent_md,
                            message=f"permission.{k} = {v!r} not in {sorted(_OPENCODE_PERMISSION_VALUES)}",
                            remediation="Values must be allow/ask/deny.",
                        )

    # 3. Every skill has OpenCode-valid frontmatter with name matching directory.
    skills_dir = root / "skills"
    if skills_dir.is_dir():
        for skill_md in skills_dir.glob("*/SKILL.md"):
            content = skill_md.read_text()
            fm, _ = parse_frontmatter(content)
            if not fm:
                report.add(
                    severity="error",
                    harness="opencode",
                    path=skill_md,
                    message="missing or invalid frontmatter",
                    remediation="Regenerate via `make generate HARNESS=opencode`.",
                )
                continue

            name = str(fm.get("name") or "")
            if name != skill_md.parent.name:
                report.add(
                    severity="error",
                    harness="opencode",
                    path=skill_md,
                    message=f"frontmatter name {name!r} != directory {skill_md.parent.name!r}",
                    remediation="OpenCode skill names must match their directory.",
                )
            if not _OPENCODE_SKILL_NAME_RE.fullmatch(name):
                report.add(
                    severity="error",
                    harness="opencode",
                    path=skill_md,
                    message=f"skill name {name!r} is not OpenCode-safe",
                    remediation="Use lowercase alphanumeric names with single hyphen separators.",
                )
            if len(name) > _OPENCODE_SKILL_NAME_MAX:
                report.add(
                    severity="error",
                    harness="opencode",
                    path=skill_md,
                    message=(
                        f"skill name {name!r} is {len(name)} chars; "
                        f"limit is {_OPENCODE_SKILL_NAME_MAX}"
                    ),
                    remediation="Shorten the plugin or skill name before generating OpenCode skills.",
                )
            if not str(fm.get("description") or "").strip():
                report.add(
                    severity="error",
                    harness="opencode",
                    path=skill_md,
                    message="empty description in frontmatter",
                    remediation="OpenCode skills require a description.",
                )


# ── Gemini validators ────────────────────────────────────────────────────────


def validate_gemini(report: Report) -> None:
    skills_dir = WORKTREE / "skills"
    agents_dir = WORKTREE / "agents"
    commands_dir = WORKTREE / "commands"

    # 1. Every TOML command parses + has description + prompt
    if commands_dir.is_dir():
        for toml_path in commands_dir.rglob("*.toml"):
            try:
                data = tomllib.loads(toml_path.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as e:
                report.add(
                    severity="error",
                    harness="gemini",
                    path=toml_path,
                    message=f"TOML parse error: {e}",
                    remediation="Likely a quoting issue in the command body. Regenerate or escape triple-quotes.",
                )
                continue
            if "description" not in data or "prompt" not in data:
                report.add(
                    severity="error",
                    harness="gemini",
                    path=toml_path,
                    message=f"missing keys (have: {sorted(data.keys())})",
                    remediation="Gemini TOML requires both `description` and `prompt`.",
                )
            if "prompt" in data and "{{args}}" not in data["prompt"]:
                report.add(
                    severity="warning",
                    harness="gemini",
                    path=toml_path,
                    message="prompt does not include {{args}} placeholder",
                    remediation="Append {{args}} so user input is appended to the prompt.",
                )

    # 2. Every native skill has frontmatter name matching directory
    if skills_dir.is_dir():
        for skill_md in skills_dir.glob("*/SKILL.md"):
            content = skill_md.read_text()
            fm, _ = parse_frontmatter(content)
            if fm.get("name") != skill_md.parent.name:
                report.add(
                    severity="error",
                    harness="gemini",
                    path=skill_md,
                    message=f"frontmatter name {fm.get('name')!r} != directory {skill_md.parent.name!r}",
                    remediation="Gemini auto-discovers by directory; name must match.",
                )

    # 3. Subagents have a Gemini-compatible model
    if agents_dir.is_dir():
        valid_model_prefixes = ("gemini-",)
        for agent_md in agents_dir.glob("*.md"):
            fm, _ = parse_frontmatter(agent_md.read_text())
            model = fm.get("model", "")
            if model and not model.startswith(valid_model_prefixes):
                report.add(
                    severity="warning",
                    harness="gemini",
                    path=agent_md,
                    message=f"model {model!r} doesn't look like a Gemini model id",
                    remediation="Gemini wants names like 'gemini-2.5-pro' / 'gemini-2.5-flash'.",
                )

    # 4. GEMINI.md size
    gemini_md = WORKTREE / "GEMINI.md"
    if gemini_md.is_file():
        line_count = len(gemini_md.read_text().splitlines())
        if line_count > 150:
            report.add(
                severity="warning",
                harness="gemini",
                path=gemini_md,
                message=f"GEMINI.md is {line_count} lines (cap: 150 — table of contents pattern)",
                remediation="Move detail to docs/.",
            )


# ── Driver ───────────────────────────────────────────────────────────────────


def validate_copilot(report: Report) -> None:
    """Validate Copilot agent, skill, and command markdown files under WORKTREE/.copilot.

    Checks that generated agent, skill, and command markdown files have valid
    frontmatter and the minimum metadata Copilot needs to discover them.
    """
    candidate_roots = [WORKTREE / ".copilot"]
    found_any = False
    for root in candidate_roots:
        agents_dir = root / "agents"
        if not agents_dir.is_dir():
            continue
        found_any = True
        for agent_md in agents_dir.glob("*.agent.md"):
            content = agent_md.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(content)
            if not fm:
                report.add(
                    severity="error",
                    harness="copilot",
                    path=agent_md,
                    message="missing or invalid frontmatter",
                    remediation="Regenerate via `make generate HARNESS=copilot`.",
                )
                continue
            _check_nonempty_str_field(report, fm, "name", "copilot", agent_md, label="agent")
            _check_nonempty_str_field(report, fm, "description", "copilot", agent_md, label="agent")
    # 3. Skills: validate .copilot/skills/*/SKILL.md exists and has valid frontmatter.
    skills_dir = WORKTREE / ".copilot" / "skills"
    if skills_dir.is_dir():
        found_any = True
        for skill_md in skills_dir.glob("*/SKILL.md"):
            content = skill_md.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(content)
            if not fm:
                report.add(
                    severity="error",
                    harness="copilot",
                    path=skill_md,
                    message="missing or invalid frontmatter",
                    remediation="Regenerate via `make generate HARNESS=copilot`.",
                )
                continue
            _check_nonempty_str_field(report, fm, "name", "copilot", skill_md, label="skill")
            _check_nonempty_str_field(report, fm, "description", "copilot", skill_md, label="skill")

    commands_dir = WORKTREE / ".copilot" / "commands"
    if commands_dir.is_dir():
        found_any = True
        for command_md in commands_dir.rglob("*.md"):
            content = command_md.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(content)
            if not fm:
                report.add(
                    severity="error",
                    harness="copilot",
                    path=command_md,
                    message="missing or invalid frontmatter",
                    remediation="Regenerate via `make generate HARNESS=copilot`.",
                )
                continue
            description = fm.get("description")
            if not isinstance(description, str) or not description.strip():
                report.add(
                    severity="error",
                    harness="copilot",
                    path=command_md,
                    message="missing required `description` field in frontmatter",
                    remediation="Copilot command prompt files need a non-empty description.",
                )
            if command_md.name != "index.md" and not body.strip():
                report.add(
                    severity="warning",
                    harness="copilot",
                    path=command_md,
                    message="command body is empty",
                    remediation="Keep the prompt body in the source command markdown.",
                )

    if not found_any:
        return


_VALIDATORS = {
    "codex": validate_codex,
    "copilot": validate_copilot,
    "cursor": validate_cursor,
    "gemini": validate_gemini,
    "opencode": validate_opencode,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated harness artifacts.")
    parser.add_argument(
        "--harness", choices=supported_harnesses(), help="Only validate one harness."
    )
    parser.add_argument("--strict", action="store_true", help="Exit nonzero on any warning.")
    args = parser.parse_args()

    targets = [args.harness] if args.harness else supported_harnesses()

    report = Report()
    for h in targets:
        _VALIDATORS[h](report)

    if not report.findings:
        print(f"OK: no issues across {len(targets)} harness(es).")
        return 0

    # Sort findings by (severity priority, harness, path) for triage-friendly output.
    severity_order = {"error": 0, "warning": 1, "info": 2}
    sorted_findings = sorted(
        report.findings,
        key=lambda f: (severity_order.get(f.severity, 9), f.harness, str(f.path)),
    )
    errors = report.errors()
    warnings = report.warnings()
    infos = report.infos()
    for f in sorted_findings:
        print(f.render())

    print()
    print(f"Total: {len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info.")
    if errors:
        return 1
    if args.strict and warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
