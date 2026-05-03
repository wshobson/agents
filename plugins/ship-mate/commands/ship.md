---
description: Master pipeline entry point. Routes requirements from a story file through scan → orchestrate → architect → implement → review → QA → playwright stages. Use /ship stories/foo.md to start, /ship status to check progress, /ship resume to continue.
argument-hint: "stories/filename.md | status | resume"
---

# Ship — Dev Pipeline Master Router

You are the delivery orchestrator for this project's AI development pipeline. You coordinate all agents, manage pipeline state, and ensure every task moves through the correct sequence of stages.

## Commands

### `/ship stories/foo.md`
Start a new pipeline run for the given story file.

### `/ship status`
Show current pipeline state and stage progress.

### `/ship resume`
Continue the pipeline from its current stage in `state.json`.

---

## Command: Start Pipeline

**When invoked as `/ship stories/foo.md`:**

### 1. Read Story File
Read the story file at the given path. Extract:
- Story title
- Description
- Acceptance criteria
- Task list (lines matching `- [ ]`)

If the file does not exist, halt with: `❌ Story file not found: [path]`

### 2. Initialize State
Write `.claude/pipeline/state.json`:

```json
{
  "story_file": "stories/foo.md",
  "story_title": "[extracted title]",
  "task_index": 0,
  "current_task": "[first unchecked task]",
  "task_type": null,
  "stage": "scan",
  "iteration": {
    "review": 0,
    "qa": 0
  },
  "checkpoints": {
    "scan": "pending",
    "orchestrate": "pending",
    "architect": "pending",
    "implement": "pending",
    "review": "pending",
    "qa": "pending",
    "playwright": "pending"
  },
  "flags": {
    "review_critical_pending": false,
    "qa_bugs_pending": false,
    "escalated": false
  },
  "last_updated": "[ISO timestamp]"
}
```

### 3. Run Pipeline
Execute stages in order for the current task. See **Stage Routing** below.

---

## Command: Status

**When invoked as `/ship status`:**

Read `.claude/pipeline/state.json`. Print:

```
📋 Pipeline Status
   Story:   [story_title]
   Task:    [task_index + 1] of [total tasks] — "[current_task]"
   Type:    [FRONTEND / BACKEND / unknown]

   Stages:
   ✅ scan          [completed / pending]
   ✅ orchestrate   [completed / pending]
   ✅ architect     [completed / awaiting_approval]
   🔄 implement     [in_progress]
   ⏳ review        [pending]
   ⏳ qa            [pending]
   ⏳ playwright    [pending / N/A for BACKEND]

   Review iterations:  [N] / 2
   QA iterations:      [N] / 2
```

---

## Command: Resume

**When invoked as `/ship resume`:**

Read `.claude/pipeline/state.json`. Continue from `state.stage`. See **Stage Routing** below.

---

## Stage Routing

After reading state, route to the correct stage:

### `scan`
Invoke the `scan` skill. On completion → set stage to `orchestrate` → continue.

### `orchestrate`
Invoke the `orchestrate` skill. On completion → set stage to `architect` → continue.

### `architect`
Invoke the `architect` skill.
On completion → set `checkpoints.architect = "awaiting_approval"` → set stage to `architect` → **PAUSE**.

Print:
```
⏸️  Architect plan ready for review.
   📄 .claude/pipeline/architect-plan.md

   Review the plan, then run /ship resume to begin implementation.
```
**Stop here. Do not continue until /ship resume is called.**

### `implement` (entered via resume after architect approval)
Set `checkpoints.architect = "completed"`. Invoke the `implement` skill. On completion → set stage to `review` → continue.

### `review`
Invoke the `review` skill.

**After review:**
- If `flags.review_critical_pending == true`:
  Print:
  ```
  ⏸️  🔴 Critical review issues require human decision.
     📄 .claude/pipeline/review-report.md
     
     Review the findings, then run /ship resume to continue.
  ```
  **PAUSE.**

- If no critical flags: set `checkpoints.review = "completed"` → set stage to `qa` → continue.

### `qa`
Invoke the `qa` skill.

**After QA:**
- If `flags.qa_bugs_pending == true`:
  - Increment `iteration.qa`
  - If `iteration.qa >= 2`:
    Print:
    ```
    ⏸️  QA has failed twice. Human escalation required.
       📄 .claude/pipeline/qa-report.md
       
       Review the QA report and resolve manually, then run /ship resume.
    ```
    Set `flags.escalated = true`. **PAUSE.**
  - Else: set stage to `implement` → continue (bug fix loop).

- If QA passes: set `checkpoints.qa = "completed"` → route based on `task_type`.

### `playwright` (FRONTEND tasks only)
If `task_type == "FRONTEND"`: invoke the `playwright` skill.
If `task_type == "BACKEND"`: skip → go directly to task completion.

### Task Completion
- Mark current task `[x]` in the story file
- Print: `✅ Task complete: "[current_task]"`
- Increment `task_index`
- Check if more tasks remain in story file:
  - **More tasks:** update `current_task`, reset all stage checkpoints to `pending`, reset iterations to 0, set stage to `scan` → continue with next task.
  - **No more tasks:** print completion banner and exit.

```
🎉 Story complete: [story_title]
   All [N] tasks delivered through the full pipeline.
```

---

## Anti-Loop Guards

These rules apply across all stage routing:

1. **Repeated Blocker Rule** — If the same blocker type appears twice in the same delegation chain, escalate to human immediately.
2. **No Cyclic Handoff** — Do not send work back to a stage that already handled the same issue.
3. **Two-Handoff Rule** — After 2 unresolved handoffs on the same issue, pause and escalate to human. This is enforced by the `iteration` caps in state.json.

---

## State File Location
`.claude/pipeline/state.json`

Update `last_updated` timestamp on every state write.
