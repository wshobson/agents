---
name: scan
description: Scans the codebase to generate project-doc.md and AGENTS.md. Use when bootstrapping a new agent-driven repo, refreshing project documentation after architectural changes, or running a delta scan to detect drift. Runs a full scan on first use and a smart delta scan on subsequent runs. Uses understand-anything + context-mode when available, falls back to native tools otherwise. Only updates AGENTS.md on detected architectural changes with human confirmation.
---

# Codebase Scanner

You are a technical analyst. Your job is to scan the project codebase and produce accurate, project-specific documentation used by all downstream agents.

## Step 1: Check Optional Plugin Dependencies

Check whether the two optional enhancement plugins are available:

```
understand-anything  →  /plugin list | grep understand-anything
context-mode         →  /plugin list | grep context-mode
```

These plugins are **optional**. They improve scan quality but are not required:

- **understand-anything** (Lum1104/Understand-Anything) — provides deeper semantic code analysis
- **context-mode** (mksglu/context-mode) — routes large outputs through a sandbox to protect the context window

If both are present, use them in Steps 3–4 as described below. If either or both are missing, proceed with the **native fallback** approach: use `find`, `grep`, `cat`, and `git` commands directly, routing large outputs through `ctx_execute` / `ctx_execute_file` if context-mode is available, otherwise summarise inline.

> **Note:** To install the optional plugins manually:
> ```
> /plugin marketplace add Lum1104/Understand-Anything && /plugin install understand-anything
> /plugin marketplace add mksglu/context-mode && /plugin install context-mode@context-mode
> ```

## Step 2: Determine Scan Mode

Check if `.claude/pipeline/project-doc.md` exists.

- **Does not exist** → FULL SCAN (first run)
- **Exists** → DELTA SCAN

## Step 3A: Full Scan

Use `understand-anything` to analyse the entire codebase. If **context-mode** is available (verified in Step 1), route ALL output through its tools (`ctx_batch_execute` / `ctx_execute_file`) — never dump raw file contents into the main context window. If context-mode is not available, summarise each file's findings inline and avoid printing raw file contents.

Produce `.claude/pipeline/project-doc.md` using the following structure (based on the architecture-blueprint-generator pattern):

```md
# Project Documentation
> Generated: [timestamp] | Mode: FULL

## Tech Stack
- Runtime: [e.g. Node.js 20, Python 3.11]
- Language: [e.g. TypeScript, Python]
- Framework: [e.g. Next.js 14 App Router, FastAPI]
- Database: [e.g. PostgreSQL via Prisma]
- Styling: [e.g. Tailwind CSS]
- State Management: [e.g. Zustand, Redux]

## Dependencies
[Key libraries with versions, grouped by: core / dev / testing]

## Architecture Pattern
[e.g. Feature-based, Layered MVC, Clean Architecture]
[Describe how the project is structured and why]

## Folder Structure
[Top-level directory map with purpose of each folder]

## Code Style Conventions
[Naming patterns, file naming, import ordering, export patterns]
[Inferred from actual code — not guessed]

## Modularity Practices
[How concerns are separated, shared module locations, service patterns]

## Data Architecture
[Entity relationships, data access patterns, ORM usage]

## Cross-Cutting Concerns
[Auth/authz approach, error handling patterns, logging, validation]

## Service Communication
[REST / GraphQL / event-driven — document what actually exists]

## Test Coverage
- Overall coverage: [X%]
- Testing framework: [e.g. Jest, Vitest, Pytest]
- Key untested areas: [list]
- Test patterns used: [unit / integration / e2e]

## Entry Points
[Main files, key config files, environment setup]

## Changed Files
[Only present in delta scans — list of files re-scanned]

## Last Scanned
[ISO timestamp]
```

After writing `project-doc.md`, proceed to **Step 4** to generate `AGENTS.md`.

## Step 3B: Delta Scan

1. Run `git diff HEAD~1 --name-only` to get changed files
2. If no changed files, report "No changes detected — project-doc.md is current" and exit
3. Use `understand-anything` to re-analyse only the changed files; route output through `ctx_execute_file` if context-mode is available, otherwise summarise inline
4. Patch only the affected sections of `.claude/pipeline/project-doc.md`
5. Update the `Last Scanned` and `Changed Files` fields
6. Proceed to **Step 4B** (architectural change detection)

## Step 4A: Generate AGENTS.md (First Run Only)

Write `AGENTS.md` to the repo root. This is NOT a copy of `project-doc.md` — it is rewritten as agent instructions, tailored to this specific project. Every agent reads this file first.

Before writing AGENTS.md, read and follow the complete [project-specific instruction template](references/agents-template.md), including its security rules and human-confirmed update requirements.

If the project is MERN stack (MongoDB + Express + React + Node.js — detected from package.json / requirements), append a `### MERN Stack Notes` section to AGENTS.md covering: use Mongoose middleware over raw queries, handle async errors in Express with a central error handler, avoid storing JWT tokens in localStorage (use httpOnly cookies), and never expose Mongoose error objects directly in API responses.

## Step 4B: Architectural Change Detection (Delta Runs Only)

After patching `project-doc.md`, compare the new version against the previous. Check for:
- New framework or major library added
- New architectural directory pattern created (e.g. new `/lib/hooks/`, `/services/`)
- Major dependency swap (e.g. axios → fetch, moment → dayjs)
- New auth or session handling pattern

If any detected, show:

```
⚠️  Architectural change detected in delta scan:
    [List specific changes found]

AGENTS.md may need updating. Review and confirm:
  [y] Update AGENTS.md — patch affected sections only
  [n] Skip — this is not an architectural change
```

Only on `[y]` confirmation: patch the relevant sections of `AGENTS.md`. Never rewrite the full file.

## Step 5: Report

Print a summary:

```
✅ Scan complete ([FULL/DELTA])
   project-doc.md → updated
   AGENTS.md      → [generated / patched / unchanged]
   Changed files  → [N files re-scanned / N/A for full scan]
   Coverage       → [X%]
```

Update `state.json` field `checkpoints.scan = "completed"`.
