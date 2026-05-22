# memory-forensics — detailed sections

## Volatility 3 Framework

### Installation and Setup

```bash
# Install Volatility 3
pip install volatility3

# Install symbol tables (Windows)
# Download from https://downloads.volatilityfoundation.org/volatility3/symbols/

# Basic usage
vol -f memory.raw <plugin>

# With symbol path
vol -f memory.raw -s /path/to/symbols windows.pslist
```

### Essential Plugins

#### Process Analysis

```bash
# List processes
vol -f memory.raw windows.pslist

# Process tree (parent-child relationships)
vol -f memory.raw windows.pstree

# Hidden process detection
vol -f memory.raw windows.psscan

# Process memory dumps
vol -f memory.raw windows.memmap --pid <PID> --dump

# Process environment variables
vol -f memory.raw windows.envars --pid <PID>

# Command line arguments
vol -f memory.raw windows.cmdline
```

#### Network Analysis

```bash
# Network connections
vol -f memory.raw windows.netscan

# Network connection state
vol -f memory.raw windows.netstat
```

#### DLL and Module Analysis

```bash
# Loaded DLLs per process
vol -f memory.raw windows.dlllist --pid <PID>

# Find hidden/injected DLLs
vol -f memory.raw windows.ldrmodules

# Kernel modules
vol -f memory.raw windows.modules

# Module dumps
vol -f memory.raw windows.moddump --pid <PID>
```

#### Memory Injection Detection

```bash
# Detect code injection
vol -f memory.raw windows.malfind

# VAD (Virtual Address Descriptor) analysis
vol -f memory.raw windows.vadinfo --pid <PID>

# Dump suspicious memory regions
vol -f memory.raw windows.vadyarascan --yara-rules rules.yar
```

#### Registry Analysis

```bash
# List registry hives
vol -f memory.raw windows.registry.hivelist

# Print registry key
vol -f memory.raw windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"

# Dump registry hive
vol -f memory.raw windows.registry.hivescan --dump
```

#### File System Artifacts

```bash
# Scan for file objects
vol -f memory.raw windows.filescan

# Dump files from memory
vol -f memory.raw windows.dumpfiles --pid <PID>

# MFT analysis
vol -f memory.raw windows.mftscan
```

### Linux Analysis

```bash
# Process listing
vol -f memory.raw linux.pslist

# Process tree
vol -f memory.raw linux.pstree

# Bash history
vol -f memory.raw linux.bash

# Network connections
vol -f memory.raw linux.sockstat

# Loaded kernel modules
vol -f memory.raw linux.lsmod

# Mount points
vol -f memory.raw linux.mount

# Environment variables
vol -f memory.raw linux.envars
```

### macOS Analysis

```bash
# Process listing
vol -f memory.raw mac.pslist

# Process tree
vol -f memory.raw mac.pstree

# Network connections
vol -f memory.raw mac.netstat

# Kernel extensions
vol -f memory.raw mac.lsmod
```
