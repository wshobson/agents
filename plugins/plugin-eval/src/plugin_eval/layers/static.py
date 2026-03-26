"""Layer 1: Static analysis — pure Python, no LLM calls, deterministic, <2 seconds."""

from __future__ import annotations

import re
from pathlib import Path

from plugin_eval.models import AntiPattern, LayerResult
from plugin_eval.parser import ParsedAgent, ParsedSkill, parse_plugin, parse_skill

# Weights for skill sub-scores
_SKILL_WEIGHTS = {
    "frontmatter_quality": 0.35,
    "orchestration_wiring": 0.25,
    "progressive_disclosure": 0.15,
    "structural_completeness": 0.10,
    "token_efficiency": 0.10,
    "ecosystem_coherence": 0.05,
}

# MUST/NEVER/ALWAYS threshold for OVER_CONSTRAINED
_OVER_CONSTRAINED_THRESHOLD = 15


def anti_pattern_penalty(count: int) -> float:
    """Return a multiplier in [0.5, 1.0] based on anti-pattern count."""
    return max(0.5, 1.0 - 0.05 * count)


# Line count threshold for BLOATED_SKILL (no references/ dir)
_BLOATED_LINE_THRESHOLD = 800


class StaticAnalyzer:
    """Deterministic structural analysis of plugin/skill quality."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze_skill(self, skill_or_dir: Path | ParsedSkill) -> LayerResult:
        """Analyze a single skill directory (or pre-parsed skill) and return a LayerResult."""
        skill = skill_or_dir if isinstance(skill_or_dir, ParsedSkill) else parse_skill(skill_or_dir)
        anti_patterns = self._detect_skill_anti_patterns(skill)

        sub_scores: dict[str, float] = {
            "frontmatter_quality": self._score_frontmatter(skill),
            "orchestration_wiring": self._score_orchestration(skill),
            "progressive_disclosure": self._score_progressive_disclosure(skill),
            "structural_completeness": self._score_structural_completeness(skill),
            "token_efficiency": self._score_token_efficiency(skill),
            "ecosystem_coherence": self._score_ecosystem_coherence(skill),
        }

        raw_score = sum(sub_scores[name] * weight for name, weight in _SKILL_WEIGHTS.items())
        penalty = anti_pattern_penalty(len(anti_patterns))
        final_score = max(0.0, min(1.0, raw_score * penalty))

        return LayerResult(
            layer="static",
            score=final_score,
            sub_scores=sub_scores,
            anti_patterns=anti_patterns,
            metadata={"skill_name": skill.name, "line_count": skill.line_count},
        )

    def analyze_plugin(self, plugin_dir: Path) -> LayerResult:
        """Analyze an entire plugin directory and return a LayerResult."""
        plugin = parse_plugin(plugin_dir)

        skill_scores: list[float] = []
        all_anti_patterns: list[AntiPattern] = []

        for skill in plugin.skills:
            result = self.analyze_skill(skill)
            skill_scores.append(result.score)
            all_anti_patterns.extend(result.anti_patterns)

        agent_scores: list[float] = []
        for agent in plugin.agents:
            agent_score = self._score_agent(agent)
            agent_scores.append(agent_score)

        all_scores = skill_scores + agent_scores
        final_score = (sum(all_scores) / len(all_scores)) if all_scores else 0.5

        return LayerResult(
            layer="static",
            score=max(0.0, min(1.0, final_score)),
            sub_scores={
                "skill_scores": skill_scores,
                "agent_scores": agent_scores,
            },
            anti_patterns=all_anti_patterns,
            metadata={"plugin_name": plugin.name},
        )

    # ------------------------------------------------------------------
    # Anti-pattern detection
    # ------------------------------------------------------------------

    def _detect_skill_anti_patterns(self, skill: ParsedSkill) -> list[AntiPattern]:
        patterns: list[AntiPattern] = []

        # OVER_CONSTRAINED: too many MUST/ALWAYS/NEVER
        if skill.must_never_always_count > _OVER_CONSTRAINED_THRESHOLD:
            patterns.append(
                AntiPattern(
                    flag="OVER_CONSTRAINED",
                    description=(
                        f"Skill contains {skill.must_never_always_count} MUST/ALWAYS/NEVER "
                        f"directives (threshold: {_OVER_CONSTRAINED_THRESHOLD}). "
                        "Overly prescriptive instructions reduce model flexibility."
                    ),
                    severity=0.10,
                )
            )

        # EMPTY_DESCRIPTION: missing or very short description
        if len(skill.description.strip()) < 20:
            patterns.append(
                AntiPattern(
                    flag="EMPTY_DESCRIPTION",
                    description=(
                        f"Description is too short ({len(skill.description.strip())} chars). "
                        "A good description should be at least 20 characters."
                    ),
                    severity=0.10,
                )
            )

        # MISSING_TRIGGER: no "Use when..." or "Use this skill when..." phrasing
        trigger_pattern = (
            r"\buse\s+(?:this\s+skill\s+)?when\b|\buse\s+proactively\b|\btrigger\s+when\b"
        )
        if not re.search(trigger_pattern, skill.description, re.IGNORECASE):
            patterns.append(
                AntiPattern(
                    flag="MISSING_TRIGGER",
                    description=(
                        'Skill description lacks a "Use when..." trigger phrase. '
                        "Without it, the model cannot determine when to invoke the skill."
                    ),
                    severity=0.15,
                )
            )

        # BLOATED_SKILL: >800 lines without a references/ directory
        if skill.line_count > _BLOATED_LINE_THRESHOLD and not skill.has_references:
            patterns.append(
                AntiPattern(
                    flag="BLOATED_SKILL",
                    description=(
                        f"Skill has {skill.line_count} lines but no references/ directory. "
                        "Large skills should offload supporting material to references/."
                    ),
                    severity=0.10,
                )
            )

        # ORPHAN_REFERENCE: a file in references/ that is explicitly mentioned in SKILL.md
        # via a dead link (i.e. listed in a "[text](references/file)" but does not exist).
        if skill.has_references:
            content = skill.raw_content
            # Find all markdown links that point into references/
            linked_refs = re.findall(r"\(references/([^)]+)\)", content)
            existing = {f.lower() for f in skill.reference_files}
            for linked in linked_refs:
                if Path(linked).name.lower() not in existing:
                    patterns.append(
                        AntiPattern(
                            flag="ORPHAN_REFERENCE",
                            description=(
                                f"SKILL.md links to 'references/{linked}' which does not exist. "
                                "Dead reference links waste context and confuse the model."
                            ),
                            severity=0.05,
                        )
                    )

        # DEAD_CROSS_REF: references a skill/agent that cannot be resolved
        skill_parent = skill.path.parent  # skills/ dir
        for ref in skill.cross_references:
            ref_path = skill_parent / ref
            if not ref_path.exists():
                patterns.append(
                    AntiPattern(
                        flag="DEAD_CROSS_REF",
                        description=(
                            f"Cross-reference to skill/agent '{ref}' cannot be resolved. "
                            "Dead links degrade ecosystem coherence."
                        ),
                        severity=0.05,
                    )
                )

        return patterns

    # ------------------------------------------------------------------
    # Skill sub-score methods
    # ------------------------------------------------------------------

    def _score_frontmatter(self, skill: ParsedSkill) -> float:
        """Score frontmatter quality: name, description length, trigger phrases, pushiness."""
        score = 0.0

        # Name present (0.15)
        if skill.name and skill.name != skill.path.name:
            score += 0.15
        elif skill.name:
            score += 0.10

        # Description length (0.25)
        desc_len = len(skill.description.strip())
        if desc_len >= 100:
            score += 0.25
        elif desc_len >= 60:
            score += 0.20
        elif desc_len >= 30:
            score += 0.15
        elif desc_len >= 10:
            score += 0.05

        # Trigger phrase quality — the primary differentiator (0.60)
        pushiness = self._description_pushiness(skill.description)
        score += pushiness * 0.60

        return min(1.0, score)

    def _score_orchestration(self, skill: ParsedSkill) -> float:
        """Score orchestration wiring: output format, input/receives patterns."""
        # Most skills are workers by default — start at 0.70 (good baseline)
        score = 0.70

        body_lower = skill.raw_content.lower()

        # Output format documentation (+0.10)
        if re.search(r"\boutput\b.*\bformat\b|\bformat\b.*\boutput\b|\breturn.*json\b", body_lower):
            score += 0.10
        # Has return/output language (+0.05)
        if re.search(r"\breturns?\b|\bproduces?\b|\boutputs?\b|\bgenerates?\b", body_lower):
            score += 0.05

        # Input/interface documentation (+0.10)
        if re.search(r"\binput\b|\breceives?\b|\baccepts?\b|\bparameters?\b|\bargs?\b", body_lower):
            score += 0.10

        # Code examples show concrete worker behavior (+0.05)
        if skill.code_block_count >= 2:
            score += 0.05

        # Penalize if the skill declares itself an orchestrator
        if re.search(r"\borchestrat\w*\b|\bcoordinat\w*\b|\bdispatch\w*\b", body_lower):
            score -= 0.15

        return max(0.0, min(1.0, score))

    def _score_progressive_disclosure(self, skill: ParsedSkill) -> float:
        """Score progressive disclosure: line count vs sweet spot, references/assets."""
        score = 0.0
        lines = skill.line_count

        # Sweet spot scoring: skills under 600 lines don't NEED refs
        if 200 <= lines <= 600:
            score += 0.60  # ideal size — refs are a bonus, not required
        elif 100 <= lines < 200:
            score += 0.50  # concise but potentially too short
        elif 600 < lines <= 800:
            score += 0.40  # getting long — refs would help
        elif lines < 100:
            score += 0.20  # stub
        else:
            # >800 lines — refs are essential at this size
            score += 0.15

        # References dir bonus (bigger bonus for larger skills)
        if skill.has_references and skill.reference_files:
            score += 0.25 if lines > 400 else 0.15

        # Assets dir bonus
        if skill.has_assets and skill.asset_files:
            score += 0.15

        return min(1.0, score)

    def _score_structural_completeness(self, skill: ParsedSkill) -> float:
        """Score structural completeness and technical depth."""
        score = 0.0

        # Headings — structure
        heading_count = skill.h2_count + skill.h3_count
        if heading_count >= 6:
            score += 0.20
        elif heading_count >= 4:
            score += 0.15
        elif heading_count >= 2:
            score += 0.10

        # Code blocks — actionability
        if skill.code_block_count >= 5:
            score += 0.20
        elif skill.code_block_count >= 3:
            score += 0.15
        elif skill.code_block_count >= 1:
            score += 0.10

        # Multi-language depth — expert-audience signal
        unique_langs = set(skill.code_block_languages)
        if len(unique_langs) >= 3:
            score += 0.15  # covers multiple languages/formats
        elif len(unique_langs) >= 2:
            score += 0.10

        # Examples section
        if skill.has_examples:
            score += 0.15

        # Troubleshooting section
        if skill.has_troubleshooting:
            score += 0.15

        # Technical depth signal: tables, diagrams, decision matrices
        body_lower = skill.raw_content.lower()
        if re.search(r"\|.*\|.*\|", skill.raw_content):  # markdown tables
            score += 0.10
        if re.search(r"(decision|when to use|comparison|tradeoff)", body_lower):
            score += 0.05

        return min(1.0, score)

    def _score_token_efficiency(self, skill: ParsedSkill) -> float:
        """Score token efficiency: MUST/NEVER/ALWAYS density, repetition detection."""
        score = 1.0
        lines = max(skill.line_count, 1)

        # MUST/NEVER/ALWAYS density — penalise above 1 per 10 lines
        density = skill.must_never_always_count / lines
        if density > 0.5:
            score -= 0.4
        elif density > 0.2:
            score -= 0.2
        elif density > 0.1:
            score -= 0.1

        # Repetition detection: split body into non-empty lines, look for duplicates
        body_lines = [
            ln.strip()
            for ln in skill.raw_content.splitlines()
            if ln.strip() and not ln.startswith("---")
        ]
        unique = len(set(body_lines))
        total = len(body_lines)
        if total > 0:
            repetition_ratio = 1.0 - (unique / total)
            score -= repetition_ratio * 0.4

        return max(0.0, min(1.0, score))

    def _score_ecosystem_coherence(self, skill: ParsedSkill) -> float:
        """Score ecosystem coherence: cross-references, related/see-also mentions."""
        score = 0.50  # baseline — most skills are standalone and that's fine

        # Cross-references to other skills/agents
        if skill.cross_references:
            score += min(0.25, len(skill.cross_references) * 0.08)

        # "related" or "see also" mentions
        body_lower = skill.raw_content.lower()
        if re.search(r"\brelated\b|\bsee also\b|\bcompanion\b|\bcomplement", body_lower):
            score += 0.25

        return min(1.0, score)

    # ------------------------------------------------------------------
    # Agent scoring
    # ------------------------------------------------------------------

    def _score_agent(self, agent: ParsedAgent) -> float:
        """Produce a simple quality score for an agent."""
        score = 0.5  # baseline

        # Proactive trigger
        if agent.has_proactive_trigger:
            score += 0.2

        # Tools restriction (scoped permissions)
        if agent.has_tools_restriction and len(agent.tools) > 0:
            score += 0.1

        # Description length
        if len(agent.description.strip()) >= 40:
            score += 0.1
        elif len(agent.description.strip()) >= 20:
            score += 0.05

        # Model specified
        if agent.model:
            score += 0.1

        return min(1.0, score)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _anti_pattern_penalty(self, count: int) -> float:
        """Delegate to module-level anti_pattern_penalty (kept for backward compatibility)."""
        return anti_pattern_penalty(count)

    def _description_pushiness(self, description: str) -> float:
        """Score how well a description guides autonomous invocation (0–1)."""
        score = 0.0
        desc_lower = description.lower()

        # "Use when" / "Use this skill when" phrases (0.25)
        if re.search(r"\buse\s+(this\s+skill\s+)?when\b", desc_lower):
            score += 0.25

        # "Use PROACTIVELY" or "proactively" (0.15)
        if re.search(r"\bproactively\b", desc_lower):
            score += 0.15

        # Additional trigger keywords (0.10)
        if re.search(r"\bautomatically\b|\balways\s+use\b|\btrigger\b|\binvoke\b", desc_lower):
            score += 0.10

        # Specificity bonus: multiple concrete contexts listed (0.20)
        # Count comma-separated or "or"-separated use cases in description
        use_cases = len(re.findall(r",\s*(?:or\s+)?(?:when|for|during|implementing|building|creating|debugging|testing|deploying|configuring|setting up)", desc_lower))
        if use_cases >= 3:
            score += 0.20
        elif use_cases >= 1:
            score += 0.10

        # Describes specific contexts or file types (0.15)
        if re.search(r"\b(when\s+\w+ing|for\s+\w+ing|during\s+\w+ing)\b", desc_lower):
            score += 0.15

        # Reasonable length (>= 40 chars) (0.10)
        if len(description.strip()) >= 40:
            score += 0.10

        return min(1.0, score)
