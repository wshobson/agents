## VoiceOver (macOS)

### Setup

```
Enable: System Settings → Accessibility → VoiceOver
Toggle: Cmd + F5
Quick Toggle: Hold Command while quickly pressing Touch ID three times
```

Source: [Apple VoiceOver setup](https://support.apple.com/guide/voiceover/vo2682/mac).

### Essential Commands

```
Navigation:
VO = Ctrl + Option (VoiceOver modifier)

VO + Right Arrow   Next element
VO + Left Arrow    Previous element
VO + Shift + Down  Enter group
VO + Shift + Up    Exit group

Reading:
VO + A             Read all from cursor
Ctrl               Stop speaking
VO + B             Read current paragraph

Interaction:
VO + Space         Activate element
VO + Shift + M     Open menu
Tab                Next focusable element
Shift + Tab        Previous focusable element

Rotor (VO + U):
Navigate by: Headings, Links, Forms, Landmarks
Left/Right Arrow   Change rotor category
Up/Down Arrow      Navigate within category
Enter              Go to item

Web Specific:
VO + Cmd + H       Next heading
VO + Cmd + J       Next form control
VO + Cmd + L       Next link
VO + Cmd + T       Next table
```

### Testing Checklist

```markdown
## VoiceOver Testing Checklist

### Page Load

- [ ] Page title announced
- [ ] Main landmark found
- [ ] Skip link works

### Navigation

- [ ] All headings discoverable via rotor
- [ ] Heading levels logical (H1 → H2 → H3)
- [ ] Landmarks properly labeled
- [ ] Skip links functional

### Links & Buttons

- [ ] Link purpose clear
- [ ] Button actions described
- [ ] New window/tab announced

### Forms

- [ ] All labels read with inputs
- [ ] Required fields announced
- [ ] Error messages read
- [ ] Instructions available
- [ ] Focus moves to errors

### Dynamic Content

- [ ] Alerts announced immediately
- [ ] Loading states communicated
- [ ] Content updates announced
- [ ] Modals trap focus correctly

### Tables

- [ ] Headers associated with cells
- [ ] Table navigation works
- [ ] Complex tables have captions
```

### Common Issues & Fixes

```html
<!-- Issue: Button not announcing purpose -->
<button><svg>...</svg></button>

<!-- Fix -->
<button aria-label="Close dialog"><svg aria-hidden="true">...</svg></button>

<!-- Issue: Dynamic content not announced -->
<div id="results">New results loaded</div>

<!-- Fix -->
<div id="results" role="status" aria-live="polite">New results loaded</div>

<!-- Issue: Form error not read -->
<input type="email" />
<span class="error">Invalid email</span>

<!-- Fix -->
<input type="email" aria-invalid="true" aria-describedby="email-error" />
<span id="email-error" role="alert">Invalid email</span>
```
