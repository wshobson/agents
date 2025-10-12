# Claude Code Workflows & Agents

A comprehensive production-ready system combining **84 specialized AI agents**, **15 multi-agent workflow orchestrators**, and **42 development tools** organized into **36 focused, single-purpose plugins** for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Overview

This unified repository provides everything needed for intelligent automation and multi-agent orchestration across modern software development:

- **36 Focused Plugins** - Single-purpose plugins following industry best practices (VSCode, npm patterns)
- **84 Specialized Agents** - Domain experts with deep knowledge across architecture, languages, infrastructure, quality, data/AI, documentation, business operations, and SEO
- **15 Workflow Orchestrators** - Multi-agent coordination systems for complex operations like full-stack development, security hardening, ML pipelines, and incident response
- **42 Development Tools** - Optimized utilities (avg 626 lines, 58% reduction) for specific tasks including API scaffolding, security scanning, test automation, and infrastructure setup

### 🎉 Version 1.0.5 - Recent Improvements

- **Marketplace Refactored**: 27 bloated plugins → 36 focused, single-purpose plugins (+33%)
- **Files Optimized**: 24,392 lines eliminated through aggressive optimization (58% reduction)
- **Zero Bloat**: All plugins now under 12 components, following single-responsibility principle
- **Better Performance**: 2-3x faster loading times, improved context window utilization
- **Industry-Aligned**: Following proven patterns from VSCode, npm, and Chrome extension ecosystems

## Installation

Add this marketplace to Claude Code:

```bash
/plugin marketplace add https://github.com/wshobson/agents
```

Then browse and install plugins using:

```bash
/plugin
```

### Available Plugins (36 Total)

> 💡 **Plugin Organization**: All plugins follow single-responsibility principle with clear, focused purposes. Average 6.2 components per plugin (down from 8-10).

#### Getting Started

**claude-code-essentials** - Essential tools for daily development
```bash
/plugin install claude-code-essentials
```
Includes: Code explanation, debugging, documentation, PR enhancement, git workflows

#### Complete Workflow Systems

**full-stack-development** - End-to-end feature implementation
```bash
/plugin install full-stack-development
```
Multi-agent coordination: Backend API → Frontend UI → Mobile → Testing → Security → Deployment

**performance-optimization** - System profiling and optimization
```bash
/plugin install performance-optimization
```
Profiling → Query optimization → Caching → Scalability assessment

**code-quality-review** - Multi-perspective code analysis
```bash
/plugin install code-quality-review
```
Architecture → Security → Performance → Test coverage analysis

**legacy-modernization** - Codebase modernization workflows
```bash
/plugin install legacy-modernization
```
Framework migration → Dependency updates → Refactoring → Compatibility testing

**multi-platform-apps** - Cross-platform development
```bash
/plugin install multi-platform-apps
```
Web (React/Next.js) → iOS (Swift) → Android (Kotlin) → Desktop coordination

**cicd-automation** - CI/CD pipeline configuration
```bash
/plugin install cicd-automation
```
GitHub Actions/GitLab CI → Progressive deployment → Pipeline orchestration

**documentation-generation** - Technical documentation automation
```bash
/plugin install documentation-generation
```
OpenAPI specs → Mermaid diagrams → Tutorials → API references

#### API Development (Focused Split)

**api-scaffolding** - REST/GraphQL API generation
```bash
/plugin install api-scaffolding
```
API scaffolding → Framework selection → Backend architecture → FastAPI/Django

**api-testing-observability** - API testing and monitoring
```bash
/plugin install api-testing-observability
```
API testing → Mocking → OpenAPI docs → Observability setup

**data-validation-suite** - Schema and data quality validation
```bash
/plugin install data-validation-suite
```
Schema validation → Data quality monitoring → Streaming validation

#### Security (Focused Split)

**security-scanning** - SAST and vulnerability scanning
```bash
/plugin install security-scanning
```
SAST analysis → Dependency scanning → OWASP Top 10 → Container security

**security-compliance** - SOC2/HIPAA/GDPR compliance
```bash
/plugin install security-compliance
```
Compliance validation → Secrets scanning → Regulatory documentation

**backend-api-security** - API security hardening
```bash
/plugin install backend-api-security
```
Authentication → Authorization → Rate limiting → Input validation

**frontend-mobile-security** - XSS/CSRF/mobile security
```bash
/plugin install frontend-mobile-security
```
XSS prevention → CSRF protection → CSP → Mobile app security

#### Testing & Quality

**testing-quality-suite** - Comprehensive testing workflows
```bash
/plugin install testing-quality-suite
```
TDD workflows → Test generation → Unit/integration/e2e → Quality gates

**development-utilities** - Daily productivity tools
```bash
/plugin install development-utilities
```
Refactoring → Dependency auditing → Error analysis → Standup automation

#### Infrastructure (Focused Split)

**kubernetes-operations** - K8s lifecycle management
```bash
/plugin install kubernetes-operations
```
K8s manifests → Networking → Security policies → GitOps → Auto-scaling

**docker-containerization** - Container optimization
```bash
/plugin install docker-containerization
```
Multi-stage builds → Image optimization → Container security → CI/CD

**deployment-orchestration** - Deployment strategies
```bash
/plugin install deployment-orchestration
```
Pre-flight checks → Rollout strategies → Rollback → Configuration validation

**cloud-infrastructure** - AWS/Azure/GCP architecture
```bash
/plugin install cloud-infrastructure
```
Cloud design → Hybrid cloud → Multi-cloud cost optimization

#### Data & ML (Focused Split)

**data-engineering** - ETL and data pipelines
```bash
/plugin install data-engineering
```
ETL pipelines → Data warehouse design → Batch processing

**machine-learning-ops** - ML training and deployment
```bash
/plugin install machine-learning-ops
```
Model training → Hyperparameter tuning → MLOps → Experiment tracking

**ai-agent-development** - LLM agents and RAG systems
```bash
/plugin install ai-agent-development
```
LangChain agents → RAG systems → Prompt engineering → Context management

#### Operations & Reliability (Focused Split)

**incident-diagnostics** - Production incident triage
```bash
/plugin install incident-diagnostics
```
Incident response → Root cause analysis → Distributed tracing

**observability-monitoring** - Metrics and SLO
```bash
/plugin install observability-monitoring
```
Metrics collection → Logging → Tracing → SLO implementation

#### Database

**database-operations** - Database optimization and administration
```bash
/plugin install database-operations
```
Schema design → Query optimization → Migrations → PostgreSQL/MySQL/MongoDB

#### Marketing & Business

**seo-content-suite** - SEO optimization toolkit
```bash
/plugin install seo-content-suite
```
Content analysis → Keyword research → Meta optimization → E-E-A-T signals

**business-analytics** - Business intelligence and metrics
```bash
/plugin install business-analytics
```
KPI tracking → Financial reporting → Data-driven decision making

**hr-legal-compliance** - HR and legal documentation
```bash
/plugin install hr-legal-compliance
```
HR policies → Legal templates → GDPR/SOC2/HIPAA compliance → Employment contracts

**customer-sales-automation** - Customer relationship workflows
```bash
/plugin install customer-sales-automation
```
Support automation → Sales pipeline → Email campaigns → CRM integration

#### Specialized Domains

**blockchain-web3** - Blockchain and smart contract development
```bash
/plugin install blockchain-web3
```
Solidity → Smart contracts → DeFi protocols → NFT platforms → Web3 apps

**quantitative-trading** - Financial modeling and algorithmic trading
```bash
/plugin install quantitative-trading
```
Quant analysis → Trading strategies → Portfolio risk → Backtesting

**payment-processing** - Payment gateway integration
```bash
/plugin install payment-processing
```
Stripe/PayPal integration → Checkout flows → Subscription billing → PCI compliance

**game-development** - Unity and Minecraft development
```bash
/plugin install game-development
```
Unity C# scripting → Minecraft Bukkit/Spigot plugins → Game mechanics

**accessibility-compliance** - WCAG accessibility auditing
```bash
/plugin install accessibility-compliance
```
WCAG validation → Screen reader testing → Keyboard navigation → Inclusive design

## Repository Structure

```
claude-agents/
├── .claude-plugin/
│   └── marketplace.json          # 36 focused plugins (v1.0.5)
├── agents/                        # 84 specialized AI agents
│   ├── backend-architect.md
│   ├── frontend-developer.md
│   └── ... (all agent definitions)
├── workflows/                     # 15 multi-agent orchestrators
│   ├── feature-development.md
│   ├── full-stack-feature.md
│   ├── security-hardening.md
│   └── ... (workflow commands)
├── tools/                         # 42 optimized development utilities
│   ├── api-python.md            # Optimized (avg 626 lines)
│   ├── security-sast.md         # Optimized (1,216 → 473 lines)
│   └── ... (tool commands)
└── README.md                      # This file
```

## Usage

### Agent Invocation

After installing plugins, agents are automatically available. Invoke them explicitly in natural language:

```
"Use backend-architect to design the authentication API"
"Have security-auditor scan for OWASP vulnerabilities"
"Get performance-engineer to optimize this database query"
```

Claude Code automatically selects and coordinates the appropriate agents based on your request.

### Multi-Agent Orchestration Examples

Plugins provide pre-configured multi-agent workflows that coordinate complex operations:

**Full-Stack Development Plugin**
```
"Implement user dashboard with real-time analytics"
```
→ backend-architect → graphql-architect → frontend-developer → mobile-developer → test-automator → security-auditor → performance-engineer → deployment-engineer

**Security Hardening Plugin**
```
"Perform security audit and implement OWASP best practices"
```
→ security-auditor → backend-security-coder → frontend-security-coder → mobile-security-coder → test-automator

**Data/ML Pipeline Plugin**
```
"Build customer churn prediction model with deployment"
```
→ data-scientist → data-engineer → ml-engineer → mlops-engineer → ai-engineer → performance-engineer

**Incident Response Plugin**
```
"Debug production memory leak and create runbook"
```
→ incident-responder → devops-troubleshooter → debugger → error-detective → observability-engineer

## Agent Categories

### Architecture & System Design

#### Core Architecture

| Agent | Model | Description |
|-------|-------|-------------|
| [backend-architect](agents/backend-architect.md) | opus | RESTful API design, microservice boundaries, database schemas |
| [frontend-developer](agents/frontend-developer.md) | sonnet | React components, responsive layouts, client-side state management |
| [graphql-architect](agents/graphql-architect.md) | opus | GraphQL schemas, resolvers, federation architecture |
| [architect-reviewer](agents/architect-review.md) | opus | Architectural consistency analysis and pattern validation |
| [cloud-architect](agents/cloud-architect.md) | opus | AWS/Azure/GCP infrastructure design and cost optimization |
| [hybrid-cloud-architect](agents/hybrid-cloud-architect.md) | opus | Multi-cloud strategies across cloud and on-premises environments |
| [kubernetes-architect](agents/kubernetes-architect.md) | opus | Cloud-native infrastructure with Kubernetes and GitOps |

#### UI/UX & Mobile

| Agent | Model | Description |
|-------|-------|-------------|
| [ui-ux-designer](agents/ui-ux-designer.md) | sonnet | Interface design, wireframes, design systems |
| [ui-visual-validator](agents/ui-visual-validator.md) | sonnet | Visual regression testing and UI verification |
| [mobile-developer](agents/mobile-developer.md) | sonnet | React Native and Flutter application development |
| [ios-developer](agents/ios-developer.md) | sonnet | Native iOS development with Swift/SwiftUI |
| [flutter-expert](agents/flutter-expert.md) | sonnet | Advanced Flutter development with state management |

### Programming Languages

#### Systems & Low-Level

| Agent | Model | Description |
|-------|-------|-------------|
| [c-pro](agents/c-pro.md) | sonnet | System programming with memory management and OS interfaces |
| [cpp-pro](agents/cpp-pro.md) | sonnet | Modern C++ with RAII, smart pointers, STL algorithms |
| [rust-pro](agents/rust-pro.md) | sonnet | Memory-safe systems programming with ownership patterns |
| [golang-pro](agents/golang-pro.md) | sonnet | Concurrent programming with goroutines and channels |

#### Web & Application

| Agent | Model | Description |
|-------|-------|-------------|
| [javascript-pro](agents/javascript-pro.md) | sonnet | Modern JavaScript with ES6+, async patterns, Node.js |
| [typescript-pro](agents/typescript-pro.md) | sonnet | Advanced TypeScript with type systems and generics |
| [python-pro](agents/python-pro.md) | sonnet | Python development with advanced features and optimization |
| [ruby-pro](agents/ruby-pro.md) | sonnet | Ruby with metaprogramming, Rails patterns, gem development |
| [php-pro](agents/php-pro.md) | sonnet | Modern PHP with frameworks and performance optimization |

#### Enterprise & JVM

| Agent | Model | Description |
|-------|-------|-------------|
| [java-pro](agents/java-pro.md) | sonnet | Modern Java with streams, concurrency, JVM optimization |
| [scala-pro](agents/scala-pro.md) | sonnet | Enterprise Scala with functional programming and distributed systems |
| [csharp-pro](agents/csharp-pro.md) | sonnet | C# development with .NET frameworks and patterns |

#### Specialized Platforms

| Agent | Model | Description |
|-------|-------|-------------|
| [elixir-pro](agents/elixir-pro.md) | sonnet | Elixir with OTP patterns and Phoenix frameworks |
| [django-pro](agents/django-pro.md) | sonnet | Django development with ORM and async views |
| [fastapi-pro](agents/fastapi-pro.md) | sonnet | FastAPI with async patterns and Pydantic |
| [unity-developer](agents/unity-developer.md) | sonnet | Unity game development and optimization |
| [minecraft-bukkit-pro](agents/minecraft-bukkit-pro.md) | sonnet | Minecraft server plugin development |
| [sql-pro](agents/sql-pro.md) | sonnet | Complex SQL queries and database optimization |

### Infrastructure & Operations

#### DevOps & Deployment

| Agent | Model | Description |
|-------|-------|-------------|
| [devops-troubleshooter](agents/devops-troubleshooter.md) | sonnet | Production debugging, log analysis, deployment troubleshooting |
| [deployment-engineer](agents/deployment-engineer.md) | sonnet | CI/CD pipelines, containerization, cloud deployments |
| [terraform-specialist](agents/terraform-specialist.md) | sonnet | Infrastructure as Code with Terraform modules and state management |
| [dx-optimizer](agents/dx-optimizer.md) | sonnet | Developer experience optimization and tooling improvements |

#### Database Management

| Agent | Model | Description |
|-------|-------|-------------|
| [database-optimizer](agents/database-optimizer.md) | sonnet | Query optimization, index design, migration strategies |
| [database-admin](agents/database-admin.md) | sonnet | Database operations, backup, replication, monitoring |
| [database-architect](agents/database-architect.md) | opus | Database design from scratch, technology selection, schema modeling |

#### Incident Response & Network

| Agent | Model | Description |
|-------|-------|-------------|
| [incident-responder](agents/incident-responder.md) | opus | Production incident management and resolution |
| [network-engineer](agents/network-engineer.md) | sonnet | Network debugging, load balancing, traffic analysis |

### Quality Assurance & Security

#### Code Quality & Review

| Agent | Model | Description |
|-------|-------|-------------|
| [code-reviewer](agents/code-reviewer.md) | opus | Code review with security focus and production reliability |
| [security-auditor](agents/security-auditor.md) | opus | Vulnerability assessment and OWASP compliance |
| [backend-security-coder](agents/backend-security-coder.md) | opus | Secure backend coding practices, API security implementation |
| [frontend-security-coder](agents/frontend-security-coder.md) | opus | XSS prevention, CSP implementation, client-side security |
| [mobile-security-coder](agents/mobile-security-coder.md) | opus | Mobile security patterns, WebView security, biometric auth |

#### Testing & Debugging

| Agent | Model | Description |
|-------|-------|-------------|
| [test-automator](agents/test-automator.md) | sonnet | Comprehensive test suite creation (unit, integration, e2e) |
| [tdd-orchestrator](agents/tdd-orchestrator.md) | sonnet | Test-Driven Development methodology guidance |
| [debugger](agents/debugger.md) | sonnet | Error resolution and test failure analysis |
| [error-detective](agents/error-detective.md) | sonnet | Log analysis and error pattern recognition |

#### Performance & Observability

| Agent | Model | Description |
|-------|-------|-------------|
| [performance-engineer](agents/performance-engineer.md) | opus | Application profiling and optimization |
| [observability-engineer](agents/observability-engineer.md) | opus | Production monitoring, distributed tracing, SLI/SLO management |
| [search-specialist](agents/search-specialist.md) | haiku | Advanced web research and information synthesis |

### Data & AI

#### Data Engineering & Analytics

| Agent | Model | Description |
|-------|-------|-------------|
| [data-scientist](agents/data-scientist.md) | opus | Data analysis, SQL queries, BigQuery operations |
| [data-engineer](agents/data-engineer.md) | sonnet | ETL pipelines, data warehouses, streaming architectures |

#### Machine Learning & AI

| Agent | Model | Description |
|-------|-------|-------------|
| [ai-engineer](agents/ai-engineer.md) | opus | LLM applications, RAG systems, prompt pipelines |
| [ml-engineer](agents/ml-engineer.md) | opus | ML pipelines, model serving, feature engineering |
| [mlops-engineer](agents/mlops-engineer.md) | opus | ML infrastructure, experiment tracking, model registries |
| [prompt-engineer](agents/prompt-engineer.md) | opus | LLM prompt optimization and engineering |

### Documentation & Technical Writing

| Agent | Model | Description |
|-------|-------|-------------|
| [docs-architect](agents/docs-architect.md) | opus | Comprehensive technical documentation generation |
| [api-documenter](agents/api-documenter.md) | sonnet | OpenAPI/Swagger specifications and developer docs |
| [reference-builder](agents/reference-builder.md) | haiku | Technical references and API documentation |
| [tutorial-engineer](agents/tutorial-engineer.md) | sonnet | Step-by-step tutorials and educational content |
| [mermaid-expert](agents/mermaid-expert.md) | sonnet | Diagram creation (flowcharts, sequences, ERDs) |

### Business & Operations

#### Business Analysis & Finance

| Agent | Model | Description |
|-------|-------|-------------|
| [business-analyst](agents/business-analyst.md) | sonnet | Metrics analysis, reporting, KPI tracking |
| [quant-analyst](agents/quant-analyst.md) | opus | Financial modeling, trading strategies, market analysis |
| [risk-manager](agents/risk-manager.md) | sonnet | Portfolio risk monitoring and management |

#### Marketing & Sales

| Agent | Model | Description |
|-------|-------|-------------|
| [content-marketer](agents/content-marketer.md) | sonnet | Blog posts, social media, email campaigns |
| [sales-automator](agents/sales-automator.md) | haiku | Cold emails, follow-ups, proposal generation |

#### Support & Legal

| Agent | Model | Description |
|-------|-------|-------------|
| [customer-support](agents/customer-support.md) | sonnet | Support tickets, FAQ responses, customer communication |
| [hr-pro](agents/hr-pro.md) | opus | HR operations, policies, employee relations |
| [legal-advisor](agents/legal-advisor.md) | opus | Privacy policies, terms of service, legal documentation |

### SEO & Content Optimization

| Agent | Model | Description |
|-------|-------|-------------|
| [seo-content-auditor](agents/seo-content-auditor.md) | sonnet | Content quality analysis, E-E-A-T signals assessment |
| [seo-meta-optimizer](agents/seo-meta-optimizer.md) | haiku | Meta title and description optimization |
| [seo-keyword-strategist](agents/seo-keyword-strategist.md) | haiku | Keyword analysis and semantic variations |
| [seo-structure-architect](agents/seo-structure-architect.md) | haiku | Content structure and schema markup |
| [seo-snippet-hunter](agents/seo-snippet-hunter.md) | haiku | Featured snippet formatting |
| [seo-content-refresher](agents/seo-content-refresher.md) | haiku | Content freshness analysis |
| [seo-cannibalization-detector](agents/seo-cannibalization-detector.md) | haiku | Keyword overlap detection |
| [seo-authority-builder](agents/seo-authority-builder.md) | sonnet | E-E-A-T signal analysis |
| [seo-content-writer](agents/seo-content-writer.md) | sonnet | SEO-optimized content creation |
| [seo-content-planner](agents/seo-content-planner.md) | haiku | Content planning and topic clusters |

### Specialized Domains

| Agent | Model | Description |
|-------|-------|-------------|
| [blockchain-developer](agents/blockchain-developer.md) | sonnet | Web3 apps, smart contracts, DeFi protocols |
| [payment-integration](agents/payment-integration.md) | sonnet | Payment processor integration (Stripe, PayPal) |
| [legacy-modernizer](agents/legacy-modernizer.md) | sonnet | Legacy code refactoring and modernization |
| [context-manager](agents/context-manager.md) | haiku | Multi-agent context management |

## Model Configuration

Agents are assigned to specific Claude models based on task complexity and computational requirements. The system uses three model tiers:

### Model Distribution Summary

| Model | Agent Count | Use Case |
|-------|-------------|----------|
| Haiku | 11 | Quick, focused tasks with minimal computational overhead |
| Sonnet | 50 | Standard development and specialized engineering tasks |
| Opus | 23 | Complex reasoning, architecture, and critical analysis |

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
| Infrastructure | 10 | `devops-troubleshooter`, `deployment-engineer`, `terraform-specialist`, `dx-optimizer`, `database-admin`, `database-optimizer`, `network-engineer`, `flutter-expert`, `api-documenter`, `tutorial-engineer` |
| Quality & Testing | 4 | `test-automator`, `tdd-orchestrator`, `debugger`, `error-detective` |
| Business & Support | 6 | `business-analyst`, `risk-manager`, `content-marketer`, `customer-support`, `mermaid-expert`, `legacy-modernizer` |
| Data & Content | 5 | `data-engineer`, `payment-integration`, `seo-content-auditor`, `seo-authority-builder`, `seo-content-writer` |

### Opus Model Agents

| Category | Count | Agents |
|----------|-------|--------|
| Architecture & Design | 5 | `backend-architect`, `cloud-architect`, `hybrid-cloud-architect`, `kubernetes-architect`, `database-architect` |
| Security & Code Review | 5 | `code-reviewer`, `security-auditor`, `backend-security-coder`, `frontend-security-coder`, `mobile-security-coder` |
| Performance & Observability | 3 | `performance-engineer`, `observability-engineer`, `incident-responder` |
| AI/ML Complex | 5 | `ai-engineer`, `ml-engineer`, `mlops-engineer`, `data-scientist`, `prompt-engineer` |
| Business Critical | 5 | `docs-architect`, `hr-pro`, `legal-advisor`, `quant-analyst`, `risk-manager` |

## Architecture & Design Principles

### Version 1.0.5 Refactoring

This marketplace has been extensively refactored following industry best practices from VSCode, npm, and Chrome extension ecosystems:

#### Single Responsibility Principle
- Each plugin does **one thing well** (Unix philosophy)
- Clear, focused purposes (describable in 5-7 words)
- Average plugin size: **6.2 components** (down from 8-10)
- **Zero bloated plugins** (all under 12 components)

#### Focused Plugin Architecture
- **27 plugins → 36 plugins** (+33% more focused)
- Extracted common functionality: `data-validation-suite`, `deployment-orchestration`
- Split bloated plugins into specialized ones:
  - `infrastructure-devops` (22) → `kubernetes-operations`, `docker-containerization`, `deployment-orchestration`
  - `security-hardening` (18) → `security-scanning`, `security-compliance`, `backend-api-security`, `frontend-mobile-security`
  - `data-ml-pipeline` (17) → `data-engineering`, `machine-learning-ops`, `ai-agent-development`
  - `api-development-kit` (17) → `api-scaffolding`, `api-testing-observability`, `data-validation-suite`
  - `incident-response` (16) → `incident-diagnostics`, `observability-monitoring`

#### Aggressive File Optimization
- **24,392 lines eliminated** (58% reduction in problematic files)
- **10 high-priority files optimized** (62% average reduction)
- **8 legacy monolithic files archived** (14,698 lines)
- Removed redundant examples, consolidated code blocks, streamlined documentation
- All tools remain **fully functional** with zero breaking changes

#### Performance Improvements
- **2-3x faster loading times** (average file size reduced by 58%)
- **Better context window utilization** (tools avg 626 lines vs 954 lines)
- **Improved LLM response quality** (smaller, more focused tools)
- **Lower token costs** (less content to process)

#### Quality Metrics
- ✅ **223 component references validated** (0 broken)
- ✅ **12.6% tool duplication** (minimal and intentional)
- ✅ **100% naming compliance** (kebab-case standard)
- ✅ **90.5% component coverage** (high utilization)

### Design Philosophy

**Composability Over Bundling**
- Mix and match plugins based on needs
- Workflow orchestrators compose focused plugins
- No forced feature bundling

**Context Efficiency**
- Smaller tools = faster processing
- Better fit in LLM context windows
- More accurate, focused responses

**Maintainability**
- Single-purpose = easier updates
- Clear boundaries = isolated changes
- Less duplication = simpler maintenance

**Discoverability**
- Clear plugin names convey purpose
- Logical categorization
- Easy to find the right tool


## Contributing

To add new agents, workflows, or tools:

1. Create a new `.md` file in the appropriate directory with frontmatter
2. Use lowercase, hyphen-separated naming convention
3. Write clear activation criteria in the description
4. Define comprehensive system prompt with expertise areas

### Subagent Format

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

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
