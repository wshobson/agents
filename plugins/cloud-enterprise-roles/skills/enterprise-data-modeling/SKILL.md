---
name: enterprise-data-modeling
description: Продвинутое моделирование данных для enterprise-систем включая концептуальное, логическое и физическое моделирование, polyglot persistence, event sourcing и data mesh паттерны. Используйте когда проектируете data models, выбираете базы данных, проектируете data architecture или оптимизируете data storage.
---

# Enterprise Data Modeling

## Когда использовать этот скилл

- Проектирование концептуальных, логических или физических data models
- Выбор оптимальных типов баз данных для различных use cases
- Проектирование polyglot persistence архитектуры
- Разработка event sourcing и CQRS паттернов
- Проектирование data lake или data mesh архитектуры
- Оптимизация database performance через индексы и партиционирование
- Проектирование master data management (MDM) стратегий
- Миграция между различными database technologies

## Основные концепции

### Концептуальное моделирование данных

#### Entity-Relationship Диаграммы (ERD)

**Базовая структура ERD:**

```
СУЩНОСТИ (Entities):
- Представляют бизнес-объекты
- Обозначаются прямоугольниками
- Имеют уникальные идентификаторы
- Содержат атрибуты

Примеры сущностей:
┌─────────────┐
│   Customer  │  - Клиент
│─────────────│
│ id (PK)     │
│ email       │
│ firstName   │
│ lastName    │
└─────────────┘

СВЯЗИ (Relationships):
- Один-к-одному (1:1)
- Один-ко-многим (1:N)
- Многие-ко-многим (M:N)

НОТАЦИИ:
1. Crow's Foot (наиболее популярная)
2. UML
3. Chen Notation
4. IDEF1X

Пример в Crow's Foot нотации:

Customer ||──o{ Order : places
Order ||──o{ OrderItem : contains
Product ||──o{ OrderItem : "is part of"

Расшифровка символов:
||  = exactly one
o|  = zero or one
}o  = zero or many
}|  = one or many
```

**Полная концептуальная модель e-commerce:**

```
┌────────────┐
│  Customer  │
│────────────│
│ id         │──────┐
│ email      │      │
│ name       │      │ places
└────────────┘      │ (1:N)
                    │
                    ↓
              ┌──────────┐         contains        ┌─────────────┐
              │  Order   │────────────────────────→│  OrderItem  │
              │──────────│         (1:N)           │─────────────│
              │ id       │                         │ id          │
              │ total    │←────────────────────────│ quantity    │
              │ status   │      "is part of"       │ price       │
              └──────────┘         (M:N)           └─────────────┘
                    │                                     │
                    │                                     │
              ships to                             references
                (1:1)                                  (N:1)
                    │                                     │
                    ↓                                     ↓
              ┌──────────┐                         ┌──────────┐
              │ Address  │                         │ Product  │
              │──────────│                         │──────────│
              │ street   │                         │ id       │
              │ city     │                         │ name     │
              │ country  │                         │ price    │
              └──────────┘                         └──────────┘
                                                        │
                                                        │
                                                   belongs to
                                                     (N:1)
                                                        │
                                                        ↓
                                                  ┌──────────┐
                                                  │ Category │
                                                  │──────────│
                                                  │ id       │
                                                  │ name     │
                                                  └──────────┘
```

#### Domain-Driven Design (DDD) подход

**Bounded Contexts и Aggregates:**

```
BOUNDED CONTEXT: Sales (Контекст продаж)
═══════════════════════════════════════════

Aggregate: Order (Корневая сущность)
┌─────────────────────────────────────┐
│ Order (Aggregate Root)              │
│─────────────────────────────────────│
│ - orderId: OrderId                  │
│ - customerId: CustomerId            │
│ - orderItems: List<OrderItem>       │ ← Value Objects
│ - shippingAddress: Address          │ ← Value Object
│ - status: OrderStatus               │ ← Enum
│ - total: Money                      │ ← Value Object
│─────────────────────────────────────│
│ + addItem(product, quantity)        │
│ + removeItem(orderItemId)           │
│ + changeShipping(address)           │
│ + submit()                          │
│ + cancel()                          │
└─────────────────────────────────────┘
        │
        │ contains (composition)
        ↓
┌─────────────────────────────────────┐
│ OrderItem (Entity)                  │
│─────────────────────────────────────│
│ - itemId: OrderItemId               │
│ - productId: ProductId              │
│ - quantity: int                     │
│ - unitPrice: Money                  │
│ - subtotal: Money                   │
└─────────────────────────────────────┘

Value Objects:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Address    │  │    Money     │  │  OrderStatus │
│──────────────│  │──────────────│  │──────────────│
│ street       │  │ amount       │  │ Pending      │
│ city         │  │ currency     │  │ Confirmed    │
│ zipCode      │  └──────────────┘  │ Shipped      │
│ country      │                     │ Delivered    │
└──────────────┘                     │ Cancelled    │
                                     └──────────────┘

ПРАВИЛА AGGREGATE:
✓ Внешние ссылки только на Aggregate Root (Order)
✓ Транзакционные границы = Aggregate границы
✓ Изменения через методы Aggregate Root
✓ Обеспечение бизнес-инвариантов внутри Aggregate
```

### Логическое моделирование данных

#### Нормализация баз данных

**Формы нормализации:**

```
0NF (НЕНОРМАЛИЗОВАННАЯ):
┌─────────────────────────────────────────────────────┐
│ OrderID │ CustomerName │ Products                   │
│─────────┼──────────────┼────────────────────────────│
│ 1       │ John Smith   │ Laptop,Mouse,Keyboard      │
│ 2       │ Jane Doe     │ Monitor,Cable              │
└─────────────────────────────────────────────────────┘
❌ Проблема: Повторяющиеся группы (Products)

1NF (ПЕРВАЯ НОРМАЛЬНАЯ ФОРМА):
Атомарные значения, без повторяющихся групп
┌──────────────────────────────────────────┐
│ OrderID │ CustomerName │ Product         │
│─────────┼──────────────┼─────────────────│
│ 1       │ John Smith   │ Laptop          │
│ 1       │ John Smith   │ Mouse           │
│ 1       │ John Smith   │ Keyboard        │
│ 2       │ Jane Doe     │ Monitor         │
│ 2       │ Jane Doe     │ Cable           │
└──────────────────────────────────────────┘
❌ Проблема: Повторение CustomerName (partial dependency)

2NF (ВТОРАЯ НОРМАЛЬНАЯ ФОРМА):
Устранение частичных зависимостей
Orders:
┌───────────────────────────┐
│ OrderID │ CustomerName    │
│─────────┼─────────────────│
│ 1       │ John Smith      │
│ 2       │ Jane Doe        │
└───────────────────────────┘

OrderItems:
┌───────────────────────────┐
│ OrderID │ Product         │
│─────────┼─────────────────│
│ 1       │ Laptop          │
│ 1       │ Mouse           │
│ 2       │ Monitor         │
└───────────────────────────┘
❌ Проблема: CustomerName зависит от CustomerID (transitive dependency)

3NF (ТРЕТЬЯ НОРМАЛЬНАЯ ФОРМА):
Устранение транзитивных зависимостей

Customers:
┌────────────────────────────┐
│ CustomerID │ CustomerName  │
│────────────┼───────────────│
│ 1          │ John Smith    │
│ 2          │ Jane Doe      │
└────────────────────────────┘

Orders:
┌─────────────────────┐
│ OrderID │CustomerID │
│─────────┼───────────│
│ 1       │ 1         │
│ 2       │ 2         │
└─────────────────────┘

OrderItems:
┌──────────────────────────────┐
│ OrderID │ ProductID │ Qty   │
│─────────┼───────────┼───────│
│ 1       │ 101       │ 1     │
│ 1       │ 102       │ 2     │
└──────────────────────────────┘

Products:
┌───────────────────────────────┐
│ ProductID │ ProductName       │
│───────────┼───────────────────│
│ 101       │ Laptop            │
│ 102       │ Mouse             │
└───────────────────────────────┘
✅ Решение: Нет транзитивных зависимостей

BCNF (BOYCE-CODD):
Усиленная 3NF для сложных случаев

4NF и 5NF:
Устранение многозначных зависимостей (редко используются)
```

**Когда использовать денормализацию:**

```
СЛУЧАИ ДЛЯ ДЕНОРМАЛИЗАЦИИ:

1. READ-HEAVY WORKLOADS
   Проблема: Joins замедляют чтение
   Решение: Предварительно рассчитанные aggregates

   Вместо JOIN при каждом запросе:
   ┌─────────────────────┐      ┌──────────────────────┐
   │ Orders              │──┐   │ OrderItems           │
   │ - orderId           │  └──→│ - orderItemId        │
   │ - customerId        │      │ - orderId (FK)       │
   │ - orderDate         │      │ - price              │
   └─────────────────────┘      └──────────────────────┘

   Денормализация:
   ┌──────────────────────────────┐
   │ Orders                       │
   │ - orderId                    │
   │ - customerId                 │
   │ - orderDate                  │
   │ - totalAmount (денормализ.)  │ ← Рассчитано при INSERT
   │ - itemCount (денормализ.)    │
   └──────────────────────────────┘

2. REPORTING & ANALYTICS
   Материализованные представления для dashboards

3. DISTRIBUTED SYSTEMS
   Каждый microservice хранит нужные данные локально

4. CACHING LAYER
   Денормализованные данные в Redis/Memcached
```

### Физическое моделирование данных

#### Выбор типа базы данных (Polyglot Persistence)

**Матрица выбора database:**

```yaml
Use Case: Транзакционные данные (OLTP)
Рекомендация: Relational Database
Варианты:
  - PostgreSQL:
      Когда: Complex queries, JSONB support, full-text search
      Примеры: AWS RDS PostgreSQL, Azure Database for PostgreSQL, Cloud SQL
      Преимущества: Advanced features, open source, extensibility

  - MySQL:
      Когда: Simple schema, read-heavy workload, replication
      Примеры: AWS RDS MySQL, Azure Database for MySQL, Cloud SQL
      Преимущества: Wide adoption, performance, tooling

  - Amazon Aurora:
      Когда: AWS native, need auto-scaling, high availability
      Преимущества: 5x MySQL/3x PostgreSQL performance, auto-scaling storage

  - SQL Server:
      Когда: .NET applications, enterprise Microsoft stack
      Примеры: Azure SQL Database, AWS RDS SQL Server
      Преимущества: Enterprise features, SSRS/SSIS integration

---

Use Case: Документоориентированные данные
Рекомендация: Document Database
Варианты:
  - MongoDB:
      Когда: Flexible schema, nested documents, rapid development
      Примеры: MongoDB Atlas (multi-cloud), DocumentDB (AWS)
      Модель данных:
        {
          "_id": "order_123",
          "customer": {
            "id": "cust_456",
            "name": "John Doe",
            "email": "john@example.com"
          },
          "items": [
            {"productId": "prod_789", "quantity": 2, "price": 99.99}
          ],
          "total": 199.98,
          "createdAt": ISODate("2024-01-15")
        }
      Преимущества: Rich queries, indexes, aggregation framework

  - DynamoDB:
      Когда: Single-digit ms latency, serverless, auto-scaling
      Модель данных: Key-value with rich documents
      Преимущества: Fully managed, predictable performance, pay-per-request

  - Azure Cosmos DB:
      Когда: Global distribution, multi-model (документы, графы, key-value)
      Преимущества: Multi-region writes, 5 consistency levels

  - Firestore:
      Когда: Mobile/web apps, real-time sync, offline support
      Преимущества: Real-time listeners, automatic scaling, Firebase integration

---

Use Case: Key-Value данные
Рекомендация: Key-Value Store
Варианты:
  - Redis:
      Когда: Caching, session store, real-time analytics, pub/sub
      Структуры: Strings, Lists, Sets, Sorted Sets, Hashes, Streams
      Примеры: AWS ElastiCache, Azure Cache for Redis, Memorystore
      TTL: Automatic expiration
      Преимущества: In-memory speed (sub-ms), rich data structures

  - Memcached:
      Когда: Simple distributed caching, high throughput
      Преимущества: Simplicity, horizontal scaling

  - DynamoDB:
      Когда: Persistent key-value store with ACID transactions
      Преимущества: Durable, consistent, serverless

---

Use Case: Wide Column данные (Time-Series, IoT)
Рекомендация: Column-Family Database
Варианты:
  - Apache Cassandra:
      Когда: Multi-region, write-heavy, linear scalability
      Модель данных: Column families with partition keys
      Примеры: AWS Keyspaces, Azure Managed Instance for Apache Cassandra
      Преимущества: No single point of failure, tunable consistency

  - HBase:
      Когда: Hadoop ecosystem integration, batch processing
      Преимущества: HDFS storage, Hadoop integration

  - Google Bigtable:
      Когда: Large-scale analytical/operational workloads, GCP native
      Преимущества: Low latency, high throughput, automatic scaling

---

Use Case: Graph данные (Relationships, Social Networks)
Рекомендация: Graph Database
Варианты:
  - Neo4j:
      Когда: Complex relationships, graph algorithms, pattern matching
      Query: Cypher language
      Пример:
        MATCH (p:Person)-[:FRIENDS_WITH]->(friend)
        WHERE p.name = 'Alice'
        RETURN friend
      Преимущества: Native graph storage, rich query language

  - Amazon Neptune:
      Когда: AWS native, Property Graph + RDF
      Query: Gremlin (Property Graph), SPARQL (RDF)
      Преимущества: Fully managed, high availability, ACID transactions

  - Azure Cosmos DB Gremlin API:
      Когда: Azure native, global distribution
      Преимущества: Multi-model, SLA-backed performance

---

Use Case: Time-Series данные (Metrics, Logs, IoT)
Рекомендация: Time-Series Database
Варианты:
  - InfluxDB:
      Когда: Metrics, monitoring, IoT sensor data
      Структура: Time-stamped points with tags
      Query: InfluxQL, Flux
      Преимущества: Compression, retention policies, continuous queries

  - TimescaleDB:
      Когда: PostgreSQL compatibility, hybrid relational+time-series
      Преимущества: SQL queries, PostgreSQL ecosystem

  - Amazon Timestream:
      Когда: Serverless, AWS native, automatic tiering
      Преимущества: Fully managed, cost-effective, built-in analytics

  - Prometheus:
      Когда: Kubernetes monitoring, metrics collection
      Query: PromQL
      Преимущества: Pull model, service discovery, alerting

---

Use Case: Search & Full-Text Search
Рекомендация: Search Engine
Варианты:
  - Elasticsearch:
      Когда: Full-text search, log analytics, application search
      Примеры: AWS OpenSearch, Elastic Cloud
      Структура: Inverted indexes
      Query: Query DSL
      Преимущества: Relevance scoring, faceted search, aggregations

  - Algolia:
      Когда: SaaS search, instant search UX, developer-friendly
      Преимущества: Fully managed, typo tolerance, ranking customization

  - Azure Cognitive Search:
      Когда: AI-powered search, OCR, entity extraction
      Преимущества: Built-in AI, skillsets, knowledge mining
```

#### Индексирование стратегии

**Типы индексов и when to use:**

```sql
-- 1. B-TREE INDEX (По умолчанию в большинстве RDBMS)
-- Когда: Точные поиски, range queries, sorting
CREATE INDEX idx_customer_email ON customers(email);

SELECT * FROM customers WHERE email = 'john@example.com';
-- ✅ Использует idx_customer_email

SELECT * FROM customers WHERE email LIKE 'john%';
-- ✅ Использует idx_customer_email (prefix match)

SELECT * FROM customers WHERE email LIKE '%john%';
-- ❌ Full table scan (wildcard at start)

-- 2. COMPOSITE INDEX (Множественные колонки)
-- Когда: Queries фильтруют по нескольким колонкам
CREATE INDEX idx_orders_customer_date
ON orders(customer_id, order_date);

-- ✅ Использует composite index (левая префиксная часть)
SELECT * FROM orders WHERE customer_id = 123;

-- ✅ Использует composite index (обе колонки)
SELECT * FROM orders
WHERE customer_id = 123 AND order_date > '2024-01-01';

-- ❌ НЕ использует composite index (пропущен customer_id)
SELECT * FROM orders WHERE order_date > '2024-01-01';

-- ПРАВИЛО LEFT-PREFIX:
-- Index (A, B, C) поддерживает:
-- ✅ WHERE A
-- ✅ WHERE A, B
-- ✅ WHERE A, B, C
-- ❌ WHERE B
-- ❌ WHERE C
-- ❌ WHERE B, C

-- 3. UNIQUE INDEX
-- Когда: Обеспечение уникальности
CREATE UNIQUE INDEX idx_users_email ON users(email);
-- Предотвращает дубликаты email

-- 4. PARTIAL/FILTERED INDEX
-- Когда: Индексировать только подмножество строк (PostgreSQL, SQL Server)
CREATE INDEX idx_active_orders
ON orders(customer_id)
WHERE status = 'Active';

-- Меньший размер индекса, быстрее для активных заказов

-- 5. FULL-TEXT INDEX
-- Когда: Текстовый поиск
-- PostgreSQL:
CREATE INDEX idx_products_search
ON products USING gin(to_tsvector('english', name || ' ' || description));

SELECT * FROM products
WHERE to_tsvector('english', name || ' ' || description)
      @@ to_tsquery('laptop & wireless');

-- MySQL:
CREATE FULLTEXT INDEX idx_articles_content ON articles(title, body);

SELECT * FROM articles
WHERE MATCH(title, body) AGAINST('machine learning' IN NATURAL LANGUAGE MODE);

-- 6. COVERING INDEX (INCLUDE columns)
-- Когда: Избежать lookup в таблице
-- PostgreSQL, SQL Server:
CREATE INDEX idx_orders_covering
ON orders(customer_id)
INCLUDE (order_date, total_amount);

-- Query может быть выполнен полностью из индекса (Index-Only Scan)
SELECT order_date, total_amount
FROM orders
WHERE customer_id = 123;

-- 7. HASH INDEX (PostgreSQL)
-- Когда: Только equality comparisons, быстрее для больших строк
CREATE INDEX idx_customer_hash ON customers USING hash(email);

-- ✅ Equality
SELECT * FROM customers WHERE email = 'john@example.com';

-- ❌ Range queries НЕ поддерживаются
SELECT * FROM customers WHERE email > 'j';

-- 8. JSONB INDEX (PostgreSQL, MongoDB)
-- Когда: Queries на JSON fields
CREATE INDEX idx_metadata_tags
ON products USING gin(metadata jsonb_path_ops);

SELECT * FROM products
WHERE metadata @> '{"tags": ["electronics"]}';

-- 9. SPATIAL INDEX (PostGIS, MongoDB, SQL Server)
-- Когда: Geospatial queries
CREATE INDEX idx_stores_location
ON stores USING gist(location);

-- Find stores within 10km radius
SELECT * FROM stores
WHERE ST_DWithin(location, ST_MakePoint(-122.4194, 37.7749)::geography, 10000);
```

**Best Practices для индексирования:**

```
✅ DO:
1. Индексировать колонки в WHERE, JOIN, ORDER BY
2. Использовать composite indexes для часто комбинируемых фильтров
3. Индексировать foreign keys
4. Использовать EXPLAIN/EXPLAIN ANALYZE для анализа query plans
5. Мониторить unused indexes (занимают место и замедляют writes)
6. Регулярно REINDEX для предотвращения bloat (PostgreSQL)
7. Анализировать index usage statistics

❌ DON'T:
1. Не создавать индексы на каждой колонке (overhead для writes)
2. Не индексировать low-cardinality колонки (boolean, status с 2-3 значениями)
3. Не дублировать индексы (A,B и A - дубликат для single-column A queries)
4. Не индексировать очень длинные строки без префикса
5. Не забывать обновлять statistics (ANALYZE в PostgreSQL)

МОНИТОРИНГ:
-- PostgreSQL: unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexrelname NOT LIKE 'pg_toast%';

-- PostgreSQL: missing indexes
SELECT schemaname, tablename, seq_scan, seq_tup_read,
       idx_scan, seq_tup_read / seq_scan as avg
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC;

-- SQL Server: missing indexes
SELECT migs.avg_user_impact, migs.avg_total_user_cost,
       mid.statement, mid.equality_columns, mid.inequality_columns
FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
ORDER BY migs.avg_user_impact DESC;
```

#### Партиционирование (Partitioning)

**Типы партиционирования:**

```sql
-- 1. RANGE PARTITIONING
-- Когда: Time-series данные, логические диапазоны

-- PostgreSQL:
CREATE TABLE orders (
    order_id BIGINT,
    customer_id BIGINT,
    order_date DATE,
    total DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE orders_2024_q3 PARTITION OF orders
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE orders_2024_q4 PARTITION OF orders
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- Преимущества:
-- ✅ Query pruning (сканируются только relevant partitions)
-- ✅ Легко удалять старые данные (DROP partition)
-- ✅ Parallel query execution across partitions

SELECT * FROM orders
WHERE order_date BETWEEN '2024-04-01' AND '2024-06-30';
-- Сканируется только orders_2024_q2

-- 2. LIST PARTITIONING
-- Когда: Категориальные данные (регионы, статусы)

CREATE TABLE sales (
    sale_id BIGINT,
    region VARCHAR(20),
    amount DECIMAL(10,2)
) PARTITION BY LIST (region);

CREATE TABLE sales_us PARTITION OF sales
    FOR VALUES IN ('US', 'USA', 'United States');

CREATE TABLE sales_eu PARTITION OF sales
    FOR VALUES IN ('UK', 'DE', 'FR', 'ES', 'IT');

CREATE TABLE sales_asia PARTITION OF sales
    FOR VALUES IN ('JP', 'CN', 'IN', 'SG');

-- 3. HASH PARTITIONING
-- Когда: Равномерное распределение по партициям

CREATE TABLE users (
    user_id BIGINT,
    email VARCHAR(255),
    created_at TIMESTAMP
) PARTITION BY HASH (user_id);

CREATE TABLE users_p0 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE users_p1 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE users_p2 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE users_p3 PARTITION OF users
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);

-- Распределение: user_id % 4 определяет партицию

-- 4. COMPOSITE PARTITIONING
-- Когда: Многоуровневое партиционирование

CREATE TABLE events (
    event_id BIGINT,
    user_id BIGINT,
    event_date DATE,
    event_type VARCHAR(50)
) PARTITION BY RANGE (event_date);

CREATE TABLE events_2024_q1 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01')
    PARTITION BY HASH (user_id);

CREATE TABLE events_2024_q1_p0 PARTITION OF events_2024_q1
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE events_2024_q1_p1 PARTITION OF events_2024_q1
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

-- И так далее...
```

**Sharding стратегии (Горизонтальное партиционирование):**

```
SHARDING PATTERNS:

1. RANGE-BASED SHARDING
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │  Shard 1     │   │  Shard 2     │   │  Shard 3     │
   │ user_id:     │   │ user_id:     │   │ user_id:     │
   │ 1 - 1M       │   │ 1M - 2M      │   │ 2M - 3M      │
   └──────────────┘   └──────────────┘   └──────────────┘

   ✅ Простой
   ❌ Unbalanced (если рост неравномерный)

2. HASH-BASED SHARDING
   Shard = hash(user_id) % num_shards

   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │  Shard 1     │   │  Shard 2     │   │  Shard 3     │
   │ hash % 3 = 0 │   │ hash % 3 = 1 │   │ hash % 3 = 2 │
   └──────────────┘   └──────────────┘   └──────────────┘

   ✅ Равномерное распределение
   ❌ Сложность rebalancing при добавлении shards

3. DIRECTORY-BASED SHARDING
   Lookup table определяет shard для каждого ключа

   ┌─────────────────────┐
   │ Shard Directory     │
   │─────────────────────│
   │ user_id │ shard     │
   │─────────┼───────────│
   │ 1-100K  │ shard_1   │
   │ 100K+   │ shard_2   │
   │ VIP     │ shard_vip │
   └─────────────────────┘

   ✅ Гибкость
   ❌ Дополнительная lookup latency

4. GEO-BASED SHARDING
   По географическому расположению

   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ US Shard     │   │ EU Shard     │   │ APAC Shard   │
   │ us-east-1    │   │ eu-west-1    │   │ ap-southeast │
   └──────────────┘   └──────────────┘   └──────────────┘

   ✅ Data locality, compliance (GDPR)
   ✅ Низкая latency
   ❌ Сложные cross-region queries

РЕАЛИЗАЦИЯ В CLOUD PLATFORMS:

- MongoDB: Automatic sharding with shard keys
- DynamoDB: Partition key определяет shard
- Cosmos DB: Partition key for horizontal scaling
- Vitess: MySQL sharding layer
- Citus: PostgreSQL extension for sharding
```

## Продвинутые паттерны

### Event Sourcing

**Концепция Event Sourcing:**

```
ТРАДИЦИОННЫЙ ПОДХОД (State-based):
┌──────────────────────────┐
│ Orders Table             │
│──────────────────────────│
│ order_id │ status        │
│──────────┼───────────────│
│ 123      │ Delivered     │  ← Текущее состояние
└──────────────────────────┘

История потеряна: Как заказ дошел до "Delivered"?

EVENT SOURCING ПОДХОД (Event-based):
┌────────────────────────────────────────────────┐
│ Order Events (Append-only log)                │
│────────────────────────────────────────────────│
│ event_id │ order_id │ event_type  │ timestamp │
│──────────┼──────────┼─────────────┼───────────│
│ 1        │ 123      │ Created     │ 10:00     │
│ 2        │ 123      │ Paid        │ 10:05     │
│ 3        │ 123      │ Shipped     │ 11:30     │
│ 4        │ 123      │ Delivered   │ 15:00     │
└────────────────────────────────────────────────┘

Current state = Replay всех events
История полностью сохранена

Event Payload:
{
  "eventId": "evt_001",
  "eventType": "OrderCreated",
  "aggregateId": "order_123",
  "timestamp": "2024-01-15T10:00:00Z",
  "data": {
    "customerId": "cust_456",
    "items": [...],
    "total": 299.99
  },
  "metadata": {
    "userId": "user_789",
    "ipAddress": "192.168.1.1"
  }
}
```

**Реализация Event Store:**

```sql
-- Event Store Schema (PostgreSQL)
CREATE TABLE event_store (
    event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_version INT NOT NULL,
    event_data JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    created_by VARCHAR(255),

    -- Оптимистичная блокировка для concurrency
    CONSTRAINT unique_version UNIQUE (aggregate_id, event_version)
);

-- Индексы для быстрого чтения
CREATE INDEX idx_event_store_aggregate
ON event_store(aggregate_id, event_version);

CREATE INDEX idx_event_store_type
ON event_store(aggregate_type, created_at);

-- Snapshot для оптимизации (периодическое состояние)
CREATE TABLE aggregate_snapshots (
    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_id UUID NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    version INT NOT NULL,
    state JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT unique_aggregate_snapshot UNIQUE (aggregate_id, version)
);

-- Пример записи события
INSERT INTO event_store (
    aggregate_id,
    aggregate_type,
    event_type,
    event_version,
    event_data,
    metadata,
    created_by
) VALUES (
    'order_123',
    'Order',
    'OrderCreated',
    1,  -- Первая версия
    '{"customerId": "cust_456", "total": 299.99}'::jsonb,
    '{"userId": "user_789", "ipAddress": "192.168.1.1"}'::jsonb,
    'user_789'
);

-- Чтение всех событий для aggregate
SELECT event_type, event_data, created_at
FROM event_store
WHERE aggregate_id = 'order_123'
ORDER BY event_version ASC;

-- Replay для восстановления состояния
WITH events AS (
    SELECT event_type, event_data
    FROM event_store
    WHERE aggregate_id = 'order_123'
    ORDER BY event_version ASC
)
-- Aggregate events into current state (application logic)
```

### CQRS (Command Query Responsibility Segregation)

**Разделение Write и Read моделей:**

```
АРХИТЕКТУРА CQRS:

┌────────────────┐
│   Commands     │ (Write operations)
│ - CreateOrder  │
│ - UpdateOrder  │
│ - CancelOrder  │
└────────┬───────┘
         │
         ↓
┌────────────────────────┐
│  Command Handlers      │
│  (Business Logic)      │
└───────────┬────────────┘
            │
            ↓ Append events
┌─────────────────────────┐
│    Event Store          │ ← Source of truth
│  (Append-only events)   │
└───────┬─────────────────┘
        │
        │ Publish events
        ↓
┌──────────────────────────┐
│   Event Bus              │
│ (Kafka, RabbitMQ, SNS)   │
└────────┬─────────────────┘
         │
         │ Subscribe
         ↓
┌────────────────────────────┐
│  Read Model Projections    │ (Materialized views)
│ - OrderListProjection      │
│ - OrderDetailProjection    │
│ - CustomerOrdersProjection │
└─────────────┬──────────────┘
              │
              ↓ Update
┌───────────────────────────────┐
│   Read Databases              │
│ - PostgreSQL (normalized)     │
│ - Elasticsearch (search)      │
│ - Redis (cache)               │
│ - DynamoDB (fast key-value)   │
└────────────┬──────────────────┘
             │
             │ Query
             ↓
┌───────────────────────┐
│   Queries             │ (Read operations)
│ - GetOrderById        │
│ - SearchOrders        │
│ - GetCustomerOrders   │
└───────────────────────┘

ПРЕИМУЩЕСТВА:
✅ Оптимизация write и read моделей независимо
✅ Масштабирование reads отдельно от writes
✅ Разные хранилища для разных use cases
✅ Eventual consistency (допустимо для многих систем)

НЕДОСТАТКИ:
❌ Повышенная сложность
❌ Eventual consistency (не сразу видно изменения)
❌ Дублирование данных
```

### Data Mesh Architecture

**Децентрализованная data architecture:**

```
ТРАДИЦИОННАЯ АРХИТЕКТУРА (Централизованная):
                ┌──────────────────┐
                │   Data Lake      │
All data ──────→│ (Single source)  │
                └──────────────────┘

❌ Проблемы:
- Bottleneck в Data team
- Сложность для domain teams
- Монолитная архитектура данных

DATA MESH АРХИТЕКТУРА (Децентрализованная):

┌─────────────────────────────────────────────────────────┐
│                   Data Mesh Platform                    │
│  (Self-serve infrastructure, Governance, Discovery)     │
└─────────────────────────────────────────────────────────┘
         │                  │                  │
         │                  │                  │
         ↓                  ↓                  ↓
┌──────────────────┐ ┌──────────────┐ ┌─────────────────┐
│  Sales Domain    │ │ Inventory    │ │ Customer Domain │
│  Data Products   │ │ Data Products│ │ Data Products   │
│──────────────────│ │──────────────│ │─────────────────│
│ - Orders         │ │ - Stock      │ │ - Profiles      │
│ - Transactions   │ │ - Warehouse  │ │ - Preferences   │
└──────────────────┘ └──────────────┘ └─────────────────┘

Каждый domain владеет своими data products
Domain teams ответственны за quality и SLAs

ПРИНЦИПЫ DATA MESH:

1. DOMAIN-ORIENTED OWNERSHIP
   - Decentralized data ownership
   - Domain teams владеют и управляют своими данными
   - Data as a product mindset

2. DATA AS A PRODUCT
   - Discoverable (data catalog)
   - Addressable (APIs, schemas)
   - Understandable (documentation, lineage)
   - Trustworthy (quality, SLAs)
   - Secure (access control, encryption)

3. SELF-SERVE DATA PLATFORM
   - Infrastructure automation
   - CI/CD for data pipelines
   - Observability and monitoring
   - Data quality frameworks

4. FEDERATED COMPUTATIONAL GOVERNANCE
   - Global policies (security, privacy, compliance)
   - Domain autonomy
   - Automated policy enforcement
```

## Справочные материалы

Для детальных примеров и шаблонов см. директорию `references/`:
- Data modeling templates
- Database schema examples
- Normalization examples
- Partitioning strategies
- Event sourcing patterns
- CQRS implementation guides

---

**Примечание**: Все паттерны и стратегии основаны на лучших практиках ведущих компаний (AWS, Azure, Google Cloud, MongoDB, Stripe, SAP, Oracle, Microsoft) и протестированы в enterprise-окружениях.
