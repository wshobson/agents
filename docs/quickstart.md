# Solar System Agents - Quick Start Guide

Get up and running with Solar System Agents in 5 minutes.

## What You'll Learn

- How to install the Solar System
- How to use planet orchestrators
- How to run multi-planet workflows
- Common usage patterns

## Prerequisites

- Claude Code installed
- Basic understanding of Claude Code plugins

## Step 1: Add the Solar System Repository (30 seconds)

```bash
/plugin marketplace add HermeticOrmus/solar-system-agents
```

This adds the Solar System marketplace to Claude Code.

## Step 2: Install Solar Core (1 minute)

```bash
/plugin install solar-core
```

This installs:
- ☀️ Sun orchestrator (solar-orchestrator)
- 8 planet orchestrators (mercury, venus, earth, mars, jupiter, saturn, uranus, neptune)

You now have the coordination layer!

## Step 3: Install Your First Planets (2 minutes)

Choose based on your work:

### For Full-Stack Developers
```bash
/plugin install full-stack-orchestration
/plugin install backend-development
/plugin install frontend-mobile-development
/plugin install git-pr-workflows
```

You now have: Earth (full-stack), Mars (backend), Venus (frontend)

### For DevOps Engineers
```bash
/plugin install cloud-infrastructure
/plugin install kubernetes-operations
/plugin install cicd-automation
/plugin install observability-monitoring
```

You now have: Jupiter (infrastructure), Neptune (operations)

### For Data Scientists
```bash
/plugin install machine-learning-ops
/plugin install llm-application-dev
/plugin install database-design
/plugin install cloud-infrastructure
```

You now have: Saturn (data/AI), Jupiter (infrastructure)

### For Security Engineers
```bash
/plugin install security-scanning
/plugin install security-compliance
/plugin install backend-api-security
/plugin install observability-monitoring
```

You now have: Uranus (security), Neptune (monitoring)

## Step 4: Use the Solar System (2 minutes)

### Option A: Let the Sun Route (Recommended)

Just describe your task naturally:

```
"Build a FastAPI microservice with OAuth2 authentication, deploy it to Kubernetes, and set up monitoring"
```

The Sun orchestrator will automatically:
1. Route to **Mars** (backend-architect, fastapi-pro)
2. Route to **Uranus** (security-auditor, backend-security-coder)
3. Route to **Jupiter** (kubernetes-architect, deployment-engineer)
4. Route to **Neptune** (observability-engineer)

### Option B: Invoke Planets Directly

For direct planet access:

```
@mars-orchestrator Design a GraphQL API for an e-commerce platform

@jupiter-orchestrator Deploy microservices to AWS EKS with Terraform

@saturn-orchestrator Build an ML training pipeline with MLflow

@venus-orchestrator Create a responsive React dashboard

@neptune-orchestrator Set up Prometheus and Grafana for K8s monitoring
```

### Option C: Invoke Specific Agents

For granular control:

```
"@backend-architect Design a RESTful API for user management"

"@kubernetes-architect Create Helm charts for my microservices"

"@security-auditor Run a comprehensive security audit"
```

## Common Workflows

### Full-Stack Feature Development

```
"Implement user authentication with email/password and OAuth2 Google login,
including frontend UI, backend API, database schema, tests, and deployment"
```

The Sun routes to:
1. 🌍 **Earth** (tdd-orchestrator) - Set up TDD workflow
2. ♄ **Saturn** (database-architect) - User schema design
3. ♂ **Mars** (backend-architect) - Authentication API
4. ♀ **Venus** (frontend-developer) - Login UI
5. ♅ **Uranus** (security-auditor) - Security review
6. 🌍 **Earth** (test-automator) - Integration tests
7. ♃ **Jupiter** (deployment-engineer) - Deploy
8. ♆ **Neptune** (observability-engineer) - Monitoring

### Quick Debugging

```
"Debug why my bash script is failing with 'command not found'"
```

The Sun routes to:
- ☿ **Mercury** (debugger + shellcheck) - Fast debugging

### Security Audit

```
"Run a comprehensive security audit and fix all vulnerabilities"
```

The Sun routes to:
1. ♅ **Uranus** (security-auditor) - SAST, dependency scan, OWASP Top 10
2. ♂ **Mars** (backend-security-coder) - Fix backend issues
3. ♀ **Venus** (frontend-security-coder) - Fix frontend issues
4. ♃ **Jupiter** (terraform-specialist) - Harden infrastructure
5. ♆ **Neptune** (observability-engineer) - Security monitoring

### ML Pipeline

```
"Build an end-to-end ML pipeline for customer churn prediction,
including data ingestion, feature engineering, model training,
deployment, and monitoring"
```

The Sun routes to:
1. ♄ **Saturn** (mlops-engineer) - Pipeline architecture
2. ♄ **Saturn** (data-engineer) - ETL pipeline
3. ♄ **Saturn** (data-scientist) - Model training
4. ♃ **Jupiter** (cloud-architect) - ML infrastructure
5. ♃ **Jupiter** (kubernetes-architect) - Deploy on K8s
6. ♆ **Neptune** (observability-engineer) - Model monitoring
7. ♂ **Mars** (backend-architect) - Prediction API

## Understanding the Planets

### ☿ Mercury - Speed & CLI
**Use when:** Shell scripts, quick debugging, CLI tools
**Speed:** Fastest (Haiku model)
**Example:** "Write a bash script to backup logs daily"

### ♀ Venus - Frontend & Beauty
**Use when:** UI development, mobile apps, design, accessibility
**Speed:** Fast (Sonnet for complex UI)
**Example:** "Create a responsive React dashboard with charts"

### 🌍 Earth - Full-Stack Hub
**Use when:** Full-stack features, TDD, code review, Git workflows
**Speed:** Balanced (Hybrid model)
**Example:** "Implement user profiles with TDD"

### ♂ Mars - Backend & APIs
**Use when:** REST/GraphQL APIs, backend logic, microservices
**Speed:** Thoughtful (Sonnet for architecture)
**Example:** "Design a microservices architecture for e-commerce"

### ♃ Jupiter - Infrastructure & Cloud
**Use when:** AWS/Azure/GCP, Kubernetes, Terraform, CI/CD
**Speed:** Complex (Hybrid model)
**Example:** "Deploy to Kubernetes with Helm and ArgoCD"

### ♄ Saturn - Data, AI & ML
**Use when:** ML pipelines, LLM apps, databases, data engineering
**Speed:** Deep analysis (Sonnet)
**Example:** "Build a RAG system for documentation"

### ♅ Uranus - Security & Compliance
**Use when:** Security audits, compliance, vulnerability scanning
**Speed:** Thorough (Sonnet)
**Example:** "Validate SOC2 compliance and fix gaps"

### ♆ Neptune - Operations & Monitoring
**Use when:** Observability, incidents, performance, SRE
**Speed:** Fast response + deep analysis (Hybrid)
**Example:** "Set up observability with Prometheus and Grafana"

## Tips & Best Practices

### 1. Start with the Sun
Let the Sun orchestrator route your tasks - it knows the best planet(s) for the job.

### 2. Install Planets as Needed
Don't install all 65 plugins at once. Start with the planets you need:
- Full-stack dev → Earth, Mars, Venus
- DevOps → Jupiter, Neptune
- Data/ML → Saturn, Jupiter
- Security → Uranus, Neptune

### 3. Use Progressive Disclosure
Planets will load skills on-demand when needed. You don't need to manage this manually.

### 4. Invoke Planets for Domain Work
Use planet orchestrators for domain-specific work:
- `@mars-orchestrator` for backend-only projects
- `@jupiter-orchestrator` for infrastructure-only projects

### 5. Understand Hierarchical Complexity
- Inner planets (Mercury, Venus, Earth) → Fast, simple tasks
- Outer planets (Saturn, Uranus, Neptune) → Complex, deep analysis
- Mars, Jupiter → Balanced complexity

### 6. Use Multi-Planet Workflows
For complex features, expect multiple planets to collaborate:
```
Full-stack feature = Earth + Mars + Venus + Uranus + Jupiter + Neptune
```

### 7. Check Planet Specialties
Each planet has specific agents and skills:
- Mars has `backend-architect` (most popular agent)
- Earth has `code-reviewer` (most used agent)
- Jupiter has 12 skills (most in the system)
- Saturn has 12 agents (tied for most)

## Troubleshooting

### "Plugin not found"
Make sure you added the marketplace:
```bash
/plugin marketplace add HermeticOrmus/solar-system-agents
```

### "Agent not loaded"
Install the planet that contains the agent:
```bash
# Example: backend-architect is on Mars
/plugin install backend-development
```

### "Too many tokens"
Install only the planets you need. Each planet loads only its plugins and agents.

### "Which planet should I use?"
Ask the Sun! Just describe your task naturally and let it route:
```
"I need to [describe your task]"
```

## Next Steps

### Learn More
- **[Solar System Architecture](solar-system-architecture.md)** - Deep dive into the architecture
- **[Planet Mapping](solar-system-mapping.md)** - See which agents are on which planets
- **[Usage Guide](usage.md)** - Advanced usage patterns

### Install More Planets
Browse available plugins:
```bash
/plugin
```

Filter by planet category or keywords.

### Explore Skills
Many planets have specialized skills that activate automatically:
- **Jupiter:** 12 skills (Terraform, K8s, CI/CD, etc.)
- **Saturn:** 6 skills (ML, LLM, RAG, etc.)
- **Python Development:** 5 skills (async, testing, packaging, etc.)

### Join the Community
- [GitHub Discussions](https://github.com/HermeticOrmus/solar-system-agents/discussions)
- [Issue Tracker](https://github.com/HermeticOrmus/solar-system-agents/issues)

## Quick Reference

### Installation Commands
```bash
# Add marketplace
/plugin marketplace add HermeticOrmus/solar-system-agents

# Install solar core
/plugin install solar-core

# Install planets
/plugin install [plugin-name]
```

### Invocation Patterns
```bash
# Let Sun route
"[natural language task description]"

# Invoke planet
@[planet]-orchestrator [task]

# Invoke agent
@[agent-name] [task]
```

### Planet Keywords

Use these keywords to trigger specific planets:

- **Mercury:** bash, shell, CLI, script, debug quickly
- **Venus:** frontend, UI, mobile, React, design, accessibility
- **Earth:** full-stack, feature, TDD, test, PR, code review
- **Mars:** API, backend, REST, GraphQL, microservice
- **Jupiter:** cloud, kubernetes, deploy, terraform, CI/CD
- **Saturn:** ML, AI, LLM, data, database, analytics
- **Uranus:** security, vulnerability, compliance, audit
- **Neptune:** monitoring, incident, performance, observability

## Congratulations! 🎉

You're now ready to use Solar System Agents! Every task finds its orbit. ☀️🪐

---

**Quick Links:**
- [Architecture Guide](solar-system-architecture.md)
- [Planet Mapping](solar-system-mapping.md)
- [Full README](../README.md)
- [GitHub Repository](https://github.com/HermeticOrmus/solar-system-agents)
