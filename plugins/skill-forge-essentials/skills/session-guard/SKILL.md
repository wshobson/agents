---
name: session-guard
description: >-
  Use when working on complex multi-step tasks, when a session is getting long
  (40+ tool calls), when the agent starts ignoring rules it followed earlier,
  when conventions drift, when output quality seems to degrade, or after any
  context compaction event. Prevents long-session corruption AND context
  compaction amnesia through behavioral self-enforcement.
---

# Session Guard

## Overview

Long sessions corrupt silently. Context compaction drops instructions unannounced. Hooks don't fix it (confirmed by multiple developers on GitHub issues #19471, #9796, #64171). This skill prevents both through behavioral self-enforcement: monitor health, anchor critical rules through compaction, split before damage occurs. No packages, no databases - pure behavioral enforcement that works in every harness.

## When to Use

- Session exceeds 40 tool calls
- Agent contradicts earlier decisions
- Style/naming conventions start drifting
- After any context compaction event
- Task scope growing unbounded

## Health Signals

| Signal | Threshold | Action |
|--------|-----------|--------|
| Tool call count | >40 | YELLOW: checkpoint + recite critical rules |
| Tool call count | >60 | RED: split or compact with anchor |
| Agent contradicts earlier decision | Any | VERIFY: re-read source of truth |
| Style/naming drift | Any | RECITE: state the active rules aloud |
| File read returns unexpected content | Any | RE-READ: don't trust cached state |
| Task scope growing unbounded | Continuous | SPLIT: one task per session |

## Protocol

### Green Zone (0-40 tool calls)
Normal operation. No intervention needed.

### Yellow Zone (40-60 tool calls)
1. CHECKPOINT - summarize progress in one paragraph
2. RECITE - state the 3-5 most critical active rules aloud: "Active rules: [naming convention], [file structure], [error handling pattern], [testing requirement]"
3. ASSESS - almost done? Push through. Not done? Prepare split.
4. REDUCE - no exploratory reads. Only targeted operations.

### Red Zone (60+ tool calls OR drift signal)
1. STOP - do not make more tool calls
2. VERIFY - re-read project rules (don't trust memory)
3. CHECKPOINT - write state to handoff document
4. SPLIT - create handoff, suggest fresh session

## Context Anchoring (anti-compaction)

When compaction has occurred (sudden loss of earlier context, or after /compact):

1. RE-READ the project's rules file immediately
2. RECITE the 3-5 critical rules aloud in your response
3. VERIFY your planned next action matches those rules before executing
4. If uncertain about ANY prior decision, RE-READ the source file - don't guess

### What survives compaction:
- Most recent user messages (high priority)
- Currently-invoked skill body (capped at 5K tokens, oldest dropped first)
- Git status and project structure
- File contents read AFTER compaction

### What gets LOST in compaction:
- Decisions made early in conversation
- Architectural rules stated only verbally (not in files)
- Context from tool outputs (file reads, command outputs)

### Compaction-Safe Pattern
Keep critical instructions in FILES (CLAUDE.md, CONTEXT.md), NOT in conversation. If a rule matters, it must live in a file the agent can re-read - not in something agreed on earlier.

## Common Mistakes

- Trusting that you remember the rules after 50+ tool calls (you don't - re-read)
- Re-reading EVERYTHING to be safe (wastes tool calls - be targeted)
- Feeling fine therefore assuming context is fine (compaction is SILENT)
- Splitting AFTER noticing problems (split BEFORE - prevention, not recovery)

## Why This Matters

Context compaction is the #1 unsolved platform problem in 2026. Hooks don't fix it (confirmed: the agent ignores post-compaction injections because the compaction summary creates narrative momentum). This skill is the lightweight behavioral countermeasure: no infrastructure, no packages - disciplined self-monitoring that works in every harness.
