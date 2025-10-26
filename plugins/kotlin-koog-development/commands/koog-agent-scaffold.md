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
