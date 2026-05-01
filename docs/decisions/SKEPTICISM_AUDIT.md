SKEPTICISM AUDIT: OTHER QUESTIONABLE CLAIMS
═════════════════════════════════════════════════════════════════════════

1. OPTION 1 REJECTION (ADR 1, line 34)
────────────────────────────────────────────────────────────────────────

Claim: "No per-plugin scoping. A user working on Python gets the same 
context as one working on Kubernetes. Skills auto-activate against the 
full catalog with no way to narrow focus."

Skepticism Level: ⚠️ MEDIUM

Issues:
  - "No way to narrow focus" assumes Gemini CLI skills can't be selectively 
    filtered or deactivated by the user
  - Gemini CLI has skill descriptions — users could be taught to ignore 
    irrelevant ones
  - Modern LLMs are good at filtering context; "bloat" may not be the killer
  - How bad is "all 150 skills in context"? Did you measure token cost?

Real question: Is Option 1 actually that bad? Would one monolithic 
GEMINI.md with all 79 plugins documented work?

Verdict: WEAK REJECTION — Should have included token cost analysis or 
user experience testing data.

═════════════════════════════════════════════════════════════════════════

2. OPTION 2 REJECTION (ADR 1, line 41)
────────────────────────────────────────────────────────────────────────

Claim: "79 separate repos to maintain, 79 separate `gemini extensions 
install` calls for users, no central catalog, and ongoing sync burden 
when plugins are added or changed. The maintenance cost is prohibitive."

Skepticism Level: 🔴 HIGH

Issues:
  - "79 separate repos" — but you COULD have:
    * A monorepo with 79 subdirectories
    * A mono-extension that reads plugin metadata from a central location
    * Automated workflows to sync all repos from a template
  - "79 separate install calls" — but you COULD have:
    * One install script: `install-all-claude-agents.sh`
    * A "plugin bundle" meta-extension that installs 10-20 common ones
    * Better CLI UX (does Gemini not support this?)
  - "No central catalog" — questionable
    * GitHub topics/search can serve as catalog
    * You could maintain a catalog.md that links to all 79
  - "Maintenance cost is prohibitive" — NOT VERIFIED
    * GitHub Actions can automate sync across repos
    * Monorepo tooling (lerna, nx, turborepo) handles this
    * Cost never actually quantified

Real question: Did you actually evaluate monorepo + automation, or did 
you reject it too quickly?

Verdict: WEAK REJECTION — Appears to assume worst case. Automation could 
mitigate most concerns. Should have explored hybrid models.

═════════════════════════════════════════════════════════════════════════

3. OPTION 3 REJECTION (ADR 1, line 47)
────────────────────────────────────────────────────────────────────────

Claim: "Subdirectory scanning would only work for users who clone the 
repo and run `gemini` from inside it — a developer workflow, not an 
end-user one."

Skepticism Level: 🔴 CRITICAL

Issues:
  - This rejection is UNDERMINED by the fact that you ALREADY DO THIS
  - You have 79 per-plugin GEMINI.md files in the repo
  - You're asking devs to clone and cd into plugin directories anyway 
    (that's the future-proofing rationale)
  - So Option 3 wasn't really "rejected for being dev-only" — you 
    chose Option 4 which ALSO requires cloning for power users
  - The distinction is artificial: "developer workflow" vs 
    "end-user workflow" for an extension that requires installation

Real question: If power users are cloning the repo anyway, why does 
Option 3 lose to Option 4?

Verdict: CIRCULAR LOGIC — The rejection hinges on a false distinction 
you then contradict by including per-plugin files for the exact "dev 
workflow" you rejected Option 3 for.

═════════════════════════════════════════════════════════════════════════

4. OPTION 1 REJECTION IN ADR 2 (line 43)
────────────────────────────────────────────────────────────────────────

Claim: "Gemini CLI has no `.geminiignore` equivalent for extension files 
— all files in the extension repo are included in the install"

Skepticism Level: ⚠️ MEDIUM

Issues:
  - Is this actually verified against official Gemini CLI docs?
  - We checked the extension reference — did we check all docs?
  - Even if true, you COULD:
    * Use a build step to filter files before installing
    * Ask users to install from a filtered branch
    * Maintain a separate "distribution" repo without per-plugin files
  - The claim "all files in the extension repo are included" might mean:
    * All .md files included, or
    * All files at all levels, or
    * Something else?

Real question: Have you actually tested whether Gemini CLI respects 
.gitignore or has any filtering mechanism?

Verdict: UNVERIFIED — Claim about Gemini CLI's file inclusion behavior 
needs explicit testing, not assumption.

═════════════════════════════════════════════════════════════════════════

5. DECISION 3 IN ADR 3 (line 51)
────────────────────────────────────────────────────────────────────────

Claim: "Real extension examples examined on GitHub (e.g., 
`gemini-cli-extensions/security`, `gemini-cli-extensions/conductor`) 
do not use `@{}` file inclusion — they embed all context in the prompt 
field directly."

Skepticism Level: 🔴 HIGH

Issues:
  - NO CITATIONS — Which exact repos? URLs? Commits?
  - "Real extension examples" is vague — how many did you check? 1? 100?
  - Survivorship bias: Maybe other extensions DO use @{}, but they're 
    archived or less popular, so you didn't find them
  - Pattern inference from 2-3 examples is weak
  - Just because existing extensions embed context doesn't mean it's 
    REQUIRED — they might do it for other reasons (simplicity, age, etc)
  - The claim "developers have hit the same wall" is pure speculation

Real question: Did you actually test @{path} with an extension-relative 
path, or just assume it doesn't work?

Verdict: WEAK EVIDENCE — Based on unnamed GitHub repos and pattern 
inference, not testing or documentation review.

═════════════════════════════════════════════════════════════════════════

6. CONSEQUENCES CLAIM IN ADR 3 (line 85)
────────────────────────────────────────────────────────────────────────

Claim: "Complex multi-phase orchestration commands (e.g., 
`feature-development`, `tdd-cycle`) lose their detailed step sequences 
in the Gemini version."

Skepticism Level: ⚠️ MEDIUM — NEEDS MEASUREMENT

Issues:
  - How much is "lost"? You don't show examples
  - Do the TOML versions actually work? Have they been tested?
  - Is this a real limitation, or theoretical?
  - Could the step sequences be re-written for TOML format?
  - Have you compared Claude Code command execution to Gemini TOML?

Real question: Can you demonstrate that a complex command actually 
fails or significantly degrades in Gemini TOML format?

Verdict: UNVERIFIED LIMITATION — Stated but not demonstrated.

═════════════════════════════════════════════════════════════════════════

7. PHASEOUT CLAIM IN ADR 1 (line 96)
────────────────────────────────────────────────────────────────────────

Claim: "Permanent gaps vs. Claude Code:
  - No per-plugin selective install (Gemini architectural limit)
  - No per-agent model tier assignment (Gemini is session-level model only)
  - No parallel subagent fan-out (Gemini executes sequentially)"

Skepticism Level: ⚠️ MEDIUM

Issues:
  - "Architectural limit" — Is this actually a limit, or just how it 
    works TODAY?
  - Gemini CLI is actively developed — these limits may change
  - No timeline or certainty stated ("permanent" is a strong word)
  - Some of these might be workable:
    * Per-plugin install: monorepo as workaround
    * Per-agent model: could be handled in agent system prompts
    * Sequential execution: might be fine if each step is well-designed

Real question: Are these really PERMANENT, or just current limitations?

Verdict: OVERSTATEMENT — "Permanent" is too strong without explicit 
verification of Gemini CLI roadmap.

═════════════════════════════════════════════════════════════════════════

SUMMARY OF SKEPTICISM
───────────────────────────────────────────────────────────────────────────

🔴 HIGH SKEPTICISM (4 items):
  - Option 2 rejection: Assumes worst case, no automation explored
  - Option 3 rejection: Circular logic undermined by your own design
  - ADR 3 example claims: No citations, unnamed repos
  - "Permanent gaps" claim: Overstatement without roadmap verification

⚠️  MEDIUM SKEPTICISM (3 items):
  - Option 1 rejection: Token cost never measured
  - ADR 2 .geminiignore claim: Untested assumption
  - ADR 3 orchestration loss: Undemonstrated limitation

PATTERN: The ADRs make claims but don't provide empirical validation.
They rely on reasoning and logical analysis, which is good, but lack
user testing, performance measurements, or code demonstrations.

