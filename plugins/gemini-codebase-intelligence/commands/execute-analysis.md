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
