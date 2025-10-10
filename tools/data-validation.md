---
model: claude-sonnet-4-5-20250929
---

# Data Validation Pipeline

Create a comprehensive data validation system for: $ARGUMENTS

Implement validation including:

1. **Schema Validation**:
   - Pydantic models for structure
   - JSON Schema generation
   - Type checking and coercion
   - Nested object validation
   - Custom validators

2. **Data Quality Checks**:
   - Null/missing value handling
   - Outlier detection
   - Statistical validation
   - Business rule enforcement
   - Referential integrity

3. **Data Profiling**:
   - Automatic type inference
   - Distribution analysis
   - Cardinality checks
   - Pattern detection
   - Anomaly identification

4. **Validation Rules**:
   - Field-level constraints
   - Cross-field validation
   - Temporal consistency
   - Format validation (email, phone, etc.)
   - Custom business logic

5. **Error Handling**:
   - Detailed error messages
   - Error categorization
   - Partial validation support
   - Error recovery strategies
   - Validation reports

6. **Performance**:
   - Streaming validation
   - Batch processing
   - Parallel validation
   - Caching strategies
   - Incremental validation

7. **Integration**:
   - API endpoint validation
   - Database constraints
   - Message queue validation
   - File upload validation
   - Real-time validation

Include data quality metrics, monitoring dashboards, and alerting. Make it extensible for custom validation rules.
