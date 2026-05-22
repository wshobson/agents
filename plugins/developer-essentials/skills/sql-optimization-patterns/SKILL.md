---
name: sql-optimization-patterns
description: Master SQL query optimization, indexing strategies, and EXPLAIN analysis to dramatically improve database performance and eliminate slow queries. Use when debugging slow queries, designing database schemas, or optimizing application performance.
---

# SQL Optimization Patterns

Transform slow database queries into lightning-fast operations through systematic optimization, proper indexing, and query plan analysis.

## When to Use This Skill

- Debugging slow-running queries
- Designing performant database schemas
- Optimizing application response times
- Reducing database load and costs
- Improving scalability for growing datasets
- Analyzing EXPLAIN query plans
- Implementing efficient indexes
- Resolving N+1 query problems

## Core Concepts

### 1. Query Execution Plans (EXPLAIN)

Understanding EXPLAIN output is fundamental to optimization.

**PostgreSQL EXPLAIN:**

```sql
-- Basic explain
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- With actual execution stats
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'user@example.com';

-- Verbose output with more details
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT u.*, o.order_total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > NOW() - INTERVAL '30 days';
```

**Key Metrics to Watch:**

- **Seq Scan**: Full table scan (usually slow for large tables)
- **Index Scan**: Using index (good)
- **Index Only Scan**: Using index without touching table (best)
- **Nested Loop**: Join method (okay for small datasets)
- **Hash Join**: Join method (good for larger datasets)
- **Merge Join**: Join method (good for sorted data)
- **Cost**: Estimated query cost (lower is better)
- **Rows**: Estimated rows returned
- **Actual Time**: Real execution time

### 2. Index Strategies

Indexes are the most powerful optimization tool.

**Index Types:**

- **B-Tree**: Default, good for equality and range queries
- **Hash**: Only for equality (=) comparisons
- **GIN**: Full-text search, array queries, JSONB
- **GiST**: Geometric data, full-text search
- **BRIN**: Block Range INdex for very large tables with correlation

```sql
-- Standard B-Tree index
CREATE INDEX idx_users_email ON users(email);

-- Composite index (order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index (index subset of rows)
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';

-- Expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Covering index (include additional columns)
CREATE INDEX idx_users_email_covering ON users(email)
INCLUDE (name, created_at);

-- Full-text search index
CREATE INDEX idx_posts_search ON posts
USING GIN(to_tsvector('english', title || ' ' || body));

-- JSONB index
CREATE INDEX idx_metadata ON events USING GIN(metadata);
```

### 3. Query Optimization Patterns

**Avoid SELECT \*:**

```sql
-- Bad: Fetches unnecessary columns
SELECT * FROM users WHERE id = 123;

-- Good: Fetch only what you need
SELECT id, email, name FROM users WHERE id = 123;
```

**Use WHERE Clause Efficiently:**

```sql
-- Bad: Function prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Good: Create functional index or use exact match
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
-- Then:
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Or store normalized data
SELECT * FROM users WHERE email = 'user@example.com';
```

**Optimize JOINs:**

```sql
-- Bad: Cartesian product then filter
SELECT u.name, o.total
FROM users u, orders o
WHERE u.id = o.user_id AND u.created_at > '2024-01-01';

-- Good: Filter before join
SELECT u.name, o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01';

-- Better: Filter both tables
SELECT u.name, o.total
FROM (SELECT * FROM users WHERE created_at > '2024-01-01') u
JOIN orders o ON u.id = o.user_id;
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

1. **Index Selectively**: Too many indexes slow down writes
2. **Monitor Query Performance**: Use slow query logs
3. **Keep Statistics Updated**: Run ANALYZE regularly
4. **Use Appropriate Data Types**: Smaller types = better performance
5. **Normalize Thoughtfully**: Balance normalization vs performance
6. **Cache Frequently Accessed Data**: Use application-level caching
7. **Connection Pooling**: Reuse database connections
8. **Regular Maintenance**: VACUUM, ANALYZE, rebuild indexes

```sql
-- Update statistics
ANALYZE users;
ANALYZE VERBOSE orders;

-- Vacuum (PostgreSQL)
VACUUM ANALYZE users;
VACUUM FULL users;  -- Reclaim space (locks table)

-- Reindex
REINDEX INDEX idx_users_email;
REINDEX TABLE users;
```

## Common Pitfalls

- **Over-Indexing**: Each index slows down INSERT/UPDATE/DELETE
- **Unused Indexes**: Waste space and slow writes
- **Missing Indexes**: Slow queries, full table scans
- **Implicit Type Conversion**: Prevents index usage
- **OR Conditions**: Can't use indexes efficiently
- **LIKE with Leading Wildcard**: `LIKE '%abc'` can't use index
- **Function in WHERE**: Prevents index usage unless functional index exists

## Monitoring Queries

```sql
-- Find slow queries (PostgreSQL)
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Find missing indexes (PostgreSQL)
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / seq_scan AS avg_seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 10;

-- Find unused indexes (PostgreSQL)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```
