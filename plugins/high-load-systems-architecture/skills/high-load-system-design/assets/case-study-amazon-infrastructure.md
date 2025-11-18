# Amazon Infrastructure Case Study

## Scale
- 300M+ customers
- 1.6M transactions/sec (Prime Day)
- 200+ AWS services
- Global infrastructure

## Architecture Principles

### Service-Oriented Architecture
- Two-pizza teams (< 10 people)
- Services own their data
- API-first design

### Everything Fails All the Time
- Design for failure
- Redundancy at every layer
- Graceful degradation

## Key Technologies

### DynamoDB
- Fully managed NoSQL
- 20M+ requests/sec
- Single-digit millisecond latency
- Auto-scaling

### SQS (Simple Queue Service)
- Decouples components
- Handles traffic spikes
- At-least-once delivery
- Dead letter queues

### CloudFront CDN
- Global edge network
- Low latency content delivery
- DDoS protection

## Lessons Learned
- Microservices for agility
- Automation at scale
- Data-driven decisions
- Customer obsession
