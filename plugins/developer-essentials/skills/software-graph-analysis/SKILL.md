---
name: software-graph-analysis
description: Use when repository understanding should come from Ontoly's deterministic Software Graph, MCP capabilities, validation reports, request tracing, dependency impact analysis, architecture review, or configuration lookup before source-file search.
---

# Software Graph Analysis

Use Ontoly's Software Graph as deterministic evidence for codebase understanding before falling back to source-file search.

## When to Use This Skill

- The repository contains `.ontoly/`, `SoftwareGraph.json`, diagnostics, graph validation reports, or Ontoly MCP configuration.
- The user asks for architecture review, request tracing, dependency impact, framework analysis, configuration lookup, route ownership, service ownership, or codebase onboarding.
- The user mentions Ontoly, Software Graph, semantic graph, graph hash, graph validation, or MCP graph capabilities.
- A refactor needs evidence about what depends on a package, module, service, route, or environment variable.

## Core Workflow

1. **Check graph availability.** Look for `.ontoly/`, `SoftwareGraph.json`, `diagnostics.json`, validation reports, semantic evaluation output, graph hash, or MCP configuration.
2. **Build when appropriate.** If no graph exists and local analysis is acceptable, run `ontoly build .`.
3. **Validate graph health.** Review diagnostics, semantic coverage, trust or quality score, framework detection, graph hash, repository path, and generation timestamp.
4. **Query Ontoly first.** Prefer Ontoly CLI or MCP capabilities for graph-answerable questions before searching source files.
5. **Answer with evidence.** Cite node IDs, edge types, file paths, source locations, diagnostics, and confidence derived from graph evidence.
6. **Fallback narrowly.** Search files only when the graph is missing, stale, incomplete, ambiguous, or the user explicitly requests source verification.

## Capability Map

| User Intent | Ontoly Capability |
| --- | --- |
| Repository architecture | `ExplainArchitecture` |
| Dependency tree | `FindDependencies` |
| Refactor blast radius | `ImpactAnalysis` |
| Request or route flow | `TraceExecution` |
| Configuration usage | `FindConfigurationUsage` |
| Framework concepts | `FrameworkReport` |
| Dead or unreachable code | `FindDeadCode` |

## Evidence Rules

- High confidence requires a matching node, relationship edge, and source location.
- Medium confidence is acceptable when the matching node exists but one relationship or source location is incomplete.
- Low confidence means only partial graph evidence exists and source verification may be needed.
- `NOT_FOUND` is better than an invented graph fact.

## Response Pattern

```text
AuthController handles authentication.

Evidence:
- node: class:src/auth/auth.controller.ts:AuthController
- route edges: HANDLES POST /login and POST /logout
- dependency edges: USES AuthService and JwtService

Confidence: high, because controller, route, and dependency edges have source locations.
```

## Avoid

- Searching the repository first when graph evidence exists.
- Treating graph size or node count as semantic correctness.
- Guessing confidence without graph evidence.
- Hiding stale graph or validation warnings.
- Inventing missing services, routes, modules, dependencies, or configuration usage.

