---
name: ai-debt-detector
description: >-
  Use after generating code, after accepting AI suggestions, or when reviewing
  AI-written modules. Also use when code works but feels brittle, when error
  handling seems thin, when orphaned resources or missing cleanup are suspected,
  or when the agent claims done but hidden debt may exist. Catches the specific
  failure patterns AI agents produce that humans would not.
---

# AI Debt Detector

## Overview

AI agents generate code that passes the happy path but hides debt: missing error handling, orphaned resources, ignored failure modes, hallucinated packages, silent architectural drift. This skill forces a targeted audit for the exact patterns AI agents get wrong.

## When to Use

- After any AI code generation session (20+ lines produced)
- Before merging AI-generated PRs
- When code works but something feels off
- After vibe-coding sprints where debt accumulates fastest
- When the agent claims done without showing verification

## Process

After code generation, scan for these AI-specific debt patterns:

1. **FAILURE MODES** - What happens when this fails?
   - Network timeout? Disk full? Permission denied? Null input?
   - Is there a try/catch? Does it catch SPECIFIC errors or swallow everything?
   - Are resources cleaned up on failure? (streams closed, connections returned, temp files deleted)

2. **ORPHANS** - What gets created but never cleaned up?
   - Temp files, event listeners, intervals, subscriptions, connections
   - Are there corresponding cleanup/dispose/close calls for every open/create?
   - In React: does every addEventListener have a removeEventListener in cleanup?

3. **EDGE CASES** - What inputs break this?
   - Empty array/string? null/undefined? Multi-MB input? Unicode? Concurrent calls?
   - Does the code assume the happy path? (AI almost always does)

4. **HALLUCINATED DEPS** - Do all imports actually exist?
   - Is every package in package.json/requirements.txt?
   - Are API methods real? (AI invents plausible-sounding methods that don't exist)
   - Does this library's latest version still export this function?

5. **ARCHITECTURAL DRIFT** - Does this match the project's patterns?
   - Same error handling style as existing code?
   - Uses the project's established utilities (not reinventing)?
   - Follows the file structure convention?

## Red Flags (stop and fix immediately)

- `catch (e) {}` or `catch (e) { console.log(e) }` - swallowed error
- No `finally` block when resources were opened
- `// TODO: handle error` - AI's way of punting
- Import from a path that doesn't exist in the project
- Timeout set but no abort/cleanup on timeout
- Database connection opened but never released back to pool

## Common Mistakes

- Trusting that compilation means correctness (compilation checks syntax, not logic)
- Reviewing only the diff without checking what the AI did NOT generate (missing error paths)
- Assuming the AI used the right library version (it often uses deprecated APIs)
- Skipping the orphan check because garbage collection handles it (it doesn't for connections, listeners, timers)

## Why This Exists

AI agents systematically optimize for "looks correct" and "passes the happy path." They miss failure modes, orphan resources, and hallucinate dependencies at rates significantly higher than manual code. This skill forces an audit for those specific blind spots.
