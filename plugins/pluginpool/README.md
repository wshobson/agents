# pluginpool

Ten focused developer productivity commands wrapped as Claude Code slash commands. Each command's core is a deterministic Python helper (Python standard library only at runtime — no `pip install` to use any of them).

## Commands

| Command | Purpose |
|---|---|
| `/commit-narrator` | Generate semantic commit message from `git diff --cached`, including the *why* behind changes |
| `/pr-storyteller` | Generate PR title, body, and test plan from commits and diff vs base branch |
| `/test-gap` | Identify lines in your diff lacking test coverage (Cobertura / lcov / coverage.json) |
| `/deps-doctor` | Multi-ecosystem dependency audit (npm, pip, cargo, go) — one unified report |
| `/env-lint` | Compare `.env` vs `.env.example` key parity — never prints values |
| `/secret-guard` | Pre-commit secret scanner using pattern and entropy detection, redacted output |
| `/standup-gen` | Generate daily standup notes from git activity across one or many repos |
| `/todo-harvest` | Scan for TODO/FIXME/HACK comments with git blame author + age |
| `/flaky-detector` | Run a test command N times and report per-test flakiness percentage |
| `/changelog-forge` | Convert conventional commits into a CHANGELOG section + semver bump |

**89 hermetic tests across the suite** (in upstream repos), all green. Each helper has a plain CLI for use without Claude Code:

```sh
git diff --staged | python3 plugins/pluginpool/scripts/narrate.py --diff - --format json
```

## Upstream

Each command also lives as its own standalone repo with a full test suite, examples, and Makefile-based development workflow:

- [mturac/pluginpool](https://github.com/mturac/pluginpool) (index)
- [pluginpool-commit-narrator](https://github.com/mturac/pluginpool-commit-narrator)
- [pluginpool-pr-storyteller](https://github.com/mturac/pluginpool-pr-storyteller)
- [pluginpool-test-gap](https://github.com/mturac/pluginpool-test-gap)
- [pluginpool-deps-doctor](https://github.com/mturac/pluginpool-deps-doctor)
- [pluginpool-env-lint](https://github.com/mturac/pluginpool-env-lint)
- [pluginpool-secret-guard](https://github.com/mturac/pluginpool-secret-guard)
- [pluginpool-standup-gen](https://github.com/mturac/pluginpool-standup-gen)
- [pluginpool-todo-harvest](https://github.com/mturac/pluginpool-todo-harvest)
- [pluginpool-flaky-detector](https://github.com/mturac/pluginpool-flaky-detector)
- [pluginpool-changelog-forge](https://github.com/mturac/pluginpool-changelog-forge)

## License

MIT.
