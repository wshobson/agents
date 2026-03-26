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

## Anti-Debugging Techniques

### Windows Anti-Debugging

#### API-Based Detection

```c
// IsDebuggerPresent
if (IsDebuggerPresent()) {
    exit(1);
}

// CheckRemoteDebuggerPresent
BOOL debugged = FALSE;
CheckRemoteDebuggerPresent(GetCurrentProcess(), &debugged);
if (debugged) exit(1);

// NtQueryInformationProcess
typedef NTSTATUS (NTAPI *pNtQueryInformationProcess)(
    HANDLE, PROCESSINFOCLASS, PVOID, ULONG, PULONG);

DWORD debugPort = 0;
NtQueryInformationProcess(
    GetCurrentProcess(),
    ProcessDebugPort,        // 7
    &debugPort,
    sizeof(debugPort),
    NULL
);
if (debugPort != 0) exit(1);

// Debug flags
DWORD debugFlags = 0;
NtQueryInformationProcess(
    GetCurrentProcess(),
    ProcessDebugFlags,       // 0x1F
    &debugFlags,
    sizeof(debugFlags),
    NULL
);
if (debugFlags == 0) exit(1);  // 0 means being debugged
```

**Bypass:** Use ScyllaHide plugin in x64dbg (patches all common checks automatically). Manually: force `IsDebuggerPresent` return to 0, patch `PEB.BeingDebugged` to 0, hook `NtQueryInformationProcess`. In IDA: `ida_bytes.patch_byte(check_addr, 0x90)`.

#### PEB-Based Detection

```c
// Direct PEB access
#ifdef _WIN64
    PPEB peb = (PPEB)__readgsqword(0x60);
#else
    PPEB peb = (PPEB)__readfsdword(0x30);
#endif

// BeingDebugged flag
if (peb->BeingDebugged) exit(1);

// NtGlobalFlag
// Debugged: 0x70 (FLG_HEAP_ENABLE_TAIL_CHECK |
//                 FLG_HEAP_ENABLE_FREE_CHECK |
//                 FLG_HEAP_VALIDATE_PARAMETERS)
if (peb->NtGlobalFlag & 0x70) exit(1);

// Heap flags
PDWORD heapFlags = (PDWORD)((PBYTE)peb->ProcessHeap + 0x70);
if (*heapFlags & 0x50000062) exit(1);
```

**Bypass:** In x64dbg, follow `gs:[60]` (x64) or `fs:[30]` (x86) in dump. Set `BeingDebugged` (offset +2) to 0; clear `NtGlobalFlag` (offset +0xBC on x64).

#### Timing-Based Detection

```c
// RDTSC timing
uint64_t start = __rdtsc();
// ... some code ...
uint64_t end = __rdtsc();
if ((end - start) > THRESHOLD) exit(1);

// QueryPerformanceCounter
LARGE_INTEGER start, end, freq;
QueryPerformanceFrequency(&freq);
QueryPerformanceCounter(&start);
// ... code ...
QueryPerformanceCounter(&end);
double elapsed = (double)(end.QuadPart - start.QuadPart) / freq.QuadPart;
if (elapsed > 0.1) exit(1);  // Too slow = debugger

// GetTickCount
DWORD start = GetTickCount();
// ... code ...
if (GetTickCount() - start > 1000) exit(1);
```

**Python script — timing-based anti-debug detection scanner:**

```python
#!/usr/bin/env python3
"""Scan a binary for common timing-based anti-debug patterns."""
import re
import sys

PATTERNS = {
    "RDTSC":              rb"\x0f\x31",                    # RDTSC opcode
    "RDTSCP":             rb"\x0f\x01\xf9",                # RDTSCP opcode
    "GetTickCount":       rb"GetTickCount\x00",
    "QueryPerfCounter":   rb"QueryPerformanceCounter\x00",
    "NtQuerySysInfo":     rb"NtQuerySystemInformation\x00",
}

def scan(path: str) -> None:
    data = open(path, "rb").read()
    print(f"Scanning: {path} ({len(data)} bytes)\n")
    for name, pattern in PATTERNS.items():
        hits = [m.start() for m in re.finditer(re.escape(pattern), data)]
        if hits:
            offsets = ", ".join(hex(h) for h in hits[:5])
            print(f"  [{name}] found at: {offsets}")
    print("\nDone. Cross-reference offsets in IDA/Ghidra to find check logic.")

if __name__ == "__main__":
    scan(sys.argv[1])
```

**Bypass:** Use hardware breakpoints (no INT3 overhead), NOP the comparison + conditional jump, freeze RDTSC via hypervisor, or hook timing APIs to return consistent values.

#### Exception-Based Detection

```c
// SEH: if debugger is attached it consumes the INT3 exception
// and execution falls through to exit(1) instead of the __except handler
__try { __asm { int 3 } }
__except(EXCEPTION_EXECUTE_HANDLER) { return; }  // Clean: exception handled here
exit(1);  // Dirty: debugger swallowed the exception

// VEH: register handler that self-handles INT3 (increments RIP past INT3)
// Debugger intercepts first, handler never runs → detected
LONG CALLBACK VectoredHandler(PEXCEPTION_POINTERS ep) {
    if (ep->ExceptionRecord->ExceptionCode == EXCEPTION_BREAKPOINT) {
        ep->ContextRecord->Rip++;
        return EXCEPTION_CONTINUE_EXECUTION;
    }
    return EXCEPTION_CONTINUE_SEARCH;
}
```

**Bypass**: In x64dbg, set "Pass exception to program" for EXCEPTION_BREAKPOINT (Options → Exceptions → add 0x80000003).

### Linux Anti-Debugging

```c
// ptrace self-trace
if (ptrace(PTRACE_TRACEME, 0, NULL, NULL) == -1) {
    // Already being traced
    exit(1);
}

// /proc/self/status
FILE *f = fopen("/proc/self/status", "r");
char line[256];
while (fgets(line, sizeof(line), f)) {
    if (strncmp(line, "TracerPid:", 10) == 0) {
        int tracer_pid = atoi(line + 10);
        if (tracer_pid != 0) exit(1);
    }
}

// Parent process check
if (getppid() != 1 && strcmp(get_process_name(getppid()), "bash") != 0) {
    // Unusual parent (might be debugger)
}
```

**Bypass (LD_PRELOAD hook):**

```bash
# hook.c: long ptrace(int request, ...) { return 0; }
# gcc -shared -fPIC -o hook.so hook.c
LD_PRELOAD=./hook.so ./target
```

**GDB bypass command sequence:**

```gdb
# 1. Make ptrace(PTRACE_TRACEME) always return 0 (success)
catch syscall ptrace
commands
  silent
  set $rax = 0
  continue
end

# 2. Bypass check after ptrace call: find "cmp rax, 0xffffffff; je <exit>"
#    Clear ZF so the conditional jump is not taken:
#    set $eflags = $eflags & ~0x40

# 3. Bypass /proc/self/status TracerPid check at the open() level
catch syscall openat
commands
  silent
  # If arg contains "status", patch the fd result to /dev/null equivalent
  continue
end

# 4. Bypass parent process name check
set follow-fork-mode child
set detach-on-fork off
```

---

## Anti-VM Detection

### Hardware Fingerprinting

```c
// CPUID-based detection
int cpuid_info[4];
__cpuid(cpuid_info, 1);
// Check hypervisor bit (bit 31 of ECX)
if (cpuid_info[2] & (1 << 31)) {
    // Running in hypervisor
}

// CPUID brand string
__cpuid(cpuid_info, 0x40000000);
char vendor[13] = {0};
memcpy(vendor, &cpuid_info[1], 12);
// "VMwareVMware", "Microsoft Hv", "KVMKVMKVM", "VBoxVBoxVBox"

// MAC address prefix
// VMware: 00:0C:29, 00:50:56
// VirtualBox: 08:00:27
// Hyper-V: 00:15:5D
```

### Registry/File Detection

```c
// Windows registry keys
// HKLM\SOFTWARE\VMware, Inc.\VMware Tools
// HKLM\SOFTWARE\Oracle\VirtualBox Guest Additions
// HKLM\HARDWARE\ACPI\DSDT\VBOX__

// Files
// C:\Windows\System32\drivers\vmmouse.sys
// C:\Windows\System32\drivers\vmhgfs.sys
// C:\Windows\System32\drivers\VBoxMouse.sys

// Processes
// vmtoolsd.exe, vmwaretray.exe
// VBoxService.exe, VBoxTray.exe
```

### Timing-Based VM Detection

```c
// VM exits cause timing anomalies
uint64_t start = __rdtsc();
__cpuid(cpuid_info, 0);  // Causes VM exit
uint64_t end = __rdtsc();
if ((end - start) > 500) {
    // Likely in VM (CPUID takes longer)
}
```

**Bypass:** Use bare-metal environment, harden VM (remove guest tools, randomize MAC, delete artifact files), patch detection branches in the binary, or use FLARE-VM/REMnux with hardened settings.

For advanced VM detection (RDTSC delta calibration, VMware backdoor port, hypervisor leaf enumeration, guest driver artifact checks), see [references/advanced-techniques.md](references/advanced-techniques.md).

---

## Code Obfuscation

### Control Flow Obfuscation

#### Control Flow Flattening

```c
// Original
if (cond) {
    func_a();
} else {
    func_b();
}
func_c();

// Flattened
int state = 0;
while (1) {
    switch (state) {
        case 0:
            state = cond ? 1 : 2;
            break;
        case 1:
            func_a();
            state = 3;
            break;
        case 2:
            func_b();
            state = 3;
            break;
        case 3:
            func_c();
            return;
    }
}
```

**Analysis Approach:**

- Identify state variable
- Map state transitions
- Reconstruct original flow
- Tools: D-810 (IDA), SATURN

#### Opaque Predicates

```c
int x = rand();
if ((x * x) >= 0) { real_code(); }   // Always true  → junk_code() is dead
if ((x*(x+1)) % 2 == 1) { junk(); }  // Always false → consecutive product is even
```

**Analysis Approach:** Identify invariant expressions via symbolic execution (angr, Triton), or pattern-match known opaque forms and prune them.

### Data Obfuscation

#### String Encryption

```c
// XOR encryption
char decrypt_string(char *enc, int len, char key) {
    char *dec = malloc(len + 1);
    for (int i = 0; i < len; i++) {
        dec[i] = enc[i] ^ key;
    }
    dec[len] = 0;
    return dec;
}

// Stack strings
char url[20];
url[0] = 'h'; url[1] = 't'; url[2] = 't'; url[3] = 'p';
url[4] = ':'; url[5] = '/'; url[6] = '/';
// ...
```

**Analysis Approach:**

```python
# FLOSS for automatic string deobfuscation
floss malware.exe

# IDAPython string decryption
def decrypt_xor(ea, length, key):
    result = ""
    for i in range(length):
        byte = ida_bytes.get_byte(ea + i)
        result += chr(byte ^ key)
    return result
```

#### API Obfuscation

```c
// Dynamic API resolution
typedef HANDLE (WINAPI *pCreateFileW)(LPCWSTR, DWORD, DWORD,
    LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE);

HMODULE kernel32 = LoadLibraryA("kernel32.dll");
pCreateFileW myCreateFile = (pCreateFileW)GetProcAddress(
    kernel32, "CreateFileW");

// API hashing
DWORD hash_api(char *name) {
    DWORD hash = 0;
    while (*name) {
        hash = ((hash >> 13) | (hash << 19)) + *name++;
    }
    return hash;
}
// Resolve by hash comparison instead of string
```

**Analysis Approach:** Identify the hash algorithm, build a database of known API name hashes, use HashDB plugin for IDA, or run under a debugger to let the binary resolve calls at runtime.

### Instruction-Level Obfuscation

```asm
; Dead code insertion — semantically inert but pollutes disassembly
push ebx / mov eax, 1 / pop ebx / xor ecx, ecx / add ecx, ecx

; Instruction substitution — same semantics, different encoding
xor eax, eax  →  sub eax, eax  |  mov eax, 0  |  and eax, 0
mov eax, 1    →  xor eax, eax; inc eax  |  push 1; pop eax
```

For advanced anti-disassembly tricks (overlapping instructions, junk byte insertion, self-modifying code, ROP as obfuscation), see [references/advanced-techniques.md](references/advanced-techniques.md).

---

## Bypass Strategies Summary

### General Principles

1. **Understand the protection**: Identify what technique is used
2. **Find the check**: Locate protection code in binary
3. **Patch or hook**: Modify check to always pass
4. **Use appropriate tools**: ScyllaHide, x64dbg plugins
5. **Document findings**: Keep notes on bypassed protections

### Tool Recommendations

```
Anti-debug bypass:    ScyllaHide, TitanHide
Unpacking:           x64dbg + Scylla, OllyDumpEx
Deobfuscation:       D-810, SATURN, miasm
VM analysis:         VMAttack, NoVmp, manual tracing
String decryption:   FLOSS, custom scripts
Symbolic execution:  angr, Triton
```

### Ethical Considerations

This knowledge should only be used for:

- Authorized security research
- Malware analysis (defensive)
- CTF competitions
- Understanding protections for legitimate purposes
- Educational purposes

Never use to bypass protections for: software piracy, unauthorized access, or malicious purposes.

---

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
