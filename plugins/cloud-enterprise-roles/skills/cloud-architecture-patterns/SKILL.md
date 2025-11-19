---
name: cloud-architecture-patterns
description: Cloud-native architecture patterns including microservices, serverless, container orchestration, event-driven architectures и multi-cloud strategies. Используйте когда проектируете cloud architecture, выбираете architecture patterns или мигрируете в облако.
---

# Cloud Architecture Patterns

## Когда использовать этот скилл

- Проектирование cloud-native архитектур
- Выбор оптимальных architecture patterns для use case
- Миграция legacy систем в облако
- Проектирование serverless архитектур
- Проектирование event-driven систем
- Multi-cloud или hybrid cloud стратегии
- Optimizing для cost, performance, scalability

## Основные архитектурные паттерны

### Microservices Architecture

**Принципы проектирования:**

```yaml
Service Design:
  Single Responsibility:
    description: "Каждый сервис отвечает за одну бизнес-capability"
    example: "OrderService только для заказов, не смешивать с inventory"

  Bounded Context (DDD):
    description: "Четкие границы домена для каждого сервиса"
    example: |
      Sales Context: Order, Customer, Payment
      Inventory Context: Product, Stock, Warehouse
      Shipping Context: Shipment, Delivery, Tracking

  Database per Service:
    description: "Каждый сервис владеет своей базой данных"
    anti_pattern: "Shared database across services"
    benefits:
      - "Loose coupling"
      - "Independent scaling"
      - "Technology freedom (polyglot persistence)"
    challenges:
      - "Distributed transactions (use Saga pattern)"
      - "Data consistency (eventual consistency)"

Communication Patterns:
  Synchronous:
    REST API:
      when: "Request-response, CRUD operations"
      format: "JSON over HTTP"
      example: "GET /api/orders/{id}"
      tools: "API Gateway, Load Balancer"

    GraphQL:
      when: "Flexible queries, mobile apps, multiple clients"
      benefits: "Client определяет нужные поля, single endpoint"
      example: |
        query {
          order(id: "123") {
            id
            customer { name }
            items { product { name } quantity }
          }
        }

    gRPC:
      when: "Internal service-to-service, high performance"
      benefits: "Binary protocol, HTTP/2, code generation"
      example: "service OrderService { rpc GetOrder(OrderId) returns (Order); }"

  Asynchronous:
    Message Queue:
      when: "Decoupling, asynchronous processing, retry logic"
      patterns: "Point-to-point, work queues"
      tools:
        AWS: "SQS"
        Azure: "Service Bus Queues"
        GCP: "Cloud Tasks"
      example: "Order created → Send to fulfillment queue"

    Pub/Sub:
      when: "Event broadcasting to multiple consumers"
      patterns: "Fan-out, event notification"
      tools:
        AWS: "SNS, EventBridge"
        Azure: "Event Grid, Service Bus Topics"
        GCP: "Pub/Sub"
      example: "OrderCreated event → Notify inventory, shipping, analytics"

    Event Streaming:
      when: "Real-time data pipelines, event sourcing"
      tools:
        - "Apache Kafka, Amazon Kinesis, Azure Event Hubs"
      example: "Stream order events for real-time analytics"

Service Mesh:
  purpose: "Service-to-service communication infrastructure"
  features:
    - "Service discovery"
    - "Load balancing"
    - "Circuit breaking"
    - "Retries and timeouts"
    - "Mutual TLS (mTLS)"
    - "Distributed tracing"
    - "Traffic management (canary, blue-green)"
  implementations:
    - name: "Istio"
      platform: "Kubernetes"
    - name: "Linkerd"
      platform: "Kubernetes, lightweight"
    - name: "AWS App Mesh"
      platform: "AWS ECS, EKS"
    - name: "Consul Connect"
      platform: "Multi-platform"

API Gateway Pattern:
  responsibilities:
    - "Request routing to backend services"
    - "Authentication & authorization"
    - "Rate limiting & throttling"
    - "Request/response transformation"
    - "Caching"
    - "API composition (aggregation)"
  implementations:
    - "AWS API Gateway"
    - "Azure API Management"
    - "Google Cloud Apigee"
    - "Kong, Tyk (open-source)"
```

### Serverless Architecture

**Function-as-a-Service (FaaS) Patterns:**

```yaml
Stateless Functions:
  principle: "Функции не хранят состояние между invocations"
  state_management:
    - "DynamoDB, Cosmos DB для persistent state"
    - "Redis, Memcached для session state"
    - "S3, Blob Storage для file state"

  example_use_cases:
    - "API endpoints (REST, GraphQL)"
    - "Data transformation (ETL)"
    - "Image/video processing"
    - "Scheduled tasks (cron jobs)"
    - "Event processing (S3 uploads, DB changes)"

Cold Start Optimization:
  problem: "Первая invocation медленная (100ms - 5s)"
  solutions:
    provisioned_concurrency:
      description: "Pre-warmed instances"
      cost: "Higher cost но predictable latency"
      platforms: "AWS Lambda, Azure Functions"

    runtime_optimization:
      - "Использовать compiled languages (Go, Rust) vs interpreted (Python, Node)"
      - "Minimize dependencies"
      - "Lazy initialization"

    keep_warm_strategies:
      - "Scheduled pings каждые 5 минут"
      - "CloudWatch scheduled events"

Function Composition:
  orchestration:
    AWS_Step_Functions:
      description: "Visual workflow для serverless functions"
      patterns:
        - "Sequential: A → B → C"
        - "Parallel: A → [B1, B2, B3] → C"
        - "Choice: if-then-else логика"
        - "Wait: delay execution"
        - "Retry: automatic retries with backoff"
      example: |
        OrderProcessing:
          ValidateOrder → CheckInventory → ProcessPayment
                                        ↓
          [ReserveInventory, CalculateShipping] → CreateShipment

    Azure_Durable_Functions:
      description: "Stateful workflows в serverless"
      patterns:
        - "Function chaining"
        - "Fan-out/fan-in"
        - "Async HTTP APIs"
        - "Monitoring"
        - "Human interaction"

    GCP_Cloud_Workflows:
      description: "YAML-based serverless orchestration"
      example: |
        - validateOrder:
            call: http.post
            args: {url: "${validateUrl}"}
        - checkInventory:
            call: http.get
            args: {url: "${inventoryUrl}"}

Backend-as-a-Service (BaaS):
  managed_services:
    Authentication:
      - "AWS Cognito"
      - "Azure AD B2C"
      - "Firebase Auth"
      - "Auth0"

    Database:
      - "DynamoDB (NoSQL key-value/document)"
      - "Firestore (NoSQL document, real-time)"
      - "Cosmos DB (Multi-model)"
      - "Aurora Serverless (Relational)"

    Storage:
      - "S3, Blob Storage, Cloud Storage (Object)"
      - "EFS, Azure Files, Filestore (File)"

    API:
      - "API Gateway (REST)"
      - "AWS AppSync (GraphQL)"
      - "Azure API Management"

Event-Driven Serverless:
  trigger_types:
    HTTP_Triggers:
      - "API Gateway → Lambda"
      - "HTTP endpoint → Cloud Function"

    Storage_Triggers:
      - "S3 object created → Process image"
      - "Blob upload → Extract metadata"

    Database_Triggers:
      - "DynamoDB Streams → Sync to Elasticsearch"
      - "Cosmos DB Change Feed → Update cache"

    Queue_Triggers:
      - "SQS message → Process order"
      - "Service Bus queue → Handle event"

    Scheduled_Triggers:
      - "CloudWatch Events (cron) → Daily report"
      - "Timer trigger → Cleanup old data"
```

### Event-Driven Architecture

**Event Sourcing + CQRS:**

```yaml
Event Sourcing:
  concept: "Состояние хранится как последовательность events"

  event_store_design:
    schema: |
      events:
        - event_id (UUID)
        - aggregate_id (entity ID)
        - event_type (OrderCreated, OrderShipped)
        - event_version (optimistic locking)
        - event_data (JSON payload)
        - timestamp
        - metadata (user, IP, etc.)

  append_only: "Events никогда не удаляются/изменяются"

  state_reconstruction: "Current state = replay всех events"

  benefits:
    - "Complete audit trail"
    - "Time travel (состояние на любой момент времени)"
    - "Event replay для bug fixing"
    - "Multiple read models из одного event stream"

  challenges:
    - "Schema evolution (event versioning)"
    - "Performance (snapshot для reduce replay time)"
    - "Storage growth (archival strategy)"

CQRS:
  principle: "Разделить write model и read model"

  write_side:
    - "Commands → Aggregate → Events → Event Store"
    - "Enforces business rules"
    - "Optimized для transactional consistency"
    - "Normalized schema"

  read_side:
    - "Events → Projections → Read Models"
    - "Materialized views для queries"
    - "Denormalized для performance"
    - "Multiple read models для different use cases"
    - "Eventual consistency"

  example_read_models:
    OrderList:
      database: "PostgreSQL"
      schema: "Flat table для list views"

    OrderSearch:
      database: "Elasticsearch"
      schema: "Indexed для full-text search"

    OrderCache:
      database: "Redis"
      schema: "Key-value для fast lookup"

  synchronization:
    - "Event bus (Kafka, EventBridge) transports events"
    - "Read model subscribers update their databases"
    - "Idempotent event handlers (handle duplicates)"

Saga Pattern:
  problem: "Distributed transactions across microservices"

  solution: "Sequence of local transactions + compensating actions"

  choreography_based:
    description: "Децентрализованная координация через events"
    flow: |
      OrderService: CreateOrder → OrderCreated event
      ↓
      InventoryService: ReserveInventory → InventoryReserved event
      ↓
      PaymentService: ProcessPayment → PaymentProcessed event
      ↓
      ShippingService: CreateShipment → ShipmentCreated event

    failure_handling: |
      PaymentService: PaymentFailed event
      ↓
      InventoryService: ReleaseInventory (compensating action)
      ↓
      OrderService: CancelOrder (compensating action)

  orchestration_based:
    description: "Централизованная координация через orchestrator"
    orchestrator: "OrderSaga координирует весь flow"
    flow: |
      OrderSaga:
        1. Call InventoryService.ReserveInventory()
        2. Call PaymentService.ProcessPayment()
        3. Call ShippingService.CreateShipment()

      On failure:
        1. Call PaymentService.RefundPayment()
        2. Call InventoryService.ReleaseInventory()
        3. Call OrderService.CancelOrder()

    implementation: "AWS Step Functions, Azure Durable Functions"
```

### Container Orchestration (Kubernetes)

**Production-Ready K8s Patterns:**

```yaml
Deployment Strategies:
  Rolling_Update:
    description: "Постепенная замена pods"
    strategy:
      maxUnavailable: 1  # Max pods offline
      maxSurge: 1        # Max extra pods during update
    zero_downtime: true
    rollback: "Automatic on health check failure"

  Blue_Green:
    description: "Два полных environments, switch traffic"
    implementation: "Service selector swap"
    benefits: "Instant rollback, testing in production"
    cost: "2x resources during deployment"

  Canary:
    description: "Постепенный rollout (5% → 25% → 50% → 100%)"
    implementation: "Service mesh (Istio), Flagger"
    benefits: "Early error detection, controlled risk"
    metrics_monitoring: "Error rate, latency, custom business metrics"

Auto-Scaling:
  Horizontal_Pod_Autoscaler:
    triggers:
      - "CPU utilization > 70%"
      - "Memory utilization > 80%"
      - "Custom metrics (requests/sec, queue depth)"
    configuration: |
      apiVersion: autoscaling/v2
      kind: HorizontalPodAutoscaler
      metadata:
        name: app-hpa
      spec:
        scaleTargetRef:
          apiVersion: apps/v1
          kind: Deployment
          name: app
        minReplicas: 2
        maxReplicas: 10
        metrics:
        - type: Resource
          resource:
            name: cpu
            target:
              type: Utilization
              averageUtilization: 70

  Vertical_Pod_Autoscaler:
    purpose: "Automatically adjust CPU/memory requests"
    when: "Workload resource needs vary"

  Cluster_Autoscaler:
    purpose: "Add/remove nodes based on pod scheduling needs"
    platforms: "EKS, AKS, GKE"

  KEDA:
    purpose: "Event-driven autoscaling"
    scalers:
      - "Kafka lag"
      - "Queue depth (SQS, Service Bus)"
      - "Prometheus metrics"
      - "Cron schedules"

Service Mesh:
  Istio_Features:
    traffic_management:
      - "Request routing (A/B testing, canary)"
      - "Load balancing (round-robin, least connection)"
      - "Timeouts, retries, circuit breakers"

    security:
      - "Mutual TLS between services"
      - "Authentication (JWT validation)"
      - "Authorization (RBAC)"

    observability:
      - "Distributed tracing (Jaeger, Zipkin)"
      - "Metrics (Prometheus, Grafana)"
      - "Access logs"

  configuration_example: |
    apiVersion: networking.istio.io/v1alpha3
    kind: VirtualService
    metadata:
      name: reviews
    spec:
      hosts:
      - reviews
      http:
      - match:
        - headers:
            user:
              exact: "test-user"
        route:
        - destination:
            host: reviews
            subset: v2
      - route:
        - destination:
            host: reviews
            subset: v1
          weight: 90
        - destination:
            host: reviews
            subset: v2
          weight: 10  # 10% canary traffic
```

## Multi-Cloud & Hybrid Patterns

**Cloud-Agnostic Design:**

```yaml
Abstraction Layers:
  Infrastructure_as_Code:
    Terraform:
      benefits: "Multi-cloud support (AWS, Azure, GCP)"
      modules: "Reusable infrastructure components"
      example: |
        resource "aws_s3_bucket" "data" { }
        resource "azurerm_storage_account" "data" { }
        resource "google_storage_bucket" "data" { }

  Container_Orchestration:
    Kubernetes:
      portability: "Runs on any cloud или on-premises"
      managed_services: "EKS, AKS, GKE"
      distributions: "OpenShift, Rancher, VMware Tanzu"

  Serverless_Abstraction:
    CloudEvents:
      description: "Standard для event data format"
      portability: "Consistent events across clouds"

    Serverless_Framework:
      description: "Deploy functions to AWS, Azure, GCP"
      configuration: "YAML-based, cloud-agnostic"

Multi-Cloud Use Cases:
  Best_of_Breed:
    example: |
      AWS: Broad service catalog, Lambda, S3
      Azure: Microsoft integration, AD, .NET
      GCP: Data/ML (BigQuery, Vertex AI), Kubernetes (GKE)

  Disaster_Recovery:
    pattern: "Active (AWS) - Passive (Azure)"
    failover: "DNS failover или global load balancer"

  Data_Residency:
    example: "EU data in Azure Europe, US data in AWS"
    compliance: "GDPR, data sovereignty"

  Avoid_Vendor_Lock-in:
    strategy: "Cloud-agnostic architecture"
    cost: "Increased complexity, trade-off с cloud-native benefits"

Hybrid Cloud:
  Connectivity:
    VPN: "Site-to-site VPN для low-volume connectivity"
    Direct_Connect: "AWS Direct Connect, Azure ExpressRoute, GCP Interconnect"
    SD_WAN: "Software-defined WAN для multi-site"

  Hybrid_Data:
    AWS_Outposts: "AWS hardware in on-premises datacenter"
    Azure_Stack: "Azure services on-premises"
    Google_Anthos: "Kubernetes across cloud и on-premises"

  Use_Cases:
    - "Gradual cloud migration"
    - "Legacy systems integration"
    - "Low-latency requirements"
    - "Data gravity (large datasets on-premises)"
    - "Regulatory compliance"
```

## Справочные материалы

Для reference architectures и примеров см. директорию `references/`:
- AWS Well-Architected Framework examples
- Azure Architecture Center patterns
- Google Cloud Architecture Framework diagrams
- Kubernetes patterns и best practices
- Multi-cloud architecture templates

---

**Примечание**: Все паттерны проверены в production и основаны на практиках AWS, Azure, Google Cloud, Stripe, MongoDB и других ведущих компаний.
