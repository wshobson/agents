---
model: claude-sonnet-4-5-20250929
---

Restore saved project context for agent coordination:

[Extended thinking: This tool uses the context-manager agent to restore previously saved project context, enabling continuity across sessions and providing agents with comprehensive project knowledge.]

## Context Restoration Process

Use Task tool with subagent_type="context-manager" to restore and apply saved context.

Prompt: "Restore project context for: $ARGUMENTS. Perform the following:

1. **Locate Saved Context**
   - Find the most recent or specified context version
   - Validate context integrity
   - Check compatibility with current codebase

2. **Load Context Components**
   - Project overview and goals
   - Architectural decisions and rationale
   - Technology stack and patterns
   - Previous agent work and findings
   - Known issues and roadmap

3. **Apply Context**
   - Set up working environment based on context
   - Restore project-specific configurations
   - Load coding conventions and patterns
   - Prepare agent coordination history

4. **Validate Restoration**
   - Verify context applies to current code state
   - Identify any conflicts or outdated information
   - Flag areas that may need updates

5. **Prepare Summary**
   - Key points from restored context
   - Important decisions and patterns
   - Recent work and current focus
   - Suggested next steps

Return a comprehensive summary of the restored context and any issues encountered."

## Context Integration

The restored context will:
- Inform all subsequent agent invocations
- Maintain consistency with past decisions
- Provide historical knowledge to agents
- Enable seamless work continuation

## Usage Scenarios

Use context restoration when:
- Starting work after a break
- Switching between projects
- Onboarding to an existing project
- Needing historical project knowledge
- Coordinating complex multi-agent workflows

## Additional Options

- Restore specific context version: Include version timestamp
- Partial restoration: Restore only specific components
- Merge contexts: Combine multiple context versions
- Diff contexts: Compare current state with saved context

Context to restore: $ARGUMENTS