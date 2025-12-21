# MDS Google AI Studio Export

## Overview
This directory contains the MDS (Million Dollar Studio) AI orchestration system formatted for Google AI Studio and Gemini API integration.

## Setup Instructions

### Step 1: Access Google AI Studio
1. Navigate to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new project or select existing

### Step 2: Import System Prompt
1. Create a new "Structured Prompt"
2. Copy contents of `system-prompt.md` to the System Instructions field
3. Save as "MDS Orchestration System"

### Step 3: Configure Model Settings
```
Model: Gemini 1.5 Pro (for complex tasks) or Gemini 1.5 Flash (for routine)
Temperature: 0.7 (balanced)
Max Output Tokens: 8192
Top P: 0.95
Top K: 40
```

### Step 4: Add Agent Prompts
For each agent in `agents/`, create a saved prompt:
1. Create new structured prompt
2. Add system instructions from agent file
3. Save with agent name as title

## Directory Structure

```
google-ai-studio-export/
├── README.md                    # This file
├── system-prompt.md             # Master orchestration prompt
├── agents/                      # Individual agent prompts
│   ├── engineering/             # Engineering department agents
│   ├── operations/              # Operations department agents
│   ├── quality/                 # Quality department agents
│   ├── data-intelligence/       # Data/AI department agents
│   ├── security/                # Security department agents
│   ├── documentation/           # Documentation department agents
│   └── growth/                  # Growth department agents
├── workflows/                   # Workflow templates
├── schemas/                     # JSON schemas for structured output
└── integration/                 # Integration guides
```

## Usage Patterns

### Pattern 1: Single Agent Invocation
```
You are now operating as the [agent-name] agent.
[Include agent system prompt]

User request: [task description]
```

### Pattern 2: Multi-Agent Orchestration
```
You are the MDS CEO Agent orchestrating multiple specialists.
[Include full system prompt]

Route this request to appropriate agents and synthesize outputs:
[complex request]
```

### Pattern 3: Workflow Execution
```
Execute the [workflow-name] workflow.
Current phase: [phase]
Context: [project context]

Proceed with the next steps.
```

## Integration with Google Workspace

### Google Docs
- Use for generating documentation
- Structure outputs with headers and formatting
- Export ADRs, PRDs, and technical specs

### Google Sheets
- Track project status
- Monitor agent activity
- Analyze workflow metrics

### Google Drive
- Store generated artifacts
- Organize project documentation
- Share with stakeholders

## API Integration

### Gemini API Setup
```python
import google.generativeai as genai

genai.configure(api_key='YOUR_API_KEY')

# Create model with MDS system prompt
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction=open('system-prompt.md').read()
)

# Start chat session
chat = model.start_chat()

# Send request
response = chat.send_message("Design a REST API for user authentication")
print(response.text)
```

### Multi-Turn Conversation
```python
# Continue with agent switching
response = chat.send_message("""
[MDS-AGENT-SWITCH: security-auditor]
Review the proposed API design for security vulnerabilities.
""")
```

## Best Practices

1. **Context Preservation**: Use `[MDS-MEMORY]` tags to maintain context
2. **Agent Switching**: Explicitly switch agents for specialized tasks
3. **Quality Gates**: Request reviews before critical decisions
4. **Documentation**: Generate ADRs for significant choices
5. **Validation**: Use schemas for structured outputs

## Troubleshooting

### Issue: Agent not responding appropriately
**Solution**: Ensure agent system prompt is correctly loaded

### Issue: Context lost between messages
**Solution**: Use memory tags and summarize context periodically

### Issue: Inconsistent outputs
**Solution**: Add structured output schemas
