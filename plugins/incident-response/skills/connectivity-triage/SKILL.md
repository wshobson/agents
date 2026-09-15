---
name: connectivity-triage
description: Use this skill when debugging active macOS connectivity failures, when an API or MCP service times out or disconnects, when DNS resolution is failing or inconsistent, or when video calls or other interactive traffic show packet loss or latency. Isolate local-LAN, DNS, upstream-path, and remote-service/application fault domains with built-in, non-destructive tools.
---

# Connectivity Triage

Localize an active connectivity failure without changing network configuration. Collect the smallest useful evidence set, distinguish observations from inference, and stop when the fault domain is clear enough for the next safe action.

## When to Use This Skill

Use this workflow when a macOS endpoint has an active symptom such as:

- an API, website, or MCP service timing out or disconnecting;
- DNS lookup failures or inconsistent name resolution;
- packet loss, latency, or unstable interactive traffic;
- an application that appears offline while other traffic works;
- uncertainty about whether the problem is local, upstream, or at the service.

This is a diagnostic workflow, not a remediation workflow. Do not change interface state, DNS settings, VPN/firewall configuration, or remote service state while establishing the fault domain.

## Fast Decision Flow

Work from the symptom toward the narrowest discriminating check:

```text
symptom
  -> local link / LAN evidence
  -> DNS configuration and resolution
  -> destination reachability
  -> path quality
  -> application / service timing
  -> fault-domain assessment
```

Stop early when the evidence is already sufficient. Do not run every probe mechanically.

### 1. Define the symptom

Record the affected application or process, destination hostname or URL, when the failure started, whether it is continuous or intermittent, and whether unrelated destinations still work.

If the symptom is application-specific, preserve the exact hostname or URL the application uses. Testing an unrelated public site can establish general connectivity but cannot prove the affected service is healthy.

### 2. Check local-link / LAN evidence

When available, run a bounded `networkQuality` sample for a broad responsiveness and throughput signal. If `networkQuality` is unavailable, continue; it is optional.

If a known local gateway or same-LAN target is available, compare a short bounded `ping` sample to that local target with a short sample to the remote destination. Do not invent a gateway address. If no local target is known, leave the LAN segment unproven and continue.

Useful pattern:

```bash
ping -c 5 <known-local-target>
ping -c 5 <destination>
```

### 3. Separate DNS configuration from DNS behavior

Inspect the system resolver state, especially when VPNs, split DNS, or scoped resolvers may be involved:

```bash
scutil --dns
```

Then test the destination name directly with a bounded DNS query:

```bash
dig +time=2 +tries=1 <hostname>
```

Treat these as different evidence. `scutil --dns` shows resolver configuration; `dig` shows query behavior. A successful lookup does not prove the returned endpoint is reachable.

### 4. Test reachability and path quality

Use a short `ping` sample when ICMP is a useful signal:

```bash
ping -c 5 <destination>
```

If the destination is unresolved, test the resolved address separately only when doing so helps distinguish DNS from path failure.

Use a bounded numeric traceroute when path visibility would reduce uncertainty:

```bash
traceroute -n -q 1 -m 20 <destination>
```

A silent or changing hop is an observation, not proof that the hop is broken. Routers may filter or rate-limit traceroute traffic while forwarding application traffic normally.

### 5. Inspect the affected application's live network activity

When the problem is process-specific, use a bounded `nettop` capture rather than watching indefinitely:

```bash
nettop -n -L 3 -p <process-name-or-pid>
```

Use it to confirm whether the process is opening connections, which endpoints it is using, and whether traffic is flowing. Lack of visible activity may mean the application never attempted the connection; it does not by itself identify why.

### 6. Time the application path

For HTTP(S), use curl phase timing against the actual affected endpoint when a safe read-only request is available:

```bash
curl -sS -o /dev/null \
  -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n' \
  --connect-timeout 5 --max-time 15 https://<host>/<safe-path>
```

Interpret the phases comparatively. High time-to-first-byte can include server processing, so it is not proof of network latency.

## Evidence Rules

Label conclusions as one of:

- **Observed** — directly supported by command output or user-provided evidence.
- **Inferred** — the most likely explanation after correlating observations.
- **Unknown** — not established by the current evidence.

Never treat one probe as proof of root cause. In particular:

- failed `ping` can reflect ICMP filtering rather than an outage;
- successful `ping` does not prove an application is healthy;
- non-responsive traceroute hops do not prove packet loss at those routers;
- successful DNS resolution does not prove reachability;
- high HTTP first-byte time can be dominated by remote application processing.

When observations conflict, prefer `inconclusive` over a confident guess.

## Fault-Domain Assessment

Return exactly one primary category:

- `local-link/LAN` — evidence degrades before or at the local network boundary;
- `DNS` — resolver configuration or lookup behavior explains the failure better than path evidence;
- `upstream-path` — local evidence is healthy and correlated path evidence degrades beyond the LAN;
- `remote-service/application` — transport/path evidence is healthy enough while the affected service or process behavior remains abnormal;
- `inconclusive` — current evidence cannot separate the remaining fault domains.

Use qualitative confidence: `low`, `medium`, or `high`. Confidence reflects evidence quality and correlation, not severity.

## Incident Result Format

### Symptom
Restate the active failure and affected destination/application.

### Observations
List only relevant measurements, including important unavailable or blocked evidence. Mark observations, inferences, and unknowns clearly.

### Fault-domain assessment
Report the category, confidence, and a short evidence-linked explanation.

### Next safest check
Give one diagnostic action that most reduces uncertainty. Do not jump to configuration changes unless the user separately asks for remediation.

## Safety and Boundaries

During diagnosis, do not:

- alter interface state or restart network services;
- edit resolver configuration or flush DNS caches;
- modify firewall or VPN settings;
- install packages or require Homebrew;
- send state-changing requests to remote services;
- run indefinite or high-volume probes when a bounded sample will answer the question.

Partial probes, blocked ICMP, VPNs, captive portals, scoped DNS, proxies, endpoint controls, and transient failures are evidence limitations rather than diagnoses.

## Detailed Interpretation

Read `references/details.md` for command-by-command interpretation, ambiguity handling, intermittent-failure guidance, and worked examples.

## Related Skills

- `incident-runbook-templates` - Turn recurring connectivity incidents into repeatable response procedures
- `on-call-handoff-patterns` - Preserve active connectivity evidence across responder handoffs
- `postmortem-writing` - Document confirmed causes and corrective actions after the incident
