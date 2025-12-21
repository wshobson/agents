# MDS Orchestrator - Google AI Studio Quick Start

## Step-by-Step Setup

### Step 1: Open Google AI Studio
1. Go to https://aistudio.google.com/
2. Sign in with your Google account
3. Click **"Create new prompt"** → Select **"Chat prompt"**

### Step 2: Configure Model Settings
In the right sidebar, set:
```
Model: Gemini 1.5 Pro (or Gemini 2.0 Flash for speed)
Temperature: 0.7
Max Output: 8192 tokens
Top P: 0.95
```

### Step 3: Add System Instructions
1. Click **"System instructions"** (top left)
2. Copy the ENTIRE content from `PROMPT-1-SYSTEM.md`
3. Paste into the System Instructions field
4. Click outside to save

### Step 4: Bootstrap the System
1. In the chat input, copy content from `PROMPT-2-BOOTSTRAP.md`
2. Send the message
3. Wait for complete response
4. Review what the system demonstrates

### Step 5: Refine as Needed
Based on bootstrap response, use refinements from `PROMPT-3-REFINEMENTS.md`:
- **Agent switching unclear?** → Use Refinement A
- **Code quality lacking?** → Use Refinement B
- **Context getting lost?** → Use Refinement C
- **Multi-task coordination weak?** → Use Refinement D
- **Skills not leveraged?** → Use Refinement E
- **BMAD phases shallow?** → Use Refinement F
- **Need diagrams?** → Use Refinement G
- **Deployment guidance needed?** → Use Refinement H

### Step 6: Test with Real Tasks
Try these sample requests:

**Quick Flow Test:**
```
Fix this Python bug - the function returns None instead of the sum:

def calculate_total(items):
    total = 0
    for item in items:
        total + item.price
```

**Standard Track Test:**
```
Build a REST API endpoint for user registration with email verification.
Tech stack: FastAPI, PostgreSQL, Redis for token storage.
```

**Enterprise Track Test:**
```
Design a HIPAA-compliant patient data management system with:
- Encrypted storage
- Audit logging
- Role-based access control
- Data retention policies
```

## File Structure
```
google-ai-studio-export/
├── QUICKSTART.md          ← You are here
├── PROMPT-1-SYSTEM.md     ← System instructions
├── PROMPT-2-BOOTSTRAP.md  ← First message to send
├── PROMPT-3-REFINEMENTS.md ← Improvement prompts
└── README.md              ← Original setup guide
```

## Tips for Best Results

1. **Start fresh each session** - Paste system prompt again
2. **Be specific** - Include tech stack, constraints, requirements
3. **Request the track** - Say "Use Enterprise track" for complex work
4. **Ask for diagrams** - Request Mermaid diagrams for architecture
5. **Request code reviews** - Ask for security-auditor or code-reviewer
6. **Use memory tags** - Reference `[MDS-MEMORY]` for context persistence

## Troubleshooting

**Issue: Agent responses feel generic**
→ Send Refinement A to improve agent identity

**Issue: Code has TODOs or placeholders**
→ Send Refinement B with strict completion rules

**Issue: System forgets previous context**
→ Send Refinement C for better memory

**Issue: Complex tasks not broken down**
→ Send Refinement D for coordination

## API Integration (Optional)

For programmatic access:

```python
import google.generativeai as genai

genai.configure(api_key='YOUR_API_KEY')

# Load system prompt
with open('PROMPT-1-SYSTEM.md', 'r') as f:
    system_prompt = f.read()

model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction=system_prompt
)

chat = model.start_chat()
response = chat.send_message("Build a rate limiter middleware in Python")
print(response.text)
```

## Ready to Go!

Your MDS Orchestrator is ready with:
- 99 specialized agents
- 107 skills
- 71 tools
- 7 departments
- BMAD methodology
- Quality protocols

Start building!
