---
name: kotlin-koog-agent-development
description: Master AI agent development with JetBrains Koog framework (v0.5.2) in Kotlin. Comprehensive guide covering strategy graphs (similar to LangGraph), tool integration, ReAct/Chat patterns, RAG systems, structured output, history compression, testing, and production deployment. Use when building Kotlin AI agents with LangChain/LangGraph-style patterns, implementing complex workflows with nodes and edges, creating type-safe agent systems, or deploying production agents on JVM/multiplatform.
---

# Kotlin Koog Agent Development - Comprehensive Guide

## Language Support

This skill documentation adapts to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

## When to Use This Skill

- Building AI agents in Kotlin with graph-based workflows (similar to LangGraph)
- Implementing ReAct, Chat, or custom agent strategies
- Designing strategy graphs with nodes, edges, and conditional routing
- Creating tools (annotation-based or class-based) for agent integration
- Building RAG systems with embeddings and semantic search
- Implementing structured output with type-safe validation
- Optimizing token usage with history compression strategies
- Adding agent memory and persistence for stateful conversations
- Integrating with Spring Boot or Ktor applications
- Testing agents with mocked LLMs and tools
- Deploying production-ready agents with observability

## Framework Overview

**Koog** is JetBrains' official Kotlin framework for building AI agents. Version 0.5.2 is production-ready and available on Maven Central.

### Key Features
- **Multiplatform**: JVM, Android, iOS, JavaScript, WebAssembly
- **Type-Safe**: Kotlin's type system prevents runtime errors
- **Graph-Based Workflows**: Similar to LangGraph's node-edge architecture
- **Fault Tolerant**: Built-in retries, persistence, and state recovery
- **LLM Flexible**: Support for Google, OpenAI, Anthropic, DeepSeek, OpenRouter, Ollama, Bedrock
- **Enterprise Ready**: Spring Boot integration, OpenTelemetry tracing, agent memory

### Architecture Comparison

| Concept | LangChain/LangGraph | Koog Equivalent |
|---------|-------------------|-----------------|
| Conversational Agent | ConversationalAgent | Chat Strategy |
| ReAct Agent | ReActAgent | ReAct Strategy |
| LangGraph Custom Graph | StateGraph | Custom Strategy Graph |
| Chains | Sequential nodes | edge() connections |
| Tools | @tool decorator | @Tool annotation or Tool<> class |
| Memory | ConversationBufferMemory | AgentMemory with facts |
| Structured Output | Pydantic models | @Serializable data classes |
| RAG | VectorStore + retriever | Embeddings + AIAgentStorage |

---

## Core Concepts

### 1. Strategy Graphs (Similar to LangGraph)

Strategy graphs define agent workflows using **nodes** (operations) connected by **edges** (transitions).

#### Graph Structure
```
nodeStart → node1 → node2 → nodeFinish
```

#### Components
- **nodeStart**: Entry point (always present)
- **nodeFinish**: Exit point (always present)
- **Custom Nodes**: LLM requests, tool calls, data transformations
- **Edges**: Connections with conditions

#### Example: Simple Linear Graph
```kotlin
val strategy = customStrategy {
    val nodeAnalyze by nodeLLMRequest<String, String>("Analyze the input")
    val nodeProcess by nodeExecuteTool("process_data")
    val nodeFormat by nodeLLMRequest<String, String>("Format the result")

    edge(nodeStart forwardTo nodeAnalyze)
    edge(nodeAnalyze onAssistantMessage forwardTo nodeProcess)
    edge(nodeProcess forwardTo nodeFormat)
    edge(nodeFormat onAssistantMessage forwardTo nodeFinish)
}
```

### 2. Predefined Agent Strategies

#### Chat Strategy (Like LangChain's ConversationalAgent)
Conversational interface with tool calling.

```kotlin
val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "You are a helpful assistant.",
    llmModel = OpenAIModels.Chat.GPT4o,
    toolRegistry = ToolRegistry { tools(weatherTools) },
    strategy = chatAgentStrategy()
)

val result = agent.run("What's the weather in Tokyo?")
```

#### ReAct Strategy (Reasoning + Acting)
Multi-step problem solving with reasoning between actions.

```kotlin
val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "Reason step by step, then act.",
    llmModel = OpenAIModels.Chat.GPT4o,
    toolRegistry = ToolRegistry { tools(researchTools) },
    strategy = reActStrategy(reasoningInterval = 1)
)

val result = agent.run("Research the latest AI developments and summarize.")
```

**Parameters:**
- `reasoningInterval`: Number of actions between reasoning steps (default: 1)
- `name`: Strategy name (default: "re_act")

### 3. Custom Strategy Graphs

For complex workflows, design custom graphs with conditional logic.

#### Conditional Routing Example
```kotlin
val strategy = customStrategy {
    val nodeClassify by nodeLLMRequest<String, String>(
        "Classify the request: urgent, standard, or low-priority"
    )

    val nodeUrgent by nodeExecuteTool("handle_urgent")
    val nodeStandard by nodeExecuteTool("handle_standard")
    val nodeLowPriority by nodeExecuteTool("handle_low_priority")

    edge(nodeStart forwardTo nodeClassify)
    edge(nodeClassify onCondition { output.contains("urgent") } forwardTo nodeUrgent)
    edge(nodeClassify onCondition { output.contains("standard") } forwardTo nodeStandard)
    edge(nodeClassify onCondition { output.contains("low") } forwardTo nodeLowPriority)

    edge(nodeUrgent forwardTo nodeFinish)
    edge(nodeStandard forwardTo nodeFinish)
    edge(nodeLowPriority forwardTo nodeFinish)
}
```

#### Loop Example (ReAct-style)
```kotlin
val strategy = customStrategy {
    val nodeSearch by nodeExecuteTool("search")
    val nodeAnalyze by nodeLLMRequest<String, String>("Analyze the findings")

    val nodeCheckComplete by node<String, Boolean> { result ->
        result.contains("COMPLETE")
    }

    edge(nodeStart forwardTo nodeSearch)
    edge(nodeSearch forwardTo nodeAnalyze)
    edge(nodeAnalyze onAssistantMessage forwardTo nodeCheckComplete)

    // Loop back if not complete
    edge(nodeCheckComplete onCondition { !it } forwardTo nodeSearch)

    // Exit when complete
    edge(nodeCheckComplete onCondition { it } forwardTo nodeFinish)
}
```

---

## Predefined Nodes

### LLM Nodes

#### nodeLLMRequest
Standard LLM request with optional tool calling.

```kotlin
val nodeAsk by nodeLLMRequest<String, String>(
    instruction = "Answer the user's question",
    allowToolCall = true
)
```

#### nodeLLMRequestStructured
Type-safe structured output.

```kotlin
@Serializable
data class Summary(
    @LLMDescription("Main points") val points: List<String>,
    @LLMDescription("Confidence 0.0-1.0") val confidence: Double
)

val nodeSummarize by nodeLLMRequestStructured<String, Summary>(
    instruction = "Summarize the text",
    retryCount = 3
)
```

#### nodeLLMRequestStreaming
Streaming responses for real-time feedback.

```kotlin
val nodeStream by nodeLLMRequestStreaming<String, String>(
    instruction = "Generate a story",
    onChunk = { chunk -> print(chunk) }
)
```

#### nodeLLMCompressHistory
Reduce conversation history token usage.

```kotlin
val nodeCompress by nodeLLMCompressHistory<String>(
    strategy = WholeHistory(), // Options: WholeHistory, FromLastNMessages, Chunked, RetrieveFactsFromHistory
    onlyIf = { messages.size > 50 }
)
```

### Tool Nodes

#### nodeExecuteTool
Execute a single tool.

```kotlin
val nodeCall by nodeExecuteTool("calculator")
```

#### nodeExecuteMultipleTools
Execute multiple tools in sequence or parallel.

```kotlin
val nodeMulti by nodeExecuteMultipleTools(
    tools = listOf("fetch_user", "fetch_orders", "fetch_preferences"),
    parallel = true
)
```

### Utility Nodes

#### nodeAppendPrompt
Add messages to the conversation.

```kotlin
val nodeAddContext by nodeAppendPrompt {
    systemMessage("You are an expert in biology.")
    userMessage("Explain photosynthesis.")
}
```

#### nodeDoNothing
Pass-through node for graph structure.

```kotlin
val nodePlaceholder by nodeDoNothing()
```

---

## Edge Types and Conditions

### Basic Edge
```kotlin
edge(nodeA forwardTo nodeB)
```

### Conditional Edges

#### onCondition
General boolean condition.

```kotlin
edge(nodeA onCondition { result -> result.isValid() } forwardTo nodeB)
```

#### onToolCall
Matches when LLM calls a tool.

```kotlin
edge(nodeLLM onToolCall forwardTo nodeExecuteTool)
```

#### onAssistantMessage
Matches LLM text responses.

```kotlin
edge(nodeLLM onAssistantMessage forwardTo nodeProcess)
```

#### onMultipleToolCalls
Matches multiple tool invocations.

```kotlin
edge(nodeLLM onMultipleToolCalls forwardTo nodeExecuteMultipleTools)
```

#### onToolNotCalled
Matches when no tool is called.

```kotlin
edge(nodeLLM onToolNotCalled forwardTo nodeFinish)
```

### Transformed Edges
Transform data before passing to next node.

```kotlin
edge(nodeA transformed { result -> result.uppercase() } forwardTo nodeB)
```

---

## Tool Integration

### Annotation-Based Tools (JVM Only)

Simple, declarative tool definition.

```kotlin
@LLMDescription("Weather information tools")
class WeatherToolSet : ToolSet {

    @Tool
    @LLMDescription("Get current weather for a location")
    fun getWeather(
        @LLMDescription("City name and country (e.g., 'Tokyo, Japan')")
        location: String
    ): String {
        // Call weather API
        return "Weather in $location: Sunny, 22°C"
    }

    @Tool
    @LLMDescription("Get 7-day forecast")
    fun getForecast(
        @LLMDescription("City name")
        location: String,

        @LLMDescription("Number of days (1-7)")
        days: Int = 7
    ): String {
        // Call forecast API
        return "7-day forecast for $location: ..."
    }
}

// Register with agent
val weatherTools = WeatherToolSet()
val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "You provide weather information.",
    llmModel = OpenAIModels.Chat.GPT4o,
    toolRegistry = ToolRegistry {
        tools(weatherTools)
    }
)
```

### Class-Based Tools (Multiplatform)

More control and flexibility.

#### Simple Tool (Text Output)
```kotlin
@Serializable
data class CalculatorArgs(
    val a: Double,
    val b: Double,
    val operation: String // "add", "subtract", "multiply", "divide"
)

class CalculatorTool : SimpleTool<CalculatorArgs>() {
    override val argsSerializer = CalculatorArgs.serializer()

    override val descriptor = ToolDescriptor(
        name = "calculator",
        description = "Perform basic arithmetic operations",
        parameters = listOf(
            ToolParameter("a", "First number"),
            ToolParameter("b", "Second number"),
            ToolParameter("operation", "Operation: add, subtract, multiply, divide")
        )
    )

    override suspend fun doExecute(args: CalculatorArgs): String {
        val result = when (args.operation) {
            "add" -> args.a + args.b
            "subtract" -> args.a - args.b
            "multiply" -> args.a * args.b
            "divide" -> if (args.b != 0.0) args.a / args.b else Double.NaN
            else -> throw IllegalArgumentException("Unknown operation")
        }
        return "Result: $result"
    }
}
```

#### Advanced Tool (Structured Output)
```kotlin
@Serializable
data class SearchArgs(val query: String, val maxResults: Int = 10)

@Serializable
data class SearchResult(
    val title: String,
    val url: String,
    val snippet: String
)

class SearchTool : Tool<SearchArgs, List<SearchResult>>() {
    override val argsSerializer = SearchArgs.serializer()
    override val resultSerializer = ListSerializer(SearchResult.serializer())

    override val descriptor = ToolDescriptor(
        name = "search",
        description = "Search the web",
        parameters = listOf(
            ToolParameter("query", "Search query"),
            ToolParameter("maxResults", "Maximum number of results (default: 10)")
        )
    )

    override suspend fun execute(args: SearchArgs): List<SearchResult> {
        // Call search API
        return listOf(
            SearchResult("Result 1", "https://...", "..."),
            SearchResult("Result 2", "https://...", "...")
        )
    }
}
```

### Tool Registry

```kotlin
val toolRegistry = ToolRegistry {
    // Add annotation-based tools
    tools(weatherToolSet)

    // Add class-based tools
    tool(CalculatorTool())
    tool(SearchTool())

    // Add tools by name reference
    tool("database_query", DatabaseQueryTool())
}
```

---

## Structured Output (Type-Safe Responses)

### Basic Example
```kotlin
@Serializable
data class UserProfile(
    @LLMDescription("User's full name")
    val name: String,

    @LLMDescription("Age between 18 and 100")
    val age: Int,

    @LLMDescription("List of hobbies")
    val hobbies: List<String>,

    @LLMDescription("Email address (optional)")
    val email: String? = null
)

val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "Extract user profiles from text.",
    llmModel = OpenAIModels.Chat.GPT4o
)

val session = agent.createWriteSession()
val profile = session.requestLLMStructured<UserProfile>(
    prompt = "User: John Doe, 28 years old, enjoys hiking and photography.",
    retryCount = 3 // Auto-fix with LLM if validation fails
)

println("Name: ${profile.name}, Age: ${profile.age}")
```

### Complex Nested Structures
```kotlin
@Serializable
data class Address(
    val street: String,
    val city: String,
    val country: String
)

@Serializable
data class Company(
    @LLMDescription("Company name")
    val name: String,

    @LLMDescription("Company address")
    val address: Address,

    @LLMDescription("Number of employees")
    val employees: Int
)

@Serializable
data class BusinessProfile(
    @LLMDescription("List of companies")
    val companies: List<Company>,

    @LLMDescription("Total revenue in USD")
    val totalRevenue: Double
)
```

### Enums for Constrained Values
```kotlin
@Serializable
enum class Sentiment {
    POSITIVE, NEGATIVE, NEUTRAL
}

@Serializable
data class TextAnalysis(
    @LLMDescription("Overall sentiment")
    val sentiment: Sentiment,

    @LLMDescription("Confidence score 0.0-1.0")
    val confidence: Double,

    @LLMDescription("Key topics mentioned")
    val topics: List<String>
)
```

### Using in Strategy Graphs
```kotlin
val strategy = customStrategy {
    val nodeExtract by nodeLLMRequestStructured<String, UserProfile>(
        instruction = "Extract user profile",
        retryCount = 2
    )

    val nodeValidate by node<UserProfile, UserProfile> { profile ->
        require(profile.age in 18..100) { "Invalid age" }
        profile
    }

    edge(nodeStart forwardTo nodeExtract)
    edge(nodeExtract forwardTo nodeValidate)
    edge(nodeValidate forwardTo nodeFinish)
}
```

---

## History Compression (Token Optimization)

Long conversations consume many tokens. History compression reduces costs while maintaining context.

### Strategy 1: WholeHistory (TLDR All)
Compress entire conversation into a single summary.

```kotlin
val strategy = customStrategy {
    val nodeRespond by nodeLLMRequest<String, String>("Respond to user")

    val nodeCompress by nodeLLMCompressHistory<String>(
        strategy = WholeHistory(),
        onlyIf = { messages.size > 30 }
    )

    edge(nodeStart forwardTo nodeRespond)
    edge(nodeRespond onAssistantMessage forwardTo nodeCompress)
    edge(nodeCompress forwardTo nodeFinish)
}
```

### Strategy 2: FromLastNMessages (Keep Recent)
Compress only older messages, keep recent ones intact.

```kotlin
val nodeCompress by nodeLLMCompressHistory<String>(
    strategy = FromLastNMessages(n = 10), // Keep last 10 messages
    preserveMemory = true // Preserve AgentMemory facts
)
```

### Strategy 3: Chunked (Compress in Chunks)
Split history into chunks and compress each independently.

```kotlin
val nodeCompress by nodeLLMCompressHistory<String>(
    strategy = Chunked(chunkSize = 15)
)
```

### Strategy 4: RetrieveFactsFromHistory (Extract Specific Info)
Extract only relevant facts matching concepts.

```kotlin
val concepts = listOf(
    Concept(
        name = "user_id",
        description = "User's ID",
        factType = FactType.SINGLE
    ),
    Concept(
        name = "preferences",
        description = "User preferences",
        factType = FactType.MULTIPLE
    )
)

val nodeCompress by nodeLLMCompressHistory<String>(
    strategy = RetrieveFactsFromHistory(concepts = concepts)
)
```

---

## Agent Memory (Persistent Facts)

AgentMemory enables agents to remember information across conversations (like LangChain's ConversationBufferMemory).

### Core Concepts
- **Facts**: Individual pieces of information (SingleFact or MultipleFacts)
- **Concepts**: Categories for organizing facts
- **Subjects**: Entities facts attach to (User, Machine, or custom)
- **Scopes**: Relevance contexts (Agent, Feature, Product, CrossProduct)

### Setup
```kotlin
val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "You remember user preferences.",
    llmModel = OpenAIModels.Chat.GPT4o,
    features = listOf(
        AgentMemory(
            memoryProvider = SqlMemoryProvider(), // or InMemoryProvider, CustomProvider
            agentName = "customer-support",
            featureName = "user-context"
        )
    )
)
```

### Using Predefined Memory Nodes
```kotlin
val strategy = customStrategy {
    // Load facts
    val nodeLoadFacts by nodeLoadAllFactsFromMemory()

    // Process with facts in context
    val nodeRespond by nodeLLMRequest<String, String>(
        "Respond using remembered facts about the user"
    )

    // Automatically extract and save new facts
    val nodeSaveFacts by nodeExtractAndSaveFactsToMemory(
        concepts = listOf(
            Concept("preferences", "User preferences", FactType.MULTIPLE),
            Concept("user_id", "User ID", FactType.SINGLE)
        )
    )

    edge(nodeStart forwardTo nodeLoadFacts)
    edge(nodeLoadFacts forwardTo nodeRespond)
    edge(nodeRespond onAssistantMessage forwardTo nodeSaveFacts)
    edge(nodeSaveFacts forwardTo nodeFinish)
}
```

### Manual Fact Management
```kotlin
val session = agent.createWriteSession()

// Save a fact
val memory = session.features.first { it is AgentMemory } as AgentMemory
memory.saveFact(
    concept = "user_name",
    value = "John Doe",
    subject = Subject.User
)

// Load facts
val facts = memory.loadFacts(scope = Scope.Agent)
```

---

## Parallel Execution

### Parallel Node Execution
Run multiple nodes concurrently and merge results.

#### Merge Strategy: selectByMax
```kotlin
val strategy = customStrategy {
    val nodeMultiModel by node<String, String> { input ->
        parallel(
            listOf(
                nodeWithGPT4(input),
                nodeWithClaude(input),
                nodeWithGemini(input)
            ),
            mergeStrategy = selectByMax { response ->
                calculateQualityScore(response)
            }
        )
    }

    edge(nodeStart forwardTo nodeMultiModel)
    edge(nodeMultiModel forwardTo nodeFinish)
}
```

#### Merge Strategy: selectByIndex
Use another LLM to select the best response.

```kotlin
mergeStrategy = selectByIndex { responses ->
    val evaluator = AIAgent(...)
    val evaluation = evaluator.run("Which response is best? ${responses.joinToString()}")
    responses.indexOfFirst { it.contains(evaluation) }
}
```

#### Merge Strategy: fold
Combine all results.

```kotlin
mergeStrategy = fold { responses ->
    responses.joinToString("\n\n---\n\n")
}
```

### Parallel Tool Execution
```kotlin
val nodeMultiTool by nodeExecuteMultipleTools(
    tools = listOf("fetch_weather", "fetch_news", "fetch_stock"),
    parallel = true // Execute concurrently
)
```

---

## Data Transfer Between Nodes

Use typed storage for passing data between nodes.

### Example
```kotlin
// Define typed keys
val userDataKey = createStorageKey<UserData>("user-data")
val analysisKey = createStorageKey<AnalysisResult>("analysis")

val strategy = customStrategy {
    val nodeFetchUser by node<String, Unit> { userId ->
        val userData = fetchFromDatabase(userId)
        storage.set(userDataKey, userData)
    }

    val nodeAnalyze by node<Unit, Unit> {
        val user = storage.getValue(userDataKey)
        val analysis = performAnalysis(user)
        storage.set(analysisKey, analysis)
    }

    val nodeRespond by node<Unit, String> {
        val analysis = storage.getValue(analysisKey)
        formatResponse(analysis)
    }

    edge(nodeStart forwardTo nodeFetchUser)
    edge(nodeFetchUser forwardTo nodeAnalyze)
    edge(nodeAnalyze forwardTo nodeRespond)
    edge(nodeRespond forwardTo nodeFinish)
}
```

---

## RAG (Retrieval-Augmented Generation)

### Embeddings
```kotlin
// Local embeddings with Ollama
val embeddings = OllamaEmbeddings(model = NOMIC_EMBED_TEXT) // 768 dimensions

// Or OpenAI embeddings
val embeddings = OpenAIEmbeddings(apiKey = apiKey, model = "text-embedding-ada-002")

// Generate embedding
val vector = embeddings.embed("Kotlin is a modern programming language")
```

### Semantic Search Agent
```kotlin
val strategy = customStrategy {
    val nodeRetrieve by node<String, List<Document>> { query ->
        val queryEmbedding = embeddings.embed(query)
        documentStore.searchByEmbedding(queryEmbedding, topK = 5)
    }

    val nodeGenerate by nodeLLMRequest<List<Document>, String>(
        instruction = """
            Answer the question using ONLY the provided documents.
            If the answer is not in the documents, say "I don't have enough information."

            Documents: {documents}
        """
    )

    edge(nodeStart forwardTo nodeRetrieve)
    edge(nodeRetrieve transformed { docs -> docs.joinToString("\n\n") } forwardTo nodeGenerate)
    edge(nodeGenerate onAssistantMessage forwardTo nodeFinish)
}
```

---

## Testing

### Mock LLM Executor
```kotlin
val mockExecutor = MockPromptExecutor(
    responses = mapOf(
        onRequestContains("weather") to "The weather is sunny",
        onRequestContains("time") to "The time is 10:00 AM",
        onRequestEquals("Hello") to "Hi there!"
    )
)

val agent = AIAgent(
    executor = mockExecutor,
    systemPrompt = "Test agent",
    llmModel = OpenAIModels.Chat.GPT4o
)
```

### Mock Tools
```kotlin
val mockWeatherTool = mockTool("get_weather") {
    returns("Sunny, 22°C")
}

val mockDatabaseTool = mockTool("query_db") { args ->
    // Execute logic with side effects
    println("Querying: ${args["query"]}")
    "Result: ..."
}

val toolRegistry = ToolRegistry {
    tool(mockWeatherTool)
    tool(mockDatabaseTool)
}
```

### Graph Structure Tests
```kotlin
@Test
fun testGraphStructure() {
    val agent = createAgent()

    agent.testGraph {
        assertNodes {
            nodeStart exists
            nodeProcess exists
            nodeFinish exists
        }

        assertEdges {
            nodeStart connectsTo nodeProcess
            nodeProcess connectsTo nodeFinish
        }
    }
}
```

### Node Behavior Tests
```kotlin
@Test
fun testNodeBehavior() {
    val agent = createAgent()

    agent.testGraph {
        assertNodes {
            node("analyze") withInput "test input" produces "analyzed output"
        }
    }
}
```

---

## Spring Boot Integration

### Setup
```kotlin
// build.gradle.kts
dependencies {
    implementation("ai.koog:koog-spring-boot-starter:0.5.2")
}
```

### Configuration
```properties
# application.properties
ai.koog.openai.enabled=true
ai.koog.openai.api-key=${OPENAI_API_KEY}

ai.koog.anthropic.enabled=true
ai.koog.anthropic.api-key=${ANTHROPIC_API_KEY}
```

### Usage
```kotlin
@Service
class AgentService(
    private val openAIExecutor: SingleLLMPromptExecutor?,
    private val anthropicExecutor: SingleLLMPromptExecutor?
) {
    fun createAgent(): AIAgent {
        val executor = openAIExecutor ?: anthropicExecutor
            ?: throw IllegalStateException("No LLM provider configured")

        return AIAgent(
            executor = executor,
            systemPrompt = "You are a helpful assistant.",
            llmModel = OpenAIModels.Chat.GPT4o
        )
    }
}
```

---

## Observability

### Agent Events
```kotlin
class CustomEventProcessor : FeatureMessageProcessor {
    override fun process(message: FeatureMessage) {
        when (message) {
            is AgentStartingEvent -> log.info("Agent started: ${message.runId}")
            is NodeExecutionStartingEvent -> log.info("Node: ${message.nodeId}")
            is LLMCallCompletedEvent -> log.info("LLM call: ${message.tokens} tokens")
            is ToolCallEvent -> log.info("Tool: ${message.toolName}")
            is AgentCompletedEvent -> log.info("Completed: ${message.result}")
            is AgentErrorEvent -> log.error("Error: ${message.error}")
        }
    }
}

val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "...",
    llmModel = OpenAIModels.Chat.GPT4o,
    features = listOf(CustomEventProcessor())
)
```

### OpenTelemetry Tracing
```kotlin
val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "...",
    llmModel = OpenAIModels.Chat.GPT4o,
    features = listOf(
        OpenTelemetryTracing(
            exporter = LangfuseExporter(apiKey = langfuseKey)
            // or WeaveExporter(apiKey = weaveKey)
        )
    )
)
```

---

## Advanced Patterns

### Multi-Agent Orchestration
```kotlin
val researchAgent = AIAgent(...)
val writerAgent = AIAgent(...)
val editorAgent = AIAgent(...)

val orchestrator = customStrategy {
    val nodeResearch by node<String, String> { topic ->
        researchAgent.run(topic)
    }

    val nodeWrite by node<String, String> { research ->
        writerAgent.run("Write an article based on: $research")
    }

    val nodeEdit by node<String, String> { draft ->
        editorAgent.run("Edit and improve: $draft")
    }

    edge(nodeStart forwardTo nodeResearch)
    edge(nodeResearch forwardTo nodeWrite)
    edge(nodeWrite forwardTo nodeEdit)
    edge(nodeEdit forwardTo nodeFinish)
}
```

### Subgraphs (Scoped Tool Access)
```kotlin
val strategy = customStrategy {
    subgraph("data_processing") {
        tools = ToolRegistry { tool(DatabaseTool()) } // Only accessible in this subgraph

        val nodeFetch by nodeExecuteTool("database_query")
        val nodeTransform by nodeLLMRequest<String, String>("Transform data")

        edge(subgraphStart forwardTo nodeFetch)
        edge(nodeFetch forwardTo nodeTransform)
        edge(nodeTransform onAssistantMessage forwardTo subgraphFinish)
    }
}
```

### Agent Sessions (Manual History Management)
```kotlin
val agent = AIAgent(...)

// Write session (modify history)
agent.writeSession {
    appendPrompt {
        systemMessage("You are an expert.")
        userMessage("What is Kotlin?")
    }

    val response1 = requestLLM()

    // Compress if needed
    if (prompt.messages.size > 50) {
        replaceHistoryWithTLDR()
    }

    userMessage("Tell me more")
    val response2 = requestLLM()
}

// Read session (read-only)
agent.readSession {
    val allMessages = prompt.messages
    println("Total messages: ${allMessages.size}")
}
```

### MCP (Model Context Protocol) Integration
```kotlin
// Connect to MCP server (e.g., Google Maps, Playwright)
val mcpTransport = StdioTransport("/path/to/mcp-server")
val mcpRegistry = McpToolRegistryProvider(
    transport = mcpTransport,
    parser = McpToolDescriptorParser()
).createRegistry()

val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "You have access to external tools via MCP.",
    llmModel = OpenAIModels.Chat.GPT4o,
    toolRegistry = mcpRegistry
)
```

---

## Best Practices

### 1. Agent Design
- **Single Responsibility**: Each agent should have one clear purpose
- **Tool Minimalism**: Only expose necessary tools to reduce token usage
- **Clear Instructions**: Write specific, constrained system prompts
- **Error Handling**: Always handle tool failures and LLM errors gracefully

### 2. Strategy Graphs
- **Keep It Simple**: Start with simple graphs, add complexity as needed
- **Descriptive Names**: Use clear node and edge names
- **Test Structure**: Validate graph structure before testing behavior
- **Handle All Paths**: Ensure every node has an exit path to nodeFinish

### 3. Tools
- **Clear Descriptions**: LLMs rely on tool descriptions to decide when to use them
- **Parameter Documentation**: Annotate all parameters with @LLMDescription
- **Type Safety**: Use strong types for args and results
- **Idempotency**: Tools should be safe to retry

### 4. Performance
- **Compress History**: Enable compression for conversations >30 messages
- **Parallel Execution**: Use parallel tools/nodes when operations are independent
- **Streaming**: Use streaming for long-running generations
- **Caching**: Cache expensive tool results when appropriate

### 5. Production Readiness
- **Retry Policies**: Use RetryPolicy.PRODUCTION for fault tolerance
- **Observability**: Add event processors and tracing from the start
- **Testing**: Write tests for graph structure, node behavior, and edge routing
- **Monitoring**: Track token usage, latency, and error rates

---

## Common Pitfalls

### 1. Circular Edges
**Problem**: Creating loops without exit conditions.

**Solution**: Always include a condition that eventually leads to nodeFinish.

```kotlin
// ❌ Bad: Infinite loop
edge(nodeA forwardTo nodeB)
edge(nodeB forwardTo nodeA)

// ✅ Good: Loop with exit
edge(nodeCheck onCondition { !isComplete() } forwardTo nodeProcess)
edge(nodeCheck onCondition { isComplete() } forwardTo nodeFinish)
```

### 2. Missing Edge Handlers
**Problem**: Not handling all possible LLM outputs.

**Solution**: Handle both tool calls and text responses.

```kotlin
// ❌ Bad: Only handles tool calls
edge(nodeLLM onToolCall forwardTo nodeExecuteTool)

// ✅ Good: Handles both cases
edge(nodeLLM onToolCall forwardTo nodeExecuteTool)
edge(nodeLLM onAssistantMessage forwardTo nodeFinish)
```

### 3. Excessive Token Usage
**Problem**: Long conversations consume too many tokens.

**Solution**: Implement history compression.

```kotlin
val nodeCompress by nodeLLMCompressHistory<String>(
    strategy = FromLastNMessages(n = 10),
    onlyIf = { messages.size > 30 }
)
```

### 4. Hallucinating Tool Names
**Problem**: LLM invents non-existent tools.

**Solution**: Be explicit in system prompt about available tools.

```kotlin
systemPrompt = """
    You have access to these tools:
    - get_weather: Get current weather
    - search_docs: Search documentation

    Do NOT use any other tools.
"""
```

---

## Resources

### Official Documentation
- [Koog Documentation](https://docs.koog.ai/)
- [Koog GitHub](https://github.com/JetBrains/koog)
- [Koog Examples](https://github.com/JetBrains/koog/tree/develop/examples)

### Key Docs by Topic
- [Key Concepts](https://docs.koog.ai/key-concepts)
- [Custom Strategy Graphs](https://docs.koog.ai/custom-strategy-graphs)
- [Predefined Agent Strategies](https://docs.koog.ai/predefined-agent-strategies)
- [Nodes and Components](https://docs.koog.ai/nodes-and-components)
- [Structured Output](https://docs.koog.ai/structured-output)
- [History Compression](https://docs.koog.ai/history-compression)
- [Agent Memory](https://docs.koog.ai/agent-memory)
- [Agent Events](https://docs.koog.ai/agent-events)
- [Prompt API](https://docs.koog.ai/prompt-api)
- [Testing](https://docs.koog.ai/testing)
- [Spring Boot Integration](https://docs.koog.ai/spring-boot)
- [Model Context Protocol](https://docs.koog.ai/model-context-protocol)

### Comparison Resources
- [LangChain Documentation](https://docs.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

## Quick Reference

### Installation
```kotlin
dependencies {
    implementation("ai.koog:koog-agents:0.5.2")
}
```

### Basic Agent
```kotlin
val agent = AIAgent(
    executor = simpleOpenAIExecutor(apiKey),
    systemPrompt = "You are a helpful assistant.",
    llmModel = OpenAIModels.Chat.GPT4o
)
```

### Chat Strategy
```kotlin
strategy = chatAgentStrategy()
```

### ReAct Strategy
```kotlin
strategy = reActStrategy()
```

### Custom Graph
```kotlin
strategy = customStrategy {
    val node1 by nodeLLMRequest<String, String>("...")
    edge(nodeStart forwardTo node1)
    edge(node1 onAssistantMessage forwardTo nodeFinish)
}
```

### Annotation-Based Tool
```kotlin
@Tool
fun myTool(@LLMDescription("param") param: String): String { }
```

### Class-Based Tool
```kotlin
class MyTool : SimpleTool<Args>() { }
```

### Structured Output
```kotlin
@Serializable
data class Output(@LLMDescription("field") val field: String)
session.requestLLMStructured<Output>(...)
```

### History Compression
```kotlin
nodeLLMCompressHistory<String>(strategy = WholeHistory())
```

### Agent Memory
```kotlin
features = listOf(AgentMemory(...))
```

### Parallel Execution
```kotlin
parallel(listOf(node1, node2), mergeStrategy = selectByMax { })
```

---

This comprehensive guide covers all major aspects of the Koog framework. Use it as a reference when building production-grade AI agents in Kotlin with patterns similar to LangChain and LangGraph.
