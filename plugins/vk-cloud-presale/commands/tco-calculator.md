---
name: tco-calculator
description: Calculate detailed TCO comparison between VK Cloud and current infrastructure (AWS/Azure/on-premises)
---

# TCO Calculator

Рассчитайте comprehensive 3-year Total Cost of Ownership (TCO) для VK Cloud solution в сравнении с текущей инфраструктурой.

## Workflow

1. **Gather Current Costs**:
   - Current infrastructure costs (compute, storage, network, databases)
   - Personnel costs (ops team)
   - Support costs
   - Data center costs (if on-premises)

2. **Design VK Cloud Equivalent**:
   - Map current infrastructure → VK Cloud services
   - Right-size instances based на utilization

3. **Calculate VK Cloud Costs**:
   - Используйте `cloud-economics-specialist` agent
   - Monthly recurring costs (compute, storage, database, network)
   - One-time costs (migration, training)

4. **3-Year TCO Comparison**:
   - Year-by-year breakdown
   - Include:
     - Infrastructure costs
     - Personnel costs (managed services reduce ops burden)
     - Migration investment
     - Support costs
     - Hidden costs (egress fees critical!)

5. **ROI Calculation**:
   - Monthly savings
   - Payback period (months)
   - 3-year ROI percentage

6. **Cost Optimization Recommendations**:
   - Reserved instances (20-40% savings)
   - Auto-scaling (30-50% savings)
   - S3 lifecycle policies (60-80% storage savings)
   - Right-sizing

7. **Sensitivity Analysis**:
   - Best case scenario
   - Worst case scenario
   - Most likely scenario

## Agents Involved

- `cloud-economics-specialist` — рассчитывает TCO и ROI

## Deliverables

- Current state cost breakdown
- VK Cloud cost breakdown
- 3-year TCO comparison table
- ROI calculation with payback period
- Cost optimization recommendations
- Sensitivity analysis

Результаты сохраняются в `outputs/vk-cloud-presale/cloud-economics/`.

## Example Output

```markdown
# TCO Analysis: [Client Name]

## Executive Summary
- Current Cost: ₽1,800,000/mo
- VK Cloud Cost: ₽1,260,000/mo
- Monthly Savings: ₽540,000/mo (30%)
- 3-Year Savings: ₽19,440,000
- Migration Investment: ₽5,000,000
- Payback Period: 9.3 months
- 3-Year ROI: 288%

## Detailed Breakdown
[Tables with cost breakdown]

## Recommendations
[Cost optimization strategies]
```
