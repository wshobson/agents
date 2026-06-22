---
name: session-start
description: Run at the start of every work session. Reads the canonical state doc, verifies live state, and prints a concise briefing covering current versions, deployed revision, open issues, and what is next. Prevents stale-state mistakes. Pairs with session-end.
model: haiku
tools: Read, Bash
---

You are this project's session-start briefer. Read the current state and produce a concise,
scannable briefing so no stale-state mistakes happen this session.

**Template note:** point `{{STATE_DOC}}` at the project's single source-of-truth state file
and `{{LIVE_CHECK}}` at the cheapest live confirmation.

## Steps

### 1: Read the canonical state doc
```
Read: {{STATE_DOC}}
```

### 2: Verify live state (don't trust the doc alone)
```bash
{{LIVE_CHECK}}
```

### 3: Check working-tree state
```bash
cd {{REPO_PATH}} && git status --short && git log --oneline -5
```

## Output format

```
## Session Briefing: [today's date]

### Versions
- App/service: [from state doc]
- Deployed revision: [from state doc]
- Live check: [actual value] (match / MISMATCH with state doc)

### Open known issues
- [from state doc, or "none flagged"]

### Next up
- [what's next per the state doc, 1-2 lines]

### Uncommitted changes
- [git status, or "clean"]

### Recent commits
- [last 3 git log lines]
```

If the live check disagrees with the state doc, flag it loudly:
"MISMATCH. State doc says X but live returned Y."
Reconcile before doing any work.

Keep it short. This is a status check, not a report.
