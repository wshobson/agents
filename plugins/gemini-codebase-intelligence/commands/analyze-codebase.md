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
