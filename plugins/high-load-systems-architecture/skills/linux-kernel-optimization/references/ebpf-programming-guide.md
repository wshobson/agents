# eBPF Programming Guide

## Overview

eBPF allows running programs in kernel space safely.

## Use Cases

- Performance monitoring
- Network filtering
- Security policies
- Tracing and debugging

## Example: Count Syscalls

```c
#include <linux/bpf.h>
#include <bpf/bpf_helpers.h>

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 1024);
    __type(key, u32);
    __type(value, u64);
} syscall_count SEC(".maps");

SEC("tracepoint/raw_syscalls/sys_enter")
int count_syscalls(struct trace_event_raw_sys_enter *ctx) {
    u32 key = ctx->id;
    u64 *count = bpf_map_lookup_elem(&syscall_count, &key);
    if (count) {
        (*count)++;
    } else {
        u64 init = 1;
        bpf_map_update_elem(&syscall_count, &key, &init, BPF_ANY);
    }
    return 0;
}
```

## Tools

- **bpftrace**: High-level tracing language
- **bcc**: BPF Compiler Collection
- **libbpf**: C library for BPF

## bpftrace Example

```bash
# Trace open() syscalls
bpftrace -e 'tracepoint:syscalls:sys_enter_open { printf("%s %s\n", comm, str(args->filename)); }'

# Profile CPU
bpftrace -e 'profile:hz:99 { @[kstack] = count(); }'
```
