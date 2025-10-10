---
model: claude-sonnet-4-5-20250929
---

# Machine Learning Pipeline

Design and implement a complete ML pipeline for: $ARGUMENTS

Create a production-ready pipeline including:

1. **Data Ingestion**:
   - Multiple data source connectors
   - Schema validation with Pydantic
   - Data versioning strategy
   - Incremental loading capabilities

2. **Feature Engineering**:
   - Feature transformation pipeline
   - Feature store integration
   - Statistical validation
   - Handling missing data and outliers

3. **Model Training**:
   - Experiment tracking (MLflow/W&B)
   - Hyperparameter optimization
   - Cross-validation strategy
   - Model versioning

4. **Model Evaluation**:
   - Comprehensive metrics
   - A/B testing framework
   - Bias detection
   - Performance monitoring

5. **Deployment**:
   - Model serving API
   - Batch/stream prediction
   - Model registry
   - Rollback capabilities

6. **Monitoring**:
   - Data drift detection
   - Model performance tracking
   - Alert system
   - Retraining triggers

Include error handling, logging, and make it cloud-agnostic. Use modern tools like DVC, MLflow, or similar. Ensure reproducibility and scalability.
