# Claude Code Plugins: Orchestration and Automation

> **⚡ Updated for Opus 4.5, Sonnet 4.5 & Haiku 4.5** — Three-tier model strategy for optimal performance

[![Run in Smithery](https://smithery.ai/badge/skills/wshobson)](https://smithery.ai/skills?ns=wshobson&utm_source=github&utm_medium=badge)

> **🎯 Agent Skills Enabled** — 129 specialized skills extend Claude's capabilities across plugins with progressive disclosure

A comprehensive production-ready system combining **108 specialized AI agents**, **15 multi-agent workflow orchestrators**, **129 agent skills**, and **72 development tools** organized into **72 focused, single-purpose plugins** for [Claude Code](https://docs.claude.com/en/docs/claude-code/overview).

## Overview

This unified repository provides everything needed for intelligent automation and multi-agent orchestration across modern software development:

- **72 Focused Plugins** - Granular, single-purpose plugins optimized for minimal token usage and composability
- **108 Specialized Agents** - Domain experts with deep knowledge across architecture, languages, infrastructure, quality, data/AI, documentation, business operations, and SEO
- **129 Agent Skills** - Modular knowledge packages with progressive disclosure for specialized expertise
- **15 Workflow Orchestrators** - Multi-agent coordination systems for complex operations like full-stack development, security hardening, ML pipelines, and incident response
- **72 Development Tools** - Optimized utilities including project scaffolding, security scanning, test automation, and infrastructure setup

### Key Features

- **Granular Plugin Architecture**: 72 focused plugins optimized for minimal token usage
- **Comprehensive Tooling**: 72 development tools including test generation, scaffolding, and security scanning
- **100% Agent Coverage**: All plugins include specialized agents
- **Agent Skills**: 129 specialized skills following for progressive disclosure and token efficiency
- **Clear Organization**: 23 categories with 1-6 plugins each for easy discovery
- **Efficient Design**: Average 3.4 components per plugin (follows Anthropic's 2-8 pattern)

### How It Works

Each plugin is completely isolated with its own agents, commands, and skills:

- **Install only what you need** - Each plugin loads only its specific agents, commands, and skills
- **Minimal token usage** - No unnecessary resources loaded into context
- **Mix and match** - Compose multiple plugins for complex workflows
- **Clear boundaries** - Each plugin has a single, focused purpose
- **Progressive disclosure** - Skills load knowledge only when activated

**Example**: Installing `python-development` loads 3 Python agents, 1 scaffolding tool, and makes 16 skills available (~1000 tokens), not the entire marketplace.

## Quick Start

### Step 1: Add the Marketplace

Add this marketplace to Claude Code:

```bash
/plugin marketplace add wshobson/agents
```

This makes all 72 plugins available for installation, but **does not load any agents or tools** into your context.

### Step 2: Install Plugins

Browse available plugins:

```bash
/plugin
```

Install the plugins you need:

```bash
# Essential development plugins
/plugin install python-development          # Python with 16 specialized skills
/plugin install javascript-typescript       # JS/TS with 4 specialized skills
/plugin install backend-development         # Backend APIs with 3 architecture skills

# Infrastructure & operations
/plugin install kubernetes-operations       # K8s with 4 deployment skills
/plugin install cloud-infrastructure        # AWS/Azure/GCP with 4 cloud skills

# Security & quality
/plugin install security-scanning           # SAST with security skill
/plugin install code-review-ai             # AI-powered code review

# Full-stack orchestration
/plugin install full-stack-orchestration   # Multi-agent workflows
```

Each installed plugin loads **only its specific agents, commands, and skills** into Claude's context.

### Plugins vs Agents

You install **plugins**, which bundle agents:

| Plugin                  | Agents                                            |
| ----------------------- | ------------------------------------------------- |
| `comprehensive-review`  | architect-review, code-reviewer, security-auditor |
| `javascript-typescript` | javascript-pro, typescript-pro                    |
| `python-development`    | python-pro, django-pro, fastapi-pro               |
| `blockchain-web3`       | blockchain-developer                              |

```bash
# ❌ Wrong - can't install agents directly
/plugin install typescript-pro

# ✅ Right - install the plugin
/plugin install javascript-typescript@claude-code-workflows
```

### Troubleshooting

**"Plugin not found"** → Use plugin names, not agent names. Add `@claude-code-workflows` suffix.

**Plugins not loading** → Clear cache and reinstall:

```bash
rm -rf ~/.claude/plugins/cache/claude-code-workflows && rm ~/.claude/plugins/installed_plugins.json
```

## Documentation

### Core Guides

- **[Plugin Reference](docs/plugins.md)** - Complete catalog of all 72 plugins
- **[Agent Reference](docs/agents.md)** - All 108 agents organized by category
- **[Agent Skills](docs/agent-skills.md)** - 129 specialized skills with progressive disclosure
- **[Usage Guide](docs/usage.md)** - Commands, workflows, and best practices
- **[Architecture](docs/architecture.md)** - Design principles and patterns

### Quick Links

- [Installation](#quick-start) - Get started in 2 steps
- [Essential Plugins](docs/plugins.md#quick-start---essential-plugins) - Top plugins for immediate productivity
- [Command Reference](docs/usage.md#command-reference-by-category) - All slash commands organized by category
- [Multi-Agent Workflows](docs/usage.md#multi-agent-workflow-examples) - Pre-configured orchestration examples
- [Model Configuration](docs/agents.md#model-configuration) - Haiku/Sonnet hybrid orchestration

## What's New

### Agent Skills (140 skills across 20 plugins)

Specialized knowledge packages following Anthropic's progressive disclosure architecture:

**Language Development:**

- **Python** (5 skills): async patterns, testing, packaging, performance, UV package manager
- **JavaScript/TypeScript** (4 skills): advanced types, Node.js patterns, testing, modern ES6+

**Infrastructure & DevOps:**

- **Kubernetes** (4 skills): manifests, Helm charts, GitOps, security policies
- **Cloud Infrastructure** (4 skills): Terraform, multi-cloud, hybrid networking, cost optimization
- **CI/CD** (4 skills): pipeline design, GitHub Actions, GitLab CI, secrets management

**Development & Architecture:**

- **Backend** (3 skills): API design, architecture patterns, microservices
- **LLM Applications** (8 skills): LangGraph, prompt engineering, RAG, evaluation, embeddings, similarity search, vector tuning, hybrid search

**Blockchain & Web3** (4 skills): DeFi protocols, NFT standards, Solidity security, Web3 testing

**Project Management:**

- **Conductor** (3 skills): context-driven development, track management, workflow patterns

**And more:** Framework migration, observability, payment processing, ML operations, security scanning

[→ View complete skills documentation](docs/agent-skills.md)

### Three-Tier Model Strategy

Strategic model assignment for optimal performance and cost:

| Tier       | Model    | Agents | Use Case                                                                                        |
| ---------- | -------- | ------ | ----------------------------------------------------------------------------------------------- |
| **Tier 1** | Opus 4.5 | 42     | Critical architecture, security, ALL code review, production coding (language pros, frameworks) |
| **Tier 2** | Inherit  | 42     | Complex tasks - user chooses model (AI/ML, backend, frontend/mobile, specialized)               |
| **Tier 3** | Sonnet   | 51     | Support with intelligence (docs, testing, debugging, network, API docs, DX, legacy, payments)   |
| **Tier 4** | Haiku    | 18     | Fast operational tasks (SEO, deployment, simple docs, sales, content, search)                   |

**Why Opus 4.5 for Critical Agents?**

- 80.9% on SWE-bench (industry-leading)
- 65% fewer tokens for complex tasks
- Best for architecture decisions and security audits

**Tier 2 Flexibility (`inherit`):**
Agents marked `inherit` use your session's default model, letting you balance cost and capability:

- Set via `claude --model opus` or `claude --model sonnet` when starting a session
- Falls back to Sonnet 4.5 if no default specified
- Perfect for frontend/mobile developers who want cost control
- AI/ML engineers can choose Opus for complex model work

**Cost Considerations:**

- **Opus 4.5**: $5/$25 per million input/output tokens - Premium for critical work
- **Sonnet 4.5**: $3/$15 per million tokens - Balanced performance/cost
- **Haiku 4.5**: $1/$5 per million tokens - Fast, cost-effective operations
- Opus's 65% token reduction on complex tasks often offsets higher rate
- Use `inherit` tier to control costs for high-volume use cases

Orchestration patterns combine models for efficiency:

```
Opus (architecture) → Sonnet (development) → Haiku (deployment)
```

[→ View model configuration details](docs/agents.md#model-configuration)

## Popular Use Cases

### Full-Stack Feature Development

```bash
/full-stack-orchestration:full-stack-feature "user authentication with OAuth2"
```

Coordinates 7+ agents: backend-architect → database-architect → frontend-developer → test-automator → security-auditor → deployment-engineer → observability-engineer

[→ View all workflow examples](docs/usage.md#multi-agent-workflow-examples)

### Security Hardening

```bash
/security-scanning:security-hardening --level comprehensive
```

Multi-agent security assessment with SAST, dependency scanning, and code review.

### Python Development with Modern Tools

```bash
/python-development:python-scaffold fastapi-microservice
```

Creates production-ready FastAPI project with async patterns, activating skills:

- `async-python-patterns` - AsyncIO and concurrency
- `python-testing-patterns` - pytest and fixtures
- `uv-package-manager` - Fast dependency management

### Kubernetes Deployment

```bash
# Activates k8s skills automatically
"Create production Kubernetes deployment with Helm chart and GitOps"
```

Uses kubernetes-architect agent with 4 specialized skills for production-grade configs.

[→ View complete usage guide](docs/usage.md)

## Plugin Categories

**23 categories, 72 plugins:**

- 🎨 **Development** (4) - debugging, backend, frontend, multi-platform
- 📚 **Documentation** (3) - code docs, API specs, diagrams, C4 architecture
- 🔄 **Workflows** (4) - git, full-stack, TDD, **Conductor** (context-driven development)
- ✅ **Testing** (2) - unit testing, TDD workflows
- 🔍 **Quality** (3) - code review, comprehensive review, performance
- 🤖 **AI & ML** (4) - LLM apps, agent orchestration, context, MLOps
- 📊 **Data** (2) - data engineering, data validation
- 🗄️ **Database** (2) - database design, migrations
- 🚨 **Operations** (4) - incident response, diagnostics, distributed debugging, observability
- ⚡ **Performance** (2) - application performance, database/cloud optimization
- ☁️ **Infrastructure** (5) - deployment, validation, Kubernetes, cloud, CI/CD
- 🔒 **Security** (4) - scanning, compliance, backend/API, frontend/mobile
- 💻 **Languages** (7) - Python, JS/TS, systems, JVM, scripting, functional, embedded
- 🔗 **Blockchain** (1) - smart contracts, DeFi, Web3
- 💰 **Finance** (1) - quantitative trading, risk management
- 💳 **Payments** (1) - Stripe, PayPal, billing
- 🎮 **Gaming** (1) - Unity, Minecraft plugins
- 📢 **Marketing** (4) - SEO content, technical SEO, SEO analysis, content marketing
- 💼 **Business** (3) - analytics, HR/legal, customer/sales
- And more...

[→ View complete plugin catalog](docs/plugins.md)

## Architecture Highlights

### Granular Design

- **Single responsibility** - Each plugin does one thing well
- **Minimal token usage** - Average 3.4 components per plugin
- **Composable** - Mix and match for complex workflows
- **100% coverage** - All 108 agents accessible across plugins

### Progressive Disclosure (Skills)

Three-tier architecture for token efficiency:

1. **Metadata** - Name and activation criteria (always loaded)
2. **Instructions** - Core guidance (loaded when activated)
3. **Resources** - Examples and templates (loaded on demand)

### Repository Structure

```
claude-agents/
├── .claude-plugin/
│   └── marketplace.json          # 72 plugins
├── plugins/
│   ├── python-development/
│   │   ├── agents/               # 3 Python experts
│   │   ├── commands/             # Scaffolding tool
│   │   └── skills/               # 5 specialized skills
│   ├── kubernetes-operations/
│   │   ├── agents/               # K8s architect
│   │   ├── commands/             # Deployment tools
│   │   └── skills/               # 4 K8s skills
│   └── ... (65 more plugins)
├── docs/                          # Comprehensive documentation
└── README.md                      # This file
```

[→ View architecture details](docs/architecture.md)

## Contributing

To add new agents, skills, or commands:

1. Identify or create the appropriate plugin directory in `plugins/`
2. Create `.md` files in the appropriate subdirectory:
   - `agents/` - For specialized agents
   - `commands/` - For tools and workflows
   - `skills/` - For modular knowledge packages
3. Follow naming conventions (lowercase, hyphen-separated)
4. Write clear activation criteria and comprehensive content
5. Update the plugin definition in `.claude-plugin/marketplace.json`

See [Architecture Documentation](docs/architecture.md) for detailed guidelines.

## Resources

### Documentation

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Plugins Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Subagents Guide](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Agent Skills Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Slash Commands Reference](https://docs.claude.com/en/docs/claude-code/slash-commands)

### This Repository

- [Plugin Reference](docs/plugins.md)
- [Agent Reference](docs/agents.md)
- [Agent Skills Guide](docs/agent-skills.md)
- [Usage Guide](docs/usage.md)
- [Architecture](docs/architecture.md)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=wshobson/agents&type=date&legend=top-left)](https://www.star-history.com/#wshobson/agents&type=date&legend=top-left)
