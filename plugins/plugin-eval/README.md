# plugin-eval

Three-layer quality evaluation framework for Claude Code plugins.

## Quick Start

```bash
cd plugins/plugin-eval
uv sync

# Evaluate a skill (static only, instant)
uv run plugin-eval score path/to/skill --depth quick

# Evaluate with LLM judge (~30s)
uv run plugin-eval score path/to/skill --depth standard

# Full certification (all layers, ~5 min)
uv run plugin-eval certify path/to/skill
```

## Layers

1. **Static Analysis** — Structural checks, anti-pattern detection. Instant, free.
2. **LLM Judge** — Semantic evaluation (triggering, orchestration, output, scope). ~30s, 4 calls.
3. **Monte Carlo** — Statistical reliability via 50–100 simulated runs. ~2–5 min.

## Commands

| CLI                   | Claude Code | Description                   |
| --------------------- | ----------- | ----------------------------- |
| `plugin-eval score`   | `/eval`     | Score a plugin or skill       |
| `plugin-eval certify` | `/certify`  | Full certification with badge |
| `plugin-eval compare` | `/compare`  | Head-to-head comparison       |
| `plugin-eval init`    | —           | Build corpus for Elo ranking  |

## Documentation

See **[docs/plugin-eval.md](../../docs/plugin-eval.md)** for the full reference: layers, dimensions, scoring formula, anti-patterns, statistical methods, and project structure.
