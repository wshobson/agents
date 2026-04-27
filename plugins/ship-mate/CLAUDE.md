# ShipMate

Your AI development teammate. ShipMate is a Claude Code plugin that installs a structured, multi-agent development pipeline into any project — replacing ad-hoc Claude usage with a repeatable workflow covering requirements → architecture → implementation → code review → QA → browser testing.

## Plugin Layout

```
plugins/ship-mate/
├── .claude-plugin/
│   └── plugin.json          ← Plugin manifest
├── agents/
│   ├── orchestrate.md       ← Product Orchestrator agent
│   ├── architect.md         ← Architect agent
│   ├── implement.md         ← Developer agent
│   ├── review.md            ← PR Reviewer agent (3-tier)
│   ├── qa.md                ← QA agent
│   └── playwright.md        ← Browser test agent (FRONTEND tasks only)
├── commands/
│   ├── ship.md              ← /ship — master entry point and pipeline router
│   └── setup.md             ← /setup — initialise pipeline state in a target project
├── skills/
│   └── scan/
│       └── SKILL.md         ← Codebase scanner (full + delta, optional enhance plugins)
├── stories/
│   └── _template.md         ← Story file template
└── docs/
    └── plans/               ← Design documents
```

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

| File | Written by |
|---|---|
| `.claude/pipeline/project-doc.md` | Scanner |
| `AGENTS.md` (repo root) | Scanner (first run only) |
| `.claude/pipeline/orchestrator-output.md` | Orchestrator |
| `.claude/pipeline/architect-plan.md` | Architect |
| `.claude/pipeline/review-report.md` | PR Reviewer |
| `.claude/pipeline/qa-report.md` | QA Agent |

## AGENTS.md

Generated once by the scanner on first run. It is the project-specific operating manual read by every agent at the start of each stage. Only updated when an architectural change is detected and confirmed by a human.

## Optional Enhancement Plugins

The `scan` skill works without these, but they improve output quality:

| Plugin | Purpose |
|---|---|
| `understand-anything` (Lum1104/Understand-Anything) | Deeper semantic code analysis |
| `context-mode` (mksglu/context-mode) | Routes large outputs through a sandbox |

Install manually if desired:
```
/plugin marketplace add Lum1104/Understand-Anything && /plugin install understand-anything
/plugin marketplace add mksglu/context-mode && /plugin install context-mode@context-mode
```

## Loop Guards

- Review loop: caps at **2 iterations** before human escalation
- QA loop: caps at **2 iterations** before human escalation
- Two-handoff rule: after 2 unresolved handoffs on the same issue, always escalates to human
