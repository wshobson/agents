# Brand Landing Page

A Claude Code skill that runs a structured brand discovery interview, generates iterative landing pages via Stitch, and delivers a deployment-ready HTML bundle.

Turn brand decisions you haven't made yet into a landing page you'd actually ship.

## When To Use

You have a product, side project, or service that needs a landing page. You can build the product but haven't established a brand direction — color palette, font pairing, visual hierarchy, or page structure. This skill handles the design decisions you'd otherwise skip or guess at.

Just ask Claude to create a landing page for your project. The skill takes it from there.

## What It Does

- **Brand discovery interview** — 10 questions across 3 phases (Product & Purpose, Brand Feel, Visual Preferences) with follow-up triggers for vague or contradictory answers
- **Design system translation** — maps brand adjectives to Stitch parameters: color palette, font pairing, shape direction, color mode
- **Visual feedback loop** — generates landing pages, opens them in your browser, translates feedback ("it looks too corporate") into targeted Stitch operations
- **Iteration** — edit specific sections, explore variants across layout/color/typography, roll back to earlier versions
- **Image handling** — extracts style cues from logos or screenshots you provide, saves originals for developer handoff
- **Delivery bundle** — final HTML, design tokens (JSON), brand documentation, and deployment checklist as a zip

## Setup

Stitch's free tier (350 standard + 200 experimental generations/month) covers all skill functionality — no paid plan required.

The skill walks you through Stitch setup the first time you use it: it'll point you to the Stitch web app for an API key and handle the SDK installation.

Requires Node.js 18+.

## File Structure

```
brand-landingpage/
  .claude-plugin/
    plugin.json
  skills/
    brand-landingpage/
      SKILL.md                         # Main skill instructions
      references/
        interview-framework.md         # Brand discovery question bank and feedback guide
        stitch-architecture.md         # Font/color/prompt/section reference
        state-and-pitfalls.md          # State schema, pitfalls, DEPLOY.md template
  README.md
```

## Limitations

- Stitch generates static HTML (no JS interactivity, no forms, no animations)
- No image upload via Stitch API — logos and images are saved in the bundle for manual integration
- You'll need to replace placeholder images, wire up the CTA link, and add analytics after deployment
