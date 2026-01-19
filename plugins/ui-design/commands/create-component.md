---
description: "Guided component creation with proper patterns"
argument-hint: "[component-name]"
---

# Create Component

Guided workflow for creating new UI components following established patterns and best practices.

## Pre-flight Checks

1. Check if `.ui-design/` directory exists:
   - If not: Create `.ui-design/` directory
   - Create `.ui-design/components/` subdirectory for component tracking

2. Detect project configuration:
   - Scan for framework (React, Vue, Svelte, Angular)
   - Scan for styling approach (CSS Modules, Tailwind, styled-components, etc.)
   - Check for existing component patterns in `src/components/` or similar
   - Load `.ui-design/design-system.json` if exists

3. Load project context:
   - Check for `conductor/tech-stack.md`
   - Check for existing component conventions

4. If no framework detected:

   ```
   I couldn't detect a UI framework. What are you using?

   1. React
   2. Vue 3
   3. Svelte
   4. Angular
   5. Vanilla JavaScript/HTML
   6. Other (specify)

   Enter number:
   ```

## Component Specification

**CRITICAL RULES:**

- Ask ONE question per turn
- Wait for user response before proceeding
- Build complete specification before generating code

### Q1: Component Name (if not provided)

```
What should this component be called?

Guidelines:
- Use PascalCase (e.g., UserCard, DataTable)
- Be descriptive but concise
- Avoid generic names like "Component" or "Widget"

Enter component name:
```

### Q2: Component Purpose

```
What is this component's primary purpose?

1. Display content (cards, lists, text blocks)
2. Collect input (forms, selects, toggles)
3. Navigation (menus, tabs, breadcrumbs)
4. Feedback (alerts, toasts, modals)
5. Layout (containers, grids, sections)
6. Data visualization (charts, graphs, indicators)
7. Other (describe)

Enter number or description:
```

### Q3: Component Complexity

```
What is the component's complexity level?

1. Simple - Single responsibility, minimal props, no internal state
2. Compound - Multiple parts, some internal state, few props
3. Complex - Multiple subcomponents, state management, many props
4. Composite - Orchestrates other components, significant logic

Enter number:
```

### Q4: Props/Inputs Specification

```
What props/inputs should this component accept?

For each prop, provide:
- Name (camelCase)
- Type (string, number, boolean, function, object, array)
- Required or optional
- Default value (if optional)

Example format:
title: string, required
variant: "primary" | "secondary", optional, default: "primary"
onClick: function, optional

Enter props (one per line, empty line when done):
```

### Q5: State Requirements

```
Does this component need internal state?

1. Stateless - Pure presentational, all data via props
2. Local state - Simple internal state (open/closed, hover, etc.)
3. Controlled - State managed by parent, component reports changes
4. Uncontrolled - Manages own state, exposes refs for parent access
5. Hybrid - Supports both controlled and uncontrolled modes

Enter number:
```

### Q6: Composition Pattern (if complexity > Simple)

```
How should child content be handled?

1. No children - Self-contained component
2. Simple children - Accepts children prop for content
3. Named slots - Multiple content areas (header, body, footer)
4. Compound components - Exports subcomponents (e.g., Card.Header, Card.Body)
5. Render props - Accepts render function for flexibility

Enter number:
```

### Q7: Accessibility Requirements

```
What accessibility features are needed?

1. Basic - Semantic HTML, aria-labels where needed
2. Keyboard navigation - Full keyboard support, focus management
3. Screen reader optimized - Live regions, announcements
4. Full WCAG AA - All applicable success criteria

Enter number:
```

### Q8: Styling Approach

```
How should this component be styled?

Detected: {detected_approach}

1. Use detected approach ({detected_approach})
2. CSS Modules
3. Tailwind CSS
4. Styled Components / Emotion
5. Plain CSS/SCSS
6. Other (specify)

Enter number:
```

## State Management

Create `.ui-design/components/{component_name}.json`:

```json
{
  "name": "{ComponentName}",
  "created_at": "ISO_TIMESTAMP",
  "purpose": "{purpose}",
  "complexity": "{level}",
  "props": [
    {
      "name": "{prop_name}",
      "type": "{type}",
      "required": true,
      "default": null,
      "description": "{description}"
    }
  ],
  "state_pattern": "{pattern}",
  "composition": "{pattern}",
  "accessibility_level": "{level}",
  "styling": "{approach}",
  "files_created": [],
  "status": "in_progress"
}
```

## Component Generation

### 1. Create Directory Structure

Based on detected patterns or ask user:

```
Where should this component be created?

Detected component directories:
1. src/components/{ComponentName}/
2. app/components/{ComponentName}/
3. components/{ComponentName}/
4. Other (specify path)

Enter number or path:
```

Create structure:

```
{component_path}/
├── index.ts                 # Barrel export
├── {ComponentName}.tsx      # Main component
├── {ComponentName}.test.tsx # Tests (if testing detected)
├── {ComponentName}.styles.{ext}  # Styles (based on approach)
└── types.ts                 # TypeScript types (if TS project)
```

### 2. Generate Component Code

Generate component based on gathered specifications.

**For React/TypeScript example:**

```tsx
// {ComponentName}.tsx
import { forwardRef } from 'react';
import type { {ComponentName}Props } from './types';
import styles from './{ComponentName}.styles.module.css';

/**
 * {ComponentName}
 *
 * {Purpose description}
 */
export const {ComponentName} = forwardRef<HTML{Element}Element, {ComponentName}Props>(
  ({ prop1, prop2 = 'default', children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={styles.root}
        {...props}
      >
        {children}
      </div>
    );
  }
);

{ComponentName}.displayName = '{ComponentName}';
```

### 3. Generate Types

```tsx
// types.ts
import type { HTMLAttributes, ReactNode } from 'react';

export interface {ComponentName}Props extends HTMLAttributes<HTMLDivElement> {
  /** {prop1 description} */
  prop1: string;

  /** {prop2 description} */
  prop2?: 'primary' | 'secondary';

  /** Component children */
  children?: ReactNode;
}
```

### 4. Generate Styles

Based on styling approach:

**CSS Modules:**

```css
/* {ComponentName}.styles.module.css */
.root {
  /* Base styles */
}

.variant-primary {
  /* Primary variant */
}

.variant-secondary {
  /* Secondary variant */
}
```

**Tailwind:**

```tsx
// Inline in component
className={cn(
  'base-classes',
  variant === 'primary' && 'primary-classes',
  className
)}
```

### 5. Generate Tests (if testing framework detected)

```tsx
// {ComponentName}.test.tsx
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { {ComponentName} } from './{ComponentName}';

describe('{ComponentName}', () => {
  it('renders without crashing', () => {
    render(<{ComponentName} prop1="test" />);
    expect(screen.getByRole('...')).toBeInTheDocument();
  });

  it('applies variant styles correctly', () => {
    // Variant tests
  });

  it('handles user interaction', async () => {
    const user = userEvent.setup();
    // Interaction tests
  });

  it('meets accessibility requirements', () => {
    // A11y tests
  });
});
```

### 6. Generate Barrel Export

```tsx
// index.ts
export { {ComponentName} } from './{ComponentName}';
export type { {ComponentName}Props } from './types';
```

## User Review

After generating files:

```
I've created the {ComponentName} component:

Files created:
- {path}/index.ts
- {path}/{ComponentName}.tsx
- {path}/{ComponentName}.test.tsx
- {path}/{ComponentName}.styles.module.css
- {path}/types.ts

Would you like to:
1. Review the generated code
2. Make modifications
3. Add more props or features
4. Generate Storybook stories
5. Done, keep as-is

Enter number:
```

### If modifications requested:

```
What would you like to modify?

1. Add a new prop
2. Change styling approach
3. Add a variant
4. Modify component structure
5. Add accessibility features
6. Other (describe)

Enter number:
```

## Storybook Integration (Optional)

If Storybook detected or user requests:

```tsx
// {ComponentName}.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { {ComponentName} } from './{ComponentName}';

const meta: Meta<typeof {ComponentName}> = {
  title: 'Components/{ComponentName}',
  component: {ComponentName},
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary'],
    },
  },
};

export default meta;
type Story = StoryObj<typeof {ComponentName}>;

export const Default: Story = {
  args: {
    prop1: 'Example',
  },
};

export const Primary: Story = {
  args: {
    ...Default.args,
    variant: 'primary',
  },
};

export const Secondary: Story = {
  args: {
    ...Default.args,
    variant: 'secondary',
  },
};
```

## Completion

Update `.ui-design/components/{component_name}.json`:

```json
{
  "status": "complete",
  "files_created": [
    "{path}/index.ts",
    "{path}/{ComponentName}.tsx",
    "{path}/{ComponentName}.test.tsx",
    "{path}/{ComponentName}.styles.module.css",
    "{path}/types.ts"
  ],
  "completed_at": "ISO_TIMESTAMP"
}
```

Display summary:

```
Component Created Successfully!

Component: {ComponentName}
Location: {path}/
Files: {count} files created

Quick reference:
  Import: import { {ComponentName} } from '{import_path}';
  Usage:  <{ComponentName} prop1="value" />

Next steps:
1. Run /ui-design:design-review {path} to validate
2. Run /ui-design:accessibility-audit {path} for a11y check
3. Add to your page/layout

Need to create another component? Run /ui-design:create-component
```

## Error Handling

- If component name conflicts: Suggest alternatives, offer to overwrite
- If directory creation fails: Report error, suggest manual creation
- If framework not supported: Provide generic template, explain limitations
- If file write fails: Save to temp location, provide recovery instructions
