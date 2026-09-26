# plugin-eval

plugin-eval scores Claude Code plugins and skills in up to three layers. The static layer is a
lint. It's fast and deterministic, and it's useful for checking structure. The LLM judge and Monte
Carlo layers are experimental, not validated against human labels. For the trace-based eval
program, see `evals/README.md` at the repository root.

## Quick start

```bash
cd plugins/plugin-eval
uv sync

# Static lint of a skill, with no model calls
uv run plugin-eval score path/to/skill --depth quick

# Static and LLM judge layers, experimental, needs `uv sync --extra llm`
uv run plugin-eval score path/to/skill --depth standard

# All three layers at deep depth (experimental)
uv run plugin-eval certify path/to/skill
```

## Layers

1. Static analysis runs structural checks and flags anti-patterns without calling a model.
   Plugin-level scores and badges, including the ones in the weekly CI report, come from this
   layer alone.
2. The LLM judge (experimental) makes four model calls and returns four holistic scores from 0
   to 1.
3. Monte Carlo (experimental) sends 50 to 100 prompts to the model and records how often it
   replies, how long the replies are, how often it errors, and how many tokens it uses.

## Commands

| CLI                   | Claude Code | Description                                        |
| --------------------- | ----------- | -------------------------------------------------- |
| `plugin-eval score`   | `/eval`     | Score a plugin or skill                            |
| `plugin-eval certify` | `/certify`  | Score at deep depth and assign a badge             |
| `plugin-eval compare` | `/compare`  | Compare two skills                                 |
| `plugin-eval init`    | none        | Write a corpus index, which no other command reads |

## Documentation

See [docs/plugin-eval.md](../../docs/plugin-eval.md) for the full reference, which covers the
layers, dimensions, scoring formula, anti-patterns, and project structure.
