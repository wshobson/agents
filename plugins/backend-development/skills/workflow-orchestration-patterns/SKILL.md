---
name: workflow-orchestration-patterns
description: Design durable workflows with Temporal for distributed systems. Covers workflow vs activity separation, saga patterns, state management, and determinism constraints. Use when building long-running processes, distributed transactions, or microservice orchestration.
---

# Workflow Orchestration Patterns

Master workflow orchestration architecture with Temporal, covering fundamental design decisions, resilience patterns, and best practices for building reliable distributed systems.

## When to Use Workflow Orchestration

### Ideal Use Cases (Source: docs.temporal.io)

- **Multi-step processes** spanning machines/services/databases
- **Distributed transactions** requiring all-or-nothing semantics
- **Long-running workflows** (hours to years) with automatic state persistence
- **Failure recovery** that must resume from last successful step
- **Business processes**: bookings, orders, campaigns, approvals
- **Entity lifecycle management**: inventory tracking, account management, cart workflows
- **Infrastructure automation**: CI/CD pipelines, provisioning, deployments
- **Human-in-the-loop** systems requiring timeouts and escalations

### When NOT to Use

- Simple CRUD operations (use direct API calls)
- Pure data processing pipelines (use Airflow, batch processing)
- Stateless request/response (use standard APIs)
- Real-time streaming (use Kafka, event processors)

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Workflow Design

1. **Keep workflows focused** - Single responsibility per workflow
2. **Small workflows** - Use child workflows for scalability
3. **Clear boundaries** - Workflow orchestrates, activities execute
4. **Test locally** - Use time-skipping test environment

### Activity Design

1. **Idempotent operations** - Safe to retry
2. **Short-lived** - Seconds to minutes, not hours
3. **Timeout configuration** - Always set timeouts
4. **Heartbeat for long tasks** - Report progress
5. **Error handling** - Distinguish retryable vs non-retryable

### Common Pitfalls

**Workflow Violations**:

- Using `datetime.now()` instead of `workflow.now()`
- Threading or async operations in workflow code
- Calling external APIs directly from workflow
- Non-deterministic logic in workflows

**Activity Mistakes**:

- Non-idempotent operations (can't handle retries)
- Missing timeouts (activities run forever)
- No error classification (retry validation errors)
- Ignoring payload limits (2MB per argument)

### Operational Considerations

**Monitoring**:

- Workflow execution duration
- Activity failure rates
- Retry attempts and backoff
- Pending workflow counts

**Scalability**:

- Horizontal scaling with workers
- Task queue partitioning
- Child workflow decomposition
- Activity batching when appropriate

## Additional Resources

**Official Documentation**:

- Temporal Core Concepts: docs.temporal.io/workflows
- Workflow Patterns: docs.temporal.io/evaluate/use-cases-design-patterns
- Best Practices: docs.temporal.io/develop/best-practices
- Saga Pattern: temporal.io/blog/saga-pattern-made-easy

**Key Principles**:

1. Workflows = orchestration, Activities = external calls
2. Determinism is non-negotiable for workflows
3. Idempotency is critical for activities
4. State preservation is automatic
5. Design for failure and recovery
