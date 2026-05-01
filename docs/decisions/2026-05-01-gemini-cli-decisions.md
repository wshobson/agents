# ADR: Gemini CLI Integration Decisions

## Context

We are implementing Gemini CLI support for the claude-agents project by creating TOML files that map Claude Code commands to Gemini CLI commands. The approach is to generate slash commands for all existing Claude Code commands.

## Decision

We will implement Gemini CLI support by:

1. Creating TOML command files for all existing commands
2. Following the pattern of mapping Claude Code commands to Gemini CLI commands
3. Maintaining compatibility with existing Claude Code workflows

## Consequences

This approach maintains backward compatibility with existing Claude Code commands while providing a smooth transition to Gemini CLI.

## Implementation Status

- [x] Basic Gemini CLI integration structure in place
- [x] Slash commands generated for all 79+ plugins
- [x] Documentation files created including GEMINI.md and tool mapping documentation
- [x] Generation script created for creating TOML files
- [ ] ADR documenting the slash command implementation decisions (this file)