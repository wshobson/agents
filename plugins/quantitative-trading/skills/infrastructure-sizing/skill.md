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
- Capacity planning

## Infrastructure Tiers

### Tier 1: Laptop (FREE)

**Suitable for:**
- Daily EOD strategies
- Small universes (<500 stocks)
- Monthly/weekly rebalancing
- No ML or simple ML

**Specs:**
- 16GB RAM
- 512GB SSD
- Standard CPU

**Storage:** <100GB

### Tier 2: Server ($100-500/month)

**Suitable for:**
- Daily rebalancing, large universe
- Intraday bars (not ticks)
- ML models (not deep learning)
- Multiple strategies

**Cloud specs (AWS/GCP):**
- 32-64GB RAM
- 1-2TB SSD
- 8-16 vCPUs

**Storage:** 100GB-1TB

### Tier 3: Distributed/GPU ($1K-10K/month)

**Suitable for:**
- Real-time tick data
- Deep learning (embeddings)
- High-frequency strategies
- Large-scale backtesting

**Specs:**
- GPU for ML training
- Multi-node cluster
- Low-latency networking
- >1TB storage

## Storage Estimation

**Daily EOD data:**
- 1 stock × 20 years × OHLCV = ~20KB
- 3000 stocks × 20 years = ~60MB

**Intraday 1-minute bars:**
- 1 stock × 1 year × 390 bars/day = ~2MB
- 3000 stocks × 5 years = ~30GB

**Tick data:**
- 1 liquid stock × 1 day = ~1GB
- Prohibitively expensive for retail

## Key Takeaways

- **Most strategies work on laptop:** Don't over-invest early
- **Storage is cheap:** Compute is expensive
- **Start small, scale up:** Validate on laptop first
- **Cloud costs add up:** Budget $100-500/month for serious strategies
