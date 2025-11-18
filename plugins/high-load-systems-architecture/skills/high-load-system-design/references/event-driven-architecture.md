# Event-Driven Architecture Reference

## Core Concepts

### Event Types

**1. Domain Events**: Business-meaningful changes
- OrderPlaced, UserRegistered, PaymentProcessed

**2. Integration Events**: Cross-system communication
- CustomerCreatedEvent, InventoryUpdatedEvent

**3. Notification Events**: Alerts and notifications
- EmailSent, SMSDelivered

---

## Patterns

### Event Sourcing

**Definition**: Store all changes as sequence of events.

**Architecture**:
```
Command → Aggregate → Event Store
              ↓
          Event Bus → Projections (Read Models)
```

**Benefits**:
- Complete audit trail
- Temporal queries (state at any point in time)
- Event replay for debugging

**Example**:
```python
# Events
class OrderCreated:
    order_id: str
    user_id: str
    total: Decimal

class OrderPaid:
    order_id: str
    payment_id: str

# Aggregate
class Order:
    def __init__(self, order_id):
        self.id = order_id
        self.status = 'pending'
        self.events = []

    def create(self, user_id, total):
        event = OrderCreated(self.id, user_id, total)
        self.apply(event)
        self.events.append(event)

    def pay(self, payment_id):
        event = OrderPaid(self.id, payment_id)
        self.apply(event)
        self.events.append(event)

    def apply(self, event):
        if isinstance(event, OrderCreated):
            self.status = 'created'
        elif isinstance(event, OrderPaid):
            self.status = 'paid'
```

---

### Event Bus (Kafka)

**Configuration**:
```yaml
topics:
  - name: orders.created
    partitions: 12
    replication: 3
    retention: 7d

  - name: orders.paid
    partitions: 12
    replication: 3
    retention: 7d

consumers:
  - group: email-service
    topics: [orders.created]
    offset: earliest

  - group: analytics-service
    topics: [orders.created, orders.paid]
    offset: latest
```

---

## Best Practices

1. **Idempotency**: Handle duplicate events
2. **Ordering**: Use partitioning by key
3. **Schema Evolution**: Use schema registry
4. **Dead Letter Queue**: Handle failed events
5. **Monitoring**: Track lag and throughput
