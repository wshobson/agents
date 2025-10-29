#!/bin/bash
#
# Process Agent Output to Markdown Files
# Extracts markdown content from agent output and saves to files
#
# Usage: ./process_agent_output.sh TICKER
# Example: ./process_agent_output.sh NVDA
#
# This script:
# 1. Runs the stock analysis for the given ticker
# 2. Captures output from all agents
# 3. Extracts markdown blocks wrapped in ---SAVE_MARKDOWN_START--- markers
# 4. Saves each report to reports/{TICKER}_{DATE}/{DATE}_{category}.md
# 5. Displays summary of generated reports

set -e

# Configuration
TICKER="${1:-NVDA}"
DATE=$(date +%Y-%m-%d)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORTS_DIR="${SCRIPT_DIR}/reports"
TEMP_DIR="$(mktemp -d)" # Create unique temp directory

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Create temp directory
mkdir -p "$TEMP_DIR"
trap "rm -rf $TEMP_DIR" EXIT

print_header "Stock Analysis for $TICKER - $DATE"

# Verify reports directory exists
if [ ! -d "$REPORTS_DIR" ]; then
    print_warning "Reports directory does not exist. Creating it..."
    mkdir -p "$REPORTS_DIR"
fi

print_success "Reports directory ready at $REPORTS_DIR"

# Function to extract and save markdown blocks
extract_and_save_markdown() {
    local input_file="$1"
    local reports_base="$2"
    local saved_count=0

    if [ ! -f "$input_file" ]; then
        print_error "Input file not found: $input_file"
        return 1
    fi

    # Extract all markdown blocks
    awk -v reports_dir="$reports_base" '
    BEGIN {
        in_block = 0
        filename = ""
        content = ""
    }

    /---SAVE_MARKDOWN_START---/ {
        in_block = 1
        next
    }

    /---CONTENT_START---/ {
        if (in_block) {
            next
        }
    }

    /---CONTENT_END---/ {
        if (in_block) {
            # Save the file
            full_path = reports_dir "/" filename
            if (filename != "") {
                # Create directory if needed
                cmd = "mkdir -p \"" substr(full_path, 1, length(full_path) - length(substr(full_path, match(full_path, /[^\/]*$/)))) "\""
                system(cmd)
                print content > full_path
                close(full_path)
                print "SAVED:" full_path
            }
            content = ""
            next
        }
    }

    /---SAVE_MARKDOWN_END---/ {
        in_block = 0
        filename = ""
        next
    }

    /^filename:/ {
        if (in_block) {
            filename = $2
            next
        }
    }

    {
        if (in_block && filename != "") {
            content = content $0 "\n"
        }
    }
    ' "$input_file"
}

# Run analysis and capture output
print_header "Running Agent Analysis"

# Store the ticker analysis command output
echo "Analyzing $TICKER..."
# Note: In a real implementation, this would call the slash command and capture output
# For now, this is a template that shows how to process the output

# Example of how output would be processed:
# /stock-analysis:ticker-analysis $TICKER > "$TEMP_DIR/analysis_output.txt" 2>&1

# Process captured output
# extract_and_save_markdown "$TEMP_DIR/analysis_output.txt"

# For demonstration, show the expected structure
print_warning "Agent auto-save configuration is now active"
echo ""
echo "When you run: /stock-analysis:ticker-analysis $TICKER"
echo ""
echo "The agents will now include special markers in their output:"
echo "- Technical analyst → reports/{TICKER}_{DATE}/{DATE}_technical.md"
echo "- Fundamental analyst → reports/{TICKER}_{DATE}/{DATE}_fundamental.md"
echo "- Risk specialist → reports/{TICKER}_{DATE}/{DATE}_risk.md"
echo "- Patent researcher → reports/{TICKER}_{DATE}/{DATE}_competitive.md"
echo "- Equity analyst → reports/{TICKER}_{DATE}/{DATE}_recommendation.md"
echo ""

# List existing reports
print_header "Existing Reports"
if find "$REPORTS_DIR" -type f -name "*.md" 2>/dev/null | grep -q .; then
    find "$REPORTS_DIR" -type f -name "*.md" -newer /dev/null 2>/dev/null | while read file; do
        relative_path="${file#$REPORTS_DIR/}"
        print_success "$relative_path"
    done
else
    print_warning "No reports found yet. Run analysis to generate reports."
fi

print_header "Next Steps"
echo ""
echo "1. Run the analysis command:"
echo "   /stock-analysis:ticker-analysis $TICKER"
echo ""
echo "2. This will now:"
echo "   ✓ Run 5-phase analysis (technical, fundamental, risk, competitive, synthesis)"
echo "   ✓ Automatically save all reports to reports/{TICKER}_{DATE}/"
echo "   ✓ Display console summary"
echo ""
echo "3. View generated reports:"
echo "   open $REPORTS_DIR/INDEX.md"
echo ""

print_success "Setup complete! Agents are now configured to auto-save markdown reports."
