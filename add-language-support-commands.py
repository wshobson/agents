#!/usr/bin/env python3
"""
Add multilingual support (Russian language) to all commands.
This script detects the language of the input and responds in the same language.
"""

import os
import re
from pathlib import Path

# The language detection and response instruction to add
LANGUAGE_INSTRUCTION = """## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages."""

def get_command_files():
    """Get all command markdown files."""
    plugins_dir = Path("/Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins")
    command_files = list(plugins_dir.rglob("commands/*.md"))
    return sorted(command_files)

def has_language_support(content):
    """Check if command already has language support instruction."""
    return "Language Support" in content or "Detect the language" in content

def add_language_support_to_command(file_path):
    """Add language support instruction to a command file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if has_language_support(content):
        return False, "Already has language support"

    lines = content.split('\n')

    # Find the first "##" heading after the title
    insert_index = None
    for i, line in enumerate(lines):
        if i > 1 and line.startswith('## '):
            insert_index = i
            break

    # If no "##" found, find the first line with content after description
    if insert_index is None:
        for i, line in enumerate(lines):
            if i > 1 and line.strip() and not line.startswith('['):
                insert_index = i
                break

    if insert_index is None:
        insert_index = len(lines) - 1

    # Insert the language instruction
    new_lines = lines[:insert_index] + [LANGUAGE_INSTRUCTION, ''] + lines[insert_index:]
    new_content = '\n'.join(new_lines)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Language support added"

def main():
    """Main function to update all commands."""
    command_files = get_command_files()

    print(f"Found {len(command_files)} command files")
    print("=" * 80)

    updated_count = 0
    skipped_count = 0
    errors = []

    for i, cmd_file in enumerate(command_files, 1):
        try:
            success, message = add_language_support_to_command(cmd_file)

            if success:
                updated_count += 1
                status = "✓ UPDATED"
            else:
                skipped_count += 1
                status = "⊘ SKIPPED"

            rel_path = cmd_file.relative_to(cmd_file.parents[3])
            print(f"[{i:3d}/{len(command_files)}] {status}: {rel_path}")

        except Exception as e:
            errors.append((cmd_file, str(e)))
            rel_path = cmd_file.relative_to(cmd_file.parents[3])
            print(f"[{i:3d}/{len(command_files)}] ✗ ERROR: {rel_path}")
            print(f"         {str(e)}")

    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Updated: {updated_count} commands")
    print(f"  Skipped: {skipped_count} commands")
    print(f"  Errors:  {len(errors)} commands")

    if errors:
        print(f"\nFailed to update:")
        for file_path, error in errors:
            rel_path = file_path.relative_to(file_path.parents[3])
            print(f"  - {rel_path}")

if __name__ == "__main__":
    main()
