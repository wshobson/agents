# Blockchain Web3

## Agents

In Gemini CLI, invoke agents by describing your task naturally. The model activates the appropriate expertise.

| Agent | Model | When to use |
|---|---|---|
| `blockchain-developer` | opus | Build production-ready Web3 applications, smart contracts, and decentralized systems. Implements DeFi protocols, NFT ... |

## Skills

Skills activate automatically when Gemini identifies a matching task.

| Skill | Activates when |
|---|---|
| `defi-protocol-templates` | Implement DeFi protocols with production-ready templates for staking, AMMs, governance, and lending systems. Use when building decentrali... |
| `nft-standards` | Implement NFT standards (ERC-721, ERC-1155) with proper metadata handling, minting strategies, and marketplace integration. Use when crea... |
| `solidity-security` | Master smart contract security best practices to prevent common vulnerabilities and implement secure Solidity patterns. Use when writing ... |
| `web3-testing` | Test smart contracts comprehensively using Hardhat and Foundry with unit tests, integration tests, and mainnet forking. Use when testing ... |

## Gemini CLI Usage

**Example natural language triggers:**

- "Build production-ready Web3 applications, smart contracts, and decentralized systems" → activates `blockchain-developer`
- "Implement DeFi protocols with production-ready templates for staking, AMMs, governance, and lending systems" → activates `defi-protocol-templates` skill

See [GEMINI.md](../../GEMINI.md) for the full plugin catalog and [docs/gemini-tool-mapping.md](../../docs/gemini-tool-mapping.md) for platform differences.
