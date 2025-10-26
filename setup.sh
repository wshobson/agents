#!/bin/bash

###############################################################################
# Claude Code Plugins - Environment Setup Script
#
# This script sets up your development environment for the Claude Code
# plugins marketplace repository.
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Main setup
print_header "Claude Code Plugins - Environment Setup"

echo "This script will:"
echo "  1. Verify system dependencies"
echo "  2. Validate the plugin marketplace structure"
echo "  3. Set up development tools"
echo "  4. Prepare the environment for contribution"
echo ""

# Check if we're in the right directory
if [ ! -f ".claude-plugin/marketplace.json" ]; then
    print_error "marketplace.json not found. Are you in the repository root?"
    exit 1
fi

print_success "Found marketplace.json"

# Check system dependencies
print_header "Checking System Dependencies"

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python installed: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check Node.js (optional but recommended)
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_success "Node.js installed: $NODE_VERSION"
else
    print_warning "Node.js not found (optional, but recommended for JSON validation)"
fi

# Check jq for JSON processing
if command -v jq &> /dev/null; then
    JQ_VERSION=$(jq --version)
    print_success "jq installed: $JQ_VERSION"
else
    print_warning "jq not found (optional, but recommended for JSON validation)"
fi

# Check git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    print_success "Git installed: $GIT_VERSION"
else
    print_error "Git not found. Please install Git."
    exit 1
fi

# Validate marketplace structure
print_header "Validating Marketplace Structure"

# Count plugins in JSON
if command -v jq &> /dev/null; then
    PLUGIN_COUNT_JSON=$(jq '.plugins | length' .claude-plugin/marketplace.json)
    print_info "Plugins in marketplace.json: $PLUGIN_COUNT_JSON"
else
    print_warning "Cannot count plugins without jq"
    PLUGIN_COUNT_JSON="unknown"
fi

# Count plugin directories
PLUGIN_COUNT_DIR=$(ls -1 plugins/ | wc -l)
print_info "Plugin directories: $PLUGIN_COUNT_DIR"

# Validate counts match
if [ "$PLUGIN_COUNT_JSON" != "unknown" ] && [ "$PLUGIN_COUNT_JSON" -eq "$PLUGIN_COUNT_DIR" ]; then
    print_success "Plugin counts match!"
else
    if [ "$PLUGIN_COUNT_JSON" != "unknown" ]; then
        print_warning "Plugin counts don't match. JSON: $PLUGIN_COUNT_JSON, Directories: $PLUGIN_COUNT_DIR"
    fi
fi

# Validate JSON syntax
print_header "Validating JSON Syntax"

if command -v jq &> /dev/null; then
    if jq empty .claude-plugin/marketplace.json 2>/dev/null; then
        print_success "marketplace.json is valid JSON"
    else
        print_error "marketplace.json has syntax errors"
        exit 1
    fi
else
    if python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))" 2>/dev/null; then
        print_success "marketplace.json is valid JSON (verified with Python)"
    else
        print_error "marketplace.json has syntax errors"
        exit 1
    fi
fi

# Repository information
print_header "Repository Information"

MARKETPLACE_NAME=$(jq -r '.name' .claude-plugin/marketplace.json 2>/dev/null || echo "unknown")
MARKETPLACE_VERSION=$(jq -r '.metadata.version' .claude-plugin/marketplace.json 2>/dev/null || echo "unknown")

print_info "Marketplace: $MARKETPLACE_NAME"
print_info "Version: $MARKETPLACE_VERSION"
print_info "Working directory: $(pwd)"

# Git status
if git rev-parse --git-dir > /dev/null 2>&1; then
    CURRENT_BRANCH=$(git branch --show-current)
    print_info "Current branch: $CURRENT_BRANCH"
    print_success "Git repository initialized"
else
    print_warning "Not a git repository"
fi

# Create helpful scripts
print_header "Setting Up Development Tools"

# Make validation script executable if it exists
if [ -f "scripts/validate-marketplace.sh" ]; then
    chmod +x scripts/validate-marketplace.sh
    print_success "Made validation script executable"
fi

# Summary
print_header "Setup Complete!"

echo "Your environment is ready for development!"
echo ""
echo "Next steps:"
echo "  1. Review the documentation in docs/"
echo "  2. Explore plugins in plugins/"
echo "  3. Run validation: ./scripts/validate-marketplace.sh (if available)"
echo ""
echo "To use this marketplace in Claude Code:"
echo "  /plugin marketplace add wshobson/agents"
echo ""
echo "To install a plugin:"
echo "  /plugin install <plugin-name>"
echo ""

print_success "Setup completed successfully!"
