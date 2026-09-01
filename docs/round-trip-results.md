# Round-trip verification results

Real-CLI verification performed at branch-cut. Each harness's actual tool was used to
load the generated artifacts and report what it found.

> Reproduce locally: see the recipes at the bottom of this file.

## Summary

| Harness | CLI version | Result | Artifacts loaded | Notes |
|---|---|---|---|---|
| **OpenCode** | 1.1.23 | ✅ pass | 191 / 191 subagents discovered | All emitted agents pass OpenCode's parser. 2 OpenCode built-ins (`explore`, `general`) appear alongside ours. |
| **Antigravity CLI** | agy 1.1.14 | ✅ pass (2026-08-18) | `agy plugin validate` passes for 91/91 generated plugins | Self-contained plugins at `.antigravity/plugins/<p>/`; `agy plugin install` + `agy plugin list` confirm discovery. Gemini CLI's harness support was retired May 2026 (Google deprecation) and is superseded by this row. |
| **Codex CLI** | 0.133.0 | ✅ pass (structural) | All 191 agent TOMLs parse via Python `tomllib`; AGENTS.md within budget (43 lines / 500 tokens) | Codex doctor surfaces no errors; deeper "did the model actually load the skill" requires interactive verification. |
| **Cursor** | (editor-only) | n/a | n/a | No CLI; manual verification recipe below. |
| **Copilot** | (structural) | ✅ pass | 191 agent profiles, 155 skills, 25 commands all validated | No CLI round-trip tool yet; structural validation via `make validate` passes. |
| **gh skill** | gh 2.98.0 | ✅ pass (2026-09-01) | 183 / 183 source skills discovered; `gh skill publish --dry-run` passes | Discovery through the `plugins/{scope}/skills/*/SKILL.md` convention; installs by bare skill name. Runs in CI via `make smoke-test`. |
| **npx skills** | skills 1.5.23 | ✅ pass (2026-09-01) | 183 / 183 source skills discovered | Flat skill names. From a generated checkout the listing also includes the gitignored harness trees. Runs in CI via `make smoke-test`. |

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

### Antigravity round-trip

```bash
# Generate artifacts
make generate HARNESS=antigravity

# Structural validation, one plugin at a time (agy's own binary, not our validator)
for p in .antigravity/plugins/*/; do
  agy plugin validate "$p"
done

# Install + discover
agy plugin install .antigravity/plugins/<name>
agy plugin list   # should list <name> among installed plugins

# Or symlink every generated plugin into agy's config dir at once
make install-antigravity
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

### Agent Skills installers (gh skill, npx skills)

```bash
# Local discovery, same conventions as a GitHub install (no network)
gh skill install . --from-local | grep -c '^\[plugins\]'
# Expected: 183 source skills, listed as `[plugins] <plugin>/<skill>`

# agentskills.io spec validation (name pattern, name == directory, frontmatter)
gh skill publish --dry-run
# Expected: exit 0; `license` warnings are advisory

# Vercel skills CLI discovery (walks gitignored generated trees too, so the count
# exceeds 183 after `make generate-all`; every source skill must be present)
DISABLE_TELEMETRY=1 npx skills add . --list -y

# From GitHub, as a user would
gh skill install wshobson/agents python-testing-patterns --dir /tmp/gh-skill-check
npx skills add wshobson/agents --skill python-testing-patterns --list
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
- Whether Antigravity's `invoke_subagent` actually dispatches our generated subagent
  against a real prompt (agy's `plugin validate` is structural only).
- Whether Copilot's agent profile and skill discovery actually loads our artifacts
  end-to-end (no CLI; requires VS Code editor).

These require interactive use and API-token-burning runs. The recipes above show how
to perform them manually.
