# April9's Claude Code Subagents Collection

A curated collection of specialized AI subagents for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), providing domain-specific expertise across software development, infrastructure, and business operations.

> **Note:** This is a fork of [wshobson/agents](https://github.com/wshobson/agents) with organization-wide configuration management. This repository contains a **whitelisted subset** of agents from the upstream repository. For the complete list of available agents, visit [wshobson/agents](https://github.com/wshobson/agents).

## Overview

This repository provides production-ready subagents that extend Claude Code's capabilities with specialized knowledge. Each subagent incorporates:

- Current industry best practices and standards (2024/2025)
- Production-ready patterns and enterprise architectures
- Deep domain expertise with 8-12 capability areas per agent
- Modern technology stacks and frameworks
- Optimized model selection based on task complexity

### Whitelisted Agents

This repository syncs **only the agents whitelisted in `agents-config.json`** to your local Claude Code configuration. If you want to use additional agents from the upstream repository, you must add them to the whitelist.

## Whitelisted Agents

This repository contains a curated subset of agents from [wshobson/agents](https://github.com/wshobson/agents). Only the agents listed below are synced to your local Claude Code configuration.

### Architecture & System Design

| Agent | Model | Description |
|-------|-------|-------------|
| [backend-architect](agents/backend-architect.md) | opus | RESTful API design, microservice boundaries, database schemas |
| [cloud-architect](agents/cloud-architect.md) | opus | AWS/Azure/GCP infrastructure design and cost optimization |
| [architect-reviewer](agents/architect-review.md) | opus | Architectural consistency analysis and pattern validation |
| [ui-ux-designer](agents/ui-ux-designer.md) | sonnet | Interface design, wireframes, design systems |

### Frontend & Mobile Development

| Agent | Model | Description |
|-------|-------|-------------|
| [frontend-developer](agents/frontend-developer.md) | sonnet | React components, responsive layouts, client-side state management |
| [flutter-expert](agents/flutter-expert.md) | sonnet | Advanced Flutter development with state management |

### Programming Languages

| Agent | Model | Description |
|-------|-------|-------------|
| [typescript-pro](agents/typescript-pro.md) | sonnet | Advanced TypeScript with type systems and generics |

### Infrastructure & Operations

| Agent | Model | Description |
|-------|-------|-------------|
| [devops-troubleshooter](agents/devops-troubleshooter.md) | sonnet | Production debugging, log analysis, deployment troubleshooting |
| [deployment-engineer](agents/deployment-engineer.md) | sonnet | CI/CD pipelines, containerization, cloud deployments |
| [dx-optimizer](agents/dx-optimizer.md) | sonnet | Developer experience optimization and tooling improvements |
| [database-optimizer](agents/database-optimizer.md) | opus | Query optimization, index design, migration strategies |
| [incident-responder](agents/incident-responder.md) | opus | Production incident management and resolution |

### Quality Assurance & Security

| Agent | Model | Description |
|-------|-------|-------------|
| [code-reviewer](agents/code-reviewer.md) | opus | Code review with security focus and production reliability |
| [security-auditor](agents/security-auditor.md) | opus | Vulnerability assessment and OWASP compliance |
| [backend-security-coder](agents/backend-security-coder.md) | opus | Secure backend coding practices, API security implementation |
| [frontend-security-coder](agents/frontend-security-coder.md) | opus | XSS prevention, CSP implementation, client-side security |
| [test-automator](agents/test-automator.md) | sonnet | Comprehensive test suite creation (unit, integration, e2e) |
| [debugger](agents/debugger.md) | sonnet | Error resolution and test failure analysis |
| [error-detective](agents/error-detective.md) | sonnet | Log analysis and error pattern recognition |
| [performance-engineer](agents/performance-engineer.md) | opus | Application profiling and optimization |

### AI & Research

| Agent | Model | Description |
|-------|-------|-------------|
| [prompt-engineer](agents/prompt-engineer.md) | opus | LLM prompt optimization and engineering |
| [search-specialist](agents/search-specialist.md) | haiku | Advanced web research and information synthesis |

### Documentation & Technical Writing

| Agent | Model | Description |
|-------|-------|-------------|
| [docs-architect](agents/docs-architect.md) | opus | Comprehensive technical documentation generation |
| [api-documenter](agents/api-documenter.md) | sonnet | OpenAPI/Swagger specifications and developer docs |
| [reference-builder](agents/reference-builder.md) | haiku | Technical references and API documentation |
| [tutorial-engineer](agents/tutorial-engineer.md) | sonnet | Step-by-step tutorials and educational content |
| [mermaid-expert](agents/mermaid-expert.md) | sonnet | Diagram creation (flowcharts, sequences, ERDs) |

### Business & Marketing

| Agent | Model | Description |
|-------|-------|-------------|
| [content-marketer](agents/content-marketer.md) | sonnet | Blog posts, social media, email campaigns |
| [sales-automator](agents/sales-automator.md) | haiku | Cold emails, follow-ups, proposal generation |
| [customer-support](agents/customer-support.md) | sonnet | Support tickets, FAQ responses, customer communication |

### SEO & Content Optimization

| Agent | Model | Description |
|-------|-------|-------------|
| [seo-content-auditor](agents/seo-content-auditor.md) | sonnet | Content quality analysis, E-E-A-T signals assessment |
| [seo-meta-optimizer](agents/seo-meta-optimizer.md) | haiku | Meta title and description optimization |
| [seo-structure-architect](agents/seo-structure-architect.md) | haiku | Content structure and schema markup |
| [seo-content-writer](agents/seo-content-writer.md) | sonnet | SEO-optimized content creation |

## Model Configuration

Agents are assigned to specific Claude models based on task complexity and computational requirements:

- **Haiku**: Quick, focused tasks with minimal computational overhead
- **Sonnet**: Standard development and specialized engineering tasks
- **Opus**: Complex reasoning, architecture, and critical analysis

### Model Distribution (Whitelisted Agents)

| Model | Agent Count | Agents |
|-------|-------------|--------|
| Haiku | 4 | `reference-builder`, `sales-automator`, `search-specialist`, `seo-meta-optimizer`, `seo-structure-architect` |
| Sonnet | 16 | `frontend-developer`, `flutter-expert`, `typescript-pro`, `ui-ux-designer`, `devops-troubleshooter`, `deployment-engineer`, `dx-optimizer`, `test-automator`, `debugger`, `error-detective`, `api-documenter`, `tutorial-engineer`, `mermaid-expert`, `content-marketer`, `customer-support`, `seo-content-auditor`, `seo-content-writer` |
| Opus | 11 | `backend-architect`, `cloud-architect`, `architect-reviewer`, `database-optimizer`, `incident-responder`, `code-reviewer`, `security-auditor`, `backend-security-coder`, `frontend-security-coder`, `performance-engineer`, `prompt-engineer`, `docs-architect` |

## Installation

Clone the repository and run the sync script:

```bash
# Clone the repository
git clone https://github.com/@april9/a9-agents.git
cd a9-agents

# Sync whitelisted agents to ~/.claude/agents
node sync-agents.js
```

That's it! The whitelisted agents from `agents-config.json` are now available in Claude Code.

### Updating Agents

```bash
cd a9-agents
git pull
node sync-agents.js
```

## Usage

### Automatic Delegation
Claude Code automatically selects the appropriate subagent based on task context and requirements. The system analyzes your request and delegates to the most suitable specialist.

### Explicit Invocation
Specify a subagent by name to use a particular specialist:

```
"Use code-reviewer to analyze the recent changes"
"Have security-auditor scan for vulnerabilities"
"Get performance-engineer to optimize this bottleneck"
```

## Usage Examples

### Code Quality & Security
```
code-reviewer: Analyze component for best practices
security-auditor: Check for OWASP compliance
test-automator: Implement comprehensive test suite
performance-engineer: Profile and optimize bottlenecks
backend-security-coder: Implement secure API authentication
```

### Development & Architecture
```
backend-architect: Design authentication API
frontend-developer: Create responsive dashboard
flutter-expert: Build cross-platform mobile app
typescript-pro: Implement type-safe data layer
```

### Infrastructure & Operations
```
devops-troubleshooter: Analyze production logs
cloud-architect: Design scalable AWS architecture
deployment-engineer: Set up CI/CD pipeline
incident-responder: Handle production outage
```

### Documentation & Content
```
docs-architect: Generate technical documentation
api-documenter: Write OpenAPI specifications
content-marketer: Create SEO-optimized content
tutorial-engineer: Create step-by-step guide
```

## Multi-Agent Workflows

Subagents coordinate automatically for complex tasks. The system intelligently sequences multiple specialists based on task requirements.

### Common Workflow Patterns

**Feature Development**
```
"Implement user authentication"
→ backend-architect → frontend-developer → test-automator → security-auditor
```

**Performance Optimization**
```
"Optimize checkout process"
→ performance-engineer → database-optimizer → frontend-developer
```

**Production Incidents**
```
"Debug high memory usage"
→ incident-responder → devops-troubleshooter → error-detective → performance-engineer
```

**Documentation & Content**
```
"Create comprehensive API documentation"
→ api-documenter → tutorial-engineer → docs-architect
```

## Subagent Format

Each subagent is defined as a Markdown file with frontmatter:

```markdown
---
name: subagent-name
description: Activation criteria for this subagent
model: haiku|sonnet|opus  # Optional: Model selection
tools: tool1, tool2       # Optional: Tool restrictions
---

System prompt defining the subagent's expertise and behavior
```

### Model Selection Criteria

- **haiku**: Simple, deterministic tasks with minimal reasoning
- **sonnet**: Standard development and engineering tasks
- **opus**: Complex analysis, architecture, and critical operations

## Agent Orchestration Patterns

### Sequential Processing
Agents execute in sequence, passing context forward:
```
backend-architect → frontend-developer → test-automator → security-auditor
```

### Parallel Execution
Multiple agents work simultaneously on different aspects:
```
performance-engineer + database-optimizer → Merged analysis
```

### Conditional Routing
Dynamic agent selection based on analysis:
```
debugger → [backend-architect | frontend-developer | devops-troubleshooter]
```

### Validation Pipeline
Primary work followed by specialized review:
```
backend-architect → security-auditor → Validated implementation
```

## Agent Selection Guide

### Architecture & Planning

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| API Design | `backend-architect` | RESTful APIs, microservices, database schemas |
| Cloud Infrastructure | `cloud-architect` | AWS/Azure/GCP design, scalability planning |
| UI/UX Design | `ui-ux-designer` | Interface design, wireframes, design systems |
| System Architecture | `architect-reviewer` | Pattern validation, consistency analysis |

### Development

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Frontend Development | `frontend-developer` | React components, responsive layouts, state management |
| Mobile Development | `flutter-expert` | Cross-platform mobile apps with Flutter |
| TypeScript Development | `typescript-pro` | Type-safe applications with advanced TypeScript |

### Operations & Infrastructure

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Production Issues | `devops-troubleshooter` | Log analysis, deployment debugging |
| Critical Incidents | `incident-responder` | Outage response, immediate mitigation |
| Database Performance | `database-optimizer` | Query optimization, indexing strategies |
| CI/CD Pipelines | `deployment-engineer` | Containerization, cloud deployments |
| Developer Experience | `dx-optimizer` | Tooling improvements, workflow optimization |

### Quality & Security

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Code Review | `code-reviewer` | Security focus, best practices |
| Security Audit | `security-auditor` | Vulnerability scanning, OWASP compliance |
| Backend Security | `backend-security-coder` | Secure API implementation |
| Frontend Security | `frontend-security-coder` | XSS prevention, CSP implementation |
| Test Creation | `test-automator` | Unit, integration, E2E test suites |
| Performance Issues | `performance-engineer` | Profiling, optimization |
| Bug Investigation | `debugger` | Error resolution, root cause analysis |
| Log Analysis | `error-detective` | Error pattern recognition |

### AI & Research

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Prompt Engineering | `prompt-engineer` | LLM prompt optimization |
| Web Research | `search-specialist` | Information synthesis |

### Documentation & Content

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Technical Docs | `docs-architect` | Comprehensive documentation generation |
| API Documentation | `api-documenter` | OpenAPI/Swagger specifications |
| Technical References | `reference-builder` | API documentation |
| Tutorials | `tutorial-engineer` | Step-by-step guides |
| Diagrams | `mermaid-expert` | Flowcharts, sequences, ERDs |
| Content Marketing | `content-marketer` | Blog posts, email campaigns |
| Sales Content | `sales-automator` | Cold emails, proposals |
| Support Content | `customer-support` | FAQ responses, customer communication |
| SEO Content | `seo-content-writer` | SEO-optimized content creation |

## Best Practices

### Task Delegation
1. **Automatic selection** - Let Claude Code analyze context and select optimal agents
2. **Clear requirements** - Specify constraints, tech stack, and quality standards
3. **Trust specialization** - Each agent is optimized for their specific domain

### Multi-Agent Workflows
1. **High-level requests** - Allow agents to coordinate complex multi-step tasks
2. **Context preservation** - Ensure agents have necessary background information
3. **Integration review** - Verify how different agents' outputs work together

### Explicit Control
1. **Direct invocation** - Specify agents when you need particular expertise
2. **Strategic combination** - Use multiple specialists for validation
3. **Review patterns** - Request specific review workflows (e.g., "security-auditor reviews API design")

### Performance Optimization
1. **Monitor effectiveness** - Track which agents work best for your use cases
2. **Iterative refinement** - Use agent feedback to improve requirements
3. **Complexity matching** - Align task complexity with agent capabilities

## Repository Structure

```
agents/                      # All agent definitions from upstream
tools/                       # Optional Claude Code tools
workflows/                   # Example multi-agent workflows
examples/                    # Usage examples

agents-config.json           # Organization-wide agent whitelist
sync-agents.js              # Sync script
```

## Contributing

### Adding Agents from Upstream

To use additional agents from [wshobson/agents](https://github.com/wshobson/agents):

1. Review the [complete agent list](https://github.com/wshobson/agents) in the upstream repository
2. Add the agent filename (with or without `.md` extension) to the `whitelist` array in `agents-config.json`
3. Run `node sync-agents.js` to sync the newly whitelisted agent

**Example:**
```json
{
  "whitelist": [
    "backend-architect.md",
    "your-new-agent.md"
  ]
}
```

### Creating Custom Agents

To create a custom agent for your organization:

1. Create a new `.md` file in the `agents/` directory with appropriate frontmatter
2. Use lowercase, hyphen-separated naming convention
3. Write clear activation criteria in the description
4. Define comprehensive system prompt with expertise areas
5. Add the agent filename to the `whitelist` in `agents-config.json`
6. Run `node sync-agents.js` to sync your custom agent

**Important:** Only agents whitelisted in `agents-config.json` will be synced to your local Claude Code configuration.

## Troubleshooting

### Agent Not Activating
- Ensure request clearly indicates the domain
- Be specific about task type and requirements
- Use explicit invocation if automatic selection fails

### Unexpected Agent Selection
- Provide more context about tech stack
- Include specific requirements in request
- Use direct agent naming for precise control

### Conflicting Recommendations
- Normal behavior - specialists have different priorities
- Request reconciliation between specific agents
- Consider trade-offs based on project requirements

### Missing Context
- Include background information in requests
- Reference previous work or patterns
- Provide project-specific constraints

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Original Repository](https://github.com/wshobson/agents)
