# Claude Code Subagents Collection

A comprehensive collection of specialized AI subagents for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), designed to enhance development workflows with domain-specific expertise.

## Overview

This repository contains 28 specialized subagents that extend Claude Code's capabilities. Each subagent is an expert in a specific domain, automatically invoked based on context or explicitly called when needed.

## Available Subagents

### Development & Architecture
- **[backend-architect](backend-architect.md)** - Design RESTful APIs, microservice boundaries, and database schemas
- **[frontend-developer](frontend-developer.md)** - Build React components, implement responsive layouts, and handle client-side state management
- **[mobile-developer](mobile-developer.md)** - Develop React Native or Flutter apps with native integrations
- **[graphql-architect](graphql-architect.md)** - Design GraphQL schemas, resolvers, and federation
- **[architect-reviewer](architect-review.md)** - Reviews code changes for architectural consistency and patterns

### Language Specialists
- **[python-pro](python-pro.md)** - Write idiomatic Python code with advanced features and optimizations
- **[golang-pro](golang-pro.md)** - Write idiomatic Go code with goroutines, channels, and interfaces

### Infrastructure & Operations
- **[devops-troubleshooter](devops-troubleshooter.md)** - Debug production issues, analyze logs, and fix deployment failures
- **[deployment-engineer](deployment-engineer.md)** - Configure CI/CD pipelines, Docker containers, and cloud deployments
- **[cloud-architect](cloud-architect.md)** - Design AWS/Azure/GCP infrastructure and optimize cloud costs
- **[database-optimizer](database-optimizer.md)** - Optimize SQL queries, design efficient indexes, and handle database migrations
- **[incident-responder](incident-responder.md)** - Handles production incidents with urgency and precision
- **[dx-optimizer](dx-optimizer.md)** - Developer Experience specialist that improves tooling, setup, and workflows

### Quality & Security
- **[code-reviewer](code-reviewer.md)** - Expert code review for quality, security, and maintainability
- **[security-auditor](security-auditor.md)** - Review code for vulnerabilities and ensure OWASP compliance
- **[test-automator](test-automator.md)** - Create comprehensive test suites with unit, integration, and e2e tests
- **[performance-engineer](performance-engineer.md)** - Profile applications, optimize bottlenecks, and implement caching strategies
- **[debugger](debugger.md)** - Debugging specialist for errors, test failures, and unexpected behavior

### Data & AI
- **[data-scientist](data-scientist.md)** - Data analysis expert for SQL queries, BigQuery operations, and data insights
- **[data-engineer](data-engineer.md)** - Build ETL pipelines, data warehouses, and streaming architectures
- **[ai-engineer](ai-engineer.md)** - Build LLM applications, RAG systems, and prompt pipelines
- **[ml-engineer](ml-engineer.md)** - Implement ML pipelines, model serving, and feature engineering
- **[prompt-engineer](prompt-engineer.md)** - Optimizes prompts for LLMs and AI systems

### Specialized Domains
- **[api-documenter](api-documenter.md)** - Create OpenAPI/Swagger specs and write developer documentation
- **[payment-integration](payment-integration.md)** - Integrate Stripe, PayPal, and payment processors
- **[quant-analyst](quant-analyst.md)** - Build financial models, backtest trading strategies, and analyze market data
- **[legacy-modernizer](legacy-modernizer.md)** - Refactor legacy codebases and implement gradual modernization
- **[context-manager](context-manager.md)** - Manages context across multiple agents and long-running tasks

## Installation

These subagents are automatically available when placed in `~/.claude/agents/` directory.

```bash
cd ~/.claude
git clone https://github.com/wshobson/agents.git
```

## Usage

### Automatic Invocation
Claude Code will automatically delegate to the appropriate subagent based on the task context and the subagent's description.

### Explicit Invocation
Mention the subagent by name in your request:
```
"Use the code-reviewer to check my recent changes"
"Have the security-auditor scan for vulnerabilities"
"Get the performance-engineer to optimize this bottleneck"
```

## Usage Examples

### Single Agent Tasks
```bash
# Code quality and review
"Use code-reviewer to analyze this component for best practices"
"Have security-auditor check for OWASP compliance issues"

# Development tasks  
"Get backend-architect to design a user authentication API"
"Use frontend-developer to create a responsive dashboard layout"

# Infrastructure and operations
"Have devops-troubleshooter analyze these production logs"
"Use cloud-architect to design a scalable AWS architecture"

# Data and AI
"Get data-scientist to analyze this customer behavior dataset"
"Use ai-engineer to build a RAG system for document search"
```

### Multi-Agent Workflows
```bash
# Feature development workflow
"Implement user authentication feature"
# Automatically uses: backend-architect → frontend-developer → test-automator → security-auditor

# Performance optimization workflow  
"Optimize the checkout process performance"
# Automatically uses: performance-engineer → database-optimizer → frontend-developer

# Production incident workflow
"Debug high memory usage in production"
# Automatically uses: incident-responder → devops-troubleshooter → performance-engineer
```

## Subagent Format

Each subagent follows this structure:
```markdown
---
name: subagent-name
description: When this subagent should be invoked
tools: tool1, tool2  # Optional - defaults to all tools
---

System prompt defining the subagent's role and capabilities
```

## Agent Orchestration Patterns

Claude Code automatically coordinates agents using these common patterns:

### Sequential Workflows
```
User Request → Agent A → Agent B → Agent C → Result

Example: "Build a new API feature"
backend-architect → frontend-developer → test-automator → security-auditor
```

### Parallel Execution
```
User Request → Agent A + Agent B (simultaneously) → Merge Results

Example: "Optimize application performance" 
performance-engineer + database-optimizer → Combined recommendations
```

### Conditional Branching
```
User Request → Analysis → Route to appropriate specialist

Example: "Fix this bug"
debugger (analyzes) → Routes to: backend-architect OR frontend-developer OR devops-troubleshooter
```

### Review & Validation
```
Primary Agent → Review Agent → Final Result

Example: "Implement payment processing"
payment-integration → security-auditor → Validated implementation
```

## When to Use Which Agent

### 🏗️ Planning & Architecture
- **backend-architect**: API design, database schemas, system architecture
- **frontend-developer**: UI/UX planning, component architecture
- **cloud-architect**: Infrastructure design, scalability planning

### 🔧 Implementation & Development  
- **python-pro**: Python-specific development tasks
- **golang-pro**: Go-specific development tasks
- **mobile-developer**: React Native/Flutter development

### 🛠️ Operations & Maintenance
- **devops-troubleshooter**: Production issues, deployment problems
- **incident-responder**: Critical outages requiring immediate response
- **database-optimizer**: Query performance, indexing strategies

### 📊 Analysis & Optimization
- **performance-engineer**: Application bottlenecks, optimization
- **security-auditor**: Vulnerability scanning, compliance checks
- **data-scientist**: Data analysis, insights, reporting

### 🧪 Quality Assurance
- **code-reviewer**: Code quality, maintainability review
- **test-automator**: Test strategy, test suite creation
- **debugger**: Bug investigation, error resolution

## Best Practices

### 🎯 Task Delegation
1. **Let Claude Code delegate automatically** - The main agent analyzes context and selects optimal agents
2. **Be specific about requirements** - Include constraints, tech stack, and quality requirements
3. **Trust agent expertise** - Each agent is optimized for their domain

### 🔄 Multi-Agent Workflows
4. **Start with high-level requests** - Let agents coordinate complex multi-step tasks
5. **Provide context between agents** - Ensure agents have necessary background information
6. **Review integration points** - Check how different agents' outputs work together

### 🎛️ Explicit Control
7. **Use explicit invocation for specific needs** - When you want a particular expert's perspective
8. **Combine multiple agents strategically** - Different specialists can validate each other's work
9. **Request specific review patterns** - "Have security-auditor review backend-architect's API design"

### 📈 Optimization
10. **Monitor agent effectiveness** - Learn which agents work best for your use cases
11. **Iterate on complex tasks** - Use agent feedback to refine requirements
12. **Leverage agent strengths** - Match task complexity to agent capabilities

## Contributing

To add a new subagent:
1. Create a new `.md` file following the format above
2. Use lowercase, hyphen-separated names
3. Write clear descriptions for when the subagent should be used
4. Include specific instructions in the system prompt

## Troubleshooting

### Common Issues

**Agent not being invoked automatically:**
- Ensure your request clearly indicates the domain (e.g., "performance issue" → performance-engineer)
- Be specific about the task type (e.g., "review code" → code-reviewer)

**Unexpected agent selection:**
- Provide more context about your tech stack and requirements
- Use explicit invocation if you need a specific agent

**Multiple agents producing conflicting advice:**
- This is normal - different specialists may have different priorities
- Ask for clarification: "Reconcile the recommendations from security-auditor and performance-engineer"

**Agent seems to lack context:**
- Provide background information in your request
- Reference previous conversations or established patterns

### Getting Help

If agents aren't working as expected:
1. Check agent descriptions in their individual files
2. Try more specific language in your requests
3. Use explicit invocation to test specific agents
4. Provide more context about your project and goals

## Learn More

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)