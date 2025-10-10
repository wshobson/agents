---
model: claude-sonnet-4-5-20250929
---

Save current project context for future agent coordination:

[Extended thinking: This tool uses the context-manager agent to capture and preserve project state, decisions, and patterns. This enables better continuity across sessions and improved agent coordination.]

## Context Capture Process

Use Task tool with subagent_type="context-manager" to save comprehensive project context.

Prompt: "Save comprehensive project context for: $ARGUMENTS. Capture:

1. **Project Overview**
   - Project goals and objectives
   - Key architectural decisions
   - Technology stack and dependencies
   - Team conventions and patterns

2. **Current State**
   - Recently implemented features
   - Work in progress
   - Known issues and technical debt
   - Performance baselines

3. **Design Decisions**
   - Architectural choices and rationale
   - API design patterns
   - Database schema decisions
   - Security implementations

4. **Code Patterns**
   - Coding conventions used
   - Common patterns and abstractions
   - Testing strategies
   - Error handling approaches

5. **Agent Coordination History**
   - Which agents worked on what
   - Successful agent combinations
   - Agent-specific context and findings
   - Cross-agent dependencies

6. **Future Roadmap**
   - Planned features
   - Identified improvements
   - Technical debt to address
   - Performance optimization opportunities

Save this context in a structured format that can be easily restored and used by future agent invocations."

## Context Storage

The context will be saved to `.claude/context/` with:
- Timestamp-based versioning
- Structured JSON/Markdown format
- Easy restoration capabilities
- Context diffing between versions

## Usage Scenarios

This saved context enables:
- Resuming work after breaks
- Onboarding new team members
- Maintaining consistency across agent invocations
- Preserving architectural decisions
- Tracking project evolution

Context to save: $ARGUMENTS