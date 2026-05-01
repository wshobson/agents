# Reverse Engineering

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `firmware-analyst` | opus | Expert firmware analyst specializing in embedded systems, IoT security, and hardware reverse engineering. Masters fir... |
| `malware-analyst` | opus | Expert malware analyst specializing in defensive malware research, threat intelligence, and incident response. Master... |
| `reverse-engineer` | opus | Expert reverse engineer specializing in binary analysis, disassembly, decompilation, and software analysis. Masters I... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `anti-reversing-techniques` | Understand anti-reversing, obfuscation, and protection techniques encountered during software analysis. Use this skill when analyzing mal... |
| `binary-analysis-patterns` | Master binary analysis patterns including disassembly, decompilation, control flow analysis, and code pattern recognition. Use when analy... |
| `memory-forensics` | Master memory forensics techniques including memory acquisition, process analysis, and artifact extraction using Volatility and related t... |
| `protocol-reverse-engineering` | Master network protocol reverse engineering including packet analysis, protocol dissection, and custom protocol documentation. Use when a... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Expert firmware analyst specializing in embedded systems, IoT security, and hardware reverse engineering" → activates `firmware-analyst`
- "Understand anti-reversing, obfuscation, and protection techniques encountered during software analysis" → activates `anti-reversing-techniques` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
