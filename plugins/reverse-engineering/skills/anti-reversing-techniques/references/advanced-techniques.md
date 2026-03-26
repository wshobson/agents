# Advanced Anti-Reversing Techniques

This reference covers advanced and niche techniques extracted from the core skill to keep SKILL.md focused on common patterns. Refer here for deep-dive analysis of virtualization-based protections, packer internals, and anti-disassembly tricks.

---

## Packing and Encryption

### Common Packers

```
UPX          - Open source, easy to unpack (upx -d)
Themida      - Commercial, VM-based protection with anti-debug
VMProtect    - Commercial, code virtualization with multiple VM architectures
ASPack       - Compression packer, LZSS-based
PECompact    - Compression packer with CRC integrity checks
Enigma       - Commercial protector with key-based licensing
MPRESS       - LZMA-based packer, often used by malware
Obsidium     - Commercial, anti-debug + anti-VM + encryption
```

### Unpacking Methodology

```
1. Identify packer (DIE, Exeinfo PE, PEiD, detect-it-easy)

2. Static unpacking (if known packer):
   - UPX: upx -d packed.exe
   - Use existing unpacker tools from UnpacMe, MalwareBazaar

3. Dynamic unpacking:
   a. Find Original Entry Point (OEP)
   b. Set breakpoint on OEP
   c. Dump memory when OEP reached
   d. Fix import table (Scylla, ImpREC)

4. OEP finding techniques:
   - Hardware breakpoint on stack (ESP trick)
   - Break on common API calls (GetCommandLineA, GetModuleHandle)
   - Trace and look for typical entry prologue (push ebp / mov ebp, esp)
   - Check for tail jump pattern: jmp <far address>
```

### Manual Unpacking (ESP Trick — x64dbg)

```
1. Load packed binary in x64dbg
2. Note entry point (packer stub address)
3. Use ESP trick:
   a. Run to entry point (F9 then F8 until PUSHAD)
   b. Right-click ESP value → "Follow in Dump"
   c. Set hardware breakpoint on access (HW BP on [ESP])
   d. Run (F9) — execution breaks after POPAD (stack restored)
4. Look for JMP to OEP (often a far jump to .text section)
5. At OEP, use Scylla plugin:
   - IAT Autosearch → Get Imports
   - Dump process
   - Fix dump with imports
```

### UPX Variant Unpacking

```bash
# Standard UPX — direct decompress
upx -d packed.exe -o unpacked.exe

# Modified UPX header (signature patched to evade upx -d):
# 1. Find UPX0/UPX1 section names (may be renamed)
# 2. Restore original UPX magic bytes: 0x55 0x50 0x58
# 3. Then run upx -d

# Python: restore UPX magic for patched header
python3 -c "
import sys
data = open(sys.argv[1], 'rb').read()
# UPX magic at various offsets — search for stub pattern
idx = data.find(b'\x60\xBE')  # PUSHAD; MOV ESI stub
print(f'Stub at: {hex(idx)}')
"
```

---

## Virtualization-Based Protection

### Code Virtualization Architecture

```
Original x86 code is converted to custom bytecode interpreted by an
embedded virtual machine at runtime.

Original:          VM Protected:
  mov eax, 1    →    push vm_context_ptr
  add eax, 2         call vm_entry
  ret                ; VM dispatcher loop decodes bytecode
                     ; and invokes handler table entries
                     ; equivalent semantics, unrecognizable form
```

### VM Component Identification

```
1. VM Entry Point:
   - Usually a CALL or JMP to a large function with a loop
   - Look for: load bytecode ptr, load handler table, dispatch loop

2. Handler Table:
   - Array of function pointers (one per virtual opcode)
   - Indexed by decoded opcode byte/word
   - Each handler emulates one instruction

3. Virtual Registers:
   - Stored in a context structure (vm_context)
   - Usually on the stack or in a dedicated heap allocation
   - Map to native registers by handler logic

4. Bytecode Location:
   - Separate section (.vmp0, .vmp1 in VMProtect)
   - Or inline with code (Themida)
   - Encrypted or compressed in some implementations
```

### Devirtualization Analysis Workflow

```
1. Identify VM entry: look for large functions with indirect dispatch (jmp [reg+offset])

2. Trace execution with logging:
   - Use x64dbg trace log: log handler address and context on each iteration
   - Example trace command in x64dbg: log "{p:rax} {p:rbx}" (on handler dispatch)

3. Map bytecode to operations:
   - Each handler maps to a semantic operation (ADD, LOAD, STORE, JCC, etc.)
   - Build a table: vm_opcode → native semantic

4. Lift to IR:
   - Tools: VMAttack (IDA plugin), SATURN, NoVmp (open source, VMProtect 3)
   - angr: load binary, explore VM entry to extract symbolic semantics
   - Triton: dynamic symbolic execution to lift VM handlers

5. Reconstruct control flow:
   - After lifting, rebuild CFG from recovered semantics
   - Tools output pseudo-C or assembly that is analyzable in IDA/Ghidra
```

### VMProtect-Specific Notes

```
VMProtect 3.x uses multiple VM architectures in one binary.
Each protected function may use a different VM instance.

Indicators:
- Sections named .vmp0, .vmp1 (or renamed)
- Characteristic dispatcher: movzx eax, byte ptr [esi]; jmp [eax*4+handler_table]
- Functions begin with PUSH of a magic constant, then JMP vm_entry

Tools:
- NoVmp: open-source devirtualizer for VMProtect 3
- SATURN: IDA plugin, handles multiple packer/VM types
- vmp_dumper: extracts bytecode for offline analysis
```

---

## Advanced Anti-Disassembly Tricks

### Overlapping Instructions

```asm
; The disassembler decodes one path, but execution takes another.
; Jump lands in the middle of a multi-byte instruction.

eb 01          ; JMP +1  (jumps over next byte)
e8             ; This byte is the "fake" start of CALL — never executed
58             ; POP EAX — this is what executes after the JMP

; Result: linear disassembly shows CALL (e8 58 ...), but at runtime
; execution reaches POP EAX at the byte after JMP target.
```

### Junk Byte Insertion

```asm
; Insert bytes that are valid as part of a multi-byte encoding
; but never actually execute (jumped over).

jmp short real_code   ; eb 03 — jump over 3 bytes
db 0xFF, 0x15, 0x00   ; Fake MOV/CALL prefix bytes — confuse disassembler
real_code:
mov eax, 1            ; Actual instruction
```

### Self-Modifying Code Patterns

```c
// Decrypt instruction bytes at runtime
unsigned char code[] = { 0x90 ^ 0xAA, 0xC3 ^ 0xAA };  // Encrypted NOP; RET
void decrypt_and_run(unsigned char *buf, size_t len, unsigned char key) {
    // Mark page executable
    VirtualProtect(buf, len, PAGE_EXECUTE_READWRITE, &old);
    for (size_t i = 0; i < len; i++) buf[i] ^= key;
    ((void(*)())buf)();
}
```

**Analysis Approach:**
- Set memory write breakpoints on the code region to catch decryption
- Use PIN or DynamoRIO to log executed instruction addresses
- Dump memory after self-modification to capture the real code

### Return-Oriented Programming as Obfuscation

```
Some protectors use ROP chains not for exploitation but for obfuscation:
- Replace direct CALL/JMP with a crafted stack + RET
- Disassembler cannot follow indirect returns easily

Detection: Look for sequences of POP; RET or ADD ESP, N; RET
Tools: ROPgadget, rp++ can enumerate; angr can follow symbolically
```

---

## Advanced VM Detection Techniques

### RDTSC Delta Calibration

```c
// Calibrate baseline on real hardware, detect anomaly in VM
// VM exits on CPUID/IN instructions inflate RDTSC delta significantly

static inline uint64_t rdtsc(void) {
    unsigned int lo, hi;
    __asm__ __volatile__("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

int detect_vm_timing(void) {
    uint64_t t1 = rdtsc();
    __asm__ __volatile__("cpuid" ::: "eax","ebx","ecx","edx");
    uint64_t t2 = rdtsc();
    // Bare metal: delta ~150-300 cycles; VM: delta >1000 cycles
    return (t2 - t1) > 750;
}
```

### VMEXIT Side-Channel via IN Instruction

```c
// IN instruction to port 0x5658 (VMware backdoor) causes VM exit
// On bare metal: raises #GP exception; in VMware: returns data
int detect_vmware_backdoor(void) {
    __try {
        __asm {
            push eax
            push ebx
            push ecx
            push edx
            mov eax, 'VMXh'   // VMware magic
            mov ecx, 10       // Get version command
            mov dx,  0x5658   // VMware backdoor port
            in eax, dx
            mov [is_vm], 1
            pop edx
            pop ecx
            pop ebx
            pop eax
        }
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        // Exception = bare metal, IN caused #GP
    }
    return is_vm;
}
```

### Hypervisor Leaf Enumeration

```c
// CPUID leaf 0x40000000–0x4FFFFFFF reserved for hypervisors
void enumerate_hypervisor(void) {
    int info[4];
    __cpuid(info, 0x40000000);
    char sig[13] = {0};
    memcpy(sig,     &info[1], 4);
    memcpy(sig + 4, &info[2], 4);
    memcpy(sig + 8, &info[3], 4);
    // Known signatures:
    // "VMwareVMware" → VMware
    // "Microsoft Hv" → Hyper-V
    // "KVMKVMKVM\0\0\0" → KVM
    // "VBoxVBoxVBox" → VirtualBox
    // "XenVMMXenVMM" → Xen
    printf("Hypervisor: %s\n", sig);
}
```

### Guest Driver / Artifact Detection

```c
// Check for known VM driver files (Windows)
const char *vm_drivers[] = {
    "C:\\Windows\\System32\\drivers\\vmmouse.sys",   // VMware
    "C:\\Windows\\System32\\drivers\\vmhgfs.sys",    // VMware shared folders
    "C:\\Windows\\System32\\drivers\\VBoxMouse.sys", // VirtualBox
    "C:\\Windows\\System32\\drivers\\VBoxGuest.sys", // VirtualBox
    "C:\\Windows\\System32\\drivers\\balloon.sys",   // QEMU/KVM
    NULL
};

int check_vm_files(void) {
    for (int i = 0; vm_drivers[i]; i++) {
        if (GetFileAttributesA(vm_drivers[i]) != INVALID_FILE_ATTRIBUTES)
            return 1;
    }
    return 0;
}

// Registry artifact check
const char *vm_reg_keys[] = {
    "SOFTWARE\\VMware, Inc.\\VMware Tools",
    "SOFTWARE\\Oracle\\VirtualBox Guest Additions",
    "HARDWARE\\ACPI\\DSDT\\VBOX__",
    NULL
};
```

---

## Packer/Protector Detection Reference

### DIE (Detect-It-Easy) Signatures

```
- Entropy > 7.0 on a section → likely packed/encrypted
- Section name mismatch (e.g., .text has exec+write permissions) → self-modifying
- Import table with only LoadLibrary + GetProcAddress → dynamic API resolution
- Single section with high entropy + no readable strings → heavy packing
```

### PE Anomaly Checklist for Packed Binaries

```
[ ] Section characteristics: writable + executable = unusual
[ ] Virtual size >> raw size on code section = unpacking stub inflates
[ ] Import table almost empty (only 1-3 imports) = dynamic resolution
[ ] Entry point not in .text section = custom stub
[ ] High entropy (>7.2) in any section = encryption/compression
[ ] Overlay data after EOF of last section = appended payload
[ ] TLS callbacks present = early execution before main EP
```
