# Gemini API Integration Guide

## Overview
Integrate the MDS orchestration system with Google's Gemini API for programmatic access.

## Prerequisites
- Google Cloud Project with Gemini API enabled
- API key or OAuth credentials
- Python 3.10+ or Node.js 18+

## Python Integration

### Installation
```bash
pip install google-generativeai
```

### Basic Setup
```python
import google.generativeai as genai
from pathlib import Path

# Configure API
genai.configure(api_key='YOUR_API_KEY')

# Load MDS system prompt
system_prompt = Path('system-prompt.md').read_text()

# Create model with MDS configuration
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction=system_prompt,
    generation_config={
        'temperature': 0.7,
        'top_p': 0.95,
        'top_k': 40,
        'max_output_tokens': 8192,
    }
)
```

### Single Request
```python
def mds_request(prompt: str) -> str:
    """Send a request to MDS system."""
    response = model.generate_content(prompt)
    return response.text

# Example usage
result = mds_request("""
Design a REST API for user authentication with:
- JWT tokens
- OAuth2 support
- Rate limiting
""")
print(result)
```

### Multi-Turn Conversation
```python
class MDSSession:
    def __init__(self):
        self.chat = model.start_chat()
        self.memory = {}

    def send(self, message: str) -> str:
        """Send message and get response."""
        response = self.chat.send_message(message)
        return response.text

    def switch_agent(self, agent_name: str, task: str) -> str:
        """Switch to specific agent for task."""
        prompt = f"""
        [MDS-SPECIALIST: {agent_name}]
        Task: {task}
        [/MDS-SPECIALIST]
        """
        return self.send(prompt)

    def save_memory(self, key: str, value: str):
        """Save to session memory."""
        self.memory[key] = value
        self.send(f"[MDS-MEMORY-UPDATE] {key}: {value}")

# Usage
session = MDSSession()

# Initial request
response = session.send("I need to build a payment processing system")

# Switch to specialist
security_review = session.switch_agent(
    "security-auditor",
    "Review the proposed payment system design for PCI compliance"
)
```

### Streaming Responses
```python
def mds_stream(prompt: str):
    """Stream MDS response for long outputs."""
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        print(chunk.text, end='', flush=True)

# Example
mds_stream("Create a comprehensive test suite for the authentication API")
```

### Structured Output
```python
import json

def mds_structured(prompt: str, schema: dict) -> dict:
    """Get structured JSON output."""
    structured_prompt = f"""
    {prompt}

    Respond in this JSON format:
    {json.dumps(schema, indent=2)}

    Output only valid JSON.
    """
    response = model.generate_content(structured_prompt)
    return json.loads(response.text)

# Example
schema = {
    "architecture": {
        "components": ["list of components"],
        "technologies": ["list of technologies"],
        "rationale": "explanation"
    }
}

result = mds_structured(
    "Design architecture for a real-time chat application",
    schema
)
```

## Node.js Integration

### Installation
```bash
npm install @google/generative-ai
```

### Basic Setup
```javascript
const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs');

const genAI = new GoogleGenerativeAI('YOUR_API_KEY');

const systemPrompt = fs.readFileSync('system-prompt.md', 'utf-8');

const model = genAI.getGenerativeModel({
  model: 'gemini-1.5-pro',
  systemInstruction: systemPrompt,
  generationConfig: {
    temperature: 0.7,
    topP: 0.95,
    topK: 40,
    maxOutputTokens: 8192,
  },
});
```

### Request Functions
```javascript
async function mdsRequest(prompt) {
  const result = await model.generateContent(prompt);
  return result.response.text();
}

class MDSSession {
  constructor() {
    this.chat = model.startChat();
  }

  async send(message) {
    const result = await this.chat.sendMessage(message);
    return result.response.text();
  }

  async switchAgent(agentName, task) {
    const prompt = `
      [MDS-SPECIALIST: ${agentName}]
      Task: ${task}
      [/MDS-SPECIALIST]
    `;
    return this.send(prompt);
  }
}

// Usage
const session = new MDSSession();
const response = await session.send('Design a microservices architecture');
```

## Error Handling

```python
from google.api_core import exceptions

def safe_mds_request(prompt: str, retries: int = 3) -> str:
    """Request with error handling and retries."""
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response.text
        except exceptions.ResourceExhausted:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
        except exceptions.InvalidArgument as e:
            return f"Invalid request: {e}"
        except Exception as e:
            return f"Error: {e}"
```

## Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute: int = 60):
    """Decorator for rate limiting API calls."""
    min_interval = 60.0 / calls_per_minute
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_minute=30)
def mds_request_limited(prompt: str) -> str:
    return model.generate_content(prompt).text
```

## Batch Processing

```python
import asyncio
from google.generativeai import GenerationConfig

async def mds_batch(prompts: list[str]) -> list[str]:
    """Process multiple prompts concurrently."""
    async def process_one(prompt):
        response = await asyncio.to_thread(
            model.generate_content, prompt
        )
        return response.text

    tasks = [process_one(p) for p in prompts]
    return await asyncio.gather(*tasks)

# Usage
prompts = [
    "Review this Python code for best practices",
    "Generate unit tests for the auth module",
    "Create API documentation for the user endpoint"
]

results = asyncio.run(mds_batch(prompts))
```

## Webhook Integration

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/mds/chat', methods=['POST'])
def mds_endpoint():
    """Webhook endpoint for MDS requests."""
    data = request.json
    prompt = data.get('prompt')
    session_id = data.get('session_id')

    # Get or create session
    session = get_or_create_session(session_id)

    # Process request
    response = session.send(prompt)

    return jsonify({
        'response': response,
        'session_id': session_id
    })

if __name__ == '__main__':
    app.run(port=5000)
```

## Best Practices

1. **Session Management**: Reuse chat sessions for context preservation
2. **Error Handling**: Always handle API errors gracefully
3. **Rate Limiting**: Respect API quotas
4. **Caching**: Cache responses for repeated queries
5. **Logging**: Log all requests for debugging
6. **Validation**: Validate outputs before using
7. **Timeouts**: Set appropriate timeouts for requests
