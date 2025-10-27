---
name: infrastructure-sizing
description: Size compute, storage, and networking infrastructure for trading strategies based on data volume and computational requirements. Use when planning infrastructure needs.
---

# Infrastructure Sizing

Determine hardware and cloud infrastructure requirements.

## When to Use
- Planning infrastructure investments
- Estimating cloud costs
- Determining if laptop/server/cluster needed

## Infrastructure Tiers

### Tier 1: Laptop (FREE)
- Daily EOD strategies, small universes (<500 stocks), monthly/weekly rebalancing
- Storage: <100GB

### Tier 2: Server ($100-500/month)
- Daily rebalancing large universe, intraday bars, ML models
- Cloud: 32-64GB RAM, 1-2TB SSD, 8-16 vCPUs
- Storage: 100GB-1TB

### Tier 3: Distributed/GPU ($1K-10K/month)
- Real-time tick data, deep learning, high-frequency
- GPU for ML training, multi-node cluster
- Storage: >1TB

## Storage Estimates
- **Daily EOD:** 3000 stocks × 20 years = ~60MB
- **Intraday 1-min:** 3000 stocks × 5 years = ~30GB
- **Tick data:** 1 liquid stock × 1 day = ~1GB (prohibitive for retail)

## Key Takeaways
- Most strategies work on laptop
- Start small, scale up
- Storage is cheap, compute is expensive
- Budget $100-500/month for serious strategies
