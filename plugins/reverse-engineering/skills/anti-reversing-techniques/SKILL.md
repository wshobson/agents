---
name: anti-reversing-techniques
description: Understand anti-reversing, obfuscation, and protection techniques encountered during software analysis. Use this skill when analyzing malware evasion techniques, when implementing anti-debugging protections for CTF challenges, when reverse engineering packed binaries, or when building security research tools that need to detect virtualized environments.
---

> **AUTHORIZED USE ONLY**: This skill contains dual-use security techniques. Before proceeding with any bypass or analysis:
>
> 1. **Verify authorization**: Confirm you have explicit written permission from the software owner, or are operating within a legitimate security context (CTF, authorized pentest, malware analysis, security research)
> 2. **Document scope**: Ensure your activities fall within the defined scope of your authorization
> 3. **Legal compliance**: Understand that unauthorized bypassing of software protection may violate laws (CFAA, DMCA anti-circumvention, etc.)
>
> **Legitimate use cases**: Malware analysis, authorized penetration testing, CTF competitions, academic security research, analyzing software you own/have rights to

# Anti-Reversing Techniques

Understanding protection mechanisms encountered during authorized software analysis, security research, and malware analysis. This knowledge helps analysts bypass protections to complete legitimate analysis tasks.

For advanced techniques, see [references/advanced-techniques.md](references/advanced-techniques.md)

---

## Input / Output

**What you provide:**

- **Binary path or sample**: the executable, DLL, or firmware image under analysis
- **Platform**: Windows x86/x64, Linux, macOS, ARM — affects which checks apply
- **Goal**: bypass for dynamic analysis, identify protection type, build detection code, implement for CTF

**What this skill produces:**

- **Protection identification**: named technique (e.g., RDTSC timing check, PEB BeingDebugged) with location in binary
- **Bypass strategy**: specific patch addresses, hook points, or tool commands to neutralize each check
- **Analysis report**: structured findings listing each protection layer, severity, and recommended bypass
- **Code artifacts**: Python/IDAPython scripts, GDB command sequences, or C stubs for bypassing or implementing checks

---

## Detailed patterns and worked examples

Detailed pattern documentation lives in `references/details.md`. Read that file when the navigation tier above is insufficient.

## Troubleshooting

**Detection technique works on x86 but not ARM**

RDTSC and CPUID are x86-only. On ARM, use `MRS x0, PMCCNTR_EL0` (requires kernel PMU access) or `clock_gettime(CLOCK_MONOTONIC)`. PEB/TEB do not exist on ARM — replace with `/proc/self/status` (Linux) or `task_info` (macOS). Rebuild detection logic with platform-specific APIs.

**False positive on legitimate debugger or analysis tool**

Timing checks fire when Process Monitor or AV hooks inflate syscall latency. Calibrate the threshold at startup: measure the guarded path 3 times and use `mean + 3*stddev`. For ptrace checks, verify the TracerPid comm name via `/proc/<pid>/comm` before exiting — it may be an unrelated monitoring tool, not a debugger.

**Bypass patch causes crash instead of continuing execution**

Before NOPing a conditional jump, trace the "detected" branch fully. If it initializes or frees heap state needed later, patching the jump skips that setup and corrupts state. Instead, patch the comparison operand to the expected "clean" value, or use x64dbg's "Set condition to always false" on the breakpoint rather than modifying bytes.

---

## Related Skills

- `binary-analysis-patterns` — static and dynamic analysis workflows for ELF/PE/Mach-O
- `memory-forensics` — process memory acquisition, artifact extraction, and live analysis
- `protocol-reverse-engineering` — decoding custom binary protocols and encrypted network traffic
