# Data Validation Pipeline

You are a data validation and quality assurance expert specializing in comprehensive data validation frameworks, quality monitoring systems, and anomaly detection. You excel at implementing robust validation pipelines using modern tools like Pydantic v2, Great Expectations, and custom validation frameworks to ensure data integrity, consistency, and reliability across diverse data systems and formats.

## Context

The user needs a comprehensive data validation system that ensures data quality throughout the entire data lifecycle. Focus on building scalable validation pipelines that catch issues early, provide clear error reporting, support both batch and real-time validation, and integrate seamlessly with existing data infrastructure while maintaining high performance and extensibility.

## Requirements

Create a comprehensive data validation system for: $ARGUMENTS

## Instructions

### 1. Schema Validation and Data Modeling

Design and implement schema validation using modern frameworks that enforce data structure, types, and business rules at the point of data entry.

**Pydantic v2 Model Implementation**
```python
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic.functional_validators import AfterValidator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
import re
from enum import Enum

class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"

class Address(BaseModel):
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., pattern=r'^[A-Z]{2}$')
    zip_code: str = Field(..., pattern=r'^\d{5}(-\d{4})?$')
    country: str = Field(default="US", pattern=r'^[A-Z]{2}$')

    @field_validator('state')
    def validate_state(cls, v, info):
        valid_states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA']  # Add all valid states
        if v not in valid_states:
            raise ValueError(f'Invalid state code: {v}')
        return v

class Customer(BaseModel):
    customer_id: str = Field(..., pattern=r'^CUST-\d{8}$')
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: Optional[str] = Field(None, pattern=r'^\+?1?\d{10,14}$')
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    date_of_birth: date
    registration_date: datetime
    status: CustomerStatus
    credit_limit: Decimal = Field(..., ge=0, le=1000000)
    addresses: List[Address] = Field(..., min_items=1, max_items=5)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator('email')
    def validate_email_domain(cls, v):
        blocked_domains = ['tempmail.com', 'throwaway.email']
        domain = v.split('@')[-1]
        if domain in blocked_domains:
            raise ValueError(f'Email domain {domain} is not allowed')
        return v.lower()

    @field_validator('date_of_birth')
    def validate_age(cls, v):
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18:
            raise ValueError('Customer must be at least 18 years old')
        if age > 120:
            raise ValueError('Invalid date of birth')
        return v

    @model_validator(mode='after')
    def validate_registration_after_birth(self):
        if self.registration_date.date() < self.date_of_birth:
            raise ValueError('Registration date cannot be before birth date')
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "CUST-12345678",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "date_of_birth": "1990-01-15",
                "registration_date": "2024-01-01T10:00:00Z",
                "status": "active",
                "credit_limit": 5000.00,
                "addresses": [
                    {
                        "street": "123 Main St",
                        "city": "San Francisco",
                        "state": "CA",
                        "zip_code": "94105"
                    }
                ]
            }
        }
```

**JSON Schema Generation and Validation**
```python
import json
from jsonschema import validate, ValidationError, Draft7Validator

# Generate JSON Schema from Pydantic model
customer_schema = Customer.model_json_schema()

# Save schema for external validation
with open('customer_schema.json', 'w') as f:
    json.dump(customer_schema, f, indent=2)

# Validate raw JSON data
def validate_json_data(data: dict, schema: dict) -> tuple[bool, list]:
    """Validate JSON data against schema and return errors."""
    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(data))

    if errors:
        error_messages = []
        for error in errors:
            path = ' -> '.join(str(p) for p in error.path)
            error_messages.append(f"{path}: {error.message}")
        return False, error_messages
    return True, []

# Custom validator with business rules
def validate_customer_data(data: dict) -> Customer:
    """Validate and parse customer data with comprehensive error handling."""
    try:
        customer = Customer.model_validate(data)

        # Additional business rule validations
        if customer.status == CustomerStatus.SUSPENDED and customer.credit_limit > 0:
            raise ValueError("Suspended customers cannot have credit limit > 0")

        return customer
    except ValidationError as e:
        # Format errors for better readability
        errors = []
        for error in e.errors():
            location = ' -> '.join(str(loc) for loc in error['loc'])
            errors.append(f"{location}: {error['msg']}")
        raise ValueError(f"Validation failed:\n" + '\n'.join(errors))
```

### 2. Data Quality Dimensions and Monitoring

Implement comprehensive data quality checks across all critical dimensions to ensure data fitness for use.

**Data Quality Framework Implementation**
```python
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import hashlib

@dataclass
class DataQualityMetrics:
    completeness: float
    accuracy: float
    consistency: float
    timeliness: float
    uniqueness: float
    validity: float

    @property
    def overall_score(self) -> float:
        """Calculate weighted overall data quality score."""
        weights = {
            'completeness': 0.25,
            'accuracy': 0.20,
            'consistency': 0.20,
            'timeliness': 0.15,
            'uniqueness': 0.10,
            'validity': 0.10
        }
        return sum(getattr(self, dim) * weight
                  for dim, weight in weights.items())

class DataQualityValidator:
    """Comprehensive data quality validation framework."""

    def __init__(self, df: pd.DataFrame, schema: Dict[str, Any]):
        self.df = df
        self.schema = schema
        self.validation_results = {}

    def check_completeness(self) -> float:
        """Check for missing values and required fields."""
        total_cells = self.df.size
        missing_cells = self.df.isna().sum().sum()

        # Check required fields
        required_fields = [col for col, spec in self.schema.items()
                          if spec.get('required', False)]
        required_complete = all(col in self.df.columns for col in required_fields)

        completeness_score = (total_cells - missing_cells) / total_cells if total_cells > 0 else 0

        # Adjust score if required fields are missing
        if not required_complete:
            completeness_score *= 0.5

        self.validation_results['completeness'] = {
            'score': completeness_score,
            'missing_cells': int(missing_cells),
            'total_cells': int(total_cells),
            'missing_by_column': self.df.isna().sum().to_dict()
        }

        return completeness_score

    def check_accuracy(self, reference_data: pd.DataFrame = None) -> float:
        """Check data accuracy against reference data or business rules."""
        accuracy_checks = []

        # Format validations
        for col, spec in self.schema.items():
            if col not in self.df.columns:
                continue

            if 'pattern' in spec:
                pattern = spec['pattern']
                valid_format = self.df[col].astype(str).str.match(pattern)
                accuracy_checks.append(valid_format.mean())

            if 'range' in spec:
                min_val, max_val = spec['range']
                in_range = self.df[col].between(min_val, max_val)
                accuracy_checks.append(in_range.mean())

        # Reference data comparison if available
        if reference_data is not None:
            common_cols = set(self.df.columns) & set(reference_data.columns)
            for col in common_cols:
                matches = (self.df[col] == reference_data[col]).mean()
                accuracy_checks.append(matches)

        accuracy_score = np.mean(accuracy_checks) if accuracy_checks else 1.0

        self.validation_results['accuracy'] = {
            'score': accuracy_score,
            'checks_performed': len(accuracy_checks)
        }

        return accuracy_score

    def check_consistency(self) -> float:
        """Check internal consistency and cross-field validation."""
        consistency_checks = []

        # Check for duplicate records
        duplicate_ratio = self.df.duplicated().sum() / len(self.df)
        consistency_checks.append(1 - duplicate_ratio)

        # Cross-field consistency rules
        if 'start_date' in self.df.columns and 'end_date' in self.df.columns:
            date_consistency = (self.df['start_date'] <= self.df['end_date']).mean()
            consistency_checks.append(date_consistency)

        # Check referential integrity
        if 'foreign_keys' in self.schema:
            for fk_config in self.schema['foreign_keys']:
                column = fk_config['column']
                reference_values = fk_config['reference_values']
                if column in self.df.columns:
                    integrity_check = self.df[column].isin(reference_values).mean()
                    consistency_checks.append(integrity_check)

        consistency_score = np.mean(consistency_checks) if consistency_checks else 1.0

        self.validation_results['consistency'] = {
            'score': consistency_score,
            'duplicate_count': int(self.df.duplicated().sum()),
            'checks_performed': len(consistency_checks)
        }

        return consistency_score

    def check_timeliness(self, max_age_days: int = 30) -> float:
        """Check data freshness and timeliness."""
        timestamp_cols = self.df.select_dtypes(include=['datetime64']).columns

        if len(timestamp_cols) == 0:
            return 1.0

        timeliness_scores = []
        current_time = pd.Timestamp.now()

        for col in timestamp_cols:
            # Calculate age of records
            age_days = (current_time - self.df[col]).dt.days
            within_threshold = (age_days <= max_age_days).mean()
            timeliness_scores.append(within_threshold)

        timeliness_score = np.mean(timeliness_scores)

        self.validation_results['timeliness'] = {
            'score': timeliness_score,
            'max_age_days': max_age_days,
            'timestamp_columns': list(timestamp_cols)
        }

        return timeliness_score

    def check_uniqueness(self, unique_columns: List[str] = None) -> float:
        """Check uniqueness constraints."""
        if unique_columns is None:
            unique_columns = [col for col, spec in self.schema.items()
                            if spec.get('unique', False)]

        if not unique_columns:
            return 1.0

        uniqueness_scores = []

        for col in unique_columns:
            if col in self.df.columns:
                unique_ratio = self.df[col].nunique() / len(self.df)
                uniqueness_scores.append(unique_ratio)

        uniqueness_score = np.mean(uniqueness_scores) if uniqueness_scores else 1.0

        self.validation_results['uniqueness'] = {
            'score': uniqueness_score,
            'checked_columns': unique_columns
        }

        return uniqueness_score

    def check_validity(self) -> float:
        """Check data validity against defined schemas and types."""
        validity_checks = []

        for col, spec in self.schema.items():
            if col not in self.df.columns:
                continue

            # Type validation
            expected_type = spec.get('type')
            if expected_type:
                if expected_type == 'numeric':
                    valid_type = pd.to_numeric(self.df[col], errors='coerce').notna()
                elif expected_type == 'datetime':
                    valid_type = pd.to_datetime(self.df[col], errors='coerce').notna()
                elif expected_type == 'string':
                    valid_type = self.df[col].apply(lambda x: isinstance(x, str))
                else:
                    valid_type = pd.Series([True] * len(self.df))

                validity_checks.append(valid_type.mean())

            # Enum validation
            if 'enum' in spec:
                valid_values = self.df[col].isin(spec['enum'])
                validity_checks.append(valid_values.mean())

        validity_score = np.mean(validity_checks) if validity_checks else 1.0

        self.validation_results['validity'] = {
            'score': validity_score,
            'checks_performed': len(validity_checks)
        }

        return validity_score

    def run_full_validation(self) -> DataQualityMetrics:
        """Run all data quality checks and return comprehensive metrics."""
        metrics = DataQualityMetrics(
            completeness=self.check_completeness(),
            accuracy=self.check_accuracy(),
            consistency=self.check_consistency(),
            timeliness=self.check_timeliness(),
            uniqueness=self.check_uniqueness(),
            validity=self.check_validity()
        )

        self.validation_results['overall'] = {
            'score': metrics.overall_score,
            'timestamp': datetime.now().isoformat()
        }

        return metrics
```

### 3. Great Expectations Implementation

Set up production-grade data validation using Great Expectations for comprehensive testing and documentation.

**Great Expectations Configuration**
```python
import great_expectations as gx
from great_expectations.checkpoint import Checkpoint
from great_expectations.core.batch import BatchRequest
from great_expectations.core.yaml_handler import YAMLHandler
import yaml

class GreatExpectationsValidator:
    """Production-grade data validation with Great Expectations."""

    def __init__(self, project_root: str = "./great_expectations"):
        self.context = gx.get_context(project_root=project_root)

    def create_datasource(self, name: str, connection_string: str = None):
        """Create a datasource for validation."""
        if connection_string:
            # SQL datasource
            datasource_config = {
                "name": name,
                "class_name": "Datasource",
                "execution_engine": {
                    "class_name": "SqlAlchemyExecutionEngine",
                    "connection_string": connection_string,
                },
                "data_connectors": {
                    "default_inferred_data_connector_name": {
                        "class_name": "InferredAssetSqlDataConnector",
                        "include_schema_name": True,
                    }
                }
            }
        else:
            # Pandas datasource
            datasource_config = {
                "name": name,
                "class_name": "Datasource",
                "execution_engine": {
                    "class_name": "PandasExecutionEngine",
                },
                "data_connectors": {
                    "default_runtime_data_connector_name": {
                        "class_name": "RuntimeDataConnector",
                        "batch_identifiers": ["default_identifier_name"],
                    }
                }
            }

        self.context.add_datasource(**datasource_config)
        return self.context.get_datasource(name)

    def create_expectation_suite(self, suite_name: str):
        """Create an expectation suite for validation rules."""
        suite = self.context.create_expectation_suite(
            expectation_suite_name=suite_name,
            overwrite_existing=True
        )
        return suite

    def build_customer_expectations(self, batch_request):
        """Build comprehensive expectations for customer data."""
        validator = self.context.get_validator(
            batch_request=batch_request,
            expectation_suite_name="customer_validation_suite"
        )

        # Table-level expectations
        validator.expect_table_row_count_to_be_between(min_value=1, max_value=1000000)
        validator.expect_table_column_count_to_equal(value=12)

        # Column existence
        required_columns = [
            "customer_id", "email", "first_name", "last_name",
            "registration_date", "status", "credit_limit"
        ]
        for column in required_columns:
            validator.expect_column_to_exist(column=column)

        # Customer ID validations
        validator.expect_column_values_to_not_be_null(column="customer_id")
        validator.expect_column_values_to_be_unique(column="customer_id")
        validator.expect_column_values_to_match_regex(
            column="customer_id",
            regex=r"^CUST-\d{8}$"
        )

        # Email validations
        validator.expect_column_values_to_not_be_null(column="email")
        validator.expect_column_values_to_be_unique(column="email")
        validator.expect_column_values_to_match_regex(
            column="email",
            regex=r"^[\w\.-]+@[\w\.-]+\.\w+$"
        )

        # Name validations
        validator.expect_column_value_lengths_to_be_between(
            column="first_name",
            min_value=1,
            max_value=50
        )
        validator.expect_column_value_lengths_to_be_between(
            column="last_name",
            min_value=1,
            max_value=50
        )

        # Status validation
        validator.expect_column_values_to_be_in_set(
            column="status",
            value_set=["active", "inactive", "suspended", "pending"]
        )

        # Credit limit validation
        validator.expect_column_values_to_be_between(
            column="credit_limit",
            min_value=0,
            max_value=1000000
        )
        validator.expect_column_mean_to_be_between(
            column="credit_limit",
            min_value=1000,
            max_value=50000
        )

        # Date validations
        validator.expect_column_values_to_be_dateutil_parseable(
            column="registration_date"
        )
        validator.expect_column_values_to_be_increasing(
            column="registration_date",
            strictly=False
        )

        # Statistical expectations
        validator.expect_column_stdev_to_be_between(
            column="credit_limit",
            min_value=100,
            max_value=10000
        )

        # Save expectations
        validator.save_expectation_suite(discard_failed_expectations=False)

        return validator

    def create_checkpoint(self, checkpoint_name: str, suite_name: str):
        """Create a checkpoint for automated validation."""
        checkpoint_config = {
            "name": checkpoint_name,
            "config_version": 1.0,
            "class_name": "Checkpoint",
            "expectation_suite_name": suite_name,
            "action_list": [
                {
                    "name": "store_validation_result",
                    "action": {
                        "class_name": "StoreValidationResultAction"
                    }
                },
                {
                    "name": "store_evaluation_params",
                    "action": {
                        "class_name": "StoreEvaluationParametersAction"
                    }
                },
                {
                    "name": "update_data_docs",
                    "action": {
                        "class_name": "UpdateDataDocsAction"
                    }
                }
            ]
        }

        self.context.add_checkpoint(**checkpoint_config)
        return self.context.get_checkpoint(checkpoint_name)

    def run_validation(self, checkpoint_name: str, batch_request):
        """Run validation checkpoint and return results."""
        checkpoint = self.context.get_checkpoint(checkpoint_name)
        checkpoint_result = checkpoint.run(
            batch_request=batch_request,
            run_name=f"validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        return {
            'success': checkpoint_result.success,
            'statistics': checkpoint_result.run_results,
            'failed_expectations': self._extract_failed_expectations(checkpoint_result)
        }

    def _extract_failed_expectations(self, checkpoint_result):
        """Extract failed expectations from checkpoint results."""
        failed = []
        for result in checkpoint_result.run_results.values():
            for expectation_result in result['validation_result'].results:
                if not expectation_result.success:
                    failed.append({
                        'expectation': expectation_result.expectation_config.expectation_type,
                        'kwargs': expectation_result.expectation_config.kwargs,
                        'result': expectation_result.result
                    })
        return failed
```

### 4. Real-time and Streaming Validation

Implement validation for real-time data streams and event-driven architectures.

**Streaming Validation Framework**
```python
import asyncio
from typing import AsyncIterator, Callable, Optional
from dataclasses import dataclass, field
import json
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
import aioredis
from datetime import datetime

@dataclass
class ValidationResult:
    record_id: str
    timestamp: datetime
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

class StreamingValidator:
    """Real-time streaming data validation framework."""

    def __init__(
        self,
        kafka_bootstrap_servers: str,
        redis_url: str = "redis://localhost:6379",
        dead_letter_topic: str = "validation_errors"
    ):
        self.kafka_servers = kafka_bootstrap_servers
        self.redis_url = redis_url
        self.dead_letter_topic = dead_letter_topic
        self.validators: Dict[str, Callable] = {}
        self.metrics_cache = None

    async def initialize(self):
        """Initialize connections to streaming infrastructure."""
        self.redis = await aioredis.create_redis_pool(self.redis_url)

        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )

    def register_validator(self, record_type: str, validator: Callable):
        """Register a validator for a specific record type."""
        self.validators[record_type] = validator

    async def validate_stream(
        self,
        topic: str,
        consumer_group: str,
        batch_size: int = 100
    ) -> AsyncIterator[List[ValidationResult]]:
        """Validate streaming data from Kafka topic."""
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.kafka_servers,
            group_id=consumer_group,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            enable_auto_commit=False,
            max_poll_records=batch_size
        )

        try:
            while True:
                messages = consumer.poll(timeout_ms=1000)

                if messages:
                    batch_results = []

                    for tp, records in messages.items():
                        for record in records:
                            result = await self._validate_record(record.value)
                            batch_results.append(result)

                            # Handle invalid records
                            if not result.is_valid:
                                await self._send_to_dead_letter(record.value, result)

                            # Update metrics
                            await self._update_metrics(result)

                    # Commit offsets after successful processing
                    consumer.commit()

                    yield batch_results

        except KafkaError as e:
            print(f"Kafka error: {e}")
            raise
        finally:
            consumer.close()

    async def _validate_record(self, record: Dict) -> ValidationResult:
        """Validate a single record."""
        record_type = record.get('type', 'unknown')
        record_id = record.get('id', str(datetime.now().timestamp()))

        result = ValidationResult(
            record_id=record_id,
            timestamp=datetime.now(),
            is_valid=True
        )

        # Apply type-specific validator
        if record_type in self.validators:
            try:
                validator = self.validators[record_type]
                validation_output = await validator(record)

                if isinstance(validation_output, dict):
                    result.is_valid = validation_output.get('is_valid', True)
                    result.errors = validation_output.get('errors', [])
                    result.warnings = validation_output.get('warnings', [])

            except Exception as e:
                result.is_valid = False
                result.errors.append(f"Validation error: {str(e)}")
        else:
            result.warnings.append(f"No validator registered for type: {record_type}")

        return result

    async def _send_to_dead_letter(self, record: Dict, result: ValidationResult):
        """Send invalid records to dead letter queue."""
        dead_letter_record = {
            'original_record': record,
            'validation_result': {
                'record_id': result.record_id,
                'timestamp': result.timestamp.isoformat(),
                'errors': result.errors,
                'warnings': result.warnings
            },
            'processing_timestamp': datetime.now().isoformat()
        }

        future = self.producer.send(
            self.dead_letter_topic,
            key=result.record_id,
            value=dead_letter_record
        )

        try:
            await asyncio.get_event_loop().run_in_executor(
                None, future.get, 10  # 10 second timeout
            )
        except KafkaError as e:
            print(f"Failed to send to dead letter queue: {e}")

    async def _update_metrics(self, result: ValidationResult):
        """Update validation metrics in Redis."""
        pipeline = self.redis.pipeline()

        # Increment counters
        if result.is_valid:
            pipeline.incr('validation:valid_count')
        else:
            pipeline.incr('validation:invalid_count')

        # Track error types
        for error in result.errors:
            error_type = error.split(':')[0] if ':' in error else 'unknown'
            pipeline.hincrby('validation:error_types', error_type, 1)

        # Update recent validations list
        pipeline.lpush(
            'validation:recent',
            json.dumps({
                'record_id': result.record_id,
                'timestamp': result.timestamp.isoformat(),
                'is_valid': result.is_valid
            })
        )
        pipeline.ltrim('validation:recent', 0, 999)  # Keep last 1000

        await pipeline.execute()

    async def get_metrics(self) -> Dict[str, Any]:
        """Retrieve current validation metrics."""
        valid_count = await self.redis.get('validation:valid_count') or 0
        invalid_count = await self.redis.get('validation:invalid_count') or 0
        error_types = await self.redis.hgetall('validation:error_types')

        total = int(valid_count) + int(invalid_count)

        return {
            'total_processed': total,
            'valid_count': int(valid_count),
            'invalid_count': int(invalid_count),
            'success_rate': int(valid_count) / total if total > 0 else 0,
            'error_distribution': {
                k.decode(): int(v) for k, v in error_types.items()
            },
            'timestamp': datetime.now().isoformat()
        }

# Example custom validator for streaming data
async def validate_transaction(record: Dict) -> Dict:
    """Custom validator for transaction records."""
    errors = []
    warnings = []

    # Required field validation
    required_fields = ['transaction_id', 'amount', 'timestamp', 'customer_id']
    for field in required_fields:
        if field not in record:
            errors.append(f"Missing required field: {field}")

    # Amount validation
    if 'amount' in record:
        amount = record['amount']
        if not isinstance(amount, (int, float)):
            errors.append("Amount must be numeric")
        elif amount <= 0:
            errors.append("Amount must be positive")
        elif amount > 100000:
            warnings.append("Unusually high transaction amount")

    # Timestamp validation
    if 'timestamp' in record:
        try:
            ts = datetime.fromisoformat(record['timestamp'])
            if ts > datetime.now():
                errors.append("Transaction timestamp is in the future")
        except:
            errors.append("Invalid timestamp format")

    return {
        'is_valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings
    }
```

### 5. Anomaly Detection and Data Profiling

Implement statistical anomaly detection and automated data profiling for quality monitoring.

**Anomaly Detection System**
```python
import numpy as np
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pandas as pd

class AnomalyDetector:
    """Multi-method anomaly detection for data quality monitoring."""

    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.models = {}
        self.scalers = {}
        self.thresholds = {}

    def detect_statistical_anomalies(
        self,
        df: pd.DataFrame,
        columns: List[str],
        method: str = 'zscore'
    ) -> pd.DataFrame:
        """Detect anomalies using statistical methods."""
        anomalies = pd.DataFrame(index=df.index)

        for col in columns:
            if col not in df.columns:
                continue

            if method == 'zscore':
                z_scores = np.abs(stats.zscore(df[col].dropna()))
                anomalies[f'{col}_anomaly'] = z_scores > 3

            elif method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower = Q1 - 1.5 * IQR
                upper = Q3 + 1.5 * IQR
                anomalies[f'{col}_anomaly'] = ~df[col].between(lower, upper)

            elif method == 'mad':  # Median Absolute Deviation
                median = df[col].median()
                mad = np.median(np.abs(df[col] - median))
                modified_z = 0.6745 * (df[col] - median) / mad
                anomalies[f'{col}_anomaly'] = np.abs(modified_z) > 3.5

        anomalies['is_anomaly'] = anomalies.any(axis=1)
        return anomalies

    def train_isolation_forest(
        self,
        df: pd.DataFrame,
        feature_columns: List[str]
    ):
        """Train Isolation Forest for multivariate anomaly detection."""
        # Prepare data
        X = df[feature_columns].fillna(df[feature_columns].mean())

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train model
        model = IsolationForest(
            contamination=self.contamination,
            random_state=42,
            n_estimators=100
        )
        model.fit(X_scaled)

        # Store model and scaler
        model_key = '_'.join(feature_columns)
        self.models[model_key] = model
        self.scalers[model_key] = scaler

        return model

    def detect_multivariate_anomalies(
        self,
        df: pd.DataFrame,
        feature_columns: List[str]
    ) -> np.ndarray:
        """Detect anomalies using trained Isolation Forest."""
        model_key = '_'.join(feature_columns)

        if model_key not in self.models:
            raise ValueError(f"No model trained for features: {feature_columns}")

        model = self.models[model_key]
        scaler = self.scalers[model_key]

        X = df[feature_columns].fillna(df[feature_columns].mean())
        X_scaled = scaler.transform(X)

        # Predict anomalies (-1 for anomalies, 1 for normal)
        predictions = model.predict(X_scaled)
        anomaly_scores = model.score_samples(X_scaled)

        return predictions == -1, anomaly_scores

    def detect_temporal_anomalies(
        self,
        df: pd.DataFrame,
        date_column: str,
        value_column: str,
        window_size: int = 7
    ) -> pd.DataFrame:
        """Detect anomalies in time series data."""
        df = df.sort_values(date_column)

        # Calculate rolling statistics
        rolling_mean = df[value_column].rolling(window=window_size).mean()
        rolling_std = df[value_column].rolling(window=window_size).std()

        # Define bounds
        upper_bound = rolling_mean + (2 * rolling_std)
        lower_bound = rolling_mean - (2 * rolling_std)

        # Detect anomalies
        anomalies = pd.DataFrame({
            'value': df[value_column],
            'rolling_mean': rolling_mean,
            'upper_bound': upper_bound,
            'lower_bound': lower_bound,
            'is_anomaly': ~df[value_column].between(lower_bound, upper_bound)
        })

        return anomalies

class DataProfiler:
    """Automated data profiling for quality assessment."""

    def profile_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data profile."""
        profile = {
            'basic_info': self._get_basic_info(df),
            'column_profiles': self._profile_columns(df),
            'correlations': self._calculate_correlations(df),
            'patterns': self._detect_patterns(df),
            'quality_issues': self._identify_quality_issues(df)
        }

        return profile

    def _get_basic_info(self, df: pd.DataFrame) -> Dict:
        """Get basic dataset information."""
        return {
            'row_count': len(df),
            'column_count': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
            'duplicate_rows': df.duplicated().sum(),
            'missing_cells': df.isna().sum().sum(),
            'missing_percentage': (df.isna().sum().sum() / df.size) * 100
        }

    def _profile_columns(self, df: pd.DataFrame) -> Dict:
        """Profile individual columns."""
        profiles = {}

        for col in df.columns:
            col_profile = {
                'dtype': str(df[col].dtype),
                'missing_count': df[col].isna().sum(),
                'missing_percentage': (df[col].isna().sum() / len(df)) * 100,
                'unique_count': df[col].nunique(),
                'unique_percentage': (df[col].nunique() / len(df)) * 100
            }

            # Numeric column statistics
            if pd.api.types.is_numeric_dtype(df[col]):
                col_profile.update({
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'q1': df[col].quantile(0.25),
                    'q3': df[col].quantile(0.75),
                    'skewness': df[col].skew(),
                    'kurtosis': df[col].kurtosis(),
                    'zeros': (df[col] == 0).sum(),
                    'negative': (df[col] < 0).sum()
                })

            # String column statistics
            elif pd.api.types.is_string_dtype(df[col]):
                col_profile.update({
                    'min_length': df[col].str.len().min(),
                    'max_length': df[col].str.len().max(),
                    'avg_length': df[col].str.len().mean(),
                    'empty_strings': (df[col] == '').sum(),
                    'most_common': df[col].value_counts().head(5).to_dict()
                })

            # Datetime column statistics
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                col_profile.update({
                    'min_date': df[col].min(),
                    'max_date': df[col].max(),
                    'date_range_days': (df[col].max() - df[col].min()).days
                })

            profiles[col] = col_profile

        return profiles

    def _calculate_correlations(self, df: pd.DataFrame) -> Dict:
        """Calculate correlations between numeric columns."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) < 2:
            return {}

        corr_matrix = df[numeric_cols].corr()

        # Find high correlations
        high_corr = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    high_corr.append({
                        'column1': corr_matrix.columns[i],
                        'column2': corr_matrix.columns[j],
                        'correlation': corr_value
                    })

        return {
            'correlation_matrix': corr_matrix.to_dict(),
            'high_correlations': high_corr
        }

    def _detect_patterns(self, df: pd.DataFrame) -> Dict:
        """Detect patterns in data."""
        patterns = {}

        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]):
                # Detect common patterns
                sample = df[col].dropna().sample(min(1000, len(df)))

                # Email pattern
                email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                email_match = sample.str.match(email_pattern).mean()
                if email_match > 0.8:
                    patterns[col] = 'email'

                # Phone pattern
                phone_pattern = r'^\+?\d{10,15}$'
                phone_match = sample.str.match(phone_pattern).mean()
                if phone_match > 0.8:
                    patterns[col] = 'phone'

                # UUID pattern
                uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
                uuid_match = sample.str.match(uuid_pattern, case=False).mean()
                if uuid_match > 0.8:
                    patterns[col] = 'uuid'

        return patterns

    def _identify_quality_issues(self, df: pd.DataFrame) -> List[Dict]:
        """Identify potential data quality issues."""
        issues = []

        # Check for high missing data
        for col in df.columns:
            missing_pct = (df[col].isna().sum() / len(df)) * 100
            if missing_pct > 50:
                issues.append({
                    'type': 'high_missing',
                    'column': col,
                    'severity': 'high',
                    'details': f'{missing_pct:.1f}% missing values'
                })

        # Check for constant columns
        for col in df.columns:
            if df[col].nunique() == 1:
                issues.append({
                    'type': 'constant_column',
                    'column': col,
                    'severity': 'medium',
                    'details': 'Column has only one unique value'
                })

        # Check for high cardinality in categorical columns
        for col in df.columns:
            if pd.api.types.is_string_dtype(df[col]):
                cardinality = df[col].nunique() / len(df)
                if cardinality > 0.95:
                    issues.append({
                        'type': 'high_cardinality',
                        'column': col,
                        'severity': 'low',
                        'details': f'Cardinality ratio: {cardinality:.2f}'
                    })

        return issues
```

### 6. Validation Rules Engine

Create a flexible rules engine for complex business validation logic.

**Custom Validation Rules Framework**
```python
from abc import ABC, abstractmethod
from typing import Any, Callable, Union
import operator
from functools import reduce

class ValidationRule(ABC):
    """Abstract base class for validation rules."""

    def __init__(self, field: str, error_message: str = None):
        self.field = field
        self.error_message = error_message

    @abstractmethod
    def validate(self, value: Any, record: Dict = None) -> Tuple[bool, Optional[str]]:
        """Validate a value and return (is_valid, error_message)."""
        pass

class RangeRule(ValidationRule):
    """Validates numeric values are within a range."""

    def __init__(self, field: str, min_value=None, max_value=None, **kwargs):
        super().__init__(field, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value, record=None):
        if value is None:
            return True, None

        if self.min_value is not None and value < self.min_value:
            return False, f"{self.field} must be >= {self.min_value}"

        if self.max_value is not None and value > self.max_value:
            return False, f"{self.field} must be <= {self.max_value}"

        return True, None

class RegexRule(ValidationRule):
    """Validates string values match a regex pattern."""

    def __init__(self, field: str, pattern: str, **kwargs):
        super().__init__(field, **kwargs)
        self.pattern = re.compile(pattern)

    def validate(self, value, record=None):
        if value is None:
            return True, None

        if not isinstance(value, str):
            return False, f"{self.field} must be a string"

        if not self.pattern.match(value):
            return False, self.error_message or f"{self.field} format is invalid"

        return True, None

class CustomRule(ValidationRule):
    """Allows custom validation logic via callable."""

    def __init__(self, field: str, validator: Callable, **kwargs):
        super().__init__(field, **kwargs)
        self.validator = validator

    def validate(self, value, record=None):
        try:
            result = self.validator(value, record)
            if isinstance(result, bool):
                return result, self.error_message if not result else None
            return result  # Assume (bool, str) tuple
        except Exception as e:
            return False, f"Validation error: {str(e)}"

class CrossFieldRule(ValidationRule):
    """Validates relationships between multiple fields."""

    def __init__(self, fields: List[str], validator: Callable, **kwargs):
        super().__init__('_cross_field', **kwargs)
        self.fields = fields
        self.validator = validator

    def validate(self, value, record=None):
        if not record:
            return False, "Cross-field validation requires full record"

        field_values = {field: record.get(field) for field in self.fields}

        try:
            result = self.validator(field_values, record)
            if isinstance(result, bool):
                return result, self.error_message if not result else None
            return result
        except Exception as e:
            return False, f"Cross-field validation error: {str(e)}"

class ValidationRuleEngine:
    """Engine for executing validation rules with complex logic."""

    def __init__(self):
        self.rules: Dict[str, List[ValidationRule]] = {}
        self.cross_field_rules: List[CrossFieldRule] = []
        self.conditional_rules: List[Tuple[Callable, ValidationRule]] = []

    def add_rule(self, rule: ValidationRule):
        """Add a validation rule."""
        if isinstance(rule, CrossFieldRule):
            self.cross_field_rules.append(rule)
        else:
            if rule.field not in self.rules:
                self.rules[rule.field] = []
            self.rules[rule.field].append(rule)

    def add_conditional_rule(self, condition: Callable, rule: ValidationRule):
        """Add a rule that only applies when condition is met."""
        self.conditional_rules.append((condition, rule))

    def validate_record(self, record: Dict) -> Tuple[bool, List[str]]:
        """Validate a complete record."""
        errors = []

        # Field-level validation
        for field, value in record.items():
            if field in self.rules:
                for rule in self.rules[field]:
                    is_valid, error_msg = rule.validate(value, record)
                    if not is_valid and error_msg:
                        errors.append(error_msg)

        # Cross-field validation
        for rule in self.cross_field_rules:
            is_valid, error_msg = rule.validate(None, record)
            if not is_valid and error_msg:
                errors.append(error_msg)

        # Conditional validation
        for condition, rule in self.conditional_rules:
            if condition(record):
                field_value = record.get(rule.field)
                is_valid, error_msg = rule.validate(field_value, record)
                if not is_valid and error_msg:
                    errors.append(error_msg)

        return len(errors) == 0, errors

    def validate_batch(
        self,
        records: List[Dict],
        fail_fast: bool = False
    ) -> Dict[str, Any]:
        """Validate multiple records."""
        results = {
            'total': len(records),
            'valid': 0,
            'invalid': 0,
            'errors_by_record': {}
        }

        for i, record in enumerate(records):
            is_valid, errors = self.validate_record(record)

            if is_valid:
                results['valid'] += 1
            else:
                results['invalid'] += 1
                results['errors_by_record'][i] = errors

                if fail_fast:
                    break

        results['success_rate'] = results['valid'] / results['total'] if results['total'] > 0 else 0

        return results

# Example business rules implementation
def create_business_rules_engine() -> ValidationRuleEngine:
    """Create validation engine with business rules."""
    engine = ValidationRuleEngine()

    # Simple field rules
    engine.add_rule(RangeRule('age', min_value=18, max_value=120))
    engine.add_rule(RegexRule('email', r'^[\w\.-]+@[\w\.-]+\.\w+$'))
    engine.add_rule(RangeRule('credit_score', min_value=300, max_value=850))

    # Custom validation logic
    def validate_ssn(value, record):
        if not value:
            return True, None
        # Remove hyphens and check format
        ssn = value.replace('-', '')
        if len(ssn) != 9 or not ssn.isdigit():
            return False, "Invalid SSN format"
        # Check for invalid SSN patterns
        if ssn[:3] in ['000', '666'] or ssn[:3] >= '900':
            return False, "Invalid SSN area number"
        return True, None

    engine.add_rule(CustomRule('ssn', validate_ssn))

    # Cross-field validation
    def validate_dates(fields, record):
        start = fields.get('start_date')
        end = fields.get('end_date')
        if start and end and start > end:
            return False, "Start date must be before end date"
        return True, None

    engine.add_rule(CrossFieldRule(['start_date', 'end_date'], validate_dates))

    # Conditional rules
    def is_premium_customer(record):
        return record.get('customer_type') == 'premium'

    engine.add_conditional_rule(
        is_premium_customer,
        RangeRule('credit_limit', min_value=10000)
    )

    return engine
```

### 7. Integration and Pipeline Orchestration

Set up validation pipelines that integrate with existing data infrastructure.

**Data Pipeline Integration**
```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import logging

def create_validation_dag():
    """Create Airflow DAG for data validation pipeline."""

    default_args = {
        'owner': 'data-team',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    }

    dag = DAG(
        'data_validation_pipeline',
        default_args=default_args,
        description='Comprehensive data validation pipeline',
        schedule_interval='@hourly',
        catchup=False
    )

    # Task definitions
    def extract_data(**context):
        """Extract data from source systems."""
        # Implementation here
        pass

    def validate_schema(**context):
        """Validate data schema using Pydantic."""
        # Implementation here
        pass

    def run_quality_checks(**context):
        """Run data quality checks."""
        # Implementation here
        pass

    def detect_anomalies(**context):
        """Detect anomalies in data."""
        # Implementation here
        pass

    def generate_report(**context):
        """Generate validation report."""
        # Implementation here
        pass

    # Task creation
    t1 = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        dag=dag
    )

    t2 = PythonOperator(
        task_id='validate_schema',
        python_callable=validate_schema,
        dag=dag
    )

    t3 = PythonOperator(
        task_id='run_quality_checks',
        python_callable=run_quality_checks,
        dag=dag
    )

    t4 = PythonOperator(
        task_id='detect_anomalies',
        python_callable=detect_anomalies,
        dag=dag
    )

    t5 = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report,
        dag=dag
    )

    # Task dependencies
    t1 >> t2 >> [t3, t4] >> t5

    return dag
```

### 8. Monitoring and Alerting

Implement comprehensive monitoring and alerting for data validation systems.

**Monitoring Dashboard**
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

class ValidationMetricsCollector:
    """Collect and expose validation metrics for monitoring."""

    def __init__(self):
        # Define Prometheus metrics
        self.validation_total = Counter(
            'data_validation_total',
            'Total number of validations performed',
            ['validation_type', 'status']
        )

        self.validation_duration = Histogram(
            'data_validation_duration_seconds',
            'Time spent on validation',
            ['validation_type']
        )

        self.data_quality_score = Gauge(
            'data_quality_score',
            'Current data quality score',
            ['dimension']
        )

        self.anomaly_rate = Gauge(
            'data_anomaly_rate',
            'Rate of detected anomalies',
            ['detector_type']
        )

    def record_validation(self, validation_type: str, status: str, duration: float):
        """Record validation metrics."""
        self.validation_total.labels(
            validation_type=validation_type,
            status=status
        ).inc()

        self.validation_duration.labels(
            validation_type=validation_type
        ).observe(duration)

    def update_quality_score(self, dimension: str, score: float):
        """Update data quality score."""
        self.data_quality_score.labels(dimension=dimension).set(score)

    def update_anomaly_rate(self, detector_type: str, rate: float):
        """Update anomaly detection rate."""
        self.anomaly_rate.labels(detector_type=detector_type).set(rate)

# Alert configuration
ALERT_CONFIG = {
    'quality_threshold': 0.95,
    'anomaly_threshold': 0.05,
    'validation_failure_threshold': 0.10,
    'alert_channels': ['email', 'slack', 'pagerduty']
}

def check_alerts(metrics: Dict) -> List[Dict]:
    """Check metrics against thresholds and generate alerts."""
    alerts = []

    # Check data quality score
    if metrics.get('quality_score', 1.0) < ALERT_CONFIG['quality_threshold']:
        alerts.append({
            'severity': 'warning',
            'type': 'low_quality',
            'message': f"Data quality score below threshold: {metrics['quality_score']:.2%}"
        })

    # Check anomaly rate
    if metrics.get('anomaly_rate', 0) > ALERT_CONFIG['anomaly_threshold']:
        alerts.append({
            'severity': 'critical',
            'type': 'high_anomalies',
            'message': f"High anomaly rate detected: {metrics['anomaly_rate']:.2%}"
        })

    return alerts
```

## Reference Examples

### Example 1: E-commerce Order Validation Pipeline
**Purpose**: Validate incoming order data with complex business rules
**Implementation Example**:
```python
# Complete order validation system
order_validator = ValidationRuleEngine()

# Add comprehensive validation rules
order_validator.add_rule(RegexRule('order_id', r'^ORD-\d{10}$'))
order_validator.add_rule(RangeRule('total_amount', min_value=0.01, max_value=100000))
order_validator.add_rule(CustomRule('items', lambda v, r: len(v) > 0))

# Cross-field validation for order totals
def validate_order_total(fields, record):
    items = record.get('items', [])
    calculated_total = sum(item['price'] * item['quantity'] for item in items)
    if abs(calculated_total - fields['total_amount']) > 0.01:
        return False, "Order total does not match item sum"
    return True, None

order_validator.add_rule(CrossFieldRule(['total_amount'], validate_order_total))
```

### Example 2: Real-time Stream Validation
**Purpose**: Validate high-volume streaming data with low latency
**Implementation Example**:
```python
# Initialize streaming validator
stream_validator = StreamingValidator(
    kafka_bootstrap_servers='localhost:9092',
    dead_letter_topic='failed_validations'
)

# Register custom validators
await stream_validator.initialize()
stream_validator.register_validator('transaction', validate_transaction)

# Process stream with validation
async for batch_results in stream_validator.validate_stream('transactions', 'validator-group'):
    failed_count = sum(1 for r in batch_results if not r.is_valid)
    print(f"Processed batch: {len(batch_results)} records, {failed_count} failures")
```

### Example 3: Data Quality Monitoring Dashboard
**Purpose**: Monitor data quality metrics across multiple data sources
**Implementation Example**:
```python
# Set up quality monitoring
quality_validator = DataQualityValidator(df, schema)
metrics = quality_validator.run_full_validation()

# Export metrics for monitoring
collector = ValidationMetricsCollector()
collector.update_quality_score('completeness', metrics.completeness)
collector.update_quality_score('accuracy', metrics.accuracy)
collector.update_quality_score('overall', metrics.overall_score)

# Check for alerts
alerts = check_alerts({
    'quality_score': metrics.overall_score,
    'anomaly_rate': 0.03
})

for alert in alerts:
    send_alert(alert)  # Send to configured channels
```

### Example 4: Batch File Validation
**Purpose**: Validate large CSV/Parquet files with comprehensive reporting
**Implementation Example**:
```python
# Load and validate batch file
df = pd.read_csv('customer_data.csv')

# Profile the data
profiler = DataProfiler()
profile = profiler.profile_dataset(df)

# Run Great Expectations validation
ge_validator = GreatExpectationsValidator()
batch_request = ge_validator.context.get_batch_request(df)
validation_result = ge_validator.run_validation('customer_checkpoint', batch_request)

# Generate comprehensive report
report = {
    'profile': profile,
    'validation': validation_result,
    'timestamp': datetime.now().isoformat()
}

# Save report
with open('validation_report.json', 'w') as f:
    json.dump(report, f, indent=2, default=str)
```

## Output Format

Provide a comprehensive data validation system that includes:

1. **Schema Validation Models**: Complete Pydantic models with custom validators and JSON schema generation
2. **Quality Assessment Framework**: Implementation of all six data quality dimensions with scoring
3. **Great Expectations Suite**: Production-ready expectation suites with checkpoints and automation
4. **Streaming Validation**: Real-time validation with Kafka integration and dead letter queues
5. **Anomaly Detection**: Statistical and ML-based anomaly detection with multiple methods
6. **Rules Engine**: Flexible validation rules framework supporting complex business logic
7. **Monitoring Dashboard**: Metrics collection, alerting, and visualization components
8. **Integration Code**: Pipeline orchestration with Airflow or similar tools
9. **Performance Optimizations**: Caching, parallel processing, and incremental validation strategies
10. **Documentation**: Clear explanation of validation strategies, configuration options, and best practices

Ensure the validation system is extensible, performant, and provides clear error reporting for debugging and remediation.