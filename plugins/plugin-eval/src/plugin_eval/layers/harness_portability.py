"""Harness portability checks — surface non-portable patterns across Codex/Cursor/OpenCode/Gemini.

Each finding ships with a `remediation` string (OpenAI harness-engineering pattern:
lint error messages inject remediation instructions into agent context).

Used by `layers/static.py` to compute the `harness_portability` sub-score.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from plugin_eval.parser import ParsedAgent, ParsedSkill

# Codex hard cap for skill body
_CODEX_SKILL_BYTE_CAP = 8 * 1024

# Names that collide with Codex built-in subagent roles
_CODEX_BUILTIN_AGENT_NAMES = {"default", "worker", "explorer"}

_CLAUDE_TOOLS = (
    "Read",
    "Edit",
    "Write",
    "Bash",
    "Grep",
    "Glob",
    "Agent",
    "Task",
    "TodoWrite",
    "WebFetch",
    "WebSearch",
    "LS",
    "LSP",
)
_TOOL_ALTERNATION = "|".join(_CLAUDE_TOOLS)

# Match a backticked tool name only when it's used in a Claude-tool context:
#   - prefixed by "the " ("the `Bash`")
#   - or suffixed by " tool" (`Task` tool)
#   - or "use `Bash`" / "call `Read`" / "invoke `Task`"
# This rules out generic prose backticks like Rust's `Task` type in API docs.
_CAMEL_TOOL_PATTERN = re.compile(
    rf"(?:\b(?:the|use|using|call|calling|invoke|invoking|via)\s+)`({_TOOL_ALTERNATION})`"
    rf"|`({_TOOL_ALTERNATION})`\s+tool\b",
    re.IGNORECASE,
)

# Phrases like "use the Read tool" / "Use the Bash tool".
# The leading article ("the" / "The" / "THE") is matched case-insensitively, but the
# tool name itself must match exact CamelCase — otherwise generic English like
# "the bash tool" (referring to the shell, not Claude's Bash) false-positives.
_TOOL_PROSE_PATTERN = re.compile(rf"(?i:\bthe)\s+(?:`)?({_TOOL_ALTERNATION})(?:`)?\s+tool\b")

# Bare model aliases that don't map cleanly (Cursor/OpenCode/Gemini need full IDs)
_BARE_MODEL_ALIAS_PATTERN = re.compile(r"^(fable|opus|sonnet|haiku)$")

# Context file line cap (per harness-engineering principle)
_CONTEXT_FILE_LINE_CAP = 150


@dataclass(frozen=True)
class PortabilityFinding:
    flag: str
    severity: float  # 0.0–0.30 (max one finding)
    description: str
    remediation: str

    def to_anti_pattern(self):
        """Render as a plugin_eval.models.AntiPattern with remediation appended."""
        from plugin_eval.models import AntiPattern

        return AntiPattern(
            flag=self.flag,
            description=f"{self.description}\nFix: {self.remediation}",
            severity=self.severity,
        )


def detect_skill_findings(skill: ParsedSkill) -> list[PortabilityFinding]:
    """All harness-portability findings for one skill."""
    findings: list[PortabilityFinding] = []

    # 1. Skill body exceeds Codex's 8 KB hard cap
    body_bytes = len(skill.raw_content.encode("utf-8"))
    if body_bytes > _CODEX_SKILL_BYTE_CAP and not skill.has_references:
        findings.append(
            PortabilityFinding(
                flag="SKILL_OVER_CODEX_CAP",
                severity=0.15,
                description=(
                    f"Skill body is {body_bytes} bytes; Codex hard-truncates skills at "
                    f"{_CODEX_SKILL_BYTE_CAP} bytes. No `references/` directory present."
                ),
                remediation=(
                    "Move detail sections into `references/details.md` (or similar) and "
                    "leave the SKILL.md body as a navigation summary. Codex will load the "
                    "references on demand."
                ),
            )
        )

    # 2. Body uses CamelCase Claude tool names in backticks ("`Read`", "`Bash`")
    raw_matches = _CAMEL_TOOL_PATTERN.findall(skill.raw_content)
    # Pattern has two alternatives so each match is a 2-tuple; pick whichever side fired.
    tool_hits = [m[0] or m[1] for m in raw_matches if m[0] or m[1]]
    if tool_hits:
        unique = sorted(set(tool_hits))
        findings.append(
            PortabilityFinding(
                flag="CLAUDE_TOOL_REFS",
                severity=min(0.10, 0.02 * len(unique)),
                description=(
                    f"Skill body references Claude Code tools by CamelCase name: {unique}. "
                    "OpenCode requires lowercase (`read`, `bash`); Codex prefers action verbs."
                ),
                remediation=(
                    "Use action verbs (e.g. 'open the file', 'run the shell command') or "
                    "lowercase the tool reference. The adapter rewrites a conservative set, "
                    "but explicit phrasing is more portable."
                ),
            )
        )

    # 3. Body uses prose like "use the Read tool"
    prose_hits = _TOOL_PROSE_PATTERN.findall(skill.raw_content)
    if prose_hits:
        unique = sorted(set(prose_hits))
        findings.append(
            PortabilityFinding(
                flag="CLAUDE_TOOL_PROSE",
                severity=0.05,
                description=(
                    f"Skill body uses prose like 'use the X tool' for: {unique}. Codex "
                    "doesn't name tools to the model; the model picks them by action."
                ),
                remediation=(
                    'Rewrite "the Read tool" as "open the file", "the Bash tool" as '
                    '"run the shell command", etc. Talk about the action, not the tool.'
                ),
            )
        )

    return findings


def detect_agent_findings(agent: ParsedAgent) -> list[PortabilityFinding]:
    """All harness-portability findings for one agent."""
    findings: list[PortabilityFinding] = []

    name = (agent.frontmatter.get("name") or "").strip().lower()
    if name in _CODEX_BUILTIN_AGENT_NAMES:
        findings.append(
            PortabilityFinding(
                flag="AGENT_NAME_COLLISION",
                severity=0.10,
                description=(
                    f"Agent name '{name}' collides with a Codex built-in role "
                    "(default/worker/explorer). The Codex adapter will namespace-rename it."
                ),
                remediation=(f"Rename to something plugin-scoped, e.g. `<plugin>-{name}`."),
            )
        )

    model = (agent.frontmatter.get("model") or "").strip().lower()
    if _BARE_MODEL_ALIAS_PATTERN.match(model):
        findings.append(
            PortabilityFinding(
                flag="BARE_MODEL_ALIAS",
                severity=0.03,
                description=(
                    f"Agent frontmatter uses bare model alias `{model}`. Cursor doesn't "
                    "accept Anthropic aliases; OpenCode requires full provider/model-id."
                ),
                remediation=(
                    "The adapter maps these at generation time. To be explicit, use "
                    "`inherit` (Cursor) or `anthropic/claude-<full-id>` (OpenCode)."
                ),
            )
        )

    raw_matches = _CAMEL_TOOL_PATTERN.findall(agent.raw_content)
    tool_hits = [m[0] or m[1] for m in raw_matches if m[0] or m[1]]
    if tool_hits:
        findings.append(
            PortabilityFinding(
                flag="CLAUDE_TOOL_REFS",
                severity=0.05,
                description=(
                    f"Agent body references Claude Code tools by CamelCase name: "
                    f"{sorted(set(tool_hits))}."
                ),
                remediation=(
                    "OpenCode wants lowercase; Codex wants action verbs. The adapter "
                    "rewrites these but explicit phrasing is more portable."
                ),
            )
        )

    return findings


def score_skill_portability(skill: ParsedSkill) -> float:
    """0.0–1.0 portability sub-score for a skill."""
    findings = detect_skill_findings(skill)
    if not findings:
        return 1.0
    penalty = sum(f.severity for f in findings)
    return max(0.0, 1.0 - penalty)


def score_agent_portability(agent: ParsedAgent) -> float:
    """0.0–1.0 portability sub-score for an agent."""
    findings = detect_agent_findings(agent)
    if not findings:
        return 1.0
    penalty = sum(f.severity for f in findings)
    return max(0.0, 1.0 - penalty)
