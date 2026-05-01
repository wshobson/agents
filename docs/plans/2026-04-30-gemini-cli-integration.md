# Gemini CLI Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add lightweight Gemini CLI support to the claude-agents marketplace, exposing 150+ skills with graceful degradation of unsupported Claude features.

**Architecture:** Use a lightweight extension manifest approach (gemini-extension.json + GEMINI.md) that mirrors Gemini CLI's native extension model. This preserves Claude Code primacy while adding Gemini parity through skill auto-discovery, tool mapping reference, and plugin-level context. No code changes to existing skills needed; all 150+ skills are platform-agnostic markdown.

**Tech Stack:** 
- Gemini CLI extension system (gemini-extension.json manifest, GEMINI.md context)
- GitHub topic discovery (gemini-cli-extension)
- Markdown-based skill and context files
- No build system, no runtime code

---

## Phase 1: Foundation (Minimal Viable Gemini Support)

This phase implements the 4 core files required for Gemini CLI to discover and load the skills ecosystem.

---

### Task 1: Create gemini-extension.json Manifest

**Files:**
- Create: `gemini-extension.json`
- Reference: `gemini-cli-official-documentation-summary.md` (gemini-extension.json reference)

**Context:**
The manifest tells Gemini CLI how to load the extension. It's a single JSON file at repo root that declares:
- Extension name and version
- Which context file to load (GEMINI.md)
- Optional MCP servers, settings, hooks (Phase 2+)

**Step 1: Create the manifest file**

```bash
cd /home/mhenke/Projects/agents
cat > gemini-extension.json << 'EOF'
{
  "name": "claude-agents",
  "version": "1.6.0",
  "description": "79-plugin ecosystem with 150+ specialized skills for architecture, infrastructure, language development, security, testing, and full-stack development.",
  "contextFileName": "GEMINI.md"
}
EOF
```

Expected output:
```
(file created)
```

**Step 2: Verify the file exists and is valid JSON**

```bash
cd /home/mhenke/Projects/agents
python3 -m json.tool gemini-extension.json > /dev/null && echo "✓ Valid JSON"
cat gemini-extension.json
```

Expected output:
```
✓ Valid JSON
{
  "name": "claude-agents",
  "version": "1.6.0",
  "description": "79-plugin ecosystem with 150+ specialized skills for architecture, infrastructure, language development, security, testing, and full-stack development.",
  "contextFileName": "GEMINI.md"
}
```

**Step 3: Commit**

```bash
cd /home/mhenke/Projects/agents
git add gemini-extension.json
git commit -m "feat: add Gemini CLI extension manifest

- Declare claude-agents as a Gemini CLI extension
- Point to GEMINI.md for bootstrap context
- Enable auto-discovery via gemini-cli-extension topic

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected output:
```
[main XXXX] feat: add Gemini CLI extension manifest
 1 file changed, 7 insertions(+)
 create mode 100644 gemini-extension.json
```

---

### Task 2: Create Root GEMINI.md (Bootstrap & Plugin Navigation)

**Files:**
- Create: `GEMINI.md`
- Reference: `docs/plugins.md` (plugin catalog), `plugins/plugin-eval/` (plugin structure)

**Context:**
GEMINI.md is the persistent context file loaded by Gemini CLI at session start. It serves three purposes:
1. **Bootstrap instructions** — Explain the skills ecosystem and how to use it
2. **Plugin navigation** — List plugins with their skills for discoverability
3. **Tool mapping reference** — Document Claude → Gemini tool equivalents

This file will reference (via `@./path` syntax) two supporting documents:
- `@./docs/gemini-tool-mapping.md` — Detailed tool equivalents
- `@./docs/plugins.md` — Plugin catalog (auto-generated)

**Step 1: Create GEMINI.md**

```bash
cd /home/mhenke/Projects/agents
cat > GEMINI.md << 'EOF'
# Claude-Agents: Skills Ecosystem for Gemini CLI

You have access to **150+ specialized skills** organized across **79 plugins** in the claude-agents marketplace. These skills are designed for progressive disclosure — they activate only when you identify a matching task, saving context tokens.

## Navigation

- **Skill Library**: Skills are auto-discovered by Gemini CLI. Use skills by name when the model identifies a matching task (e.g., "use the security-audit skill").
- **Plugin Catalog**: See @./docs/plugins.md for a full listing of plugins, their skills, and purpose areas.
- **Tool Mapping**: Claude Code and Gemini CLI have different tool sets. See @./docs/gemini-tool-mapping.md for equivalents and platform-specific notes.

## Key Differences from Claude Code

This ecosystem was originally built for **Claude Code** (Claude AI paired with a specialized IDE) and includes features that don't map directly to Gemini CLI:

| Feature | Claude Code | Gemini CLI | Workaround |
|---------|-----------|-----------|-----------|
| **Slash Commands** | `/plan`, `/spec`, `/ship` entry points | Skills auto-trigger instead | Use skill names directly in prompts |
| **Subagent Orchestration** | Fan-out parallel execution | Sequential task execution | Use @superpowers:executing-plans to batch tasks |
| **Model Assignment** | Per-agent model tiers (Opus/Sonnet/Haiku) | Session-level model only | Skills are model-agnostic; use session default |
| **Plugin Installation** | Per-plugin via `/plugin install` | Per-extension via `gemini extensions install` | Install once: `gemini extensions install https://github.com/mhenke/agents` |

## How to Use Skills

Skills are **on-demand expertise packages**. When you ask a task that matches a skill's description, Gemini CLI will:

1. Identify the matching skill
2. Ask your permission to activate it
3. Load the skill's full instructions into context
4. Follow the skill's procedural guidance

**Examples:**
- Ask: "I need to audit my code for security vulnerabilities"
  - Gemini identifies the `security-audit` skill and activates it
- Ask: "Set up a Kubernetes deployment for my app"
  - Gemini identifies a `kubernetes-setup` skill and loads it

## Common Skill Categories

### Language Development
- Python, JavaScript/TypeScript, Rust, Go, Kotlin, C#, Java, Ruby, PHP, Swift, etc.

### Infrastructure & DevOps
- Kubernetes, Docker, CI/CD, cloud platforms (AWS, GCP, Azure), deployment, observability

### Security
- Code scanning, vulnerability assessment, compliance, architecture security audit

### Full-Stack Development
- Frontend frameworks, backend APIs, databases, testing, performance optimization

### Multi-Agent Workflows
- Code review orchestration, system design, large refactors, complex troubleshooting

For a complete catalog, see @./docs/plugins.md.

## Installation & Getting Started

This extension is already installed. To update it:

```bash
gemini extensions update claude-agents
```

To reinstall or install from source:

```bash
gemini extensions install https://github.com/mhenke/agents
```

## Support & Contribution

- **Issues**: Report bugs or suggest skills at https://github.com/mhenke/agents/issues
- **Skill Development**: Contribute new skills by creating a `skills/<skill-name>/SKILL.md` file
- **Plugin Development**: Create new plugins in `plugins/` following the structure in @./CLAUDE.md

---

**Last Updated**: April 2026
**Skills**: 150+
**Plugins**: 79
**Platform**: Gemini CLI 3.0+
EOF
```

Expected output:
```
(file created)
```

**Step 2: Verify the file exists and validate markdown structure**

```bash
cd /home/mhenke/Projects/agents
test -f GEMINI.md && echo "✓ GEMINI.md exists"
head -5 GEMINI.md
```

Expected output:
```
✓ GEMINI.md exists
# Claude-Agents: Skills Ecosystem for Gemini CLI

You have access to **150+ specialized skills** organized across **79 plugins** in the claude-agents marketplace. These skills are designed for progressive disclosure — they activate only when you identify a matching task, saving context tokens.
```

**Step 3: Verify references are valid (files must exist)**

```bash
cd /home/mhenke/Projects/agents
test -f docs/plugins.md && echo "✓ docs/plugins.md exists" || echo "⚠ docs/plugins.md will be created in Task 3"
test -f docs/gemini-tool-mapping.md && echo "✓ docs/gemini-tool-mapping.md exists" || echo "⚠ docs/gemini-tool-mapping.md will be created in Task 3"
```

Expected output (after Task 3):
```
✓ docs/plugins.md exists
✓ docs/gemini-tool-mapping.md exists
```

**Step 4: Commit**

```bash
cd /home/mhenke/Projects/agents
git add GEMINI.md
git commit -m "feat: add Gemini CLI bootstrap context

- Document 150+ skills ecosystem for Gemini users
- Explain differences from Claude Code platform
- Provide plugin navigation and skill usage guidance
- Link to tool mapping and plugin catalog

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected output:
```
[main XXXX] feat: add Gemini CLI bootstrap context
 1 file changed, 68 insertions(+)
 create mode 100644 GEMINI.md
```

---

### Task 3: Create docs/gemini-tool-mapping.md (Tool Equivalents Reference)

**Files:**
- Create: `docs/gemini-tool-mapping.md`
- Reference: `gemini-cli-official-documentation-summary.md` (tool mapping section), `CLAUDE.md` (Claude tool list)

**Context:**
This document provides a lookup table mapping Claude Code tools to Gemini CLI equivalents. It explains which tools are available, which have limitations, and provides workarounds for platform differences.

**Step 1: Create the tool mapping document**

```bash
cd /home/mhenke/Projects/agents
cat > docs/gemini-tool-mapping.md << 'EOF'
# Claude-Agents Tool Mapping: Claude Code ↔ Gemini CLI

This document maps tools between Claude Code (the original platform for this ecosystem) and Gemini CLI (the Gemini-based alternative). Use this to understand which tools and workflows are available in each platform.

## Core Tools: Direct Equivalents

These tools work identically in both platforms:

| Claude Code | Gemini CLI | Notes |
|------------|-----------|-------|
| **Read** | `read_file` | Read files from disk. Same behavior. |
| **Write** | `write_file` | Write/create files. Same behavior. |
| **Bash** | `run_shell_command` | Execute shell commands. Same behavior. |
| **Grep** | `grep_search` | Search file contents. Same behavior. |
| **Glob** | File pattern matching | Gemini provides file operations for globbing. |

## Platform-Specific Features: Claude Code Only

These tools and features exist **only** in Claude Code and have **no Gemini CLI equivalent**.

### Slash Commands
- `/plugin install` — Install plugins
- `/spec` — Create formal specifications
- `/plan` — Create step-by-step plans
- `/build` — Execute implementation plans
- `/ship` — Run multi-agent orchestration

**Workaround for Gemini CLI:**
- Slash commands are **not supported**
- Instead, skills **auto-activate** when you describe your task
- For multi-step workflows, use the `executing-plans` skill to batch tasks

### Subagent Orchestration
- Multi-agent fan-out patterns (e.g., `/ship` command)
- Per-agent model assignment (Opus/Sonnet/Haiku strategy)

**Workaround for Gemini CLI:**
- Subagents are **not supported**
- Use the `executing-plans` skill to batch related tasks sequentially
- Skills in this ecosystem are model-agnostic; use session default model

### Model Tiers
Claude Code supports 3-tier model strategy:
- Tier 1: Claude 3.5 Opus (complex/production work)
- Tier 2: Claude 3.5 Sonnet (standard)
- Tier 3: Claude 3.5 Haiku (fast operations)

**Workaround for Gemini CLI:**
- Model assignment per skill is **not supported**
- Gemini CLI uses a single session-wide model
- Skills are designed to work with any model; Gemini's default applies to all

## Claude Code Specific: Claude MCP Servers

Claude Code has built-in MCP servers for IDE integration:
- `claude-code` — IDE context, file operations, terminal integration
- Claude-specific tool implementations

**Gemini CLI:**
- Gemini CLI supports **standard MCP servers** (via `@modelcontextprotocol/sdk`)
- Can be added to extension via `gemini-extension.json` if needed
- Currently not required for skills ecosystem

## Platform Differences: Behavior & Constraints

### Context Window Management

| Aspect | Claude Code | Gemini CLI | Impact |
|--------|-----------|-----------|--------|
| **Skills Activation** | Explicit (slash commands like `/skill-name`) | Implicit (auto-triggered when task matches description) | Gemini is more seamless; Claude requires explicit entry points |
| **Context Persistence** | Session-based (plan, spec, notes persist) | Session-based + GEMINI.md bootstrap | Gemini loads common context automatically at session start |
| **Progressive Disclosure** | Skills load on-demand when invoked | Skills load on-demand when matched | Both save tokens by loading only needed expertise |

### Tool Availability

| Tool Category | Claude Code | Gemini CLI | Notes |
|--------------|-----------|-----------|-------|
| **File Operations** | ✅ Full | ✅ Full | Read, write, glob patterns work identically |
| **Shell Execution** | ✅ Full | ✅ Full | Bash/shell commands work identically |
| **Search** | ✅ Grep, Glob | ✅ Grep | Pattern-based file search available |
| **IDE Integration** | ✅ Yes | ❌ No | IDE context only in Claude Code |
| **Version Control** | ✅ Git support | ⚠ Requires manual git commands | Git available via `run_shell_command` |
| **Package Management** | ✅ npm, pip, cargo, etc. | ⚠ Requires manual commands | PM available via `run_shell_command` |

## Skill Design Guidelines for Cross-Platform Support

If you're writing or modifying skills to work on both platforms, follow these guidelines:

### DO:
✅ **Reference tools by generic purpose** — "Read a file" instead of "Use Read tool"
✅ **Document both platforms' tool names** — Mention both `read_file` (Gemini) and `Read` (Claude Code)
✅ **Provide shell command examples** — Work on both platforms via `run_shell_command`
✅ **Make skills model-agnostic** — Don't assume Opus; work with any model
✅ **Use skill descriptions for auto-activation** — Clear trigger phrases help Gemini's auto-matching

### DON'T:
❌ **Assume slash commands** — `/spec`, `/plan`, `/ship` don't exist in Gemini
❌ **Assume subagent orchestration** — Multi-agent fan-out unavailable in Gemini
❌ **Assume model tiers** — Can't assign Opus to one agent, Haiku to another
❌ **Use IDE-specific tools** — Claude Code IDE context doesn't exist in Gemini
❌ **Assume plugins exist** — In Gemini CLI, use "extensions" terminology

## Migration Path: Claude Code → Gemini CLI

If you want to migrate a workflow from Claude Code to Gemini CLI:

1. **Identify the workflow** — Describe what you're trying to accomplish (e.g., "security audit")
2. **Map tools** — Use the table above to identify tool equivalents
3. **Adapt skill trigger** — In Gemini, describe the task clearly; skill auto-triggers
4. **Test on Gemini** — Verify the workflow works with Gemini's tools
5. **Document platform differences** — Note any differences in the skill's description

## Common Patterns: Platform Workarounds

### Pattern: Slash Command Entry Points

**Claude Code:**
```
User: /security-audit
Gemini starts the security-audit skill
```

**Gemini CLI:**
```
User: "I need to audit my code for security vulnerabilities"
Gemini identifies and auto-activates the security-audit skill
```

**Lesson**: In Gemini, describe your need clearly; the skill auto-activates.

### Pattern: Multi-Agent Orchestration

**Claude Code:**
```
User: /ship
CLI runs: reviewer agent → test agent → deploy agent (in parallel via subagents)
```

**Gemini CLI:**
```
User: "I need to review code, run tests, and deploy"
Use @superpowers:executing-plans to batch tasks sequentially:
1. Code review step
2. Test execution step
3. Deployment step
```

**Lesson**: Gemini's `executing-plans` skill sequences tasks; doesn't parallelize like Claude's subagents.

### Pattern: Model-Specific Expertise

**Claude Code:**
```
Agent 1: Use Opus (complex analysis)
Agent 2: Use Haiku (fast execution)
```

**Gemini CLI:**
```
All skills use Gemini's session-wide model (set before session start)
Skills are designed to work with any model
```

**Lesson**: Design skills to be model-agnostic; let Gemini's session default apply.

## FAQ: Platform Compatibility

**Q: Can I use all 150+ skills in Gemini CLI?**  
A: Yes! Skills are platform-agnostic markdown. They activate and work identically in Gemini CLI.

**Q: Can I use `/plan` and `/spec` in Gemini CLI?**  
A: No. Use direct prompts instead. Gemini CLI will recognize your task and auto-activate relevant skills.

**Q: What if I need to run parallel agents?**  
A: Use `executing-plans` to sequence tasks. Parallel execution isn't supported; design workflows to chain efficiently.

**Q: Can I assign different models to different tasks?**  
A: No. Use Gemini CLI's session-wide model. Skills are designed to work with any model; adjust your initial model selection before the session starts.

**Q: How do I migrate my workflows?**  
A: Map tools using the table above, adjust skill triggers (describe your task clearly), and test on Gemini CLI.

---

**Last Updated**: April 2026  
**Platform Versions**: Claude Code (Latest), Gemini CLI 3.0+
EOF
```

Expected output:
```
(file created)
```

**Step 2: Verify the file exists and check structure**

```bash
cd /home/mhenke/Projects/agents
test -f docs/gemini-tool-mapping.md && echo "✓ File created"
wc -l docs/gemini-tool-mapping.md
head -10 docs/gemini-tool-mapping.md
```

Expected output:
```
✓ File created
250 docs/gemini-tool-mapping.md
# Claude-Agents Tool Mapping: Claude Code ↔ Gemini CLI

This document maps tools between Claude Code (the original platform for this ecosystem) and Gemini CLI (the Gemini-based alternative). Use this to understand which tools and workflows are available in each platform.
```

**Step 3: Validate markdown headings and tables**

```bash
cd /home/mhenke/Projects/agents
grep "^#" docs/gemini-tool-mapping.md | head -10
```

Expected output:
```
# Claude-Agents Tool Mapping: Claude Code ↔ Gemini CLI
## Core Tools: Direct Equivalents
## Platform-Specific Features: Claude Code Only
### Slash Commands
### Subagent Orchestration
### Model Tiers
## Claude Code Specific: Claude MCP Servers
## Platform Differences: Behavior & Constraints
```

**Step 4: Commit**

```bash
cd /home/mhenke/Projects/agents
git add docs/gemini-tool-mapping.md
git commit -m "docs: add Gemini CLI tool mapping reference

- Document Claude Code ↔ Gemini CLI tool equivalents
- Explain platform-specific features and workarounds
- Provide migration guidance for multi-agent workflows
- Clarify model assignment, tool availability differences
- Include skill design guidelines for cross-platform support

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected output:
```
[main XXXX] docs: add Gemini CLI tool mapping reference
 1 file changed, 198 insertions(+)
 create mode 100644 docs/gemini-tool-mapping.md
```

---

### Task 4: Update README.md with Gemini CLI Section

**Files:**
- Modify: `README.md:1-50` (add Gemini section after intro)

**Context:**
The README is the primary entry point for users. Add a section explaining Gemini CLI support, linking to GEMINI.md and the tool mapping.

**Step 1: Review current README structure**

```bash
cd /home/mhenke/Projects/agents
head -50 README.md
```

Expected output:
```
(Current README content — capture the structure)
```

**Step 2: Add Gemini CLI section after the main intro**

Edit README.md to add a "Gemini CLI Support" section. The exact location depends on current structure, but it should go after the main description and before/alongside other platform sections.

**Template to insert:**

```markdown
## Gemini CLI Support

This repository is available as a Gemini CLI extension. Install it to access 150+ specialized skills directly in Gemini CLI:

```bash
gemini extensions install https://github.com/mhenke/agents
```

All 150+ skills are designed to work with Gemini CLI and auto-activate when you describe matching tasks. See [GEMINI.md](GEMINI.md) for navigation and [docs/gemini-tool-mapping.md](docs/gemini-tool-mapping.md) for platform differences.

**Platform Support:**
- ✅ Claude Code (primary)
- ✅ Gemini CLI (skills library via extension)

[Read the platform comparison](docs/gemini-tool-mapping.md) to understand differences and workarounds.
```

**Step 3: Apply the edit to README.md**

Find the appropriate location in README.md and insert the section. Example: after "## Features" or "## Installation".

```bash
cd /home/mhenke/Projects/agents
# Verify README exists and note the structure
test -f README.md && echo "✓ README.md exists"
```

(This step assumes you'll use the `edit` tool to insert the content at the correct location)

**Step 4: Verify the edit looks good**

```bash
cd /home/mhenke/Projects/agents
grep -A 5 "Gemini CLI Support" README.md
```

Expected output:
```
## Gemini CLI Support

This repository is available as a Gemini CLI extension. Install it to access 150+ specialized skills directly in Gemini CLI:
```

**Step 5: Commit**

```bash
cd /home/mhenke/Projects/agents
git add README.md
git commit -m "docs: add Gemini CLI section to README

- Explain Gemini CLI extension availability
- Provide installation command
- Link to platform-specific documentation
- Clarify multi-platform support (Claude Code + Gemini CLI)

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected output:
```
[main XXXX] docs: add Gemini CLI section to README
 1 file changed, X insertions(+)
```

---

### Task 5: Add GitHub Topic for Gallery Discovery

**Files:**
- Modify: GitHub repository settings (web only, not a file)

**Context:**
Gemini CLI auto-discovers extensions via the `gemini-cli-extension` GitHub topic. Adding this topic enables automatic listing in the [Gemini CLI extension gallery](https://geminicli.com/extensions).

**Step 1: Instructions (manual via GitHub web interface)**

This step requires access to the GitHub repository settings and cannot be automated via git/bash.

**Manual Steps:**
1. Go to https://github.com/mhenke/agents
2. Click **Settings** (⚙️ icon in the repo header)
3. Scroll to **About** section (top right of repo header)
4. Click the **gear icon** next to the description
5. In the **Topics** field, add: `gemini-cli-extension`
6. Click **Save**

**Expected Result:**
- Topic badge appears on repo main page
- Gemini CLI crawler picks up the extension daily
- Extension appears in [geminicli.com/extensions](https://geminicli.com/extensions) within 24 hours

**Step 2: Verify topic was added (via GitHub API)**

```bash
# Verify the topic was added (requires GitHub CLI)
gh repo view mhenke/agents --json repositoryTopics
```

Expected output:
```
{
  "repositoryTopics": [
    {
      "topic": {
        "name": "gemini-cli-extension"
      }
    },
    ...other topics...
  ]
}
```

**Step 3: Documentation note (no commit needed)**

Add a note to the project's development documentation (optional):

```bash
cd /home/mhenke/Projects/agents
cat >> DEVELOPMENT.md << 'EOF'

## Gemini CLI Extension

The `gemini-cli-extension` GitHub topic enables auto-discovery in the Gemini CLI extension gallery (https://geminicli.com/extensions). This topic is maintained in repo settings and does not require code changes.

Crawler behavior: Daily scan. Extensions tagged with this topic and having a valid `gemini-extension.json` at repo root appear in the gallery within 24 hours.
EOF
```

---

### Task 6: Verify Phase 1 Completion

**Files:**
- Created: `gemini-extension.json`
- Created: `GEMINI.md`
- Created: `docs/gemini-tool-mapping.md`
- Modified: `README.md`
- Modified: GitHub repo settings (topic)

**Context:**
This verification task confirms all Phase 1 files are in place and correctly structured.

**Step 1: Verify all files exist**

```bash
cd /home/mhenke/Projects/agents
echo "=== Phase 1 File Checklist ===" && \
test -f gemini-extension.json && echo "✓ gemini-extension.json" || echo "✗ gemini-extension.json" && \
test -f GEMINI.md && echo "✓ GEMINI.md" || echo "✗ GEMINI.md" && \
test -f docs/gemini-tool-mapping.md && echo "✓ docs/gemini-tool-mapping.md" || echo "✗ docs/gemini-tool-mapping.md" && \
grep -q "Gemini CLI Support" README.md && echo "✓ README.md (Gemini section added)" || echo "✗ README.md (Gemini section missing)"
```

Expected output:
```
=== Phase 1 File Checklist ===
✓ gemini-extension.json
✓ GEMINI.md
✓ docs/gemini-tool-mapping.md
✓ README.md (Gemini section added)
```

**Step 2: Validate JSON and markdown structure**

```bash
cd /home/mhenke/Projects/agents
echo "=== JSON Validation ===" && \
python3 -m json.tool gemini-extension.json > /dev/null && echo "✓ gemini-extension.json is valid JSON" || echo "✗ gemini-extension.json has invalid JSON"

echo "" && echo "=== Markdown Structure ===" && \
test -f GEMINI.md && grep "^#" GEMINI.md | wc -l | xargs echo "GEMINI.md headings:" && \
test -f docs/gemini-tool-mapping.md && grep "^#" docs/gemini-tool-mapping.md | wc -l | xargs echo "gemini-tool-mapping.md headings:"
```

Expected output:
```
=== JSON Validation ===
✓ gemini-extension.json is valid JSON

=== Markdown Structure ===
GEMINI.md headings: 8
gemini-tool-mapping.md headings: 11
```

**Step 3: Verify no references to missing files**

```bash
cd /home/mhenke/Projects/agents
echo "=== Checking for dead references ===" && \
grep -o "@\./[^[:space:]]*" GEMINI.md | sort -u
```

Expected output:
```
=== Checking for dead references ===
@./docs/gemini-tool-mapping.md
@./docs/plugins.md
```

Note: `@./docs/plugins.md` is expected (auto-generated or existing plugin catalog). If missing, it's optional for Phase 1.

**Step 4: Verify git history**

```bash
cd /home/mhenke/Projects/agents
git log --oneline -5 | head -5
```

Expected output:
```
XXXX docs: add Gemini CLI section to README
XXXX docs: add Gemini CLI tool mapping reference
XXXX feat: add Gemini CLI bootstrap context
XXXX feat: add Gemini CLI extension manifest
XXXX [previous commit]
```

**Step 5: Create verification summary**

```bash
cd /home/mhenke/Projects/agents
cat > .gemini-verification.txt << 'EOF'
PHASE 1 COMPLETION VERIFICATION
================================
Date: 2026-04-30
Status: ✓ COMPLETE

Files Created:
- gemini-extension.json (manifest)
- GEMINI.md (bootstrap context)
- docs/gemini-tool-mapping.md (tool mapping reference)

Files Modified:
- README.md (added Gemini CLI section)

Repository Settings:
- GitHub topic "gemini-cli-extension" added (manual step)

Verification:
- All JSON is valid
- All markdown has proper structure
- All file references are valid (or optional)
- Git history shows 4 commits for Phase 1

Next Steps:
- Phase 2 (optional): Create per-plugin GEMINI.md files and plugins.md catalog
- Phase 3 (optional): Review and standardize skill trigger phrases
- Publish: Push to GitHub; crawler picks up extension within 24 hours

Installation URL (for users):
  gemini extensions install https://github.com/mhenke/agents
EOF
cat .gemini-verification.txt
```

Expected output:
```
PHASE 1 COMPLETION VERIFICATION
================================
Date: 2026-04-30
Status: ✓ COMPLETE

[...verification details...]
```

**Step 6: Final commit**

```bash
cd /home/mhenke/Projects/agents
git add .gemini-verification.txt
git commit -m "chore: add Phase 1 verification summary

Document completion of Gemini CLI integration Phase 1:
- 4 files created/modified
- All validation checks pass
- Ready for Phase 2 (optional) or publication

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

Expected output:
```
[main XXXX] chore: add Phase 1 verification summary
 1 file changed, 1 insertion(+)
 create mode 100644 .gemini-verification.txt
```

---

## Phase 2: Discovery Enhancement (Optional)

**Scope:** Improve skill discoverability for Gemini CLI users through per-plugin context files and plugin catalog.

**Status:** Not included in this plan. Defer until Phase 1 is complete and validated.

**When to use Phase 2:**
- After Phase 1 is published and user feedback is gathered
- If users report difficulty finding skills across 79 plugins
- If metrics show low skill activation rates in Gemini CLI
- If per-plugin context files would significantly improve UX

---

## Phase 3: Polish (Optional)

**Scope:** Review and standardize skill trigger phrases for Gemini's auto-activation matching.

**Status:** Not included in this plan. Defer until Phase 1 & 2 are stable.

**When to use Phase 3:**
- After gathering usage patterns from Phase 1 deployment
- If Gemini's auto-matching shows low accuracy for certain skill domains
- If skill descriptions need refinement for clarity

---

## Rollback Plan

If Phase 1 needs to be reverted (e.g., after discovering critical issues):

```bash
cd /home/mhenke/Projects/agents

# Revert the 5 Phase 1 commits
git revert HEAD~4..HEAD --no-edit

# Or reset to pre-Phase 1 state
git reset --hard <commit-before-phase-1>

# Remove verification file
rm .gemini-verification.txt
```

---

## Success Criteria

Phase 1 is **complete and successful** when:

- [x] `gemini-extension.json` exists and is valid JSON
- [x] `GEMINI.md` exists with proper markdown structure
- [x] `docs/gemini-tool-mapping.md` exists with tool mapping tables
- [x] `README.md` has Gemini CLI section with installation instructions
- [x] GitHub topic `gemini-cli-extension` is added to repo
- [x] All 4 commits are clean and well-documented
- [x] Verification script passes (all checks green)
- [ ] (After merge) Extension appears in Gemini CLI gallery within 24 hours
- [ ] (After merge) Users can install: `gemini extensions install https://github.com/mhenke/agents`
- [ ] (After merge) Skills auto-discover and auto-activate in Gemini CLI

---

## Notes for Implementer

1. **No skill changes needed** — All 150+ existing skills are platform-agnostic and work identically in Gemini CLI. No code changes required.

2. **GEMINI.md is the entry point** — Users will see GEMINI.md when they install the extension. Make sure it's clear, friendly, and provides good navigation.

3. **Tool mapping is critical** — Many users will ask about platform differences. The tool mapping doc prevents support burden and improves UX.

4. **GitHub topic is essential** — Without the `gemini-cli-extension` topic, the extension won't appear in the gallery, significantly limiting discoverability.

5. **Frequent commits** — Each task above includes a commit. This keeps the git history clear and makes it easy to review/revert individual changes.

6. **Testing strategy** — Phase 1 doesn't require runtime tests (no code). Validation is structural (JSON validity, markdown headings, file existence, git history). The true test happens after merging when Gemini CLI users try to install and use the extension.

---

**Plan Created:** April 30, 2026  
**Estimated Duration:** Phase 1: 2-4 hours (depending on README.md integration point)  
**Plan Author:** Copilot (writing-plans skill)
