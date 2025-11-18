---
name: discovery-session
description: Conduct comprehensive technical discovery session for VK Cloud pre-sale opportunities
---

# Discovery Session

Проведите глубокую техническую discovery сессию для понимания текущей инфраструктуры клиента, требований и разработки VK Cloud решения.

## Workflow

1. **Подготовка**:
   - Исследуйте бизнес клиента (индустрия, конкуренты, новости)
   - Подготовьте вопросы discovery
   - Принесите референсные архитектуры для их индустрии

2. **Business Context** (30 минут):
   - Используйте `technical-discovery-specialist` agent для сбора бизнес требований
   - Вопросы: Strategic goals, current challenges, timeline, budget

3. **Current State Assessment** (60-90 минут):
   - Inventory текущей инфраструктуры (compute, storage, database, network)
   - Architecture walkthrough с диаграммами
   - Dependency mapping

4. **Requirements Gathering** (60 минут):
   - Functional и non-functional requirements
   - Performance, scalability, availability, security

5. **Gap Analysis**:
   - Используйте `presale-solution-architect` для mapping current → VK Cloud
   - Identify gaps и workarounds

6. **Documentation**:
   - Все результаты сохраняются в markdown
   - Architecture diagrams (Mermaid)
   - Requirement matrix

7. **Next Steps**:
   - Schedule solution design session
   - Define POC scope (if needed)
   - Set timeline for proposal delivery

## Agents Involved

- `technical-discovery-specialist` — проводит discovery
- `presale-solution-architect` — анализирует requirements и gap analysis
- `cloud-economics-specialist` — собирает текущие cost metrics

## Deliverables

- Discovery notes (markdown)
- Current state architecture diagram
- Requirements matrix
- Gap analysis
- Next steps and timeline

Результаты автоматически сохраняются в `outputs/vk-cloud-presale/technical-discovery/`.
