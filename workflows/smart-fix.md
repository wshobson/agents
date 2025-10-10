---
model: claude-sonnet-4-5-20250929
---

Intelligently fix the issue using automatic agent selection with explicit Task tool invocations:

[Extended thinking: This workflow analyzes the issue and automatically routes to the most appropriate specialist agent(s). Complex issues may require multiple agents working together.]

First, analyze the issue to categorize it, then use Task tool with the appropriate agent:

## Analysis Phase
Examine the issue: "$ARGUMENTS" to determine the problem domain.

## Agent Selection and Execution

### For Deployment/Infrastructure Issues
If the issue involves deployment failures, infrastructure problems, or DevOps concerns:
- Use Task tool with subagent_type="devops-troubleshooter"
- Prompt: "Debug and fix this deployment/infrastructure issue: $ARGUMENTS"

### For Code Errors and Bugs
If the issue involves application errors, exceptions, or functional bugs:
- Use Task tool with subagent_type="debugger"
- Prompt: "Analyze and fix this code error: $ARGUMENTS. Provide root cause analysis and solution."

### For Database Performance
If the issue involves slow queries, database bottlenecks, or data access patterns:
- Use Task tool with subagent_type="database-optimizer"
- Prompt: "Optimize database performance for: $ARGUMENTS. Include query analysis, indexing strategies, and schema improvements."

### For Application Performance
If the issue involves slow response times, high resource usage, or performance degradation:
- Use Task tool with subagent_type="performance-engineer"
- Prompt: "Profile and optimize application performance issue: $ARGUMENTS. Identify bottlenecks and provide optimization strategies."

### For Legacy Code Issues
If the issue involves outdated code, deprecated patterns, or technical debt:
- Use Task tool with subagent_type="legacy-modernizer"
- Prompt: "Modernize and fix legacy code issue: $ARGUMENTS. Provide migration path and updated implementation."

## Multi-Domain Coordination
For complex issues spanning multiple domains:
1. Use primary agent based on main symptom
2. Use secondary agents for related aspects
3. Coordinate fixes across all affected areas
4. Verify integration between different fixes

Issue: $ARGUMENTS
