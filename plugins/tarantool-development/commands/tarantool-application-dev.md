# Tarantool Application Development

Develop complete Tarantool applications with Lua stored procedures, API endpoints, and business logic:

[Extended thinking: This command orchestrates end-to-end Tarantool application development including data schema, Lua business logic, stored procedures, triggers, HTTP API handlers, testing, and deployment. It covers application structure, API design, error handling, performance optimization, and production deployment considerations.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Application Type
- **stateless-api**: REST API service
- **stateful-service**: Stateful application with Lua logic
- **cartridge-app**: Multi-role Cartridge application
- **data-processor**: Data processing and ETL
- **real-time-analytics**: Real-time analytics engine

### Framework
- **vanilla**: Pure Tarantool with HTTP module
- **cartridge**: Cartridge framework with roles
- **myapp-framework**: Custom framework

## Phase 1: Architecture Design

1. **Application Architecture**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Design Tarantool application architecture for: $ARGUMENTS. Type: $APP_TYPE. Define application structure, Lua modules, API endpoints, data flow, error handling strategy. Design for scalability and maintainability."
   - Expected output: Architecture design with diagrams

2. **Data Model Definition**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Define data model for: $ARGUMENTS. Using architecture: [include design]. Create spaces, indexes, and relationships. Define data types and constraints. Plan for future growth."
   - Expected output: Complete data model specification

## Phase 2: Implementation

3. **Core Lua Implementation**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Implement core Lua code for: $ARGUMENTS. Create modules for business logic. Implement stored procedures. Add error handling and validation. Follow best practices for transactions and consistency."
   - Expected output: Complete Lua implementation with modules

4. **Stored Procedures & Triggers**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Implement stored procedures and triggers for: $ARGUMENTS. Create ACID transactions. Implement audit triggers if needed. Add data validation. Handle edge cases and errors."
   - Expected output: Stored procedures and trigger code

5. **API Implementation**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Build REST API for: $ARGUMENTS. Create HTTP endpoints for CRUD operations. Implement error handling. Add input validation. Design response formats. Document API endpoints."
   - Expected output: Complete API implementation

## Phase 3: Testing & Deployment

6. **Testing Implementation**
   - Use Task tool with subagent_type="unit-testing::test-automator"
   - Prompt: "Create tests for Tarantool application: $ARGUMENTS. Write unit tests for Lua functions. Create integration tests for API. Test error cases. Create performance benchmarks."
   - Expected output: Test suite with examples

7. **Deployment Setup**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Configure deployment for: $ARGUMENTS. Setup development, staging, production environments. Configure Tarantool instances. Setup monitoring and logging. Create deployment guide."
   - Expected output: Deployment configuration and guide

## Execution Parameters

### Required
- **--app-name**: Application name and description
- **--app-type**: Application type (stateless-api|stateful-service|cartridge-app|data-processor|real-time-analytics)

### Optional
- **--framework**: Framework choice (vanilla|cartridge) - default: vanilla
- **--port**: HTTP API port - default: 8080
- **--enable-monitoring**: Enable metrics collection (true|false) - default: true
- **--enable-logging**: Enable structured logging (true|false) - default: true

## Success Criteria

- Complete application code
- Stored procedures and triggers
- REST API fully functional
- Test suite passing
- Performance meets targets
- Documentation complete
- Ready for deployment

Tarantool application development for: $ARGUMENTS
