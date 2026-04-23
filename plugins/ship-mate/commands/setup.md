---
name: setup
description: Installs the dev pipeline plugin into the current project. Copies skills, creates the stories folder, installs required plugins (understand-anything, context-mode), and runs the initial codebase scan to generate project-doc.md and AGENTS.md.
user-invocable: true
---

# Dev Pipeline Setup

You are setting up the AI development pipeline in this project for the first time. Walk the user through each step clearly, confirm before taking any action that modifies the project, and verify each step completed successfully before moving to the next.

## What This Installs

```
[project-root]/
├── stories/
│   └── _template.md          ← Story file template
├── AGENTS.md                 ← Generated on first scan (project-specific agent instructions)
└── .claude/
    ├── skills/
    │   ├── ship.md            ← /ship command (master entry point)
    │   ├── scan.md
    │   ├── orchestrate.md
    │   ├── architect.md
    │   ├── implement.md
    │   ├── review.md
    │   ├── qa.md
    │   ├── playwright.md
    │   └── setup.md           ← this file
    └── pipeline/              ← created on first /ship run
```

## Step 1: Confirm Installation

Print this message and wait for the user to confirm before proceeding:

```
🚀 Dev Pipeline Setup

This will add the following to your project:
  • .claude/skills/   — 8 pipeline skill files
  • stories/          — story file folder + template
  • AGENTS.md         — generated after initial scan

Two Claude Code plugins will also be installed:
  • understand-anything  (Lum1104/Understand-Anything)
  • context-mode         (mksglu/context-mode)

These plugins are required for codebase scanning and context management.

Proceed with installation? [y/n]
```

If the user says no, exit cleanly: `Setup cancelled. Run /setup when ready.`

## Step 2: Check Prerequisites

Before copying files, verify:

1. **Git repository** — check if `.git/` exists in the project root. If not:
   ```
   ⚠️  This project is not a git repository.
   The pipeline uses git diff for delta scans.
   
   Initialise git now? [y/n]
   ```
   If yes: run `git init`. If no: warn the user that delta scanning will use full scans every time, then continue.

2. **Existing `.claude/skills/` folder** — if it already exists, check for conflicts:
   ```
   ⚠️  .claude/skills/ already exists.
   Existing files will not be overwritten.
   Only new pipeline skill files will be added.
   Continue? [y/n]
   ```

## Step 3: Install Plugin Dependencies

Run the following commands in sequence:

```bash
# understand-anything
/plugin marketplace add Lum1104/Understand-Anything
/plugin install understand-anything

# context-mode
/plugin marketplace add mksglu/context-mode
/plugin install context-mode@context-mode
```

Verify both installed successfully. If either fails, show the manual install command and continue — the user can install manually before running `/ship`.

## Step 4: Copy Skill Files

Copy all skill files from the plugin source into `.claude/skills/` in the current project:

Skills to install:
- `ship.md`
- `scan.md`
- `orchestrate.md`
- `architect.md`
- `implement.md`
- `review.md`
- `qa.md`
- `playwright.md`
- `setup.md`

Do not overwrite any file that already exists with the same name — print a warning and skip it.

## Step 5: Create Stories Folder

Create `stories/` in the project root (if it does not exist).
Copy `_template.md` into `stories/_template.md`.

## Step 6: Create Pipeline Folder

Create `.claude/pipeline/` (if it does not exist).
This folder will hold all pipeline state and stage output files.

## Step 7: Run Initial Scan

Print:
```
📡 Running initial codebase scan...
   This generates project-doc.md and AGENTS.md.
   Large codebases may take a moment.
```

Invoke the `scan` skill. This will:
- Perform a full scan of the codebase
- Write `.claude/pipeline/project-doc.md`
- Write `AGENTS.md` at the project root

## Step 8: Confirm Setup Complete

Print the completion summary:

```
✅ Dev Pipeline installed successfully!

   Project scanned:  .claude/pipeline/project-doc.md
   Agent guide:      AGENTS.md
   Story template:   stories/_template.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Review AGENTS.md
     Verify the generated project instructions look correct.
     If anything is wrong, edit it manually — it won't be
     auto-overwritten unless an architectural change is detected.

  2. Write a story
     Copy stories/_template.md → stories/your-story.md
     Fill in the title, description, acceptance criteria, and tasks.
     One task = one pipeline run. Keep tasks focused.

  3. Start the pipeline
     /ship stories/your-story.md

  4. Check progress anytime
     /ship status

  5. Resume after a human checkpoint
     /ship resume

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HUMAN CHECKPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  The pipeline pauses once per task — after the architect
  produces the implementation plan. Review the plan at:
  .claude/pipeline/architect-plan.md

  Run /ship resume when ready to start implementation.

  The pipeline also pauses if a 🔴 Critical review issue
  is found. Check .claude/pipeline/review-report.md and
  run /ship resume after resolving.
```
