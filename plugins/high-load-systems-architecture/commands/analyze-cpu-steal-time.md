---
name: analyze-cpu-steal-time
description: Diagnose CPU steal time issues, identify root causes, and generate comprehensive optimization recommendations with actionable remediation steps. Analyzes VM performance, hypervisor configuration, and provides cloud-specific solutions. Saves detailed report to markdown file.
---

# Analyze CPU Steal Time

This command performs comprehensive CPU steal time diagnosis and generates an expert optimization report.

## What This Command Does

1. **Gathers System Information**
   - Collects CPU steal time metrics from guest OS
   - Analyzes vCPU configuration and pinning
   - Examines hypervisor settings and resource allocation
   - Identifies noisy neighbor patterns

2. **Root Cause Analysis**
   - Detects CPU overcommitment ratios
   - Identifies SMT (Hyper-Threading) contention
   - Analyzes NUMA topology misalignment
   - Evaluates scheduler configuration

3. **Generates Optimization Recommendations**
   - Prioritized list of mitigation strategies
   - Step-by-step implementation guides
   - Cloud platform-specific solutions
   - Performance tuning scripts

4. **Creates Comprehensive Report**
   - Executive summary with key findings
   - Detailed diagnostic results
   - Prioritized action items
   - Configuration examples and scripts
   - Saves to `cpu-steal-time-analysis-YYYY-MM-DD-HHMMSS.md`

## Usage

Simply invoke this command and provide:
- Target system hostname or VM name
- Access credentials if needed
- Cloud platform (AWS/GCP/Azure/KVM/other)

## Example Interaction

**You:** Analyze CPU steal time for production-web-01

**Assistant:** I'll perform a comprehensive CPU steal time analysis for production-web-01.

*[Collects metrics, analyzes configuration, identifies issues]*

**Report Generated:** `cpu-steal-time-analysis-2025-11-18-143022.md`

**Key Findings:**
- CPU Steal: 15.3% (Critical)
- Root Cause: 2:1 CPU overcommitment + noisy neighbor
- Priority: HIGH - Immediate action required

**Recommendations:**
1. Enable CPU pinning (Est. improvement: 70%)
2. Migrate to dedicated instance (Est. improvement: 95%)
3. Isolate CPUs on host (Est. improvement: 85%)

## Report Contents

The generated markdown report includes:

```markdown
# CPU Steal Time Analysis Report
*Generated: [timestamp]*
*System: [hostname]*
*Platform: [cloud/hypervisor]*

## Executive Summary
- Current steal time: X%
- Severity: [Critical/Warning/Normal]
- Primary root cause: [identified cause]
- Estimated performance impact: X%

## Diagnostic Results

### CPU Metrics
- Average steal time: X%
- Peak steal time: X%
- Affected vCPUs: [list]
- Temporal pattern: [description]

### Configuration Analysis
- vCPU allocation: [details]
- CPU pinning: [status]
- NUMA configuration: [details]
- Scheduler settings: [details]

### Root Cause Assessment
1. **Primary Cause:** [description]
   - Evidence: [data points]
   - Impact: [quantification]

2. **Contributing Factors:** [list]

### Noisy Neighbor Analysis
- Detected: [yes/no]
- Evidence: [details]
- Impact assessment: [analysis]

## Recommendations

### Priority 1: Immediate Actions
1. **[Action Name]**
   - Estimated improvement: X%
   - Implementation time: [estimate]
   - Risk level: [low/medium/high]
   - Steps: [detailed instructions]

### Priority 2: Short-term Optimizations
[...]

### Priority 3: Long-term Solutions
[...]

## Implementation Guides

### Quick Win: Enable CPU Pinning
\`\`\`bash
# [Script with comments]
\`\`\`

### Cloud Platform Solutions

#### AWS
- Recommended instance types: [list]
- Migration steps: [guide]

#### GCP
[...]

## Monitoring Setup

### Continuous Monitoring
\`\`\`bash
# Monitoring script
\`\`\`

### Alert Configuration
[...]

## Appendix

### Collected Metrics
[Raw data tables]

### Configuration Files
[Relevant configs]
```

## When to Use This Command

- Experiencing application latency spikes in VMs
- CPU steal time consistently above 5%
- Planning VM placement strategy
- Troubleshooting performance degradation
- Before/after migration analysis
- Capacity planning for critical workloads

## Skills Used

This command leverages the **cpu-steal-time-optimization** skill to provide world-class expertise in:
- CPU steal time diagnosis
- Hypervisor performance analysis
- Cloud platform optimization
- Real-time performance monitoring
- Production troubleshooting workflows

## Output Location

Reports are saved to: `./reports/cpu-steal-time-analysis-YYYY-MM-DD-HHMMSS.md`

If the `reports` directory doesn't exist, it will be created automatically.
