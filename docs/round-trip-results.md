# Round-trip verification results

Real-CLI verification performed at branch-cut. Each harness's actual tool was used to
load the generated artifacts and report what it found.

> Reproduce locally: see the recipes at the bottom of this file.

## Summary

| Harness | CLI version | Result | Artifacts loaded | Notes |
|---|---|---|---|---|
| **OpenCode** | 1.1.23 | ✅ pass | 191 / 191 subagents discovered | All emitted agents pass OpenCode's parser. 2 OpenCode built-ins (`explore`, `general`) appear alongside ours. |
| **Gemini CLI** | 0.42.0 | ✅ pass | `gemini extensions validate .` returns "successfully validated" | Native skills + subagents at extension root recognized. |
| **Codex CLI** | 0.133.0 | ✅ pass (structural) | All 191 agent TOMLs parse via Python `tomllib`; AGENTS.md within budget (43 lines / 500 tokens) | Codex doctor surfaces no errors; deeper "did the model actually load the skill" requires interactive verification. |
| **Cursor** | (editor-only) | n/a | n/a | No CLI; manual verification recipe below. |
| **Copilot** | (structural) | ✅ pass | 191 agent profiles, 155 skills, 25 commands all validated | No CLI round-trip tool yet; structural validation via `make validate` passes. |

## Issues surfaced and fixed during round-trip

The real-CLI runs caught two bugs that pure unit tests missed. Both are now fixed and
covered by regression tests:

1. **YAML block-scalar descriptions** (`description: >` followed by indented lines).
   `tools/adapters/base.py:parse_frontmatter` was producing strings starting with the
   literal `>` indicator, which then broke OpenCode's agent loader. Fix: detect `>`,
   `>-`, `|`, `|-` and collapse the following indented lines into a single string.
   Affected agents: 4 (arm-cortex-expert + 3 meigen-ai-design agents).

2. **OpenCode permission block degraded to deny-everything** when source `tools:` only
   contained MCP tools (`mcp__...`) or was an empty list `[]`. The OpenCode adapter
   emitted `read: deny, edit: deny, ...` which made the agent inert. Fix: if no source
   tool maps to a known OpenCode permission key, omit the permission block entirely
   (default permissive — MCP tools come in via the MCP server config, not the
   permission allowlist).

3. **OpenCode rejected `$source` extension key in `opencode.json`.** Schema only allows
   `$schema`. Fix: drop the custom `$source` annotation. The adapter emits a clean
   `{"$schema": "https://opencode.ai/config.json"}` now.

## Reproduce locally

### OpenCode round-trip

```bash
# 1. Generate artifacts
make generate HARNESS=opencode
# 2. Copy into a scratch directory (or use the repo root directly)
mkdir -p /tmp/round-trip && cd /tmp/round-trip
cp -r /path/to/claude-agents/.opencode .
cp /path/to/claude-agents/opencode.json .

# 3. Verify
opencode agent list | grep "subagent)$" | wc -l
# Expected: 191 source agents discovered (plus OpenCode built-ins: explore, general)
```

### Gemini round-trip

```bash
# Native validator
gemini extensions validate /path/to/claude-agents

# Or link as an extension and probe
gemini extensions link /path/to/claude-agents
gemini skills list   # should list all generated skills
gemini extensions list | grep claude-code-workflows
```

### Codex round-trip

```bash
# Generate AGENTS.md + .codex/skills/ + .codex/agents/
make generate HARNESS=codex
# Symlink into ~/.codex (Codex uses CODEX_HOME)
mkdir -p ~/.codex/skills ~/.codex/agents
ln -sf /path/to/claude-agents/.codex/skills/* ~/.codex/skills/
ln -sf /path/to/claude-agents/.codex/agents/* ~/.codex/agents/

# AGENTS.md is read automatically when codex runs from the repo root
codex doctor | head -40   # no warnings expected from our artifacts

# Deeper: launch interactive session and ask Codex to use a generated skill by name.
# Requires interactive use — not automatable without consuming API tokens.
codex
> /skills            # browser should list all generated skills
> have backend-development__backend-architect summarize plugins/backend-development
```

### Cursor (no CLI)

```bash
# Generate
make generate HARNESS=cursor
# Manually:
# 1. Open Cursor 2.5+
# 2. Settings → Plugins → Add Local Plugin Source
# 3. Point at /path/to/claude-agents/
# 4. Verify the marketplace browser lists all 81 local plugins
# 5. Verify .cursor/rules/*.mdc files activate per their `globs`
# 6. Skills under .claude/skills/ should auto-trigger from descriptions
```

### Copilot (no CLI round-trip yet)

```bash
# Generate
make generate HARNESS=copilot

# Structural validation (parses every generated artifact)
make validate

# Verify artifact tree
ls .copilot/agents/   # 191 agent profiles (*.agent.md)
ls .copilot/skills/   # 155 skill dirs (each with SKILL.md)
ls .copilot/commands/ # command-prompt files

# Global install (optional)
make install-copilot   # symlinks .copilot/ -> ~/.copilot/
```

Copilot currently lacks a CLI verification tool. Manual testing: open VS
Code, open the Copilot Chat (Ctrl+Shift+I), and verify agents appear in the
agent selector and skills auto-trigger from matching prompts.

## Automated structural checks (no CLI needed)

The `tools/validate_generated.py` script approximates round-trip without installing the
harnesses:

```bash
make validate                 # all five harnesses
make validate HARNESS=codex   # one only
```

It parses every TOML/JSON/MDC artifact against documented schemas. Run before merging
any adapter change.

## Recurring drift detection

```bash
make garden       # find stale artifacts, oversized context files, dead links, etc.
```

`tools/doc_gardener.py` per the OpenAI harness-engineering pattern — recurring task
that surfaces drift with concrete remediation hints.

## Coverage limits

The pure-structural validators do **not** verify that the model can actually consume
the artifacts at runtime. Specifically untested by the automated suite:

- Whether Codex's skill discovery actually selects our skills on relevant prompts (vs.
  ignoring them or selecting wrong ones).
- Whether OpenCode's `task` tool dispatches our subagents end-to-end.
- Whether Cursor 2.5+ marketplace browser displays our plugin entries (requires the
  editor; can't be scripted).
- Whether Gemini's `@<agent>` invocation runs our generated subagent against a real
  prompt.
- Whether Copilot's agent profile and skill discovery actually loads our artifacts
  end-to-end (no CLI; requires VS Code editor).

These require interactive use and API-token-burning runs. The recipes above show how
to perform them manually.
