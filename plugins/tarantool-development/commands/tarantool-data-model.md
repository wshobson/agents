# Tarantool Data Model Design

Design and implement optimized data models for Tarantool applications:

[Extended thinking: This command guides users through designing efficient Tarantool data models, including space definitions, index strategies, data types, and storage engine selection. It covers denormalization patterns, sharding key selection, and optimization for specific query patterns. The workflow includes analysis of access patterns, schema design, index optimization, and validation against performance requirements.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Data Model Type
- **transactional**: OLTP with frequent updates
- **analytical**: OLAP with read-heavy patterns
- **time-series**: Time-based data with retention policies
- **cache**: High-speed caching layer
- **hybrid**: Mixed read/write patterns

### Storage Engine
- **memtx**: In-memory (ultra-fast, RAM-limited)
- **vinyl**: Persistent LSM-tree (slower, unlimited)
- **mixed**: Different spaces on different engines

### Scale
- **small**: < 100GB data
- **medium**: 100GB - 1TB
- **large**: 1TB - 10TB
- **massive**: > 10TB (requires sharding)

## Phase 1: Analysis & Design

1. **Workload Analysis**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Analyze Tarantool data model requirements: $ARGUMENTS. Determine: primary access patterns, read/write ratio, data size estimates, latency requirements, consistency needs. Create workload profile with query patterns and performance targets."
   - Expected output: Workload analysis document

2. **Data Model Design**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Design Tarantool data model for: $ARGUMENTS. Based on workload analysis: [include analysis]. Define spaces with appropriate fields and types. Design for storage engine: $STORAGE_ENGINE. Create schema with normalized and denormalized options. Document trade-offs."
   - Expected output: Data model specification with schema

3. **Index Strategy**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Optimize indexing strategy for: $ARGUMENTS. For workload patterns: [include from analysis]. Create indexes for all filters and joins. Design composite indexes for multi-field queries. Analyze index trade-offs (speed vs storage). Estimate index sizes."
   - Expected output: Index configuration with performance analysis

## Phase 2: Implementation

4. **Schema Implementation**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Implement Tarantool schema for: $ARGUMENTS. Create complete Lua code for spaces and indexes using schema: [include design]. Add data type definitions. Configure storage engine parameters. Include migration procedures for schema changes."
   - Expected output: Complete schema implementation code

5. **Denormalization Planning**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Plan denormalization for: $ARGUMENTS. Based on query patterns: [include access patterns]. Identify data that should be denormalized. Design update triggers for maintaining denormalized data. Document consistency implications."
   - Expected output: Denormalization strategy with code

6. **Sharding Key Design**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Design sharding strategy for: $ARGUMENTS. If sharding is required. Select sharding key ensuring even distribution. Verify key uniqueness and cardinality. Design for growth. Document sharding trade-offs."
   - Expected output: Sharding key selection and distribution analysis

## Phase 3: Validation & Optimization

7. **Performance Validation**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Validate model performance for: $ARGUMENTS. Create benchmark queries for access patterns. Simulate expected load. Verify latency meets targets. Identify bottlenecks. Suggest optimization options."
   - Expected output: Performance validation report

8. **Generate Documentation**
   - Use Task tool with subagent_type="documentation-generation::docs-architect"
   - Prompt: "Generate data model documentation for: $ARGUMENTS. Include schema diagrams, space definitions, index explanation, query patterns, migration guide, troubleshooting tips."
   - Expected output: Complete data model documentation

## Execution Parameters

### Required
- **--app-name**: Application name and description
- **--data-type**: Data model type (transactional|analytical|time-series|cache|hybrid)
- **--estimated-size**: Estimated data size (small|medium|large|massive)

### Optional
- **--engine**: Storage engine (memtx|vinyl|mixed) - default: memtx
- **--sharding-required**: Enable sharding (true|false) - default: false
- **--consistency-level**: Read/write consistency (strong|eventual) - default: strong
- **--retention-period**: Data retention in days (for time-series)

## Success Criteria

- Schema designed for access patterns
- All indexes created and optimized
- Storage engine selected appropriately
- Latency targets achievable
- Growth planned for scale
- Documentation complete

Tarantool data model design for: $ARGUMENTS
