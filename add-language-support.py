#!/usr/bin/env python3
"""
Add multilingual support (Russian language) to all agents.
This script detects the language of the input and responds in the same language.
"""

import os
import re
from pathlib import Path

# The language detection and response instruction to add
LANGUAGE_INSTRUCTION = """## Language Support

Detect the language of the user's input and respond in the same language:
- If input is in **Russian**, respond entirely in **Russian**
- If input is in **English**, respond in **English**
- For mixed language input, respond in the language of the primary content
- Maintain all technical terms, variable names, and code samples in their original form

This applies to all interactions: explanations, code generation, documentation, and technical guidance."""

def get_agent_files():
    """Get all agent markdown files."""
    agents_dir = Path("/Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins")
    agent_files = list(agents_dir.rglob("agents/*.md"))
    return sorted(agent_files)

def has_language_support(content):
    """Check if agent already has language support instruction."""
    return "Language Support" in content or "Detect the language" in content

def add_language_support_to_agent(file_path):
    """Add language support instruction to an agent file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_language_support(content):
        return False, "Already has language support"

    # Find where to insert the language instruction
    # Look for the first "##" heading or end of initial content block
    lines = content.split('\n')

    insert_index = None

    # First try to find a "##" heading after the initial content
    for i, line in enumerate(lines):
        if i > 5 and line.startswith('## '):
            insert_index = i
            break

    # If no "##" found, insert at the end of the preamble (after first empty line block)
    if insert_index is None:
        for i, line in enumerate(lines):
            if i > 5 and line.strip() == '':
                # Found empty line, insert after it
                insert_index = i + 1
                break

    # Last resort: insert near the end
    if insert_index is None:
        insert_index = len(lines) - 1

    # Insert the language instruction at the found position
    new_lines = lines[:insert_index] + [LANGUAGE_INSTRUCTION, ''] + lines[insert_index:]
    new_content = '\n'.join(new_lines)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Language support added"

def main():
    """Main function to update all agents."""
    agent_files = get_agent_files()

    print(f"Found {len(agent_files)} agent files")
    print("=" * 80)

    updated_count = 0
    skipped_count = 0
    errors = []

    for i, agent_file in enumerate(agent_files, 1):
        try:
            success, message = add_language_support_to_agent(agent_file)

            if success:
                updated_count += 1
                status = "✓ UPDATED"
            else:
                skipped_count += 1
                status = "⊘ SKIPPED"

            rel_path = agent_file.relative_to(agent_file.parents[3])
            print(f"[{i:3d}/{len(agent_files)}] {status}: {rel_path}")

        except Exception as e:
            errors.append((agent_file, str(e)))
            rel_path = agent_file.relative_to(agent_file.parents[3])
            print(f"[{i:3d}/{len(agent_files)}] ✗ ERROR: {rel_path}")
            print(f"         {str(e)}")

    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Updated: {updated_count} agents")
    print(f"  Skipped: {skipped_count} agents")
    print(f"  Errors:  {len(errors)} agents")

    if errors:
        print(f"\nFailed to update:")
        for file_path, error in errors:
            rel_path = file_path.relative_to(file_path.parents[3])
            print(f"  - {rel_path}")

if __name__ == "__main__":
    main()
