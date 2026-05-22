# python-background-jobs — detailed worked examples

## Advanced Patterns

### Pattern 5: Dead Letter Queue

Handle permanently failed tasks for manual inspection.

```python
@app.task(bind=True, max_retries=3)
def process_webhook(self, webhook_id: str, payload: dict) -> None:
    """Process webhook with DLQ for failures."""
    try:
        result = send_webhook(payload)
        if not result.success:
            raise WebhookFailedError(result.error)
    except Exception as e:
        if self.request.retries >= self.max_retries:
            # Move to dead letter queue for manual inspection
            dead_letter_queue.send({
                "task": "process_webhook",
                "webhook_id": webhook_id,
                "payload": payload,
                "error": str(e),
                "attempts": self.request.retries + 1,
                "failed_at": datetime.utcnow().isoformat(),
            })
            logger.error(
                "Webhook moved to DLQ after max retries",
                webhook_id=webhook_id,
                error=str(e),
            )
            return

        # Exponential backoff retry
        raise self.retry(exc=e, countdown=2 ** self.request.retries * 60)
```

### Pattern 6: Status Polling Endpoint

Provide an endpoint for clients to check job status.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str) -> JobStatusResponse:
    """Get current status of a background job."""
    job = await jobs_repo.get(job_id)

    if job is None:
        raise HTTPException(404, f"Job {job_id} not found")

    return JobStatusResponse(
        job_id=job.id,
        status=job.status.value,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at,
        result=job.result if job.status == JobStatus.SUCCEEDED else None,
        error=job.error if job.status == JobStatus.FAILED else None,
        # Helpful for clients
        is_terminal=job.status in (JobStatus.SUCCEEDED, JobStatus.FAILED),
    )
```

### Pattern 7: Task Chaining and Workflows

Compose complex workflows from simple tasks.

```python
from celery import chain, group, chord

# Simple chain: A → B → C
workflow = chain(
    extract_data.s(source_id),
    transform_data.s(),
    load_data.s(destination_id),
)

# Parallel execution: A, B, C all at once
parallel = group(
    send_email.s(user_email),
    send_sms.s(user_phone),
    update_analytics.s(event_data),
)

# Chord: Run tasks in parallel, then a callback
# Process all items, then send completion notification
workflow = chord(
    [process_item.s(item_id) for item_id in item_ids],
    send_completion_notification.s(batch_id),
)

workflow.apply_async()
```

### Pattern 8: Alternative Task Queues

Choose the right tool for your needs.

**RQ (Redis Queue)**: Simple, Redis-based
```python
from rq import Queue
from redis import Redis

queue = Queue(connection=Redis())
job = queue.enqueue(send_email, "user@example.com", "Subject", "Body")
```

**Dramatiq**: Modern Celery alternative
```python
import dramatiq
from dramatiq.brokers.redis import RedisBroker

dramatiq.set_broker(RedisBroker())

@dramatiq.actor
def send_email(to: str, subject: str, body: str) -> None:
    email_client.send(to, subject, body)
```

**Cloud-native options:**
- AWS SQS + Lambda
- Google Cloud Tasks
- Azure Functions
