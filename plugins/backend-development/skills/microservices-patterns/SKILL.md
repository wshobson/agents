---
name: microservices-patterns
description: Design microservices architectures with service boundaries, event-driven communication, and resilience patterns. Use when building distributed systems, decomposing monoliths, or implementing microservices.
---

# Microservices Patterns

Master microservices architecture patterns including service boundaries, inter-service communication, data management, and resilience patterns for building distributed systems.

## When to Use This Skill

- Decomposing monoliths into microservices
- Designing service boundaries and contracts
- Implementing inter-service communication
- Managing distributed data and transactions
- Building resilient distributed systems
- Implementing service discovery and load balancing
- Designing event-driven architectures

## Core Concepts

### 1. Service Decomposition Strategies

**By Business Capability**

- Organize services around business functions
- Each service owns its domain
- Example: OrderService, PaymentService, InventoryService

**By Subdomain (DDD)**

- Core domain, supporting subdomains
- Bounded contexts map to services
- Clear ownership and responsibility

**Strangler Fig Pattern**

- Gradually extract from monolith
- New functionality as microservices
- Proxy routes to old/new systems

### 2. Communication Patterns

**Synchronous (Request/Response)**

- REST APIs
- gRPC
- GraphQL

**Asynchronous (Events/Messages)**

- Event streaming (Kafka)
- Message queues (RabbitMQ, SQS)
- Pub/Sub patterns

### 3. Data Management

**Database Per Service**

- Each service owns its data
- No shared databases
- Loose coupling

**Saga Pattern**

- Distributed transactions
- Compensating actions
- Eventual consistency

### 4. Resilience Patterns

**Circuit Breaker**

- Fail fast on repeated errors
- Prevent cascade failures

**Retry with Backoff**

- Transient fault handling
- Exponential backoff

**Bulkhead**

- Isolate resources
- Limit impact of failures

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

