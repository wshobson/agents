---
name: postgresql-table-design
description: Use this skill when designing or reviewing a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, performance patterns, and advanced features
---

# PostgreSQL Table Design

## When to Use

- Designing a new PostgreSQL schema, or reviewing one before it ships.
- Choosing column types, keys, constraints, or indexes for PostgreSQL specifically.
- Deciding whether and how to partition a large table, or how to store semi-structured data.
- Planning a schema change on a live database without downtime.

The rules and decision points for a PostgreSQL schema. The full data-type catalog, workload
patterns (update-heavy, insert-heavy, upsert, schema evolution), extensions, JSONB indexing,
and worked DDL examples are in `references/details.md`; open it when a section below points there.

## Core Rules

- Define a **PRIMARY KEY** for reference tables (users, orders, etc.). Not always needed for time-series/event/log data. When used, prefer `BIGINT GENERATED ALWAYS AS IDENTITY`; use `UUID` only when global uniqueness/opacity is needed.
- **Normalize first (to 3NF)** to eliminate data redundancy and update anomalies; denormalize **only** for measured, high-ROI reads where join performance is proven problematic.
- Add **NOT NULL** everywhere it is semantically required; use **DEFAULT**s for common values.
- Create **indexes for access paths you actually query**: PK/unique (auto), **FK columns (manual!)**, frequent filters/sorts, and join keys.
- Prefer **TIMESTAMPTZ** for event time; **NUMERIC** for money; **TEXT** for strings; **BIGINT** for integers; **DOUBLE PRECISION** for floats (or `NUMERIC` for exact decimal arithmetic).

## PostgreSQL Gotchas

- **Identifiers**: unquoted → lowercased. Avoid quoted/mixed-case names; use `snake_case`.
- **Unique + NULLs**: UNIQUE allows multiple NULLs. Use `UNIQUE NULLS NOT DISTINCT (...)` (PG15+) to restrict to one NULL.
- **FK indexes**: PostgreSQL **does not** auto-index FK columns. Add them.
- **No silent coercions**: length/precision overflows error out (no truncation). Inserting 999 into `NUMERIC(2,0)` fails, unlike databases that silently truncate or round.
- **Sequences/identity have gaps** (normal; don't "fix"). Rollbacks, crashes, and concurrent transactions leave gaps (1, 2, 5, 6...).
- **Heap storage**: no clustered PK by default; `CLUSTER` is a one-off reorganization, not maintained on later inserts.
- **MVCC**: updates/deletes leave dead tuples; vacuum handles them—design to avoid hot wide-row churn.

## Data Types

- **IDs**: `BIGINT GENERATED ALWAYS AS IDENTITY`; `UUID` for distributed or opaque IDs, generated with `uuidv7()` (PG18+) or `gen_random_uuid()`.
- **Numbers**: `BIGINT` unless storage is critical; `DOUBLE PRECISION` over `REAL`; `NUMERIC(p,s)` for money and exact decimals.
- **Strings**: `TEXT`, with `CHECK (LENGTH(col) <= n)` when a limit is needed; `BYTEA` for binary. Case-insensitive lookups: expression index on `LOWER(col)`, or `CITEXT` when a constraint must be case-insensitive.
- **Time**: `TIMESTAMPTZ`, `DATE`, `INTERVAL`. `now()` is transaction start; `clock_timestamp()` is wall clock.
- **Booleans**: `BOOLEAN NOT NULL` unless tri-state is required.
- **Enums**: `CREATE TYPE ... AS ENUM` only for small, stable sets; evolving business values get `TEXT` + `CHECK` or a lookup table.
- **JSONB** over JSON, indexed with GIN, for optional/semi-structured attributes only.
- Arrays, ranges, network, geometric, full-text, domain, composite, and vector types, plus TOAST storage and collation control: see `references/details.md`.

### Types to avoid

| Avoid | Use instead |
|---|---|
| `timestamp` (without time zone) | `timestamptz` |
| `char(n)`, `varchar(n)` | `text` (+ `CHECK` on length if needed) |
| `money` | `numeric` |
| `timetz` | `timestamptz` |
| `timestamptz(0)` or any precision | `timestamptz` |
| `serial` | `generated always as identity` |

## Constraints

- **PK**: implicit UNIQUE + NOT NULL; creates a B-tree index.
- **FK**: specify `ON DELETE/UPDATE` (`CASCADE`, `RESTRICT`, `SET NULL`, `SET DEFAULT`). Index the referencing column. Use `DEFERRABLE INITIALLY DEFERRED` for circular dependencies checked at commit.
- **UNIQUE**: creates a B-tree index; allows multiple NULLs unless `NULLS NOT DISTINCT` (PG15+). Prefer `NULLS NOT DISTINCT` unless duplicate NULLs are wanted.
- **CHECK**: row-local; NULL passes (three-valued logic). Combine with `NOT NULL`: `price NUMERIC NOT NULL CHECK (price > 0)`.
- **EXCLUDE**: prevents overlaps with operators, e.g. `EXCLUDE USING gist (room_id WITH =, booking_period WITH &&)` stops double-booking. Needs a GiST-capable type.

## Indexing

- **B-tree**: default for equality/range (`=`, `<`, `>`, `BETWEEN`, `ORDER BY`).
- **Composite**: leftmost-prefix rule (`WHERE a = ? AND b > ?` uses `(a,b)`; `WHERE b = ?` does not). Most selective columns first.
- **Covering**: `CREATE INDEX ON tbl (id) INCLUDE (name, email)` for index-only scans.
- **Partial**: hot subsets, `CREATE INDEX ON tbl (user_id) WHERE status = 'active'`.
- **Expression**: `CREATE INDEX ON tbl (LOWER(email))`; the query must use the same expression.
- **GIN**: JSONB containment/existence, arrays, full-text search. **GiST**: ranges, geometry, exclusion constraints.
- **BRIN**: large, naturally ordered data (time-series) at minimal storage cost; effective when disk order correlates with the indexed column.

## Partitioning

- Use for large tables (>100M rows) whose queries consistently filter on the partition key, or where maintenance (pruning, bulk replacement) follows a key.
- **RANGE** for time-series (`PARTITION BY RANGE (created_at)`; **TimescaleDB** automates it with retention and compression), **LIST** for discrete values, **HASH** for even distribution without a natural key.
- **Constraint exclusion**: the planner prunes partitions through their `CHECK` constraints; declarative partitioning (PG10+) creates them for you.
- Prefer declarative partitioning or hypertables. Do NOT use table inheritance.
- **Limitations**: no global UNIQUE constraints—include the partition key in PK/UNIQUE. FKs from partitioned tables need PG11+, FKs referencing a partitioned table need PG12+; on older versions, use triggers.

## Examples

```sql
CREATE TABLE users (
  user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE UNIQUE INDEX ON users (LOWER(email));
CREATE INDEX ON users (created_at);
```

```sql
CREATE TABLE orders (
  order_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(user_id),
  status TEXT NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING','PAID','CANCELED')),
  total NUMERIC(10,2) NOT NULL CHECK (total > 0),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ON orders (user_id);
CREATE INDEX ON orders (created_at);
```

```sql
-- JSONB attributes with a generated, indexable scalar
CREATE TABLE profiles (
  user_id BIGINT PRIMARY KEY REFERENCES users(user_id),
  attrs JSONB NOT NULL DEFAULT '{}',
  theme TEXT GENERATED ALWAYS AS (attrs->>'theme') STORED
);
CREATE INDEX profiles_attrs_gin ON profiles USING GIN (attrs);
```

## Going deeper

`references/details.md` holds the material this file only names:

- The full data-type catalog: TOAST storage, collations, arrays, ranges, network, geometric, text search, domains, composites, vectors.
- Table types (`TEMPORARY`, `UNLOGGED`) and row-level security.
- Constraint and index notes, and partitioning DDL for RANGE, LIST, and HASH.
- Workload patterns: update-heavy, insert-heavy, upsert design, safe schema evolution.
- Generated columns and extensions (`pg_trgm`, `citext`, `timescaledb`, `postgis`, `pgvector`, and more).
- JSONB indexing strategies, including `jsonb_path_ops` and extracted B-tree columns.
