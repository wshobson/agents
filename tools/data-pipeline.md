---
model: claude-sonnet-4-5-20250929
---

# Data Pipeline Architecture

Design and implement a scalable data pipeline for: $ARGUMENTS

Create a production-ready data pipeline including:

1. **Data Ingestion**:
   - Multiple source connectors (APIs, databases, files, streams)
   - Schema evolution handling
   - Incremental/batch loading
   - Data quality checks at ingestion
   - Dead letter queue for failures

2. **Transformation Layer**:
   - ETL/ELT architecture decision
   - Apache Beam/Spark transformations
   - Data cleansing and normalization
   - Feature engineering pipeline
   - Business logic implementation

3. **Orchestration**:
   - Airflow/Prefect DAGs
   - Dependency management
   - Retry and failure handling
   - SLA monitoring
   - Dynamic pipeline generation

4. **Storage Strategy**:
   - Data lake architecture
   - Partitioning strategy
   - Compression choices
   - Retention policies
   - Hot/cold storage tiers

5. **Streaming Pipeline**:
   - Kafka/Kinesis integration
   - Real-time processing
   - Windowing strategies
   - Late data handling
   - Exactly-once semantics

6. **Data Quality**:
   - Automated testing
   - Data profiling
   - Anomaly detection
   - Lineage tracking
   - Quality metrics and dashboards

7. **Performance & Scale**:
   - Horizontal scaling
   - Resource optimization
   - Caching strategies
   - Query optimization
   - Cost management

Include monitoring, alerting, and data governance considerations. Make it cloud-agnostic with specific implementation examples for AWS/GCP/Azure.
