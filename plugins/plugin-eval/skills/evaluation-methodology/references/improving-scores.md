# Improving a PluginEval score

Start with the static layer, because it's the only layer that gives the same result on every run.
Each section below names what the code checks and how to change the result. The judge and Monte
Carlo layers are experimental, so a change that moves only their scores may not reflect a real
change in quality.

## Anti-pattern flags

Each flag cuts the composite score by 5%, down to a floor of 50%.

| Flag | What triggers it | Fix |
|---|---|---|
| `OVER_CONSTRAINED` | More than 15 uses of the uppercase words MUST, ALWAYS, or NEVER in SKILL.md | Keep hard rules for safety and correctness, and explain the reason for the rest. |
| `EMPTY_DESCRIPTION` | A description shorter than 20 characters | Write a longer description that includes a trigger phrase. |
| `MISSING_TRIGGER` | No trigger phrase, such as "Use when", "Use this skill when", "Use proactively", or "Trigger when", in the description | Add "Use this skill when" followed by specific contexts. |
| `BLOATED_SKILL` | More than 800 lines and no `references/` directory | Move long tables, examples, and background into `references/`, and link to them from SKILL.md. |
| `ORPHAN_REFERENCE` | A link from SKILL.md into `references/` that points at a missing file | Create the file or remove the link. |
| `DEAD_CROSS_REF` | Text in SKILL.md that looks like a skill path, such as `skills/<name>`, and doesn't resolve | Fix the path or reword the text. |

Skills with `disable-model-invocation: true` or a `paths:` glob in the frontmatter are exempt from
`MISSING_TRIGGER`. The `DEAD_CROSS_REF` check matches plain prose too, so a phrase like
"skills/agents" counts as a path.

## Harness portability findings

Portability findings lower the `harness_portability` sub-score, which is 1.0 minus the sum of
their severities. The report doesn't list the findings, so compare the sub-score in the JSON
output.

| Finding | Severity | What triggers it |
|---|---|---|
| `SKILL_OVER_CODEX_CAP` | 0.15 | The SKILL.md file is over 8 KB and the skill has no `references/` directory. |
| `CLAUDE_TOOL_REFS` | 0.02 for each tool, up to 0.10 | A backticked tool name used as a tool, such as "use `Bash`" or "the `Read` tool". |
| `CLAUDE_TOOL_PROSE` | 0.05 | A phrase such as "the Read tool". |

To fix either tool finding, name the action instead of the tool, e.g., "open the file" or "run
the shell command". The code also has checks for agent files, but no score uses them.

## Tips for each dimension

Work on the dimensions with the largest weight first, because they move the composite the most.
At quick depth only the static checks count, so each tip names the static check it affects.

### triggering_accuracy (weight 0.25)

The static part of this dimension is `frontmatter_quality`. It rewards a description of at least
100 characters, a trigger phrase, the word "proactively", and three or more comma-separated
contexts that start with words such as "when" or "for". Write "Use this skill when" followed by
specific contexts, and then check by hand that the description wouldn't match unrelated requests.

### orchestration_fitness (weight 0.20)

The static part is `orchestration_wiring`. It starts at 0.70 and adds points when SKILL.md
describes an output format, describes its inputs, and has at least two code blocks. It subtracts
0.15 when the text uses a word that starts with "orchestrat", "coordinat", or "dispatch".
Describe what the skill receives and what it returns.

### output_quality (weight 0.15) and scope_calibration (weight 0.12)

Only the experimental layers score these dimensions, so a quick-depth score ignores them. The
anchors in [rubrics.md](rubrics.md) describe what the judge is asked to look for.

### progressive_disclosure (weight 0.10)

The check scores the line count of SKILL.md as follows:

- 0.60 for 200 to 600 lines
- 0.50 for 100 to 199 lines
- 0.40 for 601 to 800 lines
- 0.20 for fewer than 100 lines, and 0.15 for more than 800

Any file in `references/` adds 0.15, or 0.25 when SKILL.md is over 400 lines. Any file in
`assets/` adds another 0.15.

### token_efficiency (weight 0.06)

The check subtracts points when MUST, NEVER, and ALWAYS appear more than once per 10 lines, and
when lines repeat. Remove repeated lines, and explain rules instead of adding more hard rules.

### structural_completeness (weight 0.03)

The check rewards six or more H2 and H3 headings, five or more code blocks, and code in three or
more languages. It also rewards a markdown table and sections whose headings start with
"Example", "Usage", or "Troubleshooting".

### ecosystem_coherence (weight 0.02)

The check starts at 0.50 and adds up to 0.25 for skill paths. It adds another 0.25 when the text
says "related", "see also", "companion", or "complement". Make sure any skill path resolves,
because a path that doesn't resolve also raises `DEAD_CROSS_REF`.

### robustness (weight 0.05) and code_template_quality (weight 0.02)

Only the Monte Carlo layer scores `robustness`, as 1 minus its failure rate. No layer scores
`code_template_quality`, so it never counts.

## Troubleshooting

- When the composite drops after an edit, look for new flags in `layers[0].anti_patterns`.
- `compare` runs at quick depth by default. A rewrite that moves content to `references/` can
  score lower there, because a shorter SKILL.md can lose `progressive_disclosure` and
  `structural_completeness` points.
- Judge scores change between runs, because the model writes new test prompts and tasks each
  time. Compare static scores when you need a result you can repeat.
