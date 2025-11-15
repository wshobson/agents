# Solar System Agents

> **☀️ An intelligent multi-agent architecture inspired by the solar system** — 65+ specialized plugins organized into 8 planetary domains with gravitational routing and orbital coordination.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/wshobson/agents)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agents](https://img.shields.io/badge/agents-100+-green.svg)](docs/agents.md)
[![Plugins](https://img.shields.io/badge/plugins-65+-orange.svg)](docs/plugins.md)

## What is Solar System Agents?

**Solar System Agents** is a revolutionary multi-agent orchestration architecture for [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) that organizes 100+ specialized AI agents into 8 planetary domains, each coordinated by a planet orchestrator. A central Sun orchestrator intelligently routes tasks based on domain expertise, complexity, and gravitational relationships between planets.

Think of it as **the solar system, but for AI agents** — where each planet specializes in a domain (Frontend, Backend, Infrastructure, etc.), and the Sun coordinates everything.

## 🌟 Why Solar System Architecture?

### The Problem with Traditional Multi-Agent Systems
- **Unclear routing:** Users must know which agent to invoke
- **No coordination:** Agents work independently
- **Inefficient:** Duplicate work across similar agents
- **Complex workflows:** Manual multi-agent orchestration

### The Solar System Solution
- **☀️ Intelligent Routing:** Sun analyzes tasks and routes to appropriate planets
- **🪐 Domain Organization:** 8 planets, each with clear specialty areas
- **🌙 Hierarchical Complexity:** Inner planets = fast/simple, Outer planets = complex/deep
- **🌍 Orbital Coordination:** Planets collaborate in defined workflow patterns
- **⚡ Performance Optimized:** Strategic model assignment (Haiku for speed, Sonnet for complexity)

## The Solar System

```
                           ☀️ SUN
                    (Solar Orchestrator)
                  Intelligent Task Routing
                            |
        ┌───────────────────┼───────────────────┐
        ↓                   ↓                   ↓
    ☿ MERCURY           ♀ VENUS            🌍 EARTH
  Speed & CLI       Frontend & UX      Full-Stack Hub
   (Haiku)            (Sonnet)            (Hybrid)

        ↓                   ↓                   ↓
    ♂ MARS              ♃ JUPITER          ♄ SATURN
  Backend & APIs    Infrastructure      Data, AI & ML
   (Sonnet)            (Hybrid)            (Sonnet)

        ↓                   ↓
    ♅ URANUS            ♆ NEPTUNE
   Security          Operations
   (Sonnet)            (Hybrid)

    ☄️ ASTEROID BELT              🌌 KUIPER BELT
   Documentation              Specialized Domains
   Code Quality            (Languages, Business, etc.)
```

## Quick Start

### 1. Add the Solar System Repository
```bash
/plugin marketplace add HermeticOrmus/solar-system-agents
```

### 2. Install Solar Core
```bash
/plugin install solar-core
```

This installs the Sun orchestrator and all 8 planet coordinators.

### 3. Install Planets (Choose Your Domain)

**☿ Mercury (Speed & CLI):**
```bash
/plugin install shell-scripting
/plugin install debugging-toolkit
```

**♀ Venus (Frontend & Mobile):**
```bash
/plugin install frontend-mobile-development
/plugin install multi-platform-apps
```

**🌍 Earth (Full-Stack Integration):**
```bash
/plugin install full-stack-orchestration
/plugin install tdd-workflows
/plugin install git-pr-workflows
```

**♂ Mars (Backend & APIs):**
```bash
/plugin install backend-development
/plugin install api-scaffolding
```

**♃ Jupiter (Infrastructure & Cloud):**
```bash
/plugin install cloud-infrastructure
/plugin install kubernetes-operations
/plugin install cicd-automation
```

**♄ Saturn (Data, AI & ML):**
```bash
/plugin install machine-learning-ops
/plugin install llm-application-dev
/plugin install database-design
```

**♅ Uranus (Security & Compliance):**
```bash
/plugin install security-scanning
/plugin install security-compliance
```

**♆ Neptune (Operations & Monitoring):**
```bash
/plugin install observability-monitoring
/plugin install incident-response
```

### 4. Use the Solar System

Let the Sun orchestrator route your tasks:
```
"Build a FastAPI service with OAuth2, deploy to Kubernetes, and set up monitoring"
```

The Sun will coordinate:
1. **Mars** - FastAPI backend development
2. **Uranus** - OAuth2 security implementation
3. **Jupiter** - Kubernetes deployment
4. **Neptune** - Observability and monitoring

Or invoke planets directly:
```
@mars-orchestrator Design a GraphQL API for e-commerce
@jupiter-orchestrator Deploy microservices to AWS EKS
@saturn-orchestrator Build an ML training pipeline
```

## The 8 Planets

### ☿ Mercury - Speed & CLI
**Distance:** 1 (fastest orbit)
**Model:** Haiku (speed optimized)
**Specialty:** Shell scripting, CLI tools, quick debugging

**Agents:** bash-pro, posix-shell-pro, debugger, error-detective
**Use For:** Fast scripts, CLI automation, quick debugging

### ♀ Venus - Frontend & Beauty
**Distance:** 2
**Model:** Sonnet (complex UI reasoning)
**Specialty:** Frontend development, mobile apps, UI/UX, accessibility

**Agents:** frontend-developer, mobile-developer, flutter-expert, ios-developer, ui-ux-designer
**Use For:** React/Vue/Angular apps, mobile apps, UI design, accessibility

### 🌍 Earth - Full-Stack Hub
**Distance:** 3 (balanced)
**Model:** Hybrid (Sonnet → Haiku → Sonnet)
**Specialty:** Full-stack integration, TDD, testing, Git workflows

**Agents:** tdd-orchestrator, test-automator, code-reviewer⭐, deployment-engineer
**Moons:** 🌙 Luna (Testing), 🌙 Selene (Git/PR)
**Use For:** Full-stack features, TDD, code review, PR workflows

### ♂ Mars - Backend & APIs
**Distance:** 4
**Model:** Sonnet (architecture decisions)
**Specialty:** Backend APIs, server architecture, microservices

**Agents:** backend-architect⭐ (most popular!), graphql-architect, fastapi-pro, django-pro
**Moons:** 🌙 Deimos (REST), 🌙 Phobos (GraphQL)
**Use For:** REST/GraphQL APIs, backend logic, microservices

### ♃ Jupiter - Infrastructure & Cloud
**Distance:** 5 (largest planet)
**Model:** Hybrid (planning + execution)
**Specialty:** Cloud infrastructure, Kubernetes, CI/CD, deployment

**Agents:** cloud-architect, kubernetes-architect, terraform-specialist, deployment-engineer
**Moons:** 🌙 Europa (K8s), 🌙 Ganymede (Cloud), 🌙 Callisto (CI/CD), 🌙 Io (Terraform)
**Skills:** 12 specialized skills (most in solar system)
**Use For:** AWS/Azure/GCP, Kubernetes, Terraform, CI/CD pipelines

### ♄ Saturn - Data, AI & ML
**Distance:** 6
**Model:** Sonnet (complex data patterns)
**Specialty:** Machine learning, data engineering, LLM applications, databases

**Agents:** ml-engineer, mlops-engineer, data-engineer, ai-engineer, prompt-engineer, database-architect
**Moons:** 🌙 Titan (LLMs), 🌙 Rhea (ML), 🌙 Iapetus (Databases), 🌙 Dione (Analytics)
**Use For:** ML pipelines, LLM apps, RAG systems, databases, data engineering

### ♅ Uranus - Security & Compliance
**Distance:** 7
**Model:** Sonnet (careful security analysis)
**Specialty:** Security scanning, compliance validation, vulnerability detection

**Agents:** security-auditor, backend-security-coder, frontend-security-coder
**Moons:** 🌙 Miranda (SAST), 🌙 Ariel (Compliance), 🌙 Umbriel (Secrets)
**Use For:** Security audits, SOC2/HIPAA/GDPR compliance, OWASP Top 10

### ♆ Neptune - Operations & Monitoring
**Distance:** 8 (furthest, deepest insights)
**Model:** Hybrid (fast response + deep analysis)
**Specialty:** Observability, incident response, performance optimization

**Agents:** observability-engineer, incident-responder, performance-engineer
**Moons:** 🌙 Triton (Observability), 🌙 Proteus (Incidents)
**Use For:** Production monitoring, incidents, performance optimization, SRE

⭐ = Most used agents across the solar system

## Multi-Planet Workflows

The power of Solar System Agents is **coordinated multi-planet workflows:**

### Example: Full-Stack Feature Development
```
☀️ Sun routes to:
  1. 🌍 Earth (tdd-orchestrator) - Set up TDD workflow
  2. ♄ Saturn (database-architect) - Design schema
  3. ♂ Mars (backend-architect) - Design & build API
  4. ♀ Venus (frontend-developer) - Build UI
  5. ♅ Uranus (security-auditor) - Security review
  6. 🌍 Earth (test-automator) - Integration tests
  7. ♃ Jupiter (deployment-engineer) - Deploy
  8. ♆ Neptune (observability-engineer) - Set up monitoring
  9. 🌍 Earth (code-reviewer) - Final review
```

### Example: Security Hardening
```
☀️ Sun routes to:
  1. ♅ Uranus (security-auditor) - Full security scan
  2. ♂ Mars (backend-security-coder) - Fix backend vulnerabilities
  3. ♀ Venus (frontend-security-coder) - Fix frontend issues
  4. ♃ Jupiter (terraform-specialist) - Harden infrastructure
  5. ♆ Neptune (observability-engineer) - Security monitoring
```

### Example: ML Pipeline
```
☀️ Sun routes to:
  1. ♄ Saturn (mlops-engineer) - Design ML pipeline
  2. ♄ Saturn (data-engineer) - Build ETL
  3. ♄ Saturn (data-scientist) - Train model
  4. ♃ Jupiter (cloud-architect) - ML infrastructure
  5. ♃ Jupiter (kubernetes-architect) - Deploy on K8s
  6. ♆ Neptune (observability-engineer) - Model monitoring
```

## Key Features

### ☀️ Gravitational Routing
The Sun orchestrator analyzes tasks and automatically routes to the right planet(s) based on:
- **Domain keywords** (API → Mars, Frontend → Venus, ML → Saturn)
- **Complexity** (Simple → Inner planets, Complex → Outer planets)
- **Multi-domain needs** (Coordinates multiple planets)

### 🪐 Hierarchical Complexity
Inner planets = fast/simple, Outer planets = complex/deep:
1. Mercury (Distance 1) - Fastest execution
2. Venus (Distance 2) - Fast UI work
3. Earth (Distance 3) - Balanced integration
4. Mars (Distance 4) - Thoughtful architecture
5. Jupiter (Distance 5) - Complex infrastructure
6. Saturn (Distance 6) - Deep data/AI analysis
7. Uranus (Distance 7) - Thorough security
8. Neptune (Distance 8) - Deepest operational insights

### ⚡ Performance Optimization
Strategic model assignment for speed and cost:
- **Haiku:** Mercury (fastest tasks)
- **Sonnet:** Venus, Mars, Saturn, Uranus (complex reasoning)
- **Hybrid:** Earth, Jupiter, Neptune (planning + execution)

### 🌙 Moons (Specialized Sub-Domains)
Planets have moons for focused specializations:
- Earth: Luna (Testing), Selene (Git/PR)
- Mars: Deimos (REST), Phobos (GraphQL)
- Jupiter: Europa (K8s), Ganymede (Cloud), Callisto (CI/CD), Io (Terraform)
- Saturn: Titan (LLMs), Rhea (ML), Iapetus (DB), Dione (Analytics)

### 📚 Progressive Disclosure
Load only what you need:
- Install only the planets relevant to your work
- Planets load only their plugins
- Skills load on-demand when activated
- Minimal token usage per task

## What's Included

- **☀️ 1 Sun:** Central orchestrator
- **🪐 8 Planets:** Domain coordinators
- **🌙 13+ Moons:** Specialized sub-domains
- **🔧 65 Plugins:** Specialized capabilities
- **🤖 100+ Agents:** Expert agents
- **📚 47 Skills:** Progressive disclosure knowledge
- **☄️ Asteroid Belt:** Documentation & code quality
- **🌌 Kuiper Belt:** Specialized domains (languages, business, etc.)

## Documentation

### Core Guides
- **[Solar System Architecture](docs/solar-system-architecture.md)** - Complete architecture guide
- **[Planet Mapping](docs/solar-system-mapping.md)** - Plugin-to-planet mapping
- **[Quick Start Guide](docs/quickstart.md)** - Get started in 5 minutes
- **[Usage Guide](docs/usage.md)** - Commands and workflows

### Reference
- **[Plugin Catalog](docs/plugins.md)** - All 65 plugins
- **[Agent Reference](docs/agents.md)** - All 100+ agents
- **[Skills Guide](docs/agent-skills.md)** - 47 specialized skills

## Comparison: Traditional vs Solar System

### Traditional Multi-Agent (v1.x)
❌ User must know which agent to use
❌ No central coordination
❌ Manual multi-agent workflows
❌ Unclear relationships between agents
❌ Potential conflicts and duplication

### Solar System Architecture (v2.0)
✅ Sun orchestrator routes automatically
✅ Coordinated multi-planet workflows
✅ Clear domain boundaries
✅ Gravitational relationships
✅ Optimized token usage
✅ Intuitive mental model
✅ Hierarchical complexity

## Use Cases

### 🚀 Startup Development
Install Earth + Mars + Jupiter for full-stack development with deployment

### 🏢 Enterprise Applications
Install all planets for comprehensive development, security, and operations

### 🔬 Data Science & ML
Install Saturn + Jupiter + Neptune for ML pipelines, deployment, and monitoring

### 🛡️ Security-First Development
Install Uranus + Earth for security-focused development with code review

### 📱 Mobile App Development
Install Venus + Mars + Jupiter for mobile frontend, backend APIs, and cloud deployment

### 🔧 DevOps & SRE
Install Jupiter + Neptune + Mercury for infrastructure, monitoring, and automation

## Architecture Principles

1. **Single Responsibility:** Each planet has a clear domain
2. **Gravitational Routing:** Natural, intuitive task routing
3. **Orbital Coordination:** Defined multi-planet workflow patterns
4. **Energy Efficiency:** Optimized token usage
5. **Progressive Disclosure:** Load only what you need
6. **Hybrid Execution:** Strategic model assignment
7. **Clear Boundaries:** No overlap between planets
8. **Scalability:** Easy to extend with new agents

## Contributing

We welcome contributions! To add new agents or plugins:

1. Identify the appropriate planet for your contribution
2. Create agents following planet-specific patterns
3. Update planet orchestrator if needed
4. Submit a pull request

See [Contributing Guide](CONTRIBUTING.md) for details.

## Version History

### v2.0.0 - Solar System Architecture (2025-11-15)
- 🌟 **NEW:** Solar System architecture with 8 planets
- ☀️ **NEW:** Sun orchestrator for intelligent routing
- 🪐 **NEW:** Planet orchestrators for domain coordination
- 🌙 **NEW:** Moons for specialized sub-domains
- ⚡ **NEW:** Hybrid model execution strategy
- 📚 **IMPROVED:** Comprehensive documentation
- 🔄 **BREAKING:** Marketplace restructured around planets

### v1.2.x - Plugin Architecture
- 65 focused plugins
- 100+ specialized agents
- 47 agent skills

## License

MIT License - see [LICENSE](LICENSE) file for details.

Copyright (c) 2025 HermeticOrmus

## Resources

### Solar System Agents
- [GitHub Repository](https://github.com/HermeticOrmus/solar-system-agents)
- [Architecture Guide](docs/solar-system-architecture.md)
- [Issue Tracker](https://github.com/HermeticOrmus/solar-system-agents/issues)

### Claude Code
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Plugins Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Subagents Guide](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Agent Skills Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

## Acknowledgments

Inspired by the elegant mechanics of our solar system, where gravitational relationships create stable, hierarchical organization. Special thanks to the Claude Code team at Anthropic for creating an extensible agent platform.

---

**☀️ Welcome to the Solar System. Every task finds its orbit. 🪐**

[![Star History Chart](https://api.star-history.com/svg?repos=HermeticOrmus/solar-system-agents&type=Date)](https://star-history.com/#HermeticOrmus/solar-system-agents&Date)
