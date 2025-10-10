---
model: claude-sonnet-4-5-20250929
---

Implement a new feature using specialized agents with explicit Task tool invocations:

[Extended thinking: This workflow orchestrates multiple specialized agents to implement a complete feature from design to deployment. Each agent receives context from previous agents to ensure coherent implementation. Supports both traditional and TDD-driven development approaches.]

## Development Mode Selection

Choose your development approach:

### Option A: Traditional Development (Default)
Use the Task tool to delegate to specialized agents in sequence:

### Option B: TDD-Driven Development
For test-first development, use the tdd-orchestrator agent:
- Use Task tool with subagent_type="tdd-orchestrator"
- Prompt: "Implement feature using TDD methodology: $ARGUMENTS. Follow red-green-refactor cycle strictly."
- Alternative: Use the dedicated tdd-cycle workflow for granular TDD control

When TDD mode is selected, the workflow follows this pattern:
1. Write failing tests first (Red phase)
2. Implement minimum code to pass tests (Green phase)
3. Refactor while keeping tests green (Refactor phase)
4. Repeat cycle for each feature component

## Traditional Development Steps

1. **Backend Architecture Design**
   - Use Task tool with subagent_type="backend-architect" 
   - Prompt: "Design RESTful API and data model for: $ARGUMENTS. Include endpoint definitions, database schema, and service boundaries."
   - Save the API design and schema for next agents

2. **Frontend Implementation**
   - Use Task tool with subagent_type="frontend-developer"
   - Prompt: "Create UI components for: $ARGUMENTS. Use the API design from backend-architect: [include API endpoints and data models from step 1]"
   - Ensure UI matches the backend API contract

3. **Test Coverage**
   - Use Task tool with subagent_type="test-automator"
   - Prompt: "Write comprehensive tests for: $ARGUMENTS. Cover both backend API endpoints: [from step 1] and frontend components: [from step 2]"
   - Include unit, integration, and e2e tests

4. **Production Deployment**
   - Use Task tool with subagent_type="deployment-engineer"
   - Prompt: "Prepare production deployment for: $ARGUMENTS. Include CI/CD pipeline, containerization, and monitoring for the implemented feature."
   - Ensure all components from previous steps are deployment-ready

## TDD Development Steps

When using TDD mode, the sequence changes to:

1. **Test-First Backend Design**
   - Use Task tool with subagent_type="tdd-orchestrator"
   - Prompt: "Design and write failing tests for backend API: $ARGUMENTS. Define test cases before implementation."
   - Create comprehensive test suite for API endpoints

2. **Test-First Frontend Design**
   - Use Task tool with subagent_type="tdd-orchestrator"
   - Prompt: "Write failing tests for frontend components: $ARGUMENTS. Include unit and integration tests."
   - Define expected UI behavior through tests

3. **Incremental Implementation**
   - Use Task tool with subagent_type="tdd-orchestrator"
   - Prompt: "Implement features to pass tests for: $ARGUMENTS. Follow strict red-green-refactor cycles."
   - Build features incrementally, guided by tests

4. **Refactoring & Optimization**
   - Use Task tool with subagent_type="tdd-orchestrator"
   - Prompt: "Refactor implementation while maintaining green tests: $ARGUMENTS. Optimize for maintainability."
   - Improve code quality with test safety net

5. **Production Deployment**
   - Use Task tool with subagent_type="deployment-engineer"
   - Prompt: "Deploy TDD-developed feature: $ARGUMENTS. Verify all tests pass in CI/CD pipeline."
   - Ensure test suite runs in deployment pipeline

## Execution Parameters

- **--tdd**: Enable TDD mode (uses tdd-orchestrator agent)
- **--strict-tdd**: Enforce strict red-green-refactor cycles
- **--test-coverage-min**: Set minimum test coverage threshold (default: 80%)
- **--tdd-cycle**: Use dedicated tdd-cycle workflow for granular control

Aggregate results from all agents and present a unified implementation plan.

Feature description: $ARGUMENTS
