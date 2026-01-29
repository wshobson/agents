# Usage Guide

Complete guide to using agents, slash commands, and multi-agent workflows.

## Overview

The plugin ecosystem provides two primary interfaces:

1. **Slash Commands** - Direct invocation of tools and workflows
2. **Natural Language** - Claude reasons about which agents to use

## Slash Commands

Slash commands are the primary interface for working with agents and workflows. Each plugin provides namespaced commands that you can run directly.

### Command Format

```bash
/plugin-name:command-name [arguments]
```

### Discovering Commands

List all available slash commands from installed plugins:

```bash
/plugin
```

### Benefits of Slash Commands

- **Direct invocation** - No need to describe what you want in natural language
- **Structured arguments** - Pass parameters explicitly for precise control
- **Composability** - Chain commands together for complex workflows
- **Discoverability** - Use `/plugin` to see all available commands

## Natural Language

Agents can also be invoked through natural language when you need Claude to reason about which specialist to use:

```
"Use backend-architect to design the authentication API"
"Have security-auditor scan for OWASP vulnerabilities"
"Get performance-engineer to optimize this database query"
```

Claude Code automatically selects and coordinates the appropriate agents based on your request.

## Command Reference by Category

### Development & Features

| Command                                        | Description                                 |
| ---------------------------------------------- | ------------------------------------------- |
| `/backend-development:feature-development`     | End-to-end backend feature development      |
| `/full-stack-orchestration:full-stack-feature` | Complete full-stack feature implementation  |
| `/multi-platform-apps:multi-platform`          | Cross-platform app development coordination |

### Testing & Quality

| Command                       | Description                           |
| ----------------------------- | ------------------------------------- |
| `/unit-testing:test-generate` | Generate comprehensive unit tests     |
| `/tdd-workflows:tdd-cycle`    | Complete TDD red-green-refactor cycle |
| `/tdd-workflows:tdd-red`      | Write failing tests first             |
| `/tdd-workflows:tdd-green`    | Implement code to pass tests          |
| `/tdd-workflows:tdd-refactor` | Refactor with passing tests           |

### Code Quality & Review

| Command                             | Description                |
| ----------------------------------- | -------------------------- |
| `/code-review-ai:ai-review`         | AI-powered code review     |
| `/comprehensive-review:full-review` | Multi-perspective analysis |
| `/comprehensive-review:pr-enhance`  | Enhance pull requests      |

### Debugging & Troubleshooting

| Command                                | Description                    |
| -------------------------------------- | ------------------------------ |
| `/debugging-toolkit:smart-debug`       | Interactive smart debugging    |
| `/incident-response:incident-response` | Production incident management |
| `/incident-response:smart-fix`         | Automated incident resolution  |
| `/error-debugging:error-analysis`      | Deep error analysis            |
| `/error-debugging:error-trace`         | Stack trace debugging          |
| `/error-diagnostics:smart-debug`       | Smart diagnostic debugging     |
| `/distributed-debugging:debug-trace`   | Distributed system tracing     |

### Security

| Command                                    | Description                         |
| ------------------------------------------ | ----------------------------------- |
| `/security-scanning:security-hardening`    | Comprehensive security hardening    |
| `/security-scanning:security-sast`         | Static application security testing |
| `/security-scanning:security-dependencies` | Dependency vulnerability scanning   |
| `/security-compliance:compliance-check`    | SOC2/HIPAA/GDPR compliance          |
| `/frontend-mobile-security:xss-scan`       | XSS vulnerability scanning          |

### Infrastructure & Deployment

| Command                                   | Description                     |
| ----------------------------------------- | ------------------------------- |
| `/observability-monitoring:monitor-setup` | Setup monitoring infrastructure |
| `/observability-monitoring:slo-implement` | Implement SLO/SLI metrics       |
| `/deployment-validation:config-validate`  | Pre-deployment validation       |
| `/cicd-automation:workflow-automate`      | CI/CD pipeline automation       |

### Data & ML

| Command                                 | Description                        |
| --------------------------------------- | ---------------------------------- |
| `/machine-learning-ops:ml-pipeline`     | ML training pipeline orchestration |
| `/data-engineering:data-pipeline`       | ETL/ELT pipeline construction      |
| `/data-engineering:data-driven-feature` | Data-driven feature development    |

### Documentation

| Command                                  | Description                                                                                |
| ---------------------------------------- | ------------------------------------------------------------------------------------------ |
| `/code-documentation:doc-generate`       | Generate comprehensive documentation                                                       |
| `/code-documentation:code-explain`       | Explain code functionality                                                                 |
| `/documentation-generation:doc-generate` | OpenAPI specs, diagrams, tutorials                                                         |
| `/c4-architecture:c4-architecture`       | Generate comprehensive C4 architecture documentation (Context, Container, Component, Code) |

### Refactoring & Maintenance

| Command                                 | Description                  |
| --------------------------------------- | ---------------------------- |
| `/code-refactoring:refactor-clean`      | Code cleanup and refactoring |
| `/code-refactoring:tech-debt`           | Technical debt management    |
| `/codebase-cleanup:deps-audit`          | Dependency auditing          |
| `/codebase-cleanup:tech-debt`           | Technical debt reduction     |
| `/framework-migration:legacy-modernize` | Legacy code modernization    |
| `/framework-migration:code-migrate`     | Framework migration          |
| `/framework-migration:deps-upgrade`     | Dependency upgrades          |

### Database

| Command                                        | Description                     |
| ---------------------------------------------- | ------------------------------- |
| `/database-migrations:sql-migrations`          | SQL migration automation        |
| `/database-migrations:migration-observability` | Migration monitoring            |
| `/database-cloud-optimization:cost-optimize`   | Database and cloud optimization |

### Git & PR Workflows

| Command                          | Description                  |
| -------------------------------- | ---------------------------- |
| `/git-pr-workflows:pr-enhance`   | Enhance pull request quality |
| `/git-pr-workflows:onboard`      | Team onboarding automation   |
| `/git-pr-workflows:git-workflow` | Git workflow automation      |

### Project Scaffolding

| Command                                      | Description                  |
| -------------------------------------------- | ---------------------------- |
| `/python-development:python-scaffold`        | FastAPI/Django project setup |
| `/javascript-typescript:typescript-scaffold` | Next.js/React + Vite setup   |
| `/systems-programming:rust-project`          | Rust project scaffolding     |

### AI & LLM Development

| Command                                     | Description                     |
| ------------------------------------------- | ------------------------------- |
| `/llm-application-dev:langchain-agent`      | LangChain agent development     |
| `/llm-application-dev:ai-assistant`         | AI assistant implementation     |
| `/llm-application-dev:prompt-optimize`      | Prompt engineering optimization |
| `/agent-orchestration:multi-agent-optimize` | Multi-agent optimization        |
| `/agent-orchestration:improve-agent`        | Agent improvement workflows     |

### Testing & Performance

| Command                                             | Description          |
| --------------------------------------------------- | -------------------- |
| `/performance-testing-review:ai-review`             | Performance analysis |
| `/application-performance:performance-optimization` | App optimization     |

### Team Collaboration

| Command                             | Description                 |
| ----------------------------------- | --------------------------- |
| `/team-collaboration:issue`         | Issue management automation |
| `/team-collaboration:standup-notes` | Standup notes generation    |

### Accessibility

| Command                                         | Description              |
| ----------------------------------------------- | ------------------------ |
| `/accessibility-compliance:accessibility-audit` | WCAG compliance auditing |

### API Development

| Command                               | Description             |
| ------------------------------------- | ----------------------- |
| `/api-testing-observability:api-mock` | API mocking and testing |

### Context Management

| Command                               | Description               |
| ------------------------------------- | ------------------------- |
| `/context-management:context-save`    | Save conversation context |
| `/context-management:context-restore` | Restore previous context  |

## Multi-Agent Workflow Examples

Plugins provide pre-configured multi-agent workflows accessible via slash commands.

### Full-Stack Development

```bash
# Command-based workflow invocation
/full-stack-orchestration:full-stack-feature "user dashboard with real-time analytics"

# Natural language alternative
"Implement user dashboard with real-time analytics"
```

**Orchestration:** backend-architect → database-architect → frontend-developer → test-automator → security-auditor → deployment-engineer → observability-engineer

**What happens:**

1. Database schema design with migrations
2. Backend API implementation (REST/GraphQL)
3. Frontend components with state management
4. Comprehensive test suite (unit/integration/E2E)
5. Security audit and hardening
6. CI/CD pipeline setup with feature flags
7. Observability and monitoring configuration

### Security Hardening

```bash
# Comprehensive security assessment and remediation
/security-scanning:security-hardening --level comprehensive

# Natural language alternative
"Perform security audit and implement OWASP best practices"
```

**Orchestration:** security-auditor → backend-security-coder → frontend-security-coder → mobile-security-coder → test-automator

### Data/ML Pipeline

```bash
# ML feature development with production deployment
/machine-learning-ops:ml-pipeline "customer churn prediction model"

# Natural language alternative
"Build customer churn prediction model with deployment"
```

**Orchestration:** data-scientist → data-engineer → ml-engineer → mlops-engineer → performance-engineer

### Incident Response

```bash
# Smart debugging with root cause analysis
/incident-response:smart-fix "production memory leak in payment service"

# Natural language alternative
"Debug production memory leak and create runbook"
```

**Orchestration:** incident-responder → devops-troubleshooter → debugger → error-detective → observability-engineer

### C4 Architecture Documentation

```bash
# Generate comprehensive C4 architecture documentation
/c4-architecture:c4-architecture

# Natural language alternative
"Create C4 architecture documentation for this codebase"
```

**Orchestration:** c4-code → c4-component → c4-container → c4-context

**What happens:**

1. **Code Level**: Bottom-up analysis of all subdirectories, creating code-level documentation with function signatures and dependencies
2. **Component Level**: Synthesizes code documentation into logical components with interfaces and relationships
3. **Container Level**: Maps components to deployment containers with OpenAPI/Swagger API specifications
4. **Context Level**: Creates high-level system context with personas, user journeys, and external dependencies

**Output:** Complete C4 documentation in `C4-Documentation/` directory with Mermaid diagrams at all levels (Context, Container, Component, Code)

## Command Arguments and Options

Many slash commands support arguments for precise control:

```bash
# Test generation for specific files
/unit-testing:test-generate src/api/users.py

# Feature development with methodology specification
/backend-development:feature-development OAuth2 integration with social login

# Security dependency scanning
/security-scanning:security-dependencies

# Component scaffolding
/frontend-mobile-development:component-scaffold UserProfile component with hooks

# TDD workflow cycle
/tdd-workflows:tdd-red User can reset password
/tdd-workflows:tdd-green
/tdd-workflows:tdd-refactor

# Smart debugging
/debugging-toolkit:smart-debug memory leak in checkout flow

# Python project scaffolding
/python-development:python-scaffold fastapi-microservice

# C4 architecture documentation generation
/c4-architecture:c4-architecture
```

## Combining Natural Language and Commands

You can mix both approaches for optimal flexibility:

```
# Start with a command for structured workflow
/full-stack-orchestration:full-stack-feature "payment processing"

# Then provide natural language guidance
"Ensure PCI-DSS compliance and integrate with Stripe"
"Add retry logic for failed transactions"
"Set up fraud detection rules"
```

## Best Practices

### When to Use Slash Commands

- **Structured workflows** - Multi-step processes with clear phases
- **Repetitive tasks** - Operations you perform frequently
- **Precise control** - When you need specific parameters
- **Discovery** - Exploring available functionality

### When to Use Natural Language

- **Exploratory work** - When you're not sure which tool to use
- **Complex reasoning** - When Claude needs to coordinate multiple agents
- **Contextual decisions** - When the right approach depends on the situation
- **Ad-hoc tasks** - One-off operations that don't fit a command

### Workflow Composition

Compose multiple plugins for complex scenarios:

```bash
# 1. Start with feature development
/backend-development:feature-development payment processing API

# 2. Add security hardening
/security-scanning:security-hardening

# 3. Generate comprehensive tests
/unit-testing:test-generate

# 4. Review the implementation
/code-review-ai:ai-review

# 5. Set up CI/CD
/cicd-automation:workflow-automate

# 6. Add monitoring
/observability-monitoring:monitor-setup
```

## Agent Skills Integration

Agent Skills work alongside commands to provide deep expertise:

```
User: "Set up FastAPI project with async patterns"
→ Activates: fastapi-templates skill
→ Invokes: /python-development:python-scaffold
→ Result: Production-ready FastAPI project with best practices

User: "Implement Kubernetes deployment with Helm"
→ Activates: helm-chart-scaffolding, k8s-manifest-generator skills
→ Guides: kubernetes-architect agent
→ Result: Production-grade K8s manifests with Helm charts
```

See [Agent Skills](./agent-skills.md) for details on the 107 specialized skills.

## See Also

- [Agent Skills](./agent-skills.md) - Specialized knowledge packages
- [Agent Reference](./agents.md) - Complete agent catalog
- [Plugin Reference](./plugins.md) - All 67 plugins
- [Architecture](./architecture.md) - Design principles
