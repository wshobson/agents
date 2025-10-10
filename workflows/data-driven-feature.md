---
model: claude-sonnet-4-5-20250929
---

Build data-driven features with integrated pipelines and ML capabilities using specialized agents:

[Extended thinking: This workflow orchestrates data scientists, data engineers, backend architects, and AI engineers to build features that leverage data pipelines, analytics, and machine learning. Each agent contributes their expertise to create a complete data-driven solution.]

## Phase 1: Data Analysis and Design

### 1. Data Requirements Analysis
- Use Task tool with subagent_type="data-scientist"
- Prompt: "Analyze data requirements for: $ARGUMENTS. Identify data sources, required transformations, analytics needs, and potential ML opportunities."
- Output: Data analysis report, feature engineering requirements, ML feasibility

### 2. Data Pipeline Architecture
- Use Task tool with subagent_type="data-engineer"
- Prompt: "Design data pipeline architecture for: $ARGUMENTS. Include ETL/ELT processes, data storage, streaming requirements, and integration with existing systems based on data scientist's analysis."
- Output: Pipeline architecture, technology stack, data flow diagrams

## Phase 2: Backend Integration

### 3. API and Service Design
- Use Task tool with subagent_type="backend-architect"
- Prompt: "Design backend services to support data-driven feature: $ARGUMENTS. Include APIs for data ingestion, analytics endpoints, and ML model serving based on pipeline architecture."
- Output: Service architecture, API contracts, integration patterns

### 4. Database and Storage Design
- Use Task tool with subagent_type="database-optimizer"
- Prompt: "Design optimal database schema and storage strategy for: $ARGUMENTS. Consider both transactional and analytical workloads, time-series data, and ML feature stores."
- Output: Database schemas, indexing strategies, storage recommendations

## Phase 3: ML and AI Implementation

### 5. ML Pipeline Development
- Use Task tool with subagent_type="ml-engineer"
- Prompt: "Implement ML pipeline for: $ARGUMENTS. Include feature engineering, model training, validation, and deployment based on data scientist's requirements."
- Output: ML pipeline code, model artifacts, deployment strategy

### 6. AI Integration
- Use Task tool with subagent_type="ai-engineer"
- Prompt: "Build AI-powered features for: $ARGUMENTS. Integrate LLMs, implement RAG if needed, and create intelligent automation based on ML engineer's models."
- Output: AI integration code, prompt engineering, RAG implementation

## Phase 4: Implementation and Optimization

### 7. Data Pipeline Implementation
- Use Task tool with subagent_type="data-engineer"
- Prompt: "Implement production data pipelines for: $ARGUMENTS. Include real-time streaming, batch processing, and data quality monitoring based on all previous designs."
- Output: Pipeline implementation, monitoring setup, data quality checks

### 8. Performance Optimization
- Use Task tool with subagent_type="performance-engineer"
- Prompt: "Optimize data processing and model serving performance for: $ARGUMENTS. Focus on query optimization, caching strategies, and model inference speed."
- Output: Performance improvements, caching layers, optimization report

## Phase 5: Testing and Deployment

### 9. Comprehensive Testing
- Use Task tool with subagent_type="test-automator"
- Prompt: "Create test suites for data pipelines and ML components: $ARGUMENTS. Include data validation tests, model performance tests, and integration tests."
- Output: Test suites, data quality tests, ML monitoring tests

### 10. Production Deployment
- Use Task tool with subagent_type="deployment-engineer"
- Prompt: "Deploy data-driven feature to production: $ARGUMENTS. Include pipeline orchestration, model deployment, monitoring, and rollback strategies."
- Output: Deployment configurations, monitoring dashboards, operational runbooks

## Coordination Notes
- Data flow and requirements cascade from data scientists to engineers
- ML models must integrate seamlessly with backend services
- Performance considerations apply to both data processing and model serving
- Maintain data lineage and versioning throughout the pipeline

Data-driven feature to build: $ARGUMENTS