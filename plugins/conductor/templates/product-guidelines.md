# Product Guidelines

## Voice & Tone

### Brand Voice

{{BRAND_VOICE_DESCRIPTION}}

### Voice Attributes

- **{{ATTRIBUTE_1}}:** {{ATTRIBUTE_1_DESCRIPTION}}
- **{{ATTRIBUTE_2}}:** {{ATTRIBUTE_2_DESCRIPTION}}
- **{{ATTRIBUTE_3}}:** {{ATTRIBUTE_3_DESCRIPTION}}

### Tone Variations by Context

| Context        | Tone                 | Example                 |
| -------------- | -------------------- | ----------------------- |
| Success states | {{SUCCESS_TONE}}     | {{SUCCESS_EXAMPLE}}     |
| Error states   | {{ERROR_TONE}}       | {{ERROR_EXAMPLE}}       |
| Onboarding     | {{ONBOARDING_TONE}}  | {{ONBOARDING_EXAMPLE}}  |
| Empty states   | {{EMPTY_STATE_TONE}} | {{EMPTY_STATE_EXAMPLE}} |

### Words We Use

- {{PREFERRED_WORD_1}}
- {{PREFERRED_WORD_2}}
- {{PREFERRED_WORD_3}}

### Words We Avoid

- {{AVOIDED_WORD_1}}
- {{AVOIDED_WORD_2}}
- {{AVOIDED_WORD_3}}

## Messaging Guidelines

### Core Messages

**Primary Message:**

> {{PRIMARY_MESSAGE}}

**Supporting Messages:**

1. {{SUPPORTING_MESSAGE_1}}
2. {{SUPPORTING_MESSAGE_2}}
3. {{SUPPORTING_MESSAGE_3}}

### Message Hierarchy

1. **Must Communicate:** {{MUST_COMMUNICATE}}
2. **Should Communicate:** {{SHOULD_COMMUNICATE}}
3. **Could Communicate:** {{COULD_COMMUNICATE}}

### Audience-Specific Messaging

| Audience       | Key Message   | Proof Points |
| -------------- | ------------- | ------------ |
| {{AUDIENCE_1}} | {{MESSAGE_1}} | {{PROOF_1}}  |
| {{AUDIENCE_2}} | {{MESSAGE_2}} | {{PROOF_2}}  |

## Design Principles

### Principle 1: {{PRINCIPLE_1_NAME}}

{{PRINCIPLE_1_DESCRIPTION}}

**Do:**

- {{PRINCIPLE_1_DO_1}}
- {{PRINCIPLE_1_DO_2}}

**Don't:**

- {{PRINCIPLE_1_DONT_1}}
- {{PRINCIPLE_1_DONT_2}}

### Principle 2: {{PRINCIPLE_2_NAME}}

{{PRINCIPLE_2_DESCRIPTION}}

**Do:**

- {{PRINCIPLE_2_DO_1}}
- {{PRINCIPLE_2_DO_2}}

**Don't:**

- {{PRINCIPLE_2_DONT_1}}
- {{PRINCIPLE_2_DONT_2}}

### Principle 3: {{PRINCIPLE_3_NAME}}

{{PRINCIPLE_3_DESCRIPTION}}

**Do:**

- {{PRINCIPLE_3_DO_1}}
- {{PRINCIPLE_3_DO_2}}

**Don't:**

- {{PRINCIPLE_3_DONT_1}}
- {{PRINCIPLE_3_DONT_2}}

## Accessibility Standards

### Compliance Target

{{ACCESSIBILITY_STANDARD}} (e.g., WCAG 2.1 AA)

### Core Requirements

#### Perceivable

- All images have meaningful alt text
- Color is not the only means of conveying information
- Text has minimum contrast ratio of 4.5:1
- Content is readable at 200% zoom

#### Operable

- All functionality available via keyboard
- No content flashes more than 3 times per second
- Skip navigation links provided
- Focus indicators clearly visible

#### Understandable

- Language is clear and simple
- Navigation is consistent
- Error messages are descriptive and helpful
- Labels and instructions are clear

#### Robust

- Valid HTML markup
- ARIA labels used appropriately
- Compatible with assistive technologies
- Progressive enhancement approach

### Testing Requirements

- Screen reader testing with {{SCREEN_READER}}
- Keyboard-only navigation testing
- Color contrast verification
- Automated accessibility scans

## Error Handling Philosophy

### Error Prevention

- Validate input early and often
- Provide clear constraints and requirements upfront
- Use inline validation where appropriate
- Confirm destructive actions

### Error Communication

#### Principles

1. **Be specific:** Tell users exactly what went wrong
2. **Be helpful:** Explain how to fix the problem
3. **Be human:** Use friendly, non-technical language
4. **Be timely:** Show errors as soon as they're detected

#### Error Message Structure

```
[What happened] + [Why it happened (if relevant)] + [How to fix it]
```

#### Examples

| Bad             | Good                                                 |
| --------------- | ---------------------------------------------------- |
| "Invalid input" | "Email address must include @ symbol"                |
| "Error 500"     | "We couldn't save your changes. Please try again."   |
| "Failed"        | "Unable to connect. Check your internet connection." |

### Error States

| Severity | Visual Treatment       | User Action Required |
| -------- | ---------------------- | -------------------- |
| Info     | {{INFO_TREATMENT}}     | Optional             |
| Warning  | {{WARNING_TREATMENT}}  | Recommended          |
| Error    | {{ERROR_TREATMENT}}    | Required             |
| Critical | {{CRITICAL_TREATMENT}} | Immediate            |

### Recovery Patterns

- Auto-save user progress where possible
- Provide clear "try again" actions
- Offer alternative paths when primary fails
- Preserve user input on errors
