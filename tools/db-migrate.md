# Database Migration Strategy and Implementation

You are a database migration expert specializing in zero-downtime deployments, data integrity, and multi-database environments. Create comprehensive migration scripts with rollback strategies, validation checks, and performance optimization.

## Context
The user needs help with database migrations that ensure data integrity, minimize downtime, and provide safe rollback options. Focus on production-ready migration strategies that handle edge cases and large datasets.

## Requirements
$ARGUMENTS

## Instructions

### 1. Migration Analysis

Analyze the required database changes:

**Schema Changes**
- **Table Operations**
  - Create new tables
  - Drop unused tables
  - Rename tables
  - Alter table engines/options
  
- **Column Operations**
  - Add columns (nullable vs non-nullable)
  - Drop columns (with data preservation)
  - Rename columns
  - Change data types
  - Modify constraints
  
- **Index Operations**
  - Create indexes (online vs offline)
  - Drop indexes
  - Modify index types
  - Add composite indexes
  
- **Constraint Operations**
  - Foreign keys
  - Unique constraints
  - Check constraints
  - Default values

**Data Migrations**
- **Transformations**
  - Data type conversions
  - Normalization/denormalization
  - Calculated fields
  - Data cleaning
  
- **Relationships**
  - Moving data between tables
  - Splitting/merging tables
  - Creating junction tables
  - Handling orphaned records

### 2. Zero-Downtime Strategy

Implement migrations without service interruption:

**Expand-Contract Pattern**
```sql
-- Phase 1: Expand (backward compatible)
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;
CREATE INDEX CONCURRENTLY idx_users_email_verified ON users(email_verified);

-- Phase 2: Migrate Data (in batches)
UPDATE users 
SET email_verified = (email_confirmation_token IS NOT NULL)
WHERE id IN (
  SELECT id FROM users 
  WHERE email_verified IS NULL 
  LIMIT 10000
);

-- Phase 3: Contract (after code deployment)
ALTER TABLE users DROP COLUMN email_confirmation_token;
```

**Blue-Green Schema Migration**
```python
# Step 1: Create new schema version
def create_v2_schema():
    """
    Create new tables with v2_ prefix
    """
    execute("""
        CREATE TABLE v2_orders (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            customer_id UUID NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metadata JSONB DEFAULT '{}'
        );
        
        CREATE INDEX idx_v2_orders_customer ON v2_orders(customer_id);
        CREATE INDEX idx_v2_orders_status ON v2_orders(status);
    """)

# Step 2: Sync data with dual writes
def enable_dual_writes():
    """
    Application writes to both old and new tables
    """
    # Trigger-based approach
    execute("""
        CREATE OR REPLACE FUNCTION sync_orders_to_v2() 
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO v2_orders (
                id, customer_id, total_amount, status, created_at
            ) VALUES (
                NEW.id, NEW.customer_id, NEW.amount, NEW.state, NEW.created
            ) ON CONFLICT (id) DO UPDATE SET
                total_amount = EXCLUDED.total_amount,
                status = EXCLUDED.status;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER sync_orders_trigger
        AFTER INSERT OR UPDATE ON orders
        FOR EACH ROW EXECUTE FUNCTION sync_orders_to_v2();
    """)

# Step 3: Backfill historical data
def backfill_data():
    """
    Copy historical data in batches
    """
    batch_size = 10000
    last_id = None
    
    while True:
        query = """
            INSERT INTO v2_orders (
                id, customer_id, total_amount, status, created_at
            )
            SELECT 
                id, customer_id, amount, state, created
            FROM orders
            WHERE ($1::uuid IS NULL OR id > $1)
            ORDER BY id
            LIMIT $2
            ON CONFLICT (id) DO NOTHING
            RETURNING id
        """
        
        results = execute(query, [last_id, batch_size])
        if not results:
            break
            
        last_id = results[-1]['id']
        time.sleep(0.1)  # Prevent overload

# Step 4: Switch reads
# Step 5: Switch writes  
# Step 6: Drop old schema
```

### 3. Migration Scripts

Generate version-controlled migration files:

**SQL Migrations**
```sql
-- migrations/001_add_user_preferences.up.sql
BEGIN;

-- Add new table
CREATE TABLE user_preferences (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(20) DEFAULT 'light',
    language VARCHAR(10) DEFAULT 'en',
    notifications JSONB DEFAULT '{"email": true, "push": false}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add update trigger
CREATE TRIGGER update_user_preferences_updated_at
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Add indexes
CREATE INDEX idx_user_preferences_language ON user_preferences(language);

-- Seed default data
INSERT INTO user_preferences (user_id)
SELECT id FROM users
ON CONFLICT DO NOTHING;

COMMIT;

-- migrations/001_add_user_preferences.down.sql
BEGIN;

DROP TABLE IF EXISTS user_preferences CASCADE;

COMMIT;
```

**Framework Migrations (Rails/Django/Laravel)**
```python
# Django migration
from django.db import migrations, models
import django.contrib.postgres.fields

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0010_previous_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreferences',
            fields=[
                ('user', models.OneToOneField(
                    'User', 
                    on_delete=models.CASCADE, 
                    primary_key=True
                )),
                ('theme', models.CharField(
                    max_length=20, 
                    default='light'
                )),
                ('language', models.CharField(
                    max_length=10, 
                    default='en',
                    db_index=True
                )),
                ('notifications', models.JSONField(
                    default=dict
                )),
                ('created_at', models.DateTimeField(
                    auto_now_add=True
                )),
                ('updated_at', models.DateTimeField(
                    auto_now=True
                )),
            ],
        ),
        
        # Custom SQL for complex operations
        migrations.RunSQL(
            sql=[
                """
                -- Forward migration
                UPDATE products 
                SET price_cents = CAST(price * 100 AS INTEGER)
                WHERE price_cents IS NULL;
                """,
            ],
            reverse_sql=[
                """
                -- Reverse migration
                UPDATE products 
                SET price = CAST(price_cents AS DECIMAL) / 100
                WHERE price IS NULL;
                """,
            ],
        ),
    ]
```

### 4. Data Integrity Checks

Implement comprehensive validation:

**Pre-Migration Validation**
```python
def validate_pre_migration():
    """
    Check data integrity before migration
    """
    checks = []
    
    # Check for NULL values in required fields
    null_check = execute("""
        SELECT COUNT(*) as count
        FROM users
        WHERE email IS NULL OR username IS NULL
    """)[0]['count']
    
    if null_check > 0:
        checks.append({
            'check': 'null_values',
            'status': 'FAILED',
            'message': f'{null_check} users with NULL email/username',
            'action': 'Fix NULL values before migration'
        })
    
    # Check for duplicate values
    duplicate_check = execute("""
        SELECT email, COUNT(*) as count
        FROM users
        GROUP BY email
        HAVING COUNT(*) > 1
    """)
    
    if duplicate_check:
        checks.append({
            'check': 'duplicates',
            'status': 'FAILED', 
            'message': f'{len(duplicate_check)} duplicate emails found',
            'action': 'Resolve duplicates before adding unique constraint'
        })
    
    # Check foreign key integrity
    orphan_check = execute("""
        SELECT COUNT(*) as count
        FROM orders o
        LEFT JOIN users u ON o.user_id = u.id
        WHERE u.id IS NULL
    """)[0]['count']
    
    if orphan_check > 0:
        checks.append({
            'check': 'orphaned_records',
            'status': 'WARNING',
            'message': f'{orphan_check} orders with non-existent users',
            'action': 'Clean up orphaned records'
        })
    
    return checks
```

**Post-Migration Validation**
```python
def validate_post_migration():
    """
    Verify migration success
    """
    validations = []
    
    # Row count validation
    old_count = execute("SELECT COUNT(*) FROM orders")[0]['count']
    new_count = execute("SELECT COUNT(*) FROM v2_orders")[0]['count']
    
    validations.append({
        'check': 'row_count',
        'expected': old_count,
        'actual': new_count,
        'status': 'PASS' if old_count == new_count else 'FAIL'
    })
    
    # Checksum validation
    old_checksum = execute("""
        SELECT 
            SUM(CAST(amount AS DECIMAL)) as total,
            COUNT(DISTINCT customer_id) as customers
        FROM orders
    """)[0]
    
    new_checksum = execute("""
        SELECT 
            SUM(total_amount) as total,
            COUNT(DISTINCT customer_id) as customers  
        FROM v2_orders
    """)[0]
    
    validations.append({
        'check': 'data_integrity',
        'status': 'PASS' if old_checksum == new_checksum else 'FAIL',
        'details': {
            'old': old_checksum,
            'new': new_checksum
        }
    })
    
    return validations
```

### 5. Rollback Procedures

Implement safe rollback strategies:

**Automatic Rollback**
```python
class MigrationRunner:
    def __init__(self, migration):
        self.migration = migration
        self.checkpoint = None
        
    def run_with_rollback(self):
        """
        Execute migration with automatic rollback on failure
        """
        try:
            # Create restore point
            self.checkpoint = self.create_checkpoint()
            
            # Run pre-checks
            pre_checks = self.migration.validate_pre()
            if any(c['status'] == 'FAILED' for c in pre_checks):
                raise MigrationError("Pre-validation failed", pre_checks)
            
            # Execute migration
            with transaction.atomic():
                self.migration.forward()
                
                # Run post-checks
                post_checks = self.migration.validate_post()
                if any(c['status'] == 'FAILED' for c in post_checks):
                    raise MigrationError("Post-validation failed", post_checks)
                    
            # Clean up checkpoint after success
            self.cleanup_checkpoint()
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            self.rollback()
            raise
            
    def rollback(self):
        """
        Restore to checkpoint
        """
        if self.checkpoint:
            execute(f"RESTORE DATABASE FROM CHECKPOINT '{self.checkpoint}'")
```

**Manual Rollback Scripts**
```bash
#!/bin/bash
# rollback_migration.sh

MIGRATION_VERSION=$1
DATABASE=$2

echo "Rolling back migration $MIGRATION_VERSION on $DATABASE"

# Check current version
CURRENT_VERSION=$(psql -d $DATABASE -t -c "SELECT version FROM schema_migrations ORDER BY version DESC LIMIT 1")

if [ "$CURRENT_VERSION" != "$MIGRATION_VERSION" ]; then
    echo "Error: Current version ($CURRENT_VERSION) doesn't match rollback version ($MIGRATION_VERSION)"
    exit 1
fi

# Execute rollback
psql -d $DATABASE -f "migrations/${MIGRATION_VERSION}.down.sql"

# Update version table
psql -d $DATABASE -c "DELETE FROM schema_migrations WHERE version = '$MIGRATION_VERSION'"

echo "Rollback completed successfully"
```

### 6. Performance Optimization

Minimize migration impact:

**Batch Processing**
```python
def migrate_large_table(batch_size=10000):
    """
    Migrate large tables in batches
    """
    total_rows = execute("SELECT COUNT(*) FROM source_table")[0]['count']
    processed = 0
    
    while processed < total_rows:
        # Process batch
        execute("""
            INSERT INTO target_table (columns...)
            SELECT columns...
            FROM source_table
            ORDER BY id
            OFFSET %s
            LIMIT %s
            ON CONFLICT DO NOTHING
        """, [processed, batch_size])
        
        processed += batch_size
        
        # Progress tracking
        progress = (processed / total_rows) * 100
        logger.info(f"Migration progress: {progress:.1f}%")
        
        # Prevent overload
        time.sleep(0.5)
```

**Index Management**
```sql
-- Drop indexes before bulk insert
ALTER TABLE large_table DROP INDEX idx_column1;
ALTER TABLE large_table DROP INDEX idx_column2;

-- Bulk insert
INSERT INTO large_table SELECT * FROM temp_data;

-- Recreate indexes concurrently
CREATE INDEX CONCURRENTLY idx_column1 ON large_table(column1);
CREATE INDEX CONCURRENTLY idx_column2 ON large_table(column2);
```

### 7. NoSQL and Cross-Platform Migration Support

Handle modern database migrations across SQL, NoSQL, and hybrid environments:

**Advanced Multi-Database Migration Framework**
```python
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import asyncio
from dataclasses import dataclass

@dataclass
class MigrationOperation:
    operation_type: str
    collection_or_table: str
    data: Dict[str, Any]
    conditions: Optional[Dict[str, Any]] = None
    batch_size: int = 1000

class DatabaseAdapter(ABC):
    @abstractmethod
    async def connect(self, connection_string: str):
        pass
    
    @abstractmethod
    async def execute_migration(self, operation: MigrationOperation):
        pass
    
    @abstractmethod
    async def validate_migration(self, operation: MigrationOperation) -> bool:
        pass
    
    @abstractmethod
    async def rollback_migration(self, operation: MigrationOperation):
        pass

class MongoDBAdapter(DatabaseAdapter):
    def __init__(self):
        self.client = None
        self.db = None
    
    async def connect(self, connection_string: str):
        from motor.motor_asyncio import AsyncIOMotorClient
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.get_default_database()
    
    async def execute_migration(self, operation: MigrationOperation):
        collection = self.db[operation.collection_or_table]
        
        if operation.operation_type == 'add_field':
            await self._add_field(collection, operation)
        elif operation.operation_type == 'rename_field':
            await self._rename_field(collection, operation)
        elif operation.operation_type == 'migrate_data':
            await self._migrate_data(collection, operation)
        elif operation.operation_type == 'create_index':
            await self._create_index(collection, operation)
        elif operation.operation_type == 'schema_validation':
            await self._add_schema_validation(collection, operation)
    
    async def _add_field(self, collection, operation):
        """Add new field to all documents"""
        field_name = operation.data['field_name']
        default_value = operation.data.get('default_value')
        
        # Add field to documents that don't have it
        result = await collection.update_many(
            {field_name: {"$exists": False}},
            {"$set": {field_name: default_value}}
        )
        
        return {
            'matched_count': result.matched_count,
            'modified_count': result.modified_count
        }
    
    async def _rename_field(self, collection, operation):
        """Rename field across all documents"""
        old_name = operation.data['old_name']
        new_name = operation.data['new_name']
        
        result = await collection.update_many(
            {old_name: {"$exists": True}},
            {"$rename": {old_name: new_name}}
        )
        
        return {
            'matched_count': result.matched_count,
            'modified_count': result.modified_count
        }
    
    async def _migrate_data(self, collection, operation):
        """Transform data during migration"""
        pipeline = operation.data['pipeline']
        
        # Use aggregation pipeline for complex transformations
        cursor = collection.aggregate([
            {"$match": operation.conditions or {}},
            *pipeline,
            {"$merge": {
                "into": operation.collection_or_table,
                "on": "_id",
                "whenMatched": "replace"
            }}
        ])
        
        return [doc async for doc in cursor]
    
    async def _add_schema_validation(self, collection, operation):
        """Add JSON schema validation to collection"""
        schema = operation.data['schema']
        
        await self.db.command({
            "collMod": operation.collection_or_table,
            "validator": {"$jsonSchema": schema},
            "validationLevel": "strict",
            "validationAction": "error"
        })

class DynamoDBAdapter(DatabaseAdapter):
    def __init__(self):
        self.dynamodb = None
    
    async def connect(self, connection_string: str):
        import boto3
        self.dynamodb = boto3.resource('dynamodb')
    
    async def execute_migration(self, operation: MigrationOperation):
        table = self.dynamodb.Table(operation.collection_or_table)
        
        if operation.operation_type == 'add_gsi':
            await self._add_global_secondary_index(table, operation)
        elif operation.operation_type == 'migrate_data':
            await self._migrate_table_data(table, operation)
        elif operation.operation_type == 'update_capacity':
            await self._update_capacity(table, operation)
    
    async def _add_global_secondary_index(self, table, operation):
        """Add Global Secondary Index"""
        gsi_spec = operation.data['gsi_specification']
        
        table.update(
            GlobalSecondaryIndexUpdates=[
                {
                    'Create': gsi_spec
                }
            ]
        )
    
    async def _migrate_table_data(self, table, operation):
        """Migrate data between DynamoDB tables"""
        scan_kwargs = {
            'ProjectionExpression': operation.data.get('projection'),
            'FilterExpression': operation.conditions
        }
        
        target_table = self.dynamodb.Table(operation.data['target_table'])
        
        # Scan source table and write to target
        while True:
            response = table.scan(**scan_kwargs)
            
            # Transform and write items
            with target_table.batch_writer() as batch:
                for item in response['Items']:
                    transformed_item = self._transform_item(item, operation.data['transformation'])
                    batch.put_item(Item=transformed_item)
            
            if 'LastEvaluatedKey' not in response:
                break
            scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']

class CassandraAdapter(DatabaseAdapter):
    def __init__(self):
        self.session = None
    
    async def connect(self, connection_string: str):
        from cassandra.cluster import Cluster
        from cassandra.auth import PlainTextAuthProvider
        
        # Parse connection string for auth
        cluster = Cluster(['127.0.0.1'])
        self.session = cluster.connect()
    
    async def execute_migration(self, operation: MigrationOperation):
        if operation.operation_type == 'add_column':
            await self._add_column(operation)
        elif operation.operation_type == 'create_materialized_view':
            await self._create_materialized_view(operation)
        elif operation.operation_type == 'migrate_data':
            await self._migrate_data(operation)
    
    async def _add_column(self, operation):
        """Add column to Cassandra table"""
        table = operation.collection_or_table
        column_name = operation.data['column_name']
        column_type = operation.data['column_type']
        
        cql = f"ALTER TABLE {table} ADD {column_name} {column_type}"
        self.session.execute(cql)
    
    async def _create_materialized_view(self, operation):
        """Create materialized view for denormalization"""
        view_spec = operation.data['view_specification']
        self.session.execute(view_spec)

class CrossPlatformMigrator:
    def __init__(self):
        self.adapters = {
            'postgresql': PostgreSQLAdapter(),
            'mysql': MySQLAdapter(),
            'mongodb': MongoDBAdapter(),
            'dynamodb': DynamoDBAdapter(),
            'cassandra': CassandraAdapter(),
            'redis': RedisAdapter(),
            'elasticsearch': ElasticsearchAdapter()
        }
    
    async def migrate_between_platforms(self, source_config, target_config, migration_spec):
        """Migrate data between different database platforms"""
        source_adapter = self.adapters[source_config['type']]
        target_adapter = self.adapters[target_config['type']]
        
        await source_adapter.connect(source_config['connection_string'])
        await target_adapter.connect(target_config['connection_string'])
        
        # Execute migration plan
        for step in migration_spec['steps']:
            if step['type'] == 'extract':
                data = await self._extract_data(source_adapter, step)
            elif step['type'] == 'transform':
                data = await self._transform_data(data, step)
            elif step['type'] == 'load':
                await self._load_data(target_adapter, data, step)
    
    async def _extract_data(self, adapter, step):
        """Extract data from source database"""
        extraction_op = MigrationOperation(
            operation_type='extract',
            collection_or_table=step['source_table'],
            data=step.get('extraction_params', {}),
            conditions=step.get('conditions'),
            batch_size=step.get('batch_size', 1000)
        )
        
        return await adapter.execute_migration(extraction_op)
    
    async def _transform_data(self, data, step):
        """Transform data between formats"""
        transformation_rules = step['transformation_rules']
        
        transformed_data = []
        for record in data:
            transformed_record = {}
            
            for target_field, source_mapping in transformation_rules.items():
                if isinstance(source_mapping, str):
                    # Simple field mapping
                    transformed_record[target_field] = record.get(source_mapping)
                elif isinstance(source_mapping, dict):
                    # Complex transformation
                    if source_mapping['type'] == 'function':
                        func = source_mapping['function']
                        args = [record.get(arg) for arg in source_mapping['args']]
                        transformed_record[target_field] = func(*args)
                    elif source_mapping['type'] == 'concatenate':
                        fields = source_mapping['fields']
                        separator = source_mapping.get('separator', ' ')
                        values = [str(record.get(field, '')) for field in fields]
                        transformed_record[target_field] = separator.join(values)
            
            transformed_data.append(transformed_record)
        
        return transformed_data
    
    async def _load_data(self, adapter, data, step):
        """Load data into target database"""
        load_op = MigrationOperation(
            operation_type='load',
            collection_or_table=step['target_table'],
            data={'records': data},
            batch_size=step.get('batch_size', 1000)
        )
        
        return await adapter.execute_migration(load_op)

# Example usage
async def migrate_sql_to_nosql():
    """Example: Migrate from PostgreSQL to MongoDB"""
    migrator = CrossPlatformMigrator()
    
    source_config = {
        'type': 'postgresql',
        'connection_string': 'postgresql://user:pass@localhost/db'
    }
    
    target_config = {
        'type': 'mongodb',
        'connection_string': 'mongodb://localhost:27017/db'
    }
    
    migration_spec = {
        'steps': [
            {
                'type': 'extract',
                'source_table': 'users',
                'conditions': {'active': True},
                'batch_size': 5000
            },
            {
                'type': 'transform',
                'transformation_rules': {
                    '_id': 'id',
                    'full_name': {
                        'type': 'concatenate',
                        'fields': ['first_name', 'last_name'],
                        'separator': ' '
                    },
                    'metadata': {
                        'type': 'function',
                        'function': lambda created, updated: {
                            'created_at': created,
                            'updated_at': updated
                        },
                        'args': ['created_at', 'updated_at']
                    }
                }
            },
            {
                'type': 'load',
                'target_table': 'users',
                'batch_size': 1000
            }
        ]
    }
    
    await migrator.migrate_between_platforms(source_config, target_config, migration_spec)
```

### 8. Modern Migration Tools and Change Data Capture

Integrate with enterprise migration tools and real-time sync:

**Atlas Schema Migrations (MongoDB)**
```javascript
// atlas-migration.js
const { MongoClient } = require('mongodb');

class AtlasMigration {
    constructor(connectionString) {
        this.client = new MongoClient(connectionString);
        this.migrations = new Map();
    }
    
    register(version, migration) {
        this.migrations.set(version, migration);
    }
    
    async migrate() {
        await this.client.connect();
        const db = this.client.db();
        
        // Get current version
        const versionsCollection = db.collection('schema_versions');
        const currentVersion = await versionsCollection
            .findOne({}, { sort: { version: -1 } });
        
        const startVersion = currentVersion?.version || 0;
        
        // Run pending migrations
        for (const [version, migration] of this.migrations) {
            if (version > startVersion) {
                console.log(`Running migration ${version}`);
                
                const session = this.client.startSession();
                
                try {
                    await session.withTransaction(async () => {
                        await migration.up(db, session);
                        await versionsCollection.insertOne({
                            version,
                            applied_at: new Date(),
                            checksum: migration.checksum
                        });
                    });
                } catch (error) {
                    console.error(`Migration ${version} failed:`, error);
                    if (migration.down) {
                        await migration.down(db, session);
                    }
                    throw error;
                } finally {
                    await session.endSession();
                }
            }
        }
    }
}

// Example MongoDB schema migration
const migration_001 = {
    checksum: 'sha256:abc123...',
    
    async up(db, session) {
        // Add new field to existing documents
        await db.collection('users').updateMany(
            { email_verified: { $exists: false } },
            { 
                $set: { 
                    email_verified: false,
                    verification_token: null,
                    verification_expires: null
                }
            },
            { session }
        );
        
        // Create new index
        await db.collection('users').createIndex(
            { email_verified: 1, verification_expires: 1 },
            { session }
        );
        
        // Add schema validation
        await db.command({
            collMod: 'users',
            validator: {
                $jsonSchema: {
                    bsonType: 'object',
                    required: ['email', 'email_verified'],
                    properties: {
                        email: { bsonType: 'string' },
                        email_verified: { bsonType: 'bool' },
                        verification_token: { 
                            bsonType: ['string', 'null'] 
                        }
                    }
                }
            }
        }, { session });
    },
    
    async down(db, session) {
        // Remove schema validation
        await db.command({
            collMod: 'users',
            validator: {}
        }, { session });
        
        // Drop index
        await db.collection('users').dropIndex(
            { email_verified: 1, verification_expires: 1 },
            { session }
        );
        
        // Remove fields
        await db.collection('users').updateMany(
            {},
            { 
                $unset: {
                    email_verified: '',
                    verification_token: '',
                    verification_expires: ''
                }
            },
            { session }
        );
    }
};
```

**Change Data Capture (CDC) for Real-time Sync**
```python
# cdc-migration.py
import asyncio
from kafka import KafkaConsumer, KafkaProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
import json

class CDCMigrationManager:
    def __init__(self, config):
        self.config = config
        self.consumer = None
        self.producer = None
        self.schema_registry = None
        self.active_migrations = {}
    
    async def setup_cdc_pipeline(self):
        """Setup Change Data Capture pipeline"""
        # Kafka consumer for CDC events
        self.consumer = KafkaConsumer(
            'database.changes',
            bootstrap_servers=self.config['kafka_brokers'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='migration-consumer',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        # Kafka producer for processed events
        self.producer = KafkaProducer(
            bootstrap_servers=self.config['kafka_brokers'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Schema registry for data validation
        self.schema_registry = SchemaRegistryClient({
            'url': self.config['schema_registry_url']
        })
    
    async def process_cdc_events(self):
        """Process CDC events and apply to target databases"""
        for message in self.consumer:
            event = message.value
            
            # Parse CDC event
            operation = event['operation']  # INSERT, UPDATE, DELETE
            table = event['table']
            data = event['data']
            
            # Check if this table has active migration
            if table in self.active_migrations:
                migration_config = self.active_migrations[table]
                await self.apply_migration_transformation(event, migration_config)
            else:
                # Standard replication
                await self.replicate_change(event)
    
    async def apply_migration_transformation(self, event, migration_config):
        """Apply data transformation during migration"""
        transformation_rules = migration_config['transformation_rules']
        target_tables = migration_config['target_tables']
        
        # Transform data according to migration rules
        transformed_data = {}
        for target_field, rule in transformation_rules.items():
            if isinstance(rule, str):
                # Simple field mapping
                transformed_data[target_field] = event['data'].get(rule)
            elif isinstance(rule, dict):
                # Complex transformation
                if rule['type'] == 'function':
                    func_name = rule['function']
                    func = getattr(self, f'transform_{func_name}')
                    args = [event['data'].get(arg) for arg in rule['args']]
                    transformed_data[target_field] = func(*args)
        
        # Apply to target tables
        for target_table in target_tables:
            await self.apply_to_target(target_table, event['operation'], transformed_data)
    
    async def setup_debezium_connector(self, source_db_config):
        """Configure Debezium for CDC"""
        connector_config = {
            "name": f"migration-connector-{source_db_config['name']}",
            "config": {
                "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
                "database.hostname": source_db_config['host'],
                "database.port": source_db_config['port'],
                "database.user": source_db_config['user'],
                "database.password": source_db_config['password'],
                "database.dbname": source_db_config['database'],
                "database.server.name": source_db_config['name'],
                "table.include.list": ",".join(source_db_config['tables']),
                "plugin.name": "pgoutput",
                "slot.name": f"migration_slot_{source_db_config['name']}",
                "publication.name": f"migration_pub_{source_db_config['name']}",
                "transforms": "route",
                "transforms.route.type": "org.apache.kafka.connect.transforms.RegexRouter",
                "transforms.route.regex": "([^.]+)\.([^.]+)\.([^.]+)",
                "transforms.route.replacement": "database.changes"
            }
        }
        
        # Submit connector to Kafka Connect
        import requests
        response = requests.post(
            f"{self.config['kafka_connect_url']}/connectors",
            json=connector_config,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code != 201:
            raise Exception(f"Failed to create connector: {response.text}")
```

**Advanced Monitoring and Observability**
```python
class EnterpriseeMigrationMonitor:
    def __init__(self, config):
        self.config = config
        self.metrics_client = self.setup_metrics_client()
        self.alerting_client = self.setup_alerting_client()
        self.migration_state = {
            'current_migrations': {},
            'completed_migrations': {},
            'failed_migrations': {}
        }
    
    def setup_metrics_client(self):
        """Setup Prometheus/Datadog metrics client"""
        from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry
        
        registry = CollectorRegistry()
        
        self.metrics = {
            'migration_duration': Histogram(
                'migration_duration_seconds',
                'Time spent on migration',
                ['migration_id', 'source_db', 'target_db'],
                registry=registry
            ),
            'rows_migrated': Counter(
                'migration_rows_total',
                'Total rows migrated',
                ['migration_id', 'table_name'],
                registry=registry
            ),
            'migration_errors': Counter(
                'migration_errors_total',
                'Total migration errors',
                ['migration_id', 'error_type'],
                registry=registry
            ),
            'active_migrations': Gauge(
                'active_migrations_count',
                'Number of active migrations',
                registry=registry
            ),
            'data_lag': Gauge(
                'migration_data_lag_seconds',
                'Data lag between source and target',
                ['migration_id'],
                registry=registry
            )
        }
        
        return registry
    
    async def track_migration_progress(self, migration_id):
        """Real-time migration progress tracking"""
        migration = self.migration_state['current_migrations'][migration_id]
        
        while migration['status'] == 'running':
            # Calculate progress metrics
            progress_stats = await self.calculate_progress_stats(migration)
            
            # Update Prometheus metrics
            self.metrics['rows_migrated'].labels(
                migration_id=migration_id,
                table_name=migration['table']
            ).inc(progress_stats['rows_processed_delta'])
            
            self.metrics['data_lag'].labels(
                migration_id=migration_id
            ).set(progress_stats['lag_seconds'])
            
            # Check for anomalies
            await self.detect_migration_anomalies(migration_id, progress_stats)
            
            # Generate alerts if needed
            await self.check_alert_conditions(migration_id, progress_stats)
            
            await asyncio.sleep(30)  # Check every 30 seconds
    
    async def detect_migration_anomalies(self, migration_id, stats):
        """AI-powered anomaly detection for migrations"""
        # Simple statistical anomaly detection
        if stats['rows_per_second'] < stats['expected_rows_per_second'] * 0.5:
            await self.trigger_alert(
                'migration_slow',
                f"Migration {migration_id} is running slower than expected",
                {'stats': stats}
            )
        
        if stats['error_rate'] > 0.01:  # 1% error rate threshold
            await self.trigger_alert(
                'migration_high_error_rate',
                f"Migration {migration_id} has high error rate: {stats['error_rate']}",
                {'stats': stats}
            )
        
        if stats['memory_usage'] > 0.8:  # 80% memory usage
            await self.trigger_alert(
                'migration_high_memory',
                f"Migration {migration_id} is using high memory: {stats['memory_usage']}",
                {'stats': stats}
            )
    
    async def setup_migration_dashboard(self):
        """Setup Grafana dashboard for migration monitoring"""
        dashboard_config = {
            "dashboard": {
                "title": "Database Migration Monitoring",
                "panels": [
                    {
                        "title": "Migration Progress",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "rate(migration_rows_total[5m])",
                                "legendFormat": "{{migration_id}} - {{table_name}}"
                            }
                        ]
                    },
                    {
                        "title": "Data Lag",
                        "type": "singlestat",
                        "targets": [
                            {
                                "expr": "migration_data_lag_seconds",
                                "legendFormat": "Lag (seconds)"
                            }
                        ]
                    },
                    {
                        "title": "Error Rate",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": "rate(migration_errors_total[5m])",
                                "legendFormat": "{{error_type}}"
                            }
                        ]
                    },
                    {
                        "title": "Migration Duration",
                        "type": "heatmap",
                        "targets": [
                            {
                                "expr": "migration_duration_seconds",
                                "legendFormat": "Duration"
                            }
                        ]
                    }
                ]
            }
        }
        
        # Submit dashboard to Grafana API
        import requests
        response = requests.post(
            f"{self.config['grafana_url']}/api/dashboards/db",
            json=dashboard_config,
            headers={
                'Authorization': f"Bearer {self.config['grafana_token']}",
                'Content-Type': 'application/json'
            }
        )
        
        return response.json()
```

### 9. Event Sourcing and CQRS Migrations

Handle event-driven architecture migrations:

**Event Store Migration Strategy**
```python
class EventStoreMigrator:
    def __init__(self, event_store_config):
        self.event_store = EventStore(event_store_config)
        self.event_transformers = {}
        self.aggregate_rebuilders = {}
    
    def register_event_transformer(self, event_type, transformer):
        """Register transformation for specific event type"""
        self.event_transformers[event_type] = transformer
    
    def register_aggregate_rebuilder(self, aggregate_type, rebuilder):
        """Register rebuilder for aggregate snapshots"""
        self.aggregate_rebuilders[aggregate_type] = rebuilder
    
    async def migrate_events(self, from_version, to_version):
        """Migrate events from one schema version to another"""
        # Get all events that need migration
        events_cursor = self.event_store.get_events_by_version_range(
            from_version, to_version
        )
        
        migrated_events = []
        
        async for event in events_cursor:
            if event.event_type in self.event_transformers:
                transformer = self.event_transformers[event.event_type]
                migrated_event = await transformer.transform(event)
                migrated_events.append(migrated_event)
            else:
                # No transformation needed
                migrated_events.append(event)
        
        # Write migrated events to new stream
        await self.event_store.append_events(
            f"migration-{to_version}",
            migrated_events
        )
        
        # Rebuild aggregates with new events
        await self.rebuild_aggregates(migrated_events)
    
    async def rebuild_aggregates(self, events):
        """Rebuild aggregate snapshots from migrated events"""
        aggregates_to_rebuild = set()
        
        for event in events:
            aggregates_to_rebuild.add(event.aggregate_id)
        
        for aggregate_id in aggregates_to_rebuild:
            aggregate_type = self.get_aggregate_type(aggregate_id)
            
            if aggregate_type in self.aggregate_rebuilders:
                rebuilder = self.aggregate_rebuilders[aggregate_type]
                await rebuilder.rebuild(aggregate_id)

# Example event transformation
class UserEventTransformer:
    async def transform(self, event):
        """Transform UserCreated event from v1 to v2"""
        if event.event_type == 'UserCreated' and event.version == 1:
            # v1 had separate first_name and last_name
            # v2 uses full_name
            old_data = event.data
            new_data = {
                'user_id': old_data['user_id'],
                'full_name': f"{old_data['first_name']} {old_data['last_name']}",
                'email': old_data['email'],
                'created_at': old_data['created_at']
            }
            
            return Event(
                event_id=event.event_id,
                event_type='UserCreated',
                aggregate_id=event.aggregate_id,
                version=2,
                data=new_data,
                metadata=event.metadata
            )
        
        return event
```

### 10. Cloud Database Migration Automation

Automate cloud database migrations with infrastructure as code:

**AWS Database Migration with CDK**
```typescript
// aws-db-migration.ts
import * as cdk from 'aws-cdk-lib';
import * as dms from 'aws-cdk-lib/aws-dms';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as stepfunctions from 'aws-cdk-lib/aws-stepfunctions';
import * as sfnTasks from 'aws-cdk-lib/aws-stepfunctions-tasks';

export class DatabaseMigrationStack extends cdk.Stack {
    constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
        super(scope, id, props);
        
        // Create VPC for migration
        const vpc = new ec2.Vpc(this, 'MigrationVPC', {
            maxAzs: 2,
            subnetConfiguration: [
                {
                    cidrMask: 24,
                    name: 'private',
                    subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS
                },
                {
                    cidrMask: 24,
                    name: 'public',
                    subnetType: ec2.SubnetType.PUBLIC
                }
            ]
        });
        
        // DMS Replication Instance
        const replicationInstance = new dms.CfnReplicationInstance(this, 'ReplicationInstance', {
            replicationInstanceClass: 'dms.t3.medium',
            replicationInstanceIdentifier: 'migration-instance',
            allocatedStorage: 100,
            autoMinorVersionUpgrade: true,
            multiAz: false,
            publiclyAccessible: false,
            replicationSubnetGroupIdentifier: this.createSubnetGroup(vpc).ref
        });
        
        // Source and Target Endpoints
        const sourceEndpoint = new dms.CfnEndpoint(this, 'SourceEndpoint', {
            endpointType: 'source',
            engineName: 'postgres',
            serverName: 'source-db.example.com',
            port: 5432,
            databaseName: 'source_db',
            username: 'migration_user',
            password: 'migration_password'
        });
        
        const targetEndpoint = new dms.CfnEndpoint(this, 'TargetEndpoint', {
            endpointType: 'target',
            engineName: 'postgres',
            serverName: 'target-db.example.com',
            port: 5432,
            databaseName: 'target_db',
            username: 'migration_user',
            password: 'migration_password'
        });
        
        // Migration Task
        const migrationTask = new dms.CfnReplicationTask(this, 'MigrationTask', {
            replicationTaskIdentifier: 'full-load-and-cdc',
            sourceEndpointArn: sourceEndpoint.ref,
            targetEndpointArn: targetEndpoint.ref,
            replicationInstanceArn: replicationInstance.ref,
            migrationType: 'full-load-and-cdc',
            tableMappings: JSON.stringify({
                "rules": [
                    {
                        "rule-type": "selection",
                        "rule-id": "1",
                        "rule-name": "1",
                        "object-locator": {
                            "schema-name": "public",
                            "table-name": "%"
                        },
                        "rule-action": "include"
                    }
                ]
            }),
            replicationTaskSettings: JSON.stringify({
                "TargetMetadata": {
                    "TargetSchema": "",
                    "SupportLobs": true,
                    "FullLobMode": false,
                    "LobChunkSize": 0,
                    "LimitedSizeLobMode": true,
                    "LobMaxSize": 32,
                    "LoadMaxFileSize": 0,
                    "ParallelLoadThreads": 0,
                    "ParallelLoadBufferSize": 0,
                    "BatchApplyEnabled": false,
                    "TaskRecoveryTableEnabled": false
                },
                "FullLoadSettings": {
                    "TargetTablePrepMode": "DROP_AND_CREATE",
                    "CreatePkAfterFullLoad": false,
                    "StopTaskCachedChangesApplied": false,
                    "StopTaskCachedChangesNotApplied": false,
                    "MaxFullLoadSubTasks": 8,
                    "TransactionConsistencyTimeout": 600,
                    "CommitRate": 10000
                },
                "Logging": {
                    "EnableLogging": true,
                    "LogComponents": [
                        {
                            "Id": "SOURCE_UNLOAD",
                            "Severity": "LOGGER_SEVERITY_DEFAULT"
                        },
                        {
                            "Id": "TARGET_LOAD",
                            "Severity": "LOGGER_SEVERITY_DEFAULT"
                        }
                    ]
                }
            })
        });
        
        // Migration orchestration with Step Functions
        this.createMigrationOrchestration(migrationTask);
    }
    
    private createSubnetGroup(vpc: ec2.Vpc): dms.CfnReplicationSubnetGroup {
        return new dms.CfnReplicationSubnetGroup(this, 'ReplicationSubnetGroup', {
            replicationSubnetGroupDescription: 'Subnet group for DMS',
            replicationSubnetGroupIdentifier: 'migration-subnet-group',
            subnetIds: vpc.privateSubnets.map(subnet => subnet.subnetId)
        });
    }
    
    private createMigrationOrchestration(migrationTask: dms.CfnReplicationTask): void {
        // Lambda functions for migration steps
        const startMigrationFunction = new lambda.Function(this, 'StartMigration', {
            runtime: lambda.Runtime.PYTHON_3_9,
            handler: 'index.handler',
            code: lambda.Code.fromInline(`
import boto3
import json

def handler(event, context):
    dms = boto3.client('dms')
    task_arn = event['task_arn']
    
    response = dms.start_replication_task(
        ReplicationTaskArn=task_arn,
        StartReplicationTaskType='start-replication'
    )
    
    return {
        'statusCode': 200,
        'task_arn': task_arn,
        'task_status': response['ReplicationTask']['Status']
    }
            `)
        });
        
        const checkMigrationStatusFunction = new lambda.Function(this, 'CheckMigrationStatus', {
            runtime: lambda.Runtime.PYTHON_3_9,
            handler: 'index.handler',
            code: lambda.Code.fromInline(`
import boto3
import json

def handler(event, context):
    dms = boto3.client('dms')
    task_arn = event['task_arn']
    
    response = dms.describe_replication_tasks(
        Filters=[
            {
                'Name': 'replication-task-arn',
                'Values': [task_arn]
            }
        ]
    )
    
    task = response['ReplicationTasks'][0]
    status = task['Status']
    
    return {
        'task_arn': task_arn,
        'task_status': status,
        'is_complete': status in ['stopped', 'failed', 'ready']
    }
            `)
        });
        
        // Step Function definition
        const startMigrationTask = new sfnTasks.LambdaInvoke(this, 'StartMigrationTask', {
            lambdaFunction: startMigrationFunction,
            inputPath: '$',
            outputPath: '$'
        });
        
        const checkStatusTask = new sfnTasks.LambdaInvoke(this, 'CheckMigrationStatusTask', {
            lambdaFunction: checkMigrationStatusFunction,
            inputPath: '$',
            outputPath: '$'
        });
        
        const waitTask = new stepfunctions.Wait(this, 'WaitForMigration', {
            time: stepfunctions.WaitTime.duration(cdk.Duration.minutes(5))
        });
        
        const migrationComplete = new stepfunctions.Succeed(this, 'MigrationComplete');
        const migrationFailed = new stepfunctions.Fail(this, 'MigrationFailed');
        
        // Define state machine
        const definition = startMigrationTask
            .next(waitTask)
            .next(checkStatusTask)
            .next(new stepfunctions.Choice(this, 'IsMigrationComplete?')
                .when(stepfunctions.Condition.booleanEquals('$.is_complete', true),
                      new stepfunctions.Choice(this, 'MigrationSuccessful?')
                          .when(stepfunctions.Condition.stringEquals('$.task_status', 'stopped'), migrationComplete)
                          .otherwise(migrationFailed))
                .otherwise(waitTask));
        
        new stepfunctions.StateMachine(this, 'MigrationStateMachine', {
            definition: definition,
            timeout: cdk.Duration.hours(24)
        });
    }
}
```

## Output Format

1. **Comprehensive Migration Strategy**: Multi-database platform support with NoSQL integration
2. **Cross-Platform Migration Tools**: SQL to NoSQL, NoSQL to SQL, and hybrid migrations
3. **Modern Tooling Integration**: Atlas, Debezium, Flyway, Prisma, and cloud-native solutions
4. **Change Data Capture Pipeline**: Real-time synchronization with Kafka and schema registry
5. **Event Sourcing Migrations**: Event store transformations and aggregate rebuilding
6. **Cloud Infrastructure Automation**: AWS DMS, GCP Database Migration Service, Azure DMS
7. **Enterprise Monitoring Suite**: Prometheus metrics, Grafana dashboards, and anomaly detection
8. **Advanced Validation Framework**: Multi-database integrity checks and performance benchmarks
9. **Automated Rollback Procedures**: Platform-specific recovery strategies
10. **Performance Optimization**: Batch processing, parallel execution, and resource management

Focus on zero-downtime migrations with comprehensive validation, automated rollbacks, and enterprise-grade monitoring across all supported database platforms.

## Cross-Command Integration

This command integrates seamlessly with other development workflow commands to create a comprehensive database-first development pipeline:

### Integration with API Development (`/api-scaffold`)
```python
# integrated-db-api-config.py
class IntegratedDatabaseApiConfig:
    def __init__(self):
        self.api_config = self.load_api_config()        # From /api-scaffold
        self.db_config = self.load_db_config()          # From /db-migrate
        self.migration_config = self.load_migration_config()
    
    def generate_api_aware_migrations(self):
        """Generate migrations that consider API endpoints and schemas"""
        return {
            # API-aware migration strategy
            'api_migration_strategy': f"""
-- Migration with API endpoint consideration
-- Migration: {datetime.now().strftime('%Y%m%d_%H%M%S')}_api_aware_schema_update.sql

-- Check API dependency before migration
DO $$
BEGIN
    -- Verify API endpoints that depend on this schema
    IF EXISTS (
        SELECT 1 FROM api_endpoints 
        WHERE schema_dependencies @> '["users", "profiles"]'
        AND is_active = true
    ) THEN
        RAISE NOTICE 'Found active API endpoints depending on this schema';
        
        -- Create migration strategy with API versioning
        CREATE TABLE IF NOT EXISTS api_migration_log (
            id SERIAL PRIMARY KEY,
            migration_name VARCHAR(255) NOT NULL,
            api_version VARCHAR(50) NOT NULL,
            schema_changes JSONB,
            rollback_script TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Log this migration for API tracking
        INSERT INTO api_migration_log (
            migration_name, 
            api_version, 
            schema_changes
        ) VALUES (
            'api_aware_schema_update',
            '{self.api_config.get("version", "v1")}',
            '{{"tables": ["users", "profiles"], "type": "schema_update"}}'::jsonb
        );
    END IF;
END $$;

-- Backward-compatible schema changes
ALTER TABLE users ADD COLUMN IF NOT EXISTS new_field VARCHAR(255);

-- Create view for API backward compatibility
CREATE OR REPLACE VIEW users_api_v1 AS 
SELECT 
    id,
    username,
    email,
    -- Maintain API compatibility
    COALESCE(new_field, 'default_value') as new_field,
    created_at,
    updated_at
FROM users;

-- Grant API service access
GRANT SELECT ON users_api_v1 TO {self.api_config.get("db_user", "api_service")};

COMMIT;
            """,
            
            # Database connection pool optimization for API
            'connection_pool_config': {
                'fastapi': f"""
# FastAPI with optimized database connections
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

class DatabaseConfig:
    def __init__(self):
        self.database_url = "{self.db_config.get('url', 'postgresql://localhost/app')}"
        self.api_config = {self.api_config}
        
    def create_engine(self):
        return create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size={self.api_config.get('db_pool_size', 20)},
            max_overflow={self.api_config.get('db_max_overflow', 0)},
            pool_pre_ping=True,
            pool_recycle=3600,
            echo={str(self.api_config.get('debug', False)).lower()}
        )
    
    def get_session_maker(self):
        engine = self.create_engine()
        return sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Migration-aware API dependencies
async def get_db_with_migration_check():
    # Check if migrations are running
    async with get_db() as session:
        result = await session.execute(
            text("SELECT COUNT(*) FROM schema_migrations WHERE is_running = true")
        )
        running_migrations = result.scalar()
        
        if running_migrations > 0:
            raise HTTPException(
                status_code=503,
                detail="Database migrations in progress. API temporarily unavailable."
            )
        
        yield session
                """,
                
                'express': f"""
// Express.js with database migration awareness
const {{ Pool }} = require('pg');
const express = require('express');
const app = express();

class DatabaseManager {{
    constructor() {{
        this.pool = new Pool({{
            connectionString: '{self.db_config.get('url', 'postgresql://localhost/app')}',
            max: {self.api_config.get('db_pool_size', 20)},
            idleTimeoutMillis: 30000,
            connectionTimeoutMillis: 2000,
        }});
        
        this.migrationStatus = new Map();
    }}
    
    async checkMigrationStatus() {{
        try {{
            const client = await this.pool.connect();
            const result = await client.query(
                'SELECT COUNT(*) as count FROM schema_migrations WHERE is_running = true'
            );
            client.release();
            
            return result.rows[0].count === '0';
        }} catch (error) {{
            console.error('Failed to check migration status:', error);
            return false;
        }}
    }}
    
    // Middleware to check migration status
    migrationStatusMiddleware() {{
        return async (req, res, next) => {{
            const isSafe = await this.checkMigrationStatus();
            
            if (!isSafe) {{
                return res.status(503).json({{
                    error: 'Database migrations in progress',
                    message: 'API temporarily unavailable during database updates'
                }});
            }}
            
            next();
        }};
    }}
}}

const dbManager = new DatabaseManager();
app.use('/api', dbManager.migrationStatusMiddleware());
                """
            }
        }
    
    def generate_api_schema_sync(self):
        """Generate API schema synchronization with database"""
        return f"""
# API Schema Synchronization
import asyncio
import aiohttp
from sqlalchemy import text

class ApiSchemaSync:
    def __init__(self, api_base_url="{self.api_config.get('base_url', 'http://localhost:8000')}"):
        self.api_base_url = api_base_url
        self.db_config = {self.db_config}
    
    async def notify_api_of_schema_change(self, migration_name, schema_changes):
        '''Notify API service of database schema changes'''
        async with aiohttp.ClientSession() as session:
            payload = {{
                'migration_name': migration_name,
                'schema_changes': schema_changes,
                'timestamp': datetime.now().isoformat()
            }}
            
            try:
                async with session.post(
                    f"{{self.api_base_url}}/internal/schema-update",
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        print(f"API notified of schema changes: {{migration_name}}")
                    else:
                        print(f"Failed to notify API: {{response.status}}")
            except Exception as e:
                print(f"Error notifying API: {{e}}")
    
    async def validate_api_compatibility(self, proposed_changes):
        '''Validate that proposed schema changes won't break API'''
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{{self.api_base_url}}/internal/validate-schema",
                    json={{'proposed_changes': proposed_changes}},
                    timeout=30
                ) as response:
                    result = await response.json()
                    return result.get('compatible', False), result.get('issues', [])
            except Exception as e:
                print(f"Error validating API compatibility: {{e}}")
                return False, [f"Validation service unavailable: {{e}}"]
        """
```

### Complete Workflow Integration
```python
# complete-database-workflow.py
class CompleteDatabaseWorkflow:
    def __init__(self):
        self.configs = {
            'api': self.load_api_config(),           # From /api-scaffold
            'testing': self.load_test_config(),      # From /test-harness
            'security': self.load_security_config(), # From /security-scan
            'docker': self.load_docker_config(),     # From /docker-optimize
            'k8s': self.load_k8s_config(),          # From /k8s-manifest
            'frontend': self.load_frontend_config(), # From /frontend-optimize
            'database': self.load_db_config()        # From /db-migrate
        }
    
    async def execute_complete_workflow(self):
        console.log("🚀 Starting complete database migration workflow...")
        
        # 1. Pre-migration Security Scan
        security_scan = await self.run_security_scan()
        console.log("✅ Database security scan completed")
        
        # 2. API Compatibility Check
        api_compatibility = await self.check_api_compatibility()
        console.log("✅ API compatibility verified")
        
        # 3. Container-based Migration Testing
        container_tests = await self.run_container_tests()
        console.log("✅ Container-based migration tests passed")
        
        # 4. Production Migration with Monitoring
        migration_result = await self.run_production_migration()
        console.log("✅ Production migration completed")
        
        # 5. Frontend Cache Invalidation
        cache_invalidation = await self.invalidate_frontend_caches()
        console.log("✅ Frontend caches invalidated")
        
        # 6. Kubernetes Deployment Update
        k8s_deployment = await self.update_k8s_deployment()
        console.log("✅ Kubernetes deployment updated")
        
        # 7. Post-migration Testing Pipeline
        post_migration_tests = await self.run_post_migration_tests()
        console.log("✅ Post-migration tests completed")
        
        return {
            'status': 'success',
            'workflow_id': self.generate_workflow_id(),
            'components': {
                security_scan,
                api_compatibility,
                container_tests,
                migration_result,
                cache_invalidation,
                k8s_deployment,
                post_migration_tests
            },
            'migration_summary': {
                'zero_downtime': True,
                'rollback_plan': 'available',
                'performance_impact': 'minimal',
                'security_validated': True
            }
        }
```

This integrated database migration workflow ensures that database changes are coordinated across all layers of the application stack, from API compatibility to frontend cache invalidation, creating a comprehensive database-first development pipeline that maintains data integrity and system reliability.

Focus on enterprise-grade migrations with zero-downtime deployments, comprehensive monitoring, and platform-agnostic strategies for modern polyglot persistence architectures.