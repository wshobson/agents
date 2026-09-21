---
name: screen-reader-testing
description: Test web applications with screen readers including VoiceOver, NVDA, and JAWS. Use when validating screen reader compatibility, debugging accessibility issues, or ensuring assistive technology support.
---

# Screen Reader Testing

Practical guide to testing web applications with screen readers for comprehensive accessibility validation.

## When to Use This Skill

- Validating screen reader compatibility
- Testing ARIA implementations
- Debugging assistive technology issues
- Verifying form accessibility
- Testing dynamic content announcements
- Ensuring navigation accessibility

## Core Concepts

### 1. Major Screen Readers

| Screen Reader | Platform  | Browser        | Usage |
| ------------- | --------- | -------------- | ----- |
| **VoiceOver** | macOS/iOS | Safari         | ~15%  |
| **NVDA**      | Windows   | Firefox/Chrome | ~31%  |
| **JAWS**      | Windows   | Chrome/IE      | ~40%  |
| **TalkBack**  | Android   | Chrome         | ~10%  |
| **Narrator**  | Windows   | Edge           | ~4%   |

### 2. Testing Priority

```
Minimum Coverage:
1. NVDA + Firefox (Windows)
2. VoiceOver + Safari (macOS)
3. VoiceOver + Safari (iOS)

Comprehensive Coverage:
+ JAWS + Chrome (Windows)
+ TalkBack + Chrome (Android)
+ Narrator + Edge (Windows)
```

### 3. Screen Reader Modes

| Mode               | Purpose                | When Used         |
| ------------------ | ---------------------- | ----------------- |
| **Browse/Virtual** | Read content           | Default reading   |
| **Focus/Forms**    | Interact with controls | Filling forms     |
| **Application**    | Custom widgets         | ARIA applications |

Before testing on macOS, read [VoiceOver setup, commands, and checklists](references/voiceover.md).

For the required iOS Safari coverage, read [VoiceOver touch setup and gestures](references/voiceover-ios.md).

Before testing with NVDA, read [NVDA setup, modes, commands, and test scripts](references/nvda.md).

Before testing with JAWS or TalkBack, read [platform setup and commands](references/jaws-talkback.md).

## Common Test Scenarios

### 1. Modal Dialog

```html
<!-- Accessible modal structure -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">This action cannot be undone.</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>
```

```javascript
// Focus management
function openModal(modal) {
  // Store last focused element
  lastFocus = document.activeElement;

  // Move focus to modal
  modal.querySelector("h2").focus();

  // Trap focus
  modal.addEventListener("keydown", trapFocus);
}

function closeModal(modal) {
  // Return focus
  lastFocus.focus();
}

function trapFocus(e) {
  if (e.key === "Tab") {
    const focusable = modal.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
    );
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      last.focus();
      e.preventDefault();
    } else if (!e.shiftKey && document.activeElement === last) {
      first.focus();
      e.preventDefault();
    }
  }

  if (e.key === "Escape") {
    closeModal(modal);
  }
}
```

### 2. Live Regions

```html
<!-- Status messages (polite) -->
<div role="status" aria-live="polite" aria-atomic="true">
  <!-- Content updates will be announced after current speech -->
</div>

<!-- Alerts (assertive) -->
<div role="alert" aria-live="assertive">
  <!-- Content updates interrupt current speech -->
</div>

<!-- Progress updates -->
<div
  role="progressbar"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Upload progress"
></div>

<!-- Log (additions only) -->
<div role="log" aria-live="polite" aria-relevant="additions">
  <!-- New messages announced, removals not -->
</div>
```

### 3. Tab Interface

```html
<div role="tablist" aria-label="Product information">
  <button role="tab" id="tab-1" aria-selected="true" aria-controls="panel-1">
    Description
  </button>
  <button
    role="tab"
    id="tab-2"
    aria-selected="false"
    aria-controls="panel-2"
    tabindex="-1"
  >
    Reviews
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Product description content...
</div>

<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Reviews content...
</div>
```

```javascript
// Tab keyboard navigation
tablist.addEventListener("keydown", (e) => {
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  const index = tabs.indexOf(document.activeElement);

  let newIndex;
  switch (e.key) {
    case "ArrowRight":
      newIndex = (index + 1) % tabs.length;
      break;
    case "ArrowLeft":
      newIndex = (index - 1 + tabs.length) % tabs.length;
      break;
    case "Home":
      newIndex = 0;
      break;
    case "End":
      newIndex = tabs.length - 1;
      break;
    default:
      return;
  }

  tabs[newIndex].focus();
  activateTab(tabs[newIndex]);
  e.preventDefault();
});
```

## Debugging Tips

```javascript
// Log what screen reader sees
function logAccessibleName(element) {
  const computed = window.getComputedStyle(element);
  console.log({
    role: element.getAttribute("role") || element.tagName,
    name:
      element.getAttribute("aria-label") ||
      element.getAttribute("aria-labelledby") ||
      element.textContent,
    state: {
      expanded: element.getAttribute("aria-expanded"),
      selected: element.getAttribute("aria-selected"),
      checked: element.getAttribute("aria-checked"),
      disabled: element.disabled,
    },
    visible: computed.display !== "none" && computed.visibility !== "hidden",
  });
}
```

## Best Practices

### Do's

- **Test with actual screen readers** - Not just simulators
- **Use semantic HTML first** - ARIA is supplemental
- **Test in browse and focus modes** - Different experiences
- **Verify focus management** - Especially for SPAs
- **Test keyboard only first** - Foundation for SR testing

### Don'ts

- **Don't assume one SR is enough** - Test multiple
- **Don't ignore mobile** - Growing user base
- **Don't test only happy path** - Test error states
- **Don't skip dynamic content** - Most common issues
- **Don't rely on visual testing** - Different experience
