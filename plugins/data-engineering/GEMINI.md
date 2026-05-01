# Data Engineering

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `backend-architect` | inherit | Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems. Ma... |
| `data-engineer` | opus | Build scalable data pipelines, modern data warehouses, and real-time streaming architectures. Implements Apache Spark... |

## Commands

These commands are available in Claude Code via slash command. In Gemini CLI, describe the equivalent task in natural language.

| Claude Code Command | Description |
|---|---|
| `/data-engineering:data-driven-feature` `<feature description> [--experiment-type ab|multivariate|bandit] [--confidence 0.90|0.95|0.99]` | Build features guided by data insights, A/B testing, and continuous measurement |
| `/data-engineering:data-pipeline` | Data Pipeline Architecture |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `airflow-dag-patterns` | Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipeline... |
| `data-quality-frameworks` | Implement data quality validation with Great Expectations, dbt tests, and data contracts. Use when building data quality pipelines, imple... |
| `dbt-transformation-patterns` | Master dbt (data build tool) for analytics engineering with model organization, testing, documentation, and incremental strategies. Use w... |
| `spark-optimization` | Optimize Apache Spark jobs with partitioning, caching, shuffle optimization, and memory tuning. Use when improving Spark performance, deb... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert backend architect specializing in scalable API design, microservices architecture, and distributed systems" → activates `backend-architect`
- "Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment" → activates `airflow-dag-patterns` skill
- In Claude Code: `/data-engineering:data-driven-feature` — in Gemini: describe the task in natural language

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
