---
model: claude-sonnet-4-5-20250929
---

Perform a comprehensive review using multiple specialized agents with explicit Task tool invocations:

[Extended thinking: This workflow performs a thorough multi-perspective review by orchestrating specialized review agents. Each agent examines different aspects and the results are consolidated into a unified action plan. Includes TDD compliance verification when enabled.]

## Review Configuration

- **Standard Review**: Traditional comprehensive review (default)
- **TDD-Enhanced Review**: Includes TDD compliance and test-first verification
  - Enable with **--tdd-review** flag
  - Verifies red-green-refactor cycle adherence
  - Checks test-first implementation patterns

Execute parallel reviews using Task tool with specialized agents:

## 1. Code Quality Review
- Use Task tool with subagent_type="code-reviewer"
- Prompt: "Review code quality and maintainability for: $ARGUMENTS. Check for code smells, readability, documentation, and adherence to best practices."
- Focus: Clean code principles, SOLID, DRY, naming conventions

## 2. Security Audit
- Use Task tool with subagent_type="security-auditor"
- Prompt: "Perform security audit on: $ARGUMENTS. Check for vulnerabilities, OWASP compliance, authentication issues, and data protection."
- Focus: Injection risks, authentication, authorization, data encryption

## 3. Architecture Review
- Use Task tool with subagent_type="architect-reviewer"
- Prompt: "Review architectural design and patterns in: $ARGUMENTS. Evaluate scalability, maintainability, and adherence to architectural principles."
- Focus: Service boundaries, coupling, cohesion, design patterns

## 4. Performance Analysis
- Use Task tool with subagent_type="performance-engineer"
- Prompt: "Analyze performance characteristics of: $ARGUMENTS. Identify bottlenecks, resource usage, and optimization opportunities."
- Focus: Response times, memory usage, database queries, caching

## 5. Test Coverage Assessment
- Use Task tool with subagent_type="test-automator"
- Prompt: "Evaluate test coverage and quality for: $ARGUMENTS. Assess unit tests, integration tests, and identify gaps in test coverage."
- Focus: Coverage metrics, test quality, edge cases, test maintainability

## 6. TDD Compliance Review (When --tdd-review is enabled)
- Use Task tool with subagent_type="tdd-orchestrator"
- Prompt: "Verify TDD compliance for: $ARGUMENTS. Check for test-first development patterns, red-green-refactor cycles, and test-driven design."
- Focus on TDD metrics:
  - **Test-First Verification**: Were tests written before implementation?
  - **Red-Green-Refactor Cycles**: Evidence of proper TDD cycles
  - **Test Coverage Trends**: Coverage growth patterns during development
  - **Test Granularity**: Appropriate test size and scope
  - **Refactoring Evidence**: Code improvements with test safety net
  - **Test Quality**: Tests that drive design, not just verify behavior

## Consolidated Report Structure
Compile all feedback into a unified report:
- **Critical Issues** (must fix): Security vulnerabilities, broken functionality, architectural flaws
- **Recommendations** (should fix): Performance bottlenecks, code quality issues, missing tests
- **Suggestions** (nice to have): Refactoring opportunities, documentation improvements
- **Positive Feedback** (what's done well): Good practices to maintain and replicate

### TDD-Specific Metrics (When --tdd-review is enabled)
Additional TDD compliance report section:
- **TDD Adherence Score**: Percentage of code developed using TDD methodology
- **Test-First Evidence**: Commits showing tests before implementation
- **Cycle Completeness**: Percentage of complete red-green-refactor cycles
- **Test Design Quality**: How well tests drive the design
- **Coverage Delta Analysis**: Coverage changes correlated with feature additions
- **Refactoring Frequency**: Evidence of continuous improvement
- **Test Execution Time**: Performance of test suite
- **Test Stability**: Flakiness and reliability metrics

## Review Options

- **--tdd-review**: Enable TDD compliance checking
- **--strict-tdd**: Fail review if TDD practices not followed
- **--tdd-metrics**: Generate detailed TDD metrics report
- **--test-first-only**: Only review code with test-first evidence

Target: $ARGUMENTS
