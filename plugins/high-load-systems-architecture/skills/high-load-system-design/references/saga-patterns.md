# Saga Patterns Reference

## Overview

Distributed transactions across microservices using compensating transactions.

---

## Choreography-Based Saga

**Definition**: Services coordinate by subscribing to events.

**Architecture**:
```
Order Service → OrderCreated event
                     ↓
Payment Service → PaymentProcessed event
                     ↓
Inventory Service → InventoryReserved event
                     ↓
Shipping Service → OrderShipped event
```

**Compensation Flow**:
```
Shipping Fails
    ↓
Inventory Service → ReleaseInventory (compensate)
    ↓
Payment Service → RefundPayment (compensate)
    ↓
Order Service → CancelOrder
```

**Example**:
```python
# Order Service
def create_order(order_data):
    order = db.insert(orders, order_data)
    publish_event('OrderCreated', {
        'order_id': order.id,
        'user_id': order.user_id,
        'items': order.items
    })

# Payment Service
@subscribe('OrderCreated')
def handle_order_created(event):
    try:
        payment = process_payment(event.user_id, event.total)
        publish_event('PaymentProcessed', {
            'order_id': event.order_id,
            'payment_id': payment.id
        })
    except PaymentFailed:
        publish_event('PaymentFailed', {
            'order_id': event.order_id
        })

# Order Service (compensation)
@subscribe('PaymentFailed')
def handle_payment_failed(event):
    db.update(orders, event.order_id, status='cancelled')
```

**Pros**:
- No central coordinator
- Services decoupled
- Fault tolerant

**Cons**:
- Hard to understand flow
- Complex debugging
- Cyclic dependencies risk

---

## Orchestration-Based Saga

**Definition**: Central coordinator manages workflow.

**Architecture**:
```
Saga Orchestrator
├─ Step 1: Create Order → Order Service
├─ Step 2: Process Payment → Payment Service
├─ Step 3: Reserve Inventory → Inventory Service
└─ Step 4: Ship Order → Shipping Service
```

**Implementation**:
```python
class OrderSagaOrchestrator:
    def execute(self, order_data):
        saga = SagaInstance(order_data)

        try:
            # Step 1: Create order
            order = self.order_service.create(order_data)
            saga.add_compensation(
                lambda: self.order_service.cancel(order.id)
            )

            # Step 2: Process payment
            payment = self.payment_service.charge(
                order.user_id,
                order.total
            )
            saga.add_compensation(
                lambda: self.payment_service.refund(payment.id)
            )

            # Step 3: Reserve inventory
            reservation = self.inventory_service.reserve(order.items)
            saga.add_compensation(
                lambda: self.inventory_service.release(reservation.id)
            )

            # Step 4: Ship order
            shipment = self.shipping_service.ship(order.id)

            return saga.complete()

        except Exception as e:
            saga.compensate()  # Execute all compensations in reverse
            raise SagaFailed(e)
```

**Pros**:
- Easy to understand
- Centralized logic
- Easier debugging

**Cons**:
- Single point of failure
- Orchestrator complexity
- Service coupling to orchestrator

---

## Comparison

| Aspect | Choreography | Orchestration |
|--------|--------------|---------------|
| Coupling | Low | Medium |
| Complexity | High | Medium |
| Debugging | Hard | Easy |
| Single Point of Failure | No | Yes |
| Use Case | Simple flows | Complex flows |
