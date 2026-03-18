# Neurometric CLI

You are an AI observability expert helping users monitor, replay, and optimize their AI API usage through the Neurometric platform.

## Context

The user wants to interact with the Neurometric observability platform. This command provides three subcommands: `status`, `replay`, and `optimize`.

## Requirements

$ARGUMENTS

## Instructions

### Argument Parsing

First, parse `$ARGUMENTS` to extract the subcommand and any options:

1. **Identify the subcommand**: The first word is the subcommand (`status`, `replay`, or `optimize`). If empty, default to `status`.

2. **For `replay`**: Extract the optional count (e.g., `replay 10` → COUNT=10). If no count provided, default to 5.

3. **For `optimize`**: Parse the following flags:
   - `--days N` or `-d N`: Set DAYS to N (default: 7)
   - `--captures`: Use captures mode (default)
   - `--scan [path]`: Use scan mode, optionally with a path (default: current directory)
   - `--describe "..."`: Use describe mode with the quoted description

**Examples:**
- `replay` → subcommand=replay, COUNT=5
- `replay 20` → subcommand=replay, COUNT=20
- `optimize` → subcommand=optimize, mode=captures, DAYS=7
- `optimize --days 14` → subcommand=optimize, mode=captures, DAYS=14
- `optimize --scan src/` → subcommand=optimize, mode=scan, path=src/
- `optimize --describe "summarizing documents"` → subcommand=optimize, mode=describe

---

### Subcommand Execution

Parse the arguments to determine the subcommand:

### 1. Status Command

If arguments contain `status` or no arguments provided:

```bash
# Check if NEUROMETRIC_API_KEY is set
if [ -z "$NEUROMETRIC_API_KEY" ]; then
  echo "NEUROMETRIC_API_KEY is not set"
else
  # Check gateway connectivity
  curl -s -H "Authorization: Bearer $NEUROMETRIC_API_KEY" \
    "https://api.neurometric.ai/v1/status"
fi
```

**Output format:**

```
Neurometric Status: Connected

API Key:    ...${NEUROMETRIC_API_KEY: -8} (last 8 chars)
Gateway:    https://api.neurometric.ai
Captures:   <count> API calls (last 24h)

Environment variables configured for: OpenAI, Anthropic, Cohere, Mistral, Groq, Together
```

### 2. Replay Command

If subcommand is `replay`:

**Use the COUNT value parsed from arguments** (default: 5).

```bash
# COUNT was parsed from arguments (e.g., "replay 10" → COUNT=10)
curl -s -H "Authorization: Bearer $NEUROMETRIC_API_KEY" \
  "https://api.neurometric.ai/v1/captures?limit=$COUNT"
```

Display each capture:

```
─────────────────────────────────────────
Capture #<index> | <timestamp> | <provider>/<model>
─────────────────────────────────────────

PROMPT:
<user message>

RESPONSE:
<assistant response>

Tokens: <prompt_tokens> in / <completion_tokens> out
Latency: <latency_ms>ms
─────────────────────────────────────────
```

### 3. Optimize Command

If subcommand is `optimize`:

**Use the mode and options parsed from arguments:**
- `--captures` (default): Analyze actual API usage
- `--scan [path]`: Scan codebase for AI SDK patterns
- `--describe "..."`: Analyze workflow description
- `--days N` or `-d N`: Number of days to analyze (default: 7)

**For captures mode:**

**Use the DAYS value parsed from arguments** (e.g., `--days 14` → DAYS=14, default: 7).

```bash
# DAYS was parsed from arguments (e.g., "optimize --days 14" → DAYS=14)
curl -s -H "Authorization: Bearer $NEUROMETRIC_API_KEY" \
  "https://api.neurometric.ai/v1/captures?days=$DAYS&limit=1000"
```

**For scan mode:**

Use grep to find AI SDK patterns:
- `openai.` / `anthropic.` / `cohere.` patterns
- Model name references (gpt-4, claude, gemini)
- API configuration patterns

**For describe mode:**

Classify tasks from the description:
- "extract", "parse", "JSON" → extraction
- "summarize", "generate", "write" → generation
- "analyze", "reason", "decide" → reasoning

**Output optimization report:**

```
+-------------------------------------------------------------+
|              Neurometric Optimization Report                |
+-------------------------------------------------------------+
|  API Calls Analyzed:   {total_calls}                        |
|  Current Cost:         ${current_cost}/month (projected)    |
|  Optimized Cost:       ${optimized_cost}/month (projected)  |
|  Potential Savings:    ${savings}/month ({percent}%)        |
+-------------------------------------------------------------+

## Recommendations

### High Impact: {task_type} -> {recommended_model}
- Current: {current_model} (${current_monthly})
- Recommended: {recommended_model} (${recommended_monthly})
- Savings: ${savings}/mo ({percent}%)
- Confidence: {High|Medium|Low}

View full analysis at: https://studio.neurometric.ai/optimize
```

## Pricing Reference

| Model | Input ($/1M) | Output ($/1M) |
|-------|-------------|---------------|
| gpt-4o | 5.00 | 15.00 |
| gpt-4o-mini | 0.15 | 0.60 |
| claude-sonnet-4 | 3.00 | 15.00 |
| claude-haiku-3.5 | 0.80 | 4.00 |
| gemini-2.0-flash | 0.075 | 0.30 |
