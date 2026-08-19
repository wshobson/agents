# eSkill — Meta-skill: build top-tier Agent Skills

eSkill is the **skill for creating skills** — a production workflow distilled from the
official [Agent Skills spec](https://agentskills.io/specification), Anthropic's
[skill-creator](https://github.com/anthropics/skills) eval loop, and real lessons from
building/shipping egram + the eSeed project.

## What it gives you

- **6-step process** to design, write, test and ship a skill (ask-first → pick a proven
  standard as "north star" → write spec-compliant SKILL.md → package known pitfalls →
  eval loop → pin activation)
- **Spec rules**: frontmatter (name/description/license/compatibility/metadata),
  progressive disclosure (<500 lines), 1-level references
- **Eval loop**: forward-test with real-looking prompts, qualitative + quantitative review
- **Naming** (Apple-style e-family: `e` + one word — eSkill, eSeed, egram)
- **Commercial checklist**: leak scan (`--leak --brand`), LICENSE, README sync, marketplace
- **Validator**: `scripts/validate-skill.py` — catches broken frontmatter, bad names,
  broken refs, oversized SKILL.md, and leaks

## Quickstart (3 prompts)

1. `Create a skill that <does X> and check it works` — eSkill interviews you, then builds it
2. `Improve this skill: <path>` — eSkill applies the eval loop and fixes it
3. `Validate this skill: <path> [--leak]` — run the validator

## Structure

```
eskill/
├── SKILL.md                     # 6-step process + golden rules (Vietnamese — user-facing)
├── README.md                    # This file (English — public-facing)
├── LICENSE                      # MIT
├── RELEASE-NOTES.md             # changelog (Keep a Changelog + semver)
├── .version-bump.json           # current version + files to sync on bump
├── CODE_OF_CONDUCT.md           # contributor covenant
├── .gitignore · .pre-commit-config.yaml
├── agents/openai.yaml           # marketplace/UI metadata
├── .claude-plugin/ · .codex-plugin/ · .cursor-plugin/   # plugin manifests
├── .github/                     # FUNDING + issue/PR templates
├── assets/                      # icon
├── template/SKILL.md            # copy-ready skill skeleton (full frontmatter)
├── references/
│   ├── spec-rules.md            # agentskills.io spec rules
│   ├── naming.md                # Apple-style e-family naming
│   ├── sales-discovery.md       # SPIN + Mom Test (step-0 interview)
│   ├── eval-loop.md             # test → evaluate → fix loop
│   ├── test-prompts-template.md # 5 test-prompt types
│   ├── rubric.md                # pre-registered pass/fail rubric
│   ├── docs-driven.md           # docs = hard gate 100%
│   ├── 12-factor-skills.md      # maintainable skill ops
│   ├── apple-writing.md         # concise SKILL.md writing
│   ├── openai-yaml.md           # agents/openai.yaml guide
│   ├── checklist-thuong-mai.md  # commercialization + safety checklist
│   └── ban-tren-github.md       # selling via GitHub (private → public)
├── examples/echeck/             # complete reference skill
└── scripts/
    ├── validate-skill.py        # validator: --leak --brand "a,b"
    └── eval-skill.py            # eval harness: test set + --verify
```

## Release

Version: `1.4.1` — xem [RELEASE-NOTES.md](RELEASE-NOTES.md).
Quy trình: sửa xong → bump `.version-bump.json` → cập nhật RELEASE-NOTES → `gh release create vX.Y.Z`
(chi tiết: `references/ban-tren-github.md`).

## Install

Recommended — one command via [skills.sh](https://skills.sh):

```bash
npx skills add hedralab/eskill
```

Claude Code — plugin marketplace:

```
/plugin marketplace add hedralab/eskill
/plugin install eskill
```

Manual — copy the folder into your agent skills dir:

```bash
cp -R eskill ~/.deepseek/skills/eskill    # DeepSeek TUI
# or ~/.claude/skills/eskill
# or ~/.codex/skills/eskill
```

## License

MIT — free to use, modify, and sell.
