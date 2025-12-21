# Anti-Hallucination Protocol

## Purpose
Prevent fabrication of information by establishing verification requirements and uncertainty handling procedures.

## Triggers Requiring Verification

### High-Risk Claims (MUST VERIFY)
- Specific numbers, dates, statistics
- Named entities with attributed facts
- Specific events claimed to have happened
- Citations or sources
- Current state of affairs (prices, versions, availability)
- Technical specifications (API versions, library functions)
- Legal or compliance statements

### Medium-Risk Claims (SHOULD HEDGE)
- Best practices and recommendations
- Performance characteristics
- Technology comparisons
- Industry trends

### Low-Risk Claims (ACCEPTABLE)
- General programming concepts
- Well-established patterns
- Basic language features
- Common conventions

## Verification Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                    CLAIM MADE                            │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  What is the source?  │
              └───────────┬───────────┘
                          │
    ┌─────────┬───────────┼───────────┬─────────┐
    │         │           │           │         │
    ▼         ▼           ▼           ▼         ▼
┌───────┐ ┌───────┐ ┌─────────┐ ┌─────────┐ ┌───────┐
│ Tool  │ │ User  │ │Training │ │Inference│ │Unknown│
│Output │ │ Input │ │  Data   │ │   Only  │ │       │
└───┬───┘ └───┬───┘ └────┬────┘ └────┬────┘ └───┬───┘
    │         │          │           │          │
    ▼         ▼          ▼           ▼          ▼
 VERIFIED  VERIFIED   ADD HEDGE   FLAG FOR   REMOVE OR
                                 VERIFY      REWRITE
```

## Source Classification

### Level 1: Verified (State as Fact)
- Tool outputs (file reads, command results)
- User-provided information
- System-generated data
- Current session context

### Level 2: Training Knowledge (Add Hedge)
- Programming patterns
- General technical concepts
- Historical facts (pre-cutoff)
- Standard practices

**Hedging Language:**
- "Based on my knowledge..."
- "Typically..."
- "As of my last update..."
- "Generally speaking..."

### Level 3: Inference (Add Strong Hedge)
- Predictions about behavior
- Assumptions about user intent
- Extrapolations from patterns

**Strong Hedging Language:**
- "It appears that..."
- "I believe..."
- "This likely..."
- "My understanding is..."

### Level 4: Unknown (Acknowledge)
- Current events (post-cutoff)
- Specific implementation details not seen
- User-specific configurations

**Acknowledgment Language:**
- "I don't have confirmed information about..."
- "I would need to verify..."
- "Please confirm whether..."

## Implementation Guidelines

### For All Agents

```python
def validate_claim(claim: str, source: str) -> ValidatedClaim:
    """
    Validate a claim before including in output.
    """
    source_level = classify_source(source)

    if source_level == "verified":
        return ValidatedClaim(claim, confidence=100, hedge=None)

    elif source_level == "training":
        hedge = select_appropriate_hedge(claim)
        return ValidatedClaim(claim, confidence=80, hedge=hedge)

    elif source_level == "inference":
        hedge = select_strong_hedge(claim)
        return ValidatedClaim(claim, confidence=60, hedge=hedge)

    elif source_level == "unknown":
        return ValidatedClaim(
            claim=None,
            alternative=f"I don't have verified information about {extract_topic(claim)}",
            confidence=0
        )
```

### Claim Categories

| Category | Example | Required Action |
|----------|---------|-----------------|
| API Version | "FastAPI 0.109.0" | Verify or use "current version" |
| Price | "$10/month" | Verify or say "check pricing page" |
| Date | "Released March 2024" | Verify or hedge with "around" |
| Statistic | "80% of developers" | Cite source or remove |
| Function | "requests.get()" | Verify exists or use generic |
| Config | "max_connections=100" | Verify or say "configure as needed" |

## Red Flags to Catch

### In Your Own Output
- [ ] Specific version numbers not from tools
- [ ] Exact dates without verification
- [ ] Statistics without sources
- [ ] Quotes attributed to specific people
- [ ] Current pricing or availability
- [ ] "The latest version..."
- [ ] "According to..."

### Correction Template
When catching a potential hallucination:

```markdown
[CORRECTION]
I need to correct my previous statement about {topic}.
I stated: "{original claim}"
However, I should clarify: "{corrected/hedged version}"
Reason: {why the original was problematic}
[/CORRECTION]
```

## Escalation Triggers

Escalate to human/Founder when:
- Asked to provide specific facts that cannot be verified
- Conflicting information from multiple sources
- User seems to be relying on claim for important decision
- Legal, financial, or medical information requested
- Claim about current events or recent changes

## Quality Metrics

Track and report:
- Hedging rate (% of claims with hedges)
- Correction rate (how often corrections needed)
- User feedback on accuracy
- Verification requests made
