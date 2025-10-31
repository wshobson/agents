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
import ai.koog.agent

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
import ai.koog.agent

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

## Setup & Dependencies

### Gradle Configuration
```kotlin
repositories {
    mavenCentral()
    maven {
        url = uri("https://repo.jetbrains.space/kotlin/p/kotlin/dev")
    }
}

dependencies {
    // Koog AI Agents Framework
    implementation("ai.koog:koog-agents:0.5.2")

    // Kotlin and Coroutines
    implementation("org.jetbrains.kotlin:kotlin-stdlib")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core")

    // Optional: Spring Boot Integration
    implementation("org.springframework.boot:spring-boot-starter")

    // Optional: Ktor Integration
    implementation("io.ktor:ktor-server-core")

    // Testing
    testImplementation("org.junit.jupiter:junit-jupiter:5.9.2")
    testImplementation("io.mockk:mockk:1.13.5")
}
```

### Kotlin Compiler Settings
```kotlin
kotlin {
    jvmToolchain(17)
}
```

## References

- [Koog Official Documentation](https://docs.koog.ai/)
- [Koog GitHub Repository](https://github.com/JetBrains/koog)
- [Koog Maven Repository](https://repo.jetbrains.space/kotlin/p/kotlin/dev)
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
