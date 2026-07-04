---
name: x402-payment
description: Core x402 payment protocol setup — monetize any MCP server via HTTP 402 with Stripe or crypto. One-line integration, zero code changes.
---

# x402 Payment Protocol

Monetize your MCP server using the x402 payment protocol (HTTP 402 Payment Required). Accept Stripe fiat or crypto (USDC) with zero code changes.

## When to Use This Skill

- Adding pay-per-call billing to any MCP server
- Setting up HTTP 402 payment walls on APIs
- Monetizing AI agent tools and services
- Implementing micropayments for agent-to-agent commerce

## Quick Start

### 1. Install the middleware

```bash
npm install @gadgethumans/x402
```

### 2. Wrap your MCP server

```javascript
import { x402 } from '@gadgethumans/x402';

const server = new McpServer({ name: 'my-server' });
server.use(x402({
  stripeKey: process.env.STRIPE_SECRET_KEY,
  price: 0.01  // $0.01 per call
}));
```

### 3. Configure environment

```env
STRIPE_SECRET_KEY=sk_live_...
X402_WALLET=0x...
X402_PRICE=0.01
```

## Payment Flow

1. Agent calls your MCP tool
2. Server responds HTTP 402 with payment requirements
3. Agent's wallet automatically pays (Stripe or crypto)
4. Server validates payment and returns the result
5. You receive funds — no subscriptions, no monthly fees

## Token Format

Payments use the `X-PAYMENT` header with signed authorization tokens from Stripe Checkout Sessions or on-chain USDC transfers on Base network.

## MCP Integration

```json
{
  "mcpServers": {
    "my-monetized-server": {
      "command": "node",
      "args": ["server.js"],
      "env": {
        "STRIPE_SECRET_KEY": "${STRIPE_SECRET_KEY}",
        "X402_PRICE": "0.01"
      }
    }
  }
}
```
