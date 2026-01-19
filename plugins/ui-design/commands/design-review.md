---
description: "Review existing UI for issues and improvements"
argument-hint: "[file-path|component-name]"
---

# Design Review

Review existing UI code for design issues, usability problems, and improvement opportunities. Provides actionable recommendations.

## Pre-flight Checks

1. Check if `.ui-design/` directory exists:
   - If not: Create `.ui-design/` directory
   - Create `.ui-design/reviews/` subdirectory for storing review results

2. Load project context if available:
   - Check for `conductor/product.md` for product context
   - Check for `conductor/tech-stack.md` for framework info
   - Check for `.ui-design/design-system.json` for design tokens

## Target Identification

### If argument provided:

- If file path: Validate file exists, read the file
- If component name: Search codebase for matching component files
- If not found: Display error with suggestions

### If no argument:

Ask user to specify target:

```
What would you like me to review?

1. A specific component (provide name or path)
2. A page/route (provide path)
3. The entire UI directory
4. Recent changes (last commit)

Enter number or provide a file path:
```

## Interactive Review Configuration

**CRITICAL RULES:**

- Ask ONE question per turn
- Wait for user response before proceeding
- Gather context to provide relevant feedback

### Q1: Review Focus

```
What aspects should I focus on?

1. Visual design (spacing, alignment, typography, colors)
2. Usability (interaction patterns, accessibility basics)
3. Code quality (patterns, maintainability, reusability)
4. Performance (render optimization, bundle size)
5. Comprehensive (all of the above)

Enter number:
```

### Q2: Design Context (if visual/usability selected)

```
What is this UI's primary purpose?

1. Data display (dashboards, tables, reports)
2. Data entry (forms, wizards, editors)
3. Navigation (menus, sidebars, breadcrumbs)
4. Content consumption (articles, media, feeds)
5. E-commerce (product display, checkout)
6. Other (describe)

Enter number or description:
```

### Q3: Target Platform

```
What platform(s) should I consider?

1. Desktop only
2. Mobile only
3. Responsive (desktop + mobile)
4. All platforms (desktop, tablet, mobile)

Enter number:
```

## State Management

Create/update `.ui-design/reviews/review_state.json`:

```json
{
  "review_id": "{target}_{YYYYMMDD_HHMMSS}",
  "target": "{file_path_or_component}",
  "focus_areas": ["visual", "usability", "code", "performance"],
  "context": "{purpose}",
  "platform": "{platform}",
  "status": "in_progress",
  "started_at": "ISO_TIMESTAMP",
  "issues_found": 0,
  "severity_counts": {
    "critical": 0,
    "major": 0,
    "minor": 0,
    "suggestion": 0
  }
}
```

## Review Execution

### 1. Code Analysis

Read and analyze the target files:

- Parse component structure
- Identify styling approach (CSS, Tailwind, styled-components, etc.)
- Detect framework (React, Vue, Svelte, etc.)
- Note component composition patterns

### 2. Visual Design Review

Check for:

**Spacing & Layout:**

- Inconsistent margins/padding
- Misaligned elements
- Unbalanced whitespace
- Magic numbers vs. design tokens

**Typography:**

- Font size consistency
- Line height appropriateness
- Text contrast ratios
- Font weight usage

**Colors:**

- Color contrast accessibility
- Consistent color usage
- Semantic color application
- Dark mode support (if applicable)

**Visual Hierarchy:**

- Clear primary actions
- Appropriate emphasis
- Scannable content structure

### 3. Usability Review

Check for:

**Interaction Patterns:**

- Clear clickable/tappable areas
- Appropriate hover/focus states
- Loading state indicators
- Error state handling
- Empty state handling

**User Flow:**

- Logical tab order
- Clear call-to-action
- Predictable behavior
- Feedback on actions

**Cognitive Load:**

- Information density
- Progressive disclosure
- Clear labels and instructions
- Consistent patterns

### 4. Code Quality Review

Check for:

**Component Patterns:**

- Single responsibility
- Prop drilling depth
- State management appropriateness
- Component reusability

**Styling Patterns:**

- Consistent naming conventions
- Reusable style definitions
- Media query organization
- CSS specificity issues

**Maintainability:**

- Clear component boundaries
- Documentation/comments
- Test coverage
- Accessibility attributes

### 5. Performance Review

Check for:

**Render Optimization:**

- Unnecessary re-renders
- Missing memoization
- Large component trees
- Expensive computations in render

**Asset Optimization:**

- Image sizes and formats
- Icon implementation
- Font loading strategy
- Code splitting opportunities

## Output Format

Generate review report in `.ui-design/reviews/{review_id}.md`:

````markdown
# Design Review: {Component/File Name}

**Review ID:** {review_id}
**Reviewed:** {YYYY-MM-DD HH:MM}
**Target:** {file_path}
**Focus:** {focus_areas}

## Summary

{2-3 sentence overview of findings}

**Issues Found:** {total_count}

- Critical: {count}
- Major: {count}
- Minor: {count}
- Suggestions: {count}

## Critical Issues

### Issue 1: {Title}

**Severity:** Critical
**Location:** {file}:{line}
**Category:** {Visual|Usability|Code|Performance}

**Problem:**
{Description of the issue}

**Impact:**
{Why this matters for users/maintainability}

**Recommendation:**
{Specific fix suggestion}

**Code Example:**

```{language}
// Before
{current_code}

// After
{suggested_code}
```
````

---

## Major Issues

### Issue 2: {Title}

...

## Minor Issues

### Issue 3: {Title}

...

## Suggestions

### Suggestion 1: {Title}

...

## Positive Observations

{List things done well to reinforce good patterns}

- {Positive observation 1}
- {Positive observation 2}

## Next Steps

1. {Prioritized action 1}
2. {Prioritized action 2}
3. {Prioritized action 3}

---

_Generated by UI Design Review. Run `/ui-design:design-review` again after fixes._

```

## Completion

After generating report:

1. Update `review_state.json`:
   - Set `status: "complete"`
   - Update issue counts

2. Display summary:

```

Design Review Complete!

Target: {component/file}
Issues Found: {total}

- {critical} Critical
- {major} Major
- {minor} Minor
- {suggestions} Suggestions

Full report: .ui-design/reviews/{review_id}.md

What would you like to do next?

1. View detailed findings for a specific issue
2. Start implementing fixes
3. Export report (markdown/JSON)
4. Review another component

```

## Follow-up Actions

If user selects "Start implementing fixes":

```

Which issues would you like to address?

1. All critical issues first
2. All issues in current file
3. Specific issue (enter number)
4. Generate a fix plan for all issues

Enter choice:

```

Guide user through fixes one at a time, updating the review report as issues are resolved.

## Error Handling

- If target file not found: Suggest similar files, offer to search
- If file is not UI code: Explain and ask for correct target
- If review fails mid-way: Save partial results, offer to resume
```
