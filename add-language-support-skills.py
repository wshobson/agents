#!/usr/bin/env python3
"""
Add multilingual support (Russian language) to all skills.
This script detects the language of the input and responds in the same language.
"""

import os
import re
from pathlib import Path

# The language detection and response instruction to add
LANGUAGE_INSTRUCTION = """## Language Support

This skill documentation and all guidance adapt to user language:
- **Russian input** → **Russian explanations and examples**
- **English input** → **English explanations and examples**
- **Mixed input** → Language of the primary content
- **Code samples and technical terms** maintain their original names

When using this skill, specify your preferred language in your request."""

def get_skill_files():
    """Get all skill SKILL.md files."""
    plugins_dir = Path("/Users/dmitry.lazarenko/Documents/projects/stocks-ai/agents/plugins")
    skill_files = list(plugins_dir.rglob("skills/*/SKILL.md"))
    return sorted(skill_files)

def has_language_support(content):
    """Check if skill already has language support instruction."""
    return "Language Support" in content or "Detect the language" in content

def add_language_support_to_skill(file_path):
    """Add language support instruction to a skill file."""
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

    if insert_index is None:
        insert_index = len(lines) - 1

    # Insert the language instruction
    new_lines = lines[:insert_index] + [LANGUAGE_INSTRUCTION, ''] + lines[insert_index:]
    new_content = '\n'.join(new_lines)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Language support added"

def main():
    """Main function to update all skills."""
    skill_files = get_skill_files()

    print(f"Found {len(skill_files)} skill files")
    print("=" * 80)

    updated_count = 0
    skipped_count = 0
    errors = []

    for i, skill_file in enumerate(skill_files, 1):
        try:
            success, message = add_language_support_to_skill(skill_file)

            if success:
                updated_count += 1
                status = "✓ UPDATED"
            else:
                skipped_count += 1
                status = "⊘ SKIPPED"

            rel_path = skill_file.relative_to(skill_file.parents[4])
            print(f"[{i:3d}/{len(skill_files)}] {status}: {rel_path}")

        except Exception as e:
            errors.append((skill_file, str(e)))
            rel_path = skill_file.relative_to(skill_file.parents[4])
            print(f"[{i:3d}/{len(skill_files)}] ✗ ERROR: {rel_path}")
            print(f"         {str(e)}")

    print("=" * 80)
    print(f"\nSummary:")
    print(f"  Updated: {updated_count} skills")
    print(f"  Skipped: {skipped_count} skills")
    print(f"  Errors:  {len(errors)} skills")

    if errors:
        print(f"\nFailed to update:")
        for file_path, error in errors:
            rel_path = file_path.relative_to(file_path.parents[4])
            print(f"  - {rel_path}")

if __name__ == "__main__":
    main()
