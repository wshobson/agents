#!/bin/bash

###############################################################################
# Claude Code Plugins - Marketplace Validation Script
#
# This script validates the marketplace.json structure and verifies that
# all plugins are properly configured.
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
ERRORS=0
WARNINGS=0
CHECKS=0

# Helper functions
print_header() {
    echo -e "\n${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
    ((CHECKS++))
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

print_error() {
    echo -e "${RED}✗${NC} $1"
    ((ERRORS++))
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Main validation
print_header "Marketplace Validation"

# Check if we're in the right directory
if [ ! -f ".claude-plugin/marketplace.json" ]; then
    print_error "marketplace.json not found. Run this from the repository root."
    exit 1
fi

# Validate JSON syntax
print_header "JSON Syntax Validation"

if command -v jq &> /dev/null; then
    if jq empty .claude-plugin/marketplace.json 2>/dev/null; then
        print_success "marketplace.json is valid JSON"
    else
        print_error "marketplace.json has syntax errors"
        jq empty .claude-plugin/marketplace.json
        exit 1
    fi
else
    print_warning "jq not installed, using Python for validation"
    if python3 -c "import json; json.load(open('.claude-plugin/marketplace.json'))" 2>/dev/null; then
        print_success "marketplace.json is valid JSON"
    else
        print_error "marketplace.json has syntax errors"
        exit 1
    fi
fi

# Validate required fields
print_header "Validating Required Fields"

REQUIRED_FIELDS=("name" "owner" "metadata" "plugins")

for field in "${REQUIRED_FIELDS[@]}"; do
    if jq -e ".$field" .claude-plugin/marketplace.json > /dev/null 2>&1; then
        print_success "Field '$field' exists"
    else
        print_error "Missing required field: $field"
    fi
done

# Validate plugin structure
print_header "Validating Plugin Definitions"

PLUGIN_COUNT=$(jq '.plugins | length' .claude-plugin/marketplace.json)
print_info "Total plugins defined: $PLUGIN_COUNT"

# Check each plugin has required fields
echo ""
print_info "Checking plugin configurations..."

PLUGIN_ERRORS=0

for i in $(seq 0 $((PLUGIN_COUNT - 1))); do
    PLUGIN_NAME=$(jq -r ".plugins[$i].name" .claude-plugin/marketplace.json)

    # Check required fields for each plugin
    PLUGIN_REQUIRED=("name" "source" "description" "version")

    for field in "${PLUGIN_REQUIRED[@]}"; do
        if ! jq -e ".plugins[$i].$field" .claude-plugin/marketplace.json > /dev/null 2>&1; then
            print_error "Plugin '$PLUGIN_NAME' missing field: $field"
            ((PLUGIN_ERRORS++))
        fi
    done

    # Verify source directory exists
    SOURCE=$(jq -r ".plugins[$i].source" .claude-plugin/marketplace.json)
    if [ ! -d "$SOURCE" ]; then
        print_error "Plugin '$PLUGIN_NAME' source directory not found: $SOURCE"
        ((PLUGIN_ERRORS++))
    fi
done

if [ $PLUGIN_ERRORS -eq 0 ]; then
    print_success "All plugins have required fields and directories"
else
    print_error "Found $PLUGIN_ERRORS plugin configuration issues"
fi

# Validate plugin directories
print_header "Validating Plugin Directories"

PLUGIN_DIR_COUNT=$(ls -1 plugins/ | wc -l)
print_info "Plugin directories: $PLUGIN_DIR_COUNT"

if [ "$PLUGIN_COUNT" -eq "$PLUGIN_DIR_COUNT" ]; then
    print_success "Plugin count matches directory count"
else
    print_warning "Mismatch: JSON has $PLUGIN_COUNT plugins, but $PLUGIN_DIR_COUNT directories exist"
fi

# Check for orphaned directories
echo ""
print_info "Checking for orphaned plugin directories..."

ORPHANED=0

for dir in plugins/*/; do
    dir_name=$(basename "$dir")

    # Check if plugin exists in marketplace.json
    if ! jq -e ".plugins[] | select(.name == \"$dir_name\")" .claude-plugin/marketplace.json > /dev/null 2>&1; then
        print_warning "Directory 'plugins/$dir_name' not found in marketplace.json"
        ((ORPHANED++))
    fi
done

if [ $ORPHANED -eq 0 ]; then
    print_success "No orphaned plugin directories found"
else
    print_warning "Found $ORPHANED orphaned plugin directories"
fi

# Validate plugin contents
print_header "Validating Plugin Contents"

echo "Checking plugin directory structure..."

MISSING_CONTENT=0

for dir in plugins/*/; do
    dir_name=$(basename "$dir")

    # Check if plugin has at least one of: agents/, commands/, or skills/
    if [ ! -d "$dir/agents" ] && [ ! -d "$dir/commands" ] && [ ! -d "$dir/skills" ]; then
        print_warning "Plugin '$dir_name' has no agents, commands, or skills directories"
        ((MISSING_CONTENT++))
    fi
done

if [ $MISSING_CONTENT -eq 0 ]; then
    print_success "All plugins have content directories"
else
    print_warning "$MISSING_CONTENT plugins missing content directories"
fi

# Summary
print_header "Validation Summary"

echo "Checks passed:    $CHECKS"
echo "Warnings:         $WARNINGS"
echo "Errors:          $ERRORS"
echo ""

if [ $ERRORS -eq 0 ]; then
    print_success "Validation completed successfully!"
    echo ""
    echo "Your marketplace is ready to use!"
    echo ""
    echo "To add this marketplace to Claude Code:"
    echo "  /plugin marketplace add wshobson/agents"
    echo ""
    exit 0
else
    print_error "Validation failed with $ERRORS errors"
    echo ""
    echo "Please fix the errors above before using this marketplace."
    echo ""
    exit 1
fi
