---
description: "Orchestrate end-to-end feature development from requirements to deployment"
argument-hint: "<feature description> [--methodology tdd|bdd|ddd] [--complexity simple|medium|complex]"
---

# Feature Development Orchestrator

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.feature-dev/` before the next step begins. Read from prior step files — do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan — execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.feature-dev/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress feature development session:
  Feature: [name from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.feature-dev/` directory and `state.json`:

```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "methodology": "traditional",
  "complexity": "medium",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--methodology` and `--complexity` flags. Use defaults if not specified.

### 3. Parse feature description

Extract the feature description from `$ARGUMENTS` (everything before the flags). This is referenced as `$FEATURE` in prompts below.

---

## Phase 1: Discovery (Steps 1–2) — Interactive

### Step 1: Requirements Gathering

Gather requirements through interactive Q&A. Ask ONE question at a time using the AskUserQuestion tool. Do NOT ask all questions at once.

**Questions to ask (in order):**

1. **Problem Statement**: "What problem does this feature solve? Who is the user and what's their pain point?"
2. **Acceptance Criteria**: "What are the key acceptance criteria? When is this feature 'done'?"
3. **Scope Boundaries**: "What is explicitly OUT of scope for this feature?"
4. **Technical Constraints**: "Any technical constraints? (e.g., must use existing auth system, specific DB, latency requirements)"
5. **Dependencies**: "Does this feature depend on or affect other features/services?"

After gathering answers, write the requirements document:

**Output file:** `.feature-dev/01-requirements.md`

```markdown
# Requirements: $FEATURE

## Problem Statement

[From Q1]

## Acceptance Criteria

[From Q2 — formatted as checkboxes]

## Scope

### In Scope

[Derived from answers]

### Out of Scope

[From Q3]

## Technical Constraints

[From Q4]

## Dependencies

[From Q5]

## Methodology: [tdd|bdd|ddd|traditional]

## Complexity: [simple|medium|complex]
```

Update `state.json`: set `current_step` to 2, add `"01-requirements.md"` to `files_created`, add step 1 to `completed_steps`.

### Step 2: Architecture & Security Design

Read `.feature-dev/01-requirements.md` to load requirements context.

Use the Task tool to launch the architecture agent:

```
Task:
  subagent_type: "backend-architect"
  description: "Design architecture for $FEATURE"
  prompt: |
    Design the technical architecture for this feature.

    ## Requirements
    [Insert full contents of .feature-dev/01-requirements.md]

    ## Deliverables
    1. **Service/component design**: What components are needed, their responsibilities, and boundaries
    2. **API design**: Endpoints, request/response schemas, error handling
    3. **Data model**: Database tables/collections, relationships, migrations needed
    4. **Security considerations**: Auth requirements, input validation, data protection, OWASP concerns
    5. **Integration points**: How this connects to existing services/systems
    6. **Risk assessment**: Technical risks and mitigation strategies

    Write your complete architecture design as a single markdown document.
```

Save the agent's output to `.feature-dev/02-architecture.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 2 to `completed_steps`.

---

## PHASE CHECKPOINT 1 — User Approval Required

You MUST stop here and present the architecture for review.

Display a summary of the architecture from `.feature-dev/02-architecture.md` (key components, API endpoints, data model overview) and ask:

```
Architecture design is complete. Please review .feature-dev/02-architecture.md

1. Approve — proceed to implementation
2. Request changes — tell me what to adjust
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1. If they select option 2, revise the architecture and re-checkpoint. If option 3, update `state.json` status and stop.

---

## Phase 2: Implementation (Steps 3–5)

### Step 3: Backend Implementation

Read `.feature-dev/01-requirements.md` and `.feature-dev/02-architecture.md`.

Use the Task tool to launch the backend architect for implementation:

```
Task:
  subagent_type: "backend-architect"
  description: "Implement backend for $FEATURE"
  prompt: |
    Implement the backend for this feature based on the approved architecture.

    ## Requirements
    [Insert contents of .feature-dev/01-requirements.md]

    ## Architecture
    [Insert contents of .feature-dev/02-architecture.md]

    ## Instructions
    1. Implement the API endpoints, business logic, and data access layer as designed
    2. Include data layer components (models, migrations, repositories) as specified in the architecture
    3. Add input validation and error handling
    4. Follow the project's existing code patterns and conventions
    5. If methodology is TDD: write failing tests first, then implement
    6. Include inline comments only where logic is non-obvious

    Write all code files. Report what files were created/modified.
```

Save a summary of what was implemented to `.feature-dev/03-backend.md` (list of files created/modified, key decisions, any deviations from architecture).

Update `state.json`: set `current_step` to 4, add step 3 to `completed_steps`.

### Step 4: Frontend Implementation

Read `.feature-dev/01-requirements.md`, `.feature-dev/02-architecture.md`, and `.feature-dev/03-backend.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement frontend for $FEATURE"
  prompt: |
    You are a frontend developer. Implement the frontend components for this feature.

    ## Requirements
    [Insert contents of .feature-dev/01-requirements.md]

    ## Architecture
    [Insert contents of .feature-dev/02-architecture.md]

    ## Backend Implementation
    [Insert contents of .feature-dev/03-backend.md]

    ## Instructions
    1. Build UI components that integrate with the backend API endpoints
    2. Implement state management, form handling, and error states
    3. Add loading states and optimistic updates where appropriate
    4. Follow the project's existing frontend patterns and component conventions
    5. Ensure responsive design and accessibility basics (semantic HTML, ARIA labels, keyboard nav)

    Write all code files. Report what files were created/modified.
```

Save a summary to `.feature-dev/04-frontend.md`.

**Note:** If the feature has no frontend component (pure backend/API), skip this step — write a brief note in `04-frontend.md` explaining why it was skipped, and continue.

Update `state.json`: set `current_step` to 5, add step 4 to `completed_steps`.

### Step 5: Testing & Validation

Read `.feature-dev/03-backend.md` and `.feature-dev/04-frontend.md`.

Launch three agents in parallel using multiple Task tool calls in a single response:

**5a. Test Suite Creation:**

```
Task:
  subagent_type: "test-automator"
  description: "Create test suite for $FEATURE"
  prompt: |
    Create a comprehensive test suite for this feature.

    ## What was implemented
    ### Backend
    [Insert contents of .feature-dev/03-backend.md]

    ### Frontend
    [Insert contents of .feature-dev/04-frontend.md]

    ## Instructions
    1. Write unit tests for all new backend functions/methods
    2. Write integration tests for API endpoints
    3. Write frontend component tests if applicable
    4. Cover: happy path, edge cases, error handling, boundary conditions
    5. Follow existing test patterns and frameworks in the project
    6. Target 80%+ code coverage for new code

    Write all test files. Report what test files were created and what they cover.
```

**5b. Security Review:**

```
Task:
  subagent_type: "security-auditor"
  description: "Security review of $FEATURE"
  prompt: |
    Perform a security review of this feature implementation.

    ## Architecture
    [Insert contents of .feature-dev/02-architecture.md]

    ## Backend Implementation
    [Insert contents of .feature-dev/03-backend.md]

    ## Frontend Implementation
    [Insert contents of .feature-dev/04-frontend.md]

    Review for: OWASP Top 10, authentication/authorization flaws, input validation gaps,
    data protection issues, dependency vulnerabilities, and any security anti-patterns.

    Provide findings with severity, location, and specific fix recommendations.
```

**5c. Performance Review:**

```
Task:
  subagent_type: "performance-engineer"
  description: "Performance review of $FEATURE"
  prompt: |
    Review the performance of this feature implementation.

    ## Architecture
    [Insert contents of .feature-dev/02-architecture.md]

    ## Backend Implementation
    [Insert contents of .feature-dev/03-backend.md]

    ## Frontend Implementation
    [Insert contents of .feature-dev/04-frontend.md]

    Review for: N+1 queries, missing indexes, unoptimized queries, memory leaks,
    missing caching opportunities, large payloads, slow rendering paths.

    Provide findings with impact estimates and specific optimization recommendations.
```

After all three complete, consolidate results into `.feature-dev/05-testing.md`:

```markdown
# Testing & Validation: $FEATURE

## Test Suite

[Summary from 5a — files created, coverage areas]

## Security Findings

[Summary from 5b — findings by severity]

## Performance Findings

[Summary from 5c — findings by impact]

## Action Items

[List any critical/high findings that need to be addressed before delivery]
```

If there are Critical or High severity findings from security or performance review, address them now before proceeding. Apply fixes and re-validate.

Update `state.json`: set `current_step` to "checkpoint-2", add step 5 to `completed_steps`.

---

## PHASE CHECKPOINT 2 — User Approval Required

Display a summary of testing and validation results from `.feature-dev/05-testing.md` and ask:

```
Testing and validation complete. Please review .feature-dev/05-testing.md

Test coverage: [summary]
Security findings: [X critical, Y high, Z medium]
Performance findings: [X critical, Y high, Z medium]

1. Approve — proceed to deployment & documentation
2. Request changes — tell me what to fix
3. Pause — save progress and stop here
```

Do NOT proceed to Phase 3 until the user approves.

---

## Phase 3: Delivery (Steps 6–7)

### Step 6: Deployment & Monitoring

Read `.feature-dev/02-architecture.md` and `.feature-dev/05-testing.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Create deployment config for $FEATURE"
  prompt: |
    You are a deployment engineer. Create the deployment and monitoring configuration for this feature.

    ## Architecture
    [Insert contents of .feature-dev/02-architecture.md]

    ## Testing Results
    [Insert contents of .feature-dev/05-testing.md]

    ## Instructions
    1. Create or update CI/CD pipeline configuration for the new code
    2. Add feature flag configuration if the feature should be gradually rolled out
    3. Define health checks and readiness probes for new services/endpoints
    4. Create monitoring alerts for key metrics (error rate, latency, throughput)
    5. Write a deployment runbook with rollback steps
    6. Follow existing deployment patterns in the project

    Write all configuration files. Report what was created/modified.
```

Save output to `.feature-dev/06-deployment.md`.

Update `state.json`: set `current_step` to 7, add step 6 to `completed_steps`.

### Step 7: Documentation & Handoff

Read all previous `.feature-dev/*.md` files.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Write documentation for $FEATURE"
  prompt: |
    You are a technical writer. Create documentation for this feature.

    ## Feature Context
    [Insert contents of .feature-dev/01-requirements.md]

    ## Architecture
    [Insert contents of .feature-dev/02-architecture.md]

    ## Implementation Summary
    ### Backend: [Insert contents of .feature-dev/03-backend.md]
    ### Frontend: [Insert contents of .feature-dev/04-frontend.md]

    ## Deployment
    [Insert contents of .feature-dev/06-deployment.md]

    ## Instructions
    1. Write API documentation for new endpoints (request/response examples)
    2. Update or create user-facing documentation if applicable
    3. Write a brief architecture decision record (ADR) explaining key design choices
    4. Create a handoff summary: what was built, how to test it, known limitations

    Write documentation files. Report what was created/modified.
```

Save output to `.feature-dev/07-documentation.md`.

Update `state.json`: set `current_step` to "complete", add step 7 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
Feature development complete: $FEATURE

## Files Created
[List all .feature-dev/ output files]

## Implementation Summary
- Requirements: .feature-dev/01-requirements.md
- Architecture: .feature-dev/02-architecture.md
- Backend: .feature-dev/03-backend.md
- Frontend: .feature-dev/04-frontend.md
- Testing: .feature-dev/05-testing.md
- Deployment: .feature-dev/06-deployment.md
- Documentation: .feature-dev/07-documentation.md

## Next Steps
1. Review all generated code and documentation
2. Run the full test suite to verify everything passes
3. Create a pull request with the implementation
4. Deploy using the runbook in .feature-dev/06-deployment.md
```
