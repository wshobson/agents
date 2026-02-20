# Best Practices

## Context Management

1. **Read context first** — always read relevant artifacts before starting work
2. **Small updates** — make incremental context changes, not massive rewrites
3. **Link decisions** — reference context when making implementation choices
4. **Version context** — commit context changes alongside code changes
5. **Review context** — include context artifact reviews in code reviews
6. **Validate regularly** — run the pre-implementation validation before major work
7. **Question staleness** — if context feels wrong, investigate and update
8. **Keep it actionable** — every context item should inform a decision or behavior

## Session Continuity

Conductor supports multi-session development through context persistence.

### Starting a New Session

1. Read `index.md` to orient yourself
2. Check `tracks.md` for active work
3. Review the relevant track's `plan.md` for current task
4. Verify context artifacts are current

### Ending a Session

1. Update `plan.md` with current progress
2. Note any blockers or decisions made
3. Commit in-progress work with clear status
4. Update `tracks.md` if status changed

### Handling Interruptions

If interrupted mid-task:

1. Mark task as `[~]` with note about stopping point
2. Commit work-in-progress to feature branch
3. Document any uncommitted decisions in `plan.md`
