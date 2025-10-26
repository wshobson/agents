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
