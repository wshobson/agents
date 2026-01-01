# Claude Code Subagents Collection

A comprehensive collection of 92 specialized AI subagents for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), providing domain-specific expertise across software development, infrastructure, and business operations.

## Overview

This repository provides production-ready subagents that extend Claude Code's capabilities with specialized knowledge. Each subagent incorporates:

- Current industry best practices and standards (2024/2025)
- Production-ready patterns and enterprise architectures
- Deep domain expertise with 8-12 capability areas per agent
- Modern technology stacks and frameworks
- Optimized model selection based on task complexity

## Agent Categories

### Architecture & System Design

#### Core Architecture

| Agent | Model | Description |
|-------|-------|-------------|
| [backend-architect](backend-architect.md) | opus | RESTful API design, microservice boundaries, database schemas |
| [frontend-developer](frontend-developer.md) | sonnet | React components, responsive layouts, client-side state management |
| [graphql-architect](graphql-architect.md) | opus | GraphQL schemas, resolvers, federation architecture |
| [architect-reviewer](architect-review.md) | opus | Architectural consistency analysis and pattern validation |
| [cloud-architect](cloud-architect.md) | opus | AWS/Azure/GCP infrastructure design and cost optimization |
| [hybrid-cloud-architect](hybrid-cloud-architect.md) | opus | Multi-cloud strategies across cloud and on-premises environments |
| [kubernetes-architect](kubernetes-architect.md) | opus | Cloud-native infrastructure with Kubernetes and GitOps |

#### UI/UX & Mobile

| Agent | Model | Description |
|-------|-------|-------------|
| [ui-ux-designer](ui-ux-designer.md) | sonnet | Interface design, wireframes, design systems |
| [ui-visual-validator](ui-visual-validator.md) | sonnet | Visual regression testing and UI verification |
| [mobile-developer](mobile-developer.md) | sonnet | React Native and Flutter application development |
| [ios-developer](ios-developer.md) | sonnet | Native iOS development with Swift/SwiftUI |
| [flutter-expert](flutter-expert.md) | sonnet | Advanced Flutter development with state management |

### Programming Languages

#### Systems & Low-Level

| Agent | Model | Description |
|-------|-------|-------------|
| [c-pro](c-pro.md) | sonnet | System programming with memory management and OS interfaces |
| [cpp-pro](cpp-pro.md) | sonnet | Modern C++ with RAII, smart pointers, STL algorithms |
| [rust-pro](rust-pro.md) | sonnet | Memory-safe systems programming with ownership patterns |
| [golang-pro](golang-pro.md) | sonnet | Concurrent programming with goroutines and channels |

#### Web & Application

| Agent | Model | Description |
|-------|-------|-------------|
| [javascript-pro](javascript-pro.md) | sonnet | Modern JavaScript with ES6+, async patterns, Node.js |
| [typescript-pro](typescript-pro.md) | sonnet | Advanced TypeScript with type systems and generics |
| [python-pro](python-pro.md) | sonnet | Python development with advanced features and optimization |
| [ruby-pro](ruby-pro.md) | sonnet | Ruby with metaprogramming, Rails patterns, gem development |
| [php-pro](php-pro.md) | sonnet | Modern PHP with frameworks and performance optimization |

#### Enterprise & JVM

| Agent | Model | Description |
|-------|-------|-------------|
| [java-pro](java-pro.md) | sonnet | Modern Java with streams, concurrency, JVM optimization |
| [scala-pro](scala-pro.md) | sonnet | Enterprise Scala with functional programming and distributed systems |
| [csharp-pro](csharp-pro.md) | sonnet | C# development with .NET frameworks and patterns |

#### Specialized Platforms

| Agent | Model | Description |
|-------|-------|-------------|
| [elixir-pro](elixir-pro.md) | sonnet | Elixir with OTP patterns and Phoenix frameworks |
| [unity-developer](unity-developer.md) | sonnet | Unity game development and optimization |
| [minecraft-bukkit-pro](minecraft-bukkit-pro.md) | sonnet | Minecraft server plugin development |
| [sql-pro](sql-pro.md) | sonnet | Complex SQL queries and database optimization |

### Infrastructure & Operations

#### DevOps & Deployment

| Agent | Model | Description |
|-------|-------|-------------|
| [devops-troubleshooter](devops-troubleshooter.md) | sonnet | Production debugging, log analysis, deployment troubleshooting |
| [deployment-engineer](deployment-engineer.md) | sonnet | CI/CD pipelines, containerization, cloud deployments |
| [terraform-specialist](terraform-specialist.md) | opus | Infrastructure as Code with Terraform modules and state management |
| [dx-optimizer](dx-optimizer.md) | sonnet | Developer experience optimization and tooling improvements |
| [sre-engineer](sre-engineer.md) | opus | SLO/SLA management, error budgets, reliability engineering |
| [platform-engineer](platform-engineer.md) | opus | Internal Developer Platforms, self-service infrastructure |
| [chaos-engineer](chaos-engineer.md) | sonnet | Fault injection, resilience testing, failure scenarios |
| [gitops-specialist](gitops-specialist.md) | sonnet | ArgoCD, Flux, GitOps workflows, progressive delivery |
| [release-manager](release-manager.md) | sonnet | Release orchestration, version control, rollback procedures |

#### Database Management

| Agent | Model | Description |
|-------|-------|-------------|
| [database-optimizer](database-optimizer.md) | opus | Query optimization, index design, migration strategies |
| [database-admin](database-admin.md) | sonnet | Database operations, backup, replication, monitoring |

#### Incident Response & Network

| Agent | Model | Description |
|-------|-------|-------------|
| [incident-responder](incident-responder.md) | opus | Production incident management and resolution |
| [network-engineer](network-engineer.md) | sonnet | Network debugging, load balancing, traffic analysis |

### Quality Assurance & Security

#### Code Quality & Review

| Agent | Model | Description |
|-------|-------|-------------|
| [code-reviewer](code-reviewer.md) | opus | Code review with security focus and production reliability |
| [security-auditor](security-auditor.md) | opus | Vulnerability assessment and OWASP compliance |
| [backend-security-coder](backend-security-coder.md) | opus | Secure backend coding practices, API security implementation |
| [frontend-security-coder](frontend-security-coder.md) | opus | XSS prevention, CSP implementation, client-side security |
| [mobile-security-coder](mobile-security-coder.md) | opus | Mobile security patterns, WebView security, biometric auth |
| [architect-reviewer](architect-review.md) | opus | Architectural consistency and pattern validation |

#### Testing & Debugging

| Agent | Model | Description |
|-------|-------|-------------|
| [test-automator](test-automator.md) | sonnet | Comprehensive test suite creation (unit, integration, e2e) |
| [tdd-orchestrator](tdd-orchestrator.md) | sonnet | Test-Driven Development methodology guidance |
| [debugger](debugger.md) | sonnet | Error resolution and test failure analysis |
| [error-detective](error-detective.md) | sonnet | Log analysis and error pattern recognition |

#### Performance & Research

| Agent | Model | Description |
|-------|-------|-------------|
| [performance-engineer](performance-engineer.md) | opus | Application profiling and optimization |
| [search-specialist](search-specialist.md) | haiku | Advanced web research and information synthesis |

### Data & AI

#### Data Engineering & Analytics

| Agent | Model | Description |
|-------|-------|-------------|
| [data-scientist](data-scientist.md) | opus | Data analysis, SQL queries, BigQuery operations |
| [data-engineer](data-engineer.md) | sonnet | ETL pipelines, data warehouses, streaming architectures |
| [bi-developer](bi-developer.md) | sonnet | Power BI, Tableau, data visualization, dashboards |
| [data-platform-architect](data-platform-architect.md) | opus | Data mesh, data fabric, end-to-end data architecture |

#### Machine Learning & AI

| Agent | Model | Description |
|-------|-------|-------------|
| [ai-engineer](ai-engineer.md) | opus | LLM applications, RAG systems, prompt pipelines |
| [ml-engineer](ml-engineer.md) | opus | ML pipelines, model serving, feature engineering |
| [mlops-engineer](mlops-engineer.md) | opus | ML infrastructure, experiment tracking, model registries |
| [prompt-engineer](prompt-engineer.md) | opus | LLM prompt optimization and engineering |
| [computer-vision-engineer](computer-vision-engineer.md) | opus | OpenCV, object detection, image processing, vision AI |
| [nlp-llm-engineer](nlp-llm-engineer.md) | opus | Text processing, transformers, BERT, GPT fine-tuning |
| [deep-learning-engineer](deep-learning-engineer.md) | opus | Neural networks, model architecture design, PyTorch/TF |

### Documentation & Technical Writing

| Agent | Model | Description |
|-------|-------|-------------|
| [docs-architect](docs-architect.md) | opus | Comprehensive technical documentation generation |
| [api-documenter](api-documenter.md) | sonnet | OpenAPI/Swagger specifications and developer docs |
| [reference-builder](reference-builder.md) | haiku | Technical references and API documentation |
| [tutorial-engineer](tutorial-engineer.md) | sonnet | Step-by-step tutorials and educational content |
| [mermaid-expert](mermaid-expert.md) | sonnet | Diagram creation (flowcharts, sequences, ERDs) |

### Business & Operations

#### Business Analysis & Finance

| Agent | Model | Description |
|-------|-------|-------------|
| [business-analyst](business-analyst.md) | sonnet | Metrics analysis, reporting, KPI tracking |
| [quant-analyst](quant-analyst.md) | opus | Financial modeling, trading strategies, market analysis |
| [risk-manager](risk-manager.md) | sonnet | Portfolio risk monitoring and management |

#### Marketing & Sales

| Agent | Model | Description |
|-------|-------|-------------|
| [content-marketer](content-marketer.md) | sonnet | Blog posts, social media, email campaigns |
| [sales-automator](sales-automator.md) | haiku | Cold emails, follow-ups, proposal generation |

#### Support & Legal

| Agent | Model | Description |
|-------|-------|-------------|
| [customer-support](customer-support.md) | sonnet | Support tickets, FAQ responses, customer communication |
| [hr-pro](hr-pro.md) | opus | HR operations, policies, employee relations |
| [legal-advisor](legal-advisor.md) | opus | Privacy policies, terms of service, legal documentation |

### Specialized Domains

| Agent | Model | Description |
|-------|-------|-------------|
| [blockchain-developer](blockchain-developer.md) | sonnet | Web3 apps, smart contracts, DeFi protocols |
| [payment-integration](payment-integration.md) | sonnet | Payment processor integration (Stripe, PayPal) |
| [legacy-modernizer](legacy-modernizer.md) | sonnet | Legacy code refactoring and modernization |
| [context-manager](context-manager.md) | haiku | Multi-agent context management |

### SEO & Content Optimization

| Agent | Model | Description |
|-------|-------|-------------|
| [seo-content-auditor](seo-content-auditor.md) | sonnet | Content quality analysis, E-E-A-T signals assessment |
| [seo-meta-optimizer](seo-meta-optimizer.md) | haiku | Meta title and description optimization |
| [seo-keyword-strategist](seo-keyword-strategist.md) | haiku | Keyword analysis and semantic variations |
| [seo-structure-architect](seo-structure-architect.md) | haiku | Content structure and schema markup |
| [seo-snippet-hunter](seo-snippet-hunter.md) | haiku | Featured snippet formatting |
| [seo-content-refresher](seo-content-refresher.md) | haiku | Content freshness analysis |
| [seo-cannibalization-detector](seo-cannibalization-detector.md) | haiku | Keyword overlap detection |
| [seo-authority-builder](seo-authority-builder.md) | sonnet | E-E-A-T signal analysis |
| [seo-content-writer](seo-content-writer.md) | sonnet | SEO-optimized content creation |
| [seo-content-planner](seo-content-planner.md) | haiku | Content planning and topic clusters |

## Model Configuration

Agents are assigned to specific Claude models based on task complexity and computational requirements. The system uses three model tiers:

### Model Distribution Summary

| Model | Agent Count | Use Case |
|-------|-------------|----------|
| Haiku | 11 | Quick, focused tasks with minimal computational overhead |
| Sonnet | 50 | Standard development and specialized engineering tasks |
| Opus | 31 | Complex reasoning, architecture, and critical analysis |

### Haiku Model Agents

| Category | Agents |
|----------|--------|
| Context & Reference | `context-manager`, `reference-builder`, `sales-automator`, `search-specialist` |
| SEO Optimization | `seo-meta-optimizer`, `seo-keyword-strategist`, `seo-structure-architect`, `seo-snippet-hunter`, `seo-content-refresher`, `seo-cannibalization-detector`, `seo-content-planner` |

### Sonnet Model Agents

| Category | Count | Agents |
|----------|-------|--------|
| Programming Languages | 18 | All language-specific agents (JavaScript, Python, Java, C++, etc.) |
| Frontend & UI | 5 | `frontend-developer`, `ui-ux-designer`, `ui-visual-validator`, `mobile-developer`, `ios-developer` |
| Infrastructure | 12 | `devops-troubleshooter`, `deployment-engineer`, `dx-optimizer`, `database-admin`, `network-engineer`, `flutter-expert`, `api-documenter`, `tutorial-engineer`, `chaos-engineer`, `gitops-specialist`, `release-manager`, `bi-developer` |
| Quality & Testing | 4 | `test-automator`, `tdd-orchestrator`, `debugger`, `error-detective` |
| Business & Support | 6 | `business-analyst`, `risk-manager`, `content-marketer`, `customer-support`, `mermaid-expert`, `legacy-modernizer` |
| Data & Content | 5 | `data-engineer`, `payment-integration`, `seo-content-auditor`, `seo-authority-builder`, `seo-content-writer` |

### Opus Model Agents

| Category | Count | Agents |
|----------|-------|--------|
| Architecture & Design | 7 | `architect-reviewer`, `backend-architect`, `cloud-architect`, `hybrid-cloud-architect`, `kubernetes-architect`, `graphql-architect`, `terraform-specialist` |
| Critical Analysis | 5 | `code-reviewer`, `security-auditor`, `performance-engineer`, `incident-responder`, `database-optimizer` |
| AI/ML Complex | 8 | `ai-engineer`, `ml-engineer`, `mlops-engineer`, `data-scientist`, `prompt-engineer`, `computer-vision-engineer`, `nlp-llm-engineer`, `deep-learning-engineer` |
| Business Critical | 5 | `docs-architect`, `hr-pro`, `legal-advisor`, `quant-analyst`, `data-platform-architect` |
| DevOps/Platform | 2 | `sre-engineer`, `platform-engineer` |

## Installation

Clone the repository to the Claude agents directory:

```bash
cd ~/.claude
git clone https://github.com/wshobson/agents.git
```

The subagents will be automatically available to Claude Code once placed in the `~/.claude/agents/` directory.

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
tdd-orchestrator: Implement feature with test-first approach
performance-engineer: Profile and optimize bottlenecks
```

### Development & Architecture
```
backend-architect: Design authentication API
frontend-developer: Create responsive dashboard
graphql-architect: Design federated GraphQL schema
mobile-developer: Build cross-platform mobile app
```

### Infrastructure & Operations
```
devops-troubleshooter: Analyze production logs
cloud-architect: Design scalable AWS architecture
network-engineer: Debug SSL certificate issues
database-admin: Configure backup and replication
terraform-specialist: Write infrastructure modules
```

### Data & Machine Learning
```
data-scientist: Analyze customer behavior dataset
ai-engineer: Build RAG system for document search
mlops-engineer: Set up experiment tracking
ml-engineer: Deploy model to production
```

### Business & Documentation
```
business-analyst: Create metrics dashboard
docs-architect: Generate technical documentation
api-documenter: Write OpenAPI specifications
content-marketer: Create SEO-optimized content
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

**Infrastructure Setup**
```
"Set up disaster recovery"
→ database-admin → database-optimizer → terraform-specialist
```

**ML Pipeline Development**
```
"Build ML pipeline with monitoring"
→ mlops-engineer → ml-engineer → data-engineer → performance-engineer
```

### Integration with Claude Code Commands

For sophisticated multi-agent orchestration, use the [Claude Code Commands](https://github.com/wshobson/commands) collection which provides 52 pre-built slash commands:

```
/full-stack-feature   # Coordinates 8+ agents for complete feature development
/incident-response    # Activates incident management workflow
/ml-pipeline         # Sets up end-to-end ML infrastructure
/security-hardening  # Implements security best practices across stack
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
payment-integration → security-auditor → Validated implementation
```

## Agent Selection Guide

### Architecture & Planning

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| API Design | `backend-architect` | RESTful APIs, microservices, database schemas |
| Cloud Infrastructure | `cloud-architect` | AWS/Azure/GCP design, scalability planning |
| UI/UX Design | `ui-ux-designer` | Interface design, wireframes, design systems |
| System Architecture | `architect-reviewer` | Pattern validation, consistency analysis |

### Development by Language

| Language Category | Agents | Primary Use Cases |
|-------------------|--------|-------------------|
| Systems Programming | `c-pro`, `cpp-pro`, `rust-pro`, `golang-pro` | OS interfaces, embedded systems, high performance |
| Web Development | `javascript-pro`, `typescript-pro`, `python-pro`, `ruby-pro`, `php-pro` | Full-stack web applications, APIs, scripting |
| Enterprise | `java-pro`, `csharp-pro`, `scala-pro` | Large-scale applications, enterprise systems |
| Mobile | `ios-developer`, `flutter-expert`, `mobile-developer` | Native and cross-platform mobile apps |
| Specialized | `elixir-pro`, `unity-developer`, `minecraft-bukkit-pro` | Domain-specific development |

### Operations & Infrastructure

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Production Issues | `devops-troubleshooter` | Log analysis, deployment debugging |
| Critical Incidents | `incident-responder` | Outage response, immediate mitigation |
| Database Performance | `database-optimizer` | Query optimization, indexing strategies |
| Database Operations | `database-admin` | Backup, replication, disaster recovery |
| Infrastructure as Code | `terraform-specialist` | Terraform modules, state management |
| Network Issues | `network-engineer` | Network debugging, load balancing |

### Quality & Security

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Code Review | `code-reviewer` | Security focus, best practices |
| Security Audit | `security-auditor` | Vulnerability scanning, OWASP compliance |
| Test Creation | `test-automator` | Unit, integration, E2E test suites |
| Performance Issues | `performance-engineer` | Profiling, optimization |
| Bug Investigation | `debugger` | Error resolution, root cause analysis |

### Data & Machine Learning

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Data Analysis | `data-scientist` | SQL queries, statistical analysis |
| LLM Applications | `ai-engineer` | RAG systems, prompt pipelines |
| ML Development | `ml-engineer` | Model training, feature engineering |
| ML Operations | `mlops-engineer` | ML infrastructure, experiment tracking |

### Documentation & Business

| Task | Recommended Agent | Key Capabilities |
|------|------------------|------------------|
| Technical Docs | `docs-architect` | Comprehensive documentation generation |
| API Documentation | `api-documenter` | OpenAPI/Swagger specifications |
| Business Metrics | `business-analyst` | KPI tracking, reporting |
| Legal Compliance | `legal-advisor` | Privacy policies, terms of service |

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

## Contributing

To add a new subagent:

1. Create a new `.md` file with appropriate frontmatter
2. Use lowercase, hyphen-separated naming convention
3. Write clear activation criteria in the description
4. Define comprehensive system prompt with expertise areas

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
- [Claude Code Commands](https://github.com/wshobson/commands)
