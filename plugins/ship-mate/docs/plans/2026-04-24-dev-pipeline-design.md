# Dev Pipeline Plugin — Design Document
**Date:** 2026-04-24  
**Status:** Approved for Implementation

---

## 1. Overview

A repo-level Claude Code plugin that turns a story file into a shipped, tested, reviewed feature — with minimal human intervention. One command kicks off a six-stage AI pipeline. The only mandatory human checkpoint is approving the architect's plan before implementation begins.

### Entry Point
```bash
/ship stories/forgot-password.md
/ship status
/ship resume
```

### Pipeline Flow
```
SCAN → ORCHESTRATE → ARCHITECT → [PAUSE: human approves plan]
     → IMPLEMENT → REVIEW → QA → [PLAYWRIGHT if FRONTEND]
                                        ↓
                                      DONE
```

### Design Principles
- **One task type per run** — FRONTEND or BACKEND, never both
- **File-based state** — survives session restarts, no external dependencies
- **No LangGraph** — built natively on Claude Code's agent spawning and skill system
- **AGENTS.md as the north star** — every agent reads this first; project-awareness is built in, not prompted each time
- **Loop guards** — review and QA loops cap at 2 iterations before escalating to human (two-handoff rule)

---

## 2. Repository Structure

After plugin installation, the following is added to any project:

```
<project-root>/
├── stories/                          # Story files live here
│   ├── _template.md                  # Starter template
│   └── forgot-password.md            # Example story
├── AGENTS.md                         # Auto-generated, tailored agent instructions
└── .claude/
    ├── skills/
    │   ├── ship.md                   # Master entry point + state router
    │   ├── scan.md                   # Codebase scanner
    │   ├── orchestrate.md            # Product orchestrator agent
    │   ├── architect.md              # Architect agent
    │   ├── implement.md              # Developer agent
    │   ├── review.md                 # PR reviewer agent
    │   ├── qa.md                     # QA agent
    │   └── playwright.md             # Browser test agent (FRONTEND only)
    └── pipeline/
        ├── state.json                # Current pipeline state
        ├── project-doc.md            # Raw codebase report (scanner output)
        ├── orchestrator-output.md    # Clarified spec from orchestrator
        ├── architect-plan.md         # Step-by-step implementation plan
        ├── review-report.md          # PR reviewer findings + resolutions
        └── qa-report.md              # QA findings + pass/fail per criterion
```

---

## 3. Story File Format

Stories live in `stories/` at the repo root. Each file contains one story with multiple tasks. The pipeline processes tasks top-to-bottom, checking them off as each completes.

```md
# Story: Forgot Password Flow

## Description
As a user, I want to reset my password via email so I can regain access if I forget it.

## Acceptance Criteria
- User can request a password reset from the login page
- Reset email is sent within 60 seconds
- Reset link expires after 24 hours
- User can set a new password via the reset link
- Old sessions are invalidated after password reset

## Tasks
- [ ] Add "Forgot Password?" link to login UI
- [ ] POST /api/auth/reset-password endpoint
- [ ] Password reset email template
- [ ] Reset password form page (with token validation)
```

**Rules:**
- Tasks are marked `[x]` as they complete
- Each task is tagged FRONTEND or BACKEND by the architect (not the author)
- One task runs through the full pipeline at a time — no parallelism

---

## 4. State Machine

`state.json` is written and read by every stage. It is the single source of truth for pipeline position.

```json
{
  "story_file": "stories/forgot-password.md",
  "requirement": "Add forgot password flow",
  "task_index": 0,
  "current_task": "Add 'Forgot Password?' link to login UI",
  "task_type": "FRONTEND",
  "stage": "architect",
  "iteration": {
    "review": 0,
    "qa": 0
  },
  "checkpoints": {
    "scan": "completed",
    "orchestrate": "completed",
    "architect": "awaiting_approval",
    "implement": "pending",
    "review": "pending",
    "qa": "pending",
    "playwright": "pending"
  },
  "flags": {
    "review_major_pending": false,
    "qa_bugs_pending": false,
    "escalated": false
  },
  "last_updated": "2026-04-24T10:32:00Z"
}
```

### Stage Routing Logic

```
/ship stories/foo.md
  → read story, extract tasks, set task_index = 0
  → SCAN (delta scan, update project-doc.md + AGENTS.md)
  → ORCHESTRATE (auto, no pause)
  → ARCHITECT → write architect-plan.md → set stage = "awaiting_approval"
  → [PAUSE] human runs /ship resume after reviewing plan
  → IMPLEMENT
  → REVIEW
      if minor flags → auto-fix → re-run REVIEW (iteration.review++)
      if major flags → [PAUSE] human decides → set flag → /ship resume
      if iteration.review >= 2 → escalate to human
  → QA
      if bugs → IMPLEMENT → REVIEW → QA (iteration.qa++)
      if iteration.qa >= 2 → escalate to human
  → if task_type == FRONTEND → PLAYWRIGHT
  → mark task [x] in story.md
  → if more tasks remain → advance task_index → restart from SCAN (delta)
  → DONE — all tasks complete
```

### Commands

| Command | Behaviour |
|---|---|
| `/ship stories/foo.md` | Start fresh pipeline for this story |
| `/ship status` | Print visual stage tracker from state.json |
| `/ship resume` | Continue from current stage in state.json |

---

## 5. Codebase Scanner

**Skill:** `scan.md`  
**Tools:**
- `understand-anything` plugin — deep code comprehension and semantic analysis
- `context-mode` plugin — sandboxes scan output to prevent context window flooding

### Plugin Dependencies
The scanner depends on two Claude Code plugins that are **not bundled** with this plugin. On first run of `/ship` (or `/ship install`), the user is prompted:

```
⚠️  Dev Pipeline requires two additional plugins to scan your codebase:

  1. understand-anything  (Lum1104/Understand-Anything)
     Install: /plugin marketplace add Lum1104/Understand-Anything
              /plugin install understand-anything

  2. context-mode  (mksglu/context-mode)
     Install: /plugin marketplace add mksglu/context-mode
              /plugin install context-mode@context-mode

These will be installed now. Continue? [y/n]
```

If the user confirms, the install commands run automatically. If they decline, the pipeline exits with instructions to install manually before proceeding.

### How the Tools Work Together

| Tool | Role |
|---|---|
| `understand-anything` | Reads and semantically understands code — extracts architecture patterns, conventions, intent, dependencies, and entry points |
| `context-mode` | Wraps all scan output in sandbox mode so raw file contents never enter the main context window |

`context-mode` is particularly critical here: scanning a large codebase without it would consume the entire context window before any agent work begins. All scan operations are routed through `ctx_batch_execute` and `ctx_execute_file`.

### First Run — Full Scan
Scans the entire repo and produces `.claude/pipeline/project-doc.md` covering:

| Section | Content |
|---|---|
| Tech Stack | Runtime, language versions, framework |
| Libraries | All dependencies with versions |
| Architecture | Pattern detected (MVC, layered, feature-based, etc.) |
| Code Style | Naming conventions, file structure, import patterns |
| Modularity | How concerns are separated, shared module locations |
| Test Coverage | Current coverage %, key untested areas |
| Entry Points | Main files, key config files |

### Delta Runs — Incremental Updates
On subsequent runs:
1. `git diff HEAD~1 --name-only` to get changed files
2. Re-scan only those files via graphifyy
3. Patch the relevant sections of `project-doc.md`
4. Update `last_scanned` timestamp and `changed_files` list at top of doc

### AGENTS.md Generation
`AGENTS.md` is generated **once** after the initial full scan. It is not regenerated on delta scans. This is intentional — `AGENTS.md` is a curated, stable document that agents rely on as a source of truth. Silent overwrites would break agent consistency mid-project.

**Update trigger:** Delta scans watch for architectural signals — new framework added, new architectural pattern introduced, major dependency swap. If detected, the pipeline surfaces a diff to the human:

```
⚠️  Architectural change detected in delta scan:
    - New dependency: @tanstack/react-query added
    - New pattern: /lib/hooks/ directory created with 3 query hooks

AGENTS.md may need updating. Review and confirm:
  [y] Update AGENTS.md with these changes
  [n] Skip — this is not an architectural change
```

Only on human confirmation does `AGENTS.md` get updated. The update patches only the affected sections, never rewrites the full file.

This is not a copy of `project-doc.md` — it is written as **agent instructions**, tailored to this specific project.

**Structure of generated AGENTS.md:**

```md
# AGENTS.md — [Project Name]
> Auto-generated by the dev pipeline scanner. Do not edit manually.
> Last updated: 2026-04-24

## How to Read This File
Every agent in this pipeline reads this file first. It defines the rules,
patterns, and guardrails specific to this project.

## Stack Context
[e.g. Next.js 14 App Router + Prisma + PostgreSQL + Tailwind]

## Code Style Rules
[Extracted and rephrased as DO/DON'T instructions from actual codebase patterns]

## Architecture Guardrails
[e.g. "Never query the DB directly from components. Use /lib/services/ only."]

## Testing Requirements
[e.g. "Coverage is at 67%. All new code must include unit tests.
QA agent: flag any feature with <80% coverage on new code."]

## Modularity Conventions
[e.g. "Shared UI components live in /components/ui. Never create one-off
styled elements inline — add to the design system."]

## Agent-Specific Instructions
### Orchestrator
[project-specific clarification prompts to always ask]

### Architect
[known complexity areas, performance constraints, patterns to prefer]

### Developer
[specific libraries to use, anti-patterns banned in this codebase]

### PR Reviewer
[what counts as a major vs minor flag in this project]

### QA Agent
[known edge cases for this domain, critical paths to always test]
```

---

## 6. The Agents

All agents read `AGENTS.md` before any stage input. This is non-negotiable — it is what makes them project-aware rather than generic.

---

### 6.1 Orchestrator
**Skill:** `orchestrate.md`  
**Persona:** Product Manager, 25 years experience  
**Input:** `stories/[active].md` + `AGENTS.md`  
**Output:** `.claude/pipeline/orchestrator-output.md`  
**Human checkpoint:** None — auto-hands off to architect

**Responsibilities:**
- Read the story and tasks
- Identify gaps in acceptance criteria
- Ask clarifying product-level questions (one at a time, conversationally)
- Confirm task type: FRONTEND or BACKEND (not both)
- Produce a complete, unambiguous spec that the architect can plan from

**Output format:**
```md
# Orchestrator Output — [Task Name]

## Task Type
FRONTEND

## Refined Requirement
[Unambiguous description of what needs to be built]

## Clarified Acceptance Criteria
[Complete list, with ambiguities resolved]

## Edge Cases to Handle
[List of edge cases surfaced during Q&A]

## Out of Scope
[Explicit exclusions to prevent scope creep]
```

---

### 6.2 Architect
**Skill:** `architect.md`  
**Persona:** Senior Software Architect, 20 years experience  
**Input:** `orchestrator-output.md` + `AGENTS.md` + `project-doc.md`  
**Output:** `.claude/pipeline/architect-plan.md`  
**Human checkpoint:** YES — pipeline pauses after this stage

**Responsibilities:**
- Read the spec and the project-doc
- Produce a numbered, step-by-step implementation plan
- Each step must reference specific files, functions, or modules
- Flag any architectural risks or deviations from existing patterns
- Confirm FRONTEND/BACKEND tag

**Output format:**
```md
# Architect Plan — [Task Name]

## Task Type
FRONTEND

## Implementation Steps
1. [Specific file] — [what to add/modify and why]
2. ...

## Files to Create
- path/to/new-file.tsx — [purpose]

## Files to Modify
- path/to/existing.ts — [what changes]

## Risks & Notes
[Any deviations from standard patterns, performance concerns, etc.]

## Test Plan
[What the developer must test before handoff to QA]
```

---

### 6.3 Developer
**Skill:** `implement.md`  
**Base:** `fullstack-developer` skill (from skills-lock.json)  
**Persona:** Senior Developer, guided by project guardrails  
**Input:** `architect-plan.md` + `AGENTS.md`  
**Output:** Code changes in the repo  
**Human checkpoint:** None

**Responsibilities:**
- Implement exactly what the architect planned — no scope additions
- Follow all rules in `AGENTS.md` without exception
- Flag (do not silently skip) any plan step that is impossible or contradictory
- Write tests for all new code per the coverage requirements in `AGENTS.md`
- Leave no TODOs, commented-out code, or debug logs

---

### 6.4 PR Reviewer
**Skill:** `review.md`  
**Base:** `code-reviewer` skill (from skills-lock.json)  
**Persona:** Senior Developer, 30 years experience  
**Input:** Git diff of implemented changes + `AGENTS.md`  
**Output:** `.claude/pipeline/review-report.md`  
**Human checkpoint:** Only on major flags

**Tiered resolution:**

| Flag type | Examples | Resolution |
|---|---|---|
| **Minor** | Naming, formatting, missing comment | Auto-fixed by developer agent, no pause |
| **Major** | Logic error, architecture violation, security concern | Pauses pipeline, surfaces to human |

**Conversation log:** All reviewer ↔ developer exchanges are appended to `review-report.md`, including final resolution (Fixed / Flagged N/A / Escalated).

---

### 6.5 QA Agent
**Skill:** `qa.md`  
**Persona:** Senior QA Engineer, 15 years experience  
**Input:** `orchestrator-output.md` (acceptance criteria + edge cases) + `AGENTS.md` + implemented code  
**Output:** `.claude/pipeline/qa-report.md`  
**Human checkpoint:** Only on 3rd failed iteration

**Responsibilities:**
- Test every acceptance criterion from `orchestrator-output.md`
- Test every edge case listed
- Test standard QA scenarios: empty states, invalid inputs, boundary values, error states
- Report pass/fail per criterion with reproduction steps for failures

**Loop behaviour:**
- Bugs → developer fixes → PR reviewer checks → QA re-tests
- After 3 failed QA cycles: pipeline pauses, escalates to human with full report

---

### 6.6 Playwright Agent
**Skill:** `playwright.md`  
**Base:** `playwright-generate-test` + `webapp-testing` skills  
**Persona:** Automation Engineer  
**Input:** `orchestrator-output.md` (acceptance criteria) + running local dev server  
**Output:** Playwright test file + browser test results  
**Condition:** Only runs when `task_type == "FRONTEND"`

**Responsibilities:**
- Start local dev server if not running
- Write Playwright tests covering each acceptance criterion
- Execute tests and capture results + screenshots on failure
- Pass = QA sign-off. Fail = back to developer

---

## 7. Cross-Cutting: Security Guardrails

The `security-guardrails` skill applies to **every agent** in the pipeline — not just the reviewer. All agents must:

### Immediate Halt + Human Escalation Triggers
Any agent that encounters the following must stop all work, log the trigger, and route to the human before resuming:
- Authentication or authorization system changes
- Token, secret, or credential handling modifications
- PII or privacy impact changes
- Dependency vulnerabilities (medium severity or higher)
- CORS/CSP policy modifications
- Permission boundary changes
- Publicly exposed API endpoint modifications
- Data encryption or hashing algorithm changes
- Session management modifications

### Agent-Specific Security Rules

| Agent | Security Rule |
|---|---|
| Developer | Never hardcode secrets. Flag auth-adjacent code to reviewer. Use env vars for all sensitive config. |
| PR Reviewer | Block merge on any secret pattern detection. Block merge on unreviewed auth changes. |
| Architect | Escalate external contract/auth boundary changes to human before design sign-off. |
| QA | Verify no sensitive data in test logs or reports. |

### Anti-Loop Guards
From the `ai-agent-coordination` governance doc — mandatory for all agent handoffs:

1. **Repeated Blocker Rule** — If an agent escalates with the same blocker reason it encountered in a previous handoff, it MUST escalate to human immediately rather than re-delegating.
2. **No Cyclic Handoff** — An agent MUST NOT hand work back to an agent that already handled the same issue in the current chain.
3. **Two-Handoff Rule** — After 2 unresolved handoffs on the same issue, the current agent MUST stop and escalate to human. No third attempt.

These rules take precedence over standard delegation patterns.

---

## 8. Plugin Dependencies

### Required Plugins (auto-installed on first run with user confirmation)

| Plugin | Source | Purpose |
|---|---|---|
| `understand-anything` | `Lum1104/Understand-Anything` | Semantic code comprehension for scanner |
| `context-mode` | `mksglu/context-mode` | Context window protection during scanning |

### Install Commands
```bash
# understand-anything
/plugin marketplace add Lum1104/Understand-Anything
/plugin install understand-anything

# context-mode
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode
```

---

## 8. Installed Skills Mapping

| skills-lock.json entry | Used by |
|---|---|
| `fullstack-developer` | Developer agent (6.3) |
| `code-reviewer` | PR Reviewer agent (6.4) |
| `playwright-generate-test` | Playwright agent (6.6) |
| `agent-governance` | Guardrails applied across all agents |
| `agent-orchestrator-task` | Informs ship.md routing logic |

Marketplace skill `webapp-testing` used by Playwright agent for server lifecycle management.

---

## 9. Full Skills & Agents Mapping

### Skills Used Per Agent

| Agent | Primary Skills | Supporting Skills |
|---|---|---|
| Scanner | `architecture-blueprint-generator`, `understand-anything` | `mern-stack` (if detected), `context-mode` |
| Orchestrator | `agent-orchestrator-task` | `security-guardrails` |
| Architect | `architecture-blueprint-generator` | `security-guardrails`, `agent-governance` |
| Developer | `fullstack-developer` | `mern-stack` (if detected), `security-guardrails`, `testing-patterns` |
| PR Reviewer | `code-reviewer`, `code-review-standards` | `security-guardrails`, `agent-governance` |
| QA | `testing-patterns` | `security-guardrails` |
| Playwright | `playwright-generate-test`, `webapp-testing` | `testing-patterns` |

### Scanner → project-doc.md Structure
The scanner uses `architecture-blueprint-generator` as its core template, producing:
- Architecture detection and overview
- Component interaction and data flow
- Architectural layers and dependencies
- Data architecture and access patterns
- Cross-cutting concerns (auth, error handling, logging, validation)
- Technology-specific patterns (auto-detected)
- Testing architecture
- Test coverage stats

### PR Reviewer — 3-Tier Taxonomy (from extra-agents/pr-reviewer.md)

| Tier | Emoji | Label | Pipeline Action |
|---|---|---|---|
| 1 | 🔴 | Critical Issues | Must fix — pipeline pauses, human notified |
| 2 | 🟡 | Improvement Opportunities | Should fix — developer agent auto-resolves |
| 3 | 💡 | Minor Suggestions | Consider — logged only, no block |

This replaces the binary minor/major split from Section 6.4 with the richer 3-tier model from the existing agent definitions.

### Extra Agents as Skill Inspiration (not direct ports)

| Extra Agent | How It Informs Our Pipeline |
|---|---|
| `delivery-orchestrator.md` | `ship.md` routing logic, 7-gate delivery model, approval logging |
| `Product Manager.md` | Orchestrator persona, INVEST story principles, HITL guardrails |
| `architect.md` | Architect boundaries (no code writing), escalation triggers |
| `pr-reviewer.md` | 3-tier taxonomy, security assessment checklist, test coverage analysis |
| `qa.md` | Bug triage severity (Critical/High/Medium/Low), test execution report format |
| `playwright-test-engineer.md` | Page object pattern, cross-browser matrix, pre-release evidence |
| `ai agent coodinatior and workflow.md` | Anti-loop guards, two-handoff rule, HITL decision authority matrix |

---

## 10. Implementation Order

1. `scan.md` — scanner skill (graphifyy integration, project-doc.md + AGENTS.md generation)
2. `ship.md` — master router + state machine (`state.json` read/write, stage routing)
3. `stories/_template.md` — story template
4. `orchestrate.md` — orchestrator agent
5. `architect.md` — architect agent
6. `implement.md` — developer agent
7. `review.md` — PR reviewer agent
8. `qa.md` — QA agent
9. `playwright.md` — Playwright agent (frontend only)

---

## 11. What This Replaces

| Without plugin | With plugin |
|---|---|
| Dev reads ticket, guesses requirements | Orchestrator clarifies before a line is written |
| Dev plans in their head | Architect produces a reviewable, human-approved plan |
| Code review happens after PR is opened | Reviewer runs immediately, loops resolved before merge |
| QA is manual or skipped | QA agent runs on every task, tied to acceptance criteria |
| Frontend testing is optional | Playwright runs automatically for every UI task |
| Project context re-explained every session | AGENTS.md loaded automatically, always current |
