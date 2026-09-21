## Custom Protocol Documentation

### Protocol Specification Template

````markdown
# Protocol Name Specification

## Overview

Brief description of protocol purpose and design.

## Transport

- Layer: TCP/UDP
- Port: XXXX
- Encryption: TLS 1.2+

## Message Format

### Header (12 bytes)

| Offset | Size | Field   | Description             |
| ------ | ---- | ------- | ----------------------- |
| 0      | 4    | Magic   | 0x50524F54 ("PROT")     |
| 4      | 2    | Version | Protocol version (1)    |
| 6      | 2    | Type    | Message type identifier |
| 8      | 4    | Length  | Payload length in bytes |

### Message Types

| Type | Name      | Description            |
| ---- | --------- | ---------------------- |
| 0x01 | HELLO     | Connection initiation  |
| 0x02 | HELLO_ACK | Connection accepted    |
| 0x03 | DATA      | Application data       |
| 0x04 | CLOSE     | Connection termination |

### Type 0x01: HELLO

| Offset | Size | Field      | Description              |
| ------ | ---- | ---------- | ------------------------ |
| 0      | 4    | ClientID   | Unique client identifier |
| 4      | 2    | Flags      | Connection flags         |
| 6      | var  | Extensions | TLV-encoded extensions   |

## State Machine
```

[INIT] --HELLO--> [WAIT_ACK] --HELLO_ACK--> [CONNECTED]
|
DATA/DATA
|
[CLOSED] <--CLOSE--+

```

## Examples
### Connection Establishment
```

Client -> Server: HELLO (ClientID=0x12345678)
Server -> Client: HELLO_ACK (Status=OK)
Client -> Server: DATA (payload)

```

````

### Wireshark Dissector (Lua)

```lua
-- custom_protocol.lua
local proto = Proto("custom", "Custom Protocol")

-- Define fields
local f_magic = ProtoField.string("custom.magic", "Magic")
local f_version = ProtoField.uint16("custom.version", "Version")
local f_type = ProtoField.uint16("custom.type", "Type")
local f_length = ProtoField.uint32("custom.length", "Length")
local f_payload = ProtoField.bytes("custom.payload", "Payload")

proto.fields = { f_magic, f_version, f_type, f_length, f_payload }

-- Message type names
local msg_types = {
    [0x01] = "HELLO",
    [0x02] = "HELLO_ACK",
    [0x03] = "DATA",
    [0x04] = "CLOSE"
}

function proto.dissector(buffer, pinfo, tree)
    -- Reject incomplete captures before creating any packet ranges.
    if buffer:len() < 12 then return 0 end
    local length = buffer(8, 4):uint()
    if length > buffer:len() - 12 then return 0 end

    pinfo.cols.protocol = "CUSTOM"

    local subtree = tree:add(proto, buffer())

    -- Parse header
    subtree:add(f_magic, buffer(0, 4))
    subtree:add(f_version, buffer(4, 2))

    local msg_type = buffer(6, 2):uint()
    subtree:add(f_type, buffer(6, 2)):append_text(
        " (" .. (msg_types[msg_type] or "Unknown") .. ")"
    )

    subtree:add(f_length, buffer(8, 4))

    if length > 0 then
        subtree:add(f_payload, buffer(12, length))
    end
end

-- Register for TCP port
local tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(8888, proto)
```
