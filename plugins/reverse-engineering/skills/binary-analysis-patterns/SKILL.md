---
name: binary-analysis-patterns
description: Master binary analysis patterns including disassembly, decompilation, control flow analysis, and code pattern recognition. Use when analyzing executables, understanding compiled code, or performing static analysis on binaries.
---

# Binary Analysis Patterns

Comprehensive patterns and techniques for analyzing compiled binaries, understanding assembly code, and reconstructing program logic.

## When to Use This Skill

- Reverse-engineering an unknown executable to understand its behavior
- Analyzing malware or obfuscated binaries with Ghidra / IDA Pro / Binary Ninja
- Recognizing common assembly idioms (function prologues, switch tables, vtable dispatch)
- Reconstructing high-level control flow from compiled code
- Identifying compiler-introduced patterns (stack canaries, PIC trampolines)

## Detailed section: Disassembly Fundamentals

Originally a 2047-byte section in this SKILL.md. Moved to `references/details.md` to fit Codex's 8 KB skill body cap.

## Control Flow Patterns

### Conditional Branches

```asm
; if (a == b)
cmp eax, ebx
jne skip_block
; ... if body ...
skip_block:

; if (a < b) - signed
cmp eax, ebx
jge skip_block    ; Jump if greater or equal
; ... if body ...
skip_block:

; if (a < b) - unsigned
cmp eax, ebx
jae skip_block    ; Jump if above or equal
; ... if body ...
skip_block:
```

### Loop Patterns

```asm
; for (int i = 0; i < n; i++)
xor ecx, ecx           ; i = 0
loop_start:
cmp ecx, [n]           ; i < n
jge loop_end
; ... loop body ...
inc ecx                ; i++
jmp loop_start
loop_end:

; while (condition)
jmp loop_check
loop_body:
; ... body ...
loop_check:
cmp eax, ebx
jl loop_body

; do-while
loop_body:
; ... body ...
cmp eax, ebx
jl loop_body
```

### Switch Statement Patterns

```asm
; Jump table pattern
mov eax, [switch_var]
cmp eax, max_case
ja default_case
jmp [jump_table + eax*8]

; Sequential comparison (small switch)
cmp eax, 1
je case_1
cmp eax, 2
je case_2
cmp eax, 3
je case_3
jmp default_case
```

## Data Structure Patterns

### Array Access

```asm
; array[i] - 4-byte elements
mov eax, [rbx + rcx*4]        ; rbx=base, rcx=index

; array[i] - 8-byte elements
mov rax, [rbx + rcx*8]

; Multi-dimensional array[i][j]
; arr[i][j] = base + (i * cols + j) * element_size
imul eax, [cols]
add eax, [j]
mov edx, [rbx + rax*4]
```

### Structure Access

```c
struct Example {
    int a;      // offset 0
    char b;     // offset 4
    // padding  // offset 5-7
    long c;     // offset 8
    short d;    // offset 16
};
```

```asm
; Accessing struct fields
mov rdi, [struct_ptr]
mov eax, [rdi]         ; s->a (offset 0)
movzx eax, byte [rdi+4] ; s->b (offset 4)
mov rax, [rdi+8]       ; s->c (offset 8)
movzx eax, word [rdi+16] ; s->d (offset 16)
```

### Linked List Traversal

```asm
; while (node != NULL)
list_loop:
test rdi, rdi          ; node == NULL?
jz list_done
; ... process node ...
mov rdi, [rdi+8]       ; node = node->next (assuming next at offset 8)
jmp list_loop
list_done:
```

## Common Code Patterns

### String Operations

```asm
; strlen pattern
xor ecx, ecx
strlen_loop:
cmp byte [rdi + rcx], 0
je strlen_done
inc ecx
jmp strlen_loop
strlen_done:
; ecx contains length

; strcpy pattern
strcpy_loop:
mov al, [rsi]
mov [rdi], al
test al, al
jz strcpy_done
inc rsi
inc rdi
jmp strcpy_loop
strcpy_done:

; memcpy using rep movsb
mov rdi, dest
mov rsi, src
mov rcx, count
rep movsb
```

### Arithmetic Patterns

```asm
; Multiplication by constant
; x * 3
lea eax, [rax + rax*2]

; x * 5
lea eax, [rax + rax*4]

; x * 10
lea eax, [rax + rax*4]  ; x * 5
add eax, eax            ; * 2

; Division by power of 2 (signed)
mov eax, [x]
cdq                     ; Sign extend to EDX:EAX
and edx, 7              ; For divide by 8
add eax, edx            ; Adjust for negative
sar eax, 3              ; Arithmetic shift right

; Modulo power of 2
and eax, 7              ; x % 8
```

### Bit Manipulation

```asm
; Test specific bit
test eax, 0x80          ; Test bit 7
jnz bit_set

; Set bit
or eax, 0x10            ; Set bit 4

; Clear bit
and eax, ~0x10          ; Clear bit 4

; Toggle bit
xor eax, 0x10           ; Toggle bit 4

; Count leading zeros
bsr eax, ecx            ; Bit scan reverse
xor eax, 31             ; Convert to leading zeros

; Population count (popcnt)
popcnt eax, ecx         ; Count set bits
```

## Decompilation Patterns

### Variable Recovery

```asm
; Local variable at rbp-8
mov qword [rbp-8], rax  ; Store to local
mov rax, [rbp-8]        ; Load from local

; Stack-allocated array
lea rax, [rbp-0x40]     ; Array starts at rbp-0x40
mov [rax], edx          ; array[0] = value
mov [rax+4], ecx        ; array[1] = value
```

### Function Signature Recovery

```asm
; Identify parameters by register usage
func:
    ; rdi used as first param (System V)
    mov [rbp-8], rdi    ; Save param to local
    ; rsi used as second param
    mov [rbp-16], rsi
    ; Identify return by RAX at end
    mov rax, [result]
    ret
```

### Type Recovery

```asm
; 1-byte operations suggest char/bool
movzx eax, byte [rdi]   ; Zero-extend byte
movsx eax, byte [rdi]   ; Sign-extend byte

; 2-byte operations suggest short
movzx eax, word [rdi]
movsx eax, word [rdi]

; 4-byte operations suggest int/float
mov eax, [rdi]
movss xmm0, [rdi]       ; Float

; 8-byte operations suggest long/double/pointer
mov rax, [rdi]
movsd xmm0, [rdi]       ; Double
```

## Ghidra Analysis Tips

### Improving Decompilation

```java
// In Ghidra scripting
// Fix function signature
Function func = getFunctionAt(toAddr(0x401000));
func.setReturnType(IntegerDataType.dataType, SourceType.USER_DEFINED);

// Create structure type
StructureDataType struct = new StructureDataType("MyStruct", 0);
struct.add(IntegerDataType.dataType, "field_a", null);
struct.add(PointerDataType.dataType, "next", null);

// Apply to memory
createData(toAddr(0x601000), struct);
```

### Pattern Matching Scripts

```python
# Find all calls to dangerous functions
for func in currentProgram.getFunctionManager().getFunctions(True):
    for ref in getReferencesTo(func.getEntryPoint()):
        if func.getName() in ["strcpy", "sprintf", "gets"]:
            print(f"Dangerous call at {ref.getFromAddress()}")
```

## IDA Pro Patterns

### IDAPython Analysis

```python
import idaapi
import idautils
import idc

# Find all function calls
def find_calls(func_name):
    for func_ea in idautils.Functions():
        for head in idautils.Heads(func_ea, idc.find_func_end(func_ea)):
            if idc.print_insn_mnem(head) == "call":
                target = idc.get_operand_value(head, 0)
                if idc.get_func_name(target) == func_name:
                    print(f"Call to {func_name} at {hex(head)}")

# Rename functions based on strings
def auto_rename():
    for s in idautils.Strings():
        for xref in idautils.XrefsTo(s.ea):
            func = idaapi.get_func(xref.frm)
            if func and "sub_" in idc.get_func_name(func.start_ea):
                # Use string as hint for naming
                pass
```

## Best Practices

### Analysis Workflow

1. **Initial triage**: File type, architecture, imports/exports
2. **String analysis**: Identify interesting strings, error messages
3. **Function identification**: Entry points, exports, cross-references
4. **Control flow mapping**: Understand program structure
5. **Data structure recovery**: Identify structs, arrays, globals
6. **Algorithm identification**: Crypto, hashing, compression
7. **Documentation**: Comments, renamed symbols, type definitions

### Common Pitfalls

- **Optimizer artifacts**: Code may not match source structure
- **Inline functions**: Functions may be expanded inline
- **Tail call optimization**: `jmp` instead of `call` + `ret`
- **Dead code**: Unreachable code from optimization
- **Position-independent code**: RIP-relative addressing
