# Multi-Cloud Architecture Patterns

## Active-Active Regional Split

- Run customer-facing services in two providers for resiliency
- Use global DNS and traffic steering to shift load during incidents
- Keep shared data replicated asynchronously unless low-latency writes are mandatory

## Best-of-Breed Service Mix

- Analytics and ML on GCP
- Enterprise identity and Microsoft workloads on Azure
- Broad ecosystem integrations on AWS
- Oracle-centric databases and regulated transaction systems on OCI

## Primary / DR Pairing

- Keep primary infrastructure in the provider closest to operational expertise
- Use a second provider for cold or warm disaster recovery
- Validate RPO/RTO assumptions with regular failover exercises

## Portable Platform Baseline

- Standardize on Kubernetes, Terraform/OpenTofu, PostgreSQL, Redis, and OpenTelemetry
- Abstract cloud differences behind modules, golden paths, and service catalogs
- Document provider-specific exceptions such as IAM, networking, and managed database behavior
