---
description: "Orchestrate legacy system modernization using the strangler fig pattern with gradual component replacement"
argument-hint: "<legacy codebase path or description> [--strategy parallel-systems|big-bang|by-feature|database-first|api-first]"
---

# Legacy Code Modernization Workflow

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.legacy-modernize/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan — execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.legacy-modernize/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress legacy modernization session:
  Target: [target from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.legacy-modernize/` directory and `state.json`:

```json
{
  "target": "$ARGUMENTS",
  "status": "in_progress",
  "strategy": "parallel-systems",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--strategy` flag. Use `parallel-systems` as default if not specified.

### 3. Parse target description

Extract the target description from `$ARGUMENTS` (everything before the flags). This is referenced as `$TARGET` in prompts below.

---

## Phase 1: Legacy Assessment and Risk Analysis (Steps 1–3)

### Step 1: Comprehensive Legacy System Analysis

Use the Task tool with subagent_type="legacy-modernizer":

```
Task:
  subagent_type: "legacy-modernizer"
  description: "Analyze legacy codebase for modernization readiness"
  prompt: |
    Analyze the legacy codebase at $TARGET. Document a technical debt inventory including:
    - Outdated dependencies and deprecated APIs
    - Security vulnerabilities and performance bottlenecks
    - Architectural anti-patterns

    Generate a modernization readiness report with:
    - Component complexity scores (1-10)
    - Dependency mapping between modules
    - Database coupling analysis
    - Quick wins vs complex refactoring targets

    Write your complete assessment as a single markdown document.
```

Save the agent's output to `.legacy-modernize/01-legacy-assessment.md`.

Update `state.json`: set `current_step` to 2, add `"01-legacy-assessment.md"` to `files_created`, add step 1 to `completed_steps`.

### Step 2: Dependency and Integration Mapping

Read `.legacy-modernize/01-legacy-assessment.md` to load assessment context.

Use the Task tool with subagent_type="architect-review":

```
Task:
  subagent_type: "architect-review"
  description: "Create dependency graph and integration point catalog"
  prompt: |
    Based on the legacy assessment report below, create a comprehensive dependency graph.

    ## Legacy Assessment
    [Insert full contents of .legacy-modernize/01-legacy-assessment.md]

    ## Deliverables
    1. Internal module dependencies
    2. External service integrations
    3. Shared database schemas and cross-system data flows
    4. Integration points requiring facade patterns or adapter layers during migration
    5. Circular dependencies and tight coupling that need resolution

    Write your complete dependency analysis as a single markdown document.
```

Save the agent's output to `.legacy-modernize/02-dependency-map.md`.

Update `state.json`: set `current_step` to 3, add step 2 to `completed_steps`.

### Step 3: Business Impact and Risk Assessment

Read `.legacy-modernize/01-legacy-assessment.md` and `.legacy-modernize/02-dependency-map.md`.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Evaluate business impact and create migration roadmap"
  prompt: |
    You are a business analyst specializing in technology transformation and risk assessment.

    Evaluate the business impact of modernizing each component identified in the assessment and dependency analysis below.

    ## Legacy Assessment
    [Insert contents of .legacy-modernize/01-legacy-assessment.md]

    ## Dependency Map
    [Insert contents of .legacy-modernize/02-dependency-map.md]

    ## Deliverables
    1. Risk assessment matrix considering: business criticality (revenue impact), user traffic patterns, data sensitivity, regulatory requirements, and fallback complexity
    2. Prioritized components using weighted scoring: (Business Value x 0.4) + (Technical Risk x 0.3) + (Quick Win Potential x 0.3)
    3. Rollback strategies for each component
    4. Recommended migration order

    Write your complete business impact analysis as a single markdown document.
```

Save the agent's output to `.legacy-modernize/03-business-impact.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 3 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — User Approval Required

You MUST stop here and present the assessment for review.

Display a summary of findings from the Phase 1 output files (key components, risk levels, recommended migration order) and ask:

```
Legacy assessment and risk analysis complete. Please review:
- .legacy-modernize/01-legacy-assessment.md
- .legacy-modernize/02-dependency-map.md
- .legacy-modernize/03-business-impact.md

1. Approve — proceed to test coverage establishment
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1. If they select option 2, revise and re-checkpoint. If option 3, update `state.json` status and stop.

---

## Phase 2: Test Coverage Establishment (Steps 4–6)

### Step 4: Legacy Code Test Coverage Analysis

Read `.legacy-modernize/01-legacy-assessment.md` and `.legacy-modernize/03-business-impact.md`.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Analyze and establish test coverage for legacy components"
  prompt: |
    You are a test automation engineer specializing in legacy system characterization testing.

    Analyze existing test coverage for legacy components at $TARGET.

    ## Legacy Assessment
    [Insert contents of .legacy-modernize/01-legacy-assessment.md]

    ## Migration Priorities
    [Insert contents of .legacy-modernize/03-business-impact.md]

    ## Instructions
    1. Use coverage tools to identify untested code paths, missing integration tests, and absent end-to-end scenarios
    2. For components with <40% coverage, generate characterization tests that capture current behavior without modifying functionality
    3. Create a test harness for safe refactoring
    4. Follow existing test patterns and frameworks in the project

    Write all test files and report what was created. Provide a coverage summary.
```

Save the agent's output to `.legacy-modernize/04-test-coverage.md`.

Update `state.json`: set `current_step` to 5, add step 4 to `completed_steps`.

### Step 5: Contract Testing Implementation

Read `.legacy-modernize/02-dependency-map.md` and `.legacy-modernize/04-test-coverage.md`.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Implement contract tests for integration points"
  prompt: |
    You are a test automation engineer specializing in contract testing and API verification.

    Implement contract tests for all integration points identified in the dependency mapping.

    ## Dependency Map
    [Insert contents of .legacy-modernize/02-dependency-map.md]

    ## Existing Test Coverage
    [Insert contents of .legacy-modernize/04-test-coverage.md]

    ## Instructions
    1. Create consumer-driven contracts for APIs, message queue interactions, and database schemas
    2. Set up contract verification in CI/CD pipeline
    3. Generate performance baselines for response times and throughput to validate modernized components maintain SLAs
    4. Follow existing test patterns and frameworks in the project

    Write all test files and report what was created.
```

Save the agent's output to `.legacy-modernize/05-contract-tests.md`.

Update `state.json`: set `current_step` to 6, add step 5 to `completed_steps`.

### Step 6: Test Data Management Strategy

Read `.legacy-modernize/02-dependency-map.md` and `.legacy-modernize/04-test-coverage.md`.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Design test data management for parallel system operation"
  prompt: |
    You are a data engineer specializing in test data management and data pipeline design.

    Design a test data management strategy for parallel system operation during migration.

    ## Dependency Map
    [Insert contents of .legacy-modernize/02-dependency-map.md]

    ## Test Coverage
    [Insert contents of .legacy-modernize/04-test-coverage.md]

    ## Instructions
    1. Create data generation scripts for edge cases
    2. Implement data masking for sensitive information
    3. Establish test database refresh procedures
    4. Set up monitoring for data consistency between legacy and modernized components during migration

    Write all configuration and script files. Report what was created.
```

Save the agent's output to `.legacy-modernize/06-test-data.md`.

Update `state.json`: set `current_step` to "checkpoint-2", add step 6 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — User Approval Required

Display a summary of test coverage establishment from Phase 2 output files and ask:

```
Test coverage establishment complete. Please review:
- .legacy-modernize/04-test-coverage.md
- .legacy-modernize/05-contract-tests.md
- .legacy-modernize/06-test-data.md

1. Approve — proceed to incremental migration implementation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 3 until the user approves.

---

## Phase 3: Incremental Migration Implementation (Steps 7–9)

### Step 7: Strangler Fig Infrastructure Setup

Read `.legacy-modernize/02-dependency-map.md` and `.legacy-modernize/03-business-impact.md`.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Implement strangler fig infrastructure with API gateway and feature flags"
  prompt: |
    You are a backend architect specializing in distributed systems and migration infrastructure.

    Implement strangler fig infrastructure for the legacy modernization.

    ## Dependency Map
    [Insert contents of .legacy-modernize/02-dependency-map.md]

    ## Migration Priorities
    [Insert contents of .legacy-modernize/03-business-impact.md]

    ## Instructions
    1. Configure API gateway for traffic routing between legacy and modern components
    2. Set up feature flags for gradual rollout using environment variables or feature management service
    3. Implement proxy layer with request routing rules based on URL patterns, headers, or user segments
    4. Implement circuit breakers and fallback mechanisms for resilience
    5. Create observability dashboard for dual-system monitoring
    6. Follow existing infrastructure patterns in the project

    Write all configuration files. Report what was created/modified.
```

Save the agent's output to `.legacy-modernize/07-infrastructure.md`.

Update `state.json`: set `current_step` to 8, add step 7 to `completed_steps`.

### Step 8: Component Modernization — First Wave

Read `.legacy-modernize/01-legacy-assessment.md`, `.legacy-modernize/03-business-impact.md`, `.legacy-modernize/04-test-coverage.md`, and `.legacy-modernize/07-infrastructure.md`.

Detect the target language/stack from the legacy assessment. Use the Task tool with subagent_type="general-purpose", providing role context matching the target stack:

```
Task:
  subagent_type: "general-purpose"
  description: "Modernize first-wave components from legacy assessment"
  prompt: |
    You are an expert [DETECTED LANGUAGE] developer specializing in legacy code modernization
    and migration to modern frameworks and patterns.

    Modernize first-wave components (quick wins identified in assessment).

    ## Legacy Assessment
    [Insert contents of .legacy-modernize/01-legacy-assessment.md]

    ## Migration Priorities
    [Insert contents of .legacy-modernize/03-business-impact.md]

    ## Test Coverage
    [Insert contents of .legacy-modernize/04-test-coverage.md]

    ## Infrastructure
    [Insert contents of .legacy-modernize/07-infrastructure.md]

    ## Instructions
    For each component in the first wave:
    1. Extract business logic from legacy code
    2. Implement using modern patterns (dependency injection, SOLID principles)
    3. Ensure backward compatibility through adapter patterns
    4. Maintain data consistency with event sourcing or dual writes
    5. Follow 12-factor app principles
    6. Run characterization tests to verify preserved behavior

    Write all code files. Report what files were created/modified.
```

**Note:** Replace `[DETECTED LANGUAGE]` with the actual language detected from the legacy assessment (e.g., "Python", "TypeScript", "Go", "Rust", "Java"). If the codebase is polyglot, launch parallel agents for each language.

Save the agent's output to `.legacy-modernize/08-first-wave.md`.

Update `state.json`: set `current_step` to 9, add step 8 to `completed_steps`.

### Step 9: Security Hardening

Read `.legacy-modernize/08-first-wave.md`.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Security audit and hardening of modernized components"
  prompt: |
    You are a security engineer specializing in application security auditing,
    OWASP compliance, and secure coding practices.

    Audit modernized components for security vulnerabilities and implement hardening.

    ## Modernized Components
    [Insert contents of .legacy-modernize/08-first-wave.md]

    ## Instructions
    1. Implement OAuth 2.0/JWT authentication where applicable
    2. Add role-based access control
    3. Implement input validation and sanitization
    4. Verify SQL injection prevention and XSS protection
    5. Configure secrets management
    6. Verify OWASP Top 10 compliance
    7. Configure security headers and implement rate limiting

    Provide a security audit report with findings by severity (Critical/High/Medium/Low)
    and list all hardening changes made. Write all code changes.
```

Save the agent's output to `.legacy-modernize/09-security.md`.

Update `state.json`: set `current_step` to "checkpoint-3", add step 9 to `completed_steps`.

---

## PHASE CHECKPOINT 3 — User Approval Required

Display a summary of migration implementation from Phase 3 output files and ask:

```
Incremental migration implementation complete. Please review:
- .legacy-modernize/07-infrastructure.md
- .legacy-modernize/08-first-wave.md
- .legacy-modernize/09-security.md

Security findings: [summarize Critical/High/Medium counts from 09-security.md]

1. Approve — proceed to performance validation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 4 until the user approves.

---

## Phase 4: Performance Validation and Rollout (Steps 10–11)

### Step 10: Performance Testing and Optimization

Read `.legacy-modernize/05-contract-tests.md` and `.legacy-modernize/08-first-wave.md`.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Performance testing of modernized vs legacy components"
  prompt: |
    You are a performance engineer specializing in load testing, benchmarking,
    and application performance optimization.

    Conduct performance testing comparing legacy vs modernized components.

    ## Contract Tests and Baselines
    [Insert contents of .legacy-modernize/05-contract-tests.md]

    ## Modernized Components
    [Insert contents of .legacy-modernize/08-first-wave.md]

    ## Instructions
    1. Run load tests simulating production traffic patterns
    2. Measure response times, throughput, and resource utilization
    3. Identify performance regressions and optimize: database queries with indexing, caching strategies, connection pooling, and async processing
    4. Validate against SLA requirements (P95 latency within 110% of baseline)

    Provide performance test results with comparison tables and optimization recommendations.
```

Save the agent's output to `.legacy-modernize/10-performance.md`.

Update `state.json`: set `current_step` to 11, add step 10 to `completed_steps`.

### Step 11: Progressive Rollout Plan

Read `.legacy-modernize/07-infrastructure.md` and `.legacy-modernize/10-performance.md`.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Create progressive rollout strategy with automated safeguards"
  prompt: |
    You are a deployment engineer specializing in progressive delivery,
    feature flag management, and production rollout strategies.

    Implement a progressive rollout strategy for the modernized components.

    ## Infrastructure
    [Insert contents of .legacy-modernize/07-infrastructure.md]

    ## Performance Results
    [Insert contents of .legacy-modernize/10-performance.md]

    ## Instructions
    1. Configure feature flags for traffic shifting: 5% -> 25% -> 50% -> 100%
    2. Define automatic rollback triggers: error rate >1%, latency >2x baseline, or business metric degradation
    3. Set 24-hour observation periods between each stage
    4. Create runbook for the complete traffic shifting process
    5. Include monitoring queries and dashboards for each stage

    Write all configuration files and the rollout runbook.
```

Save the agent's output to `.legacy-modernize/11-rollout.md`.

Update `state.json`: set `current_step` to "checkpoint-4", add step 11 to `completed_steps`.

---

## PHASE CHECKPOINT 4 — User Approval Required

Display a summary of performance and rollout plans and ask:

```
Performance validation and rollout planning complete. Please review:
- .legacy-modernize/10-performance.md
- .legacy-modernize/11-rollout.md

Performance: [summarize key metrics from 10-performance.md]

1. Approve — proceed to decommissioning and documentation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 5 until the user approves.

---

## Phase 5: Migration Completion and Documentation (Steps 12–13)

### Step 12: Legacy Component Decommissioning

Read `.legacy-modernize/01-legacy-assessment.md`, `.legacy-modernize/08-first-wave.md`, and `.legacy-modernize/11-rollout.md`.

Use the Task tool with subagent_type="legacy-modernizer":

```
Task:
  subagent_type: "legacy-modernizer"
  description: "Plan safe decommissioning of replaced legacy components"
  prompt: |
    Plan safe decommissioning of replaced legacy components.

    ## Legacy Assessment
    [Insert contents of .legacy-modernize/01-legacy-assessment.md]

    ## Modernized Components
    [Insert contents of .legacy-modernize/08-first-wave.md]

    ## Rollout Status
    [Insert contents of .legacy-modernize/11-rollout.md]

    ## Instructions
    1. Verify no remaining dependencies through traffic analysis (minimum 30 days at 0% traffic)
    2. Archive legacy code with documentation of original functionality
    3. Update CI/CD pipelines to remove legacy builds
    4. Clean up unused database tables and remove deprecated API endpoints
    5. Document any retained legacy components with sunset timeline

    Provide a decommissioning checklist and timeline.
```

Save the agent's output to `.legacy-modernize/12-decommission.md`.

Update `state.json`: set `current_step` to 13, add step 12 to `completed_steps`.

### Step 13: Documentation and Knowledge Transfer

Read all previous `.legacy-modernize/*.md` files.

Use the Task tool with subagent_type="general-purpose":

```
Task:
  subagent_type: "general-purpose"
  description: "Create comprehensive modernization documentation package"
  prompt: |
    You are a technical writer specializing in system migration documentation
    and developer knowledge transfer materials.

    Create comprehensive modernization documentation.

    ## All Migration Artifacts
    [Insert contents of all .legacy-modernize/*.md files]

    ## Instructions
    1. Create architectural diagrams (before/after)
    2. Write API documentation with migration guides
    3. Create runbooks for dual-system operation
    4. Write troubleshooting guides for common issues
    5. Create a lessons learned report
    6. Generate developer onboarding guide for the modernized system
    7. Document technical decisions and trade-offs made during migration

    Write all documentation files. Report what was created.
```

Save the agent's output to `.legacy-modernize/13-documentation.md`.

Update `state.json`: set `current_step` to "complete", add step 13 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
Legacy modernization complete: $TARGET

## Session Files
- .legacy-modernize/01-legacy-assessment.md — Legacy system analysis
- .legacy-modernize/02-dependency-map.md — Dependency and integration mapping
- .legacy-modernize/03-business-impact.md — Business impact and risk assessment
- .legacy-modernize/04-test-coverage.md — Test coverage analysis
- .legacy-modernize/05-contract-tests.md — Contract tests and baselines
- .legacy-modernize/06-test-data.md — Test data management strategy
- .legacy-modernize/07-infrastructure.md — Strangler fig infrastructure
- .legacy-modernize/08-first-wave.md — First wave component modernization
- .legacy-modernize/09-security.md — Security audit and hardening
- .legacy-modernize/10-performance.md — Performance testing results
- .legacy-modernize/11-rollout.md — Progressive rollout plan
- .legacy-modernize/12-decommission.md — Decommissioning checklist
- .legacy-modernize/13-documentation.md — Documentation package

## Success Criteria
- All high-priority components modernized with >80% test coverage
- Zero unplanned downtime during migration
- Performance metrics maintained (P95 latency within 110% of baseline)
- Security vulnerabilities reduced by >90%
- Technical debt score improved by >60%

## Next Steps
1. Review all generated code, tests, and documentation
2. Execute the progressive rollout plan in .legacy-modernize/11-rollout.md
3. Monitor for 30 days post-migration per .legacy-modernize/12-decommission.md
4. Complete decommissioning after observation period
```
