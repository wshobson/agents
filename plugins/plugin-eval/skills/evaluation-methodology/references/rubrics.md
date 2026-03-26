# Anchored Rubrics for LLM Judge Dimensions

## Triggering Accuracy

| Score | Level | Description |
|-------|-------|-------------|
| 0.0-0.2 | Poor | Description vague, triggers for wrong prompts or misses right ones |
| 0.3-0.4 | Below avg | Some trigger phrases but missing key use cases |
| 0.5-0.6 | Average | Reasonable but imprecise — false positives or misses |
| 0.7-0.8 | Good | Good coverage with minor gaps |
| 0.9-1.0 | Excellent | Precise, comprehensive — fires exactly when it should |

### Good trigger descriptions
- Start with what the skill does (one sentence)
- Follow with "Use this skill when..." + 3 specific contexts
- Mention concrete technologies, patterns, or file types
- Disambiguate from adjacent skills

## Orchestration Fitness

| Score | Level | Description |
|-------|-------|-------------|
| 0.0-0.2 | Poor | Acts as standalone agent — manages own tool calls |
| 0.3-0.4 | Below avg | Mixes worker and orchestrator roles |
| 0.5-0.6 | Average | Worker but outputs not structured for supervisor |
| 0.7-0.8 | Good | Clean worker, structured outputs, minor assumptions |
| 0.9-1.0 | Excellent | Pure worker — composable, clear contracts |

### Good signals
- Documents expected inputs and output format
- Produces artifacts a supervisor can consume
- Uses imperative instructions, not conditional delegation

### Bad signals
- Contains "orchestrate", "coordinate", "dispatch" language
- References other skills as dependencies
- Manages multi-step workflows internally

## Output Quality

| Score | Level | Description |
|-------|-------|-------------|
| 0.0-0.2 | Poor | Instructions produce incorrect or unhelpful output |
| 0.3-0.4 | Below avg | Some guidance but major gaps |
| 0.5-0.6 | Average | Adequate for basic cases, struggles with complexity |
| 0.7-0.8 | Good | Quality output for most cases |
| 0.9-1.0 | Excellent | Comprehensive, actionable, handles edge cases |

### Judge checks
- Code examples syntactically correct and runnable
- Complete workflows (not fragments)
- Error handling and edge case coverage
- Version-appropriate APIs (not deprecated)

## Scope Calibration

| Score | Level | Description |
|-------|-------|-------------|
| 0.0-0.2 | Too thin | Stub, insufficient to be useful |
| 0.3-0.4 | Too narrow | Covers topic but missing key aspects |
| 0.5-0.6 | Slightly off | Minor over-breadth or under-coverage |
| 0.7-0.8 | Well-scoped | Comprehensive without bloat |
| 0.9-1.0 | Perfect | Exactly right depth and breadth |

### Category norms
| Category | Lines | Pattern |
|----------|-------|---------|
| Technical | 400-600 | Steps + code + troubleshooting |
| Coordination | 100-200 | Decisions + process + checklists |
| Reference | 300-500 | Topics + examples per entry |
