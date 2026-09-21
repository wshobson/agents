## Binary Protocol Analysis

### Structure Identification

```text
# Common patterns in binary protocols

# Length-prefixed message
struct Message {
    uint32_t length;      # Payload length (excludes header)
    uint16_t msg_type;    # Message type identifier
    uint8_t  flags;       # Flags/options
    uint8_t  reserved;    # Padding/alignment
    uint8_t  payload[];   # Variable-length payload
};

# Type-Length-Value (TLV)
struct TLV {
    uint8_t  type;        # Field type
    uint16_t length;      # Field length
    uint8_t  value[];     # Field data
};

# Fixed header + variable payload
struct Packet {
    uint8_t  magic[4];    # "ABCD" signature
    uint32_t version;
    uint32_t payload_len;
    uint32_t checksum;    # CRC32 or similar
    uint8_t  payload[];
};
```

### Python Protocol Parser

```python
import struct
from dataclasses import dataclass

@dataclass
class MessageHeader:
    magic: bytes
    version: int
    msg_type: int
    length: int

    @classmethod
    def from_bytes(cls, data: bytes):
        magic, version, msg_type, length = struct.unpack(
            ">4sHHI", data[:12]
        )
        return cls(magic, version, msg_type, length)

def parse_messages(data: bytes):
    offset = 0
    messages = []

    while offset < len(data):
        if len(data) - offset < 12:
            raise ValueError("truncated message header")
        header = MessageHeader.from_bytes(data[offset:])
        if header.length > len(data) - offset - 12:
            raise ValueError("truncated message payload")
        payload = data[offset+12:offset+12+header.length]
        messages.append((header, payload))
        offset += 12 + header.length

    return messages

# Parse TLV structure
def parse_tlv(data: bytes):
    fields = []
    offset = 0

    while offset < len(data):
        if len(data) - offset < 3:
            raise ValueError("truncated TLV header")
        field_type = data[offset]
        length = struct.unpack(">H", data[offset+1:offset+3])[0]
        if length > len(data) - offset - 3:
            raise ValueError("truncated TLV value")
        value = data[offset+3:offset+3+length]
        fields.append((field_type, value))
        offset += 3 + length

    return fields
```

### Hex Dump Analysis

```python
def hexdump(data: bytes, width: int = 16):
    """Format binary data as hex dump."""
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i:i+width]
        hex_part = ' '.join(f'{b:02x}' for b in chunk)
        ascii_part = ''.join(
            chr(b) if 32 <= b < 127 else '.'
            for b in chunk
        )
        lines.append(f'{i:08x}  {hex_part:<{width*3}}  {ascii_part}')
    return '\n'.join(lines)

# Example output:
# 00000000  48 54 54 50 2f 31 2e 31  20 32 30 30 20 4f 4b 0d  HTTP/1.1 200 OK.
# 00000010  0a 43 6f 6e 74 65 6e 74  2d 54 79 70 65 3a 20 74  .Content-Type: t
```

## Encryption Analysis

### Identifying Encryption

```python
# Entropy analysis - high entropy suggests encryption/compression
import math
from collections import Counter

def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counter = Counter(data)
    probs = [count / len(data) for count in counter.values()]
    return -sum(p * math.log2(p) for p in probs)

# Entropy thresholds:
# < 6.0: Likely plaintext or structured data
# 6.0-7.5: Possibly compressed
# > 7.5: Likely encrypted or random

# Common encryption indicators
# - High, uniform entropy
# - No obvious structure or patterns
# - Length often multiple of block size (16 for AES)
# - Possible IV at start (16 bytes for AES-CBC)
```

### TLS Analysis

These fields follow the [TLS](https://www.wireshark.org/docs/dfref/t/tls.html) and [X.509](https://www.wireshark.org/docs/dfref/x/x509sat.html) display-filter references (JA3/JA3S requires Wireshark 3.6+).

```bash
# Extract TLS metadata
tshark -r capture.pcap -Y "tls.handshake" \
    -T fields -e ip.src -e tls.handshake.ciphersuite

# JA3 fingerprinting (client)
tshark -r capture.pcap -Y "tls.handshake.type == 1" \
    -T fields -e tls.handshake.ja3

# JA3S fingerprinting (server)
tshark -r capture.pcap -Y "tls.handshake.type == 2" \
    -T fields -e tls.handshake.ja3s

# Certificate name/attribute strings
tshark -r capture.pcap -Y "tls.handshake.certificate" \
    -T fields -e x509sat.PrintableString
```

### Decryption Approaches

```bash
# Pre-master secret log (browser)
export SSLKEYLOGFILE=/tmp/keys.log

# Configure Wireshark
# Edit > Preferences > Protocols > TLS
# (Pre)-Master-Secret log filename: /tmp/keys.log

# Decrypt with private key (if available)
# Only works for RSA key exchange
# Edit > Preferences > Protocols > TLS > RSA keys list
```
