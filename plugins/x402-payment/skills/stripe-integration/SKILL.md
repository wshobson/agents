---
name: stripe-integration
description: Configure Stripe billing for x402 payment protocol — products, prices, webhooks, and checkout flows for pay-per-call AI agent APIs.
---

# Stripe Integration for x402

Configure Stripe as the fiat payment rail for your x402-enabled MCP server.

## Prerequisites

- Stripe account (live or test mode)
- x402 server running

## Setup

### 1. Create a Stripe product

Each MCP tool maps to a Stripe product with a per-unit price.

### 2. Configure webhooks

```bash
stripe listen --forward-to localhost:3000/x402/webhook
```

Add your webhook signing secret to env:
```env
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 3. Test with test card

```
Card: 4242 4242 4242 4242
Exp: 12/34
CVC: 123
```

## Pricing Models

| Model | Description | Example |
|-------|-------------|---------|
| Per-call | Pay per tool invocation | $0.01/tool |
| Token-based | Pay per token consumed | $0.001/1K tokens |
| Tiered | Different prices for different tools | $0.01 for basic, $0.10 for premium |
| Bundle | Pre-paid call bundles | $1 for 100 calls |

## Troubleshooting

- **Webhook not received**: Check Stripe Dashboard webhook delivery logs
- **Payment not validating**: Verify webhook secret matches your env
- **Price mismatch**: Ensure Stripe price ID matches x402 config
