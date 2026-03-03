---
name: find
description: >-
  Quick gallery search. Use when user runs /meigen:find with keywords
  to browse inspiration.
argument-hint: <keywords>
---

# Quick Find

Search the curated gallery for inspiration. Show visual results immediately.

## Instructions

1. Call `search_gallery` with query: `$ARGUMENTS`
   - If no arguments provided, call with no query to get trending picks
   - Use limit: 6 for a good visual spread
2. Display results as a compact list:
   - Number, preview image (markdown), one-line prompt excerpt, category
3. End with: "Say a number to see the full prompt, or describe what you want to generate."

If the user picks a number, call `get_inspiration` with that entry's ID to show the full prompt and images.

Keep output visual and scannable. No long explanations.
