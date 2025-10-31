---
name: gemini-cli-configuration
description: Setup, installation, authentication, and optimization of Gemini CLI. Covers environment configuration, API credentials, performance tuning, and troubleshooting common issues. Use when initializing Gemini CLI or resolving configuration problems.
---

# Gemini CLI Configuration Skill

## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request.

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
