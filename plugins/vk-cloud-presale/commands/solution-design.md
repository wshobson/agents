---
name: solution-design
description: Design comprehensive VK Cloud solution architecture based on discovery and requirements
---

# Solution Design

Разработайте detailed VK Cloud архитектурное решение на основе discovery и customer requirements.

## Workflow

1. **Review Discovery**:
   - Загрузите discovery notes и requirements
   - Clarify unknowns с клиентом

2. **Architecture Design**:
   - Используйте `presale-solution-architect` для проектирования решения
   - Reference `vk-cloud-products` skill для mapping сервисов
   - Reference `reference-architectures` skill для proven patterns

3. **VK Cloud Service Mapping**:
   - Compute: VMs, Kubernetes, Bare Metal
   - Storage: Block Storage, S3
   - Database: PostgreSQL, ClickHouse, MongoDB, Redis
   - Network: VPC, Load Balancers, VPN
   - Platform: Kafka, GitLab

4. **Create Architecture Diagrams**:
   - Logical architecture
   - Physical architecture
   - Network topology
   - Data flow diagram
   - Use Mermaid format

5. **Sizing & Costing**:
   - Используйте `cloud-economics-specialist` для TCO analysis
   - Calculate monthly и 3-year costs
   - Compare с current costs

6. **Migration Strategy**:
   - Define migration approach (lift-and-shift, replatform, refactor)
   - Phased migration roadmap
   - Data migration plan

7. **Risk Assessment**:
   - Technical risks и mitigation
   - Migration risks
   - Security risks

## Agents Involved

- `presale-solution-architect` — проектирует архитектуру
- `cloud-economics-specialist` — рассчитывает TCO и sizing
- `competitive-strategist` — позиционирование vs конкуренты

## Deliverables

- Architecture diagrams (logical, physical, network)
- Technical specification
- VK Cloud service mapping
- Migration strategy
- TCO analysis
- Risk mitigation plan

Результаты сохраняются в `outputs/vk-cloud-presale/presale-solution-architect/`.
