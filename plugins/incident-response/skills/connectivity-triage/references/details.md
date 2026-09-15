# connectivity-triage — detailed interpretation and examples

Use this reference when the fast path in `SKILL.md` does not provide enough context to interpret conflicting, partial, or intermittent evidence.

## Interpretation Principles

Connectivity triage is fault-domain isolation, not root-cause proof. A useful diagnosis narrows the failure to the smallest defensible segment while preserving uncertainty that the available probes cannot resolve.

Prefer correlated evidence across layers:

1. local or same-LAN behavior;
2. resolver configuration and lookup behavior;
3. destination reachability;
4. path visibility and loss/latency patterns;
5. application-specific connections and timings.

An observation becomes a stronger inference when an independent probe supports the same boundary. When independent probes disagree, report the disagreement and choose `inconclusive` until a discriminating check resolves it.

## Command Interpretation

### `networkQuality`

Use `networkQuality` as a broad endpoint-to-Internet responsiveness and throughput snapshot when it is available. It is useful for answering questions such as "is this Mac generally experiencing degraded network responsiveness right now?"

What it can support:

- general evidence that the endpoint has usable Internet connectivity;
- a contemporaneous responsiveness/throughput baseline;
- comparison between a visibly degraded period and a later healthy period.

What it cannot establish alone:

- whether a specific API or service is healthy;
- which hop or provider caused poor responsiveness;
- whether DNS for the affected hostname is correct;
- whether the local LAN or an upstream segment is specifically responsible.

If the command is unavailable, record that limitation and continue. Do not install anything just to obtain it.

### `ping`

Use short bounded samples. Five probes are usually sufficient for a first discriminator during active triage:

```bash
ping -c 5 <target>
```

A same-LAN target is especially useful when it is already known. Compare it with the affected destination rather than treating a remote ping in isolation.

Useful observations include:

- whether any replies return;
- measured round-trip times for replies;
- loss within the bounded sample;
- a material difference between local and remote targets.

Do not overinterpret:

- 100% loss can mean ICMP filtering;
- 0% loss across five probes does not exclude intermittent loss;
- a fast ping does not prove TCP, TLS, HTTP, or the application is healthy;
- latency to one destination is not a universal latency measurement.

A strong `local-link/LAN` inference needs evidence that the local segment itself is degraded, such as loss or extreme latency to a known same-LAN target while the endpoint is actively affected.

### `traceroute`

Use numeric output to avoid adding reverse-DNS noise and bound the probe count:

```bash
traceroute -n -q 1 -m 20 <destination>
```

Traceroute is best for locating where path visibility changes, not for declaring a router faulty.

Potentially useful patterns:

- repeated runs stop becoming visible at the same boundary during the incident;
- local hops remain stable while later path visibility changes;
- the destination is reached despite one or more silent intermediate hops.

Cautions:

- routers may deprioritize or suppress TTL-expired responses;
- different probes can follow different paths because of load balancing;
- asterisks do not prove that forwarding traffic is being dropped;
- the final destination may ignore traceroute probes while the application works normally.

Assign `upstream-path` only when traceroute observations agree with other evidence, such as remote-only loss or connection failure while local/DNS evidence remains healthy.

### `scutil --dns`

Use:

```bash
scutil --dns
```

This reports the current macOS DNS configuration, including scoped resolvers that can matter when VPNs, enterprise networking, or split DNS are present.

Look for:

- the resolver selected for the relevant domain;
- search domains;
- interface-scoped resolver entries;
- VPN-associated resolver state;
- obvious absence of an expected resolver.

The output is configuration evidence, not a successful resolution test. A resolver can be configured correctly but fail to answer, and an unexpected resolver can still return an apparently valid answer.

### `dig`

Use a bounded query:

```bash
dig +time=2 +tries=1 <hostname>
```

Useful observations include:

- timeout versus response;
- answer records returned;
- response code such as `NOERROR` or `NXDOMAIN`;
- whether repeated results are stable during the symptom.

Interpret `dig` together with `scutil --dns`. macOS may use scoped/system resolver behavior that a simple direct `dig` invocation does not fully reproduce for every application. A successful `dig` response therefore does not prove that the affected application used the same resolver path or received the same answer.

When split DNS is plausible, prefer `inconclusive` until the relevant resolver scope is understood.

### `nettop`

Use a bounded logging capture for the affected process:

```bash
nettop -n -L 3 -p <process-name-or-pid>
```

This is useful when general network checks succeed but one application is failing.

What it can show:

- whether the process has network activity at all;
- which remote endpoints appear in its active connections;
- whether traffic counters are moving during the symptom;
- whether the application is connecting somewhere different from the hostname or endpoint assumed during manual tests.

What it cannot prove alone:

- why a connection is absent;
- whether a remote endpoint is semantically healthy;
- whether an application-layer timeout is caused by the network or server processing.

If the process does not appear, confirm the process name or PID before inferring that it made no network attempt.

### `curl -w` timing

For an HTTP(S) endpoint, use a read-only request to the same host and safe path the incident concerns:

```bash
curl -sS -o /dev/null \
  -w 'dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n' \
  --connect-timeout 5 --max-time 15 https://<host>/<safe-path>
```

Interpret the cumulative timings carefully:

- `time_namelookup`: time until name resolution completed;
- `time_connect`: time until the transport connection completed;
- `time_appconnect`: time until TLS or equivalent application connection setup completed;
- `time_starttransfer`: time until the first response byte arrived, including server processing before that byte;
- `time_total`: total transfer duration.

The values are cumulative timestamps from the beginning of the transfer, not independent phase durations. Compare boundaries rather than reading each value as isolated latency.

Examples:

- large increase before `time_connect` with normal DNS can support transport/path suspicion;
- large increase between connect and TLS completion can support TLS/transport investigation but not identify the responsible network device;
- large increase after TLS completion and before first byte can be server/application processing, upstream dependency delay, or network delay in response delivery.

Use a safe read-only endpoint. Do not send POST, PUT, DELETE, or other state-changing requests merely to test connectivity.

## Ambiguity and Failure Conditions

### ICMP filtering or rate limiting

If `ping` fails but HTTP(S) or another affected transport succeeds, mark ICMP as unavailable evidence. Do not classify the destination as down.

If traceroute has silent hops but the final destination and application are reachable, treat the silent hops as non-diagnostic.

### VPNs and tunnel interfaces

A VPN can change routing, resolver scope, source address, and path behavior simultaneously. When symptoms occur only with the VPN active, distinguish "VPN-associated" from a proven VPN fault unless the evidence isolates the failure within the tunnel or resolver policy.

Do not disable the VPN during the diagnostic phase unless the user separately approves that comparison and doing so is operationally safe.

### Split-horizon or scoped DNS

A hostname may intentionally resolve differently on different interfaces or resolver scopes. Compare `scutil --dns` with observed `dig` results and the endpoint the affected application actually uses.

A public resolver returning a different address is not automatically evidence that the system resolver is wrong.

### Captive portals

Captive portals can allow some DNS or HTTP traffic while intercepting other requests. If the environment recently joined Wi-Fi and behavior is inconsistent across destinations, keep captive-portal interception as an inference until confirmed through safe user-facing checks.

Do not attempt to bypass or automate portal authentication.

### Proxies and enterprise endpoint controls

Proxies, content filters, endpoint security products, and managed network extensions can cause one application's path to differ from direct command-line probes. If curl succeeds while the application fails, inspect application-specific activity with `nettop` and report policy/interception as a possibility rather than assuming an application bug.

Do not disable enterprise controls as part of triage.

### Services that reject diagnostic requests

An endpoint can reject HEAD requests, unauthenticated requests, or requests to an arbitrary path while the production application path is healthy. Use a known safe read-only path when available and distinguish "HTTP response received" from "application operation succeeded."

### Transient failures

If all probes are healthy after the symptom disappears, do not retroactively label the incident healthy. Report that the failure was not reproduced and move to an intermittent-evidence strategy.

## Intermittent-Symptom Guidance

For intermittent incidents, keep each probe bounded and repeat it only across the user-reported failure window. The goal is correlation, not continuous monitoring.

Capture:

- exact timestamps of symptom onset/recovery when known;
- whether DNS answers change across good and bad periods;
- whether local and remote ping behavior diverges during bad periods;
- whether traceroute visibility changes at the same time as the application failure;
- whether the affected process opens connections during failure;
- whether curl timing changes in the same phase each time.

Avoid declaring packet loss or path instability from one isolated sample. A useful intermittent diagnosis needs repeated correlation between the symptom and at least one independent network observation.

If the incident cannot be reproduced, return `inconclusive` with the next safest check to run during the next occurrence rather than recommending invasive remediation.

## Worked Examples

### Example 1: API timeout

**Symptom:** A read-only API request times out from one Mac while unrelated websites load normally.

**Observed:**

- system DNS configuration contains the expected resolver;
- bounded `dig` returns the expected API address;
- local target ping is stable;
- remote destination ping is filtered, so ICMP is unknown;
- curl connects and completes TLS quickly but spends most of the total time before first byte.

**Assessment:** `remote-service/application`, medium confidence.

**Why:** DNS and connection setup complete normally, while delay accumulates after transport/TLS setup. First-byte delay can include server processing, so the evidence points beyond basic connectivity but does not prove the remote application's exact root cause.

**Next safest check:** Compare the same safe API request from another known-good client or inspect service-side request timing if available.

### Example 2: DNS failure

**Symptom:** An internal hostname fails to resolve after connecting to a corporate VPN.

**Observed:**

- `scutil --dns` does not show the expected scoped resolver for the internal domain;
- bounded `dig` for the hostname times out or returns no usable internal answer;
- already-known IP connectivity to the service network remains available.

**Assessment:** `DNS`, high confidence if the resolver scope is demonstrably absent; otherwise medium confidence.

**Why:** The failure is name-specific while path evidence to a known service address remains available, and resolver configuration does not match the expected internal namespace.

**Next safest check:** Verify the expected VPN resolver policy/configuration with the network owner; do not edit DNS settings manually during diagnosis.

### Example 3: MCP disconnect

**Symptom:** An MCP client repeatedly disconnects while general Internet access appears normal.

**Observed:**

- general `networkQuality` and unrelated destinations look healthy;
- DNS for the MCP hostname is stable;
- bounded curl timing to a safe HTTP(S) endpoint on the same service is normal;
- `nettop` shows the MCP client repeatedly opening and closing connections to the expected remote endpoint.

**Assessment:** `remote-service/application`, medium confidence.

**Why:** General endpoint connectivity, DNS, and basic service transport are healthy enough, while the affected process exhibits repeated connection churn. That narrows the problem toward the client/service/application layer but does not prove which side closes the session.

**Next safest check:** Correlate client and service logs for the disconnect timestamps and determine which side initiated closure.

### Example 4: Degraded interactive traffic

**Symptom:** A video call becomes choppy while ordinary web browsing still works.

**Observed:**

- local same-LAN ping remains low-latency with no loss in several bounded samples;
- remote bounded samples show elevated latency or loss during the choppy periods;
- `networkQuality` responsiveness also degrades during those periods;
- traceroute visibility changes beyond the local network but no single silent hop consistently proves failure.

**Assessment:** `upstream-path`, medium confidence.

**Why:** Multiple independent measurements degrade only beyond the LAN and correlate with the interactive symptom. Traceroute alone is not used as proof.

**Next safest check:** Compare the same bounded measurements from another device on the same LAN during the symptom to separate endpoint-specific behavior from the shared upstream path.

## Output Quality Checklist

Before returning an incident result, verify that it:

- names the actual symptom and affected destination/process;
- states measured evidence separately from inference;
- uses exactly one primary fault-domain category;
- includes `low`, `medium`, or `high` confidence;
- calls blocked/unavailable probes evidence limitations;
- avoids claiming a single command proves root cause;
- proposes one next diagnostic action that most reduces uncertainty;
- does not prescribe configuration changes unless remediation was separately requested.
