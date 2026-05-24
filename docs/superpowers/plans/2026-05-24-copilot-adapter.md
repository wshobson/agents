# Copilot Harness Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a native GitHub Copilot CLI/Cloud Agent harness adapter so `make generate HARNESS=copilot --all` emits Copilot-compatible agent files at `.copilot/agents/<plugin>__<agent>.md`.

**Architecture:** Follow the existing opencode.py adapter pattern. A `CopilotAdapter` class extends `HarnessAdapter`, iterates plugin agents, and writes Markdown agent profiles with YAML frontmatter (name, description, tools, model). Tool names are lowercased to Copilot's naming convention. Model IDs are resolved via capabilities.py's `resolve_model` with provider-prefixed IDs.

**Tech Stack:** Python 3, adapter framework from `tools/adapters/base.py`, Copilot's YAML-frontmatter Markdown agent format.

**Spec ref:** `COPILOT_ADAPTER_IMPLEMENTATION.md` (reproot), `research/copilot-integrating-agents-and-skills-harness.md`

---

### Task 1: Create tools/adapters/copilot.py

**Files:**
- Create: `tools/adapters/copilot.py`

- [ ] **Step 1: Write the adapter class skeleton**

```python
"""Copilot adapter for GitHub Copilot CLI and Cloud Agent.

Emits Markdown agent profiles with YAML frontmatter for ingestion by:
- Copilot CLI via ~/.copilot/agents/ and .github/agents/
- Copilot Cloud Agent via .github/agents/ in repository

Discovery precedence:
  1. User: ~/.copilot/agents/
  2. Project: .github/agents/
  3. Organization: .github-private repo under /agents/
  4. Enterprise: enterprise-level config

Agent files are Markdown with YAML frontmatter (name, description, tools, model).
Body is the agent's prompt/instructions with lowercased tool references.
"""

from __future__ import annotations

from pathlib import Path

from tools.adapters.base import (
    AgentSource,
    EmitResult,
    HarnessAdapter,
    PluginSource,
)
from tools.adapters.capabilities import TOOL_NAME_MAPS, resolve_model


def _copilot_frontmatter(fm: dict) -> str:
    """Format YAML frontmatter for Copilot agent files.

    Handles scalars, lists, and booleans. Omits None values.
    Lists are emitted as block list items.
    """
    lines = ["---"]
    for k, v in fm.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - {item}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {'true' if v else 'false'}")
        elif v is not None:
            value = str(v).replace("\n", " ").strip()
            lines.append(f"{k}: {value}")
    lines.append("---")
    return "\n".join(lines)


def _rewrite_body_lowercase_tools(body: str) -> str:
    """Lowercase Claude Code CamelCase tool names in backticked references.

    For example, `Read` becomes `read`, `Bash` becomes `bash`.
    Uses TOOL_NAME_MAPS["copilot"] for the mapping.
    """
    out = body
    for camel, replacement in TOOL_NAME_MAPS["copilot"].items():
        out = out.replace(f"`{camel}`", f"`{replacement}`")
    return out


def _build_tools_list(agent_tools: list[str]) -> list[str]:
    """Map source tools to Copilot tool names.

    Unmapped tools (e.g. mcp__*, custom) pass through unchanged.
    """
    copilot_map = TOOL_NAME_MAPS["copilot"]
    return [copilot_map.get(t, t) for t in agent_tools]


class CopilotAdapter(HarnessAdapter):
    harness_id = "copilot"

    def emit_plugin(self, plugin: PluginSource) -> EmitResult:
        result = EmitResult()
        for agent in plugin.agents:
            self._emit_agent(plugin, agent, result)
        return result

    def emit_global(self, plugins: list[PluginSource]) -> EmitResult:
        return EmitResult()

    def _emit_agent(self, plugin: PluginSource, agent: AgentSource, result: EmitResult) -> None:
        agent_id = f"{plugin.name}__{agent.name}"
        rel = Path(".copilot") / "agents" / f"{agent_id}.md"

        model, warning = resolve_model("copilot", agent.model)
        if warning:
            result.warnings.append(f"agent `{agent_id}`: {warning}")

        fm: dict = {
            "name": agent_id,
            "description": agent.description or f"{agent.name} (from {plugin.name})",
        }

        has_tools_field = "tools" in agent.frontmatter
        if has_tools_field:
            if agent.tools:
                fm["tools"] = _build_tools_list(agent.tools)
            else:
                fm["tools"] = []

        if model:
            fm["model"] = model

        body = _rewrite_body_lowercase_tools(agent.body).rstrip() + "\n"
        content = _copilot_frontmatter(fm) + "\n\n" + body
        result.written.append(self.write(rel, content))
```

- [ ] **Step 2: Verify the file parses**

Run: `python -c "import tools.adapters.copilot; print('copilot.py imports OK')"`
Expected: `copilot.py imports OK`

### Task 2: Update tools/adapters/capabilities.py

**Files:**
- Modify: `tools/adapters/capabilities.py`

- [ ] **Step 1: Add copilot Capability entry**

After the `gemini` entry (around line 151), add:

```python
    "copilot": Capability(
        harness_id="copilot",
        display_name="GitHub Copilot",
        skills_native=True,
        agents_native=True,
        commands_native=False,
        plugin_marketplace=False,
        parallel_agents=True,
        tool_allowlist_per_agent=True,
        todowrite=False,
        task_spawn=True,
        mcp_servers=True,
        hooks=False,
        context_file_name=None,
        context_file_max_lines=_CONTEXT_LINES_CAP,
        skill_body_max_bytes=_NO_CAP,
        tool_name_case="lowercase",
        bare_model_aliases=False,
        notes="Discovers .claude/skills/ + .github/skills/ natively. Agents at .github/agents/ (project) or ~/.copilot/agents/ (user). Cloud Agent reads .github/agents/ from default branch.",
    ),
```

- [ ] **Step 2: Add copilot to TOOL_NAME_MAPS**

In the `TOOL_NAME_MAPS` dict (after the `gemini` entry around line 210), add:

```python
    "copilot": {
        "Read": "read",
        "Edit": "edit",
        "Write": "write",
        "Bash": "bash",
        "Grep": "grep",
        "Glob": "glob",
        "LS": "list",
        "WebFetch": "webfetch",
        "WebSearch": "websearch",
        "TodoWrite": "todowrite",
        "Agent": "task",
        "Task": "task",
        "Skill": "skill",
        "LSP": "lsp",
    },
```

- [ ] **Step 3: Add copilot to MODEL_ALIASES**

After the `gemini` entry in `MODEL_ALIASES` (around line 245), add:

```python
    "copilot": {
        "opus": "claude-opus-4",
        "sonnet": "claude-sonnet-4",
        "haiku": "claude-haiku-4-5-20251001",
        "inherit": "claude-sonnet-4",
    },
```

### Task 3: Update tools/generate.py

**Files:**
- Modify: `tools/generate.py`

- [ ] **Step 1: Add copilot to _HARNESS_TARGETS**

Add after the `gemini` entry (around line 36):

```python
    "copilot": [".copilot"],
```

- [ ] **Step 2: Wire get_adapter for copilot**

Add after the `gemini` branch (around line 57):

```python
    if harness_id == "copilot":
        from tools.adapters.copilot import CopilotAdapter

        return CopilotAdapter(output_root=output_root)
```

- [ ] **Step 3: Add copilot to prune_orphans**

Add after the `gemini` branch (around line 157):

```python
    elif harness_id == "copilot":
        d = output_root / ".copilot"
        if d.is_dir():
            candidates.extend(p for p in d.rglob("*") if p.is_file())
```

### Task 4: Add copilot validator to validate_generated.py

**Files:**
- Modify: `tools/validate_generated.py`

- [ ] **Step 1: Add validate_copilot function**

After `validate_gemini` (around line 499), add:

```python
def validate_copilot(report: Report) -> None:
    root = WORKTREE / ".copilot"
    if not root.is_dir():
        return

    agents_dir = root / "agents"
    if agents_dir.is_dir():
        for agent_md in agents_dir.glob("*.md"):
            content = agent_md.read_text()
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
            if "name" not in fm:
                report.add(
                    severity="error",
                    harness="copilot",
                    path=agent_md,
                    message="missing required `name` field in frontmatter",
                    remediation="Each Copilot agent needs a name.",
                )
            if "description" not in fm:
                report.add(
                    severity="warning",
                    harness="copilot",
                    path=agent_md,
                    message="missing `description` in frontmatter",
                    remediation="Copilot agents should have a description for discoverability.",
                )
```

- [ ] **Step 2: Register the validator**

Add to the `_VALIDATORS` dict (around line 509):

```python
    "copilot": validate_copilot,
```

### Task 5: Update Makefile

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Add copilot to HARNESSES list**

Change line 160 from:

```makefile
HARNESSES := codex cursor opencode gemini
```

to:

```makefile
HARNESSES := codex copilot cursor opencode gemini
```

### Task 6: Run generator and verify

- [ ] **Step 1: Generate copilot artifacts**

Run: `make generate HARNESS=copilot --all`
Expected: Generates `.copilot/agents/` with agent files for every plugin that has agents.

- [ ] **Step 2: Validate generated artifacts**

Run: `python tools/validate_generated.py --harness copilot`
Expected: No errors (warnings about missing descriptions are OK).

- [ ] **Step 3: Verify output structure**

Run: `ls .copilot/agents/ | head -10`
Expected: List of `<plugin>__<agent>.md` files.

- [ ] **Step 4: Spot-check one agent file**

Run: `head -15 .copilot/agents/<any-plugin>__<any-agent>.md`
Expected: YAML frontmatter with name, description, tools, model.

- [ ] **Step 5: Commit**

```bash
git add tools/adapters/copilot.py tools/adapters/capabilities.py tools/generate.py tools/validate_generated.py Makefile
git add docs/superpowers/plans/2026-05-24-copilot-adapter.md
git commit -m "feat: add Copilot harness adapter"
```
