# Gemini CLI Tool Mapping Reference

A comprehensive guide for users migrating from Claude Code to Gemini CLI. This document maps tool equivalents, explains platform-specific features, and provides migration guidance for skills.

## 1. Core Tools: Direct Equivalents

| Claude Code Tool | Gemini CLI Tool | Purpose | Notes |
|------------------|-----------------|---------|-------|
| `view` | `read_file` | Read file contents | Gemini: Reads single files only; use for full file context |
| `create` | `write_file` | Create new files | Both: File must not exist; must have parent directories |
| `edit` | `write_file` (overwrite) | Modify file contents | Gemini: No partial edit; rewrite entire file content |
| `bash` | `run_shell_command` | Execute shell commands | Gemini: Synchronous only, no async/detach modes |
| `grep` | `grep_search` | Search file contents | Gemini: Simpler API; uses patterns only (no context flags) |
| `glob` | File system iteration | Find files by pattern | Gemini: Use `run_shell_command` with `find` instead |
| `web_fetch` | `web_search` / `fetch_url` | Retrieve web content | Gemini: Separate tools for search vs. fetch |
| LSP/editor tools | Code navigation tools | Language server integration | Gemini: Via run_shell_command with language servers |

### Key Differences in Tool Behavior

**File Operations:**
- Claude Code `edit` performs surgical string replacement; Gemini requires full file rewrite
- Claude Code `view` supports view_range for large files; Gemini `read_file` reads entire content
- Claude Code `create` prevents overwriting; Gemini `write_file` requires explicit overwrite flag

**Shell Execution:**
- Claude Code `bash` supports `mode: "async"` and `detach: true`; Gemini is synchronous only
- Claude Code `bash` supports `initial_wait` parameter; Gemini uses simple timeout
- Both support shell expansion and piping; both require command input as string

**Search & Navigation:**
- Claude Code `grep` supports multiline matching and context flags (-B, -A, -C)
- Gemini `grep_search` is simpler: pattern-based matching in specified paths
- Claude Code `glob` is built-in; Gemini uses `find` command via `run_shell_command`

---

## 2. Platform-Specific Features: Claude Code Only

The following features are **unique to Claude Code** and do not have direct Gemini CLI equivalents. Skills designed for cross-platform compatibility should avoid relying on these features.

### Global Slash Commands (`/plan`, `/spec`, `/ship`)
**Claude Code:** Global entry points that trigger predefined workflows
```
/plan - Structured planning skill execution
/spec - Specification writing and review
/ship - Finalization and delivery checklist
```

**Gemini CLI Status:** Gemini CLI **does support custom slash commands** via TOML files. However, Gemini's commands are extension-specific and plugin-namespaced (e.g., `/security-scan`, `/conductor:orchestrate`), not global workflow shortcuts.

**Gemini CLI Implementation:** Custom commands defined in `commands/` directory. Users can:
- Type `/` to see all available commands in the current extension
- Invoke plugin-specific commands: `/plugin-name`, `/plugin-name:command-name`
- Skills auto-activate by name matching for tasks without explicit commands

If your skill needs global triggering (like Gemini's `/plan` equivalent), structure it for auto-activation by intent matching rather than explicit command invocation.

### Subagent Orchestration (Parallel Execution)
**Claude Code:** `task` tool dispatches parallel subagents (explore, task, code-review, general-purpose, custom agents)
```python
# Claude Code pattern
task(agent_type="explore", prompt="Search 3 codebases")  # Runs in parallel
task(agent_type="code-review", prompt="Review PR")       # Runs in parallel
```

**Gemini CLI Workaround:** Sequential execution only. Skills can batch work but cannot fan-out:
```
Use the superpowers:executing-plans skill to batch related tasks
Use the dispatching-parallel-agents skill to conceptually organize parallel work
```

### Per-Agent Model Assignment
**Claude Code:** Each subagent can run with different model tiers (Opus, Sonnet, Haiku)
```python
# Claude Code pattern
task(agent_type="explore", model="claude-haiku-4.5")     # Fast/cheap
task(agent_type="code-review", model="claude-opus-4")    # High quality
```

**Gemini CLI Workaround:** Session-level model only. All work uses the current session's model:
```
gemini --model=gemini-2.0-pro      # High quality for code review
gemini --model=gemini-1.5-mini     # Fast for exploratory work
```

### MCP Server Integration
**Claude Code:** Direct access to Model Context Protocol servers for extended capabilities
**Gemini CLI:** Uses native extensions instead. Configure via `gemini extensions`.

---

## 3. Claude Code Specific: MCP Servers

**Model Context Protocol (MCP)** is a Claude Code feature that allows integration with specialized servers. MCP servers provide additional capabilities beyond built-in tools.

### What are MCP Servers?

MCP servers are external processes that Claude Code can communicate with to access specialized tools and data sources:
- **GitHub MCP Server**: Unified access to GitHub APIs (repos, PRs, issues, actions, code search)
- **SQLite MCP Server**: Query relational databases within Claude Code context
- **Custom MCP Servers**: User-defined servers for domain-specific capabilities

### Usage Pattern in Claude Code
```python
# Invoke MCP server via tool call
github_mcp_server_search_code(query="find Authentication.ts", repo="myapp")
github_mcp_server_list_issues(owner="myorg", repo="myapp")
```

### Gemini CLI Migration Path

If a skill relies heavily on MCP servers:

1. **GitHub Operations**: Use `run_shell_command` with `gh` CLI (GitHub CLI)
   ```bash
   gh repo view owner/repo --json nameWithOwner,description
   gh pr list --search "is:open"
   gh api /search/code --input query
   ```

2. **Database Queries**: Use `run_shell_command` with `sqlite3` or language-specific clients
   ```bash
   sqlite3 database.db "SELECT * FROM users WHERE active = 1;"
   ```

3. **Custom Servers**: Deploy as standalone services and communicate via HTTP/webhooks with Gemini CLI

See [docs/plugins.md](docs/plugins.md) for Gemini-native plugins that provide similar capabilities.

---

## 4. Platform Differences: Behavior & Constraints

### Context Limits & Token Management

| Aspect | Claude Code | Gemini CLI |
|--------|-----------|-----------|
| **Context Window** | Model-dependent (200K for Opus) | Model-dependent (varies by Gemini version) |
| **Session Context** | Per-agent isolation | Single session context |
| **Skill Loading** | Full skill text loaded per invocation | Skill description only; full text on demand |
| **File Content** | Cached in conversation history | Re-read on demand |

**Implication:** Gemini CLI skills should minimize context waste by:
- Avoiding unnecessary file reads
- Batching related operations
- Clearing context after long-running tasks

### Tool Availability

| Tool | Claude Code | Gemini CLI | Note |
|------|-----------|-----------|------|
| File operations | Full support | Limited (read/write only) | No partial edits; full rewrite required |
| Shell execution | Full async + sync | Sync only | No background processes or detached modes |
| Browser automation | Full Playwright support | Via run_shell_command | Use external browser tools |
| Code search | Built-in + MCP | Via gh CLI or grep_search | Less sophisticated than MCP |
| AI model access | Fixed per task | Session-wide | All operations use same model |

### Error Handling & Retry Logic

**Claude Code:** Automatic retry on transient failures; model-specific behavior
**Gemini CLI:** Manual error handling required; tools return exit codes and stderr

```bash
# Gemini CLI pattern: Check exit code explicitly
if ! git clone URL; then
    echo "Clone failed" >&2
    exit 1
fi
```

---

## 5. Skill Design Guidelines: Gemini Compatibility

When designing or porting skills to Gemini CLI, follow these DO's and DON'Ts to ensure compatibility.

### DO's: Portable, Platform-Agnostic Skills

✅ **Use simple shell commands** instead of tool abstractions
```bash
# Good: Works on both platforms
find . -name '*.ts' -type f
grep -r 'import.*auth' src/
```

✅ **Structure skills for sequential execution** with batched operations
```bash
# Good: Batch related work in one task
for task in lint test build; do
    npm run "$task"
done
```

✅ **Read files once, reuse in context** rather than multiple reads
```bash
# Good: Single read, reuse content
config=$(cat config.json)
# Process config multiple times from variable
echo "$config" | jq '.key'
```

✅ **Provide explicit error messages** for debugging
```bash
if ! npm install; then
    echo "Installation failed" >&2
    echo "Workaround: Use 'npm ci' for CI environments" >&2
    exit 1
fi
```

### DON'Ts: Platform-Specific Anti-Patterns

❌ **Don't rely on subagent parallelism**
```bash
# Bad: Gemini can't run in parallel
# task(agent_type="explore", prompt="...")  # Claude Code only
# task(agent_type="code-review", prompt="...")  # Claude Code only
# Gemini will serialize these
```

❌ **Don't use per-agent model assignment**
```bash
# Bad: Gemini doesn't support per-task models
# task(agent_type="explore", model="haiku")  # Claude Code only
# task(agent_type="review", model="opus")  # Claude Code only
# This pattern doesn't translate to Gemini
```

❌ **Don't perform partial file edits with expectation of atomicity**
```bash
# Bad: Gemini requires full file rewrite
# edit(file, old_str="x", new_str="y")  # Claude Code only
# Use: read entire file, make all changes, write once
```

❌ **Don't assume shell features beyond POSIX basics**
```bash
# Bad: Not portable across all systems
pushd /tmp && do_work && popd  # May not work in all shells
# Good: Use cd with && chaining
cd /tmp && do_work && cd -
```

---

## 6. Migration Path: Adapting Claude Code Skills

### Step 1: Identify Tool Usage
Audit your Claude Code skill for:
- Subagent dispatches (`task()` calls)
- Partial file edits (`edit()` calls)
- Async shell execution (`mode="async"`)
- MCP server calls

### Step 2: Replace Unsupported Patterns
| Claude Code Pattern | Gemini CLI Equivalent |
|-------------------|----------------------|
| `task(agent_type="X")` | Inline the task; batch operations in skill |
| `edit(file, old_str="X", new_str="Y")` | `read_file` → modify → `write_file` |
| `bash(mode="async", detach=true)` | `run_shell_command` with nohup/background |
| `github_mcp_server_*` | `gh` CLI via `run_shell_command` |

### Step 3: Update Skill Description
Gemini CLI auto-discovers skills by name and description. Update your SKILL.md:

```markdown
# My Migrated Skill

**Platform Compatibility:** Claude Code, Gemini CLI
**Activation Trigger:** When user asks to "...feature..."
**Model Fit:** Works well with [model type]

## Differences from Claude Code
- Now uses sequential execution instead of parallel subagents
- File operations use read/write instead of partial edits
- Shell commands are synchronous only

## Usage
```

### Step 4: Test Both Platforms
- Run skill in Claude Code to verify original behavior
- Run skill in Gemini CLI to verify new implementation
- Document any behavioral differences

---

## 7. Common Patterns: Side-by-Side Examples

### Pattern: Search and Replace in Multiple Files

**Claude Code Approach (Partial Edits):**
```python
files = glob("src/**/*.ts")
for file in files:
    content = view(file)
    if "oldString" in content:
        edit(file, old_str="oldString", new_str="newString")
```

**Gemini CLI Approach (Full Rewrites):**
```bash
# Batch read and write
for file in $(find src -name "*.ts" -type f); do
    if grep -q "oldString" "$file"; then
        content=$(cat "$file" | sed 's/oldString/newString/g')
        echo "$content" > "$file"
    fi
done
```

Or use a language-aware tool:
```bash
# Using ripgrep and sed for atomic operations
find src -name '*.ts' -type f -exec sed -i 's/oldString/newString/g' {} +
```

### Pattern: Code Review Workflow

**Claude Code (Parallel Subagents):**
```python
# Parallel execution
task(agent_type="code-review", prompt="Review API changes")
task(agent_type="code-review", prompt="Review UI changes")
```

**Gemini CLI (Sequential with Batching):**
```bash
# Sequential but organized
echo "=== Reviewing API changes ==="
# Review logic here

echo "=== Reviewing UI changes ==="
# Review logic here

# Or use a skill that handles review orchestration internally
```

### Pattern: File Reading with Large File Support

**Claude Code (with view_range):**
```python
# Read specific section
content = view("large_file.js", view_range=[100, 150])
```

**Gemini CLI (read entire, then parse):**
```bash
# Invoke read_file via Gemini CLI tool
# Read full file into variable - requires running through Gemini tool
# Example: read the file, then extract lines in shell
sed -n '100,150p' large_file.js
```

### Pattern: Conditional Shell Execution

**Claude Code (with proper error handling):**
```python
result = bash("npm run test", initial_wait=60)
if result.exit_code == 0:
    bash("npm run build")
else:
    print("Tests failed; skipping build")
```

**Gemini CLI (explicit error checking):**
```bash
# Run npm test and check exit code
npm run test
if [ $? -eq 0 ]; then
    npm run build
else
    echo "Tests failed; skipping build"
fi
```

---

## 8. FAQ: Troubleshooting & Common Questions

### Q: I have a Claude Code skill with multiple subagents. Can I port it to Gemini CLI?

**A:** Yes, but the architecture changes. Instead of parallel subagent execution, skills in Gemini CLI:
1. Execute sequentially within a single skill context
2. Batch related work to minimize redundant operations
3. Use the `superpowers:executing-plans` skill to organize complex workflows

**Example:** A code review orchestration skill might process all files in one skill invocation rather than dispatching separate review subagents.

---

### Q: My Claude Code skill uses `edit()` for small string replacements. How do I do this in Gemini CLI?

**A:** `read_file` → modify in memory/string processing → `write_file`:

```bash
# Gemini CLI pattern: read, transform, write
content=$(cat config.json)
updated=$(echo "$content" | sed 's/"old_key": "old_value"/"old_key": "new_value"/g')
echo "$updated" > config.json
```

For multiple edits to the same file, collect all changes, then write once to minimize I/O.

---

### Q: Can I use the same MCP server calls in Gemini CLI?

**A:** No. Replace MCP calls with native tools:
- **GitHub MCP** → Use `gh` CLI (GitHub CLI installed separately)
- **SQLite MCP** → Use `sqlite3` command-line tool
- **Custom MCP** → Deploy as HTTP service, call with `curl` via `run_shell_command`

Example: Replace `github_mcp_server_list_issues()` with:
```bash
gh issue list --repo owner/repo --json number,title,state
```

---

### Q: My skill times out in Gemini CLI. What's different from Claude Code?

**A:** Possible causes:
1. **Large file reads** → Gemini reads entire file; Claude Code supports view_range. Read strategically.
2. **Complex shell commands** → Long-running operations may hit timeouts. Add explicit wait/retry logic.
3. **Synchronous-only execution** → You can't spawn background processes like in Claude Code async mode.

**Solution:** Break long operations into checkpoints, report progress, and allow user to retry if needed.

---

### Q: How do I run background tasks in Gemini CLI?

**A:** Gemini CLI doesn't support detached async processes. Instead:

1. **Use `nohup` with output redirection:**
   ```bash
   nohup npm run watch > build.log 2>&1 &
   ```

2. **Check status later:**
   ```bash
   ps aux | grep 'npm run watch'
   tail -f build.log
   ```

3. **For long-running tasks**, use the skill's built-in checkpointing to allow resumption.

---

### Q: What if a Gemini CLI user runs my skill designed for Claude Code?

**A:** The skill will fail on unsupported features:
- Subagent `task()` calls → Error: "task tool not available"
- Async execution → Shell commands won't start background processes
- MCP server calls → Error: "Unknown tool"

**Best Practice:** Clearly mark skills as "Claude Code Only" or "Cross-Platform" in your SKILL.md metadata. Provide alternative instructions for Gemini CLI users.

---

### Q: How does model selection work in Gemini CLI skills?

**A:** Gemini CLI doesn't support per-agent model assignment. All operations in a skill use the session-wide model:

```bash
# Start session with specific model
gemini --model=gemini-2.0-pro

# Skill cannot override this model
# All skill operations use gemini-2.0-pro
```

**For skills that need different model tiers:** Document that users should run the skill multiple times with different session models, or use the superpowers:executing-plans skill to conceptually separate high-quality vs. fast operations.

---

## Summary: Quick Reference

### When Porting a Claude Code Skill to Gemini CLI

| Issue | Solution |
|-------|----------|
| Multiple subagents in parallel | Batch work in single skill; use executing-plans for organization |
| Partial file edits | Read full file, modify, write back |
| Async shell execution | Use `nohup` or shell control flow; monitor with polling |
| MCP server access | Use `gh` CLI, `sqlite3`, or HTTP requests via `curl` |
| Model-specific tuning | Document model recommendations; users select model at session start |
| Slash command entry points | Update skill description; trigger on intent matching |

### Minimal Viable Port Checklist

- [ ] Replace all `task()` calls with inline logic or sequential execution
- [ ] Replace all `edit()` calls with read-modify-write patterns
- [ ] Replace MCP server calls with native tools or CLI equivalents
- [ ] Test shell commands for POSIX compatibility
- [ ] Update SKILL.md with platform compatibility notes
- [ ] Document Gemini CLI–specific behavior differences

---

**Last Updated:** April 2026  
**For more information:** See [GEMINI.md](../GEMINI.md) for feature overview and [docs/plugins.md](plugins.md) for available plugins.
