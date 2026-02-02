<div align="right">
  <details>
    <summary >🌐 Language</summary>
    <div>
      <div align="center">
        <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=en">English</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=zh-CN">简体中文</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=zh-TW">繁體中文</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=ja">日本語</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=ko">한국어</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=hi">हिन्दी</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=th">ไทย</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=fr">Français</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=de">Deutsch</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=es">Español</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=it">Italiano</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=ru">Русский</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=pt">Português</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=nl">Nederlands</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=pl">Polski</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=ar">العربية</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=fa">فارسی</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=tr">Türkçe</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=vi">Tiếng Việt</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=id">Bahasa Indonesia</a>
        | <a href="https://openaitx.github.io/view.html?user=wshobson&project=agents&lang=as">অসমীয়া</
      </div>
    </div>
  </details>
</div>

# Claude Code Subagents Collection

A comprehensive collection of specialized AI subagents for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), designed to enhance development workflows with domain-specific expertise. Now featuring **Hive-Mind Architecture** for intelligent multi-agent coordination.

## Overview

This repository contains **95 expert-level subagents** that extend Claude Code's capabilities with deep, specialized knowledge across all areas of software development and business operations. Each subagent has been comprehensively enhanced with:

- **2024/2025 Best Practices** - Latest tools, frameworks, and industry standards
- **Production-Ready Knowledge** - Real-world scenarios and enterprise patterns
- **Expert-Level Depth** - 8-12 detailed capability subsections per agent
- **Modern Tech Stacks** - Current versions and cutting-edge technologies
- **Optimal Model Selection** - Opus/Sonnet/Haiku assignment based on task complexity
- **Hive-Mind Architecture** - Distributed multi-agent coordination for complex tasks

## 🐝 Hive-Mind Architecture

The hive-mind system enables intelligent coordination of multiple agents for complex, enterprise-scale tasks. Inspired by swarm intelligence and distributed systems patterns.

### Queen Agents (Strategic Leadership)

| Agent | Purpose | Model |
|-------|---------|-------|
| **[hive-queen-strategic](hive-queen-strategic.md)** | High-level planning, goal decomposition, multi-agent orchestration | Opus |
| **[hive-queen-tactical](hive-queen-tactical.md)** | Real-time execution coordination, progress monitoring, blocker resolution | Opus |
| **[hive-queen-adaptive](hive-queen-adaptive.md)** | Continuous optimization, pattern learning, workflow improvement | Opus |

### Coordination Agents (Swarm Management)

| Agent | Purpose | Model |
|-------|---------|-------|
| **[swarm-coordinator](swarm-coordinator.md)** | Distributed agent spawning, communication protocols, result aggregation | Sonnet |
| **[consensus-builder](consensus-builder.md)** | Multi-agent decision-making, conflict resolution, voting mechanisms | Sonnet |
| **[memory-archivist](memory-archivist.md)** | Persistent shared memory, knowledge consolidation, cross-session continuity | Sonnet |
| **[task-router](task-router.md)** | Intelligent task assignment, capability matching, load balancing | Haiku |
| **[agent-spawner](agent-spawner.md)** | Agent creation, configuration, lifecycle management | Haiku |

### Hive-Mind Workflow Example

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HIVE-QUEEN-STRATEGIC                             │
│                 (Planning & Decomposition)                          │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    HIVE-QUEEN-TACTICAL                              │
│                 (Execution Coordination)                            │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │ SWARM   │  │ TASK    │  │ MEMORY  │
        │COORDNTR │  │ ROUTER  │  │ARCHIVIST│
        └────┬────┘  └────┬────┘  └────┬────┘
             │            │            │
     ┌───────┴───────┐    │            │
     │               │    │            │
     ▼               ▼    ▼            ▼
┌─────────┐    ┌─────────────┐   ┌─────────────┐
│ Worker  │    │   Worker    │   │   Shared    │
│ Agents  │    │   Agents    │   │   Memory    │
│ (Swarm) │    │  (Routed)   │   │   System    │
└─────────┘    └─────────────┘   └─────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    HIVE-QUEEN-ADAPTIVE                              │
│            (Learning & Continuous Improvement)                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Hive-Mind Use Cases

```bash
# Enterprise-scale platform migration
"Use hive-queen-strategic to orchestrate migration from monolith to microservices"
# Spawns: backend-architect, database-architect, kubernetes-architect, devops-troubleshooter

# Complex feature with multiple teams
"Have hive-queen-tactical coordinate the checkout feature across frontend, backend, and payments"
# Coordinates: frontend-developer, backend-architect, payment-integration, test-automator

# Continuous optimization
"Use hive-queen-adaptive to analyze our deployment patterns and suggest improvements"
# Analyzes: deployment-engineer, performance-engineer, observability-engineer

# Distributed code analysis
"Have swarm-coordinator spawn parallel code reviewers across the codebase"
# Spawns: multiple code-reviewer instances, consensus-builder for aggregation

# Multi-agent decision making
"Use consensus-builder to resolve the architecture disagreement between teams"
# Coordinates: backend-architect, frontend-developer, security-auditor
```

---

## Available Subagents

### Development & Architecture
- **[backend-architect](backend-architect.md)** - Design RESTful APIs, microservice boundaries, and database schemas
- **[frontend-developer](frontend-developer.md)** - Build React components, implement responsive layouts, and handle client-side state management
- **[ui-ux-designer](ui-ux-designer.md)** - Create interface designs, wireframes, and design systems
- **[ui-visual-validator](ui-visual-validator.md)** - Verify whether UI modifications have achieved their intended goals through rigorous screenshot analysis
- **[mobile-developer](mobile-developer.md)** - Develop React Native or Flutter apps with native integrations
- **[graphql-architect](graphql-architect.md)** - Design GraphQL schemas, resolvers, and federation
- **[architect-reviewer](architect-review.md)** - Reviews code changes for architectural consistency and patterns
- **[database-architect](database-architect.md)** - Design scalable database systems, data modeling, and distributed data architecture
- **[event-sourcing-architect](event-sourcing-architect.md)** - Expert in event sourcing, CQRS, and event-driven architecture patterns
- **[monorepo-architect](monorepo-architect.md)** - Monorepo strategy with Nx, Turborepo, and Bazel for large-scale codebases

### Language Specialists
- **[python-pro](python-pro.md)** - Write idiomatic Python code with advanced features and optimizations
- **[ruby-pro](ruby-pro.md)** - Write idiomatic Ruby code with metaprogramming, Rails patterns, gem development, and testing frameworks
- **[golang-pro](golang-pro.md)** - Write idiomatic Go code with goroutines, channels, and interfaces
- **[rust-pro](rust-pro.md)** - Write idiomatic Rust with ownership patterns, lifetimes, and trait implementations
- **[c-pro](c-pro.md)** - Write efficient C code with proper memory management and system calls
- **[cpp-pro](cpp-pro.md)** - Write idiomatic C++ code with modern features, RAII, smart pointers, and STL algorithms
- **[javascript-pro](javascript-pro.md)** - Master modern JavaScript with ES6+, async patterns, and Node.js APIs
- **[typescript-pro](typescript-pro.md)** - Master TypeScript with advanced types, generics, and strict type safety
- **[php-pro](php-pro.md)** - Write idiomatic PHP code with modern features and performance optimizations
- **[java-pro](java-pro.md)** - Master modern Java with streams, concurrency, and JVM optimization
- **[elixir-pro](elixir-pro.md)** - Write idiomatic Elixir code with OTP patterns, functional programming, and Phoenix frameworks
- **[csharp-pro](csharp-pro.md)** - Write modern C# code with advanced features and .NET optimization
- **[scala-pro](scala-pro.md)** - Master enterprise-grade Scala development with functional programming, distributed systems, and big data processing
- **[flutter-expert](flutter-expert.md)** - Master Flutter development with Dart, widgets, and platform integrations
- **[unity-developer](unity-developer.md)** - Build Unity games with optimized scripts and performance tuning
- **[minecraft-bukkit-pro](minecraft-bukkit-pro.md)** - Master Minecraft server plugin development with Bukkit, Spigot, and Paper APIs
- **[ios-developer](ios-developer.md)** - Develop native iOS applications with Swift/SwiftUI
- **[sql-pro](sql-pro.md)** - Write complex SQL queries, optimize execution plans, and design normalized schemas
- **[haskell-pro](haskell-pro.md)** - Pure functional programming with advanced type systems and GHC

### Infrastructure & Operations
- **[devops-troubleshooter](devops-troubleshooter.md)** - Debug production issues, analyze logs, and fix deployment failures
- **[deployment-engineer](deployment-engineer.md)** - Configure CI/CD pipelines, Docker containers, and cloud deployments
- **[cloud-architect](cloud-architect.md)** - Design AWS/Azure/GCP infrastructure and optimize cloud costs
- **[hybrid-cloud-architect](hybrid-cloud-architect.md)** - Design hybrid cloud infrastructure across AWS/Azure/GCP and OpenStack on-premises environments
- **[kubernetes-architect](kubernetes-architect.md)** - Design cloud-native infrastructure with Kubernetes at its core and GitOps principles across AWS/Azure/GCP and hybrid environments.
- **[database-optimizer](database-optimizer.md)** - Optimize SQL queries, design efficient indexes, and handle database migrations
- **[database-admin](database-admin.md)** - Manage database operations, backups, replication, and monitoring
- **[terraform-specialist](terraform-specialist.md)** - Write advanced Terraform modules, manage state files, and implement IaC best practices
- **[incident-responder](incident-responder.md)** - Handles production incidents with urgency and precision
- **[network-engineer](network-engineer.md)** - Debug network connectivity, configure load balancers, and analyze traffic patterns
- **[dx-optimizer](dx-optimizer.md)** - Developer Experience specialist that improves tooling, setup, and workflows
- **[service-mesh-expert](service-mesh-expert.md)** - Istio, Linkerd, and Envoy for microservice traffic management and mTLS
- **[observability-engineer](observability-engineer.md)** - OpenTelemetry, metrics, logging, and distributed tracing
- **[arm-cortex-expert](arm-cortex-expert.md)** - Embedded systems with ARM Cortex-M, RTOS, and bare-metal programming

### Quality & Security
- **[code-reviewer](code-reviewer.md)** - Expert code review with deep configuration security focus and production reliability
- **[security-auditor](security-auditor.md)** - Review code for vulnerabilities and ensure OWASP compliance
- **[test-automator](test-automator.md)** - Create comprehensive test suites with unit, integration, and e2e tests
- **[performance-engineer](performance-engineer.md)** - Profile applications, optimize bottlenecks, and implement caching strategies
- **[debugger](debugger.md)** - Debugging specialist for errors, test failures, and unexpected behavior
- **[error-detective](error-detective.md)** - Search logs and codebases for error patterns, stack traces, and anomalies
- **[search-specialist](search-specialist.md)** - Expert web researcher using advanced search techniques and synthesis
- **[tdd-orchestrator](tdd-orchestrator.md)** - Test-Driven Development workflows and testing strategy

### Data & AI
- **[data-scientist](data-scientist.md)** - Data analysis expert for SQL queries, BigQuery operations, and data insights
- **[data-engineer](data-engineer.md)** - Build ETL pipelines, data warehouses, and streaming architectures
- **[ai-engineer](ai-engineer.md)** - Build LLM applications, RAG systems, and prompt pipelines
- **[ml-engineer](ml-engineer.md)** - Implement ML pipelines, model serving, and feature engineering
- **[mlops-engineer](mlops-engineer.md)** - Build ML pipelines, experiment tracking, and model registries
- **[prompt-engineer](prompt-engineer.md)** - Optimizes prompts for LLMs and AI systems
- **[vector-database-engineer](vector-database-engineer.md)** - Pinecone, Qdrant, Weaviate, and semantic search systems

### Specialized Domains
- **[api-documenter](api-documenter.md)** - Create OpenAPI/Swagger specs and write developer documentation
- **[payment-integration](payment-integration.md)** - Integrate Stripe, PayPal, and payment processors
- **[quant-analyst](quant-analyst.md)** - Build financial models, backtest trading strategies, and analyze market data
- **[risk-manager](risk-manager.md)** - Monitor portfolio risk, R-multiples, and position limits
- **[legacy-modernizer](legacy-modernizer.md)** - Refactor legacy codebases and implement gradual modernization
- **[context-manager](context-manager.md)** - Manages context across multiple agents and long-running tasks
- **[blockchain-developer](blockchain-developer.md)** - Smart contracts, DeFi, Web3, and blockchain security with Solidity

### Documentation
- **[docs-architect](docs-architect.md)** - Creates comprehensive technical documentation from existing codebases
- **[mermaid-expert](mermaid-expert.md)** - Create Mermaid diagrams for flowcharts, sequences, ERDs, and architectures
- **[reference-builder](reference-builder.md)** - Creates exhaustive technical references and API documentation
- **[tutorial-engineer](tutorial-engineer.md)** - Creates step-by-step tutorials and educational content from code

### Business & Marketing
- **[business-analyst](business-analyst.md)** - Analyze metrics, create reports, and track KPIs
- **[content-marketer](content-marketer.md)** - Write blog posts, social media content, and email newsletters
- **[hp-pro](hp-pro.md)** - Partner for hiring, onboarding/offboarding, PTO and leave, performance, compliant policies, and employee relations.
- **[sales-automator](sales-automator.md)** - Draft cold emails, follow-ups, and proposal templates
- **[customer-support](customer-support.md)** - Handle support tickets, FAQ responses, and customer emails
- **[legal-advisor](legal-advisor.md)** - Draft privacy policies, terms of service, disclaimers, and legal notices

### SEO & Content Optimization
- **[seo-content-auditor](seo-content-auditor.md)** - Analyzes provided content for quality, E-E-A-T signals, and SEO best practices
- **[seo-meta-optimizer](seo-meta-optimizer.md)** - Creates optimized meta titles, descriptions, and URL suggestions
- **[seo-keyword-strategist](seo-keyword-strategist.md)** - Analyzes keyword usage, calculates density, suggests semantic variations
- **[seo-structure-architect](seo-structure-architect.md)** - Optimizes content structure, header hierarchy, and schema markup
- **[seo-snippet-hunter](seo-snippet-hunter.md)** - Formats content for featured snippets and SERP features
- **[seo-content-refresher](seo-content-refresher.md)** - Identifies outdated elements and suggests content updates
- **[seo-cannibalization-detector](seo-cannibalization-detector.md)** - Analyzes multiple pages for keyword overlap and conflicts
- **[seo-authority-builder](seo-authority-builder.md)** - Analyzes content for E-E-A-T signals and trust indicators
- **[seo-content-writer](seo-content-writer.md)** - Writes SEO-optimized content based on keywords and briefs
- **[seo-content-planner](seo-content-planner.md)** - Creates content outlines, topic clusters, and calendars

## Model Assignments

All 95 subagents are configured with specific Claude models based on task complexity:

### 🚀 Haiku (Fast & Cost-Effective) - 15 agents
**Model:** `haiku`
- `context-manager` - AI context engineering with vector databases
- `reference-builder` - Exhaustive technical references and API documentation
- `sales-automator` - Modern sales automation with CRM integration
- `search-specialist` - Expert web research and information synthesis
- `seo-meta-optimizer` - Meta title and description optimization
- `seo-keyword-strategist` - Keyword density and semantic analysis
- `seo-structure-architect` - Content structure and schema markup
- `seo-snippet-hunter` - Featured snippet formatting
- `seo-content-refresher` - Content freshness updates
- `seo-cannibalization-detector` - Keyword overlap detection
- `seo-content-planner` - Content calendars and topic clusters
- `task-router` - Intelligent task assignment and capability matching
- `agent-spawner` - Agent creation and lifecycle management

### ⚡ Sonnet (Balanced Performance) - 49 agents
**Model:** `sonnet`

**Development & Languages:**
- `python-pro` - Python development with advanced features
- `ruby-pro` - Ruby development with metaprogramming, Rails patterns, and gem development
- `javascript-pro` - Modern JavaScript and Node.js
- `typescript-pro` - Advanced TypeScript with type systems
- `golang-pro` - Go concurrency and idiomatic patterns
- `rust-pro` - Rust memory safety and systems programming
- `c-pro` - C programming and embedded systems
- `cpp-pro` - Modern C++ with STL and templates
- `php-pro` - Modern PHP with advanced features
- `java-pro` - Modern Java with streams and concurrency
- `elixir-pro` - Elixir with OTP patterns and Phoenix
- `csharp-pro` - Modern C# with .NET frameworks and patterns
- `scala-pro` - Enterprise Scala with Apache Pekko, Akka, Spark, and ZIO/Cats Effect
- `flutter-expert` - Flutter development with state management and animations
- `unity-developer` - Unity game development and optimization
- `minecraft-bukkit-pro` - Minecraft plugin development with Bukkit/Spigot/Paper
- `ios-developer` - Native iOS development with Swift/SwiftUI
- `frontend-developer` - React components and UI
- `ui-ux-designer` - Interface design and wireframes
- `ui-visual-validator` - Rigorous UI validation through screenshot analysis
- `backend-architect` - API design and microservices
- `mobile-developer` - React Native/Flutter apps
- `sql-pro` - Complex SQL optimization
- `graphql-architect` - GraphQL schemas and resolvers
- `haskell-pro` - Pure functional programming with advanced type systems

**Infrastructure & Operations:**
- `devops-troubleshooter` - Production debugging with modern observability
- `deployment-engineer` - GitOps workflows and platform engineering
- `cloud-architect` - Multi-cloud expertise with FinOps optimization
- `hybrid-cloud-architect` - Complex multi-cloud and edge architectures
- `kubernetes-architect` - Cloud-native infrastructure with service mesh
- `database-optimizer` - Advanced performance tuning and scalability
- `database-admin` - Cloud databases and reliability engineering
- `terraform-specialist` - Advanced IaC with OpenTofu knowledge
- `network-engineer` - Zero-trust networking and service mesh
- `security-auditor` - DevSecOps and compliance automation
- `performance-engineer` - OpenTelemetry and comprehensive optimization
- `incident-responder` - SRE principles and modern incident management
- `dx-optimizer` - Developer experience and platform engineering
- `data-engineer` - Modern data stack and real-time streaming
- `service-mesh-expert` - Istio, Linkerd, and microservice traffic management
- `arm-cortex-expert` - Embedded systems with ARM Cortex-M microcontrollers
- `monorepo-architect` - Nx, Turborepo, and Bazel for large codebases
- `swarm-coordinator` - Distributed agent spawning and coordination
- `consensus-builder` - Multi-agent decision-making and conflict resolution
- `memory-archivist` - Persistent shared memory for multi-agent operations
- `tdd-orchestrator` - Test-Driven Development workflows

**Quality & AI/ML:**
- `test-automator` - AI-powered testing with self-healing frameworks
- `code-reviewer` - Expert code analysis with modern security scanning
- `ai-engineer` - Advanced LLM integration with RAG and agent systems
- `ml-engineer` - Production ML with modern frameworks and monitoring
- `mlops-engineer` - Comprehensive ML infrastructure and automation
- `data-scientist` - Advanced analytics with cloud platforms
- `prompt-engineer` - Cutting-edge LLM optimization techniques

### 🧠 Opus (Maximum Capability) - 31 agents
**Model:** `opus`

**Critical Analysis & Architecture:**
- `ai-engineer` - LLM applications and RAG systems
- `architect-reviewer` - Architectural consistency and patterns
- `backend-architect` - System architecture and scalability design
- `cloud-architect` - Multi-cloud infrastructure architecture
- `code-reviewer` - Critical code quality and security analysis
- `data-scientist` - Complex analytics and statistical modeling
- `database-optimizer` - Performance-critical query optimization
- `database-architect` - Scalable database design and distributed systems
- `event-sourcing-architect` - Event sourcing, CQRS, and domain-driven design

**Complex Engineering & Operations:**
- `hybrid-cloud-architect` - Complex multi-cloud strategies
- `incident-responder` - Critical production incident handling
- `kubernetes-architect` - Cloud-native infrastructure design
- `ml-engineer` - Complex ML model development and deployment
- `mlops-engineer` - ML infrastructure and automation
- `performance-engineer` - Advanced application optimization
- `prompt-engineer` - Advanced LLM optimization techniques
- `security-auditor` - Comprehensive vulnerability analysis
- `terraform-specialist` - Infrastructure architecture with IaC
- `observability-engineer` - OpenTelemetry, distributed tracing, and monitoring
- `vector-database-engineer` - Semantic search and RAG infrastructure
- `blockchain-developer` - Smart contracts, DeFi, and Web3 security

**Hive-Mind Leadership:**
- `hive-queen-strategic` - Strategic planning and multi-agent orchestration
- `hive-queen-tactical` - Real-time execution coordination
- `hive-queen-adaptive` - Continuous optimization and learning

**Business Critical & Compliance:**
- `context-manager` - Multi-agent coordination for complex tasks
- `docs-architect` - Comprehensive technical documentation
- `hr-pro` - Complex HR scenarios and legal compliance
- `legal-advisor` - Legal analysis and contract review
- `quant-analyst` - Advanced financial modeling and algorithmic trading

**Model Optimization:**
Agents are strategically assigned models based on task complexity:
- **Opus (31)**: Complex reasoning, critical analysis, architecture, hive-mind leadership
- **Sonnet (49)**: Balanced development, specialized tasks, swarm coordination
- **Haiku (15)**: Fast, focused utility tasks, task routing

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
"Have code-reviewer scrutinize these configuration changes"
"Have security-auditor check for OWASP compliance issues"

# Development tasks  
"Get backend-architect to design a user authentication API"
"Use frontend-developer to create a responsive dashboard layout"

# Infrastructure and operations
"Have devops-troubleshooter analyze these production logs"
"Use cloud-architect to design a scalable AWS architecture"
"Get network-engineer to debug SSL certificate issues"
"Use database-admin to set up backup and replication"

# Data and AI
"Get data-scientist to analyze this customer behavior dataset"
"Use ai-engineer to build a RAG system for document search"
"Have mlops-engineer set up MLflow experiment tracking"

# Business and marketing
"Have business-analyst create investor deck with growth metrics"
"Use content-marketer to write SEO-optimized blog post"
"Get sales-automator to create cold email sequence"
"Have customer-support draft FAQ documentation"
```

### Multi-Agent Workflows

These subagents work together seamlessly, and for more complex orchestrations, you can use the **[Claude Code Commands](https://github.com/wshobson/commands)** collection which provides 52 pre-built slash commands that leverage these subagents in sophisticated workflows.

```bash
# Feature development workflow
"Implement user authentication feature"
# Automatically uses: backend-architect → frontend-developer → test-automator → security-auditor

# Performance optimization workflow  
"Optimize the checkout process performance"
# Automatically uses: performance-engineer → database-optimizer → frontend-developer

# Production incident workflow
"Debug high memory usage in production"
# Automatically uses: incident-responder → devops-troubleshooter → error-detective → performance-engineer

# Network connectivity workflow
"Fix intermittent API timeouts"
# Automatically uses: network-engineer → devops-troubleshooter → performance-engineer

# Database maintenance workflow
"Set up disaster recovery for production database"
# Automatically uses: database-admin → database-optimizer → incident-responder

# ML pipeline workflow
"Build end-to-end ML pipeline with monitoring"
# Automatically uses: mlops-engineer → ml-engineer → data-engineer → performance-engineer

# Product launch workflow
"Launch new feature with marketing campaign"
# Automatically uses: business-analyst → content-marketer → sales-automator → customer-support
```

### Advanced Workflows with Slash Commands

For more sophisticated multi-subagent orchestration, use the companion [Commands repository](https://github.com/wshobson/commands):

```bash
# Complex feature development (8+ subagents)
/full-stack-feature Build user dashboard with real-time analytics

# Production incident response (5+ subagents) 
/incident-response Database connection pool exhausted

# ML infrastructure setup (6+ subagents)
/ml-pipeline Create recommendation engine with A/B testing

# Security-focused implementation (7+ subagents)
/security-hardening Implement OAuth2 with zero-trust architecture
```

## Subagent Format

Each subagent follows this structure:
```markdown
---
name: subagent-name
description: When this subagent should be invoked
model: haiku  # Optional - specify which model to use (haiku/sonnet/opus)
tools: tool1, tool2  # Optional - defaults to all tools
---

System prompt defining the subagent's role and capabilities
```

### Model Configuration

As of Claude Code v1.0.64, subagents can specify which Claude model they should use. This allows for cost-effective task delegation based on complexity:

- **Low Complexity (Haiku)**: Simple tasks like basic data analysis, documentation generation, and standard responses
- **Medium Complexity (Sonnet)**: Development tasks, code review, testing, and standard engineering work  
- **High Complexity (Opus)**: Critical tasks like security auditing, architecture review, incident response, and AI/ML engineering

Available models (using simplified naming as of Claude Code v1.0.64):
- `haiku` - Fast and cost-effective for simple tasks
- `sonnet` - Balanced performance for most development work
- `opus` - Most capable for complex analysis and critical tasks

If no model is specified, the subagent will use the system's default model.

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

### 🐝 Hive-Mind & Orchestration
- **hive-queen-strategic**: Enterprise-scale planning, multi-team coordination, complex initiatives
- **hive-queen-tactical**: Active project execution, progress monitoring, blocker resolution
- **hive-queen-adaptive**: Workflow optimization, pattern analysis, continuous improvement
- **swarm-coordinator**: Parallel task execution, distributed agent management
- **consensus-builder**: Multi-agent decisions, conflict resolution, voting
- **memory-archivist**: Persistent context, cross-session continuity, collective knowledge
- **task-router**: Automatic task assignment, capability matching
- **agent-spawner**: Dynamic agent creation, configuration management

### 🏗️ Planning & Architecture
- **backend-architect**: API design, database schemas, system architecture
- **frontend-developer**: UI/UX planning, component architecture
- **ui-ux-designer**: Interface design, wireframes, design systems, user research
- **cloud-architect**: Infrastructure design, scalability planning
- **database-architect**: Data modeling, distributed databases, sharding strategies
- **event-sourcing-architect**: Event sourcing, CQRS, domain-driven design
- **monorepo-architect**: Nx, Turborepo, Bazel, large-scale repo management

### 🔧 Implementation & Development  
- **python-pro**: Python-specific development tasks
- **ruby-pro**: Ruby metaprogramming, Rails applications, gem development, RSpec/Minitest testing
- **golang-pro**: Go-specific development tasks
- **rust-pro**: Rust-specific development, memory safety, systems programming
- **c-pro**: C programming, embedded systems, performance-critical code
- **javascript-pro**: Modern JavaScript, async patterns, Node.js/browser code
- **typescript-pro**: Advanced TypeScript, generics, type inference, enterprise patterns
- **java-pro**: Modern Java development, streams, concurrency, Spring Boot
- **elixir-pro**: Elixir development, OTP patterns, Phoenix frameworks, functional programming
- **csharp-pro**: Modern C# development, .NET frameworks, enterprise patterns
- **scala-pro**: Enterprise Scala with functional programming, Apache Pekko/Akka actors, Apache Spark, ZIO/Cats Effect, reactive architectures
- **flutter-expert**: Flutter development, Dart, state management, animations, cross-platform deployment
- **unity-developer**: Unity game development, C# scripting, performance optimization
- **minecraft-bukkit-pro**: Minecraft plugin development, event systems, server-side features
- **ios-developer**: Native iOS development with Swift/SwiftUI
- **sql-pro**: Database queries, schema design, query optimization
- **mobile-developer**: React Native/Flutter development
- **haskell-pro**: Pure functional programming, advanced type systems
- **arm-cortex-expert**: Embedded systems, ARM Cortex-M, RTOS

### 🛠️ Operations & Maintenance
- **devops-troubleshooter**: Production issues, deployment problems
- **incident-responder**: Critical outages requiring immediate response
- **database-optimizer**: Query performance, indexing strategies
- **database-admin**: Backup strategies, replication, user management, disaster recovery
- **terraform-specialist**: Infrastructure as Code, Terraform modules, state management
- **network-engineer**: Network connectivity, load balancers, SSL/TLS, DNS debugging
- **service-mesh-expert**: Istio, Linkerd, Envoy, mTLS, traffic management
- **observability-engineer**: OpenTelemetry, metrics, logging, distributed tracing

### 📊 Analysis & Optimization
- **performance-engineer**: Application bottlenecks, optimization
- **security-auditor**: Vulnerability scanning, compliance checks
- **data-scientist**: Data analysis, insights, reporting
- **mlops-engineer**: ML infrastructure, experiment tracking, model registries, pipeline automation
- **vector-database-engineer**: Pinecone, Qdrant, Weaviate, semantic search, RAG systems

### 🧪 Quality Assurance
- **code-reviewer**: Code quality, configuration security, production reliability
- **test-automator**: Test strategy, test suite creation
- **debugger**: Bug investigation, error resolution
- **error-detective**: Log analysis, error pattern recognition, root cause analysis
- **search-specialist**: Deep web research, competitive analysis, fact-checking
- **tdd-orchestrator**: Test-Driven Development, testing strategy, test pyramid design

### 📚 Documentation & Architecture
- **api-documenter**: AI-powered documentation with modern dev portal architecture
- **docs-architect**: Comprehensive technical documentation with automated generation
- **reference-builder**: Exhaustive API references with interactive examples
- **tutorial-engineer**: AI-enhanced educational content with progressive learning
- **architect-reviewer**: Master software architecture with modern patterns
- **graphql-architect**: Modern GraphQL federation and performance optimization

### 💼 Business & Specialized Domains
- **business-analyst**: Advanced BI with AI-powered analytics and strategic frameworks
- **hr-pro**: Modern HR technology with talent management and compliance
- **legal-advisor**: Legal technology with contract analysis and compliance automation
- **content-marketer**: AI-powered content marketing with omnichannel distribution
- **sales-automator**: Modern sales automation with CRM integration
- **customer-support**: AI-powered support with conversational automation
- **quant-analyst**: Advanced quantitative finance with algorithmic trading
- **risk-manager**: Comprehensive risk management with modern analytics
- **payment-integration**: Modern payment systems and fintech integration
- **legacy-modernizer**: Strategic legacy transformation with cloud migration
- **blockchain-developer**: Smart contracts, DeFi, Web3, Solidity, blockchain security

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Learn More

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
