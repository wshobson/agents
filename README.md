# Claude Code Plugins: Orchestration and Automation

> **⚡ Updated for Sonnet 4.5 & Haiku 4.5** — All agents optimized for latest models with hybrid orchestration

A comprehensive production-ready system combining **87 specialized AI agents**, **15 multi-agent workflow orchestrators**, and **44 development tools** organized into **64 focused, single-purpose plugins** for [Claude Code](https://docs.claude.com/en/docs/claude-code/overview).

## Overview

This unified repository provides everything needed for intelligent automation and multi-agent orchestration across modern software development:

- **64 Focused Plugins** - Granular, single-purpose plugins optimized for minimal token usage and composability
- **87 Specialized Agents** - Domain experts with deep knowledge across architecture, languages, infrastructure, quality, data/AI, documentation, business operations, and SEO
- **15 Workflow Orchestrators** - Multi-agent coordination systems for complex operations like full-stack development, security hardening, ML pipelines, and incident response
- **44 Development Tools** - Optimized utilities including project scaffolding, security scanning, test automation, and infrastructure setup

### Key Features

- **Granular Plugin Architecture**: 64 focused plugins optimized for minimal token usage
- **Comprehensive Tooling**: 44 development tools including test generation, scaffolding, and security scanning
- **100% Agent Coverage**: All plugins include specialized agents
- **Clear Organization**: 23 categories with 1-6 plugins each for easy discovery
- **Efficient Design**: Average 3.4 components per plugin (follows Anthropic's 2-8 pattern)

### How It Works

Each plugin is completely isolated with its own agents and commands:

- **Install only what you need** - Each plugin loads only its specific agents and tools
- **Minimal token usage** - No unnecessary resources loaded into context
- **Mix and match** - Compose multiple plugins for complex workflows
- **Clear boundaries** - Each plugin has a single, focused purpose

**Example**: Installing `python-development` loads only 3 Python agents and 1 scaffolding tool (~300 tokens), not the entire marketplace.

## Installation

### Step 1: Add the Marketplace

Add this marketplace to Claude Code:

```bash
/plugin marketplace add wshobson/agents
```

This makes all 64 plugins available for installation, but **does not load any agents or tools** into your context.

### Step 2: Install Specific Plugins

Browse available plugins:

```bash
/plugin
```

Install only the plugins you need:

```bash
/plugin install python-development
/plugin install backend-development
```

Each installed plugin loads **only its specific agents and commands** into Claude's context.

## Quick Start - Essential Plugins

> 💡 **Getting Started?** Install these popular plugins for immediate productivity gains.

### Development Essentials

**code-documentation** - Documentation and technical writing

```bash
/plugin install code-documentation
```

Automated doc generation, code explanation, and tutorial creation for comprehensive technical documentation.

**debugging-toolkit** - Smart debugging and developer experience

```bash
/plugin install debugging-toolkit
```

Interactive debugging, error analysis, and DX optimization for faster problem resolution.

**git-pr-workflows** - Git automation and PR enhancement

```bash
/plugin install git-pr-workflows
```

Git workflow automation, pull request enhancement, and team onboarding processes.

### Full-Stack Development

**backend-development** - Backend API design and architecture

```bash
/plugin install backend-development
```

RESTful and GraphQL API design with test-driven development and modern backend architecture patterns.

**frontend-mobile-development** - UI and mobile development

```bash
/plugin install frontend-mobile-development
```

React/React Native component development with automated scaffolding and cross-platform implementation.

**full-stack-orchestration** - End-to-end feature development

```bash
/plugin install full-stack-orchestration
```

Multi-agent coordination from backend → frontend → testing → security → deployment.

### Testing & Quality

**unit-testing** - Automated test generation

```bash
/plugin install unit-testing
```

Generate pytest (Python) and Jest (JavaScript) unit tests automatically with comprehensive edge case coverage.

**code-review-ai** - AI-powered code review

```bash
/plugin install code-review-ai
```

Architectural analysis, security assessment, and code quality review with actionable feedback.

### Infrastructure & Operations

**cloud-infrastructure** - Cloud architecture design

```bash
/plugin install cloud-infrastructure
```

AWS/Azure/GCP architecture, Kubernetes setup, Terraform IaC, and multi-cloud cost optimization.

**incident-response** - Production incident management

```bash
/plugin install incident-response
```

Rapid incident triage, root cause analysis, and automated resolution workflows for production systems.

### Language Support

**python-development** - Python project scaffolding

```bash
/plugin install python-development
```

FastAPI/Django project initialization with modern tooling (uv, ruff) and production-ready architecture.

**javascript-typescript** - JavaScript/TypeScript scaffolding

```bash
/plugin install javascript-typescript
```

Next.js, React + Vite, and Node.js project setup with pnpm and TypeScript best practices.

---

## Complete Plugin Reference

> 📋 **All 64 Plugins** - Browse by category to find specialized plugins for your workflow.

### 🎨 Development (4 plugins)

| Plugin                          | Description                                       | Install                                       |
| ------------------------------- | ------------------------------------------------- | --------------------------------------------- |
| **debugging-toolkit**           | Interactive debugging and DX optimization         | `/plugin install debugging-toolkit`           |
| **backend-development**         | Backend API design with GraphQL and TDD           | `/plugin install backend-development`         |
| **frontend-mobile-development** | Frontend UI and mobile development                | `/plugin install frontend-mobile-development` |
| **multi-platform-apps**         | Cross-platform app coordination (web/iOS/Android) | `/plugin install multi-platform-apps`         |

### 📚 Documentation (2 plugins)

| Plugin                       | Description                                   | Install                                    |
| ---------------------------- | --------------------------------------------- | ------------------------------------------ |
| **code-documentation**       | Documentation generation and code explanation | `/plugin install code-documentation`       |
| **documentation-generation** | OpenAPI specs, Mermaid diagrams, tutorials    | `/plugin install documentation-generation` |

### 🔄 Workflows (3 plugins)

| Plugin                       | Description                         | Install                                    |
| ---------------------------- | ----------------------------------- | ------------------------------------------ |
| **git-pr-workflows**         | Git automation and PR enhancement   | `/plugin install git-pr-workflows`         |
| **full-stack-orchestration** | End-to-end feature orchestration    | `/plugin install full-stack-orchestration` |
| **tdd-workflows**            | Test-driven development methodology | `/plugin install tdd-workflows`            |

### ✅ Testing (2 plugins)

| Plugin            | Description                                        | Install                         |
| ----------------- | -------------------------------------------------- | ------------------------------- |
| **unit-testing**  | Automated unit test generation (Python/JavaScript) | `/plugin install unit-testing`  |
| **tdd-workflows** | Test-driven development methodology                | `/plugin install tdd-workflows` |

### 🔍 Quality (3 plugins)

| Plugin                         | Description                                   | Install                                      |
| ------------------------------ | --------------------------------------------- | -------------------------------------------- |
| **code-review-ai**             | AI-powered architectural review               | `/plugin install code-review-ai`             |
| **comprehensive-review**       | Multi-perspective code analysis               | `/plugin install comprehensive-review`       |
| **performance-testing-review** | Performance analysis and test coverage review | `/plugin install performance-testing-review` |

### 🛠️ Utilities (4 plugins)

| Plugin                    | Description                                | Install                                 |
| ------------------------- | ------------------------------------------ | --------------------------------------- |
| **code-refactoring**      | Code cleanup and technical debt management | `/plugin install code-refactoring`      |
| **dependency-management** | Dependency auditing and version management | `/plugin install dependency-management` |
| **error-debugging**       | Error analysis and trace debugging         | `/plugin install error-debugging`       |
| **team-collaboration**    | Team workflows and standup automation      | `/plugin install team-collaboration`    |

### 🤖 AI & ML (4 plugins)

| Plugin                   | Description                         | Install                                |
| ------------------------ | ----------------------------------- | -------------------------------------- |
| **llm-application-dev**  | LLM apps and prompt engineering     | `/plugin install llm-application-dev`  |
| **agent-orchestration**  | Multi-agent system optimization     | `/plugin install agent-orchestration`  |
| **context-management**   | Context persistence and restoration | `/plugin install context-management`   |
| **machine-learning-ops** | ML training pipelines and MLOps     | `/plugin install machine-learning-ops` |

### 📊 Data (2 plugins)

| Plugin                    | Description                        | Install                                 |
| ------------------------- | ---------------------------------- | --------------------------------------- |
| **data-engineering**      | ETL pipelines and data warehouses  | `/plugin install data-engineering`      |
| **data-validation-suite** | Schema validation and data quality | `/plugin install data-validation-suite` |

### 🗄️ Database (2 plugins)

| Plugin                  | Description                             | Install                               |
| ----------------------- | --------------------------------------- | ------------------------------------- |
| **database-design**     | Database architecture and schema design | `/plugin install database-design`     |
| **database-migrations** | Database migration automation           | `/plugin install database-migrations` |

### 🚨 Operations (4 plugins)

| Plugin                       | Description                           | Install                                    |
| ---------------------------- | ------------------------------------- | ------------------------------------------ |
| **incident-response**        | Production incident management        | `/plugin install incident-response`        |
| **error-diagnostics**        | Error tracing and root cause analysis | `/plugin install error-diagnostics`        |
| **distributed-debugging**    | Distributed system tracing            | `/plugin install distributed-debugging`    |
| **observability-monitoring** | Metrics, logging, tracing, and SLO    | `/plugin install observability-monitoring` |

### ⚡ Performance (2 plugins)

| Plugin                          | Description                                | Install                                       |
| ------------------------------- | ------------------------------------------ | --------------------------------------------- |
| **application-performance**     | Application profiling and optimization     | `/plugin install application-performance`     |
| **database-cloud-optimization** | Database query and cloud cost optimization | `/plugin install database-cloud-optimization` |

### ☁️ Infrastructure (5 plugins)

| Plugin                    | Description                                 | Install                                 |
| ------------------------- | ------------------------------------------- | --------------------------------------- |
| **deployment-strategies** | Deployment patterns and rollback automation | `/plugin install deployment-strategies` |
| **deployment-validation** | Pre-deployment checks and validation        | `/plugin install deployment-validation` |
| **kubernetes-operations** | K8s manifests and GitOps workflows          | `/plugin install kubernetes-operations` |
| **cloud-infrastructure**  | AWS/Azure/GCP cloud architecture            | `/plugin install cloud-infrastructure`  |
| **cicd-automation**       | CI/CD pipeline configuration                | `/plugin install cicd-automation`       |

### 🔒 Security (4 plugins)

| Plugin                       | Description                              | Install                                    |
| ---------------------------- | ---------------------------------------- | ------------------------------------------ |
| **security-scanning**        | SAST analysis and vulnerability scanning | `/plugin install security-scanning`        |
| **security-compliance**      | SOC2/HIPAA/GDPR compliance               | `/plugin install security-compliance`      |
| **backend-api-security**     | API security and authentication          | `/plugin install backend-api-security`     |
| **frontend-mobile-security** | XSS/CSRF prevention and mobile security  | `/plugin install frontend-mobile-security` |

### 🔄 Modernization (2 plugins)

| Plugin                  | Description                               | Install                               |
| ----------------------- | ----------------------------------------- | ------------------------------------- |
| **framework-migration** | Framework upgrades and migration planning | `/plugin install framework-migration` |
| **codebase-cleanup**    | Technical debt reduction and cleanup      | `/plugin install codebase-cleanup`    |

### 🌐 API (2 plugins)

| Plugin                        | Description                 | Install                                     |
| ----------------------------- | --------------------------- | ------------------------------------------- |
| **api-scaffolding**           | REST/GraphQL API generation | `/plugin install api-scaffolding`           |
| **api-testing-observability** | API testing and monitoring  | `/plugin install api-testing-observability` |

### 📢 Marketing (4 plugins)

| Plugin                         | Description                             | Install                                      |
| ------------------------------ | --------------------------------------- | -------------------------------------------- |
| **seo-content-creation**       | SEO content writing and planning        | `/plugin install seo-content-creation`       |
| **seo-technical-optimization** | Meta tags, keywords, and schema markup  | `/plugin install seo-technical-optimization` |
| **seo-analysis-monitoring**    | Content analysis and authority building | `/plugin install seo-analysis-monitoring`    |
| **content-marketing**          | Content strategy and web research       | `/plugin install content-marketing`          |

### 💼 Business (3 plugins)

| Plugin                        | Description                          | Install                                     |
| ----------------------------- | ------------------------------------ | ------------------------------------------- |
| **business-analytics**        | KPI tracking and financial reporting | `/plugin install business-analytics`        |
| **hr-legal-compliance**       | HR policies and legal templates      | `/plugin install hr-legal-compliance`       |
| **customer-sales-automation** | Support and sales automation         | `/plugin install customer-sales-automation` |

### 💻 Languages (8 plugins)

| Plugin                     | Description                              | Install                                  |
| -------------------------- | ---------------------------------------- | ---------------------------------------- |
| **python-development**     | Python 3.12+ with Django/FastAPI         | `/plugin install python-development`     |
| **javascript-typescript**  | JavaScript/TypeScript with Node.js       | `/plugin install javascript-typescript`  |
| **systems-programming**    | Rust, Go, C, C++ for systems development | `/plugin install systems-programming`    |
| **jvm-languages**          | Java, Scala, C# with enterprise patterns | `/plugin install jvm-languages`          |
| **web-scripting**          | PHP and Ruby for web applications        | `/plugin install web-scripting`          |
| **functional-programming**        | Elixir with OTP and Phoenix              | `/plugin install functional-programming`        |
| **shell-scripting**        | Production Bash with defensive programming | `/plugin install shell-scripting`        |
| **arm-cortex-microcontrollers** | ARM Cortex-M firmware and drivers        | `/plugin install arm-cortex-microcontrollers` |

### 🔗 Blockchain (1 plugin)

| Plugin              | Description                        | Install                           |
| ------------------- | ---------------------------------- | --------------------------------- |
| **blockchain-web3** | Smart contracts and DeFi protocols | `/plugin install blockchain-web3` |

### 💰 Finance (1 plugin)

| Plugin                   | Description                             | Install                                |
| ------------------------ | --------------------------------------- | -------------------------------------- |
| **quantitative-trading** | Algorithmic trading and risk management | `/plugin install quantitative-trading` |

### 💳 Payments (1 plugin)

| Plugin                 | Description                           | Install                              |
| ---------------------- | ------------------------------------- | ------------------------------------ |
| **payment-processing** | Stripe/PayPal integration and billing | `/plugin install payment-processing` |

### 🎮 Gaming (1 plugin)

| Plugin               | Description                            | Install                            |
| -------------------- | -------------------------------------- | ---------------------------------- |
| **game-development** | Unity and Minecraft plugin development | `/plugin install game-development` |

### ♿ Accessibility (1 plugin)

| Plugin                       | Description                        | Install                                    |
| ---------------------------- | ---------------------------------- | ------------------------------------------ |
| **accessibility-compliance** | WCAG auditing and inclusive design | `/plugin install accessibility-compliance` |

## Repository Structure

```
claude-agents/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace catalog (64 plugins)
├── plugins/                       # Isolated plugin directories
│   ├── python-development/
│   │   ├── agents/               # Python language agents
│   │   │   ├── python-pro.md
│   │   │   ├── django-pro.md
│   │   │   └── fastapi-pro.md
│   │   └── commands/             # Python tooling
│   │       └── python-scaffold.md
│   ├── backend-development/
│   │   ├── agents/
│   │   │   ├── backend-architect.md
│   │   │   ├── graphql-architect.md
│   │   │   └── tdd-orchestrator.md
│   │   └── commands/
│   │       └── feature-development.md
│   ├── security-scanning/
│   │   ├── agents/
│   │   │   └── security-auditor.md
│   │   └── commands/
│   │       ├── security-hardening.md
│   │       ├── security-sast.md
│   │       └── security-dependencies.md
│   └── ... (59 more isolated plugins)
└── README.md                      # This file
```

Each plugin contains:

- **agents/** - Specialized agents for that domain
- **commands/** - Tools and workflows specific to that plugin

## Usage

### Using Plugin Slash Commands

After installing plugins, you can invoke their capabilities using **slash commands** - the primary interface for working with agents and workflows. Each plugin provides namespaced commands that you can run directly:

```bash
# List all available slash commands from installed plugins
/plugin

# Run a workflow command with arguments
/backend-development:feature-development user authentication with JWT

# Execute specialized tools
/unit-testing:test-generate src/auth/login.py

# Invoke security scans
/security-scanning:security-sast
```

**Key benefits of slash commands:**

- **Direct invocation** - No need to describe what you want in natural language
- **Structured arguments** - Pass parameters explicitly for precise control
- **Composability** - Chain commands together for complex workflows
- **Discoverability** - Use `/plugin` to see all available commands

### Agent Invocation

Agents can also be invoked through natural language when you need Claude to reason about which specialist to use:

```
"Use backend-architect to design the authentication API"
"Have security-auditor scan for OWASP vulnerabilities"
"Get performance-engineer to optimize this database query"
```

Claude Code automatically selects and coordinates the appropriate agents based on your request.

### Multi-Agent Workflow Examples

Plugins provide pre-configured multi-agent workflows accessible via slash commands:

#### Full-Stack Development

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

#### Security Hardening

```bash
# Comprehensive security assessment and remediation
/security-scanning:security-hardening --level comprehensive

# Natural language alternative
"Perform security audit and implement OWASP best practices"
```

**Orchestration:** security-auditor → backend-security-coder → frontend-security-coder → mobile-security-coder → test-automator

#### Data/ML Pipeline

```bash
# ML feature development with production deployment
/machine-learning-ops:ml-pipeline "customer churn prediction model"

# Natural language alternative
"Build customer churn prediction model with deployment"
```

**Orchestration:** data-scientist → data-engineer → ml-engineer → mlops-engineer → performance-engineer

#### Incident Response

```bash
# Smart debugging with root cause analysis
/incident-response:smart-fix "production memory leak in payment service"

# Natural language alternative
"Debug production memory leak and create runbook"
```

**Orchestration:** incident-responder → devops-troubleshooter → debugger → error-detective → observability-engineer

### Command Arguments and Options

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
```

### Combining Natural Language and Commands

You can mix both approaches for optimal flexibility:

```
# Start with a command for structured workflow
/full-stack-orchestration:full-stack-feature "payment processing"

# Then provide natural language guidance
"Ensure PCI-DSS compliance and integrate with Stripe"
"Add retry logic for failed transactions"
"Set up fraud detection rules"
```

### Discovering Commands

Use these commands to explore available functionality:

```bash
# List all installed plugins and their commands
/plugin

# Install a specific plugin
/plugin install python-development

# View available commands in a plugin
# After installation, commands will be listed with the format:
# /plugin-name:command-name
```

### Real Command Examples by Category

**Development & Features:**

- `/backend-development:feature-development` - End-to-end backend feature development
- `/full-stack-orchestration:full-stack-feature` - Complete full-stack feature implementation
- `/multi-platform-apps:multi-platform` - Cross-platform app development coordination

**Testing & Quality:**

- `/unit-testing:test-generate` - Generate comprehensive unit tests
- `/tdd-workflows:tdd-cycle` - Complete TDD red-green-refactor cycle
- `/tdd-workflows:tdd-red` - Write failing tests first
- `/tdd-workflows:tdd-green` - Implement code to pass tests
- `/tdd-workflows:tdd-refactor` - Refactor with passing tests

**Code Quality & Review:**

- `/code-review-ai:ai-review` - AI-powered code review
- `/comprehensive-review:full-review` - Multi-perspective analysis
- `/comprehensive-review:pr-enhance` - Enhance pull requests

**Debugging & Troubleshooting:**

- `/debugging-toolkit:smart-debug` - Interactive smart debugging
- `/incident-response:incident-response` - Production incident management
- `/incident-response:smart-fix` - Automated incident resolution
- `/error-debugging:error-analysis` - Deep error analysis
- `/error-debugging:error-trace` - Stack trace debugging
- `/error-diagnostics:smart-debug` - Smart diagnostic debugging
- `/distributed-debugging:debug-trace` - Distributed system tracing

**Security:**

- `/security-scanning:security-hardening` - Comprehensive security hardening
- `/security-scanning:security-sast` - Static application security testing
- `/security-scanning:security-dependencies` - Dependency vulnerability scanning
- `/security-compliance:compliance-check` - SOC2/HIPAA/GDPR compliance
- `/frontend-mobile-security:xss-scan` - XSS vulnerability scanning

**Infrastructure & Deployment:**

- `/observability-monitoring:monitor-setup` - Setup monitoring infrastructure
- `/observability-monitoring:slo-implement` - Implement SLO/SLI metrics
- `/deployment-validation:config-validate` - Pre-deployment validation
- `/cicd-automation:workflow-automate` - CI/CD pipeline automation

**Data & ML:**

- `/machine-learning-ops:ml-pipeline` - ML training pipeline orchestration
- `/data-engineering:data-pipeline` - ETL/ELT pipeline construction
- `/data-engineering:data-driven-feature` - Data-driven feature development

**Documentation:**

- `/code-documentation:doc-generate` - Generate comprehensive documentation
- `/code-documentation:code-explain` - Explain code functionality
- `/documentation-generation:doc-generate` - OpenAPI specs, diagrams, tutorials

**Refactoring & Maintenance:**

- `/code-refactoring:refactor-clean` - Code cleanup and refactoring
- `/code-refactoring:tech-debt` - Technical debt management
- `/codebase-cleanup:deps-audit` - Dependency auditing
- `/codebase-cleanup:tech-debt` - Technical debt reduction
- `/framework-migration:legacy-modernize` - Legacy code modernization
- `/framework-migration:code-migrate` - Framework migration
- `/framework-migration:deps-upgrade` - Dependency upgrades

**Database:**

- `/database-migrations:sql-migrations` - SQL migration automation
- `/database-migrations:migration-observability` - Migration monitoring
- `/database-cloud-optimization:cost-optimize` - Database and cloud optimization

**Git & PR Workflows:**

- `/git-pr-workflows:pr-enhance` - Enhance pull request quality
- `/git-pr-workflows:onboard` - Team onboarding automation
- `/git-pr-workflows:git-workflow` - Git workflow automation

**Project Scaffolding:**

- `/python-development:python-scaffold` - FastAPI/Django project setup
- `/javascript-typescript:typescript-scaffold` - Next.js/React + Vite setup
- `/systems-programming:rust-project` - Rust project scaffolding

**AI & LLM Development:**

- `/llm-application-dev:langchain-agent` - LangChain agent development
- `/llm-application-dev:ai-assistant` - AI assistant implementation
- `/llm-application-dev:prompt-optimize` - Prompt engineering optimization
- `/agent-orchestration:multi-agent-optimize` - Multi-agent optimization
- `/agent-orchestration:improve-agent` - Agent improvement workflows

**Testing & Performance:**

- `/performance-testing-review:ai-review` - Performance analysis
- `/application-performance:performance-optimization` - App optimization

**Team Collaboration:**

- `/team-collaboration:issue` - Issue management automation
- `/team-collaboration:standup-notes` - Standup notes generation

**Accessibility:**

- `/accessibility-compliance:accessibility-audit` - WCAG compliance auditing

**API Development:**

- `/api-testing-observability:api-mock` - API mocking and testing

**Context Management:**

- `/context-management:context-save` - Save conversation context
- `/context-management:context-restore` - Restore previous context

## Agent Categories

### Architecture & System Design

#### Core Architecture

| Agent                                                                                    | Model  | Description                                                        |
| ---------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------ |
| [backend-architect](plugins/backend-development/agents/backend-architect.md)             | opus   | RESTful API design, microservice boundaries, database schemas      |
| [frontend-developer](plugins/multi-platform-apps/agents/frontend-developer.md)           | sonnet | React components, responsive layouts, client-side state management |
| [graphql-architect](plugins/backend-development/agents/graphql-architect.md)             | opus   | GraphQL schemas, resolvers, federation architecture                |
| [architect-reviewer](plugins/comprehensive-review/agents/architect-review.md)            | opus   | Architectural consistency analysis and pattern validation          |
| [cloud-architect](plugins/cloud-infrastructure/agents/cloud-architect.md)                | opus   | AWS/Azure/GCP infrastructure design and cost optimization          |
| [hybrid-cloud-architect](plugins/cloud-infrastructure/agents/hybrid-cloud-architect.md)  | opus   | Multi-cloud strategies across cloud and on-premises environments   |
| [kubernetes-architect](plugins/kubernetes-operations/agents/kubernetes-architect.md)     | opus   | Cloud-native infrastructure with Kubernetes and GitOps             |

#### UI/UX & Mobile

| Agent                                                                            | Model  | Description                                        |
| -------------------------------------------------------------------------------- | ------ | -------------------------------------------------- |
| [ui-ux-designer](plugins/multi-platform-apps/agents/ui-ux-designer.md)          | sonnet | Interface design, wireframes, design systems       |
| [ui-visual-validator](plugins/accessibility-compliance/agents/ui-visual-validator.md) | sonnet | Visual regression testing and UI verification      |
| [mobile-developer](plugins/multi-platform-apps/agents/mobile-developer.md)      | sonnet | React Native and Flutter application development   |
| [ios-developer](plugins/multi-platform-apps/agents/ios-developer.md)            | sonnet | Native iOS development with Swift/SwiftUI          |
| [flutter-expert](plugins/multi-platform-apps/agents/flutter-expert.md)          | sonnet | Advanced Flutter development with state management |

### Programming Languages

#### Systems & Low-Level

| Agent                                                        | Model  | Description                                                 |
| ------------------------------------------------------------ | ------ | ----------------------------------------------------------- |
| [c-pro](plugins/systems-programming/agents/c-pro.md)         | sonnet | System programming with memory management and OS interfaces |
| [cpp-pro](plugins/systems-programming/agents/cpp-pro.md)     | sonnet | Modern C++ with RAII, smart pointers, STL algorithms        |
| [rust-pro](plugins/systems-programming/agents/rust-pro.md)   | sonnet | Memory-safe systems programming with ownership patterns     |
| [golang-pro](plugins/systems-programming/agents/golang-pro.md) | sonnet | Concurrent programming with goroutines and channels         |

#### Web & Application

| Agent                                                            | Model  | Description                                                |
| ---------------------------------------------------------------- | ------ | ---------------------------------------------------------- |
| [javascript-pro](plugins/javascript-typescript/agents/javascript-pro.md) | sonnet | Modern JavaScript with ES6+, async patterns, Node.js       |
| [typescript-pro](plugins/javascript-typescript/agents/typescript-pro.md) | sonnet | Advanced TypeScript with type systems and generics         |
| [python-pro](plugins/python-development/agents/python-pro.md)    | sonnet | Python development with advanced features and optimization |
| [ruby-pro](plugins/web-scripting/agents/ruby-pro.md)            | sonnet | Ruby with metaprogramming, Rails patterns, gem development |
| [php-pro](plugins/web-scripting/agents/php-pro.md)              | sonnet | Modern PHP with frameworks and performance optimization    |

#### Enterprise & JVM

| Agent                                                    | Model  | Description                                                          |
| -------------------------------------------------------- | ------ | -------------------------------------------------------------------- |
| [java-pro](plugins/jvm-languages/agents/java-pro.md)    | sonnet | Modern Java with streams, concurrency, JVM optimization              |
| [scala-pro](plugins/jvm-languages/agents/scala-pro.md)  | sonnet | Enterprise Scala with functional programming and distributed systems |
| [csharp-pro](plugins/jvm-languages/agents/csharp-pro.md) | sonnet | C# development with .NET frameworks and patterns                     |

#### Specialized Platforms

| Agent                                                                    | Model  | Description                                     |
| ------------------------------------------------------------------------ | ------ | ----------------------------------------------- |
| [elixir-pro](plugins/functional-programming/agents/elixir-pro.md)       | sonnet | Elixir with OTP patterns and Phoenix frameworks |
| [bash-pro](plugins/shell-scripting/agents/bash-pro.md)                  | sonnet | Defensive Bash scripting with POSIX compliance  |
| [posix-shell-pro](plugins/shell-scripting/agents/posix-shell-pro.md)    | sonnet | Strict POSIX sh for maximum portability         |
| [django-pro](plugins/api-scaffolding/agents/django-pro.md)              | sonnet | Django development with ORM and async views     |
| [fastapi-pro](plugins/api-scaffolding/agents/fastapi-pro.md)            | sonnet | FastAPI with async patterns and Pydantic        |
| [unity-developer](plugins/game-development/agents/unity-developer.md)   | sonnet | Unity game development and optimization         |
| [minecraft-bukkit-pro](plugins/game-development/agents/minecraft-bukkit-pro.md) | sonnet | Minecraft server plugin development             |
| [sql-pro](plugins/database-design/agents/sql-pro.md)                    | sonnet | Complex SQL queries and database optimization   |

### Infrastructure & Operations

#### DevOps & Deployment

| Agent                                                                        | Model  | Description                                                        |
| ---------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------ |
| [devops-troubleshooter](plugins/incident-response/agents/devops-troubleshooter.md) | sonnet | Production debugging, log analysis, deployment troubleshooting     |
| [deployment-engineer](plugins/cloud-infrastructure/agents/deployment-engineer.md)   | sonnet | CI/CD pipelines, containerization, cloud deployments               |
| [terraform-specialist](plugins/cloud-infrastructure/agents/terraform-specialist.md) | sonnet | Infrastructure as Code with Terraform modules and state management |
| [dx-optimizer](plugins/team-collaboration/agents/dx-optimizer.md)           | sonnet | Developer experience optimization and tooling improvements         |

#### Database Management

| Agent                                                                      | Model  | Description                                                         |
| -------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------- |
| [database-optimizer](plugins/observability-monitoring/agents/database-optimizer.md) | sonnet | Query optimization, index design, migration strategies              |
| [database-admin](plugins/database-migrations/agents/database-admin.md)    | sonnet | Database operations, backup, replication, monitoring                |
| [database-architect](plugins/database-design/agents/database-architect.md) | opus   | Database design from scratch, technology selection, schema modeling |

#### Incident Response & Network

| Agent                                                                    | Model  | Description                                         |
| ------------------------------------------------------------------------ | ------ | --------------------------------------------------- |
| [incident-responder](plugins/incident-response/agents/incident-responder.md) | opus   | Production incident management and resolution       |
| [network-engineer](plugins/observability-monitoring/agents/network-engineer.md) | sonnet | Network debugging, load balancing, traffic analysis |

### Quality Assurance & Security

#### Code Quality & Review

| Agent                                                                        | Model | Description                                                  |
| ---------------------------------------------------------------------------- | ----- | ------------------------------------------------------------ |
| [code-reviewer](plugins/comprehensive-review/agents/code-reviewer.md)        | opus  | Code review with security focus and production reliability   |
| [security-auditor](plugins/comprehensive-review/agents/security-auditor.md)  | opus  | Vulnerability assessment and OWASP compliance                |
| [backend-security-coder](plugins/data-validation-suite/agents/backend-security-coder.md) | opus  | Secure backend coding practices, API security implementation |
| [frontend-security-coder](plugins/frontend-mobile-security/agents/frontend-security-coder.md) | opus  | XSS prevention, CSP implementation, client-side security     |
| [mobile-security-coder](plugins/frontend-mobile-security/agents/mobile-security-coder.md) | opus  | Mobile security patterns, WebView security, biometric auth   |

#### Testing & Debugging

| Agent                                                                | Model  | Description                                                |
| -------------------------------------------------------------------- | ------ | ---------------------------------------------------------- |
| [test-automator](plugins/codebase-cleanup/agents/test-automator.md) | sonnet | Comprehensive test suite creation (unit, integration, e2e) |
| [tdd-orchestrator](plugins/backend-development/agents/tdd-orchestrator.md) | sonnet | Test-Driven Development methodology guidance               |
| [debugger](plugins/error-debugging/agents/debugger.md)               | sonnet | Error resolution and test failure analysis                 |
| [error-detective](plugins/error-debugging/agents/error-detective.md) | sonnet | Log analysis and error pattern recognition                 |

#### Performance & Observability

| Agent                                                                        | Model | Description                                                    |
| ---------------------------------------------------------------------------- | ----- | -------------------------------------------------------------- |
| [performance-engineer](plugins/observability-monitoring/agents/performance-engineer.md) | opus  | Application profiling and optimization                         |
| [observability-engineer](plugins/observability-monitoring/agents/observability-engineer.md) | opus  | Production monitoring, distributed tracing, SLI/SLO management |
| [search-specialist](plugins/content-marketing/agents/search-specialist.md)  | haiku | Advanced web research and information synthesis                |

### Data & AI

#### Data Engineering & Analytics

| Agent                                                                | Model  | Description                                             |
| -------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [data-scientist](plugins/machine-learning-ops/agents/data-scientist.md) | opus   | Data analysis, SQL queries, BigQuery operations         |
| [data-engineer](plugins/data-engineering/agents/data-engineer.md)   | sonnet | ETL pipelines, data warehouses, streaming architectures |

#### Machine Learning & AI

| Agent                                                            | Model | Description                                              |
| ---------------------------------------------------------------- | ----- | -------------------------------------------------------- |
| [ai-engineer](plugins/llm-application-dev/agents/ai-engineer.md) | opus  | LLM applications, RAG systems, prompt pipelines          |
| [ml-engineer](plugins/machine-learning-ops/agents/ml-engineer.md) | opus  | ML pipelines, model serving, feature engineering         |
| [mlops-engineer](plugins/machine-learning-ops/agents/mlops-engineer.md) | opus  | ML infrastructure, experiment tracking, model registries |
| [prompt-engineer](plugins/llm-application-dev/agents/prompt-engineer.md) | opus  | LLM prompt optimization and engineering                  |

### Documentation & Technical Writing

| Agent                                                                    | Model  | Description                                       |
| ------------------------------------------------------------------------ | ------ | ------------------------------------------------- |
| [docs-architect](plugins/code-documentation/agents/docs-architect.md)    | opus   | Comprehensive technical documentation generation  |
| [api-documenter](plugins/api-testing-observability/agents/api-documenter.md) | sonnet | OpenAPI/Swagger specifications and developer docs |
| [reference-builder](plugins/documentation-generation/agents/reference-builder.md) | haiku  | Technical references and API documentation        |
| [tutorial-engineer](plugins/code-documentation/agents/tutorial-engineer.md) | sonnet | Step-by-step tutorials and educational content    |
| [mermaid-expert](plugins/documentation-generation/agents/mermaid-expert.md) | sonnet | Diagram creation (flowcharts, sequences, ERDs)    |

### Business & Operations

#### Business Analysis & Finance

| Agent                                                                | Model  | Description                                             |
| -------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [business-analyst](plugins/business-analytics/agents/business-analyst.md) | sonnet | Metrics analysis, reporting, KPI tracking               |
| [quant-analyst](plugins/quantitative-trading/agents/quant-analyst.md) | opus   | Financial modeling, trading strategies, market analysis |
| [risk-manager](plugins/quantitative-trading/agents/risk-manager.md) | sonnet | Portfolio risk monitoring and management                |

#### Marketing & Sales

| Agent                                                                  | Model  | Description                                  |
| ---------------------------------------------------------------------- | ------ | -------------------------------------------- |
| [content-marketer](plugins/content-marketing/agents/content-marketer.md) | sonnet | Blog posts, social media, email campaigns    |
| [sales-automator](plugins/customer-sales-automation/agents/sales-automator.md) | haiku  | Cold emails, follow-ups, proposal generation |

#### Support & Legal

| Agent                                                                      | Model  | Description                                             |
| -------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [customer-support](plugins/customer-sales-automation/agents/customer-support.md) | sonnet | Support tickets, FAQ responses, customer communication  |
| [hr-pro](plugins/hr-legal-compliance/agents/hr-pro.md)                    | opus   | HR operations, policies, employee relations             |
| [legal-advisor](plugins/hr-legal-compliance/agents/legal-advisor.md)      | opus   | Privacy policies, terms of service, legal documentation |

### SEO & Content Optimization

| Agent                                                                                        | Model  | Description                                          |
| -------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------- |
| [seo-content-auditor](plugins/seo-content-creation/agents/seo-content-auditor.md)           | sonnet | Content quality analysis, E-E-A-T signals assessment |
| [seo-meta-optimizer](plugins/seo-technical-optimization/agents/seo-meta-optimizer.md)       | haiku  | Meta title and description optimization              |
| [seo-keyword-strategist](plugins/seo-technical-optimization/agents/seo-keyword-strategist.md) | haiku  | Keyword analysis and semantic variations             |
| [seo-structure-architect](plugins/seo-technical-optimization/agents/seo-structure-architect.md) | haiku  | Content structure and schema markup                  |
| [seo-snippet-hunter](plugins/seo-technical-optimization/agents/seo-snippet-hunter.md)       | haiku  | Featured snippet formatting                          |
| [seo-content-refresher](plugins/seo-analysis-monitoring/agents/seo-content-refresher.md)    | haiku  | Content freshness analysis                           |
| [seo-cannibalization-detector](plugins/seo-analysis-monitoring/agents/seo-cannibalization-detector.md) | haiku  | Keyword overlap detection                            |
| [seo-authority-builder](plugins/seo-analysis-monitoring/agents/seo-authority-builder.md)    | sonnet | E-E-A-T signal analysis                              |
| [seo-content-writer](plugins/seo-content-creation/agents/seo-content-writer.md)             | sonnet | SEO-optimized content creation                       |
| [seo-content-planner](plugins/seo-content-creation/agents/seo-content-planner.md)           | haiku  | Content planning and topic clusters                  |

### Specialized Domains

| Agent                                                                        | Model  | Description                                                |
| ---------------------------------------------------------------------------- | ------ | ---------------------------------------------------------- |
| [arm-cortex-expert](plugins/arm-cortex-microcontrollers/agents/arm-cortex-expert.md)   | sonnet | ARM Cortex-M firmware and peripheral driver development    |
| [blockchain-developer](plugins/blockchain-web3/agents/blockchain-developer.md) | sonnet | Web3 apps, smart contracts, DeFi protocols                 |
| [payment-integration](plugins/payment-processing/agents/payment-integration.md) | sonnet | Payment processor integration (Stripe, PayPal) |
| [legacy-modernizer](plugins/framework-migration/agents/legacy-modernizer.md) | sonnet | Legacy code refactoring and modernization      |
| [context-manager](plugins/agent-orchestration/agents/context-manager.md)    | haiku  | Multi-agent context management                 |

## Model Configuration

Agents are assigned to specific Claude models based on task complexity and computational requirements. The system uses two model tiers:

### Model Distribution Summary

| Model  | Agent Count | Use Case                                                                           |
| ------ | ----------- | ---------------------------------------------------------------------------------- |
| Haiku  | 47          | Fast execution tasks: testing, documentation, ops, database optimization, business |
| Sonnet | 99          | Complex reasoning, architecture, language expertise, orchestration, security       |

### Haiku Model Agents

| Category                   | Count | Agents                                                                                                                                                                          |
| -------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Testing & Debugging        | 7     | `test-automator`, `debugger`, `error-detective`                                                                                                                                 |
| Documentation              | 4     | `api-documenter`, `tutorial-engineer`, `mermaid-expert`                                                                                                                         |
| Infrastructure & DevOps    | 10    | `deployment-engineer`, `devops-troubleshooter`, `network-engineer`, `database-admin`                                                                                            |
| Database Optimization      | 3     | `database-optimizer`, `sql-pro`                                                                                                                                                 |
| Code Quality & Refactoring | 3     | `legacy-modernizer`                                                                                                                                                             |
| Business Operations        | 4     | `customer-support`, `business-analyst`, `content-marketer`, `risk-manager`                                                                                                      |
| Developer Experience       | 3     | `dx-optimizer`, `terraform-specialist`                                                                                                                                          |
| Specialized Tools          | 2     | `payment-integration`, `context-manager`                                                                                                                                        |
| SEO Optimization           | 7     | `seo-meta-optimizer`, `seo-keyword-strategist`, `seo-structure-architect`, `seo-snippet-hunter`, `seo-content-refresher`, `seo-cannibalization-detector`, `seo-content-planner` |
| Context & Reference        | 4     | `context-manager`, `reference-builder`, `sales-automator`, `search-specialist`                                                                                                  |

### Sonnet Model Agents

| Category                    | Count | Key Agents                                                                                                                                                              |
| --------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Architecture & Design       | 12    | `backend-architect`, `frontend-developer`, `cloud-architect`, `hybrid-cloud-architect`, `kubernetes-architect`, `database-architect`, `graphql-architect`               |
| Programming Languages       | 18    | All language-specific experts: `python-pro`, `javascript-pro`, `typescript-pro`, `rust-pro`, `golang-pro`, `java-pro`, `cpp-pro`, `c-pro`, `php-pro`, `ruby-pro`, etc. |
| Scripting Languages         | 2     | `bash-pro`, `posix-shell-pro`                                                                                                                                           |
| Security & Code Review      | 8     | `code-reviewer`, `security-auditor`, `backend-security-coder`, `frontend-security-coder`, `mobile-security-coder`                                                      |
| Frontend & UI               | 5     | `frontend-developer`, `ui-ux-designer`, `ui-visual-validator`, `mobile-developer`, `ios-developer`, `flutter-expert`                                                   |
| AI/ML & Data                | 7     | `ai-engineer`, `ml-engineer`, `mlops-engineer`, `data-scientist`, `prompt-engineer`, `data-engineer`                                                                   |
| Performance & Observability | 3     | `performance-engineer`, `observability-engineer`, `incident-responder`                                                                                                  |
| Framework Specialists       | 6     | `django-pro`, `fastapi-pro`, `tdd-orchestrator`, `graphql-architect`                                                                                                   |
| Documentation               | 2     | `docs-architect`, `tutorial-engineer`                                                                                                                                   |
| Business Critical           | 4     | `hr-pro`, `legal-advisor`, `quant-analyst`                                                                                                                              |
| SEO & Content               | 3     | `seo-content-auditor`, `seo-authority-builder`, `seo-content-writer`                                                                                                    |
| Specialized Domains         | 6     | `blockchain-developer`, `unity-developer`, `minecraft-bukkit-pro`, `arm-cortex-expert`, `payment-integration`, `elixir-pro`                                             |
| Infrastructure & Tools      | 23    | Remaining infrastructure, DevOps, database, and tooling agents                                                                                                          |

### Hybrid Orchestration Patterns

The plugin ecosystem leverages Sonnet + Haiku orchestration for optimal performance and cost efficiency:

#### Pattern 1: Planning → Execution
```
Sonnet: backend-architect (design API architecture)
  ↓
Haiku: Generate API endpoints following spec
  ↓
Haiku: test-automator (generate comprehensive tests)
  ↓
Sonnet: code-reviewer (architectural review)
```

#### Pattern 2: Reasoning → Action (Incident Response)
```
Sonnet: incident-responder (diagnose issue, create strategy)
  ↓
Haiku: devops-troubleshooter (execute fixes)
  ↓
Haiku: deployment-engineer (deploy hotfix)
  ↓
Haiku: Implement monitoring alerts
```

#### Pattern 3: Complex → Simple (Database Design)
```
Sonnet: database-architect (schema design, technology selection)
  ↓
Haiku: sql-pro (generate migration scripts)
  ↓
Haiku: database-admin (execute migrations)
  ↓
Haiku: database-optimizer (tune query performance)
```

#### Pattern 4: Multi-Agent Workflows
```
Full-Stack Feature Development:
Sonnet: backend-architect + frontend-developer (design components)
  ↓
Haiku: Generate code following designs
  ↓
Haiku: test-automator (unit + integration tests)
  ↓
Sonnet: security-auditor (security review)
  ↓
Haiku: deployment-engineer (CI/CD setup)
  ↓
Haiku: Setup observability stack
```

## Architecture & Design Principles

This marketplace follows industry best practices with a focus on granularity, composability, and minimal token usage:

### Single Responsibility Principle

- Each plugin does **one thing well** (Unix philosophy)
- Clear, focused purposes (describable in 5-10 words)
- Average plugin size: **3.4 components** (follows Anthropic's 2-8 pattern)
- **Zero bloated plugins** - all plugins focused and purposeful

### Granular Plugin Architecture

- **64 focused plugins** optimized for specific use cases
- **23 clear categories** with 1-6 plugins each for easy discovery
- Organized by domain:
  - **Development**: 4 plugins (debugging, backend, frontend, multi-platform)
  - **Security**: 4 plugins (scanning, compliance, backend-api, frontend-mobile)
  - **Operations**: 4 plugins (incident, diagnostics, distributed, observability)
  - **Languages**: 8 plugins (Python, JS/TS, systems, JVM, web scripting, functional, shell, embedded)
  - **Infrastructure**: 5 plugins (deployment, validation, K8s, cloud, CI/CD)
  - And 18 more specialized categories

### Tools & Capabilities

- **44 development tools** including:
  - `test-generate.md` - Automated unit test generation (pytest/Jest)
  - `component-scaffold.md` - React/React Native scaffolding
  - `xss-scan.md` - XSS vulnerability scanner with secure patterns
  - `python-scaffold.md` - Python project scaffolding (FastAPI/Django)
  - `typescript-scaffold.md` - TypeScript project scaffolding (Next.js/Vite)
  - `rust-project.md` - Rust project scaffolding (cargo/Axum)
- **100% agent coverage** - all plugins include at least one agent
- **Language-specific plugins** - 8 dedicated plugins for language experts

### Performance & Quality

- **Optimized token usage** - isolated plugins load only what you need
- **Better context efficiency** - granular plugins reduce unnecessary context
- **Clear discoverability** - well-organized categories and focused purposes
- **Isolated dependencies** - each plugin contains only its required resources
- **100% component coverage** - all 87 agents available across plugins

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

To add new agents or commands:

1. Identify or create the appropriate plugin directory in `plugins/`
2. Create a new `.md` file in `plugins/{plugin-name}/agents/` or `plugins/{plugin-name}/commands/`
3. Use lowercase, hyphen-separated naming convention
4. Write clear activation criteria in the description
5. Define comprehensive system prompt with expertise areas
6. Update the plugin definition in `.claude-plugin/marketplace.json`

### Plugin Structure

Each plugin must follow this structure:

```
plugins/{plugin-name}/
├── agents/          # Agent definitions (optional)
│   └── agent-name.md
└── commands/        # Commands/tools (optional)
    └── command-name.md
```

### Subagent Format

Each subagent is defined as a Markdown file with frontmatter:

```markdown
---
name: subagent-name
description: Activation criteria for this subagent
model: haiku|sonnet|opus # Optional: Model selection
tools: tool1, tool2 # Optional: Tool restrictions
---

System prompt defining the subagent's expertise and behavior
```

### Model Selection Criteria

Choose the right model for your agent based on these guidelines:

#### Haiku - Fast Execution & Deterministic Tasks
**Use when:**
- Generating code from well-defined specifications
- Creating tests following established patterns
- Writing documentation with clear templates
- Executing infrastructure operations
- Performing database query optimization
- Handling customer support responses
- Processing SEO optimization tasks
- Managing deployment pipelines

#### Sonnet - Complex Reasoning & Architecture
**Use when:**
- Designing system architecture
- Making technology selection decisions
- Performing security audits
- Reviewing code for architectural patterns
- Creating complex AI/ML pipelines
- Providing language-specific expertise
- Orchestrating multi-agent workflows
- Handling business-critical legal/HR matters

**Decision Tree:**
```
Does the task require architectural decisions or domain expertise?
  YES → sonnet
  NO  → Is it a well-defined, deterministic execution task?
    YES → haiku
    NO  → sonnet (default)
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Claude Code Plugins Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Claude Code Subagents Guide](https://docs.claude.com/en/docs/claude-code/sub-agents)
- [Claude Code Slash Commands Reference](https://docs.claude.com/en/docs/claude-code/slash-commands)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=wshobson/agents&type=date&legend=top-left)](https://www.star-history.com/#wshobson/agents&type=date&legend=top-left)
