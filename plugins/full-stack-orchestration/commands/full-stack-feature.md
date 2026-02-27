---
description: "Orchestrate end-to-end full-stack feature development across backend, frontend, database, and infrastructure layers"
argument-hint: "<feature description> [--stack react/fastapi/postgres] [--api-style rest|graphql] [--complexity simple|medium|complex]"
---

# Full-Stack Feature Orchestrator

## CRITICAL BEHAVIORAL RULES

You MUST follow these rules exactly. Violating any of them is a failure.

1. **Execute steps in order.** Do NOT skip ahead, reorder, or merge steps.
2. **Write output files.** Each step MUST produce its output file in `.full-stack-feature/` before the next step begins. Read from prior step files -- do NOT rely on context window memory.
3. **Stop at checkpoints.** When you reach a `PHASE CHECKPOINT`, you MUST stop and wait for explicit user approval before continuing. Use the AskUserQuestion tool with clear options.
4. **Halt on failure.** If any step fails (agent error, test failure, missing dependency), STOP immediately. Present the error and ask the user how to proceed. Do NOT silently continue.
5. **Use only local agents.** All `subagent_type` references use agents bundled with this plugin or `general-purpose`. No cross-plugin dependencies.
6. **Never enter plan mode autonomously.** Do NOT use EnterPlanMode. This command IS the plan -- execute it.

## Pre-flight Checks

Before starting, perform these checks:

### 1. Check for existing session

Check if `.full-stack-feature/state.json` exists:

- If it exists and `status` is `"in_progress"`: Read it, display the current step, and ask the user:

  ```
  Found an in-progress full-stack feature session:
  Feature: [name from state]
  Current step: [step from state]

  1. Resume from where we left off
  2. Start fresh (archives existing session)
  ```

- If it exists and `status` is `"complete"`: Ask whether to archive and start fresh.

### 2. Initialize state

Create `.full-stack-feature/` directory and `state.json`:

```json
{
  "feature": "$ARGUMENTS",
  "status": "in_progress",
  "stack": "auto-detect",
  "api_style": "rest",
  "complexity": "medium",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

Parse `$ARGUMENTS` for `--stack`, `--api-style`, and `--complexity` flags. Use defaults if not specified.

### 3. Parse feature description

Extract the feature description from `$ARGUMENTS` (everything before the flags). This is referenced as `$FEATURE` in prompts below.

---

## Phase 1: Architecture & Design Foundation (Steps 1-3) -- Interactive

### Step 1: Requirements Gathering

Gather requirements through interactive Q&A. Ask ONE question at a time using the AskUserQuestion tool. Do NOT ask all questions at once.

**Questions to ask (in order):**

1. **Problem Statement**: "What problem does this feature solve? Who is the user and what's their pain point?"
2. **Acceptance Criteria**: "What are the key acceptance criteria? When is this feature 'done'?"
3. **Scope Boundaries**: "What is explicitly OUT of scope for this feature?"
4. **Technical Constraints**: "Any technical constraints? (e.g., existing API conventions, specific DB, latency requirements, auth system)"
5. **Stack Confirmation**: "Confirm the tech stack -- detected [stack] from project. Frontend framework? Backend framework? Database? Any changes?"
6. **Dependencies**: "Does this feature depend on or affect other features/services?"

After gathering answers, write the requirements document:

**Output file:** `.full-stack-feature/01-requirements.md`

```markdown
# Requirements: $FEATURE

## Problem Statement

[From Q1]

## Acceptance Criteria

[From Q2 -- formatted as checkboxes]

## Scope

### In Scope

[Derived from answers]

### Out of Scope

[From Q3]

## Technical Constraints

[From Q4]

## Technology Stack

[From Q5 -- frontend, backend, database, infrastructure]

## Dependencies

[From Q6]

## Configuration

- Stack: [detected or specified]
- API Style: [rest|graphql]
- Complexity: [simple|medium|complex]
```

Update `state.json`: set `current_step` to 2, add `"01-requirements.md"` to `files_created`, add step 1 to `completed_steps`.

### Step 2: Database & Data Model Design

Read `.full-stack-feature/01-requirements.md` to load requirements context.

Use the Task tool to launch a database architecture agent:

```
Task:
  subagent_type: "general-purpose"
  description: "Design database schema and data models for $FEATURE"
  prompt: |
    You are a database architect. Design the database schema and data models for this feature.

    ## Requirements
    [Insert full contents of .full-stack-feature/01-requirements.md]

    ## Deliverables
    1. **Entity relationship design**: Tables/collections, relationships, cardinality
    2. **Schema definitions**: Column types, constraints, defaults, nullable fields
    3. **Indexing strategy**: Which columns to index, index types, composite indexes
    4. **Migration strategy**: How to safely add/modify schema in production
    5. **Query patterns**: Expected read/write patterns and how the schema supports them
    6. **Data access patterns**: Repository/DAO interface design

    Write your complete database design as a single markdown document.
```

Save the agent's output to `.full-stack-feature/02-database-design.md`.

Update `state.json`: set `current_step` to 3, add step 2 to `completed_steps`.

### Step 3: Backend & Frontend Architecture

Read `.full-stack-feature/01-requirements.md` and `.full-stack-feature/02-database-design.md`.

Use the Task tool to launch an architecture agent:

```
Task:
  subagent_type: "general-purpose"
  description: "Design full-stack architecture for $FEATURE"
  prompt: |
    You are a full-stack architect. Design the complete backend and frontend architecture for this feature.

    ## Requirements
    [Insert contents of .full-stack-feature/01-requirements.md]

    ## Database Design
    [Insert contents of .full-stack-feature/02-database-design.md]

    ## Deliverables

    ### Backend Architecture
    1. **API design**: Endpoints/resolvers, request/response schemas, error handling, versioning
    2. **Service layer**: Business logic components, their responsibilities, boundaries
    3. **Authentication/authorization**: How auth applies to new endpoints
    4. **Integration points**: How this connects to existing services/systems

    ### Frontend Architecture
    1. **Component hierarchy**: Page components, containers, presentational components
    2. **State management**: What state is needed, where it lives, data flow
    3. **Routing**: New routes, navigation structure, route guards
    4. **API integration**: Data fetching strategy, caching, optimistic updates

    ### Cross-Cutting Concerns
    1. **Error handling**: Backend errors -> API responses -> frontend error states
    2. **Security considerations**: Input validation, XSS prevention, CSRF, data protection
    3. **Risk assessment**: Technical risks and mitigation strategies

    Write your complete architecture design as a single markdown document.
```

Save the agent's output to `.full-stack-feature/03-architecture.md`.

Update `state.json`: set `current_step` to "checkpoint-1", add step 3 to `completed_steps`.

---

## PHASE CHECKPOINT 1 -- User Approval Required

You MUST stop here and present the architecture for review.

Display a summary of the database design and architecture from `.full-stack-feature/02-database-design.md` and `.full-stack-feature/03-architecture.md` (key components, API endpoints, data model overview, component structure) and ask:

```
Architecture and database design are complete. Please review:
- .full-stack-feature/02-database-design.md
- .full-stack-feature/03-architecture.md

1. Approve -- proceed to implementation
2. Request changes -- tell me what to adjust
3. Pause -- save progress and stop here
```

Do NOT proceed to Phase 2 until the user selects option 1. If they select option 2, revise and re-checkpoint. If option 3, update `state.json` and stop.

---

## Phase 2: Implementation (Steps 4-7)

### Step 4: Database Implementation

Read `.full-stack-feature/01-requirements.md` and `.full-stack-feature/02-database-design.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement database layer for $FEATURE"
  prompt: |
    You are a database engineer. Implement the database layer for this feature.

    ## Requirements
    [Insert contents of .full-stack-feature/01-requirements.md]

    ## Database Design
    [Insert contents of .full-stack-feature/02-database-design.md]

    ## Instructions
    1. Create migration scripts for schema changes
    2. Implement models/entities matching the schema design
    3. Implement repository/data access layer with the designed query patterns
    4. Add database-level validation constraints
    5. Optimize queries with proper indexes as designed
    6. Follow the project's existing ORM and migration patterns

    Write all code files. Report what files were created/modified.
```

Save a summary to `.full-stack-feature/04-database-impl.md`.

Update `state.json`: set `current_step` to 5, add step 4 to `completed_steps`.

### Step 5: Backend Implementation

Read `.full-stack-feature/01-requirements.md`, `.full-stack-feature/03-architecture.md`, and `.full-stack-feature/04-database-impl.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement backend services for $FEATURE"
  prompt: |
    You are a backend developer. Implement the backend services for this feature based on the approved architecture.

    ## Requirements
    [Insert contents of .full-stack-feature/01-requirements.md]

    ## Architecture
    [Insert contents of .full-stack-feature/03-architecture.md]

    ## Database Implementation
    [Insert contents of .full-stack-feature/04-database-impl.md]

    ## Instructions
    1. Implement API endpoints/resolvers as designed in the architecture
    2. Implement business logic in the service layer
    3. Wire up the data access layer from the database implementation
    4. Add input validation, error handling, and proper HTTP status codes
    5. Implement authentication/authorization middleware as designed
    6. Add structured logging and observability hooks
    7. Follow the project's existing code patterns and conventions

    Write all code files. Report what files were created/modified.
```

Save a summary to `.full-stack-feature/05-backend-impl.md`.

Update `state.json`: set `current_step` to 6, add step 5 to `completed_steps`.

### Step 6: Frontend Implementation

Read `.full-stack-feature/01-requirements.md`, `.full-stack-feature/03-architecture.md`, and `.full-stack-feature/05-backend-impl.md`.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Implement frontend for $FEATURE"
  prompt: |
    You are a frontend developer. Implement the frontend components for this feature.

    ## Requirements
    [Insert contents of .full-stack-feature/01-requirements.md]

    ## Architecture
    [Insert contents of .full-stack-feature/03-architecture.md]

    ## Backend Implementation
    [Insert contents of .full-stack-feature/05-backend-impl.md]

    ## Instructions
    1. Build UI components following the component hierarchy from the architecture
    2. Implement state management and data flow as designed
    3. Integrate with the backend API endpoints using the designed data fetching strategy
    4. Implement form handling, validation, and error states
    5. Add loading states and optimistic updates where appropriate
    6. Ensure responsive design and accessibility basics (semantic HTML, ARIA labels, keyboard nav)
    7. Follow the project's existing frontend patterns and component conventions

    Write all code files. Report what files were created/modified.
```

Save a summary to `.full-stack-feature/06-frontend-impl.md`.

**Note:** If the feature has no frontend component (pure backend/API), skip this step -- write a brief note in `06-frontend-impl.md` explaining why it was skipped, and continue.

Update `state.json`: set `current_step` to 7, add step 6 to `completed_steps`.

### Step 7: Testing & Validation

Read `.full-stack-feature/04-database-impl.md`, `.full-stack-feature/05-backend-impl.md`, and `.full-stack-feature/06-frontend-impl.md`.

Launch three agents in parallel using multiple Task tool calls in a single response:

**7a. Test Suite Creation:**

```
Task:
  subagent_type: "test-automator"
  description: "Create test suite for $FEATURE"
  prompt: |
    Create a comprehensive test suite for this full-stack feature.

    ## What was implemented
    ### Database
    [Insert contents of .full-stack-feature/04-database-impl.md]

    ### Backend
    [Insert contents of .full-stack-feature/05-backend-impl.md]

    ### Frontend
    [Insert contents of .full-stack-feature/06-frontend-impl.md]

    ## Instructions
    1. Write unit tests for all new backend functions/methods
    2. Write integration tests for API endpoints
    3. Write database tests for migrations and query patterns
    4. Write frontend component tests if applicable
    5. Cover: happy path, edge cases, error handling, boundary conditions
    6. Follow existing test patterns and frameworks in the project
    7. Target 80%+ code coverage for new code

    Write all test files. Report what test files were created and what they cover.
```

**7b. Security Review:**

```
Task:
  subagent_type: "security-auditor"
  description: "Security review of $FEATURE"
  prompt: |
    Perform a security review of this full-stack feature implementation.

    ## Architecture
    [Insert contents of .full-stack-feature/03-architecture.md]

    ## Database Implementation
    [Insert contents of .full-stack-feature/04-database-impl.md]

    ## Backend Implementation
    [Insert contents of .full-stack-feature/05-backend-impl.md]

    ## Frontend Implementation
    [Insert contents of .full-stack-feature/06-frontend-impl.md]

    Review for: OWASP Top 10, authentication/authorization flaws, input validation gaps,
    SQL injection risks, XSS/CSRF vulnerabilities, data protection issues, dependency vulnerabilities,
    and any security anti-patterns.

    Provide findings with severity, location, and specific fix recommendations.
```

**7c. Performance Review:**

```
Task:
  subagent_type: "performance-engineer"
  description: "Performance review of $FEATURE"
  prompt: |
    Review the performance of this full-stack feature implementation.

    ## Architecture
    [Insert contents of .full-stack-feature/03-architecture.md]

    ## Database Implementation
    [Insert contents of .full-stack-feature/04-database-impl.md]

    ## Backend Implementation
    [Insert contents of .full-stack-feature/05-backend-impl.md]

    ## Frontend Implementation
    [Insert contents of .full-stack-feature/06-frontend-impl.md]

    Review for: N+1 queries, missing indexes, unoptimized queries, memory leaks,
    missing caching opportunities, large payloads, slow rendering paths,
    bundle size concerns, unnecessary re-renders.

    Provide findings with impact estimates and specific optimization recommendations.
```

After all three complete, consolidate results into `.full-stack-feature/07-testing.md`:

```markdown
# Testing & Validation: $FEATURE

## Test Suite

[Summary from 7a -- files created, coverage areas]

## Security Findings

[Summary from 7b -- findings by severity]

## Performance Findings

[Summary from 7c -- findings by impact]

## Action Items

[List any critical/high findings that need to be addressed before delivery]
```

If there are Critical or High severity findings from security or performance review, address them now before proceeding. Apply fixes and re-validate.

Update `state.json`: set `current_step` to "checkpoint-2", add step 7 to `completed_steps`.

---

## PHASE CHECKPOINT 2 -- User Approval Required

Display a summary of testing and validation results from `.full-stack-feature/07-testing.md` and ask:

```
Testing and validation complete. Please review .full-stack-feature/07-testing.md

Test coverage: [summary]
Security findings: [X critical, Y high, Z medium]
Performance findings: [X critical, Y high, Z medium]

1. Approve -- proceed to deployment & documentation
2. Request changes -- tell me what to fix
3. Pause -- save progress and stop here
```

Do NOT proceed to Phase 3 until the user approves.

---

## Phase 3: Delivery (Steps 8-9)

### Step 8: Deployment & Infrastructure

Read `.full-stack-feature/03-architecture.md` and `.full-stack-feature/07-testing.md`.

Use the Task tool:

```
Task:
  subagent_type: "deployment-engineer"
  description: "Create deployment config for $FEATURE"
  prompt: |
    Create the deployment and infrastructure configuration for this full-stack feature.

    ## Architecture
    [Insert contents of .full-stack-feature/03-architecture.md]

    ## Testing Results
    [Insert contents of .full-stack-feature/07-testing.md]

    ## Instructions
    1. Create or update CI/CD pipeline configuration for the new code
    2. Add database migration steps to the deployment pipeline
    3. Add feature flag configuration if the feature should be gradually rolled out
    4. Define health checks and readiness probes for new services/endpoints
    5. Create monitoring alerts for key metrics (error rate, latency, throughput)
    6. Write a deployment runbook with rollback steps (including database rollback)
    7. Follow existing deployment patterns in the project

    Write all configuration files. Report what was created/modified.
```

Save output to `.full-stack-feature/08-deployment.md`.

Update `state.json`: set `current_step` to 9, add step 8 to `completed_steps`.

### Step 9: Documentation & Handoff

Read all previous `.full-stack-feature/*.md` files.

Use the Task tool:

```
Task:
  subagent_type: "general-purpose"
  description: "Write documentation for $FEATURE"
  prompt: |
    You are a technical writer. Create documentation for this full-stack feature.

    ## Feature Context
    [Insert contents of .full-stack-feature/01-requirements.md]

    ## Architecture
    [Insert contents of .full-stack-feature/03-architecture.md]

    ## Implementation Summary
    ### Database: [Insert contents of .full-stack-feature/04-database-impl.md]
    ### Backend: [Insert contents of .full-stack-feature/05-backend-impl.md]
    ### Frontend: [Insert contents of .full-stack-feature/06-frontend-impl.md]

    ## Deployment
    [Insert contents of .full-stack-feature/08-deployment.md]

    ## Instructions
    1. Write API documentation for new endpoints (request/response examples)
    2. Document the database schema changes and migration notes
    3. Update or create user-facing documentation if applicable
    4. Write a brief architecture decision record (ADR) explaining key design choices
    5. Create a handoff summary: what was built, how to test it, known limitations

    Write documentation files. Report what was created/modified.
```

Save output to `.full-stack-feature/09-documentation.md`.

Update `state.json`: set `current_step` to "complete", add step 9 to `completed_steps`.

---

## Completion

Update `state.json`:

- Set `status` to `"complete"`
- Set `last_updated` to current timestamp

Present the final summary:

```
Full-stack feature development complete: $FEATURE

## Files Created
[List all .full-stack-feature/ output files]

## Implementation Summary
- Requirements: .full-stack-feature/01-requirements.md
- Database Design: .full-stack-feature/02-database-design.md
- Architecture: .full-stack-feature/03-architecture.md
- Database Implementation: .full-stack-feature/04-database-impl.md
- Backend Implementation: .full-stack-feature/05-backend-impl.md
- Frontend Implementation: .full-stack-feature/06-frontend-impl.md
- Testing & Validation: .full-stack-feature/07-testing.md
- Deployment: .full-stack-feature/08-deployment.md
- Documentation: .full-stack-feature/09-documentation.md

## Next Steps
1. Review all generated code and documentation
2. Run the full test suite to verify everything passes
3. Create a pull request with the implementation
4. Deploy using the runbook in .full-stack-feature/08-deployment.md
```
