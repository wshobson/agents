# ShipMate

Your AI development teammate. ShipMate is a Claude Code plugin that installs a structured, multi-agent development pipeline into any project — replacing ad-hoc Claude usage with a repeatable workflow covering requirements → architecture → implementation → code review → QA → browser testing.

## What This Repo Contains

```
.claude/skills/          ← The pipeline skills (install these into target projects)
  ship.md                ← Master entry point and pipeline router
  scan.md                ← Codebase scanner (understand-anything + context-mode)
  orchestrate.md         ← Product orchestrator agent
  architect.md           ← Architect agent
  implement.md           ← Developer agent
  review.md              ← PR reviewer agent (3-tier)
  qa.md                  ← QA agent
  playwright.md          ← Browser test agent (FRONTEND tasks only)

stories/
  _template.md           ← Story file template

.agents/skills/          ← Skills pulled from external sources (via skills-lock.json)
extra-agents/            ← Reference agent definitions (VSCode agents, used as inspiration)
extra-skills/            ← Reference skill definitions (used as inspiration)
docs/plans/              ← Design documents
```

## How to Install Into a Target Project

Run the `setup` skill in the target project:
```
/setup
```

Or follow the manual steps in `INSTALL.md`.

## How to Use the Pipeline

### 1. Write a Story
Copy `stories/_template.md` into your target project's `stories/` folder.
Fill in the story title, description, acceptance criteria, and task list.

### 2. Run the Pipeline
```
/ship stories/your-story.md
```

### 3. Human Checkpoints
The pipeline pauses **once** per task — after the architect produces the plan:
```
⏸️  Architect plan ready for review.
   📄 .claude/pipeline/architect-plan.md
   Run /ship resume to begin implementation.
```
Review the plan. If it looks right, run `/ship resume`.

### 4. Check Progress
```
/ship status
```

### 5. Resume After a Pause
```
/ship resume
```

## Pipeline Flow

```
/ship stories/foo.md
    │
    ▼
[SCAN] Delta scan → update project-doc.md (+ AGENTS.md on first run)
    │
    ▼
[ORCHESTRATE] PM agent asks clarifying questions → orchestrator-output.md
    │
    ▼
[ARCHITECT] Step-by-step implementation plan → architect-plan.md
    │
    ▼ ⏸️  HUMAN CHECKPOINT — review architect-plan.md, then /ship resume
    │
    ▼
[IMPLEMENT] Developer agent follows plan, writes tests
    │
    ▼
[REVIEW] PR Reviewer — 3-tier findings
    │  🔴 Critical → ⏸️ HUMAN CHECKPOINT
    │  🟡 Should Fix → auto-resolved by developer
    │  💡 Consider → logged only
    ▼
[QA] QA agent tests all ACs + edge cases → qa-report.md
    │  Bugs found → back to IMPLEMENT (max 2 loops)
    │  QA passes ↓
    ▼
[PLAYWRIGHT] Browser tests — FRONTEND tasks only
    │
    ▼
✅  Task complete → next task in story
```

## Story File Format

```md
# Story: [Title]

## Description
As a [user], I want [goal] so that [benefit].

## Acceptance Criteria
- Given [context], when [action], then [outcome]

## Tasks
- [ ] [Task 1 — FRONTEND or BACKEND, one concern per task]
- [ ] [Task 2]
```

**Rules:**
- One task = one pipeline run (scan → QA)
- Each task is either FRONTEND or BACKEND — never both
- Tasks are processed sequentially, top to bottom

## Pipeline State

All state is stored in `.claude/pipeline/state.json`. The pipeline can be interrupted and resumed across sessions.

Stage outputs:
| File | Written by |
|---|---|
| `.claude/pipeline/project-doc.md` | Scanner |
| `AGENTS.md` (repo root) | Scanner (first run only) |
| `.claude/pipeline/orchestrator-output.md` | Orchestrator |
| `.claude/pipeline/architect-plan.md` | Architect |
| `.claude/pipeline/review-report.md` | PR Reviewer |
| `.claude/pipeline/qa-report.md` | QA Agent |

## AGENTS.md

`AGENTS.md` is generated once by the scanner on first run. It is the project-specific operating manual read by every agent at the start of each stage. It is NOT updated automatically — only when an architectural change is detected and confirmed by a human.

## Required Plugins

These are installed automatically on first `/ship` run (with confirmation):

| Plugin | Install command |
|---|---|
| `understand-anything` | `/plugin marketplace add Lum1104/Understand-Anything` then `/plugin install understand-anything` |
| `context-mode` | `/plugin marketplace add mksglu/context-mode` then `/plugin install context-mode@context-mode` |

## Loop Guards

To prevent infinite agent loops:
- Review loop: caps at **2 iterations** before human escalation
- QA loop: caps at **2 iterations** before human escalation
- Two-handoff rule: after 2 unresolved handoffs on the same issue, always escalates to human

## Working on This Plugin Repo

When modifying skills in `.claude/skills/`, remember:
- Skills are read by Claude at invocation time — they are instructions, not code
- Every skill references `AGENTS.md` and pipeline output files by path — keep paths consistent
- The `ship.md` skill is the state machine — changes there affect all routing logic
- Test changes against a real project with a sample story before committing
