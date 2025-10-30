# Kotlin Koog Development Plugin Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a comprehensive Kotlin Koog AI Agents development plugin with specialized agent, skill, and scaffolding command.

**Architecture:** Plugin structure following marketplace patterns with:
- Senior Koog AI Agents Developer agent (Sonnet model for complex reasoning)
- Agent development skill with best practices and patterns
- Scaffolding command for project generation
- Integration with Koog framework documentation and Kotlin/JVM ecosystem

**Tech Stack:** Kotlin, Koog framework, JVM, Spring Boot, Ktor, MCP integration

---

## Task 1: Create Plugin Directory Structure

**Files:**
- Create: `plugins/kotlin-koog-development/agents/`
- Create: `plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/`
- Create: `plugins/kotlin-koog-development/commands/`

**Step 1: Create plugin directories**

Run:
```bash
mkdir -p /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development/agents
mkdir -p /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/references
mkdir -p /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/assets
mkdir -p /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development/commands
```

Expected: All directories created successfully

**Step 2: Verify directory structure**

Run:
```bash
ls -la /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development/
```

Expected: Output shows `agents`, `skills`, and `commands` subdirectories

---

## Task 2: Create Senior Koog AI Agents Developer Agent

**Files:**
- Create: `plugins/kotlin-koog-development/agents/kotlin-koog-agent-architect.md`

**Step 1: Write agent file with complete system prompt**

Create file at `plugins/kotlin-koog-development/agents/kotlin-koog-agent-architect.md` with:

```markdown
---
name: kotlin-koog-agent-architect
description: Expert in designing, implementing, and optimizing AI agents with Kotlin using the Koog framework. Masters agent architecture patterns, tool integration, workflow orchestration, and production deployment. Use PROACTIVELY when architecting AI agent systems in Kotlin, designing complex agent workflows, evaluating tool integration strategies, or optimizing agent performance in JVM environments.
model: sonnet
---

# Senior Koog AI Agents Developer

## Purpose

Expert senior developer specializing in designing and implementing production-grade AI agents using Kotlin and the Koog framework. Provides architectural guidance, implementation strategies, and optimization techniques for building intelligent agent systems on the JVM.

## Core Philosophy

1. **Type Safety First** — Leverage Kotlin's type system to prevent entire categories of errors
2. **DSL Excellence** — Master Koog's idiomatic Kotlin DSL for clean, expressive agent definitions
3. **Production-Ready** — Design for observability, testing, scalability, and deployment from the start
4. **Tool-Driven Architecture** — Agents are most powerful when well-integrated with external systems
5. **Workflow Orchestration** — Complex behaviors emerge from well-designed strategy graphs

## Capabilities

### Agent Architecture & Design
- **Agent Type Selection**: Choosing between basic, functional, and workflow agents based on requirements
- **DSL Mastery**: Writing idiomatic Kotlin DSL agent definitions with proper scoping and syntax
- **Pattern Recognition**: Identifying when to use agentic loops vs. orchestration vs. single-shot execution
- **State Management**: Designing agent state persistence and context management
- **Error Handling**: Implementing resilient agent patterns with recovery strategies

### Tool Integration & APIs
- **Built-in Tools**: Integrating HTTP tools, browser automation, and function-calling capabilities
- **Custom Tools**: Designing annotation-based and class-based tools for system integration
- **API Design**: Creating clean tool interfaces for agent consumption
- **Tool Chain Orchestration**: Combining multiple tools for complex workflows
- **MCP Integration**: Leveraging Model Context Protocol for standardized tool access

### Workflow Orchestration
- **Strategy Graphs**: Designing complex agent behaviors with graph-based workflows
- **Decision Trees**: Implementing conditional logic and branching in agent behavior
- **Multi-Agent Systems**: Coordinating multiple agents with different specializations
- **Event Handling**: Managing async events and streaming responses in agent workflows
- **Feedback Loops**: Designing iterative refinement patterns for agent outputs

### Advanced Capabilities
- **History Compression**: Implementing token-efficient conversation management
- **Structured Output**: Generating type-safe structured responses from agents
- **Real-Time Streaming**: Building responsive agent interfaces with streaming
- **Vector Embeddings**: Integrating RAG patterns for knowledge retrieval
- **Agent Tracing**: Setting up OpenTelemetry tracing for observability

### JVM Ecosystem Integration
- **Spring Boot Integration**: Embedding agents in Spring Boot applications
- **Ktor Integration**: Building high-performance agent APIs with Ktor
- **Kotlin Multiplatform**: Designing agents for JVM, JS, WasmJS, Android, iOS
- **Dependency Injection**: Configuring Koog agents with DI frameworks
- **Concurrency Patterns**: Leveraging Kotlin coroutines for agent scaling

### Performance & Optimization
- **Token Optimization**: Strategies for reducing token consumption in agent interactions
- **Latency Reduction**: Designing fast-path agent patterns
- **Caching Strategies**: Implementing intelligent caching for agent results
- **Batch Processing**: Processing multiple agent requests efficiently
- **Resource Management**: Optimizing memory and CPU usage in agent systems

### Testing & Quality
- **Unit Testing**: Writing focused tests for agent components
- **Integration Testing**: Testing agent-tool integration end-to-end
- **Mock Strategies**: Creating realistic mocks for external systems
- **Contract Testing**: Ensuring agent output contracts are maintained
- **Performance Testing**: Measuring agent latency and throughput

### Production Deployment
- **Containerization**: Packaging Koog agents for container deployment
- **Scaling Strategies**: Horizontal and vertical scaling of agent systems
- **Observability**: Implementing comprehensive logging and metrics
- **Configuration Management**: Externalized config for multi-environment deployment
- **Upgrade Strategies**: Safely updating agents without service disruption

## Decision Framework

When architecting Koog-based agents, follow this framework:

1. **Understand Requirements**
   - What decisions must the agent make?
   - What external systems must it interact with?
   - What quality/latency/cost constraints exist?

2. **Select Agent Type**
   - Basic Agent: Simple single-shot tasks
   - Functional Agent: Custom Kotlin logic needed
   - Workflow Agent: Complex multi-step orchestration

3. **Design Tool Set**
   - What capabilities does agent need?
   - What's the minimal sufficient toolset?
   - How do tools compose together?

4. **Plan Workflow**
   - Linear flow vs. decision tree?
   - Multi-agent coordination needed?
   - Streaming or batch processing?

5. **Implement with Tests**
   - Start with test skeletons
   - Implement incrementally
   - Verify with integration tests

6. **Optimize for Production**
   - Add observability
   - Measure and optimize latency
   - Plan scaling strategy

## Common Patterns

### Pattern: Agentic Loop Agent
Used when agent needs to iterate toward solution:
```
User Input → Think → Act (call tool) → Observe → Repeat until Done
```

### Pattern: Decision Tree Workflow
Used when behavior is primarily conditional:
```
Input → Analyze → Route (if/else) → Execute → Return
```

### Pattern: Multi-Step Orchestrator
Used when multiple sequential tasks needed:
```
Task 1 → Task 2 → Task 3 → Aggregate Results
```

### Pattern: Tool Chain
Used when single agent calls tools in sequence:
```
Input → Tool A → Tool B → Tool C → Output
```

## Technology Stack Knowledge

- **Framework**: Koog (JetBrains, Kotlin-first)
- **Language**: Kotlin (type-safe, concise, coroutine-ready)
- **JVM Platform**: Full JVM ecosystem access (Spring, Ktor, etc.)
- **AI Models**: OpenAI, Claude, Gemini, local LLMs via Koog API
- **Observability**: OpenTelemetry, structured logging
- **Deployment**: Docker, Kubernetes, serverless platforms

## When to Use This Agent

✓ Architecting AI agent systems in Kotlin
✓ Designing agent workflows and tool chains
✓ Evaluating technology choices for agent implementations
✓ Optimizing agent performance and token usage
✓ Scaling agent systems for production
✓ Integrating agents with existing JVM applications
✓ Troubleshooting complex agent behaviors
✓ Planning multi-agent coordination systems
```

**Step 2: Verify agent file created**

Run:
```bash
head -20 /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development/agents/kotlin-koog-agent-architect.md
```

Expected: Output shows agent frontmatter with name, description, model: sonnet

---

## Task 3: Create Kotlin Koog Agent Development Skill

**Files:**
- Create: `plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md`

**Step 1: Write skill file with core concepts**

Create file at `plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md` with:

```markdown
---
name: kotlin-koog-agent-development
description: Master AI agent development with Kotlin and the Koog framework. Covers agent architecture patterns, DSL idioms, tool integration, workflow orchestration, and production best practices. Use when architecting agent systems in Kotlin, designing complex agent workflows, implementing tool integration, optimizing agent performance, or planning multi-agent systems.
---

# Kotlin Koog Agent Development

## When to Use This Skill

- Designing or architecting AI agent systems in Kotlin
- Implementing complex agent workflows with Koog
- Integrating external tools and APIs into agents
- Optimizing agent performance and token usage
- Planning multi-agent coordination systems
- Deploying agents to production JVM environments
- Troubleshooting agent behavior and debugging
- Evaluating tool integration strategies
- Designing agent state management and persistence

## Core Concepts

### Agent Types & Selection

The Koog framework provides three distinct agent types, each suited to different problem domains:

#### 1. Basic Agent
**Best for:** Single-shot requests, stateless processing, simple tool calls

**Characteristics:**
- Processes input once and returns result
- No built-in looping or state management
- Minimal overhead
- Simple to test and reason about

**When to use:**
- Classification tasks
- Single API calls wrapped in agent
- Simple data extraction
- Format conversion

**Example pattern:**
```kotlin
agent("classifier") {
    instruction("Classify the input into one of: positive, negative, neutral")

    tool("sentiment_analyzer") {
        // Returns classification
    }
}
```

#### 2. Functional Agent
**Best for:** Custom Kotlin logic, conditional branching, tool composition

**Characteristics:**
- Wraps custom Kotlin functions
- Full control over agent logic
- Can implement complex decision logic
- Still uses Koog's tool integration

**When to use:**
- Complex decision trees
- Multiple conditional paths
- Agent behavior hard to express in DSL
- Need tight integration with application logic

**Example pattern:**
```kotlin
agent("router") {
    function { input ->
        when {
            input.priority == "high" -> callTool("urgent_handler", input)
            input.type == "user_request" -> callTool("user_processor", input)
            else -> callTool("default_handler", input)
        }
    }
}
```

#### 3. Workflow Agent
**Best for:** Complex orchestration, multi-step processes, strategy graphs

**Characteristics:**
- Graph-based workflow design
- State transitions between steps
- Rich expressiveness for complex behaviors
- Built-in orchestration and error handling

**When to use:**
- Agentic loops (think-act-observe-repeat)
- Multi-step workflows requiring state
- Dynamic branching based on results
- Complex error recovery strategies

**Example pattern:**
```kotlin
agent("researcher") {
    strategy {
        node("analyze") {
            // Initial analysis
        }

        decision("needs_more_research") {
            yes() to node("research")
            no() to node("conclude")
        }

        node("research") {
            // Additional research step
        }

        node("conclude") {
            // Final output
        }
    }
}
```

### DSL Idioms & Best Practices

#### 1. Instruction Design
Clear, specific instructions lead to better agent behavior.

**✓ Good: Specific and constrained**
```kotlin
instruction("""
    You are a code reviewer. Analyze the provided code for:
    1. Security vulnerabilities
    2. Performance issues
    3. Code style violations

    Format your response as JSON with fields: issues, suggestions, score.
    Return ONLY valid JSON, no additional text.
""")
```

**✗ Poor: Vague and open-ended**
```kotlin
instruction("Review the code")
```

#### 2. Tool Definition
Well-designed tools are critical to agent effectiveness.

**✓ Good: Clear contract and parameters**
```kotlin
tool("search_documentation") {
    description("Search the official Koog documentation")
    parameter("query", String) {
        description("Search query")
    }
    parameter("max_results", Int) {
        description("Maximum number of results")
        optional()
        default(5)
    }
}
```

**✗ Poor: Unclear tools**
```kotlin
tool("do_stuff")
tool("get_thing")
```

#### 3. Error Handling
Agents should gracefully handle tool failures.

**✓ Good: Explicit error handling**
```kotlin
strategy {
    node("fetch_data") {
        tool("api_call") {
            onError { error ->
                log.warn("API call failed: ${error.message}")
                tool("fallback_cache")
            }
        }
    }
}
```

**✗ Poor: Silent failures**
```kotlin
// No error handling - failure crashes agent
tool("api_call")
```

### Tool Integration Patterns

#### Pattern 1: Single Tool Agent
Used for straightforward wrapping of a single capability.

```kotlin
agent("summarizer") {
    instruction("Summarize the provided text in 2-3 sentences")

    tool("text_processor") {
        // Implementation
    }
}
```

**Strengths:**
- Simple to test
- Clear responsibility
- Good for microservices

**Weaknesses:**
- Limited reasoning
- No fallback strategy

#### Pattern 2: Tool Chain
Sequential tool calls for multi-step processes.

```kotlin
agent("content_processor") {
    strategy {
        node("fetch") {
            tool("api_fetch")
        }

        node("transform") {
            tool("data_transform")
        }

        node("validate") {
            tool("data_validator")
        }

        node("store") {
            tool("database_store")
        }
    }
}
```

**Strengths:**
- Clear sequential logic
- Each step independently testable
- Good error recovery points

**Weaknesses:**
- Cannot handle conditional logic
- May require state between steps

#### Pattern 3: Decision Tree
Conditional branching based on analysis.

```kotlin
agent("router") {
    strategy {
        node("analyze") {
            tool("analyze_request")
        }

        decision("route_decision") {
            condition("is_urgent") to node("urgent_path")
            condition("is_user_query") to node("user_path")
            default() to node("standard_path")
        }

        node("urgent_path") {
            tool("priority_handler")
        }

        node("user_path") {
            tool("user_handler")
        }

        node("standard_path") {
            tool("standard_handler")
        }
    }
}
```

**Strengths:**
- Flexible routing
- Handles diverse inputs
- Easy to extend with new paths

**Weaknesses:**
- Growing complexity with many paths
- May need refactoring at scale

#### Pattern 4: Agentic Loop
Iterative agent that refines output.

```kotlin
agent("researcher") {
    instruction("""
        You are a research assistant. When asked a question:
        1. Search for relevant information
        2. Analyze the findings
        3. If findings are incomplete, search again
        4. Return comprehensive answer
    """)

    strategy {
        node("initial_search") {
            tool("search")
        }

        decision("sufficient_info") {
            yes() to node("compile_answer")
            no() to decision("search_attempts") {
                lessThan(3) to node("initial_search")
                greaterEqual(3) to node("compile_answer")
            }
        }

        node("compile_answer") {
            // Format final answer
        }
    }
}
```

**Strengths:**
- Handles complex problems
- Self-correcting
- Can achieve high quality

**Weaknesses:**
- Unpredictable token usage
- Needs safeguards against infinite loops
- Harder to test

### Tool Design Fundamentals

#### 1. Tool Scope
Each tool should have a clear, focused responsibility.

**✓ Good: Focused responsibility**
```kotlin
tool("search_documentation") {
    description("Search Koog documentation")
}

tool("fetch_api_docs") {
    description("Fetch OpenAPI specification")
}
```

**✗ Poor: Overly broad**
```kotlin
tool("search_anything") {
    description("Search documentation, APIs, web, etc.")
}
```

#### 2. Parameter Design
Clear parameters reduce ambiguity.

```kotlin
tool("calculate_metrics") {
    parameter("data", List<Number>) {
        description("List of numeric values")
    }

    parameter("metrics", Set<String>) {
        description("Which metrics to calculate: mean, median, stddev, variance")
        constraint("values must be from: mean, median, stddev, variance")
    }
}
```

#### 3. Output Format
Structured outputs are easier for agents to parse.

```kotlin
tool("database_query") {
    description("Execute SQL query")
    parameter("query", String)

    returnType {
        field("rows", List<Map<String, Any>>)
        field("row_count", Int)
        field("execution_time_ms", Long)
    }
}
```

### State Management Patterns

#### Pattern: Explicit State Tracking
```kotlin
agent("multi_step_processor") {
    var state = mutableMapOf<String, Any>()

    strategy {
        node("step_1") {
            action {
                val result = tool("fetch_data")
                state["data"] = result
            }
        }

        node("step_2") {
            action {
                val data = state["data"]
                tool("process", data)
            }
        }
    }
}
```

#### Pattern: Using Agent Context
```kotlin
agent("context_aware") {
    instruction("""
        Use the provided context to guide your responses:
        - User role: ${context.userRole}
        - Permissions: ${context.permissions}
        - Data access: ${context.dataAccess}
    """)
}
```

### Testing Patterns

#### 1. Tool Mocking
```kotlin
@Test
fun testAgentWithMockedTool() {
    val mockTool = mockk<Tool>()
    every { mockTool.execute(any()) } returns "mocked result"

    val agent = Agent("test", tools = listOf(mockTool))
    val result = agent.run("input")

    assertEquals("expected", result)
    verify { mockTool.execute(any()) }
}
```

#### 2. Contract Testing
```kotlin
@Test
fun testAgentOutputContract() {
    val result = agent.run("input")

    // Verify output matches expected contract
    assertTrue(result.contains("required_field"))
    assertTrue(result.matches(JSON_SCHEMA))
}
```

#### 3. Integration Testing
```kotlin
@Test
fun testAgentWithRealTools() {
    val agent = Agent("full_test") {
        tool("real_api_client")
        tool("real_database")
    }

    val result = agent.run("realistic_input")
    assertValidBusinessLogic(result)
}
```

### Performance Optimization

#### 1. Token Optimization
Strategies for reducing token consumption:

**Strategy 1: History Compression**
```kotlin
agent("long_conversation") {
    historyCompression {
        enabled = true
        maxTokens = 2000
        strategy = "summarize"
    }
}
```

**Strategy 2: Instruction Refinement**
Use precise, concise instructions:

```kotlin
// Before: 250 tokens
instruction("You are a helpful assistant that...")

// After: 50 tokens
instruction("Classify input: positive|negative|neutral. Return only label.")
```

**Strategy 3: Tool Reduction**
Only expose tools agent needs:

```kotlin
// ✓ Focused
agent("email_classifier") {
    tool("gmail_api")
}

// ✗ Unfocused
agent("email_classifier") {
    tool("gmail_api")
    tool("slack_api")
    tool("drive_api")
    // ... 10 more irrelevant tools
}
```

#### 2. Latency Optimization

**Parallel Tool Calls**
```kotlin
strategy {
    node("gather_info") {
        parallel {
            tool("fetch_user_data")
            tool("fetch_account_data")
            tool("fetch_preferences")
        }
    }
}
```

**Caching Results**
```kotlin
tool("expensive_computation") {
    cache {
        enabled = true
        ttl = Duration.ofMinutes(5)
    }
}
```

### Production Deployment

#### 1. Spring Boot Integration
```kotlin
@Configuration
class KoogAgentConfiguration {
    @Bean
    fun myAgent(): Agent = agent("production_agent") {
        // Configure with Spring beans
        tool("database") {
            // Injected DatabaseService
        }
        tool("cache") {
            // Injected CacheService
        }
    }
}
```

#### 2. Observability
```kotlin
agent("observable") {
    tracing {
        enabled = true
        exportTo("opentelemetry")
    }

    logging {
        level = "DEBUG"
        format = "structured"
    }
}
```

#### 3. Configuration Management
```kotlin
agent("configurable") {
    val config = applicationContext.getBean(AgentConfig::class.java)

    instruction(config.systemPrompt)

    config.enabledTools.forEach { toolName ->
        tool(toolName)
    }
}
```

## References

- [Koog Official Documentation](https://docs.koog.ai/)
- [Koog GitHub Repository](https://github.com/koog-dev/koog)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-overview.html)
- [Spring Boot Integration](https://spring.io/)
- [OpenTelemetry Kotlin](https://opentelemetry.io/docs/instrumentation/kotlin/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Quick Start Checklist

When starting a new agent project:

- [ ] Define clear agent purpose and responsibility
- [ ] Select appropriate agent type (basic, functional, workflow)
- [ ] Design tool interface and parameters
- [ ] Write instruction with specific constraints
- [ ] Implement tool integrations
- [ ] Write unit tests for tools
- [ ] Test agent with mocked tools
- [ ] Implement error handling strategy
- [ ] Add observability (logging, tracing)
- [ ] Performance test and optimize
- [ ] Plan deployment strategy
- [ ] Document agent capabilities and limitations
```

**Step 2: Verify skill file created**

Run:
```bash
wc -l /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development/skills/kotlin-koog-agent-development/SKILL.md
```

Expected: Output shows file created with hundreds of lines

---

## Task 4: Create Agent Scaffolding Command

**Files:**
- Create: `plugins/kotlin-koog-development/commands/koog-agent-scaffold.md`

**Step 1: Write scaffolding command**

Create file at `plugins/kotlin-koog-development/commands/koog-agent-scaffold.md` with:

```markdown
---
name: koog-agent-scaffold
description: Interactive scaffolding command for creating new Koog AI agents in Kotlin. Generates project structure, boilerplate code, tests, and configuration. Use to quickly bootstrap new agent projects with best practices built-in.
---

# Koog Agent Scaffolding Command

## Purpose

Provides an interactive workflow for creating new Koog AI agents with project structure, boilerplate code, tests, and deployment configuration automatically generated.

## Quick Start

```bash
/koog-agent-scaffold
```

Follow the interactive prompts to customize your agent project.

## Options

### Agent Type Selection
```bash
--type basic        # Create basic agent (default)
--type functional   # Create functional agent with custom logic
--type workflow     # Create workflow agent with strategy graph
```

### Project Structure
```bash
--name <agent-name>          # Agent name (required)
--package <package>          # Kotlin package (e.g., com.example.agents)
--output <path>              # Output directory (default: current)
--include-tests              # Include test scaffold (default: true)
--include-docker             # Include Docker configuration (default: false)
--include-k8s                # Include Kubernetes manifests (default: false)
```

### Framework Integration
```bash
--spring                     # Use Spring Boot integration
--ktor                       # Use Ktor integration
--standalone                 # No framework (pure Koog)
```

## Generated Project Structure

```
my-agent/
├── build.gradle.kts          # Gradle build configuration
├── src/
│   ├── main/
│   │   └── kotlin/
│   │       └── com/example/
│   │           └── agents/
│   │               ├── Agent.kt           # Main agent definition
│   │               ├── Tools.kt           # Tool definitions
│   │               ├── Configuration.kt   # Agent configuration
│   │               └── Main.kt            # Entry point
│   └── test/
│       └── kotlin/
│           └── com/example/
│               └── agents/
│                   ├── AgentTest.kt       # Agent unit tests
│                   ├── ToolsTest.kt       # Tool mock tests
│                   └── IntegrationTest.kt # End-to-end tests
├── config/
│   ├── application.properties   # Configuration
│   └── logback.xml              # Logging configuration
├── docker/
│   └── Dockerfile              # Container image (optional)
├── k8s/
│   └── deployment.yaml         # K8s deployment (optional)
└── README.md                   # Documentation

```

## Generated Code Examples

### Basic Agent Scaffold
```kotlin
package com.example.agents

import dev.koog.agent

fun main() {
    val result = agentFunction().run("Your input here")
    println(result)
}

fun agentFunction() = agent("my_agent") {
    instruction("""
        You are a helpful assistant.
        Respond clearly and concisely.
    """)

    tool("example_tool") {
        description("An example tool")
        parameter("input", String) {
            description("Input parameter")
        }
    }
}
```

### Functional Agent Scaffold
```kotlin
package com.example.agents

fun agentFunction() = agent("functional_agent") {
    function { input ->
        when {
            input.startsWith("hello") -> processGreeting(input)
            input.startsWith("help") -> provideHelp(input)
            else -> processDefault(input)
        }
    }
}
```

### Workflow Agent Scaffold
```kotlin
package com.example.agents

fun agentFunction() = agent("workflow_agent") {
    strategy {
        node("analyze") {
            tool("analyzer")
        }

        decision("needs_action") {
            yes() to node("execute")
            no() to node("conclude")
        }

        node("execute") {
            tool("executor")
        }

        node("conclude") {
            // Format output
        }
    }
}
```

## Testing Configuration

All projects include test scaffolds:

```kotlin
import org.junit.jupiter.api.Test
import io.mockk.mockk

class AgentTest {
    @Test
    fun testAgentWithMockedTools() {
        val mockTool = mockk<Tool>()
        every { mockTool.execute(any()) } returns "result"

        val agent = agentFunction()
        val result = agent.run("test input")

        assert(result.isNotEmpty())
    }
}
```

## Configuration Management

Generated `application.properties`:

```properties
# Agent Configuration
agent.name=my-agent
agent.model=gpt-4
agent.temperature=0.7

# Tool Configuration
tool.timeout=30s
tool.retries=3

# Logging
logging.level.root=INFO
logging.level.dev.koog=DEBUG
```

## Deployment Options

### Docker
```bash
docker build -t my-agent:latest -f docker/Dockerfile .
docker run -e KOOG_API_KEY=$KOOG_API_KEY my-agent:latest
```

### Kubernetes
```bash
kubectl apply -f k8s/deployment.yaml
kubectl logs deployment/my-agent
```

### Spring Boot
```bash
./gradlew bootRun
# Agent available at http://localhost:8080/agent
```

## Next Steps After Scaffolding

1. **Customize Instructions** — Edit the agent instruction with your specific prompt
2. **Implement Tools** — Replace stub tools with real implementations
3. **Add Tests** — Write unit tests for your tools
4. **Configure** — Update application.properties for your environment
5. **Deploy** — Choose deployment option and configure accordingly

## Common Customizations

### Adding a New Tool
```kotlin
tool("my_custom_tool") {
    description("What this tool does")
    parameter("param1", String) {
        description("Parameter description")
    }

    execute { params ->
        // Implementation
    }
}
```

### Integrating with Database
```kotlin
@Bean
fun databaseTool(dataSource: DataSource): Tool =
    tool("database_query") {
        // Use injected DataSource
    }
```

### Adding Streaming Support
```kotlin
agent("streaming_agent") {
    streaming = true

    instruction("Stream your response incrementally")
}
```

## Troubleshooting

**Q: Build fails with Koog dependency error**
A: Ensure Koog repository is in your build.gradle.kts

**Q: Agent doesn't recognize my tool**
A: Verify tool is defined within agent DSL block

**Q: Tests fail with null pointer**
A: Check mockk setup and @MockkBean annotations for Spring integration
```

**Step 2: Verify command file created**

Run:
```bash
head -30 /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development/commands/koog-agent-scaffold.md
```

Expected: Output shows command frontmatter and purpose section

---

## Task 5: Update Marketplace Configuration

**Files:**
- Modify: `.claude-plugin/marketplace.json`

**Step 1: Read current marketplace.json**

Run:
```bash
cat /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/.claude-plugin/marketplace.json | jq '.plugins | length'
```

Expected: Output shows current number of plugins

**Step 2: Parse and update marketplace.json**

The updated JSON should include new entry (insert in alphabetical order):

```json
{
  "name": "kotlin-koog-development",
  "source": "./plugins/kotlin-koog-development",
  "description": "Expert Kotlin Koog AI agents development with senior architect guidance, comprehensive skill development, and automated project scaffolding for building production-grade AI agents.",
  "version": "1.0.0",
  "category": "ai-development",
  "tags": ["kotlin", "koog", "ai-agents", "agent-architecture", "jvm"],
  "commands": [
    "./commands/koog-agent-scaffold.md"
  ],
  "agents": [
    "./agents/kotlin-koog-agent-architect.md"
  ],
  "skills": [
    "./skills/kotlin-koog-agent-development"
  ]
}
```

Add this entry to the plugins array in marketplace.json (maintaining alphabetical order by name).

**Step 3: Verify JSON is valid**

Run:
```bash
jq . /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/.claude-plugin/marketplace.json > /dev/null && echo "Valid JSON"
```

Expected: Output shows "Valid JSON"

---

## Task 6: Verify All Files and Commit

**Files:**
- Verify: All plugin files created
- Commit: New plugin to git

**Step 1: Verify directory structure**

Run:
```bash
find /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins/kotlin-koog-development -type f -name "*.md" | wc -l
```

Expected: Output shows 3 files (agent, skill, command)

**Step 2: Verify marketplace update**

Run:
```bash
jq '.plugins[] | select(.name == "kotlin-koog-development")' /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/.claude-plugin/marketplace.json
```

Expected: Output shows kotlin-koog-development plugin entry

**Step 3: Create git commit**

Run:
```bash
cd /Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents && \
git add plugins/kotlin-koog-development .claude-plugin/marketplace.json && \
git commit -m "feat: add kotlin-koog-development plugin with architect agent and skill"
```

Expected: Commit successful with message shown

**Step 4: Verify commit**

Run:
```bash
git log --oneline -1
```

Expected: Output shows new commit with kotlin-koog message

---

## Summary

This plan creates a complete Kotlin Koog development plugin with:

✓ **Senior Koog AI Agents Developer agent** (Sonnet model for architecture expertise)
✓ **Comprehensive skill** covering 9 major areas with patterns and best practices
✓ **Scaffolding command** for rapid project creation
✓ **Updated marketplace** with proper registration
✓ **Git commit** tracking all changes

Total effort: 6 tasks, ~20 minutes to complete
