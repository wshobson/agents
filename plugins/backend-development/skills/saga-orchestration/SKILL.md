---
name: saga-orchestration
description: Implement saga patterns for distributed transactions and cross-aggregate workflows. Use this skill when implementing distributed transactions across microservices where 2PC is unavailable, designing compensating actions for failed order workflows that span inventory, payment, and shipping services, building event-driven saga coordinators for travel booking systems that must roll back hotel, flight, and car rental reservations atomically, or debugging stuck saga states in production where compensation steps never complete.
---

# Saga Orchestration

Patterns for managing distributed transactions and long-running business processes without two-phase commit.

## Inputs and Outputs

**What you provide:**
- Service boundaries and ownership (which service owns which step)
- Transaction requirements (which steps must be atomic, which can be eventual)
- Failure modes for each step (transient vs. permanent, retry policy)
- SLA requirements per step (informs timeout configuration)
- Existing event/messaging infrastructure (Kafka, RabbitMQ, SQS, etc.)

**What this skill produces:**
- Saga definition with ordered steps, action commands, and compensation commands
- Orchestrator or choreography implementation for your chosen pattern
- Compensation logic for each participant service (idempotent, always-succeeds)
- Step timeout configuration with per-step deadlines
- Monitoring setup: state machine metrics, stuck saga detection, DLQ recovery

---

## When to Use This Skill

- Coordinating multi-service transactions without distributed locks
- Implementing compensating transactions for partial failures
- Managing long-running business workflows (minutes to hours)
- Handling failures in distributed systems where atomicity is required
- Building order fulfillment, approval, or booking processes
- Replacing fragile two-phase commit with async compensation

---

## Detailed section: Core Concepts

Moved to `references/details.md`.

## Detailed section: Templates

Moved to `references/details.md`.

## Best Practices

### Do's

- **Make every step idempotent** — Commands may be replayed on broker reconnect
- **Design compensations carefully** — They are the most critical code path
- **Use correlation IDs** — The `saga_id` must flow through every event and log
- **Implement per-step timeouts** — Never wait indefinitely for a participant reply
- **Log state transitions** — `saga_id`, `step_name`, `old_state → new_state` on every change
- **Test compensation paths explicitly** — Inject failures at each step index in integration tests

### Don'ts

- **Don't assume instant completion** — Sagas are async and may take minutes
- **Don't skip compensation testing** — The rollback path is the hardest to get right
- **Don't couple services directly** — Use async messaging, never synchronous calls inside a saga step
- **Don't ignore partial failures** — A step that partially executed still needs compensation
- **Don't use a global timeout** — Each step has different latency characteristics

---

## Troubleshooting

### Saga stuck in COMPENSATING state

A saga enters compensation but never reaches FAILED. This means a compensation handler is throwing an unhandled exception and never publishing `SagaCompensationCompleted`. Add dead-letter queue (DLQ) handling to compensation consumers and ensure every compensation action publishes a result event even when the underlying operation was already rolled back.

```python
async def handle_release_reservation(self, command: Dict):
    try:
        await self.release_reservation(command["original_result"]["reservation_id"])
    except ReservationNotFoundError:
        pass  # Already released — treat as success
    # Always publish completion, regardless of outcome
    await self.event_publisher.publish("SagaCompensationCompleted", {
        "saga_id": command["saga_id"],
        "step_name": "reserve_inventory"
    })
```

### Duplicate saga executions on restart

If your orchestrator service restarts mid-saga, it may replay events and re-execute already-completed steps. Guard every step action with an idempotency key — see **Template 3** above.

### Choreography saga losing events

In a choreography-based saga, a downstream service may miss an event if it was offline when published. Use a durable message broker (Kafka with replication, RabbitMQ with persistence) and store the current saga state in a dedicated `saga_log` table so you can replay from the last known good step.

### Timeout firing before a slow-but-valid step completes

A step like `create_shipment` might take up to 15 minutes during peak load but your global timeout is 5 minutes, causing spurious compensation. Make step timeouts configurable per step type — see `references/advanced-patterns.md` for the `TimeoutSagaOrchestrator` implementation and the `STEP_TIMEOUTS` dict pattern.

### Compensation order not matching execution order

When two steps both complete before a failure is detected, compensation must run in strict reverse order or you leave data in an inconsistent state. Verify that `_compensate()` iterates from `current_step - 1` down to `0`, and add an integration test that deliberately fails at each step index to confirm correct rollback order.

---

## Advanced Patterns

The `references/` directory contains production-grade implementations not needed for most sagas:

- **`references/advanced-patterns.md`** — Full `SagaOrchestrator` abstract base class, `TimeoutSagaOrchestrator` with per-step deadlines, detailed bank transfer compensating transaction chain, Prometheus instrumentation, stuck saga PromQL alerts, and DLQ recovery worker.

---

## Related Skills

- `cqrs-implementation` — Pair sagas with CQRS for read-model updates after each step completes
- `event-store-design` — Store saga events in an event store for full audit trail and replay capability
- `workflow-orchestration-patterns` — Higher-level workflow engines (Temporal, Conductor) that build on saga concepts
