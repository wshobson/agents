---
name: security-requirement-extraction
description: Derive security requirements from threat models and business context. Use when translating threats into actionable requirements, creating security user stories, or building security test cases.
---

# Security Requirement Extraction

Transform threat analysis into actionable security requirements.

## When to Use This Skill

- Converting threat models to requirements
- Writing security user stories
- Creating security test cases
- Building security acceptance criteria
- Compliance requirement mapping
- Security architecture documentation

## Core Concepts

### 1. Requirement Categories

```
Business Requirements → Security Requirements → Technical Controls
         ↓                       ↓                      ↓
  "Protect customer    "Encrypt PII at rest"   "AES-256 encryption
   data"                                        with KMS key rotation"
```

### 2. Security Requirement Types

| Type               | Focus                   | Example                               |
| ------------------ | ----------------------- | ------------------------------------- |
| **Functional**     | What system must do     | "System must authenticate users"      |
| **Non-functional** | How system must perform | "Authentication must complete in <2s" |
| **Constraint**     | Limitations imposed     | "Must use approved crypto libraries"  |

### 3. Requirement Attributes

| Attribute        | Description                 |
| ---------------- | --------------------------- |
| **Traceability** | Links to threats/compliance |
| **Testability**  | Can be verified             |
| **Priority**     | Business importance         |
| **Risk Level**   | Impact if not met           |

## Templates and detailed worked examples

Full template library lives in `references/details.md`. Read that file when you need concrete templates for this skill.

## Best Practices

### Do's

- **Trace to threats** - Every requirement should map to threats
- **Be specific** - Vague requirements can't be tested
- **Include acceptance criteria** - Define "done"
- **Consider compliance** - Map to frameworks early
- **Review regularly** - Requirements evolve with threats

### Don'ts

- **Don't be generic** - "Be secure" is not a requirement
- **Don't skip rationale** - Explain why it matters
- **Don't ignore priorities** - Not all requirements are equal
- **Don't forget testability** - If you can't test it, you can't verify it
- **Don't work in isolation** - Involve stakeholders
