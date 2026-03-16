# Multi-Cloud Service Comparison

## Compute

| Use Case | AWS | Azure | GCP | OCI |
| -------- | --- | ----- | --- | --- |
| General-purpose VMs | EC2 | Virtual Machines | Compute Engine | Compute |
| Managed Kubernetes | EKS | AKS | GKE | OKE |
| Serverless functions | Lambda | Functions | Cloud Functions | Functions |
| Containers without cluster management | ECS/Fargate | Container Apps / Container Instances | Cloud Run | Container Instances |

## Storage

| Use Case | AWS | Azure | GCP | OCI |
| -------- | --- | ----- | --- | --- |
| Object storage | S3 | Blob Storage | Cloud Storage | Object Storage |
| Block storage | EBS | Managed Disks | Persistent Disk | Block Volumes |
| File storage | EFS | Azure Files | Filestore | File Storage |
| Archive storage | Glacier / Deep Archive | Archive Storage | Archive Storage | Archive Storage |

## Data Services

| Use Case | AWS | Azure | GCP | OCI |
| -------- | --- | ----- | --- | --- |
| Managed relational database | RDS | SQL Database | Cloud SQL | MySQL HeatWave |
| Distributed / globally resilient SQL | Aurora Global Database | Cosmos DB for PostgreSQL / SQL patterns | Cloud Spanner | Autonomous Database |
| NoSQL | DynamoDB | Cosmos DB | Firestore | NoSQL Database |
| Streaming | Kinesis / MSK | Event Hubs | Pub/Sub / Confluent | Streaming |

## Platform Selection Notes

1. Prefer provider-native managed services when team expertise and lock-in tolerance are high.
2. Prefer Kubernetes, PostgreSQL, Redis, and open observability stacks when portability matters.
3. Use OCI when Oracle database affinity, predictable networking, or regulated workload isolation are primary drivers.
4. Compare egress, managed service premiums, and support plans before splitting workloads across providers.
