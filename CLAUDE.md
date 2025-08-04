# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the Claude Code Subagents Collection - a comprehensive set of 50 specialized AI agents designed to extend Claude Code's capabilities with domain-specific expertise. Each agent is configured with specific Claude models (haiku/sonnet/opus) based on task complexity for optimal performance.

## Architecture

### Agent Structure
Each agent follows a consistent markdown format:
```markdown
---
name: agent-name
description: When this agent should be invoked
model: haiku|sonnet|opus  # Model assignment based on complexity
tools: tool1, tool2       # Optional - defaults to all tools
---

System prompt defining the agent's role and capabilities
```

### Model Tiers
- **Haiku (8 agents)**: Simple tasks - documentation, basic analysis, content generation
- **Sonnet (31 agents)**: Development tasks - coding, testing, standard engineering work
- **Opus (11 agents)**: Complex tasks - security auditing, architecture, AI/ML, incident response

### Agent Categories
1. **Development & Architecture**: backend-architect, frontend-developer, ui-ux-designer, etc.
2. **Language Specialists**: python-pro, golang-pro, rust-pro, c-pro, etc.
3. **Infrastructure & Operations**: devops-troubleshooter, deployment-engineer, cloud-architect, etc.
4. **Quality & Security**: code-reviewer, security-auditor, test-automator, etc.
5. **Data & AI**: data-scientist, ai-engineer, ml-engineer, mlops-engineer, etc.
6. **Business & Marketing**: business-analyst, content-marketer, sales-automator, etc.

## Development Guidelines

### Adding New Agents
1. Create a new `.md` file with lowercase, hyphen-separated name
2. Include the frontmatter with name, description, and model assignment
3. Write clear, specific system prompts focusing on practical implementation
4. Assign appropriate model based on task complexity:
   - Haiku: Simple, well-defined tasks
   - Sonnet: Standard development and engineering tasks
   - Opus: Complex analysis, critical operations, AI/ML tasks

### Agent Prompt Best Practices
- Start with a clear role definition
- Define specific focus areas and expertise
- Include structured approach/workflow
- Specify expected output format
- Emphasize practical implementation over theory
- Include domain-specific guidelines and patterns

### Testing Agents
When modifying agents:
1. Test the agent's ability to handle its core use cases
2. Verify appropriate model assignment for task complexity
3. Ensure clear activation criteria in the description
4. Check for overlap with existing agents

## Key Patterns

### Proactive Agents
These agents are marked with "Use PROACTIVELY" in their descriptions:
- code-reviewer: Reviews code immediately after changes
- backend-architect: Activates when creating new services/APIs
- dx-optimizer: Improves developer experience when friction detected
- incident-responder: Handles production issues with urgency

### Critical Focus Agents
Some agents have specific critical focuses:
- code-reviewer: Configuration security and production reliability
- security-auditor: OWASP compliance and vulnerability detection
- incident-responder: Production incident urgency and coordination
- context-manager: Required for projects >10k tokens

### Multi-Agent Workflows
Agents are designed to work together in common patterns:
- Sequential: backend-architect → frontend-developer → test-automator
- Parallel: performance-engineer + database-optimizer
- Review: payment-integration → security-auditor
- Incident: incident-responder → devops-troubleshooter → error-detective

## Important Agent-Specific Notes

### code-reviewer
- Deep focus on configuration security and magic numbers
- Proactively reviews all code changes
- Special attention to connection pools, timeouts, rate limits

### context-manager
- MUST be used for projects exceeding 10k tokens
- Manages state across multiple agents and sessions
- Creates context checkpoints at major milestones

### incident-responder
- Immediate activation for production issues
- Coordinates debugging across multiple agents
- Documents post-mortems

### search-specialist
- Advanced web research with multi-source verification
- Handles competitive analysis and fact-checking
- Masters search operators and result filtering

## Common Commands

Since this is a collection of agent definitions rather than a traditional codebase, there are no build/test commands. However, agents can be:

1. **Viewed**: Read individual agent files to understand their capabilities
2. **Modified**: Edit agent prompts to refine behavior
3. **Added**: Create new agent files following the established format
4. **Tested**: Invoke agents explicitly to verify behavior

Example invocations:
```
"Use code-reviewer to check my recent changes"
"Have security-auditor scan for vulnerabilities"  
"Get performance-engineer to optimize this bottleneck"
```

## Integration with Claude Code

These agents integrate seamlessly with Claude Code's Task tool. They can be:
- Automatically invoked based on task context
- Explicitly called by name in requests
- Chained together in multi-agent workflows
- Used with the companion Commands repository for sophisticated orchestration