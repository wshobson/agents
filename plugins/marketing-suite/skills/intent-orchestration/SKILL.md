---
name: intent-orchestration
description: Использование intent data и behavioral signals для orchestration персонализированных ABM campaigns в real-time. Use when building intent-driven workflows, prioritizing accounts, or coordinating sales-marketing touches.
---

# Intent-Based Orchestration

## Когда использовать

- Prioritizing accounts на основе buying signals
- Triggering automated workflows от intent spikes
- Coordinating sales-marketing touches in real-time
- Personalizing campaigns на основе research behavior
- Identifying "strike zone" opportunities (high intent + high fit)

## Ключевые концепции

### Intent Signal Types

**First-Party Intent (Your Properties):**
```
Website:
- Pricing page visits (high intent)
- Documentation deep-dives (technical evaluation)
- Case study consumption (validation stage)
- Multiple stakeholders visiting (buying committee active)

Product:
- Free trial signup (very high intent)
- Feature usage patterns (identifying needs)
- Integration exploration (tech stack fit)

Content:
- Whitepaper downloads (research mode)
- Webinar attendance (education phase)
- Email engagement (interest signals)
```

**Third-Party Intent (External):**
```
Topic Research (Bombora, 6sense):
- Intent surge on competitor keywords
- Category research (problem awareness)
- Solution comparison (evaluation phase)

Review Sites:
- G2/TrustRadius research
- Comparing vendors
- Reading reviews

Technographic:
- New tools added to stack
- Job postings (hiring for roles)
- Technology migrations
```

### Intent Scoring

**Composite Score:**
```
Intent Score = (First-Party × 0.4) + (Third-Party × 0.3) + (Engagement × 0.3)

Thresholds:
- 80-100: 🔥 Strike Zone (immediate action)
- 60-79:  🟡 Warm (accelerated nurture)
- 40-59:  ⚪ Cool (standard nurture)
- 0-39:   ❄️  Cold (awareness campaigns)
```

### Strike Zone Playbooks

**High Intent + High Fit = Immediate Action:**

```
Hour 0: Intent spike detected
Hour 1: SDR alerted, begins research
Hour 4: Personalized email from AE
Hour 24: LinkedIn connection request
Day 2: Direct mail sent
Day 3: Phone call attempt
Day 5: Executive outreach if no response
```

## Orchestration Platforms

**Tech Stack:**
- **6sense**: AI-powered intent + orchestration
- **Demandbase**: ABM platform with intent
- **Bombora**: Company-level intent data
- **Salesforce**: CRM automation
- **Outreach/Salesloft**: Sales engagement

**Integration:**
```
Intent Platform → CRM → Sales Engagement → Marketing Automation
     ↓              ↓            ↓                  ↓
  Scoring      Assignment   Sequences          Campaigns
```

## Best Practices

**Real-Time Response**:
- Alerts to sales within 15 minutes
- Same-day outreach on hot signals
- Coordinated multi-channel touches

**Personalization**:
- Reference specific research topics
- Tailor content to stage
- Multi-stakeholder coordination

**Measurement**:
- Intent-to-opportunity conversion
- Time to engagement
- Win rate by intent score

## Дополнительные ресурсы

См. `references/` и `assets/` для playbooks и automation templates.
