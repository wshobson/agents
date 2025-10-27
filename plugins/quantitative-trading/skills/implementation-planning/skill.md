---
name: implementation-planning
description: Estimate implementation timelines, identify dependencies, and create phased development plans for trading strategies. Use when planning strategy development.
---

# Implementation Planning

Estimate development timelines and create implementation roadmaps.

## When to Use
- Planning strategy development
- Estimating resource requirements
- Creating project timelines
- Identifying critical path dependencies

## Timeline by Complexity

- **LOW (1-2 weeks):** Daily/monthly rebalancing, standard data, simple calculations
- **MEDIUM (4-8 weeks):** Daily rebalancing, alternative data, basic ML
- **HIGH (8-16 weeks):** Intraday execution, advanced ML (embeddings), extensive custom development

## Implementation Phases

**Phase 1: Data Pipeline (20-30%)** - Acquisition, validation, storage
**Phase 2: Strategy Implementation (30-40%)** - Core logic, signals, portfolio construction
**Phase 3: Backtesting (20-25%)** - Historical simulation, costs, metrics
**Phase 4: Testing & Deployment (15-25%)** - OOS validation, paper trading, live deployment

## Key Takeaways
- Data pipeline takes 25% of time
- Testing is not optional (20-25% minimum)
- Complex strategies take 3+ months
- Identify blockers early
