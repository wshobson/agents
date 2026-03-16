# OCI Terraform Module Patterns

## VCN Module

- VCN with public/private subnets
- Dynamic Routing Gateway (DRG) attachments
- Internet Gateway, NAT Gateway, Service Gateway
- Route tables and security lists / NSGs
- VCN Flow Logs

## OKE Module

- OKE cluster and node pools
- IAM policies and dynamic groups
- VCN-native pod networking
- Cluster autoscaling and observability hooks
- OCIR integration

## Autonomous Database Module

- Autonomous Database provisioning
- Network access controls and private endpoints
- Wallet and secret handling
- Backup and maintenance preferences
- Tagging and cost tracking

## Object Storage Module

- Buckets with lifecycle rules
- Versioning and retention
- Customer-managed encryption keys
- Replication policies
- Event rules and service connectors

## Load Balancer Module

- Public or private load balancer
- Backend sets and listeners
- TLS certificates
- Health checks
- Logging and metrics integration

## Best Practices

1. Use the OCI provider version `~> 7.26`
2. Model compartments explicitly and pass them through module interfaces
3. Prefer NSGs over broad security list rules where practical
4. Tag all resources with owner, environment, and cost center metadata
5. Use dynamic groups and least-privilege IAM policies for workload access
6. Keep network, identity, and data modules loosely coupled
7. Expose OCIDs and subnet details for module composition
8. Enable logging, metrics, and backup settings by default
