## NVDA (Windows)

### Setup

```
Download: nvaccess.org
Start: Ctrl + Alt + N
Stop: Insert + Q
```

### Essential Commands

```
Navigation:
Insert = NVDA modifier

Down Arrow         Next line
Up Arrow           Previous line
Tab                Next focusable
Shift + Tab        Previous focusable

Reading:
NVDA + Down Arrow  Say all
Ctrl               Stop speech
NVDA + Up Arrow    Current line

Headings:
H                  Next heading
Shift + H          Previous heading
1-6                Heading level 1-6

Forms:
F                  Next form field
B                  Next button
E                  Next edit field
X                  Next checkbox
C                  Next combo box

Links:
K                  Next link
U                  Next unvisited link
V                  Next visited link

Landmarks:
D                  Next landmark
Shift + D          Previous landmark

Tables:
T                  Next table
Ctrl + Alt + Arrows Navigate cells

Elements List (NVDA + F7):
Shows all links, headings, form fields, landmarks
```

### Browse vs Focus Mode

```
NVDA automatically switches modes:
- Browse Mode: Arrow keys navigate content
- Focus Mode: Arrow keys control interactive elements

Manual switch: NVDA + Space

Watch for:
- "Browse mode" announcement when navigating
- "Focus mode" when entering form fields
- Application role forces forms mode
```

### Testing Script

```markdown
## NVDA Test Script

### Initial Load

1. Navigate to page
2. Let page finish loading
3. Press Insert + Down to read all
4. Note: Page title, main content identified?

### Landmark Navigation

1. Press D repeatedly
2. Check: All main areas reachable?
3. Check: Landmarks properly labeled?

### Heading Navigation

1. Press Insert + F7 → Headings
2. Check: Logical heading structure?
3. Press H to navigate headings
4. Check: All sections discoverable?

### Form Testing

1. Press F to find first form field
2. Check: Label read?
3. Fill in invalid data
4. Submit form
5. Check: Errors announced?
6. Check: Focus moved to error?

### Interactive Elements

1. Tab through all interactive elements
2. Check: Each announces role and state
3. Activate buttons with Enter/Space
4. Check: Result announced?

### Dynamic Content

1. Trigger content update
2. Check: Change announced?
3. Open modal
4. Check: Focus trapped?
5. Close modal
6. Check: Focus returns?
```
