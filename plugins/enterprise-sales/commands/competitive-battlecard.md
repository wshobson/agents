---
name: competitive-battlecard
description: Generate competitive battlecard for VK Cloud vs. specific competitor with positioning, differentiation, landmine questions, and objection handling.
---

# Competitive Battlecard Generator

You will create a comprehensive competitive battlecard for VK Cloud against a specific competitor.

## Process

### 1. Identify Competitor

Ask the user which competitor to analyze:
- **Global Hyperscalers**: AWS, Microsoft Azure, Google Cloud (GCP)
- **Local Providers**: Yandex Cloud, Sbercloud, MTS Cloud
- **On-Premises**: VMware vSphere, OpenStack, Nutanix
- **Other**: Specific competitor

### 2. Gather Intelligence

**Competitor Profile**:
- Company background and market position
- Product portfolio and key offerings
- Pricing model and typical contract terms
- Target customer segments
- Strengths and weaknesses
- Recent news, funding, strategic moves

**Customer Context**:
- What specific products are they evaluating?
- What's driving their interest in this competitor?
- What have they heard about competitor (positive/negative)?
- What decision criteria matter most to them?

### 3. Generate Battlecard

Create a structured battlecard with the following sections:

#### Competitor Overview

**Who They Are**:
- Company description (1-2 sentences)
- Market position and size
- Primary customer segments
- Key products and services

**When They Win**:
- Scenarios where competitor is strong choice
- Customer profiles that fit their sweet spot
- Use cases where they excel
- Be honest and objective

**When We Win**:
- Scenarios where VK Cloud is superior choice
- Our advantages and differentiators
- Proof points and customer references

#### Head-to-Head Comparison

Create detailed comparison table:

| Category | VK Cloud | [Competitor] | Winner |
|----------|----------|-------------|--------|
| **Data Sovereignty** | ✅ Full 152-FZ compliance, Russian data residency | ❌ Limited or no Russian data centers | VK ✅ |
| **Pricing** | $X/month (example workload) | $Y/month (30% higher) | VK ✅ |
| **Support** | 24/7 Russian-language support | English-only or limited Russian | VK ✅ |
| **Kubernetes** | Free control plane, standard K8s | $0.10/hour control plane fee | VK ✅ |
| **S3 Storage** | $X/GB, S3-compatible API | $Y/GB (+25%) | VK ✅ |
| **Global Reach** | Russia-focused | 25+ regions worldwide | Competitor |
| **Service Breadth** | 20+ core services | 200+ services | Competitor |
| **Ecosystem** | Growing ISV/SI partners | Largest partner ecosystem | Competitor |
| **Sanctions Risk** | ✅ No risk | ⚠️ Potential service disruption | VK ✅ |

#### Positioning Strategy

**Primary Message**:
"VK Cloud delivers [key benefit] with [differentiator] while [addressing customer pain point], unlike [Competitor] which [weakness]."

**Example vs. AWS**:
"VK Cloud delivers enterprise-grade cloud infrastructure with full Russian data sovereignty and 30% cost savings, while eliminating sanctions risk—unlike AWS which faces ongoing regulatory uncertainty in Russia."

**Example vs. Yandex Cloud**:
"VK Cloud provides enterprise-ready Kubernetes platform with VK Group ecosystem integration and superior customer support, making it ideal for enterprises requiring mission-critical reliability."

#### Landmine Questions

Questions that expose competitor weaknesses (ask customer these):

**vs. AWS**:
- "How confident are you in AWS's long-term commitment to the Russian market given recent geopolitical tensions?"
- "Have you calculated data egress costs? AWS charges $X per GB to transfer data out."
- "What's your plan if AWS faces sanctions or service restrictions in Russia?"
- "How important is Russian-language support at 2AM Moscow time?"
- "Can your data legally reside outside Russia under 152-FZ regulations?"

**vs. Azure**:
- "Have you evaluated the complexity of Azure licensing and Enterprise Agreements?"
- "What's your multi-cloud strategy if you become fully dependent on Microsoft?"
- "How does Azure's SQL Server licensing compare to open-source PostgreSQL costs?"
- "Are you comfortable with complete Microsoft stack dependency?"

**vs. GCP**:
- "How critical is Google's long-term commitment to enterprise in Russia?"
- "Have you compared ClickHouse vs. BigQuery for analytics workloads?"
- "What's your data residency strategy with GCP's limited Russia presence?"

**vs. Yandex Cloud**:
- "Have you compared Kubernetes maturity and enterprise features?"
- "What level of customer support and SLA do you require?"
- "How important is VK Group ecosystem integration for your use cases?"

**vs. On-Premises**:
- "What's your hardware refresh cycle cost over 5 years?"
- "How quickly can you provision new environments today vs. what you need?"
- "What's your disaster recovery strategy and RTO/RPO?"
- "How many FTEs are dedicated to infrastructure management?"

#### Differentiation Points

**Our Unique Advantages**:
1. **Data Sovereignty**: 100% compliance with Russian data laws (152-FZ, 187-FZ, GOST)
2. **Cost**: 20-40% lower TCO for Russian customers
3. **No Sanctions Risk**: Domestic provider immune to geopolitical disruptions
4. **Local Support**: Russian-language, timezone-aligned, in-country escalation
5. **Open Standards**: Kubernetes, S3 API, PostgreSQL—no lock-in
6. **VK Ecosystem**: Integration with VK Group services and platforms

**Proof Points**:
- [Customer X] migrated from [Competitor] and saved $XXX,XXX annually
- [Customer Y] chose VK Cloud over [Competitor] for [reason]
- [Analyst report] validates VK Cloud's [capability]
- [Benchmark] shows VK Cloud [performance advantage]

#### Objection Handling

**"[Competitor] is the market leader"**:
- Response: "Market leadership doesn't equal best fit for Russian enterprises. VK Cloud is purpose-built for Russian regulatory requirements and offers 30% cost savings. Being #1 globally doesn't help if they can't meet your data sovereignty needs."

**"[Competitor] has more services"**:
- Response: "We focus on the 80% of services enterprises actually use—compute, storage, databases, Kubernetes. What specific capability do you need that we don't offer? Often, breadth creates complexity without value."

**"We're worried about a smaller provider"**:
- Response: "VK Group is one of Russia's largest tech companies with 20+ years operating internet-scale infrastructure. We have the scale and reliability of a hyperscaler, with the focus and support of a local partner."

**"Your pricing seems similar/high"**:
- Response: "Let's compare total cost of ownership, not just list price. When you include data egress, support quality, compliance costs, and risk mitigation, VK Cloud delivers 30-40% lower TCO."

**"We're already invested in [Competitor]"**:
- Response: "Many customers use multi-cloud strategies. VK Cloud's Kubernetes and S3 API compatibility means you can easily move workloads. What workloads are best suited for Russia-based infrastructure?"

#### FUD (Fear, Uncertainty, Doubt) Counter

**Common Attacks from Competitors**:

**Attack**: "VK Cloud is smaller and less proven"
- **Counter**: "VK Group operates Russia's largest social network and email platform—billions of requests daily. Our infrastructure is battle-tested at scale. Plus, we focus on enterprise support quality, not just scale."

**Attack**: "They don't have global reach"
- **Counter**: "For Russian workloads, local infrastructure is an advantage—lower latency, data sovereignty, no sanctions risk. If you need global reach, we support hybrid architectures with VK Cloud for Russia, other providers for global."

**Attack**: "Limited service portfolio"
- **Counter**: "We focus on core services enterprises actually need. Our roadmap is customer-driven. What specific service do you need that we don't offer? We're often more responsive to customer needs than hyperscalers."

#### Win Strategy

**Tactical Approach**:
1. **Discovery**: Understand customer priorities (cost, compliance, risk, performance)
2. **Positioning**: Lead with differentiation (sovereignty, cost, no sanctions risk)
3. **Proof**: Provide customer references, case studies, POC results
4. **Landmines**: Ask questions that expose competitor weaknesses
5. **Close**: Quantify total value (TCO, ROI, risk mitigation)

**Resources to Deploy**:
- Customer references (competitors displaced or evaluated against)
- Case studies with quantified results
- TCO/ROI calculator
- Executive sponsor for peer-to-peer engagement
- POC to prove capabilities

#### Pricing Comparison

Provide specific pricing examples:

**Example Workload**: 100 vCPUs, 400GB RAM, 10TB storage, 5TB egress

| Cost Component | VK Cloud | [Competitor] | Difference |
|----------------|----------|--------------|------------|
| Compute | $X,XXX/month | $X,XXX/month | -20% |
| Storage | $XXX/month | $XXX/month | -30% |
| Egress | $XXX/month | $X,XXX/month | -70% |
| Support | Included | $X,XXX/month | -$X,XXX |
| **Total Monthly** | **$X,XXX** | **$X,XXX** | **-30%** |
| **Annual TCO** | **$XX,XXX** | **$XX,XXX** | **-$X,XXX** |

### 4. Output Format

Provide battlecard as:
- **1-page Quick Reference**: Key points, pricing, landmine questions
- **Detailed Battlecard** (2-3 pages): Full comparison, objection handling, win strategy

Format for:
- Sales team training
- Deal-specific preparation
- Competitive response documents

## Example Interaction

**You**: "Which competitor would you like to create a battlecard for?"

**User**: "AWS. We're competing against them in a $1M deal with Sberbank."

**You**: "Perfect. Let me create a comprehensive AWS battlecard. A few questions:

1. What specific AWS services are they evaluating? (EC2, RDS, S3, EKS?)
2. What's driving Sberbank's interest in AWS?
3. What are their top priorities? (cost, features, compliance, risk)
4. Have they expressed any concerns about AWS?"

[Continue discovery...]

After gathering context, generate tailored battlecard for this specific deal.

## Tips

- **Be Honest**: Acknowledge where competitor is strong
- **Be Specific**: Use real pricing, real customer examples
- **Be Prepared**: Anticipate competitor attacks and prepare counters
- **Be Competitive**: Win with superior value, not just price
- **Update Regularly**: Competitors change pricing, features, strategy
- **Tailor to Customer**: Emphasize decision criteria that matter to them
- **Proof Points**: Evidence beats claims (references, case studies, benchmarks)
- **Train the Team**: Battlecard is only useful if sales team uses it

Activate the vk-cloud-competitive-positioning skill for detailed guidance.
