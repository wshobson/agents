---
description: Use when preparing to let an AI coding agent modify a repository; produce a preflight safety receipt before changes begin.
argument-hint: "optional target path, branch, or risk focus"
---

# Agent Preflight Safety Receipt

Use this command when a developer, maintainer, or small team wants a quick safety receipt before Claude Code, Codex, Cursor, or another AI coding agent edits a real repository.

## Context

$ARGUMENTS

## Instructions

1. Confirm repository state.
   - Identify the current branch and whether there are uncommitted changes.
   - Refuse to proceed silently if user work is dirty; report the exact files first.
   - Note the latest commit SHA or state that no Git repository is present.

2. Map the blast radius.
   - List the files or directories the requested agent work is likely to touch.
   - Flag sensitive areas such as payment code, deployment config, credentials, migrations, CI, auth, security policy, or production data paths.
   - If the work touches a sensitive area, name the risk and ask for explicit confirmation before mutation.

3. Find the cheapest validation path.
   - Detect available test, lint, typecheck, build, or smoke commands from package scripts, Makefile targets, project docs, or obvious framework conventions.
   - Prefer the smallest command that proves the requested change.
   - If no validator is available, state that clearly and suggest one low-friction check.

4. Produce the preflight receipt.
   - Summarize: repo/branch, dirty-state result, risky files, intended edit scope, validation command, rollback plan, and any human approval needed.
   - Keep the receipt copyable into a PR, issue, or handoff note.
   - Do not modify files until the user approves the receipt.

## Output

Return a concise receipt in this format:

```text
Agent preflight receipt
Repo/branch:
Dirty state:
Likely edit scope:
Risk flags:
Validation command:
Rollback plan:
Human approval needed:
Recommended next step:
```

## Related free resource

For a fuller standalone starter pack with sample hooks, checklists, and receipt templates, see:
https://github.com/el-zachariah/ai-agent-safety-starter-pack
