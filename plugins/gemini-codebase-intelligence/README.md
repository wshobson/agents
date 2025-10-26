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
