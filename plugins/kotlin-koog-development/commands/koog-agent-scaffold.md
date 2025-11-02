---
name: koog-agent-scaffold
description: Interactive scaffolding command for creating new Koog AI agents in Kotlin. Generates project structure, boilerplate code, tests, and configuration. Use to quickly bootstrap new agent projects with best practices built-in.
---

# Koog Agent Scaffolding Command

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

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

## Build Configuration

The generated `build.gradle.kts` includes:

```kotlin
repositories {
    mavenCentral()
    maven {
        url = uri("https://repo.jetbrains.space/kotlin/p/kotlin/dev")
    }
}

dependencies {
    // Koog AI Agents Framework (0.5.2)
    implementation("ai.koog:koog-agents:0.5.2")

    // Kotlin standard library
    implementation("org.jetbrains.kotlin:kotlin-stdlib")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core")

    // Logging
    implementation("ch.qos.logback:logback-classic:1.4.11")

    // Optional framework integrations
    // Uncomment as needed:
    // implementation("org.springframework.boot:spring-boot-starter")
    // implementation("io.ktor:ktor-server-core")

    // Testing dependencies
    testImplementation("org.junit.jupiter:junit-jupiter:5.9.2")
    testImplementation("io.mockk:mockk:1.13.5")
}

kotlin {
    jvmToolchain(17)
}
```

**Key Points:**
- JetBrains Maven repository added for Koog framework
- Koog Agents version 0.5.2 is the latest stable release
- Java 17 JVM target for modern Kotlin features
- MockK for testing with mocked tools

## Generated Code Examples

### Basic Agent Scaffold
```kotlin
package com.example.agents

import ai.koog.agent

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

### Using the Prompt API with Multimodal Content
```kotlin
val executor = SingleProviderPromptExecutor(
    client = OpenAiLLMClient(modelId = "gpt-4-vision"),
    retryPolicy = RetryPolicy.PRODUCTION
)

val result = executor.executeStructured<Result> {
    systemMessage("Analyze the provided content")

    userMessage {
        text("What's important in this image?")
        attachment(ImageAttachment(url = "https://example.com/image.jpg"))
        attachment(DocumentAttachment(path = "/path/to/pdf"))
    }

    timeout = 30.seconds
}
```

### Adding Agent Event Monitoring
```kotlin
class ProductionEventProcessor : FeatureMessageProcessor {
    override fun process(message: FeatureMessage) {
        when (message) {
            is NodeExecutionEvent -> metrics.recordNodeExecution(message.nodeId)
            is ToolCallEvent -> log.info("Tool: ${message.toolName}")
            is AgentErrorEvent -> alerting.sendAlert(message.error)
        }
    }
}

agent("monitored") {
    addFeatureMessageProcessor(ProductionEventProcessor())
}
```

### Implementing Parallel Node Execution
```kotlin
agent("parallel_analysis") {
    strategy {
        node("fetch_parallel") {
            // Execute multiple tools concurrently
            parallel(
                listOf(
                    nodeExecuteTool("fetch_user_data"),
                    nodeExecuteTool("fetch_analytics"),
                    nodeExecuteTool("fetch_recommendations")
                ),
                mergeStrategy = fold { results ->
                    combineResults(results)
                }
            )
        }
    }
}
```

### Using Typed Data Storage Between Nodes
```kotlin
// Define typed keys
val sessionDataKey = createStorageKey<SessionData>("session")
val analysisKey = createStorageKey<Analysis>("analysis_result")

agent("data_flow_agent") {
    strategy {
        node("init") {
            action {
                storage.set(sessionDataKey, loadSession(input.sessionId))
            }
        }

        node("analyze") {
            action {
                val session = storage.getValue(sessionDataKey)
                val analysis = performAnalysis(session)
                storage.set(analysisKey, analysis)
            }
        }

        node("respond") {
            action {
                val analysis = storage.getValue(analysisKey)
                format(analysis)
            }
        }
    }
}
```

### Implementing History Compression
```kotlin
agent("conversation_agent") {
    strategy {
        node("respond") {
            nodeLLMRequest(instruction = "Respond helpfully")
        }

        // Auto-compress when context grows
        node("compress_if_long") {
            nodeLLMCompressHistory(
                strategy = Chunked(chunkSize = 15),
                onlyIf = { messages.size > 40 }
            )
        }

        edge(node("respond") onAssistantMessage to node("compress_if_long"))
    }
}
```

### Adding Content Moderation
```kotlin
agent("safe_agent") {
    val moderator = OpenAiModerator()

    strategy {
        node("check_input") {
            action {
                val modResult = moderator.moderate(input)
                if (modResult.isHarmful) {
                    throw SecurityException("Input rejected: ${modResult.flaggedCategories}")
                }
            }
        }

        node("generate") {
            nodeLLMRequest(instruction = "Generate helpful response")
        }
    }
}
```

### Creating Structured Output Requests
```kotlin
@Serializable
data class ExtractionResult(
    @LLMDescription("Extracted entities")
    val entities: List<String>,

    @LLMDescription("Sentiment: positive, neutral, negative")
    val sentiment: String,

    @LLMDescription("Confidence score 0.0-1.0")
    val confidence: Double
)

agent("extractor") {
    val session = agent.createWriteSession()

    val result = session.requestLLMStructured<ExtractionResult>(
        prompt = "Extract information from text",
        retryCount = 2 // Auto-correct with LLM
    )
}
```

### Integrating Model Context Protocol
```kotlin
// Connect to MCP servers for standardized tools
val mcpRegistry = McpToolRegistryProvider(
    transport = StdioTransport("/path/to/mcp-server"),
    parser = McpToolDescriptorParser()
).createRegistry()

agent("mcp_agent") {
    tools = mcpRegistry // All MCP tools available
}
```

### Working with Embeddings
```kotlin
// Local embeddings with Ollama
val embedder = OllamaEmbeddings(model = NOMIC_EMBED_TEXT)

agent("semantic_search") {
    val codeEmbedding = embedder.embed(userCode)
    val queryEmbedding = embedder.embed(userQuery)

    val similarity = cosineSimilarity(codeEmbedding, queryEmbedding)
    // Use similarity score for ranking
}
```

### Multi-Provider Model Selection
```kotlin
// Define capabilities-based model selection
val models = listOf(
    LLModel(
        provider = OpenAI,
        modelId = "gpt-4-turbo",
        capabilities = listOf(Vision, Tools, JsonSchema),
        contextLength = 128000
    ),
    LLModel(
        provider = Anthropic,
        modelId = "claude-3-sonnet",
        capabilities = listOf(Vision, Tools, CacheControl),
        contextLength = 200000
    )
)

// Select model dynamically
val bestModel = models.filter { model ->
    model.supports(Vision) && model.contextLength >= 100000
}.maxByOrNull { it.contextLength }
```

### Adding Comprehensive Observability
```kotlin
agent("production_agent") {
    // OpenTelemetry tracing
    features.add(OpenTelemetryTracing())

    // Agent memory and snapshots
    features.add(AgentMemory(persistenceProvider = SqlPersistence()))
    features.add(AgentSnapshots())

    // Event logging
    features.add(EventLogger())

    // Debug support
    features.add(DebuggerSupport())
}
```

## Troubleshooting

**Q: Build fails with "Cannot resolve symbol 'ai.koog'"**
A: Ensure you have the JetBrains Maven repository configured in `build.gradle.kts`:
```kotlin
maven {
    url = uri("https://repo.jetbrains.space/kotlin/p/kotlin/dev")
}
```

**Q: Build fails with "Dependency not found: ai.koog:koog-agents:0.5.2"**
A: Make sure the repository URL is correct and reachable. Verify your network connection. You can also try adding the mavenCentral() repository as a fallback.

**Q: Agent doesn't recognize my tool**
A: Verify the tool is defined within the `agent()` DSL block and follows proper naming conventions.

**Q: Tests fail with null pointer**
A: Check mockk setup and @MockkBean annotations for Spring integration. Ensure mocks are properly initialized before test execution.

**Q: Import error: dev.koog.agent not found**
A: Update your imports from `dev.koog.agent` to `ai.koog.agent`. The old namespace is deprecated.
