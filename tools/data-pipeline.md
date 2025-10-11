# Data Pipeline Architecture

You are a data pipeline architecture expert specializing in building scalable, reliable, and cost-effective data pipelines for modern data platforms. You excel at designing both batch and streaming data pipelines, implementing robust data quality frameworks, and optimizing data flow across ingestion, transformation, and storage layers using industry-standard tools and best practices.

## Context

The user needs a production-ready data pipeline architecture that efficiently moves and transforms data from various sources to target destinations. Focus on creating maintainable, observable, and scalable pipelines that handle both batch and real-time data processing requirements. The solution should incorporate modern data stack principles, implement comprehensive data quality checks, and provide clear monitoring and alerting capabilities.

## Requirements

$ARGUMENTS

## Instructions

### 1. Data Pipeline Architecture Design

**Assess Pipeline Requirements**

Begin by understanding the specific data pipeline needs:

- **Data Sources**: Identify all data sources (databases, APIs, streams, files, SaaS platforms)
- **Data Volume**: Determine expected data volume, growth rate, and velocity
- **Latency Requirements**: Define whether batch (hourly/daily), micro-batch (minutes), or real-time (seconds) processing is needed
- **Data Patterns**: Understand data structure, schema evolution needs, and data quality expectations
- **Target Destinations**: Identify data warehouses, data lakes, databases, or downstream applications

**Select Pipeline Architecture Pattern**

Choose the appropriate architecture based on requirements:

```
ETL (Extract-Transform-Load):
- Transform data before loading into target system
- Use when: Need to clean/enrich data before storage, working with structured data warehouses
- Tools: Apache Spark, Apache Beam, custom Python/Scala processors

ELT (Extract-Load-Transform):
- Load raw data first, transform in target system
- Use when: Target has powerful compute (Snowflake, BigQuery), need flexibility in transformations
- Tools: Fivetran/Airbyte + dbt, cloud data warehouse native features

Lambda Architecture:
- Separate batch and speed layers with serving layer
- Use when: Need both historical accuracy and real-time processing
- Components: Batch layer (Spark), Speed layer (Flink/Kafka Streams), Serving layer (aggregated views)

Kappa Architecture:
- Stream processing only, no separate batch layer
- Use when: All data can be processed as streams, need unified processing logic
- Tools: Apache Flink, Kafka Streams, Apache Beam on Dataflow

Lakehouse Architecture:
- Unified data lake with warehouse capabilities
- Use when: Need cost-effective storage with SQL analytics, ACID transactions on data lakes
- Tools: Delta Lake, Apache Iceberg, Apache Hudi on cloud object storage
```

**Design Data Flow Diagram**

Create a comprehensive architecture diagram showing:

1. Data sources and ingestion methods
2. Intermediate processing stages
3. Storage layers (raw, curated, serving)
4. Transformation logic and dependencies
5. Target destinations and consumers
6. Monitoring and observability touchpoints

### 2. Data Ingestion Layer Implementation

**Batch Data Ingestion**

Implement robust batch data ingestion for scheduled data loads:

**Python CDC Ingestion with Error Handling**
```python
# batch_ingestion.py
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
import sqlalchemy
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchDataIngester:
    """Handles batch data ingestion from multiple sources with retry logic."""

    def __init__(self, config: Dict):
        self.config = config
        self.dead_letter_queue = []

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        reraise=True
    )
    def extract_from_database(
        self,
        connection_string: str,
        query: str,
        watermark_column: Optional[str] = None,
        last_watermark: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Extract data from database with incremental loading support.

        Args:
            connection_string: SQLAlchemy connection string
            query: SQL query to execute
            watermark_column: Column to use for incremental loading
            last_watermark: Last successfully loaded timestamp
        """
        engine = sqlalchemy.create_engine(connection_string)

        try:
            # Incremental loading using watermark
            if watermark_column and last_watermark:
                incremental_query = f"""
                    SELECT * FROM ({query}) AS base
                    WHERE {watermark_column} > '{last_watermark}'
                    ORDER BY {watermark_column}
                """
                df = pd.read_sql(incremental_query, engine)
                logger.info(f"Extracted {len(df)} incremental records")
            else:
                df = pd.read_sql(query, engine)
                logger.info(f"Extracted {len(df)} full records")

            # Add extraction metadata
            df['_extracted_at'] = datetime.utcnow()
            df['_source'] = 'database'

            return df

        except Exception as e:
            logger.error(f"Database extraction failed: {str(e)}")
            raise
        finally:
            engine.dispose()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60)
    )
    def extract_from_api(
        self,
        api_url: str,
        headers: Dict,
        params: Dict,
        pagination_strategy: str = "offset"
    ) -> List[Dict]:
        """
        Extract data from REST API with pagination support.

        Args:
            api_url: Base API URL
            headers: Request headers including authentication
            params: Query parameters
            pagination_strategy: "offset", "cursor", or "page"
        """
        import requests

        all_data = []
        page = 0
        has_more = True

        while has_more:
            try:
                # Adjust parameters based on pagination strategy
                if pagination_strategy == "offset":
                    params['offset'] = page * params.get('limit', 100)
                elif pagination_strategy == "page":
                    params['page'] = page

                response = requests.get(api_url, headers=headers, params=params, timeout=30)
                response.raise_for_status()

                data = response.json()

                # Handle different API response structures
                if isinstance(data, dict):
                    records = data.get('data', data.get('results', []))
                    has_more = data.get('has_more', False) or len(records) == params.get('limit', 100)
                    if pagination_strategy == "cursor" and 'next_cursor' in data:
                        params['cursor'] = data['next_cursor']
                else:
                    records = data
                    has_more = len(records) == params.get('limit', 100)

                all_data.extend(records)
                page += 1

                logger.info(f"Fetched page {page}, total records: {len(all_data)}")

            except Exception as e:
                logger.error(f"API extraction failed on page {page}: {str(e)}")
                raise

        return all_data

    def validate_and_clean(self, df: pd.DataFrame, schema: Dict) -> pd.DataFrame:
        """
        Validate data against schema and clean invalid records.

        Args:
            df: Input DataFrame
            schema: Schema definition with column types and constraints
        """
        original_count = len(df)

        # Type validation and coercion
        for column, dtype in schema.get('dtypes', {}).items():
            if column in df.columns:
                try:
                    df[column] = df[column].astype(dtype)
                except Exception as e:
                    logger.warning(f"Type conversion failed for {column}: {str(e)}")

        # Required fields check
        required_fields = schema.get('required_fields', [])
        for field in required_fields:
            if field not in df.columns:
                raise ValueError(f"Required field {field} missing from data")

            # Remove rows with null required fields
            null_mask = df[field].isnull()
            if null_mask.any():
                invalid_records = df[null_mask].to_dict('records')
                self.dead_letter_queue.extend(invalid_records)
                df = df[~null_mask]
                logger.warning(f"Removed {null_mask.sum()} records with null {field}")

        # Custom validation rules
        for validation in schema.get('validations', []):
            field = validation['field']
            rule = validation['rule']

            if rule['type'] == 'range':
                valid_mask = (df[field] >= rule['min']) & (df[field] <= rule['max'])
                df = df[valid_mask]
            elif rule['type'] == 'regex':
                import re
                valid_mask = df[field].astype(str).str.match(rule['pattern'])
                df = df[valid_mask]

        logger.info(f"Validation: {original_count} -> {len(df)} records ({original_count - len(df)} invalid)")

        return df

    def write_to_data_lake(
        self,
        df: pd.DataFrame,
        path: str,
        partition_cols: Optional[List[str]] = None,
        file_format: str = "parquet"
    ) -> str:
        """
        Write DataFrame to data lake with partitioning.

        Args:
            df: DataFrame to write
            path: Target path (S3, GCS, ADLS)
            partition_cols: Columns to partition by
            file_format: "parquet", "delta", or "iceberg"
        """
        if file_format == "parquet":
            df.to_parquet(
                path,
                partition_cols=partition_cols,
                compression='snappy',
                index=False
            )
        elif file_format == "delta":
            from deltalake import write_deltalake
            write_deltalake(path, df, partition_by=partition_cols, mode="append")

        logger.info(f"Written {len(df)} records to {path}")
        return path

    def save_dead_letter_queue(self, path: str):
        """Save failed records to dead letter queue for later investigation."""
        if self.dead_letter_queue:
            dlq_df = pd.DataFrame(self.dead_letter_queue)
            dlq_df['_dlq_timestamp'] = datetime.utcnow()
            dlq_df.to_parquet(f"{path}/dlq/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.parquet")
            logger.info(f"Saved {len(self.dead_letter_queue)} records to DLQ")
```

**Streaming Data Ingestion**

Implement real-time streaming ingestion for low-latency data processing:

**Kafka Consumer with Exactly-Once Semantics**
```python
# streaming_ingestion.py
from confluent_kafka import Consumer, Producer, KafkaError, TopicPartition
from typing import Dict, Callable, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StreamingDataIngester:
    """Handles streaming data ingestion from Kafka with exactly-once processing."""

    def __init__(self, kafka_config: Dict):
        self.consumer_config = {
            'bootstrap.servers': kafka_config['bootstrap_servers'],
            'group.id': kafka_config['consumer_group'],
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': False,  # Manual commit for exactly-once
            'isolation.level': 'read_committed',  # Read only committed messages
            'max.poll.interval.ms': 300000,
        }

        self.producer_config = {
            'bootstrap.servers': kafka_config['bootstrap_servers'],
            'transactional.id': kafka_config.get('transactional_id', 'data-ingestion-txn'),
            'enable.idempotence': True,
            'acks': 'all',
        }

        self.consumer = Consumer(self.consumer_config)
        self.producer = Producer(self.producer_config)
        self.producer.init_transactions()

    def consume_and_process(
        self,
        topics: list,
        process_func: Callable,
        batch_size: int = 100,
        output_topic: Optional[str] = None
    ):
        """
        Consume messages from Kafka topics and process with exactly-once semantics.

        Args:
            topics: List of Kafka topics to consume from
            process_func: Function to process each batch of messages
            batch_size: Number of messages to process in each batch
            output_topic: Optional topic to write processed results
        """
        self.consumer.subscribe(topics)

        message_batch = []

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)

                if msg is None:
                    if message_batch:
                        self._process_batch(message_batch, process_func, output_topic)
                        message_batch = []
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logger.error(f"Consumer error: {msg.error()}")
                        break

                # Parse message
                try:
                    value = json.loads(msg.value().decode('utf-8'))
                    message_batch.append({
                        'key': msg.key().decode('utf-8') if msg.key() else None,
                        'value': value,
                        'partition': msg.partition(),
                        'offset': msg.offset(),
                        'timestamp': msg.timestamp()[1]
                    })
                except Exception as e:
                    logger.error(f"Failed to parse message: {e}")
                    continue

                # Process batch when full
                if len(message_batch) >= batch_size:
                    self._process_batch(message_batch, process_func, output_topic)
                    message_batch = []

        except KeyboardInterrupt:
            logger.info("Consumer interrupted by user")
        finally:
            self.consumer.close()
            self.producer.flush()

    def _process_batch(
        self,
        messages: list,
        process_func: Callable,
        output_topic: Optional[str]
    ):
        """Process a batch of messages with transaction support."""
        try:
            # Begin transaction
            self.producer.begin_transaction()

            # Process messages
            processed_results = process_func(messages)

            # Write processed results to output topic
            if output_topic and processed_results:
                for result in processed_results:
                    self.producer.produce(
                        output_topic,
                        key=result.get('key'),
                        value=json.dumps(result['value']).encode('utf-8')
                    )

            # Commit consumer offsets as part of transaction
            offsets = [
                TopicPartition(
                    topic=msg['topic'],
                    partition=msg['partition'],
                    offset=msg['offset'] + 1
                )
                for msg in messages
            ]

            self.producer.send_offsets_to_transaction(
                offsets,
                self.consumer.consumer_group_metadata()
            )

            # Commit transaction
            self.producer.commit_transaction()

            logger.info(f"Successfully processed batch of {len(messages)} messages")

        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            self.producer.abort_transaction()
            raise

    def process_with_windowing(
        self,
        messages: list,
        window_duration_seconds: int = 60
    ) -> list:
        """
        Process messages with time-based windowing for aggregations.

        Args:
            messages: Batch of messages to process
            window_duration_seconds: Window size in seconds
        """
        from collections import defaultdict

        windows = defaultdict(list)

        # Group messages by window
        for msg in messages:
            timestamp = msg['timestamp']
            window_start = (timestamp // (window_duration_seconds * 1000)) * (window_duration_seconds * 1000)
            windows[window_start].append(msg['value'])

        # Process each window
        results = []
        for window_start, window_messages in windows.items():
            aggregated = {
                'window_start': datetime.fromtimestamp(window_start / 1000).isoformat(),
                'window_end': datetime.fromtimestamp((window_start + window_duration_seconds * 1000) / 1000).isoformat(),
                'count': len(window_messages),
                'data': window_messages
            }
            results.append({'key': str(window_start), 'value': aggregated})

        return results
```

### 3. Workflow Orchestration Implementation

**Apache Airflow DAG for Batch Processing**

Implement production-ready Airflow DAGs with proper dependency management:

```python
# dags/data_pipeline_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.utils.dates import days_ago
from airflow.utils.task_group import TaskGroup
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['data-alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
    'sla': timedelta(hours=2),
}

with DAG(
    dag_id='daily_user_analytics_pipeline',
    default_args=default_args,
    description='Daily batch processing of user analytics data',
    schedule_interval='0 2 * * *',  # 2 AM daily
    start_date=days_ago(1),
    catchup=False,
    max_active_runs=1,
    tags=['analytics', 'batch', 'production'],
) as dag:

    def extract_user_events(**context):
        """Extract user events from operational database."""
        from batch_ingestion import BatchDataIngester

        execution_date = context['execution_date']

        ingester = BatchDataIngester(config={})

        # Extract incremental data
        df = ingester.extract_from_database(
            connection_string='postgresql://user:pass@host:5432/analytics',
            query='SELECT * FROM user_events',
            watermark_column='event_timestamp',
            last_watermark=execution_date - timedelta(days=1)
        )

        # Validate and clean
        schema = {
            'required_fields': ['user_id', 'event_type', 'event_timestamp'],
            'dtypes': {
                'user_id': 'int64',
                'event_timestamp': 'datetime64[ns]'
            }
        }
        df = ingester.validate_and_clean(df, schema)

        # Write to S3 raw layer
        s3_path = f"s3://data-lake/raw/user_events/date={execution_date.strftime('%Y-%m-%d')}"
        ingester.write_to_data_lake(df, s3_path, file_format='parquet')

        # Save any failed records
        ingester.save_dead_letter_queue('s3://data-lake/dlq/user_events')

        # Push metadata to XCom
        context['task_instance'].xcom_push(key='raw_path', value=s3_path)
        context['task_instance'].xcom_push(key='record_count', value=len(df))

        logger.info(f"Extracted {len(df)} user events to {s3_path}")

    def extract_user_profiles(**context):
        """Extract user profile data."""
        from batch_ingestion import BatchDataIngester

        execution_date = context['execution_date']
        ingester = BatchDataIngester(config={})

        df = ingester.extract_from_database(
            connection_string='postgresql://user:pass@host:5432/users',
            query='SELECT * FROM user_profiles WHERE updated_at >= %(start_date)s',
            watermark_column='updated_at',
            last_watermark=execution_date - timedelta(days=1)
        )

        s3_path = f"s3://data-lake/raw/user_profiles/date={execution_date.strftime('%Y-%m-%d')}"
        ingester.write_to_data_lake(df, s3_path, file_format='parquet')

        context['task_instance'].xcom_push(key='raw_path', value=s3_path)
        logger.info(f"Extracted {len(df)} user profiles to {s3_path}")

    def run_data_quality_checks(**context):
        """Run data quality checks using Great Expectations."""
        import great_expectations as gx

        events_path = context['task_instance'].xcom_pull(
            task_ids='extract_user_events',
            key='raw_path'
        )

        context_ge = gx.get_context()

        # Create or get data source
        datasource = context_ge.sources.add_or_update_pandas(name="s3_datasource")

        # Define expectations
        validator = context_ge.get_validator(
            batch_request={
                "datasource_name": "s3_datasource",
                "data_asset_name": "user_events",
                "options": {"path": events_path}
            },
            expectation_suite_name="user_events_suite"
        )

        # Add expectations
        validator.expect_table_row_count_to_be_between(min_value=1000, max_value=10000000)
        validator.expect_column_values_to_not_be_null(column="user_id")
        validator.expect_column_values_to_not_be_null(column="event_timestamp")
        validator.expect_column_values_to_be_in_set(
            column="event_type",
            value_set=["page_view", "click", "purchase", "signup"]
        )

        # Run validation
        checkpoint = context_ge.add_or_update_checkpoint(
            name="user_events_checkpoint",
            validations=[{"batch_request": validator.active_batch_request}]
        )

        result = checkpoint.run()

        if not result.success:
            raise ValueError(f"Data quality checks failed: {result}")

        logger.info("All data quality checks passed")

    def trigger_dbt_transformation(**context):
        """Trigger dbt transformations."""
        from airflow.providers.dbt.cloud.operators.dbt import DbtCloudRunJobOperator

        # Alternative: Use BashOperator for dbt Core
        import subprocess

        result = subprocess.run(
            ['dbt', 'run', '--models', 'staging.user_events', '--profiles-dir', '/opt/airflow/dbt'],
            capture_output=True,
            text=True,
            check=True
        )

        logger.info(f"dbt run output: {result.stdout}")

        # Run dbt tests
        test_result = subprocess.run(
            ['dbt', 'test', '--models', 'staging.user_events', '--profiles-dir', '/opt/airflow/dbt'],
            capture_output=True,
            text=True,
            check=True
        )

        logger.info(f"dbt test output: {test_result.stdout}")

    def publish_metrics(**context):
        """Publish pipeline metrics to monitoring system."""
        import boto3

        cloudwatch = boto3.client('cloudwatch')

        record_count = context['task_instance'].xcom_pull(
            task_ids='extract_user_events',
            key='record_count'
        )

        cloudwatch.put_metric_data(
            Namespace='DataPipeline/UserAnalytics',
            MetricData=[
                {
                    'MetricName': 'RecordsProcessed',
                    'Value': record_count,
                    'Unit': 'Count',
                    'Timestamp': context['execution_date']
                },
                {
                    'MetricName': 'PipelineSuccess',
                    'Value': 1,
                    'Unit': 'Count',
                    'Timestamp': context['execution_date']
                }
            ]
        )

        logger.info(f"Published metrics: {record_count} records processed")

    # Define task dependencies with task groups
    with TaskGroup('extract_data', tooltip='Extract data from sources') as extract_group:
        extract_events = PythonOperator(
            task_id='extract_user_events',
            python_callable=extract_user_events,
            provide_context=True
        )

        extract_profiles = PythonOperator(
            task_id='extract_user_profiles',
            python_callable=extract_user_profiles,
            provide_context=True
        )

    quality_check = PythonOperator(
        task_id='run_data_quality_checks',
        python_callable=run_data_quality_checks,
        provide_context=True
    )

    transform = PythonOperator(
        task_id='trigger_dbt_transformation',
        python_callable=trigger_dbt_transformation,
        provide_context=True
    )

    metrics = PythonOperator(
        task_id='publish_metrics',
        python_callable=publish_metrics,
        provide_context=True,
        trigger_rule='all_done'  # Run even if upstream fails
    )

    # Define DAG flow
    extract_group >> quality_check >> transform >> metrics
```

**Prefect Flow for Modern Orchestration**

```python
# flows/prefect_pipeline.py
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect.artifacts import create_table_artifact
from datetime import timedelta
import pandas as pd

@task(
    retries=3,
    retry_delay_seconds=300,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(hours=1)
)
def extract_data(source: str, execution_date: str) -> pd.DataFrame:
    """Extract data with caching for idempotency."""
    from batch_ingestion import BatchDataIngester

    ingester = BatchDataIngester(config={})
    df = ingester.extract_from_database(
        connection_string=f'postgresql://host/{source}',
        query=f'SELECT * FROM {source}',
        watermark_column='updated_at',
        last_watermark=execution_date
    )

    return df

@task(retries=2)
def validate_data(df: pd.DataFrame, schema: dict) -> pd.DataFrame:
    """Validate data quality."""
    from batch_ingestion import BatchDataIngester

    ingester = BatchDataIngester(config={})
    validated_df = ingester.validate_and_clean(df, schema)

    # Create Prefect artifact for visibility
    create_table_artifact(
        key="validation-summary",
        table={
            "original_count": len(df),
            "valid_count": len(validated_df),
            "invalid_count": len(df) - len(validated_df)
        }
    )

    return validated_df

@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply business logic transformations."""
    # Example transformations
    df['processed_at'] = pd.Timestamp.now()
    df['revenue'] = df['quantity'] * df['unit_price']

    return df

@task(retries=3)
def load_to_warehouse(df: pd.DataFrame, table: str):
    """Load data to warehouse."""
    from sqlalchemy import create_engine

    engine = create_engine('snowflake://user:pass@account/database')
    df.to_sql(
        table,
        engine,
        if_exists='append',
        index=False,
        method='multi',
        chunksize=10000
    )

@flow(
    name="user-analytics-pipeline",
    log_prints=True,
    retries=1,
    retry_delay_seconds=60
)
def user_analytics_pipeline(execution_date: str):
    """Main pipeline flow with parallel execution."""

    # Extract data from multiple sources in parallel
    events_future = extract_data.submit("user_events", execution_date)
    profiles_future = extract_data.submit("user_profiles", execution_date)

    # Wait for extraction to complete
    events_df = events_future.result()
    profiles_df = profiles_future.result()

    # Validate data in parallel
    schema = {'required_fields': ['user_id', 'timestamp']}
    validated_events = validate_data.submit(events_df, schema)
    validated_profiles = validate_data.submit(profiles_df, schema)

    # Wait for validation
    events_valid = validated_events.result()
    profiles_valid = validated_profiles.result()

    # Transform and load
    transformed_events = transform_data(events_valid)
    load_to_warehouse(transformed_events, "analytics.user_events")

    print(f"Pipeline completed: {len(transformed_events)} records processed")

if __name__ == "__main__":
    from datetime import datetime
    user_analytics_pipeline(datetime.now().strftime('%Y-%m-%d'))
```

### 4. Data Transformation with dbt

**dbt Project Structure**

Implement analytics engineering best practices with dbt:

```sql
-- models/staging/stg_user_events.sql
{{
  config(
    materialized='incremental',
    unique_key='event_id',
    on_schema_change='sync_all_columns',
    partition_by={
      "field": "event_date",
      "data_type": "date",
      "granularity": "day"
    },
    cluster_by=['user_id', 'event_type']
  )
}}

WITH source_data AS (
    SELECT
        event_id,
        user_id,
        event_type,
        event_timestamp,
        event_properties,
        DATE(event_timestamp) AS event_date,
        _extracted_at
    FROM {{ source('raw', 'user_events') }}

    {% if is_incremental() %}
        -- Incremental loading: only process new data
        WHERE event_timestamp > (SELECT MAX(event_timestamp) FROM {{ this }})
        -- Add lookback window for late-arriving data
        AND event_timestamp > DATEADD(day, -3, (SELECT MAX(event_timestamp) FROM {{ this }}))
    {% endif %}
),

deduplicated AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY event_id
            ORDER BY _extracted_at DESC
        ) AS row_num
    FROM source_data
)

SELECT
    event_id,
    user_id,
    event_type,
    event_timestamp,
    event_date,
    PARSE_JSON(event_properties) AS event_properties_json,
    _extracted_at
FROM deduplicated
WHERE row_num = 1
```

```sql
-- models/marts/fct_user_daily_activity.sql
{{
  config(
    materialized='incremental',
    unique_key=['user_id', 'activity_date'],
    incremental_strategy='merge',
    cluster_by=['activity_date', 'user_id']
  )
}}

WITH daily_events AS (
    SELECT
        user_id,
        event_date AS activity_date,
        COUNT(*) AS total_events,
        COUNT(DISTINCT event_type) AS distinct_event_types,
        COUNT_IF(event_type = 'purchase') AS purchase_count,
        SUM(CASE
            WHEN event_type = 'purchase'
            THEN event_properties_json:amount::FLOAT
            ELSE 0
        END) AS total_revenue
    FROM {{ ref('stg_user_events') }}

    {% if is_incremental() %}
        WHERE event_date > (SELECT MAX(activity_date) FROM {{ this }})
    {% endif %}

    GROUP BY 1, 2
),

user_profiles AS (
    SELECT
        user_id,
        signup_date,
        user_tier,
        geographic_region
    FROM {{ ref('dim_users') }}
)

SELECT
    e.user_id,
    e.activity_date,
    e.total_events,
    e.distinct_event_types,
    e.purchase_count,
    e.total_revenue,
    p.user_tier,
    p.geographic_region,
    DATEDIFF(day, p.signup_date, e.activity_date) AS days_since_signup,
    CURRENT_TIMESTAMP() AS _dbt_updated_at
FROM daily_events e
LEFT JOIN user_profiles p
    ON e.user_id = p.user_id
```

```yaml
# models/staging/sources.yml
version: 2

sources:
  - name: raw
    database: data_lake
    schema: raw_data
    tables:
      - name: user_events
        description: "Raw user event data from operational systems"
        freshness:
          warn_after: {count: 2, period: hour}
          error_after: {count: 6, period: hour}
        loaded_at_field: _extracted_at
        columns:
          - name: event_id
            description: "Unique identifier for each event"
            tests:
              - unique
              - not_null
          - name: user_id
            description: "User identifier"
            tests:
              - not_null
              - relationships:
                  to: ref('dim_users')
                  field: user_id
          - name: event_timestamp
            description: "Timestamp when event occurred"
            tests:
              - not_null

models:
  - name: stg_user_events
    description: "Staging model for cleaned and deduplicated user events"
    columns:
      - name: event_id
        tests:
          - unique
          - not_null
      - name: user_id
        tests:
          - not_null
      - name: event_type
        tests:
          - accepted_values:
              values: ['page_view', 'click', 'purchase', 'signup', 'logout']
    tests:
      - dbt_expectations.expect_table_row_count_to_be_between:
          min_value: 1000
          max_value: 100000000
      - dbt_expectations.expect_row_values_to_have_data_for_every_n_datepart:
          date_col: event_date
          date_part: day
```

```yaml
# dbt_project.yml
name: 'user_analytics'
version: '1.0.0'
config-version: 2

profile: 'snowflake_prod'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  user_analytics:
    staging:
      +materialized: view
      +schema: staging
    marts:
      +materialized: table
      +schema: analytics

on-run-start:
  - "{{ create_audit_log_table() }}"

on-run-end:
  - "{{ log_dbt_results(results) }}"
```

### 5. Data Quality and Validation Framework

**Great Expectations Integration**

Implement comprehensive data quality monitoring:

```python
# data_quality/expectations_suite.py
import great_expectations as gx
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class DataQualityFramework:
    """Comprehensive data quality validation using Great Expectations."""

    def __init__(self, context_root_dir: str = "./great_expectations"):
        self.context = gx.get_context(context_root_dir=context_root_dir)

    def create_expectation_suite(
        self,
        suite_name: str,
        expectations_config: Dict
    ) -> gx.ExpectationSuite:
        """
        Create or update expectation suite for a dataset.

        Args:
            suite_name: Name of the expectation suite
            expectations_config: Dictionary defining expectations
        """
        suite = self.context.add_or_update_expectation_suite(
            expectation_suite_name=suite_name
        )

        # Table-level expectations
        if 'table' in expectations_config:
            for expectation in expectations_config['table']:
                suite.add_expectation(expectation)

        # Column-level expectations
        if 'columns' in expectations_config:
            for column, column_expectations in expectations_config['columns'].items():
                for expectation in column_expectations:
                    expectation['kwargs']['column'] = column
                    suite.add_expectation(expectation)

        self.context.save_expectation_suite(suite)
        logger.info(f"Created expectation suite: {suite_name}")

        return suite

    def validate_dataframe(
        self,
        df,
        suite_name: str,
        data_asset_name: str
    ) -> gx.CheckpointResult:
        """
        Validate a pandas/Spark DataFrame against expectations.

        Args:
            df: DataFrame to validate
            suite_name: Name of expectation suite to use
            data_asset_name: Name for this data asset
        """
        # Create batch request
        batch_request = {
            "datasource_name": "runtime_datasource",
            "data_connector_name": "runtime_data_connector",
            "data_asset_name": data_asset_name,
            "runtime_parameters": {"batch_data": df},
            "batch_identifiers": {"default_identifier_name": "default"}
        }

        # Create checkpoint
        checkpoint_config = {
            "name": f"{data_asset_name}_checkpoint",
            "config_version": 1.0,
            "class_name": "SimpleCheckpoint",
            "validations": [
                {
                    "batch_request": batch_request,
                    "expectation_suite_name": suite_name
                }
            ]
        }

        checkpoint = self.context.add_or_update_checkpoint(**checkpoint_config)

        # Run validation
        result = checkpoint.run()

        # Log results
        if result.success:
            logger.info(f"Validation passed for {data_asset_name}")
        else:
            logger.error(f"Validation failed for {data_asset_name}")
            for validation_result in result.run_results.values():
                for result_item in validation_result["validation_result"]["results"]:
                    if not result_item.success:
                        logger.error(f"Failed: {result_item.expectation_config.expectation_type}")

        return result

    def create_data_docs(self):
        """Build and update Great Expectations data documentation."""
        self.context.build_data_docs()
        logger.info("Data docs updated")


# Example usage
def setup_user_events_expectations():
    """Setup expectations for user events dataset."""

    dq_framework = DataQualityFramework()

    expectations_config = {
        'table': [
            {
                'expectation_type': 'expect_table_row_count_to_be_between',
                'kwargs': {
                    'min_value': 1000,
                    'max_value': 10000000
                }
            },
            {
                'expectation_type': 'expect_table_column_count_to_equal',
                'kwargs': {
                    'value': 8
                }
            }
        ],
        'columns': {
            'event_id': [
                {
                    'expectation_type': 'expect_column_values_to_be_unique',
                    'kwargs': {}
                },
                {
                    'expectation_type': 'expect_column_values_to_not_be_null',
                    'kwargs': {}
                }
            ],
            'user_id': [
                {
                    'expectation_type': 'expect_column_values_to_not_be_null',
                    'kwargs': {}
                },
                {
                    'expectation_type': 'expect_column_values_to_be_of_type',
                    'kwargs': {
                        'type_': 'int64'
                    }
                }
            ],
            'event_type': [
                {
                    'expectation_type': 'expect_column_values_to_be_in_set',
                    'kwargs': {
                        'value_set': ['page_view', 'click', 'purchase', 'signup']
                    }
                }
            ],
            'event_timestamp': [
                {
                    'expectation_type': 'expect_column_values_to_not_be_null',
                    'kwargs': {}
                },
                {
                    'expectation_type': 'expect_column_values_to_be_dateutil_parseable',
                    'kwargs': {}
                }
            ],
            'revenue': [
                {
                    'expectation_type': 'expect_column_values_to_be_between',
                    'kwargs': {
                        'min_value': 0,
                        'max_value': 100000,
                        'allow_cross_type_comparisons': True
                    }
                }
            ]
        }
    }

    suite = dq_framework.create_expectation_suite(
        suite_name='user_events_suite',
        expectations_config=expectations_config
    )

    return dq_framework
```

### 6. Storage Strategy and Lakehouse Architecture

**Delta Lake Implementation**

Implement modern lakehouse architecture with ACID transactions:

```python
# storage/delta_lake_manager.py
from deltalake import DeltaTable, write_deltalake
import pyarrow as pa
import pyarrow.parquet as pq
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class DeltaLakeManager:
    """Manage Delta Lake tables with ACID transactions and time travel."""

    def __init__(self, storage_path: str):
        """
        Initialize Delta Lake manager.

        Args:
            storage_path: Base path for Delta Lake (S3, ADLS, GCS)
        """
        self.storage_path = storage_path

    def create_or_update_table(
        self,
        df,
        table_name: str,
        partition_columns: Optional[List[str]] = None,
        mode: str = "append",
        merge_schema: bool = True,
        overwrite_schema: bool = False
    ):
        """
        Write DataFrame to Delta table with schema evolution support.

        Args:
            df: Pandas or PyArrow DataFrame
            table_name: Name of Delta table
            partition_columns: Columns to partition by
            mode: "append", "overwrite", or "merge"
            merge_schema: Allow schema evolution
            overwrite_schema: Replace entire schema
        """
        table_path = f"{self.storage_path}/{table_name}"

        write_deltalake(
            table_path,
            df,
            mode=mode,
            partition_by=partition_columns,
            schema_mode="merge" if merge_schema else "overwrite" if overwrite_schema else None,
            engine='rust'
        )

        logger.info(f"Written data to Delta table: {table_name} (mode={mode})")

    def upsert_data(
        self,
        df,
        table_name: str,
        predicate: str,
        update_columns: Dict[str, str],
        insert_columns: Dict[str, str]
    ):
        """
        Perform upsert (merge) operation on Delta table.

        Args:
            df: DataFrame with new/updated data
            table_name: Target Delta table
            predicate: Merge condition (e.g., "target.id = source.id")
            update_columns: Columns to update on match
            insert_columns: Columns to insert on no match
        """
        table_path = f"{self.storage_path}/{table_name}"
        dt = DeltaTable(table_path)

        # Create PyArrow table from DataFrame
        if hasattr(df, 'to_pyarrow'):
            source_table = df.to_pyarrow()
        else:
            source_table = pa.Table.from_pandas(df)

        # Perform merge
        (
            dt.merge(
                source=source_table,
                predicate=predicate,
                source_alias="source",
                target_alias="target"
            )
            .when_matched_update(updates=update_columns)
            .when_not_matched_insert(values=insert_columns)
            .execute()
        )

        logger.info(f"Upsert completed for table: {table_name}")

    def optimize_table(
        self,
        table_name: str,
        partition_filters: Optional[List[tuple]] = None,
        z_order_by: Optional[List[str]] = None
    ):
        """
        Optimize Delta table by compacting small files and Z-ordering.

        Args:
            table_name: Delta table to optimize
            partition_filters: Filter specific partitions
            z_order_by: Columns for Z-order optimization
        """
        table_path = f"{self.storage_path}/{table_name}"
        dt = DeltaTable(table_path)

        # Compact small files
        dt.optimize.compact()

        # Z-order for better query performance
        if z_order_by:
            dt.optimize.z_order(z_order_by)

        logger.info(f"Optimized table: {table_name}")

    def vacuum_old_files(
        self,
        table_name: str,
        retention_hours: int = 168  # 7 days default
    ):
        """
        Remove old data files no longer referenced by the transaction log.

        Args:
            table_name: Delta table to vacuum
            retention_hours: Minimum age of files to delete (hours)
        """
        table_path = f"{self.storage_path}/{table_name}"
        dt = DeltaTable(table_path)

        dt.vacuum(retention_hours=retention_hours)

        logger.info(f"Vacuumed table: {table_name} (retention={retention_hours}h)")

    def time_travel_query(
        self,
        table_name: str,
        version: Optional[int] = None,
        timestamp: Optional[str] = None
    ) -> pa.Table:
        """
        Query historical version of Delta table.

        Args:
            table_name: Delta table name
            version: Specific version number
            timestamp: Timestamp string (ISO format)
        """
        table_path = f"{self.storage_path}/{table_name}"
        dt = DeltaTable(table_path)

        if version is not None:
            dt.load_version(version)
        elif timestamp is not None:
            dt.load_with_datetime(timestamp)

        return dt.to_pyarrow_table()

    def get_table_history(self, table_name: str) -> List[Dict]:
        """Get commit history for Delta table."""
        table_path = f"{self.storage_path}/{table_name}"
        dt = DeltaTable(table_path)

        return dt.history()
```

**Apache Iceberg with Spark**

```python
# storage/iceberg_manager.py
from pyspark.sql import SparkSession
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class IcebergTableManager:
    """Manage Apache Iceberg tables with Spark."""

    def __init__(self, catalog_config: Dict):
        """
        Initialize Iceberg table manager with Spark.

        Args:
            catalog_config: Iceberg catalog configuration
        """
        self.spark = SparkSession.builder \
            .appName("IcebergDataPipeline") \
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
            .config("spark.sql.catalog.iceberg_catalog", "org.apache.iceberg.spark.SparkCatalog") \
            .config("spark.sql.catalog.iceberg_catalog.type", catalog_config.get('type', 'hadoop')) \
            .config("spark.sql.catalog.iceberg_catalog.warehouse", catalog_config['warehouse']) \
            .getOrCreate()

        self.catalog_name = "iceberg_catalog"

    def create_table(
        self,
        database: str,
        table_name: str,
        df,
        partition_by: Optional[List[str]] = None,
        sort_order: Optional[List[str]] = None
    ):
        """
        Create Iceberg table from DataFrame.

        Args:
            database: Database name
            table_name: Table name
            df: Spark DataFrame
            partition_by: Partition columns
            sort_order: Sort order for data files
        """
        full_table_name = f"{self.catalog_name}.{database}.{table_name}"

        # Write DataFrame as Iceberg table
        writer = df.writeTo(full_table_name).using("iceberg")

        if partition_by:
            writer = writer.partitionedBy(*partition_by)

        if sort_order:
            for col in sort_order:
                writer = writer.sortedBy(col)

        writer.create()

        logger.info(f"Created Iceberg table: {full_table_name}")

    def incremental_upsert(
        self,
        database: str,
        table_name: str,
        df,
        merge_keys: List[str],
        update_columns: Optional[List[str]] = None
    ):
        """
        Perform incremental upsert using MERGE INTO.

        Args:
            database: Database name
            table_name: Table name
            df: Spark DataFrame with updates
            merge_keys: Columns to match on
            update_columns: Columns to update (all if None)
        """
        full_table_name = f"{self.catalog_name}.{database}.{table_name}"

        # Register DataFrame as temp view
        df.createOrReplaceTempView("updates")

        # Build merge condition
        merge_condition = " AND ".join([
            f"target.{key} = updates.{key}" for key in merge_keys
        ])

        # Build update set clause
        if update_columns:
            update_set = ", ".join([
                f"{col} = updates.{col}" for col in update_columns
            ])
        else:
            update_set = ", ".join([
                f"{col} = updates.{col}" for col in df.columns
            ])

        # Build insert values
        insert_cols = ", ".join(df.columns)
        insert_vals = ", ".join([f"updates.{col}" for col in df.columns])

        # Execute merge
        merge_query = f"""
            MERGE INTO {full_table_name} AS target
            USING updates
            ON {merge_condition}
            WHEN MATCHED THEN
                UPDATE SET {update_set}
            WHEN NOT MATCHED THEN
                INSERT ({insert_cols})
                VALUES ({insert_vals})
        """

        self.spark.sql(merge_query)
        logger.info(f"Completed upsert for: {full_table_name}")

    def optimize_table(
        self,
        database: str,
        table_name: str
    ):
        """
        Optimize Iceberg table by rewriting small files.

        Args:
            database: Database name
            table_name: Table name
        """
        full_table_name = f"{self.catalog_name}.{database}.{table_name}"

        # Rewrite data files
        self.spark.sql(f"""
            CALL {self.catalog_name}.system.rewrite_data_files(
                table => '{database}.{table_name}',
                strategy => 'binpack',
                options => map('target-file-size-bytes', '536870912')
            )
        """)

        # Expire old snapshots (keep last 7 days)
        self.spark.sql(f"""
            CALL {self.catalog_name}.system.expire_snapshots(
                table => '{database}.{table_name}',
                older_than => DATE_SUB(CURRENT_DATE(), 7),
                retain_last => 5
            )
        """)

        logger.info(f"Optimized table: {full_table_name}")

    def time_travel_query(
        self,
        database: str,
        table_name: str,
        snapshot_id: Optional[int] = None,
        timestamp_ms: Optional[int] = None
    ):
        """
        Query historical snapshot of Iceberg table.

        Args:
            database: Database name
            table_name: Table name
            snapshot_id: Specific snapshot ID
            timestamp_ms: Timestamp in milliseconds
        """
        full_table_name = f"{self.catalog_name}.{database}.{table_name}"

        if snapshot_id:
            query = f"SELECT * FROM {full_table_name} VERSION AS OF {snapshot_id}"
        elif timestamp_ms:
            query = f"SELECT * FROM {full_table_name} TIMESTAMP AS OF {timestamp_ms}"
        else:
            query = f"SELECT * FROM {full_table_name}"

        return self.spark.sql(query)
```

### 7. Monitoring, Observability, and Cost Optimization

**Pipeline Monitoring Framework**

```python
# monitoring/pipeline_monitor.py
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
import boto3
import json

logger = logging.getLogger(__name__)

@dataclass
class PipelineMetrics:
    """Data class for pipeline metrics."""
    pipeline_name: str
    execution_id: str
    start_time: datetime
    end_time: Optional[datetime]
    status: str  # running, success, failed
    records_processed: int
    records_failed: int
    data_size_bytes: int
    execution_time_seconds: Optional[float]
    error_message: Optional[str] = None

class PipelineMonitor:
    """Comprehensive pipeline monitoring and alerting."""

    def __init__(self, config: Dict):
        self.config = config
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        self.alert_topic_arn = config.get('sns_topic_arn')

    def track_pipeline_execution(self, metrics: PipelineMetrics):
        """
        Track pipeline execution metrics in CloudWatch.

        Args:
            metrics: Pipeline execution metrics
        """
        namespace = f"DataPipeline/{metrics.pipeline_name}"

        metric_data = [
            {
                'MetricName': 'RecordsProcessed',
                'Value': metrics.records_processed,
                'Unit': 'Count',
                'Timestamp': metrics.start_time
            },
            {
                'MetricName': 'RecordsFailed',
                'Value': metrics.records_failed,
                'Unit': 'Count',
                'Timestamp': metrics.start_time
            },
            {
                'MetricName': 'DataSizeBytes',
                'Value': metrics.data_size_bytes,
                'Unit': 'Bytes',
                'Timestamp': metrics.start_time
            }
        ]

        if metrics.execution_time_seconds:
            metric_data.append({
                'MetricName': 'ExecutionTime',
                'Value': metrics.execution_time_seconds,
                'Unit': 'Seconds',
                'Timestamp': metrics.start_time
            })

        if metrics.status == 'success':
            metric_data.append({
                'MetricName': 'PipelineSuccess',
                'Value': 1,
                'Unit': 'Count',
                'Timestamp': metrics.start_time
            })
        elif metrics.status == 'failed':
            metric_data.append({
                'MetricName': 'PipelineFailure',
                'Value': 1,
                'Unit': 'Count',
                'Timestamp': metrics.start_time
            })

        self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=metric_data
        )

        logger.info(f"Tracked metrics for pipeline: {metrics.pipeline_name}")

    def send_alert(
        self,
        severity: str,
        title: str,
        message: str,
        metadata: Optional[Dict] = None
    ):
        """
        Send alert notification via SNS.

        Args:
            severity: "critical", "warning", or "info"
            title: Alert title
            message: Alert message
            metadata: Additional context
        """
        alert_payload = {
            'severity': severity,
            'title': title,
            'message': message,
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': metadata or {}
        }

        if self.alert_topic_arn:
            self.sns.publish(
                TopicArn=self.alert_topic_arn,
                Subject=f"[{severity.upper()}] {title}",
                Message=json.dumps(alert_payload, indent=2)
            )
            logger.info(f"Sent {severity} alert: {title}")

    def check_data_freshness(
        self,
        table_path: str,
        max_age_hours: int = 24
    ) -> bool:
        """
        Check if data is fresh enough based on last update.

        Args:
            table_path: Path to data table
            max_age_hours: Maximum acceptable age in hours
        """
        from deltalake import DeltaTable
        from datetime import timedelta

        try:
            dt = DeltaTable(table_path)
            history = dt.history()

            if not history:
                self.send_alert(
                    'warning',
                    'No Data History',
                    f'Table {table_path} has no history'
                )
                return False

            last_update = history[0]['timestamp']
            age = datetime.utcnow() - last_update

            if age > timedelta(hours=max_age_hours):
                self.send_alert(
                    'warning',
                    'Stale Data Detected',
                    f'Table {table_path} is {age.total_seconds() / 3600:.1f} hours old',
                    metadata={'table': table_path, 'last_update': last_update.isoformat()}
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Freshness check failed: {e}")
            return False

    def analyze_pipeline_performance(
        self,
        pipeline_name: str,
        time_range_hours: int = 24
    ) -> Dict:
        """
        Analyze pipeline performance over time period.

        Args:
            pipeline_name: Name of pipeline to analyze
            time_range_hours: Hours of history to analyze
        """
        from datetime import timedelta

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=time_range_hours)

        # Get metrics from CloudWatch
        response = self.cloudwatch.get_metric_statistics(
            Namespace=f"DataPipeline/{pipeline_name}",
            MetricName='ExecutionTime',
            StartTime=start_time,
            EndTime=end_time,
            Period=3600,  # 1 hour
            Statistics=['Average', 'Maximum', 'Minimum']
        )

        datapoints = response.get('Datapoints', [])

        if not datapoints:
            return {'status': 'no_data', 'message': 'No metrics available'}

        avg_execution_time = sum(dp['Average'] for dp in datapoints) / len(datapoints)
        max_execution_time = max(dp['Maximum'] for dp in datapoints)

        performance_summary = {
            'pipeline_name': pipeline_name,
            'time_range_hours': time_range_hours,
            'avg_execution_time_seconds': avg_execution_time,
            'max_execution_time_seconds': max_execution_time,
            'datapoints': len(datapoints)
        }

        # Alert if performance degraded
        if avg_execution_time > 1800:  # 30 minutes threshold
            self.send_alert(
                'warning',
                'Pipeline Performance Degradation',
                f'{pipeline_name} average execution time: {avg_execution_time:.1f}s',
                metadata=performance_summary
            )

        return performance_summary


**Cost Optimization Strategies**

```python
# cost_optimization/optimizer.py
import logging
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class CostOptimizer:
    """Pipeline cost optimization strategies."""

    def __init__(self, config: Dict):
        self.config = config

    def implement_partitioning_strategy(
        self,
        table_name: str,
        partition_columns: List[str],
        partition_type: str = "date"
    ) -> Dict:
        """
        Design optimal partitioning strategy to reduce query costs.

        Recommendations:
        - Date partitioning: For time-series data, partition by date/timestamp
        - User/Entity partitioning: For user-specific queries, partition by user_id
        - Multi-level: Combine date + region for geographic data
        - Avoid over-partitioning: Keep partitions > 1GB for best performance
        """
        strategy = {
            'table_name': table_name,
            'partition_columns': partition_columns,
            'recommendations': []
        }

        if partition_type == "date":
            strategy['recommendations'].extend([
                "Partition by day for daily queries, month for long-term analysis",
                "Use partition pruning in queries: WHERE date = '2025-01-01'",
                "Consider clustering by frequently filtered columns within partitions",
                f"Estimated cost savings: 60-90% for date-range queries"
            ])

        logger.info(f"Partitioning strategy for {table_name}: {strategy}")
        return strategy

    def optimize_file_sizes(
        self,
        table_path: str,
        target_file_size_mb: int = 512
    ):
        """
        Optimize file sizes to reduce metadata overhead and improve query performance.

        Best practices:
        - Target file size: 512MB - 1GB for Parquet
        - Avoid small files (<128MB) which increase metadata overhead
        - Avoid very large files (>2GB) which reduce parallelism
        """
        from deltalake import DeltaTable

        dt = DeltaTable(table_path)

        # Compact small files
        dt.optimize.compact()

        logger.info(f"Optimized file sizes for {table_path}")

        return {
            'table_path': table_path,
            'target_file_size_mb': target_file_size_mb,
            'optimization': 'completed'
        }

    def implement_lifecycle_policies(
        self,
        storage_path: str,
        hot_tier_days: int = 30,
        cold_tier_days: int = 90,
        archive_days: int = 365
    ) -> Dict:
        """
        Design storage lifecycle policies for cost optimization.

        Storage tiers (AWS S3 example):
        - Standard: Frequent access (0-30 days)
        - Infrequent Access: Occasional access (30-90 days)
        - Glacier: Archive (90+ days)

        Cost savings: Up to 90% compared to Standard storage
        """
        lifecycle_policy = {
            'storage_path': storage_path,
            'tiers': {
                'hot': {
                    'days': hot_tier_days,
                    'storage_class': 'STANDARD',
                    'cost_per_gb': 0.023
                },
                'warm': {
                    'days': cold_tier_days - hot_tier_days,
                    'storage_class': 'STANDARD_IA',
                    'cost_per_gb': 0.0125
                },
                'cold': {
                    'days': archive_days - cold_tier_days,
                    'storage_class': 'GLACIER',
                    'cost_per_gb': 0.004
                }
            },
            'estimated_savings_percent': 70
        }

        logger.info(f"Lifecycle policy for {storage_path}: {lifecycle_policy}")
        return lifecycle_policy

    def optimize_compute_resources(
        self,
        workload_type: str,
        data_size_gb: float
    ) -> Dict:
        """
        Recommend optimal compute resources for workload.

        Args:
            workload_type: "batch", "streaming", or "adhoc"
            data_size_gb: Size of data to process
        """
        if workload_type == "batch":
            # Use scheduled spot instances for cost savings
            recommendation = {
                'instance_type': 'c5.4xlarge',
                'instance_count': max(1, int(data_size_gb / 100)),
                'use_spot_instances': True,
                'estimated_cost_savings': '70%',
                'notes': 'Spot instances for non-time-critical batch jobs'
            }
        elif workload_type == "streaming":
            # Use reserved or on-demand for reliability
            recommendation = {
                'instance_type': 'r5.2xlarge',
                'instance_count': max(2, int(data_size_gb / 50)),
                'use_spot_instances': False,
                'estimated_cost_savings': '0%',
                'notes': 'On-demand for reliable streaming processing'
            }
        else:
            # Adhoc queries - use serverless
            recommendation = {
                'service': 'AWS Athena / BigQuery / Snowflake',
                'billing': 'pay-per-query',
                'estimated_cost': f'${data_size_gb * 0.005:.2f}',
                'notes': 'Serverless for unpredictable adhoc workloads'
            }

        logger.info(f"Compute recommendation for {workload_type}: {recommendation}")
        return recommendation
```

## Reference Examples

### Example 1: Real-Time E-Commerce Analytics Pipeline

**Purpose**: Process e-commerce events in real-time, enrich with user data, aggregate metrics, and serve to dashboards.

**Architecture**:
- **Ingestion**: Kafka receives clickstream and transaction events
- **Processing**: Flink performs stateful stream processing with windowing
- **Storage**: Write to Iceberg for ad-hoc queries, Redis for real-time metrics
- **Orchestration**: Kubernetes manages Flink jobs
- **Monitoring**: Prometheus + Grafana for observability

**Implementation**:

```python
# Real-time e-commerce pipeline with Flink (PyFlink)
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.functions import MapFunction, KeyedProcessFunction
from pyflink.common.time import Time
from pyflink.common.typeinfo import Types
import json

class EventEnrichment(MapFunction):
    """Enrich events with additional context."""

    def __init__(self, user_cache):
        self.user_cache = user_cache

    def map(self, value):
        event = json.loads(value)
        user_id = event.get('user_id')

        # Enrich with user data from cache/database
        if user_id and user_id in self.user_cache:
            event['user_tier'] = self.user_cache[user_id]['tier']
            event['user_region'] = self.user_cache[user_id]['region']

        return json.dumps(event)

class RevenueAggregator(KeyedProcessFunction):
    """Calculate rolling revenue metrics per user."""

    def process_element(self, value, ctx):
        event = json.loads(value)

        if event.get('event_type') == 'purchase':
            revenue = event.get('amount', 0)

            # Emit aggregated metric
            yield {
                'user_id': event['user_id'],
                'timestamp': ctx.timestamp(),
                'revenue': revenue,
                'window': 'last_hour'
            }

def create_ecommerce_pipeline():
    """Create real-time e-commerce analytics pipeline."""

    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(4)

    # Kafka consumer properties
    kafka_props = {
        'bootstrap.servers': 'kafka:9092',
        'group.id': 'ecommerce-analytics'
    }

    # Create Kafka source
    kafka_consumer = FlinkKafkaConsumer(
        topics='ecommerce-events',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )

    # Read stream
    events = env.add_source(kafka_consumer)

    # Enrich events
    user_cache = {}  # In production, use Redis or other cache
    enriched = events.map(EventEnrichment(user_cache))

    # Calculate revenue per user (tumbling window)
    revenue_metrics = (
        enriched
        .key_by(lambda x: json.loads(x)['user_id'])
        .window(Time.hours(1))
        .process(RevenueAggregator())
    )

    # Write to Kafka for downstream consumption
    kafka_producer = FlinkKafkaProducer(
        topic='revenue-metrics',
        serialization_schema=SimpleStringSchema(),
        producer_config=kafka_props
    )

    revenue_metrics.map(lambda x: json.dumps(x)).add_sink(kafka_producer)

    # Execute
    env.execute("E-Commerce Analytics Pipeline")

if __name__ == "__main__":
    create_ecommerce_pipeline()
```

### Example 2: Data Lakehouse with dbt Transformations

**Purpose**: Build dimensional data warehouse on lakehouse architecture for analytics.

**Complete Pipeline**:

```python
# Complete lakehouse pipeline orchestration
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

def extract_and_load_to_lakehouse():
    """Extract from multiple sources and load to Delta Lake."""
    from storage.delta_lake_manager import DeltaLakeManager
    from batch_ingestion import BatchDataIngester

    ingester = BatchDataIngester(config={})
    delta_manager = DeltaLakeManager(storage_path='s3://data-lakehouse/bronze')

    # Extract from PostgreSQL
    orders_df = ingester.extract_from_database(
        connection_string='postgresql://localhost:5432/ecommerce',
        query='SELECT * FROM orders WHERE created_at >= CURRENT_DATE - INTERVAL \'1 day\'',
        watermark_column='created_at',
        last_watermark=datetime.now() - timedelta(days=1)
    )

    # Write to bronze layer (raw data)
    delta_manager.create_or_update_table(
        df=orders_df,
        table_name='orders',
        partition_columns=['order_date'],
        mode='append'
    )

with DAG(
    'lakehouse_analytics_pipeline',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    extract = PythonOperator(
        task_id='extract_to_bronze',
        python_callable=extract_and_load_to_lakehouse
    )

    # dbt transformation: bronze -> silver -> gold
    dbt_silver = BashOperator(
        task_id='dbt_silver_layer',
        bash_command='dbt run --models silver.* --profiles-dir /opt/dbt'
    )

    dbt_gold = BashOperator(
        task_id='dbt_gold_layer',
        bash_command='dbt run --models gold.* --profiles-dir /opt/dbt'
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='dbt test --profiles-dir /opt/dbt'
    )

    extract >> dbt_silver >> dbt_gold >> dbt_test
```

### Example 3: CDC Pipeline with Debezium and Kafka

**Purpose**: Capture database changes in real-time and replicate to data warehouse.

**Architecture**: MySQL -> Debezium -> Kafka -> Flink -> Snowflake

```python
# CDC processing with Kafka consumer
from streaming_ingestion import StreamingDataIngester
import snowflake.connector

def process_cdc_events(messages):
    """Process CDC events from Debezium."""
    processed = []

    for msg in messages:
        event = msg['value']
        operation = event.get('op')  # 'c'=create, 'u'=update, 'd'=delete

        if operation in ['c', 'u']:
            # Insert or update
            after = event.get('after', {})
            processed.append({
                'key': after.get('id'),
                'value': {
                    'operation': 'upsert',
                    'table': event.get('source', {}).get('table'),
                    'data': after,
                    'timestamp': event.get('ts_ms')
                }
            })
        elif operation == 'd':
            # Delete
            before = event.get('before', {})
            processed.append({
                'key': before.get('id'),
                'value': {
                    'operation': 'delete',
                    'table': event.get('source', {}).get('table'),
                    'id': before.get('id'),
                    'timestamp': event.get('ts_ms')
                }
            })

    return processed

def sync_to_snowflake(processed_events):
    """Sync CDC events to Snowflake."""
    conn = snowflake.connector.connect(
        user='user',
        password='pass',
        account='account',
        warehouse='COMPUTE_WH',
        database='analytics',
        schema='replicated'
    )

    cursor = conn.cursor()

    for event in processed_events:
        if event['value']['operation'] == 'upsert':
            # Merge into Snowflake
            data = event['value']['data']
            table = event['value']['table']

            merge_sql = f"""
                MERGE INTO {table} AS target
                USING (SELECT {', '.join([f"'{v}' AS {k}" for k, v in data.items()])}) AS source
                ON target.id = source.id
                WHEN MATCHED THEN UPDATE SET {', '.join([f"{k} = source.{k}" for k in data.keys()])}
                WHEN NOT MATCHED THEN INSERT ({', '.join(data.keys())})
                VALUES ({', '.join([f"source.{k}" for k in data.keys()])})
            """
            cursor.execute(merge_sql)

        elif event['value']['operation'] == 'delete':
            table = event['value']['table']
            id_val = event['value']['id']
            cursor.execute(f"DELETE FROM {table} WHERE id = {id_val}")

    conn.commit()
    cursor.close()
    conn.close()

# Run CDC pipeline
kafka_config = {
    'bootstrap_servers': 'kafka:9092',
    'consumer_group': 'cdc-replication',
    'transactional_id': 'cdc-txn'
}

ingester = StreamingDataIngester(kafka_config)
ingester.consume_and_process(
    topics=['mysql.ecommerce.orders', 'mysql.ecommerce.customers'],
    process_func=process_cdc_events,
    batch_size=100
)
```

## Output Format

Deliver a comprehensive data pipeline solution with the following components:

### 1. Architecture Documentation
- **Architecture diagram** showing data flow from sources to destinations
- **Technology stack** with justification for each component
- **Scalability analysis** with expected throughput and growth patterns
- **Failure modes** and recovery strategies

### 2. Implementation Code
- **Ingestion layer**: Batch and streaming data ingestion code
- **Transformation layer**: dbt models or Spark jobs for data transformations
- **Orchestration**: Airflow/Prefect DAGs with dependency management
- **Storage**: Delta Lake/Iceberg table management code
- **Data quality**: Great Expectations suites and validation logic

### 3. Configuration Files
- **Orchestration configs**: DAG definitions, schedules, retry policies
- **dbt project**: models, sources, tests, documentation
- **Infrastructure**: Docker Compose, Kubernetes manifests, Terraform for cloud resources
- **Environment configs**: Development, staging, production configurations

### 4. Monitoring and Observability
- **Metrics collection**: Pipeline execution metrics, data quality scores
- **Alerting rules**: Thresholds for failures, performance degradation, data freshness
- **Dashboards**: Grafana/CloudWatch dashboards for pipeline monitoring
- **Logging strategy**: Structured logging with correlation IDs

### 5. Operations Guide
- **Deployment procedures**: How to deploy pipeline updates
- **Troubleshooting guide**: Common issues and resolution steps
- **Scaling guide**: How to scale for increased data volume
- **Cost optimization**: Strategies implemented and potential savings
- **Disaster recovery**: Backup and recovery procedures

### Success Criteria
- [ ] Pipeline processes data within defined SLA (latency requirements met)
- [ ] Data quality checks pass with >99% success rate
- [ ] Pipeline handles failures gracefully with automatic retry and alerting
- [ ] Comprehensive monitoring shows pipeline health and performance
- [ ] Documentation enables other engineers to understand and maintain pipeline
- [ ] Cost optimization strategies reduce infrastructure costs by 30-50%
- [ ] Schema evolution handled without pipeline downtime
- [ ] End-to-end data lineage tracked from source to destination
