# Agent Reference

Complete reference for all **100 specialized AI agents** organized by category with model assignments.

## Agent Categories

### Architecture & System Design

#### Core Architecture

| Agent                                                                                         | Model  | Description                                                            |
| --------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------- |
| [backend-architect](../plugins/backend-development/agents/backend-architect.md)               | opus   | RESTful API design, microservice boundaries, database schemas          |
| [frontend-developer](../plugins/multi-platform-apps/agents/frontend-developer.md)             | sonnet | React components, responsive layouts, client-side state management     |
| [graphql-architect](../plugins/backend-development/agents/graphql-architect.md)               | opus   | GraphQL schemas, resolvers, federation architecture                    |
| [architect-reviewer](../plugins/comprehensive-review/agents/architect-review.md)              | opus   | Architectural consistency analysis and pattern validation              |
| [cloud-architect](../plugins/cloud-infrastructure/agents/cloud-architect.md)                  | opus   | AWS/Azure/GCP infrastructure design and cost optimization              |
| [hybrid-cloud-architect](../plugins/cloud-infrastructure/agents/hybrid-cloud-architect.md)    | opus   | Multi-cloud strategies across cloud and on-premises environments       |
| [kubernetes-architect](../plugins/kubernetes-operations/agents/kubernetes-architect.md)       | opus   | Cloud-native infrastructure with Kubernetes and GitOps                 |
| [service-mesh-expert](../plugins/cloud-infrastructure/agents/service-mesh-expert.md)          | opus   | Istio/Linkerd service mesh architecture, mTLS, and traffic management  |
| [event-sourcing-architect](../plugins/backend-development/agents/event-sourcing-architect.md) | opus   | Event sourcing, CQRS patterns, event stores, and saga orchestration    |
| [monorepo-architect](../plugins/developer-essentials/agents/monorepo-architect.md)            | opus   | Monorepo tooling with Nx, Turborepo, Bazel, and workspace optimization |

#### UI/UX & Mobile

| Agent                                                                                    | Model  | Description                                             |
| ---------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [ui-designer](../plugins/ui-design/agents/ui-designer.md)                                | opus   | UI/UX design for mobile and web with modern patterns    |
| [accessibility-expert](../plugins/ui-design/agents/accessibility-expert.md)              | opus   | WCAG compliance, accessibility audits, inclusive design |
| [design-system-architect](../plugins/ui-design/agents/design-system-architect.md)        | opus   | Design tokens, component libraries, theming systems     |
| [ui-ux-designer](../plugins/multi-platform-apps/agents/ui-ux-designer.md)                | sonnet | Interface design, wireframes, design systems            |
| [ui-visual-validator](../plugins/accessibility-compliance/agents/ui-visual-validator.md) | sonnet | Visual regression testing and UI verification           |
| [mobile-developer](../plugins/multi-platform-apps/agents/mobile-developer.md)            | sonnet | React Native and Flutter application development        |
| [ios-developer](../plugins/multi-platform-apps/agents/ios-developer.md)                  | sonnet | Native iOS development with Swift/SwiftUI               |
| [flutter-expert](../plugins/multi-platform-apps/agents/flutter-expert.md)                | sonnet | Advanced Flutter development with state management      |

### Programming Languages

#### Systems & Low-Level

| Agent                                                             | Model  | Description                                                 |
| ----------------------------------------------------------------- | ------ | ----------------------------------------------------------- |
| [c-pro](../plugins/systems-programming/agents/c-pro.md)           | sonnet | System programming with memory management and OS interfaces |
| [cpp-pro](../plugins/systems-programming/agents/cpp-pro.md)       | sonnet | Modern C++ with RAII, smart pointers, STL algorithms        |
| [rust-pro](../plugins/systems-programming/agents/rust-pro.md)     | sonnet | Memory-safe systems programming with ownership patterns     |
| [golang-pro](../plugins/systems-programming/agents/golang-pro.md) | sonnet | Concurrent programming with goroutines and channels         |

#### Web & Application

| Agent                                                                               | Model  | Description                                                                       |
| ----------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------- |
| [javascript-pro](../plugins/javascript-typescript/agents/javascript-pro.md)         | sonnet | Modern JavaScript with ES6+, async patterns, Node.js                              |
| [typescript-pro](../plugins/javascript-typescript/agents/typescript-pro.md)         | sonnet | Advanced TypeScript with type systems and generics                                |
| [python-pro](../plugins/python-development/agents/python-pro.md)                    | sonnet | Python development with advanced features and optimization                        |
| [temporal-python-pro](../plugins/backend-development/agents/temporal-python-pro.md) | sonnet | Temporal workflow orchestration with Python SDK, durable workflows, saga patterns |
| [ruby-pro](../plugins/web-scripting/agents/ruby-pro.md)                             | sonnet | Ruby with metaprogramming, Rails patterns, gem development                        |
| [php-pro](../plugins/web-scripting/agents/php-pro.md)                               | sonnet | Modern PHP with frameworks and performance optimization                           |

#### Enterprise & JVM

| Agent                                                       | Model  | Description                                                          |
| ----------------------------------------------------------- | ------ | -------------------------------------------------------------------- |
| [java-pro](../plugins/jvm-languages/agents/java-pro.md)     | sonnet | Modern Java with streams, concurrency, JVM optimization              |
| [scala-pro](../plugins/jvm-languages/agents/scala-pro.md)   | sonnet | Enterprise Scala with functional programming and distributed systems |
| [csharp-pro](../plugins/jvm-languages/agents/csharp-pro.md) | sonnet | C# development with .NET frameworks and patterns                     |

#### Specialized Platforms

| Agent                                                                              | Model  | Description                                                                               |
| ---------------------------------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------- |
| [elixir-pro](../plugins/functional-programming/agents/elixir-pro.md)               | sonnet | Elixir with OTP patterns and Phoenix frameworks                                           |
| [django-pro](../plugins/api-scaffolding/agents/django-pro.md)                      | sonnet | Django development with ORM and async views                                               |
| [fastapi-pro](../plugins/api-scaffolding/agents/fastapi-pro.md)                    | sonnet | FastAPI with async patterns and Pydantic                                                  |
| [haskell-pro](../plugins/functional-programming/agents/haskell-pro.md)             | sonnet | Strongly typed functional programming with purity, advanced type systems, and concurrency |
| [unity-developer](../plugins/game-development/agents/unity-developer.md)           | sonnet | Unity game development and optimization                                                   |
| [minecraft-bukkit-pro](../plugins/game-development/agents/minecraft-bukkit-pro.md) | sonnet | Minecraft server plugin development                                                       |
| [sql-pro](../plugins/database-design/agents/sql-pro.md)                            | sonnet | Complex SQL queries and database optimization                                             |

### Infrastructure & Operations

#### DevOps & Deployment

| Agent                                                                                  | Model  | Description                                                        |
| -------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------ |
| [devops-troubleshooter](../plugins/incident-response/agents/devops-troubleshooter.md)  | sonnet | Production debugging, log analysis, deployment troubleshooting     |
| [deployment-engineer](../plugins/cloud-infrastructure/agents/deployment-engineer.md)   | sonnet | CI/CD pipelines, containerization, cloud deployments               |
| [terraform-specialist](../plugins/cloud-infrastructure/agents/terraform-specialist.md) | sonnet | Infrastructure as Code with Terraform modules and state management |
| [dx-optimizer](../plugins/team-collaboration/agents/dx-optimizer.md)                   | sonnet | Developer experience optimization and tooling improvements         |

#### Database Management

| Agent                                                                                  | Model  | Description                                                         |
| -------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------- |
| [database-optimizer](../plugins/observability-monitoring/agents/database-optimizer.md) | sonnet | Query optimization, index design, migration strategies              |
| [database-admin](../plugins/database-migrations/agents/database-admin.md)              | sonnet | Database operations, backup, replication, monitoring                |
| [database-architect](../plugins/database-design/agents/database-architect.md)          | opus   | Database design from scratch, technology selection, schema modeling |

#### Incident Response & Network

| Agent                                                                              | Model  | Description                                         |
| ---------------------------------------------------------------------------------- | ------ | --------------------------------------------------- |
| [incident-responder](../plugins/incident-response/agents/incident-responder.md)    | opus   | Production incident management and resolution       |
| [network-engineer](../plugins/observability-monitoring/agents/network-engineer.md) | sonnet | Network debugging, load balancing, traffic analysis |

#### Project Management

| Agent                                                             | Model | Description                                                                          |
| ----------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------ |
| [conductor-validator](../conductor/agents/conductor-validator.md) | opus  | Validates Conductor project artifacts for completeness, consistency, and correctness |

### Quality Assurance & Security

#### Code Quality & Review

| Agent                                                                                            | Model | Description                                                     |
| ------------------------------------------------------------------------------------------------ | ----- | --------------------------------------------------------------- |
| [code-reviewer](../plugins/comprehensive-review/agents/code-reviewer.md)                         | opus  | Code review with security focus and production reliability      |
| [security-auditor](../plugins/comprehensive-review/agents/security-auditor.md)                   | opus  | Vulnerability assessment and OWASP compliance                   |
| [backend-security-coder](../plugins/data-validation-suite/agents/backend-security-coder.md)      | opus  | Secure backend coding practices, API security implementation    |
| [frontend-security-coder](../plugins/frontend-mobile-security/agents/frontend-security-coder.md) | opus  | XSS prevention, CSP implementation, client-side security        |
| [mobile-security-coder](../plugins/frontend-mobile-security/agents/mobile-security-coder.md)     | opus  | Mobile security patterns, WebView security, biometric auth      |
| [threat-modeling-expert](../plugins/security-scanning/agents/threat-modeling-expert.md)          | opus  | STRIDE threat modeling, attack trees, and security requirements |

#### Testing & Debugging

| Agent                                                                         | Model  | Description                                                |
| ----------------------------------------------------------------------------- | ------ | ---------------------------------------------------------- |
| [test-automator](../plugins/codebase-cleanup/agents/test-automator.md)        | sonnet | Comprehensive test suite creation (unit, integration, e2e) |
| [tdd-orchestrator](../plugins/backend-development/agents/tdd-orchestrator.md) | sonnet | Test-Driven Development methodology guidance               |
| [debugger](../plugins/error-debugging/agents/debugger.md)                     | sonnet | Error resolution and test failure analysis                 |
| [error-detective](../plugins/error-debugging/agents/error-detective.md)       | sonnet | Log analysis and error pattern recognition                 |

#### Performance & Observability

| Agent                                                                                          | Model | Description                                                    |
| ---------------------------------------------------------------------------------------------- | ----- | -------------------------------------------------------------- |
| [performance-engineer](../plugins/observability-monitoring/agents/performance-engineer.md)     | opus  | Application profiling and optimization                         |
| [observability-engineer](../plugins/observability-monitoring/agents/observability-engineer.md) | opus  | Production monitoring, distributed tracing, SLI/SLO management |
| [search-specialist](../plugins/content-marketing/agents/search-specialist.md)                  | haiku | Advanced web research and information synthesis                |

### Data & AI

#### Data Engineering & Analytics

| Agent                                                                      | Model  | Description                                             |
| -------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [data-scientist](../plugins/machine-learning-ops/agents/data-scientist.md) | opus   | Data analysis, SQL queries, BigQuery operations         |
| [data-engineer](../plugins/data-engineering/agents/data-engineer.md)       | sonnet | ETL pipelines, data warehouses, streaming architectures |

#### Machine Learning & AI

| Agent                                                                                         | Model | Description                                                           |
| --------------------------------------------------------------------------------------------- | ----- | --------------------------------------------------------------------- |
| [ai-engineer](../plugins/llm-application-dev/agents/ai-engineer.md)                           | opus  | LLM applications, RAG systems, prompt pipelines                       |
| [ml-engineer](../plugins/machine-learning-ops/agents/ml-engineer.md)                          | opus  | ML pipelines, model serving, feature engineering                      |
| [mlops-engineer](../plugins/machine-learning-ops/agents/mlops-engineer.md)                    | opus  | ML infrastructure, experiment tracking, model registries              |
| [prompt-engineer](../plugins/llm-application-dev/agents/prompt-engineer.md)                   | opus  | LLM prompt optimization and engineering                               |
| [vector-database-engineer](../plugins/llm-application-dev/agents/vector-database-engineer.md) | opus  | Vector databases, embeddings, similarity search, and hybrid retrieval |

### Documentation & Technical Writing

| Agent                                                                                | Model  | Description                                                           |
| ------------------------------------------------------------------------------------ | ------ | --------------------------------------------------------------------- |
| [docs-architect](../plugins/code-documentation/agents/docs-architect.md)             | opus   | Comprehensive technical documentation generation                      |
| [api-documenter](../plugins/api-testing-observability/agents/api-documenter.md)      | sonnet | OpenAPI/Swagger specifications and developer docs                     |
| [reference-builder](../plugins/documentation-generation/agents/reference-builder.md) | haiku  | Technical references and API documentation                            |
| [tutorial-engineer](../plugins/code-documentation/agents/tutorial-engineer.md)       | sonnet | Step-by-step tutorials and educational content                        |
| [mermaid-expert](../plugins/documentation-generation/agents/mermaid-expert.md)       | sonnet | Diagram creation (flowcharts, sequences, ERDs)                        |
| [c4-code](../plugins/c4-architecture/agents/c4-code.md)                              | haiku  | C4 Code-level documentation with function signatures and dependencies |
| [c4-component](../plugins/c4-architecture/agents/c4-component.md)                    | sonnet | C4 Component-level architecture synthesis and documentation           |
| [c4-container](../plugins/c4-architecture/agents/c4-container.md)                    | sonnet | C4 Container-level architecture with API documentation                |
| [c4-context](../plugins/c4-architecture/agents/c4-context.md)                        | sonnet | C4 Context-level system documentation with personas and user journeys |

### Business & Operations

#### Business Analysis & Finance

| Agent                                                                        | Model  | Description                                             |
| ---------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [business-analyst](../plugins/business-analytics/agents/business-analyst.md) | sonnet | Metrics analysis, reporting, KPI tracking               |
| [quant-analyst](../plugins/quantitative-trading/agents/quant-analyst.md)     | opus   | Financial modeling, trading strategies, market analysis |
| [risk-manager](../plugins/quantitative-trading/agents/risk-manager.md)       | sonnet | Portfolio risk monitoring and management                |

#### Marketing & Sales

| Agent                                                                             | Model  | Description                                  |
| --------------------------------------------------------------------------------- | ------ | -------------------------------------------- |
| [content-marketer](../plugins/content-marketing/agents/content-marketer.md)       | sonnet | Blog posts, social media, email campaigns    |
| [sales-automator](../plugins/customer-sales-automation/agents/sales-automator.md) | haiku  | Cold emails, follow-ups, proposal generation |

#### Support & Legal

| Agent                                                                               | Model  | Description                                             |
| ----------------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [customer-support](../plugins/customer-sales-automation/agents/customer-support.md) | sonnet | Support tickets, FAQ responses, customer communication  |
| [hr-pro](../plugins/hr-legal-compliance/agents/hr-pro.md)                           | opus   | HR operations, policies, employee relations             |
| [legal-advisor](../plugins/hr-legal-compliance/agents/legal-advisor.md)             | opus   | Privacy policies, terms of service, legal documentation |

### SEO & Content Optimization

| Agent                                                                                                     | Model  | Description                                          |
| --------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------- |
| [seo-content-auditor](../plugins/seo-content-creation/agents/seo-content-auditor.md)                      | sonnet | Content quality analysis, E-E-A-T signals assessment |
| [seo-meta-optimizer](../plugins/seo-technical-optimization/agents/seo-meta-optimizer.md)                  | haiku  | Meta title and description optimization              |
| [seo-keyword-strategist](../plugins/seo-technical-optimization/agents/seo-keyword-strategist.md)          | haiku  | Keyword analysis and semantic variations             |
| [seo-structure-architect](../plugins/seo-technical-optimization/agents/seo-structure-architect.md)        | haiku  | Content structure and schema markup                  |
| [seo-snippet-hunter](../plugins/seo-technical-optimization/agents/seo-snippet-hunter.md)                  | haiku  | Featured snippet formatting                          |
| [seo-content-refresher](../plugins/seo-analysis-monitoring/agents/seo-content-refresher.md)               | haiku  | Content freshness analysis                           |
| [seo-cannibalization-detector](../plugins/seo-analysis-monitoring/agents/seo-cannibalization-detector.md) | haiku  | Keyword overlap detection                            |
| [seo-authority-builder](../plugins/seo-analysis-monitoring/agents/seo-authority-builder.md)               | sonnet | E-E-A-T signal analysis                              |
| [seo-content-writer](../plugins/seo-content-creation/agents/seo-content-writer.md)                        | sonnet | SEO-optimized content creation                       |
| [seo-content-planner](../plugins/seo-content-creation/agents/seo-content-planner.md)                      | haiku  | Content planning and topic clusters                  |

### Specialized Domains

| Agent                                                                                   | Model  | Description                                             |
| --------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------- |
| [arm-cortex-expert](../plugins/arm-cortex-microcontrollers/agents/arm-cortex-expert.md) | sonnet | ARM Cortex-M firmware and peripheral driver development |
| [blockchain-developer](../plugins/blockchain-web3/agents/blockchain-developer.md)       | sonnet | Web3 apps, smart contracts, DeFi protocols              |
| [payment-integration](../plugins/payment-processing/agents/payment-integration.md)      | sonnet | Payment processor integration (Stripe, PayPal)          |
| [legacy-modernizer](../plugins/framework-migration/agents/legacy-modernizer.md)         | sonnet | Legacy code refactoring and modernization               |
| [context-manager](../plugins/agent-orchestration/agents/context-manager.md)             | haiku  | Multi-agent context management                          |

## Model Configuration

Agents are assigned to specific Claude models based on task complexity and computational requirements.

### Model Distribution Summary

| Model  | Agent Count | Use Case                                                        |
| ------ | ----------- | --------------------------------------------------------------- |
| Opus   | 42          | Critical architecture, security, code review, production coding |
| Sonnet | 39          | Complex tasks, support with intelligence                        |
| Haiku  | 18          | Fast operational tasks                                          |

### Model Selection Criteria

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

## Agent Invocation

### Natural Language

Agents can be invoked through natural language when you need Claude to reason about which specialist to use:

```
"Use backend-architect to design the authentication API"
"Have security-auditor scan for OWASP vulnerabilities"
"Get performance-engineer to optimize this database query"
```

### Slash Commands

Many agents are accessible through plugin slash commands for direct invocation:

```bash
/backend-development:feature-development user authentication
/security-scanning:security-sast
/incident-response:smart-fix "memory leak in payment service"
```

## Contributing

To add a new agent:

1. Create `plugins/{plugin-name}/agents/{agent-name}.md`
2. Add frontmatter with name, description, and model assignment
3. Write comprehensive system prompt
4. Update plugin definition in `.claude-plugin/marketplace.json`

See [Contributing Guide](../CONTRIBUTING.md) for details.
