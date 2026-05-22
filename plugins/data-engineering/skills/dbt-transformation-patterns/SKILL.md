---
name: dbt-transformation-patterns
description: Master dbt (data build tool) for analytics engineering with model organization, testing, documentation, and incremental strategies. Use when building data transformations, creating data models, or implementing analytics engineering best practices.
---

# dbt Transformation Patterns

Production-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing.

## When to Use This Skill

- Building data transformation pipelines with dbt
- Organizing models into staging, intermediate, and marts layers
- Implementing data quality tests
- Creating incremental models for large datasets
- Documenting data models and lineage
- Setting up dbt project structure

## Core Concepts

### 1. Model Layers (Medallion Architecture)

```
sources/          Raw data definitions
    ↓
staging/          1:1 with source, light cleaning
    ↓
intermediate/     Business logic, joins, aggregations
    ↓
marts/            Final analytics tables
```

### 2. Naming Conventions

| Layer        | Prefix         | Example                       |
| ------------ | -------------- | ----------------------------- |
| Staging      | `stg_`         | `stg_stripe__payments`        |
| Intermediate | `int_`         | `int_payments_pivoted`        |
| Marts        | `dim_`, `fct_` | `dim_customers`, `fct_orders` |

## Quick Start

```yaml
# dbt_project.yml
name: "analytics"
version: "1.0.0"
profile: "analytics"

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]

vars:
  start_date: "2020-01-01"

models:
  analytics:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      +schema: analytics
```

```
# Project structure
models/
├── staging/
│   ├── stripe/
│   │   ├── _stripe__sources.yml
│   │   ├── _stripe__models.yml
│   │   ├── stg_stripe__customers.sql
│   │   └── stg_stripe__payments.sql
│   └── shopify/
│       ├── _shopify__sources.yml
│       └── stg_shopify__orders.sql
├── intermediate/
│   └── finance/
│       └── int_payments_pivoted.sql
└── marts/
    ├── core/
    │   ├── _core__models.yml
    │   ├── dim_customers.sql
    │   └── fct_orders.sql
    └── finance/
        └── fct_revenue.sql
```

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Best Practices

### Do's

- **Use staging layer** - Clean data once, use everywhere
- **Test aggressively** - Not null, unique, relationships
- **Document everything** - Column descriptions, model descriptions
- **Use incremental** - For tables > 1M rows
- **Version control** - dbt project in Git

### Don'ts

- **Don't skip staging** - Raw → mart is tech debt
- **Don't hardcode dates** - Use `{{ var('start_date') }}`
- **Don't repeat logic** - Extract to macros
- **Don't test in prod** - Use dev target
- **Don't ignore freshness** - Monitor source data
