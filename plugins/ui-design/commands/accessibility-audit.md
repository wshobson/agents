---
description: "Audit UI code for WCAG compliance"
argument-hint: "[file-path|component-name|--level AA|AAA]"
---

# Accessibility Audit

Comprehensive audit of UI code for WCAG 2.1/2.2 compliance. Identifies accessibility issues and provides actionable remediation guidance.

## Pre-flight Checks

1. Check if `.ui-design/` directory exists:
   - If not: Create `.ui-design/` directory
   - Create `.ui-design/audits/` subdirectory for audit results

2. Load project context:
   - Check for `conductor/tech-stack.md` for framework info
   - Check for `.ui-design/design-system.json` for color tokens
   - Detect testing framework for a11y test suggestions

## Target and Level Configuration

### If argument provided:

- Parse for file path or component name
- Parse for `--level` flag (AA or AAA)
- Default to WCAG 2.1 Level AA if not specified

### If no argument:

**Q1: Audit Target**

```
What would you like to audit?

1. A specific component (provide name or path)
2. A page/route (provide path)
3. All components in a directory
4. The entire application
5. Recent changes only (last commit)

Enter number or provide a file path:
```

**Q2: Compliance Level**

```
What WCAG compliance level should I audit against?

1. Level A   - Minimum accessibility (must-fix issues)
2. Level AA  - Standard compliance (recommended, most common target)
3. Level AAA - Enhanced accessibility (highest standard)

Note: Each level includes all requirements from previous levels.

Enter number:
```

**Q3: Focus Areas (optional)**

```
Any specific areas to focus on? (Press enter to audit all)

1. Color contrast and visual presentation
2. Keyboard navigation and focus management
3. Screen reader compatibility
4. Forms and input validation
5. Dynamic content and ARIA
6. All areas

Enter numbers (comma-separated) or press enter:
```

## State Management

Create `.ui-design/audits/audit_state.json`:

```json
{
  "audit_id": "{target}_{YYYYMMDD_HHMMSS}",
  "target": "{file_path_or_scope}",
  "wcag_level": "AA",
  "focus_areas": ["all"],
  "status": "in_progress",
  "started_at": "ISO_TIMESTAMP",
  "files_audited": 0,
  "issues_found": {
    "critical": 0,
    "serious": 0,
    "moderate": 0,
    "minor": 0
  },
  "criteria_checked": 0,
  "criteria_passed": 0
}
```

## Audit Execution

### 1. File Discovery

Identify all files to audit:

- If single file: Audit that file
- If component: Find all related files (component, styles, tests)
- If directory: Recursively find UI files (`.tsx`, `.vue`, `.svelte`, etc.)
- If application: Audit all component and page files

### 2. Static Code Analysis

For each file, check against WCAG criteria:

#### Perceivable (WCAG 1.x)

**1.1 Text Alternatives:**

- [ ] Images have `alt` attributes
- [ ] Decorative images use `alt=""` or `role="presentation"`
- [ ] Complex images have extended descriptions
- [ ] Icon buttons have accessible names

**1.2 Time-based Media:**

- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] Media players are keyboard accessible

**1.3 Adaptable:**

- [ ] Semantic HTML structure (headings, lists, landmarks)
- [ ] Proper heading hierarchy (h1 > h2 > h3)
- [ ] Form inputs have associated labels
- [ ] Tables have proper headers
- [ ] Reading order is logical

**1.4 Distinguishable:**

- [ ] Color contrast meets requirements (4.5:1 normal, 3:1 large)
- [ ] Color is not sole means of conveying information
- [ ] Text can be resized to 200%
- [ ] Focus indicators are visible
- [ ] Content reflows at 320px width (AA)

#### Operable (WCAG 2.x)

**2.1 Keyboard Accessible:**

- [ ] All interactive elements are keyboard accessible
- [ ] No keyboard traps
- [ ] Focus order is logical
- [ ] Custom widgets follow ARIA patterns

**2.2 Enough Time:**

- [ ] Time limits can be extended/disabled
- [ ] Auto-updating content can be paused
- [ ] No content times out unexpectedly

**2.3 Seizures:**

- [ ] No content flashes more than 3 times/second
- [ ] Animations can be disabled (prefers-reduced-motion)

**2.4 Navigable:**

- [ ] Skip links present
- [ ] Page has descriptive title
- [ ] Focus visible on all elements
- [ ] Link purpose is clear
- [ ] Multiple ways to find pages

**2.5 Input Modalities:**

- [ ] Touch targets are at least 44x44px (AAA: 44px, AA: 24px)
- [ ] Functionality not dependent on motion
- [ ] Dragging has alternative

#### Understandable (WCAG 3.x)

**3.1 Readable:**

- [ ] Language is specified (`lang` attribute)
- [ ] Unusual words are defined
- [ ] Abbreviations are expanded

**3.2 Predictable:**

- [ ] Focus doesn't trigger unexpected changes
- [ ] Input doesn't trigger unexpected changes
- [ ] Navigation is consistent
- [ ] Components behave consistently

**3.3 Input Assistance:**

- [ ] Error messages are descriptive
- [ ] Labels or instructions provided
- [ ] Error suggestions provided
- [ ] Important submissions can be reviewed

#### Robust (WCAG 4.x)

**4.1 Compatible:**

- [ ] HTML validates (no duplicate IDs)
- [ ] Custom components have proper ARIA
- [ ] Status messages announced to screen readers

### 3. Pattern Detection

Identify common accessibility anti-patterns:

```javascript
// Anti-patterns to detect
const antiPatterns = [
  // Missing alt text
  /<img(?![^>]*alt=)[^>]*>/,

  // onClick without keyboard handler
  /onClick={[^}]+}(?!.*onKeyDown)/,

  // Div/span with click handlers (likely needs role)
  /<(?:div|span)[^>]*onClick/,

  // Non-semantic buttons
  /<(?:div|span)[^>]*role="button"/,

  // Missing form labels
  /<input(?![^>]*(?:aria-label|aria-labelledby|id))[^>]*>/,

  // Positive tabindex (disrupts natural order)
  /tabIndex={[1-9]/,

  // Empty links
  /<a[^>]*>[\s]*<\/a>/,

  // Missing lang attribute
  /<html(?![^>]*lang=)/,

  // Autofocus (usually bad for a11y)
  /autoFocus/,
];
```

### 4. Color Contrast Analysis

If design tokens or CSS available:

- Extract color combinations used in text/background
- Calculate contrast ratios using WCAG formula
- Flag combinations that fail requirements:
  - Normal text: 4.5:1 (AA), 7:1 (AAA)
  - Large text (18pt+ or 14pt bold): 3:1 (AA), 4.5:1 (AAA)
  - UI components: 3:1 (AA)

### 5. ARIA Validation

Check ARIA usage:

- Verify ARIA roles are valid
- Check required ARIA attributes are present
- Verify ARIA values are valid
- Check for redundant ARIA (e.g., `role="button"` on `<button>`)
- Validate ARIA references (aria-labelledby, aria-describedby)

## Output Format

Generate audit report in `.ui-design/audits/{audit_id}.md`:

````markdown
# Accessibility Audit Report

**Audit ID:** {audit_id}
**Date:** {YYYY-MM-DD HH:MM}
**Target:** {target}
**WCAG Level:** {level}
**Standard:** WCAG 2.1

## Executive Summary

**Compliance Status:** {Passing | Needs Improvement | Failing}

| Severity | Count | % of Issues |
| -------- | ----- | ----------- |
| Critical | {n}   | {%}         |
| Serious  | {n}   | {%}         |
| Moderate | {n}   | {%}         |
| Minor    | {n}   | {%}         |

**Criteria Checked:** {n}
**Criteria Passed:** {n} ({%})
**Files Audited:** {n}

## Critical Issues (Must Fix)

These issues prevent users with disabilities from using the interface.

### Issue 1: {Title}

**WCAG Criterion:** {number} - {name} (Level {A|AA|AAA})
**Severity:** Critical
**Location:** `{file}:{line}`
**Element:** `{element_snippet}`

**Problem:**
{Description of the issue}

**Impact:**
{Who is affected and how}

**Remediation:**
{Step-by-step fix instructions}

**Code Fix:**

```{language}
// Before
{current_code}

// After
{fixed_code}
```
````

**Testing:**

- Manual: {how to manually verify}
- Automated: {suggested test}

---

### Issue 2: ...

## Serious Issues

These issues create significant barriers for some users.

### Issue 3: ...

## Moderate Issues

These issues may cause difficulty for some users.

### Issue 4: ...

## Minor Issues

These are best practice improvements.

### Issue 5: ...

## Passed Criteria

The following WCAG criteria passed:

| Criterion | Name                   | Level |
| --------- | ---------------------- | ----- |
| 1.1.1     | Non-text Content       | A     |
| 1.3.1     | Info and Relationships | A     |
| ...       | ...                    | ...   |

## Recommendations

### Quick Wins (< 1 hour each)

1. {Quick fix 1}
2. {Quick fix 2}

### Medium Effort (1-4 hours each)

1. {Medium fix 1}
2. {Medium fix 2}

### Significant Effort (> 4 hours)

1. {Larger fix 1}

## Testing Resources

### Automated Testing

Add these tests to catch regressions:

```javascript
// Example jest-axe test
import { axe, toHaveNoViolations } from "jest-axe";

expect.extend(toHaveNoViolations);

test("component has no accessibility violations", async () => {
  const { container } = render(<Component />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
```

### Manual Testing Checklist

- [ ] Navigate entire page using only keyboard
- [ ] Test with screen reader (VoiceOver/NVDA)
- [ ] Zoom to 200% and verify usability
- [ ] Test with high contrast mode
- [ ] Verify focus indicators are visible
- [ ] Test with prefers-reduced-motion

### Recommended Tools

- axe DevTools browser extension
- WAVE Web Accessibility Evaluator
- Lighthouse accessibility audit
- Color contrast analyzers

---

_Generated by UI Design Accessibility Audit_
_WCAG Reference: https://www.w3.org/WAI/WCAG21/quickref/_

````

## Completion

Update `audit_state.json`:

```json
{
  "status": "complete",
  "completed_at": "ISO_TIMESTAMP",
  "compliance_status": "needs_improvement",
  "issues_found": {
    "critical": 2,
    "serious": 5,
    "moderate": 8,
    "minor": 3
  }
}
````

Display summary:

```
Accessibility Audit Complete!

Target: {target}
WCAG Level: {level}
Compliance Status: {status}

Issues Found:
  - {n} Critical (must fix)
  - {n} Serious
  - {n} Moderate
  - {n} Minor

Full report: .ui-design/audits/{audit_id}.md

What would you like to do next?
1. View details for critical issues
2. Start fixing issues (guided)
3. Generate automated tests
4. Export report for stakeholders
5. Audit another component

Enter number:
```

## Guided Fix Mode

If user selects "Start fixing issues":

```
Let's fix accessibility issues starting with critical ones.

Issue 1 of {n}: {Issue Title}
WCAG {criterion}: {criterion_name}
Location: {file}:{line}

{Show current code}

The fix is:
{Explain the fix}

Should I:
1. Apply this fix automatically
2. Show me the fixed code first
3. Skip this issue
4. Stop fixing

Enter number:
```

Apply fixes one at a time, re-validating after each fix.

## Error Handling

- If file not found: Suggest alternatives, offer to search
- If not UI code: Explain limitation, suggest correct target
- If color extraction fails: Note in report, suggest manual check
- If audit incomplete: Save partial results, offer to resume
