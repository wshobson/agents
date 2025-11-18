# KVM Architecture Deep Dive

## Components

### KVM Kernel Module
- `/dev/kvm` character device
- Hardware virtualization (VMX/SVM)
- Memory management (EPT/NPT)

### QEMU Process
- Device emulation
- I/O handling
- Machine model

### VM Lifecycle
```
VM Create → VM Start → VM Run → VM Stop → VM Destroy
```

## Hardware Virtualization

### Intel VT-x
- VMCS (Virtual Machine Control Structure)
- VM-Entry / VM-Exit
- EPT (Extended Page Tables)

### AMD-V
- VMCB (Virtual Machine Control Block)
- NPT (Nested Page Tables)

## Performance Considerations

- VM-Exit overhead: 1000-5000 cycles
- Context switches: minimize with pinning
- TLB flushes: use huge pages
