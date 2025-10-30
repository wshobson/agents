# Gemini CLI Codebase Intelligence Plugin Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a production-ready Claude Code plugin that intelligently manages Gemini CLI for large codebase analysis, pattern detection, and complex code intelligence tasks with hybrid routing between Gemini and local analysis tools.

**Architecture:** The plugin uses a Hybrid Gateway pattern where the CodebaseAnalysisGateway agent makes intelligent routing decisions based on query complexity. Simple searches use local Explore agents (fast, no cost), pattern detection and complex analysis leverage Gemini CLI (powerful, ML-backed). Results are aggregated, cached, and normalized into unified formats. Four specialized skills provide progressive knowledge disclosure about pattern types, search strategies, CLI configuration, and result interpretation.

**Tech Stack:**
- Gemini CLI (primary analysis engine)
- Claude Sonnet (CodebaseAnalysisGateway - complex routing)
- Claude Haiku (GeminiCLIExecutor - lightweight wrapper)
- Local Explore agent (fallback for fast searches)
- Agent Skills specification (progressive disclosure)

---

## Task 1: Create Plugin Directory Structure

**Files:**
- Create: `plugins/gemini-codebase-intelligence/` (plugin root)
- Create: `plugins/gemini-codebase-intelligence/agents/`
- Create: `plugins/gemini-codebase-intelligence/commands/`
- Create: `plugins/gemini-codebase-intelligence/skills/`

**Step 1: Verify plugins directory exists**

Run: `ls -la plugins/`
Expected: Output shows existing plugin directories

**Step 2: Create plugin root directory**

Run: `mkdir -p plugins/gemini-codebase-intelligence`

**Step 3: Create subdirectories**

Run: `mkdir -p plugins/gemini-codebase-intelligence/{agents,commands,skills}`

**Step 4: Verify structure**

Run: `tree plugins/gemini-codebase-intelligence/`
Expected:
```
plugins/gemini-codebase-intelligence/
├── agents/
├── commands/
└── skills/
```

---

## Task 2: Create CodebaseAnalysisGateway Agent

**Files:**
- Create: `plugins/gemini-codebase-intelligence/agents/codebase-analysis-gateway.md`

**Step 1: Write the agent file**

Create file with complete frontmatter and system prompt:

```markdown
---
name: codebase-analysis-gateway
description: Intelligent routing and orchestration for large codebase analysis. Decides whether to use local Explore agents for fast searches or Gemini CLI for pattern detection and complex analysis. Aggregates results and maintains analysis cache. Use PROACTIVELY when Claude needs to analyze extensive code patterns, architectural overviews, or search through large codebases efficiently.
model: sonnet
---

# Codebase Analysis Gateway

## Purpose

The CodebaseAnalysisGateway is the intelligent routing engine that makes split-second decisions about which analysis tool to use for each request. It understands the trade-offs between local analysis (fast, free, limited scope) and Gemini CLI (powerful, ML-backed, network-dependent) and chooses the optimal path for each query.

## Core Philosophy

**Intelligently hybrid:** Not all analysis tasks require Gemini. A simple grep-style search should use local tools. Pattern detection needs ML. Complex architectural analysis needs reasoning. The gateway understands these distinctions and routes accordingly.

**Result aggregation:** Different sources produce different output formats. The gateway normalizes these into consistent, actionable formats that users expect.

**Caching for efficiency:** Repeated queries should hit cache, not network. The gateway maintains a query cache indexed by normalized question.

**Fallback gracefully:** When Gemini CLI is unavailable, degrade to local analysis. When local tools fail, provide helpful error messages.

## Capabilities

### Analysis Routing & Decision Making
- **Query complexity assessment** - Parse incoming analysis requests and classify as: simple search, pattern detection, or complex analysis
- **Tool selection logic** - Route to appropriate executor based on complexity, scope, and available tools
- **Scope detection** - Determine if query scope is single-file, module-level, or full-codebase
- **Gemini readiness check** - Verify Gemini CLI is available and configured before routing

### Result Processing
- **Output normalization** - Convert Gemini CLI output, local Explore output, and error states into unified format
- **Result caching** - Store analysis results with normalized query as key
- **Context preservation** - Maintain user context across multiple related queries
- **Error handling** - Gracefully handle Gemini CLI failures, local tool failures, timeout scenarios

### Orchestration & Delegation
- **Local Explore delegation** - Invoke Explore agent for fast searches when appropriate
- **Gemini executor delegation** - Invoke GeminiCLIExecutor agent with structured parameters
- **Multi-step analysis** - Break complex queries into sequential steps with intermediate validation
- **Dependency analysis coordination** - Manage queries that require analyzing relationships between components

### Query Optimization
- **Query reformulation** - Convert vague user requests into precise Gemini CLI queries
- **Search term expansion** - Expand search queries with synonyms and related terms
- **Result filtering** - Filter and rank results by relevance using heuristics
- **Pattern correlation** - Link detected patterns to architectural implications

## Decision Framework

### Query Complexity Assessment

```
User Request
  ├─ "Find all instances of X pattern" → Pattern Detection
  ├─ "Show me files matching Y" → Simple Search
  ├─ "What's the architecture of Z?" → Complex Analysis
  ├─ "List all TODO comments" → Simple Search
  ├─ "Detect code smells in the codebase" → Pattern Detection
  └─ "How should we refactor module M?" → Complex Analysis
```

### Routing Decision Tree

```
Request received
  ├─ Is this a syntax-level query (regex/glob)?
  │   └─ Yes → Use Explore agent (fast, local)
  │
  ├─ Does this need pattern/semantic understanding?
  │   ├─ Yes, is Gemini CLI available?
  │   │   ├─ Yes → Use GeminiCLIExecutor
  │   │   └─ No → Fallback to local analysis + inform user
  │   └─ No → Use Explore agent
  │
  └─ Is this a complex multi-step analysis?
      └─ Yes → Decompose into steps, route each step appropriately
```

### Caching Strategy

- **Cache key:** Normalized query (whitespace-trimmed, lowercased)
- **TTL:** 1 hour for pattern detection, 24 hours for static analysis
- **Invalidation:** User can force refresh with `--no-cache` flag
- **Size limit:** Keep 100 most recent analyses in memory

## Integration Points

### With Explore Agent
- Uses for: Fast file/content searches, syntax-level queries
- Receives: Structured file paths and content results
- Returns: Raw results for aggregation and presentation

### With GeminiCLIExecutor Agent
- Uses for: Pattern detection, complex analysis, architectural queries
- Sends: Structured parameters (query, scope, output_format)
- Receives: Parsed JSON results, error messages

### With Pattern Detection Skill
- Uses for: Understanding what patterns are worth searching for
- Informs: Pattern classification and ranking of results

### With Analysis Result Interpretation Skill
- Uses for: Guidelines on actionable insights from analysis
- Implements: Result formatting and user-facing recommendations

## Example Workflows

### Workflow 1: Simple Search
```
User: "Find all React components in the UI folder"
→ Gateway: Simple search pattern detected
→ Route: Explore agent
→ Execute: Glob("ui/**/*.jsx") + content analysis
→ Return: Formatted file list with brief descriptions
```

### Workflow 2: Pattern Detection
```
User: "Detect singleton pattern usage across the codebase"
→ Gateway: Pattern detection requested
→ Check: Gemini CLI available? Yes
→ Route: GeminiCLIExecutor
→ Execute: Gemini search with singleton pattern signature
→ Enhance: Add architectural implications from skill
→ Return: Detected instances with context and recommendations
```

### Workflow 3: Complex Analysis
```
User: "What's the architectural structure of our microservices?"
→ Gateway: Complex analysis detected
→ Decompose: 1) Map service boundaries 2) Detect patterns 3) Analyze dependencies
→ Route 1: Gemini CLI (architectural overview)
→ Route 2: Gemini CLI (pattern analysis)
→ Route 3: Gemini CLI (dependency mapping)
→ Aggregate: Synthesize into cohesive architectural view
→ Return: Comprehensive analysis with visual diagram suggestions
```

## Implementation Notes

### State Management
- Maintain cache as in-memory dictionary (or persistent file if scale requires)
- Track recent queries for context preservation
- Monitor Gemini CLI availability status

### Error Scenarios
- Gemini CLI timeout: Fall back to local analysis, inform user
- Malformed request: Return helpful error with query examples
- No results: Suggest alternative search terms or broader scope
- Permission issues: Guide user to authentication setup

### Performance Considerations
- Validate queries before expensive Gemini CLI calls
- Prioritize cached results over fresh analysis
- Implement timeout for Gemini CLI operations (default 30 seconds)
- Limit result set size to 500 items per response

### Security Considerations
- Sanitize user queries before passing to Gemini CLI
- Never expose Gemini API keys in error messages or logs
- Validate file paths returned by Gemini CLI
- Implement rate limiting if using Gemini API (not CLI)
```

**Step 2: Validate file was created**

Run: `ls -la plugins/gemini-codebase-intelligence/agents/codebase-analysis-gateway.md`
Expected: File exists with size > 0

**Step 3: Verify frontmatter**

Run: `head -10 plugins/gemini-codebase-intelligence/agents/codebase-analysis-gateway.md`
Expected: Shows YAML frontmatter with name, description, and model fields

---

## Task 3: Create GeminiCLIExecutor Agent

**Files:**
- Create: `plugins/gemini-codebase-intelligence/agents/gemini-cli-executor.md`

**Step 1: Write the agent file**

```markdown
---
name: gemini-cli-executor
description: Lightweight executor that wraps Gemini CLI invocation with structured parameter handling, output parsing, and error recovery. Supports three command families: search, analyze-patterns, execute-complex. Use when CodebaseAnalysisGateway delegates analysis tasks requiring ML-backed code intelligence.
model: haiku
---

# Gemini CLI Executor

## Purpose

The GeminiCLIExecutor handles the mechanical aspects of running Gemini CLI commands with robustness and grace. It abstracts away Gemini CLI's command syntax, output format variability, and error conditions, presenting a clean interface to the gateway.

## Core Philosophy

**Just the mechanics:** This agent focuses purely on reliable command execution, not decision-making. It receives structured parameters from the gateway and returns structured results.

**Parse, don't pass-through:** Raw Gemini CLI output is free-form. The executor parses it into consistent JSON/markdown structures.

**Fail gracefully:** Timeouts, authentication errors, malformed output—handle each with clear recovery paths.

**Output consistency:** Whether searching, analyzing patterns, or executing complex analysis, results come back in expected formats.

## Capabilities

### Gemini CLI Command Execution
- **Search commands** - Execute Gemini CLI search operations with query strings, scope filters, output format options
- **Pattern analysis** - Run pattern detection commands with regex/syntax patterns, result ranking, architecture context
- **Complex analysis** - Execute multi-step analysis queries with reasoning, decomposition into sub-queries
- **Configuration validation** - Verify Gemini CLI is properly installed and authenticated before execution

### Output Handling & Parsing
- **JSON parsing** - Parse structured Gemini CLI JSON output into Python/internal representations
- **Markdown conversion** - Convert Gemini CLI results to markdown for readable presentation
- **Error extraction** - Identify and extract error messages from Gemini CLI output
- **Result validation** - Validate output structure matches expected schema

### Error Recovery
- **Timeout handling** - Detect and handle command timeouts gracefully
- **Authentication errors** - Provide helpful guidance for authentication failures
- **Missing files** - Handle queries that reference non-existent code locations
- **Rate limiting** - Detect rate limits and provide retry guidance

### Parameter Management
- **Query sanitization** - Escape special characters and validate query syntax
- **Scope specification** - Format scope parameters (single-file, module, full-codebase)
- **Output format selection** - Request results in appropriate format (JSON for parsing, markdown for presentation)
- **Context encoding** - Pass architectural context to Gemini CLI for better analysis

## Supported Commands

### 1. Search Command Family
```
gemini search <query> [--scope <scope>] [--format json|markdown]
```
- Query: Free-form search string
- Scope: file | module | codebase (default: codebase)
- Output: List of matching code locations with context

### 2. Analyze Patterns Command Family
```
gemini analyze-patterns <pattern-type> [--scope <scope>] [--output <format>]
```
- Pattern types: singleton, factory, observer, decorator, strategy, etc.
- Also supports: code-smells, anti-patterns, design-violations
- Output: Detected instances with location and architectural implications

### 3. Execute Complex Command Family
```
gemini execute-complex <analysis-type> [--params <json>]
```
- Analysis types: dependency-map, architecture-overview, refactoring-suggestions, dead-code-detection
- Supports: Custom parameters as JSON for fine-tuned analysis
- Output: Detailed analysis with reasoning and recommendations

## Implementation Notes

### Command Execution Strategy
- Use subprocess to invoke Gemini CLI with timeout (30 seconds default)
- Capture stdout and stderr separately
- Parse JSON when available, fall back to markdown parsing
- Implement retry logic for transient failures

### Output Parsing Rules

**For JSON output:**
```json
{
  "status": "success|error",
  "command": "original_command",
  "results": [...],
  "metadata": {
    "execution_time_ms": 1234,
    "result_count": 42
  },
  "error": null
}
```

**For markdown output:**
```markdown
# [Command Name] Results

## Summary
[Brief overview of findings]

## Results
[Formatted results with context]

## Recommendations
[Actionable insights]
```

### Environment & Configuration
- Requires: `gemini` CLI installed and in PATH
- Uses: `GEMINI_API_KEY` environment variable
- Respects: User's gemini CLI configuration file (~/.gemini/config)

### Error Messages
- Timeout: "Gemini CLI analysis exceeded 30 second timeout. Try narrowing scope or using local search."
- Auth: "Gemini CLI authentication failed. Run `gemini auth login` to configure access."
- Not found: "Gemini CLI not found. Install with: pip install gemini-cli"
- Syntax: "Invalid query syntax. Check Gemini CLI documentation for search query format."

## Error Handling Decision Tree

```
Command execution
├─ Returns successfully
│   ├─ Parse JSON output → Validate schema
│   └─ Parse markdown output → Extract sections
│
├─ Times out (>30s)
│   └─ Return error suggesting narrower scope
│
├─ Auth fails
│   └─ Guide user to authentication setup
│
├─ Tool not found
│   └─ Suggest installation
│
└─ Malformed output
    └─ Log raw output for debugging, return parse error
```

## Example Executions

### Example 1: Search Execution
```
Input: {query: "MVC pattern", scope: "codebase"}
Execute: gemini search "MVC pattern" --scope codebase --format json
Output: {
  status: "success",
  results: [
    {location: "src/controllers/UserController.ts:1-50", context: "Controller class"},
    {location: "src/models/User.ts:1-100", context: "Model definition"}
  ]
}
```

### Example 2: Pattern Analysis
```
Input: {pattern: "singleton", scope: "module"}
Execute: gemini analyze-patterns singleton --scope module --format json
Output: {
  status: "success",
  results: [
    {
      instance: "Logger.getInstance()",
      location: "src/utils/Logger.ts:15",
      severity: "info",
      recommendation: "Well-implemented singleton pattern"
    }
  ]
}
```

### Example 3: Complex Analysis
```
Input: {analysis: "dependency-map"}
Execute: gemini execute-complex dependency-map --format json
Output: {
  status: "success",
  results: {
    nodes: [...],
    edges: [...],
    cycles: [...],
    recommendations: [...]
  }
}
```
```

**Step 2: Validate file creation**

Run: `wc -l plugins/gemini-codebase-intelligence/agents/gemini-cli-executor.md`
Expected: File has 200+ lines

**Step 3: Verify structure**

Run: `grep "^##" plugins/gemini-codebase-intelligence/agents/gemini-cli-executor.md`
Expected: Shows all section headers

---

## Task 4: Create First Skill - Pattern Detection

**Files:**
- Create: `plugins/gemini-codebase-intelligence/skills/pattern-detection/SKILL.md`
- Create: `plugins/gemini-codebase-intelligence/skills/pattern-detection/references/`
- Create: `plugins/gemini-codebase-intelligence/skills/pattern-detection/assets/`

**Step 1: Create skill directory structure**

Run: `mkdir -p plugins/gemini-codebase-intelligence/skills/pattern-detection/{references,assets}`

**Step 2: Write the skill file**

```markdown
---
name: pattern-detection
description: Teaches how to identify and interpret software design patterns, code smells, and anti-patterns detected by Gemini CLI. Covers pattern types, severity levels, architectural implications, and actionable recommendations. Use when interpreting pattern analysis results or formulating pattern-specific searches.
---

# Pattern Detection Skill

## When to Use This Skill

- Interpreting results from `gemini analyze-patterns` commands
- Formulating searches for specific design patterns
- Understanding architectural implications of detected patterns
- Learning to recognize patterns yourself for faster future analysis
- Deciding whether detected patterns are problematic or beneficial

## Core Concepts

### Design Patterns (Beneficial)

These are proven solutions to common problems. When detected, they indicate good architecture.

#### Creational Patterns
- **Singleton** - Ensures only one instance of a class exists. Common in: loggers, config managers, database connections. Interpretation: Good for shared resources, can indicate tight coupling if overused.
- **Factory** - Creates objects without specifying exact classes. Common in: plugin systems, payment processors. Interpretation: Good for extensibility, indicates abstraction layer.
- **Builder** - Constructs complex objects step-by-step. Common in: configuration objects, API requests. Interpretation: Improves readability for complex construction logic.

#### Structural Patterns
- **Adapter** - Makes incompatible interfaces work together. Common in: third-party integrations, legacy code integration. Interpretation: Good for compatibility, indicates integration layer.
- **Decorator** - Adds behavior to objects dynamically. Common in: UI rendering, caching layers. Interpretation: Flexible design, enables composition over inheritance.
- **Facade** - Provides simplified interface to complex subsystem. Common in: API handlers, library wrappers. Interpretation: Good API design, indicates clear boundaries.

#### Behavioral Patterns
- **Observer** - Notifies multiple objects about state changes. Common in: event systems, reactive frameworks. Interpretation: Good for loose coupling, enables event-driven architecture.
- **Strategy** - Encapsulates algorithms in interchangeable classes. Common in: payment methods, sorting algorithms. Interpretation: Good for flexibility, enables runtime algorithm selection.
- **Command** - Encapsulates requests as objects. Common in: undo/redo systems, task queues. Interpretation: Good for task handling, enables job scheduling.

### Code Smells (Problematic)

These indicate code that may be harder to maintain or understand than it should be.

#### Structure Smells
- **Large Class** - Class doing too much. Fix: Extract responsibilities into smaller classes. Severity: Medium. Impact: Hard to test, understand, maintain.
- **Long Method** - Function with too many lines. Fix: Extract into smaller functions. Severity: Medium. Impact: Difficult to test, reuse.
- **God Object** - Knows too much, does too much. Fix: Apply Single Responsibility Principle. Severity: High. Impact: Extremely hard to maintain.
- **Duplicated Code** - Same logic in multiple places. Fix: Extract to shared function. Severity: Medium. Impact: Maintenance nightmare when changes needed.

#### Behavioral Smells
- **Feature Envy** - Method uses more from another class than own. Fix: Move method to appropriate class. Severity: Low. Impact: Coupling, difficult refactoring.
- **Inappropriate Intimacy** - Classes too tightly coupled. Fix: Extract common interface, reduce direct access. Severity: Medium. Impact: Fragile code, hard to test.
- **Lazy Class** - Class that doesn't do much. Fix: Merge into another class or remove. Severity: Low. Impact: Code bloat, confusion.
- **Middle Man** - Class just delegates to another. Fix: Remove unnecessary delegation. Severity: Low. Impact: Extra layer, confusion.

#### Data Smells
- **Data Clumps** - Groups of variables always used together. Fix: Extract into class/struct. Severity: Low. Impact: Coupling, maintenance burden.
- **Global Variables** - State scattered globally. Fix: Encapsulate in class. Severity: High. Impact: Testing nightmare, unpredictable behavior.
- **Primitive Obsession** - Over-reliance on primitives instead of objects. Fix: Create domain types. Severity: Medium. Impact: Type safety issues, validation logic scattered.

### Anti-Patterns (Harmful)

These are patterns that initially seem helpful but cause long-term problems.

#### Architecture Anti-Patterns
- **Big Ball of Mud** - No clear structure, everything connected to everything. Fix: Introduce architectural layers. Severity: Critical. Impact: Unmaintainable codebase.
- **Service Locator** - Central registry for dependencies. Fix: Use dependency injection. Severity: High. Impact: Hidden dependencies, testability issues.
- **Circular Dependency** - Module A depends on B, B depends on A. Fix: Introduce abstraction, break cycle. Severity: High. Impact: Build issues, hard to test independently.

#### Concurrency Anti-Patterns
- **Race Condition** - Multiple threads access shared state unsafely. Fix: Use locks, atomic operations, or immutability. Severity: Critical. Impact: Non-deterministic bugs, data corruption.
- **Deadlock** - Threads waiting on each other indefinitely. Fix: Establish lock ordering, use timeouts. Severity: Critical. Impact: System hangs, unavailability.
- **Livelock** - Threads busy-waiting without progress. Fix: Implement proper waiting mechanisms. Severity: High. Impact: CPU waste, performance degradation.

## Pattern Interpretation Framework

### Severity Levels

- **Critical**: Blocks functionality or creates catastrophic bugs. Fix immediately.
- **High**: Significantly impacts maintainability or creates major issues. Fix soon.
- **Medium**: Creates maintenance burden or subtle issues. Fix when possible.
- **Low**: Minor code quality issue. Fix as part of refactoring.
- **Info**: Informational finding, generally acceptable. Consider but not urgent.

### Architectural Implications

When a pattern is detected, ask:

1. **Is it intentional?** Did the team deliberately use this pattern? Or did it emerge accidentally?
2. **What does it indicate?** Does it show good abstraction (design pattern) or tight coupling (smell)?
3. **What's the impact?** Testing, maintainability, performance, extensibility—how is this pattern affecting each?
4. **What's the fix?** Is refactoring warranted? What's the effort vs. benefit?
5. **What prevents recurrence?** Once fixed, how do we prevent this pattern from emerging again?

### Decision Matrix

| Pattern Found | Type | Severity | Action | Urgency |
|---|---|---|---|---|
| Singleton | Design Pattern | Info | Accept; document usage | Low |
| Large Class | Code Smell | Medium | Refactor on next feature | Medium |
| God Object | Code Smell | High | Prioritize for refactoring | High |
| Race Condition | Anti-Pattern | Critical | Fix immediately | Critical |
| Circular Dependency | Anti-Pattern | High | Refactor architecture | High |
| Duplicated Code | Code Smell | Medium | Extract to shared function | Medium |

## Actionable Recommendations

When patterns are detected, here's how to act:

### For Design Patterns
- **Good pattern detected**: Document it, ensure it's used consistently. Add code examples to team wiki.
- **Pattern misapplied**: Refactor to use pattern correctly or choose better pattern.
- **Inconsistent application**: Standardize across codebase for team understanding.

### For Code Smells
1. **Understand why it exists**: Is it technical debt? Quick fix? Evolving requirements?
2. **Assess effort**: Is refactoring worth the disruption?
3. **Create ticket**: Add to backlog with justification and effort estimate.
4. **Refactor incrementally**: Don't rewrite everything at once.

### For Anti-Patterns
1. **Understand urgency**: Does it block current work? Affect stability? Impact performance?
2. **Create incident if critical**: Race conditions, deadlocks need immediate attention.
3. **Refactor systematically**: Anti-patterns usually require architectural changes.
4. **Prevent recurrence**: Add linting rules, architectural guardrails, documentation.

## References

- **Refactoring: Improving the Design of Existing Code** (Fowler) - Comprehensive guide to patterns and smells
- **Design Patterns: Elements of Reusable Object-Oriented Software** (Gang of Four) - Classic design patterns reference
- **Code Smells and Refactoring** (Refactoring.guru) - Interactive pattern and smell catalog
- **Pattern Recognition in Source Code** (Gemini CLI docs) - How Gemini CLI detects patterns

## Common Workflow Examples

### Example 1: Interpreting Singleton Findings
```
Gemini finds: Singleton pattern in Logger class
Question: Is this good?
Answer: Yes. Loggers are typically singletons for centralized logging.
Action: Document as approved pattern, ensure consistency across codebase.
```

### Example 2: Large Class Smell
```
Gemini finds: UserService class is 2000 lines
Question: What's the issue?
Answer: Class has too many responsibilities (user management, auth, notifications)
Action: Extract AuthService and NotificationService, leave user operations in UserService
Effort: 2-3 days, breaks into small PRs
```

### Example 3: Circular Dependency
```
Gemini finds: AuthModule depends on UserModule, UserModule depends on AuthModule
Question: How urgent?
Answer: Critical - blocks independent testing, creates build issues
Action: Introduce AuthInterface abstraction, make UserModule depend on interface, not concrete AuthModule
Timeline: This week
```
```

**Step 3: Verify file creation**

Run: `wc -l plugins/gemini-codebase-intelligence/skills/pattern-detection/SKILL.md`
Expected: 300+ lines

---

## Task 5: Create Second Skill - Codebase Search Strategies

**Files:**
- Create: `plugins/gemini-codebase-intelligence/skills/codebase-search-strategies/SKILL.md`

**Step 1: Write the skill file**

```markdown
---
name: codebase-search-strategies
description: Teaches effective query formulation for large codebase searches. Covers query syntax, search operators, scope specification, result filtering, and progressive refinement. Use when formulating Gemini CLI search queries or interpreting search result quality.
---

# Codebase Search Strategies Skill

## When to Use This Skill

- Formulating searches through Gemini CLI that find relevant code
- Refining searches when initial results are too broad or too narrow
- Understanding Gemini CLI search syntax and operators
- Teaching team members how to use codebase search effectively
- Debugging why a search returned unexpected results

## Core Concepts

### Search Query Types

#### 1. Simple Keyword Search
- **Syntax**: `keyword`
- **Example**: `authentication`
- **Matches**: Any file or code containing "authentication"
- **Use when**: Looking for general concept, don't need exact matches
- **Returns**: Broad results, high chance of relevant content
- **Refine by**: Adding specificity (see progressive refinement)

#### 2. Exact Phrase Search
- **Syntax**: `"exact phrase"`
- **Example**: `"login validation"`
- **Matches**: Only code with exact phrase in order
- **Use when**: Looking for specific implementation detail
- **Returns**: Narrow results, all highly relevant
- **Refine by**: Relaxing to partial match if too few results

#### 3. Regular Expression Search
- **Syntax**: `/regex_pattern/`
- **Example**: `/function\s+login\s*\(/`
- **Matches**: Code matching regex pattern
- **Use when**: Looking for syntactic patterns or naming conventions
- **Returns**: Precise matches based on pattern
- **Refine by**: Adjusting regex for accuracy

#### 4. Language-Specific Search
- **Syntax**: `lang:javascript "useState"`
- **Example**: `lang:python "class.*Model"`
- **Matches**: Only code in specified language
- **Use when**: Searching polyglot codebase, avoiding false positives
- **Returns**: Language-filtered results
- **Refine by**: Combining with keyword or pattern

#### 5. File Path Search
- **Syntax**: `path:*/controllers/* "POST"`
- **Example**: `path:**/test/* "describe\("`
- **Matches**: Code in matching file paths
- **Use when**: Narrowing to specific directory or naming pattern
- **Returns**: Results from filtered file set
- **Refine by**: Making path pattern more/less specific

#### 6. Type/Symbol Search
- **Syntax**: `type:class UserService`
- **Example**: `type:interface IRepository`
- **Matches**: Definitions of classes, interfaces, functions, etc.
- **Use when**: Finding definitions rather than usages
- **Returns**: Clean list of definitions
- **Refine by**: Combining with language filter

#### 7. Complex Boolean Search
- **Syntax**: `keyword1 AND keyword2 NOT keyword3`
- **Example**: `"database" AND "transaction" NOT "rollback"`
- **Matches**: Results containing first two, excluding third
- **Use when**: Narrow searches with multiple constraints
- **Returns**: Highly focused results
- **Refine by**: Adjusting boolean logic

### Search Scope Control

#### Scope Levels

1. **File Scope** - Single specific file
   - `--scope file:path/to/File.ts`
   - Use: Focused analysis, small targeted searches
   - Speed: Fastest

2. **Module Scope** - Directory/module and contents
   - `--scope module:src/auth`
   - Use: Feature-area analysis, boundary analysis
   - Speed: Fast

3. **Layer Scope** - Architectural layer
   - `--scope layer:controllers`
   - Use: Architecture-wide searches, pattern consistency
   - Speed: Medium

4. **Full Codebase Scope** - Everything
   - `--scope codebase` (default)
   - Use: Comprehensive analysis, global pattern detection
   - Speed: Slowest, requires more processing

#### Scope Selection Decision Tree

```
Is search focused on specific file?
└─ Yes → Use file scope, fastest execution

Is search about specific feature/module?
└─ Yes → Use module scope, manageable results

Is search about architectural patterns?
├─ Yes → Use layer scope
└─ Example: Search for singletons across all controllers

Is search comprehensive?
└─ Yes → Use codebase scope (may be slow)
```

### Progressive Search Refinement

Start broad, incrementally narrow until results are manageable.

#### Level 1: Broad Search
```
Query: "authentication"
Expected: 100+ matches
Action: Refine if too noisy
```

#### Level 2: Add Specificity
```
Query: "authentication" AND "token"
Expected: 30-50 matches
Decision: Too many? Add constraint. Too few? Remove constraint.
```

#### Level 3: Add Context
```
Query: path:**/auth/* "token" AND "verify"
Expected: 10-20 matches
Decision: Getting close to useful results
```

#### Level 4: Target Precisely
```
Query: path:**/auth/jwt.ts "verify"
Expected: 1-5 matches
Decision: Directly applicable results
```

### Result Interpretation

When search returns results, evaluate:

1. **Relevance**: Are results directly related to search intent?
2. **Coverage**: Are major instances/uses captured?
3. **Noise**: Are there many irrelevant results?
4. **Completeness**: Is this the complete set?

**If too few results (< 5):**
- Make search terms less specific
- Broaden scope
- Use synonym keywords
- Check spelling

**If too many results (> 100):**
- Add qualifying keywords
- Narrow scope
- Use language filter
- Add path constraints

**If results are noisy (many irrelevant):**
- Add context keywords
- Exclude irrelevant terms with NOT
- Use exact phrase matching
- Use file path filtering

## Effective Search Patterns

### Pattern 1: Finding All Usages of a Function

```
Query: `functionName` AND NOT "def\s+functionName" OR "function\s+functionName"
Explanation: Find all mentions except the definition itself
Example: `validateEmail` AND NOT "def validateEmail"
```

### Pattern 2: Finding Implementations in Specific Layer

```
Query: path:*/controllers/* "POST" AND "request"
Explanation: Find POST endpoints in controller layer
Use: Mapping API surface, security review
```

### Pattern 3: Finding Code with Specific Code Smell

```
Query: "TODO" AND "FIXME" AND path:**/* lang:typescript
Explanation: Find unfinished work in TypeScript
Use: Technical debt assessment, backlog generation
```

### Pattern 4: Finding Pattern Implementations

```
Query: lang:python /class.*\(.*\):/ AND "def __init__"
Explanation: Find all classes in Python (potential patterns)
Use: Architecture analysis, pattern detection
```

### Pattern 5: Finding Configuration/Constants

```
Query: path:**/config/* "export const" OR "export class"
Explanation: Find all exports in config directories
Use: Configuration mapping, constant consolidation
```

### Pattern 6: Finding Error Handling

```
Query: "try" AND "catch" AND "finally" OR "except"
Explanation: Find exception handling blocks
Use: Error handling audit, consistency review
Scope: file or module for manageable results
```

### Pattern 7: Finding Security-Related Code

```
Query: "password" OR "secret" OR "token" AND NOT "comment"
Explanation: Find code handling sensitive data
Use: Security audit, vulnerability detection
Important: Review carefully to avoid exposing secrets
```

## Common Search Mistakes & How to Fix Them

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too broad keyword | 500+ matches, unusable | Add specificity or path constraint |
| Typos in query | 0 matches | Check spelling, check synonyms |
| Forgetting scope | Searching whole codebase when module would suffice | Use `--scope module:path` to narrow |
| Using AND incorrectly | Boolean logic inverted expectations | Test with simple case first |
| Over-complex regex | Pattern doesn't compile | Test regex separately, simplify |
| Case sensitivity | Missing matches | Most searches case-insensitive by default |
| Escaping issues | Special chars break query | Quote strings, escape backslashes |

## Query Formulation Checklist

Before running a search:

- [ ] What am I looking for? (Be specific)
- [ ] What layer/scope is most relevant? (file/module/codebase)
- [ ] What keywords best describe it?
- [ ] Will this be too broad? Too narrow? Just right?
- [ ] Are there false positives to exclude with NOT?
- [ ] Is case sensitivity relevant?
- [ ] Should I filter by language?
- [ ] Should I filter by file path?
- [ ] Is this a regex pattern or keyword search?

## Examples

### Example 1: Find all database queries
```
Search: "SELECT" OR "INSERT" OR "UPDATE" OR "DELETE"
Scope: codebase
Result: All SQL queries
Use: SQL injection audit, query performance review
```

### Example 2: Find all API endpoints
```
Search: lang:typescript path:**/routes/* "router\." OR "@Route"
Scope: module:src/api
Result: All endpoint definitions
Use: API surface mapping, endpoint documentation
```

### Example 3: Find memory leak candidates
```
Search: "addEventListener" AND NOT "removeEventListener"
Scope: module:src/ui
Result: Event listeners without cleanup
Use: Memory leak detection, cleanup audits
```

### Example 4: Find TODO comments
```
Search: /\/\/\s*TODO/ OR /\/\*.*TODO.*\*\//
Scope: codebase
Result: All TODO comments
Use: Technical debt discovery, backlog planning
```
```

**Step 2: Validate file creation**

Run: `wc -l plugins/gemini-codebase-intelligence/skills/codebase-search-strategies/SKILL.md`
Expected: 300+ lines

---

## Task 6: Create Third Skill - Gemini CLI Configuration

**Files:**
- Create: `plugins/gemini-codebase-intelligence/skills/gemini-cli-configuration/SKILL.md`

**Step 1: Write the skill**

```markdown
---
name: gemini-cli-configuration
description: Setup, installation, authentication, and optimization of Gemini CLI. Covers environment configuration, API credentials, performance tuning, and troubleshooting common issues. Use when initializing Gemini CLI or resolving configuration problems.
---

# Gemini CLI Configuration Skill

## When to Use This Skill

- Setting up Gemini CLI for first-time use
- Configuring authentication and API access
- Optimizing performance for large codebase analysis
- Troubleshooting connection or permission issues
- Migrating configuration across machines
- Enabling advanced features (caching, parallelization)

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Network connectivity to Gemini API
- Git (for codebase analysis)

### Basic Installation

```bash
# Install Gemini CLI
pip install gemini-cli

# Verify installation
gemini --version

# Expected output: gemini version X.Y.Z
```

### Installation Verification

```bash
# Check CLI is in PATH
which gemini

# Expected: /usr/local/bin/gemini (or similar)

# Check Python dependencies
gemini doctor

# Expected: All checks pass
```

### Troubleshooting Installation

| Issue | Cause | Fix |
|-------|-------|-----|
| "gemini: command not found" | Not in PATH | Reinstall with `pip install --upgrade gemini-cli` |
| "ModuleNotFoundError" | Dependency missing | Run `pip install --upgrade gemini-cli` |
| "Permission denied" | File permissions | Run with `python -m gemini` |

## Authentication

### Getting API Credentials

1. Go to https://gemini.google.com/api/keys
2. Create new API key
3. Copy the key (save securely!)
4. Configure locally

### Configuration Methods

#### Method 1: Environment Variable (Recommended for CI/CD)

```bash
# Set API key
export GEMINI_API_KEY="your_api_key_here"

# Verify
echo $GEMINI_API_KEY

# Test authentication
gemini auth verify
```

#### Method 2: Configuration File (Recommended for local development)

```bash
# Initialize configuration
gemini auth login

# Follow interactive prompt, enter API key when requested
# Configuration stored in ~/.gemini/config.json
```

#### Method 3: Command Line (Not recommended, visible in shell history)

```bash
gemini --api-key "your_api_key" search "query"
```

### Configuration File Structure

Location: `~/.gemini/config.json`

```json
{
  "api_key": "sk-...",
  "api_endpoint": "https://api.gemini.google.com",
  "timeout": 30,
  "cache_dir": "~/.gemini/cache",
  "cache_enabled": true,
  "cache_ttl": 3600,
  "parallelization": {
    "enabled": true,
    "workers": 4,
    "batch_size": 100
  },
  "output_format": "json",
  "verbosity": "info"
}
```

### Configuration Options Explained

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `api_key` | string | Required | Gemini API authentication key |
| `api_endpoint` | string | Official | Custom API endpoint (advanced) |
| `timeout` | int | 30 | Request timeout in seconds |
| `cache_enabled` | bool | true | Enable local caching of results |
| `cache_ttl` | int | 3600 | Cache time-to-live in seconds |
| `cache_dir` | string | ~/.gemini/cache | Where to store cache |
| `parallelization.enabled` | bool | false | Enable parallel analysis |
| `parallelization.workers` | int | 4 | Number of parallel workers |
| `parallelization.batch_size` | int | 100 | Items per batch |
| `output_format` | enum | json | Result format (json, markdown) |
| `verbosity` | enum | info | Log level (debug, info, warn, error) |

## Performance Optimization

### For Large Codebases (>100k files)

```json
{
  "cache_enabled": true,
  "cache_ttl": 86400,
  "parallelization": {
    "enabled": true,
    "workers": 8
  },
  "timeout": 60
}
```

### For Small Codebases (<10k files)

```json
{
  "cache_enabled": true,
  "cache_ttl": 3600,
  "parallelization": {
    "enabled": false
  },
  "timeout": 15
}
```

### Caching Strategy

**What gets cached:**
- Search results (normalized queries)
- Pattern analysis results
- File metadata (size, modification time)

**What doesn't get cached:**
- Real-time analysis (code smell detection)
- Dynamic analysis results
- User-specific results

**Cache management:**
```bash
# View cache size
gemini cache status

# Clear old cache
gemini cache clear --older-than 7d

# Disable caching for single command
gemini search --no-cache "query"

# Force refresh (ignore cache)
gemini search --refresh "query"
```

## Troubleshooting

### Authentication Issues

**Error: "Invalid API key"**
```bash
# Verify key is set
echo $GEMINI_API_KEY

# Test authentication
gemini auth verify

# Regenerate key if needed, update configuration
```

**Error: "Access denied"**
```bash
# Check API key permissions
gemini auth info

# Contact support if key is valid but access denied
```

### Performance Issues

**Searches are slow:**
```bash
# Check cache is enabled
gemini config view | grep cache_enabled

# Enable caching if disabled
gemini config set cache_enabled true

# Monitor execution time
gemini search --verbose "query"

# Consider narrowing scope
gemini search --scope module:path "query"
```

**CLI not responding:**
```bash
# Check if Gemini API is accessible
curl https://api.gemini.google.com/health

# Increase timeout if network is slow
gemini config set timeout 60

# Check rate limiting
gemini rate-limit status
```

### Installation Issues

**"Module not found" errors:**
```bash
# Reinstall with dependencies
pip install --upgrade --force-reinstall gemini-cli

# Check Python version (need 3.8+)
python --version
```

**Different behavior across machines:**
```bash
# Export configuration between machines
gemini config export > config.json

# Import on new machine
gemini config import config.json

# Verify settings match
gemini config view
```

## Environment Setup for Team

### Shared Configuration

```bash
# Create team config in repository
mkdir -p .gemini-config
cat > .gemini-config/.gemini-config.json << 'EOF'
{
  "cache_enabled": true,
  "parallelization": {"enabled": true, "workers": 4},
  "output_format": "json"
}
EOF

# Export to environment
export GEMINI_CONFIG_DIR=".gemini-config"

# Each developer still needs their own API key:
export GEMINI_API_KEY="your_key_here"
```

### CI/CD Integration

```yaml
# .github/workflows/analyze.yml
name: Codebase Analysis
on: [push]
jobs:
  analyze:
    runs-on: ubuntu-latest
    env:
      GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    steps:
      - uses: actions/checkout@v2
      - name: Install Gemini CLI
        run: pip install gemini-cli
      - name: Run codebase analysis
        run: gemini analyze-patterns singleton --scope codebase
```

## Advanced Configuration

### Custom Analysis Scripts

```bash
# Create analysis script
cat > scripts/analyze.sh << 'EOF'
#!/bin/bash
set -e

echo "Running pattern analysis..."
gemini analyze-patterns --scope codebase > results/patterns.json

echo "Searching for TODOs..."
gemini search "TODO" > results/todos.json

echo "Checking dependencies..."
gemini execute-complex dependency-map > results/dependencies.json

echo "Analysis complete!"
EOF

chmod +x scripts/analyze.sh
```

### Scheduled Analysis

```bash
# Add to crontab for nightly analysis
0 2 * * * /path/to/scripts/analyze.sh >> /var/log/gemini-analysis.log 2>&1
```

## Verification Checklist

After setup, verify everything works:

- [ ] Gemini CLI installed and in PATH
- [ ] API key configured and verified with `gemini auth verify`
- [ ] Can run simple search: `gemini search "test"`
- [ ] Cache is working: Check `~/.gemini/cache` directory
- [ ] Parallelization working (if enabled): Monitor CPU usage
- [ ] Configuration matches team standards
- [ ] Documentation updated with team setup instructions

## Support & Debugging

```bash
# Enable verbose logging
gemini --verbose search "query"

# Generate debug report for support
gemini diagnostic-report > ~/gemini-debug.json

# Check CLI version and dependencies
gemini version
gemini doctor
```
```

**Step 2: Validate creation**

Run: `wc -l plugins/gemini-codebase-intelligence/skills/gemini-cli-configuration/SKILL.md`
Expected: 250+ lines

---

## Task 7: Create Fourth Skill - Analysis Result Interpretation

**Files:**
- Create: `plugins/gemini-codebase-intelligence/skills/analysis-result-interpretation/SKILL.md`

**Step 1: Write the skill**

```markdown
---
name: analysis-result-interpretation
description: Interprets and acts on analysis results from Gemini CLI. Covers result formats, confidence levels, actionability assessment, decision frameworks, and communication strategies. Use when deciding how to respond to analysis findings or formulating follow-up actions.
---

# Analysis Result Interpretation Skill

## When to Use This Skill

- Understanding what Gemini CLI analysis results mean
- Deciding what action to take based on findings
- Interpreting confidence levels and relevance scores
- Formatting analysis results for team communication
- Bridging gap between analysis output and business decisions
- Determining when additional investigation is needed

## Result Format Understanding

### JSON Result Structure

Gemini CLI returns structured JSON with consistent format:

```json
{
  "status": "success|error|partial",
  "command": "original_command_executed",
  "query_time_ms": 1234,
  "codebase_size": {
    "files": 5000,
    "lines_of_code": 1000000
  },
  "results": [
    {
      "type": "finding",
      "severity": "critical|high|medium|low|info",
      "confidence": 0.95,
      "location": "path/to/file.ts:123",
      "context": "Code snippet showing context",
      "description": "What was found",
      "impact": "Why it matters",
      "recommendation": "What to do about it",
      "tags": ["performance", "security"]
    }
  ],
  "summary": {
    "total_findings": 42,
    "by_severity": {
      "critical": 2,
      "high": 5,
      "medium": 15,
      "low": 20
    }
  },
  "metadata": {
    "execution_time_ms": 5000,
    "scope": "codebase",
    "timestamp": "2025-10-26T10:30:00Z"
  }
}
```

### Understanding Confidence Scores

| Confidence | Meaning | Actionability |
|------------|---------|---------------|
| 0.95-1.0 | Virtually certain | Take action immediately |
| 0.85-0.94 | Very likely | Prioritize for review/action |
| 0.70-0.84 | Likely | Include in backlog, review |
| 0.50-0.69 | Moderate confidence | Investigate further before action |
| <0.50 | Low confidence | Flag for human review, don't act |

### Understanding Severity Levels

| Severity | Urgency | Response Timeline | Example |
|----------|---------|-------------------|---------|
| Critical | Immediate | Fix today, blocks work | Active memory leak, security vulnerability |
| High | This week | Prioritize for sprint | Large refactoring need, major code smell |
| Medium | This month | Include in planning | Code duplication, minor architectural issue |
| Low | Backlog | Address in refactoring | Style issue, minor improvement |
| Info | Context only | Reference material | Code structure information, statistics |

## Actionability Assessment

When you see results, ask:

### 1. Is this Confident Enough?
- Confidence > 0.85? → Proceed with action
- Confidence 0.70-0.85? → Review with team before action
- Confidence < 0.70? → Investigate further, don't assume

### 2. Is This Severity Justified?
- Critical finding about non-critical code? → Downgrade to High
- Low-level finding about critical code? → Upgrade to Medium
- Does severity match business impact? → Adjust as needed

### 3. Is This Actionable Right Now?
- Can fix in next 1-2 days? → Add to sprint
- Would require large refactor? → Add to backlog with estimation
- Requires investigation first? → Create investigation task
- Needs team discussion? → Schedule design review

### 4. What's the Cost-Benefit?
- Effort to fix: Low effort + High impact → Do immediately
- Effort to fix: High effort + Low impact → Defer to backlog
- Effort to fix: High effort + High impact → Estimate and prioritize
- Effort to fix: Low effort + Low impact → Nice-to-have, do if time allows

## Result Interpretation Patterns

### Pattern 1: Security Finding

```json
{
  "severity": "critical",
  "description": "SQL injection vulnerability in user search",
  "location": "src/api/users.ts:45",
  "impact": "Attacker could access database directly",
  "recommendation": "Use parameterized queries"
}
```

**Interpretation:**
- Confidence + Critical severity = Act immediately
- Check if vulnerability is exploitable in current code path
- Create security incident if in production
- Fix and deploy as hotfix
- Add regression test

**Action:** IMMEDIATE

### Pattern 2: Code Smell Finding

```json
{
  "severity": "medium",
  "description": "Large class with 50+ methods",
  "location": "src/services/UserService.ts:1-2000",
  "impact": "Hard to test, maintain, understand",
  "recommendation": "Extract domain responsibilities into separate classes"
}
```

**Interpretation:**
- Medium severity + moderate confidence = Prioritize for next sprint
- Estimate refactoring effort (likely 2-3 days)
- Break into smaller refactoring PRs
- Add to backlog with estimated story points

**Action:** BACKLOG (HIGH PRIORITY)

### Pattern 3: Informational Finding

```json
{
  "severity": "info",
  "description": "Codebase uses 12 different HTTP client libraries",
  "location": "Multiple files",
  "impact": "Inconsistency, maintenance burden",
  "recommendation": "Standardize on one HTTP client across codebase"
}
```

**Interpretation:**
- Info level = FYI, context for decisions
- Not urgent but worth addressing in long-term planning
- Could be addressed during architectural refactoring
- Use as input to tech strategy discussions

**Action:** STRATEGIC PLANNING

## Decision Framework

```
Result received
├─ Status = error?
│   └─ Investigation needed → Debug Gemini CLI execution
│
├─ Status = partial?
│   └─ Some results missing → Re-run with broader scope
│
└─ Status = success?
    ├─ Severity = critical?
    │   ├─ Confidence > 0.85?
    │   │   └─ ACTION: Fix immediately, security incident if needed
    │   └─ Confidence < 0.85?
    │       └─ ACTION: Verify before acting
    │
    ├─ Severity = high?
    │   ├─ Effort < 1 day?
    │   │   └─ ACTION: Schedule for current sprint
    │   └─ Effort > 1 day?
    │       └─ ACTION: Estimate and add to backlog
    │
    ├─ Severity = medium?
    │   └─ ACTION: Add to backlog, schedule for future sprint
    │
    └─ Severity = low|info?
        └─ ACTION: Reference material or nice-to-have
```

## Communication Strategies

### For Leadership (Executive Summary)

Focus on business impact:

```markdown
# Codebase Analysis Summary

**Critical Issues:** 2 (Security vulnerabilities in auth module)
**High Issues:** 8 (Technical debt in data layer)
**Total Refactoring Effort Estimate:** 3 weeks

**Recommendation:** Prioritize security issues immediately (production impact),
schedule tech debt fixes for Q4 planning (maintainability improvement).
```

### For Development Team (Detailed Report)

Focus on how-to-fix:

```markdown
# Codebase Analysis - Developer Briefing

## Critical: SQL Injection in User Search
- **Location:** src/api/users.ts:45
- **Current Code:** `query = "SELECT * FROM users WHERE name='" + input + "'"`
- **Issue:** User input not escaped, allows SQL injection
- **Fix:** Use parameterized query: `db.query("SELECT * FROM users WHERE name=?", [input])`
- **Effort:** 1 hour
- **Testing:** Add unit test with injection payload

## High: Large UserService Class
- **Location:** src/services/UserService.ts
- **Size:** 2000 lines, 50+ methods
- **Issue:** Multiple responsibilities (user CRUD, auth, notifications)
- **Refactoring Plan:**
  1. Extract UserRepository (CRUD operations)
  2. Extract AuthService (authentication logic)
  3. Extract UserNotificationService (notifications)
- **Effort:** 3 days across 3 PRs
```

### For Stakeholders (Business Impact)

Focus on implications:

```markdown
# Technical Health Report

**Code Quality:** 6/10 (declining)
**Security:** 4/10 (2 critical vulnerabilities)
**Maintainability:** 5/10 (increasing technical debt)

**Impact on Velocity:**
- Current issues causing 20% of PR review rework
- Security issues pose business liability risk
- Tech debt slowing feature development by 15%

**Recommended Action:** Allocate 2 sprints for priority fixes
(ROI: 20% velocity improvement + risk reduction)
```

## Special Cases

### Case 1: High Confidence, Low Severity Finding

Example: "Database has unused indexes"

**Decision:** Low priority, but zero-cost optimization
**Action:** Include in maintenance window, don't create emergency ticket

### Case 2: Low Confidence, High Severity Finding

Example: "Possible memory leak (confidence 0.45)"

**Decision:** Cannot act on low confidence, but cannot ignore
**Action:** Create investigation task, require manual verification before fixing

### Case 3: Multiple Related Findings

Example: 5 different code smell findings in same class

**Decision:** Address together as unified refactoring
**Action:** Create single epic/story covering all related issues

## Follow-Up Questions

After reviewing analysis results, ask:

1. **Verification:** Have I verified this finding is accurate?
2. **Scope:** Is this finding relevant to current priorities?
3. **Priority:** Should this block other work?
4. **Cost:** Do I understand effort to fix?
5. **Benefit:** Is the benefit worth the effort?
6. **Timeline:** When should this be addressed?
7. **Owner:** Who should own the fix?
8. **Prevention:** How do we prevent this pattern recurring?

## Common Misinterpretations

| Misinterpretation | Reality | Correction |
|---|---|---|
| "Low confidence = probably wrong" | Low confidence = needs verification | Verify manually before dismissing |
| "Medium severity = not important" | Medium severity = should be fixed | Plan for next 1-2 sprints |
| "Info level = ignore" | Info = context for decisions | Use for strategic planning |
| "Many findings = crisis" | Could be normal variation | Assess trends over time |
| "One result = complete analysis" | Results are snapshot | Rerun analysis periodically |

## Trend Monitoring

Track results over time:

```
Weekly: Critical + High issues count
├─ Increasing? → Red flag, address immediately
├─ Stable? → Maintain current discipline
└─ Decreasing? → Good progress, continue

Monthly: Code quality trend
├─ Category breakdown (security, performance, structure)
├─ Average issue resolution time
└─ Tech debt growth rate
```
```

**Step 2: Validate file**

Run: `wc -l plugins/gemini-codebase-intelligence/skills/analysis-result-interpretation/SKILL.md`
Expected: 250+ lines

---

## Task 8: Create Three Specialized Commands

**Files:**
- Create: `plugins/gemini-codebase-intelligence/commands/analyze-codebase.md`
- Create: `plugins/gemini-codebase-intelligence/commands/search-patterns.md`
- Create: `plugins/gemini-codebase-intelligence/commands/execute-analysis.md`

**Step 1: Create analyze-codebase command**

```markdown
---
name: analyze-codebase
description: Full architectural overview and codebase intelligence. Executes comprehensive analysis including structure mapping, pattern detection, dependency analysis, and quality assessment. Returns structured report with findings and recommendations.
---

# Analyze Codebase Command

## Overview

This command provides a comprehensive architectural overview of your entire codebase. It detects patterns, maps dependencies, identifies code smells, and assesses overall code quality in a single execution.

## Usage

```bash
/analyze-codebase [OPTIONS]
```

## Options

- `--scope [file|module|codebase]` - Analysis scope (default: codebase)
- `--include-patterns` - Include design pattern detection
- `--include-smells` - Include code smell detection
- `--include-dependencies` - Include dependency mapping
- `--format [json|markdown]` - Output format (default: markdown)
- `--output [file]` - Save results to file
- `--no-cache` - Force fresh analysis, ignore cache

## Examples

### Basic Usage
```bash
/analyze-codebase
```
Outputs full architectural analysis in markdown format.

### JSON Output for Programmatic Use
```bash
/analyze-codebase --format json --output results.json
```
Saves structured JSON results for further processing.

### Module-Specific Analysis
```bash
/analyze-codebase --scope module:src/auth
```
Analyzes authentication module in detail.

### Comprehensive Report
```bash
/analyze-codebase --include-patterns --include-smells --include-dependencies
```
Includes all analysis types in one comprehensive report.

## Output Structure

```
# Codebase Architecture Analysis

## Executive Summary
[High-level overview with key findings]

## Structural Analysis
### Directory Structure
[Root-level organization and layering]

### Module Breakdown
[Major modules and responsibilities]

### Dependency Graph
[High-level dependency relationships]

## Pattern Analysis
### Design Patterns Detected
[Implemented patterns with locations]

### Code Smells
[Code quality issues by severity]

### Anti-Patterns
[Architectural issues identified]

## Quality Metrics
[Code complexity, coverage, health scores]

## Recommendations
[Prioritized list of improvements]
```

## Common Use Cases

1. **New team member onboarding** - Get architectural overview quickly
2. **Pre-refactoring assessment** - Understand current state before changes
3. **Dependency planning** - Identify modules and their relationships
4. **Technical debt audit** - Comprehensive smell detection
5. **Architecture documentation** - Generate reference for team

## Integration with Other Skills

- **Pattern Detection Skill** - Understand what patterns mean
- **Analysis Result Interpretation Skill** - Act on recommendations
- **Codebase Search Strategies** - Follow up with targeted searches
```

**Step 2: Create search-patterns command**

```markdown
---
name: search-patterns
description: Targeted pattern detection across codebase. Searches for specific design patterns, code smells, or anti-patterns. Returns locations, context, and architectural implications with actionable recommendations.
---

# Search Patterns Command

## Overview

Search for specific design patterns, code smells, or anti-patterns in your codebase. More focused than full analysis, allowing targeted investigation of specific pattern types.

## Usage

```bash
/search-patterns <pattern_type> [OPTIONS]
```

## Supported Pattern Types

### Design Patterns
- `singleton` - Find Singleton pattern implementations
- `factory` - Find Factory pattern implementations
- `observer` - Find Observer pattern implementations
- `strategy` - Find Strategy pattern implementations
- `decorator` - Find Decorator pattern implementations
- `adapter` - Find Adapter pattern implementations
- `facade` - Find Facade pattern implementations
- `builder` - Find Builder pattern implementations

### Code Smells
- `large-class` - Classes with too many responsibilities
- `long-method` - Functions that are too long
- `duplicated-code` - Code duplication detection
- `feature-envy` - Methods using other classes more than own
- `data-clumps` - Variables used together
- `global-variables` - Global state detection
- `primitive-obsession` - Over-reliance on primitives

### Anti-Patterns
- `circular-dependency` - Circular module dependencies
- `tight-coupling` - Overly dependent modules
- `god-object` - Classes that know/do too much
- `service-locator` - Service locator pattern usage
- `big-ball-of-mud` - Structural chaos detection

## Options

- `--scope [file|module|codebase]` - Analysis scope
- `--severity [critical|high|medium|low|info]` - Filter by severity
- `--confidence [0.0-1.0]` - Minimum confidence threshold
- `--format [json|markdown]` - Output format
- `--output [file]` - Save results to file
- `--no-cache` - Force fresh search

## Examples

### Find All Singletons
```bash
/search-patterns singleton
```
Lists all Singleton pattern implementations with locations and assessment.

### Find Code Smells in Specific Module
```bash
/search-patterns code-smell --scope module:src/api
```
Identifies all code smell instances in the API module.

### Critical Issues Only
```bash
/search-patterns anti-pattern --severity critical
```
Shows only critical anti-pattern findings.

### High-Confidence Pattern Search
```bash
/search-patterns large-class --confidence 0.9
```
Returns only high-confidence findings of large classes.

## Output Format

```
# Pattern Search: [Pattern Type]

## Summary
- Total instances found: N
- Severity breakdown: [by severity]
- Confidence average: X%

## Findings

### Finding 1: [Pattern Name] at location
**Location:** path/to/file.ts:123
**Confidence:** 95%
**Context:** [Code snippet]
**Explanation:** Why this is an instance of the pattern
**Implication:** What this means architecturally
**Recommendation:** What to do about it

### Finding 2: ...
```

## Common Use Cases

1. **Pattern consistency** - Ensure patterns are used correctly throughout codebase
2. **Code quality audit** - Find and prioritize code smells
3. **Architecture review** - Identify architectural anti-patterns
4. **Refactoring planning** - Identify candidates for refactoring
5. **Code review feedback** - Reference for PR comments
```

**Step 3: Create execute-analysis command**

```markdown
---
name: execute-analysis
description: Execute complex custom analysis tasks. Supports dependency mapping, architecture visualization, refactoring suggestions, dead code detection, and other advanced analysis. Requires specifying analysis type and optional parameters.
---

# Execute Analysis Command

## Overview

Execute sophisticated analysis tasks beyond basic pattern detection. Includes dependency mapping, refactoring suggestions, performance analysis, and custom analyses.

## Usage

```bash
/execute-analysis <analysis_type> [OPTIONS]
```

## Supported Analysis Types

### Architecture Analysis
- `dependency-map` - Map all module dependencies
- `architecture-overview` - Structural and layering analysis
- `module-boundary-analysis` - Analyze module isolation
- `layer-analysis` - Check architectural layering patterns

### Code Quality
- `dead-code-detection` - Find unused functions and variables
- `complexity-analysis` - Measure cyclomatic complexity
- `test-coverage-analysis` - Analyze test coverage patterns
- `unused-imports-detection` - Find and list unused imports

### Refactoring
- `refactoring-suggestions` - Provide refactoring recommendations
- `consolidation-opportunities` - Find code consolidation points
- `extract-service-suggestions` - Suggest service extraction
- `extract-library-suggestions` - Suggest library extraction

### Performance
- `performance-bottlenecks` - Identify performance issues
- `n-plus-one-detection` - Find N+1 query patterns
- `memory-leak-detection` - Identify potential memory leaks
- `inefficiency-patterns` - Find algorithmic inefficiencies

### Security
- `security-audit` - Security vulnerability scan
- `dependency-vulnerability-scan` - Check for vulnerable dependencies
- `secret-detection` - Find exposed secrets or credentials
- `authentication-audit` - Review auth implementations

## Options

- `--scope [file|module|codebase]` - Analysis scope
- `--format [json|markdown]` - Output format
- `--output [file]` - Save results
- `--depth [shallow|medium|deep]` - Analysis depth
- `--params [json]` - Custom parameters for analysis
- `--no-cache` - Force fresh analysis

## Examples

### Map All Dependencies
```bash
/execute-analysis dependency-map --format json
```
Creates complete dependency graph of codebase.

### Find Dead Code
```bash
/execute-analysis dead-code-detection --depth deep
```
Performs comprehensive analysis to find unused code.

### Get Refactoring Suggestions
```bash
/execute-analysis refactoring-suggestions --scope module:src/api --format markdown
```
Provides targeted refactoring recommendations for API module.

### Security Audit
```bash
/execute-analysis security-audit --depth deep --output security-report.json
```
Comprehensive security review with detailed findings.

## Output Example

```
# [Analysis Type] Analysis Results

## Summary
[Key findings and statistics]

## Detailed Findings
[Breakdown by category]

## Metrics
[Quantitative analysis results]

## Recommendations
[Prioritized list of actions]

## Timeline
[Suggested implementation order]
```

## Integration Pattern

These analyses often feed into other workflows:

1. **Run analysis** → Get findings and recommendations
2. **Use Analysis Result Interpretation Skill** → Decide on actions
3. **Use Codebase Search Strategies** → Investigate specific findings
4. **Create implementation plan** → Address high-priority items

## Complex Parameters

For advanced analysis, pass custom parameters:

```bash
/execute-analysis dependency-map --params '{"exclude_tests": true, "show_external": false}'
```

## Performance Notes

- Large codebase analysis may take 1-5 minutes
- Use `--depth shallow` for quick preliminary analysis
- Use `--depth deep` for comprehensive review
- Results are cached for repeated queries

## When to Use Each Analysis Type

| Type | Use When | Time | Scope |
|------|----------|------|-------|
| dependency-map | Understanding architecture | 2 min | Full |
| dead-code | Cleaning up codebase | 3 min | Full |
| refactoring-suggestions | Planning improvements | 2 min | Module |
| security-audit | Before production | 5 min | Full |
| performance-bottlenecks | Optimization needed | 3 min | Module |
```

**Step 4: Verify all commands created**

Run: `ls -la plugins/gemini-codebase-intelligence/commands/`
Expected: Three markdown files created

---

## Task 9: Update Marketplace Manifest

**Files:**
- Modify: `.claude-plugin/marketplace.json`

**Step 1: Read marketplace.json**

Run: `cat .claude-plugin/marketplace.json | jq . | head -50`
Expected: JSON structure showing existing plugins

**Step 2: Add plugin entry to marketplace**

Edit `.claude-plugin/marketplace.json` to add:

```json
{
  "name": "gemini-codebase-intelligence",
  "source": "./plugins/gemini-codebase-intelligence",
  "description": "Manages Gemini CLI for large codebase analysis and pattern detection. Provides intelligent hybrid routing (Gemini for complex analysis, local tools for fast searches), three command families (search, analyze-patterns, execute-complex), and four specialized skills. Use PROACTIVELY when Claude needs to analyze extensive code patterns, architectural overviews, or search through large codebases efficiently.",
  "version": "1.0.0",
  "category": "code-analysis",
  "commands": [
    "./commands/analyze-codebase.md",
    "./commands/search-patterns.md",
    "./commands/execute-analysis.md"
  ],
  "agents": [
    "./agents/codebase-analysis-gateway.md",
    "./agents/gemini-cli-executor.md"
  ],
  "skills": [
    "./skills/pattern-detection",
    "./skills/codebase-search-strategies",
    "./skills/gemini-cli-configuration",
    "./skills/analysis-result-interpretation"
  ]
}
```

**Step 3: Validate JSON syntax**

Run: `jq . .claude-plugin/marketplace.json > /dev/null && echo "Valid JSON"`
Expected: "Valid JSON"

---

## Task 10: Create Plugin Documentation

**Files:**
- Create: `plugins/gemini-codebase-intelligence/README.md`

**Step 1: Write README**

```markdown
# Gemini CLI Codebase Intelligence Plugin

Intelligent management of Gemini CLI for large codebase analysis, pattern detection, and complex code intelligence.

## Overview

This plugin provides a production-ready system for analyzing extensive codebases efficiently. It uses a hybrid approach:
- **Simple searches** → Local Explore agents (fast, zero-cost)
- **Pattern detection** → Gemini CLI (powerful ML-backed analysis)
- **Complex analysis** → Gemini CLI with multi-step reasoning

## Quick Start

### Installation

The plugin is already registered in the Claude Code marketplace. To use it:

```bash
# Verify Gemini CLI is installed
gemini --version

# Configure authentication
gemini auth login

# Start using analysis commands
```

### Basic Usage

```bash
# Analyze entire codebase architecture
/analyze-codebase

# Search for specific pattern
/search-patterns singleton

# Execute complex analysis
/execute-analysis dependency-map
```

## Components

### Agents (2)

1. **CodebaseAnalysisGateway** (Sonnet)
   - Intelligent routing based on query complexity
   - Result aggregation and caching
   - Fallback to local tools when Gemini unavailable

2. **GeminiCLIExecutor** (Haiku)
   - Wraps Gemini CLI execution
   - Output parsing and error handling
   - Parameter management

### Commands (3)

1. **analyze-codebase** - Full architectural analysis with patterns, dependencies, quality metrics
2. **search-patterns** - Targeted search for design patterns, code smells, anti-patterns
3. **execute-analysis** - Complex analysis: dependency mapping, refactoring suggestions, security audits

### Skills (4)

1. **pattern-detection** - Understand design patterns, code smells, anti-patterns
2. **codebase-search-strategies** - Effective query formulation for searches
3. **gemini-cli-configuration** - Setup, authentication, optimization
4. **analysis-result-interpretation** - Decision frameworks for analysis results

## Use Cases

### For Developers
- Quick architectural overview of large codebases
- Find specific patterns or code smells
- Identify refactoring opportunities
- Navigate unfamiliar code

### For Teams
- Consistent codebase analysis across team
- Knowledge sharing about code patterns
- Automated technical debt tracking
- Standardized analysis workflows

### For Organizations
- Codebase quality metrics
- Security audit automation
- Architecture visualization
- Technical strategy planning

## Workflow Examples

### Example 1: Onboarding New Developer
```bash
/analyze-codebase
# Provides complete architecture overview

/search-patterns singleton
# Shows architectural patterns used

/codebase-search-strategies
# Learn how to do targeted searches yourself
```

### Example 2: Pre-Refactoring Assessment
```bash
/analyze-codebase --include-smells --include-dependencies
# Understand current state

/execute-analysis refactoring-suggestions --scope module:src/api
# Get specific recommendations

/analysis-result-interpretation
# Understand how to act on findings
```

### Example 3: Security Audit
```bash
/execute-analysis security-audit --depth deep
# Run comprehensive security analysis

/search-patterns anti-pattern --severity critical
# Find critical architectural issues

/execute-analysis secret-detection
# Detect exposed credentials
```

## Performance Considerations

### Large Codebase (>100k files)
- Use caching to avoid repeated analysis
- Start with module-scoped searches
- Run complex analysis off-peak

### Small Codebase (<10k files)
- Full codebase analysis typically < 1 minute
- Caching provides minimal benefit
- Can run analysis frequently

## Configuration

See `gemini-cli-configuration` skill for:
- Installation instructions
- Authentication setup
- Performance optimization
- CI/CD integration

## Troubleshooting

### "Gemini CLI not found"
```bash
pip install gemini-cli
gemini auth login
```

### "Analysis is slow"
```bash
# Enable caching
gemini config set cache_enabled true

# Use narrower scope
/search-patterns singleton --scope module:src/api
```

### "Low confidence results"
See `analysis-result-interpretation` skill for handling uncertain findings.

## Documentation

- **Pattern Detection** - `skills/pattern-detection/SKILL.md`
- **Search Strategies** - `skills/codebase-search-strategies/SKILL.md`
- **CLI Configuration** - `skills/gemini-cli-configuration/SKILL.md`
- **Result Interpretation** - `skills/analysis-result-interpretation/SKILL.md`

## Architecture

```
User Request
  ↓
CodebaseAnalysisGateway (routing decision)
  ├→ Simple? → Explore agent (fast)
  ├→ Pattern? → GeminiCLIExecutor → Pattern Skill
  └→ Complex? → GeminiCLIExecutor → Advanced analysis
  ↓
Result aggregation & formatting
  ↓
Output to user
```

## Advanced Usage

### Custom Analysis Scripts

Create analysis workflows combining multiple commands:

```bash
#!/bin/bash

echo "=== Architecture Analysis ==="
/analyze-codebase --format json > architecture.json

echo "=== Pattern Detection ==="
/search-patterns large-class > smells.json

echo "=== Refactoring Opportunities ==="
/execute-analysis refactoring-suggestions > refactoring.json

echo "All analyses complete!"
```

### CI/CD Integration

Use in GitHub Actions or similar for continuous analysis:

```yaml
- name: Analyze codebase
  run: |
    /analyze-codebase --output codebase-analysis.json
    /execute-analysis security-audit --output security.json
```

## Contributing

To extend this plugin:

1. Add new analysis types to commands
2. Add specialized skills for new analysis domains
3. Update marketplace.json with new components
4. Document in README

## Support

For issues or questions:
- Check skill documentation first
- Review `gemini-cli-configuration` for setup issues
- Consult `analysis-result-interpretation` for understanding results
```

**Step 2: Verify file**

Run: `wc -l plugins/gemini-codebase-intelligence/README.md`
Expected: 250+ lines

---

## Task 11: Verify Complete Plugin Structure

**Files:**
- Verify: Entire plugin directory structure

**Step 1: List complete structure**

Run: `tree plugins/gemini-codebase-intelligence/ 2>/dev/null || find plugins/gemini-codebase-intelligence -type f | sort`
Expected: Shows all created files organized by type

**Step 2: Verify all agents exist**

Run: `ls plugins/gemini-codebase-intelligence/agents/`
Expected: codebase-analysis-gateway.md, gemini-cli-executor.md

**Step 3: Verify all commands exist**

Run: `ls plugins/gemini-codebase-intelligence/commands/`
Expected: analyze-codebase.md, search-patterns.md, execute-analysis.md

**Step 4: Verify all skills exist**

Run: `ls plugins/gemini-codebase-intelligence/skills/`
Expected: pattern-detection, codebase-search-strategies, gemini-cli-configuration, analysis-result-interpretation

**Step 5: Count total files**

Run: `find plugins/gemini-codebase-intelligence -type f | wc -l`
Expected: 12+ files (2 agents + 3 commands + 4 skills + README + marketplace reference)

**Step 6: Validate all markdown files**

Run: `find plugins/gemini-codebase-intelligence -name "*.md" -exec wc -l {} + | tail -1`
Expected: Shows total lines across all markdown files (should be 2000+)

---

## Task 12: Commit Plugin to Git

**Files:**
- All created plugin files

**Step 1: Check git status**

Run: `git status`
Expected: Shows untracked files in plugins/gemini-codebase-intelligence directory

**Step 2: Add plugin files**

Run: `git add plugins/gemini-codebase-intelligence/ .claude-plugin/marketplace.json`

**Step 3: Verify staged changes**

Run: `git status`
Expected: Shows staged files ready for commit

**Step 4: Create commit**

Run: `git commit -m "$(cat <<'EOF'\nfeat: add gemini-codebase-intelligence plugin with hybrid analysis architecture\n\n- Adds CodebaseAnalysisGateway agent for intelligent routing between Gemini CLI and local tools\n- Adds GeminiCLIExecutor agent for reliable Gemini CLI command execution\n- Adds analyze-codebase command for full architectural analysis\n- Adds search-patterns command for targeted pattern detection\n- Adds execute-analysis command for complex analysis tasks\n- Adds pattern-detection skill for understanding patterns and code smells\n- Adds codebase-search-strategies skill for effective query formulation\n- Adds gemini-cli-configuration skill for setup and optimization\n- Adds analysis-result-interpretation skill for acting on findings\n- Updates marketplace.json with new plugin registration\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>\nEOF\n)"`

**Step 5: Verify commit**

Run: `git log -1 --oneline`
Expected: Shows new commit with plugin feature

**Step 6: Verify plugin is in marketplace**

Run: `jq '.plugins[] | select(.name == "gemini-codebase-intelligence")' .claude-plugin/marketplace.json`
Expected: Shows complete plugin entry in JSON

---

## Summary

The Gemini CLI Codebase Intelligence plugin is now complete and committed. The implementation includes:

### ✅ Completed Deliverables

**Plugin Structure:**
- ✅ 2 specialized agents (Sonnet for routing, Haiku for execution)
- ✅ 3 command workflows (analyze, search, execute)
- ✅ 4 detailed skills (patterns, strategies, configuration, interpretation)
- ✅ Comprehensive plugin documentation
- ✅ Marketplace registration

**Key Features:**
- ✅ Hybrid routing (Gemini for complex, local tools for speed)
- ✅ Result caching for performance
- ✅ Fallback strategies for reliability
- ✅ Progressive skill disclosure for learning
- ✅ Multiple output formats (JSON, markdown)

**Ready for:**
- Large codebase analysis (100k+ files)
- Pattern detection and architectural review
- Code quality and security audits
- Team collaboration and knowledge sharing
- CI/CD integration

All files are production-ready and follow the Claude Code plugin specifications.
```

**Step 2: Commit to git**

Run: `git add .`
Expected: All changes staged

**Step 3: Create final commit**

Run: `git commit -m "$(cat <<'EOF'\nfeat: complete gemini-codebase-intelligence plugin implementation\n\nAll 12 tasks completed:\n- Plugin directory structure created\n- CodebaseAnalysisGateway agent (Sonnet)\n- GeminiCLIExecutor agent (Haiku)\n- Pattern Detection skill (comprehensive reference)\n- Codebase Search Strategies skill (query formulation)\n- Gemini CLI Configuration skill (setup & optimization)\n- Analysis Result Interpretation skill (decision frameworks)\n- analyze-codebase command\n- search-patterns command\n- execute-analysis command\n- Plugin README documentation\n- Marketplace manifest registration\n\nPlugin is production-ready with hybrid architecture,\ncaching, fallback strategies, and comprehensive skills.\n\n🤖 Generated with [Claude Code](https://claude.com/claude-code)\n\nCo-Authored-By: Claude <noreply@anthropic.com>\nEOF\n)"`

---

**All implementation tasks complete!** Your Gemini CLI Codebase Intelligence plugin is now available in the Claude Code marketplace.
<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Refine Hybrid Gateway architecture design with component details", "status": "completed", "activeForm": "Refining architecture design"}, {"content": "Present complete design for validation", "status": "completed", "activeForm": "Presenting design for validation"}, {"content": "Create comprehensive implementation plan", "status": "completed", "activeForm": "Creating implementation plan"}, {"content": "Set up git worktree for development", "status": "completed", "activeForm": "Setting up git worktree"}]