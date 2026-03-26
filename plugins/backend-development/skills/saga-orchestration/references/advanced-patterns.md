# Saga Orchestration — Advanced Patterns

Complex implementations extracted from core skill for deeper reference.

---

## Full Saga Orchestrator Base Class

The abstract base handles all state transitions, compensation ordering, and event publishing. Subclass this for every saga type in your system.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import uuid


class SagaState(Enum):
    STARTED = "started"
    PENDING = "pending"
    COMPENSATING = "compensating"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SagaStep:
    name: str
    action: str
    compensation: str
    status: str = "pending"
    result: Optional[Dict] = None
    error: Optional[str] = None
    executed_at: Optional[datetime] = None
    compensated_at: Optional[datetime] = None
    timeout_at: Optional[datetime] = None


@dataclass
class Saga:
    saga_id: str
    saga_type: str
    state: SagaState
    data: Dict[str, Any]
    steps: List[SagaStep]
    current_step: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class SagaOrchestrator(ABC):
    """Base class for all saga orchestrators.

    Responsibilities:
    - Execute steps in sequence via async command messages
    - Trigger compensation in reverse order on any failure
    - Persist saga state after every transition
    - Publish domain events on completion and failure
    """

    def __init__(self, saga_store, event_publisher):
        self.saga_store = saga_store
        self.event_publisher = event_publisher

    @abstractmethod
    def define_steps(self, data: Dict) -> List[SagaStep]:
        """Define the ordered saga steps for this workflow."""
        pass

    @property
    @abstractmethod
    def saga_type(self) -> str:
        """Unique identifier for this saga type (e.g., 'OrderFulfillment')."""
        pass

    async def start(self, data: Dict) -> Saga:
        """Start a new saga instance."""
        saga = Saga(
            saga_id=str(uuid.uuid4()),
            saga_type=self.saga_type,
            state=SagaState.STARTED,
            data=data,
            steps=self.define_steps(data)
        )
        await self.saga_store.save(saga)
        await self._execute_next_step(saga)
        return saga

    async def handle_step_completed(self, saga_id: str, step_name: str, result: Dict):
        """Handle a successful step reply from a participant service."""
        saga = await self.saga_store.get(saga_id)

        for step in saga.steps:
            if step.name == step_name:
                step.status = "completed"
                step.result = result
                step.executed_at = datetime.utcnow()
                break

        saga.current_step += 1
        saga.updated_at = datetime.utcnow()

        if saga.current_step >= len(saga.steps):
            saga.state = SagaState.COMPLETED
            await self.saga_store.save(saga)
            await self._on_saga_completed(saga)
        else:
            saga.state = SagaState.PENDING
            await self.saga_store.save(saga)
            await self._execute_next_step(saga)

    async def handle_step_failed(self, saga_id: str, step_name: str, error: str):
        """Handle a step failure and begin compensation."""
        saga = await self.saga_store.get(saga_id)

        for step in saga.steps:
            if step.name == step_name:
                step.status = "failed"
                step.error = error
                break

        saga.state = SagaState.COMPENSATING
        saga.updated_at = datetime.utcnow()
        await self.saga_store.save(saga)
        await self._compensate(saga)

    async def _execute_next_step(self, saga: Saga):
        """Publish the command for the current step."""
        if saga.current_step >= len(saga.steps):
            return

        step = saga.steps[saga.current_step]
        step.status = "executing"
        await self.saga_store.save(saga)

        await self.event_publisher.publish(
            step.action,
            {
                "saga_id": saga.saga_id,
                "step_name": step.name,
                **saga.data
            }
        )

    async def _compensate(self, saga: Saga):
        """Execute compensation steps in reverse order."""
        for i in range(saga.current_step - 1, -1, -1):
            step = saga.steps[i]
            if step.status == "completed":
                step.status = "compensating"
                await self.saga_store.save(saga)

                await self.event_publisher.publish(
                    step.compensation,
                    {
                        "saga_id": saga.saga_id,
                        "step_name": step.name,
                        "original_result": step.result,
                        **saga.data
                    }
                )

    async def handle_compensation_completed(self, saga_id: str, step_name: str):
        """Mark a compensation step done and check if all are finished."""
        saga = await self.saga_store.get(saga_id)

        for step in saga.steps:
            if step.name == step_name:
                step.status = "compensated"
                step.compensated_at = datetime.utcnow()
                break

        all_compensated = all(
            s.status in ("compensated", "pending", "failed")
            for s in saga.steps
        )

        if all_compensated:
            saga.state = SagaState.FAILED
            await self._on_saga_failed(saga)

        await self.saga_store.save(saga)

    async def _on_saga_completed(self, saga: Saga):
        await self.event_publisher.publish(
            f"{self.saga_type}Completed",
            {"saga_id": saga.saga_id, **saga.data}
        )

    async def _on_saga_failed(self, saga: Saga):
        await self.event_publisher.publish(
            f"{self.saga_type}Failed",
            {"saga_id": saga.saga_id, "error": "Saga failed after compensation", **saga.data}
        )
```

---

## Saga Orchestrator with Per-Step Timeouts

Each step gets an independent deadline. The scheduler fires a timeout job; if the step is still `executing` at that point, compensation begins automatically. Use this when participant SLAs vary widely (e.g., payment = 30 s, shipping label = 15 min).

```python
class TimeoutSagaOrchestrator(SagaOrchestrator):
    """Extends the base orchestrator with configurable per-step timeouts."""

    # Override per saga subclass as needed
    STEP_TIMEOUTS: Dict[str, timedelta] = {
        "reserve_inventory": timedelta(minutes=2),
        "process_payment":   timedelta(minutes=1),
        "create_shipment":   timedelta(minutes=15),
        "send_confirmation": timedelta(minutes=2),
    }

    def __init__(self, saga_store, event_publisher, scheduler):
        super().__init__(saga_store, event_publisher)
        self.scheduler = scheduler

    async def _execute_next_step(self, saga: Saga):
        if saga.current_step >= len(saga.steps):
            return

        step = saga.steps[saga.current_step]
        step.status = "executing"
        step.timeout_at = datetime.utcnow() + self.STEP_TIMEOUTS.get(
            step.name, timedelta(minutes=5)
        )
        await self.saga_store.save(saga)

        # Schedule the timeout watchdog
        await self.scheduler.schedule(
            job_id=f"saga_timeout_{saga.saga_id}_{step.name}",
            handler=self._check_timeout,
            payload={"saga_id": saga.saga_id, "step_name": step.name},
            run_at=step.timeout_at
        )

        await self.event_publisher.publish(
            step.action,
            {"saga_id": saga.saga_id, "step_name": step.name, **saga.data}
        )

    async def _check_timeout(self, data: Dict):
        """Called by the scheduler when a step deadline is reached."""
        saga = await self.saga_store.get(data["saga_id"])
        step = next((s for s in saga.steps if s.name == data["step_name"]), None)

        if step and step.status == "executing":
            await self.handle_step_failed(
                data["saga_id"],
                data["step_name"],
                f"Step '{data['step_name']}' timed out after {self.STEP_TIMEOUTS.get(data['step_name'])}"
            )

    async def handle_step_completed(self, saga_id: str, step_name: str, result: Dict):
        """Cancel the timeout job before processing the success reply."""
        await self.scheduler.cancel(f"saga_timeout_{saga_id}_{step_name}")
        await super().handle_step_completed(saga_id, step_name, result)
```

---

## Detailed Compensating Transaction Chains

The pattern below shows a full compensation chain for a bank transfer saga. Each compensation is idempotent and always emits a result event — even when the underlying resource is already in the desired state.

```python
class BankTransferSaga(SagaOrchestrator):
    """Saga for transferring funds between accounts across services."""

    @property
    def saga_type(self) -> str:
        return "BankTransfer"

    def define_steps(self, data: Dict) -> List[SagaStep]:
        return [
            SagaStep(
                name="debit_source",
                action="AccountService.DebitAccount",
                compensation="AccountService.CreditAccount"  # reverse the debit
            ),
            SagaStep(
                name="create_transfer_record",
                action="LedgerService.CreateTransfer",
                compensation="LedgerService.VoidTransfer"
            ),
            SagaStep(
                name="credit_destination",
                action="AccountService.CreditDestinationAccount",
                compensation="AccountService.DebitAccount"  # reverse the credit
            ),
            SagaStep(
                name="notify_parties",
                action="NotificationService.SendTransferConfirmation",
                compensation="NotificationService.SendTransferFailureNotice"
            ),
        ]


class AccountService:
    async def handle_debit_account(self, command: Dict):
        idempotency_key = f"debit-{command['saga_id']}-{command['account_id']}"
        existing = await self.ledger.find_by_key(idempotency_key)
        if existing:
            await self._publish_completed(command, {"transaction_id": existing.id})
            return
        try:
            txn = await self.ledger.debit(
                account_id=command["source_account_id"],
                amount=command["amount"],
                idempotency_key=idempotency_key
            )
            await self._publish_completed(command, {"transaction_id": txn.id})
        except InsufficientFundsError as e:
            await self._publish_failed(command, str(e))

    async def handle_credit_account(self, command: Dict):
        """Compensation: credit back a previously debited account."""
        idempotency_key = f"credit-comp-{command['saga_id']}-{command['account_id']}"
        existing = await self.ledger.find_by_key(idempotency_key)
        if not existing:
            await self.ledger.credit(
                account_id=command["source_account_id"],
                amount=command["amount"],
                idempotency_key=idempotency_key
            )
        # Always publish — even if already credited
        await self.event_publisher.publish("SagaCompensationCompleted", {
            "saga_id": command["saga_id"],
            "step_name": "debit_source"
        })
```

---

## Production Monitoring Setup

### Prometheus Metrics

Expose saga health metrics for alerting on stuck sagas and compensation rates.

```python
from prometheus_client import Counter, Histogram, Gauge
import time

saga_started_total = Counter(
    "saga_started_total",
    "Total sagas started",
    ["saga_type"]
)
saga_completed_total = Counter(
    "saga_completed_total",
    "Total sagas completed successfully",
    ["saga_type"]
)
saga_failed_total = Counter(
    "saga_failed_total",
    "Total sagas that failed after compensation",
    ["saga_type"]
)
saga_compensating_total = Counter(
    "saga_compensating_total",
    "Total sagas that entered compensation",
    ["saga_type"]
)
saga_duration_seconds = Histogram(
    "saga_duration_seconds",
    "Saga execution duration",
    ["saga_type", "outcome"],
    buckets=[1, 5, 15, 30, 60, 300, 600]
)
saga_stuck_gauge = Gauge(
    "saga_stuck_count",
    "Sagas stuck in COMPENSATING or PENDING > threshold",
    ["saga_type", "state"]
)


class InstrumentedSagaOrchestrator(SagaOrchestrator):
    """Wraps base orchestrator with Prometheus instrumentation."""

    async def start(self, data: Dict) -> Saga:
        saga_started_total.labels(saga_type=self.saga_type).inc()
        saga = await super().start(data)
        saga._start_time = time.monotonic()
        return saga

    async def _on_saga_completed(self, saga: Saga):
        duration = time.monotonic() - getattr(saga, "_start_time", 0)
        saga_completed_total.labels(saga_type=self.saga_type).inc()
        saga_duration_seconds.labels(
            saga_type=self.saga_type, outcome="completed"
        ).observe(duration)
        await super()._on_saga_completed(saga)

    async def _on_saga_failed(self, saga: Saga):
        duration = time.monotonic() - getattr(saga, "_start_time", 0)
        saga_failed_total.labels(saga_type=self.saga_type).inc()
        saga_duration_seconds.labels(
            saga_type=self.saga_type, outcome="failed"
        ).observe(duration)
        await super()._on_saga_failed(saga)
```

### Stuck Saga Detection Query (Prometheus)

Flag sagas that have been in COMPENSATING or PENDING for more than 10 minutes:

```promql
# Alert: saga stuck in compensation for > 10 min
increase(saga_compensating_total[10m]) - increase(saga_failed_total[10m]) > 0

# Alert: saga completion rate drops below 95%
(
  rate(saga_completed_total[5m]) /
  (rate(saga_completed_total[5m]) + rate(saga_failed_total[5m]))
) < 0.95
```

### Dead Letter Queue Recovery

When a compensation handler throws an unhandled exception the message lands on a DLQ. Implement a recovery worker that replays DLQ messages with exponential backoff:

```python
class SagaDLQRecovery:
    """Replays failed compensation messages from the dead-letter queue."""

    MAX_RETRIES = 5
    BASE_DELAY_SECONDS = 10

    async def process_dlq_message(self, message: Dict, attempt: int):
        delay = self.BASE_DELAY_SECONDS * (2 ** attempt)
        if attempt >= self.MAX_RETRIES:
            await self._move_to_poison_queue(message)
            await self._alert_on_call(message)
            return

        await asyncio.sleep(delay)
        try:
            await self.event_publisher.publish(message["original_topic"], message["payload"])
        except Exception as e:
            await self.process_dlq_message(message, attempt + 1)
```

---

## See Also

- Core patterns and decision tables: `../SKILL.md`
- `cqrs-implementation` skill — read-model updates after each saga step
- `event-store-design` skill — durable saga event log and replay capability
