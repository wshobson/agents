---
name: vk-cloud-products
description: Comprehensive VK Cloud product catalog covering Public Cloud, Private Cloud, VK S3, VK Kubernetes, VK Data Platform, VK Dev Platform, Bare Metal, and DBaaS. Use when designing solutions, comparing services, positioning VK Cloud capabilities, or mapping requirements to VK Cloud products.
---

# VK Cloud Products

## When to Use This Skill

- Designing cloud solutions using VK Cloud services
- Mapping customer requirements to VK Cloud products
- Comparing VK Cloud vs. AWS/Azure/GCP service portfolios
- Positioning VK Cloud capabilities in proposals
- Creating architecture diagrams with VK Cloud components
- Calculating pricing and sizing for VK Cloud deployments
- Answering "Does VK Cloud support..." questions

## VK Cloud Platform Overview

**VK Cloud** — российская облачная платформа, предоставляющая IaaS, PaaS, и managed services для enterprise customers. Основана на open standards (Kubernetes, S3 API, PostgreSQL) для избежания vendor lock-in.

**Core Value Proposition**:
1. **Data Sovereignty**: Data centers в России, compliance с 152-FZ
2. **Cost Advantage**: 30-40% ниже AWS/Azure/GCP
3. **No Sanctions Risk**: Российская компания, immune to geopolitical disruptions
4. **Open Standards**: Kubernetes, S3, PostgreSQL — no proprietary lock-in
5. **Enterprise-Grade**: Powers VK.com, Mail.ru (internet-scale infrastructure)

## Product Portfolio

### 1. Public Cloud (Публичное облако)

**Описание**: Shared multi-tenant infrastructure with pay-as-you-go pricing.

#### Compute (Вычислительные ресурсы)

**VM Instances (Виртуальные машины)**:

| Instance Type | vCPU | RAM | Use Case | Pricing (примерно) |
|---------------|------|-----|----------|---------------------|
| **General Purpose** | | | Balanced workloads | |
| gp.small | 1 | 2 GB | Development, small apps | ~₽2,500/mo |
| gp.medium | 2 | 4 GB | Web servers, apps | ~₽5,000/mo |
| gp.large | 4 | 8 GB | Larger apps, databases | ~₽10,000/mo |
| gp.xlarge | 8 | 16 GB | Enterprise apps | ~₽20,000/mo |
| **CPU-Optimized** | | | CPU-intensive workloads | |
| cpu.medium | 4 | 4 GB | Compute-heavy, batch processing | ~₽8,000/mo |
| cpu.large | 8 | 8 GB | HPC, encoding, simulations | ~₽16,000/mo |
| **Memory-Optimized** | | | Memory-intensive workloads | |
| mem.medium | 2 | 16 GB | Databases, caching, in-memory | ~₽12,000/mo |
| mem.large | 4 | 32 GB | Large databases, analytics | ~₽24,000/mo |
| **GPU Instances** | | | ML training, rendering | |
| gpu.small | 4 | 16 GB + NVIDIA T4 | ML inference, light training | ~₽50,000/mo |
| gpu.large | 8 | 32 GB + NVIDIA A100 | ML training, deep learning | ~₽200,000/mo |

**Features**:
- **Operating Systems**: Linux (Ubuntu, CentOS, Debian, AlmaLinux), Windows Server
- **Auto-Scaling**: Horizontal scaling with load balancers
- **Snapshots**: Point-in-time VM snapshots for backup/recovery
- **SSH/RDP Access**: Full root/admin access
- **Reserved Instances**: 1-year (20% discount), 3-year (40% discount)

**AWS Equivalent**: EC2 instances
**Azure Equivalent**: Virtual Machines
**GCP Equivalent**: Compute Engine

#### Storage (Хранилище)

**Block Storage (Блочные диски)**:

| Storage Type | Performance | Use Case | Pricing (примерно) |
|--------------|-------------|----------|---------------------|
| **SSD** | High IOPS (3000+) | Databases, transactional workloads | ~₽5/GB/mo |
| **HDD** | Standard IOPS (500) | Backups, archives, non-critical | ~₽2/GB/mo |
| **NVMe** | Ultra-high IOPS (10000+) | High-performance databases, latency-sensitive | ~₽10/GB/mo |

**Features**:
- **Persistent**: Data survives VM termination
- **Snapshots**: Incremental backups
- **Resizable**: Expand volumes without downtime
- **Encryption**: Optional encryption at rest

**AWS Equivalent**: EBS (Elastic Block Store)
**Azure Equivalent**: Managed Disks
**GCP Equivalent**: Persistent Disks

#### Networking (Сетевые сервисы)

**VPC (Virtual Private Cloud)**:
- **Private Networks**: Isolated network environments
- **Subnets**: Segment networks for security and organization
- **Security Groups**: Stateful firewall rules (allow/deny traffic)
- **Floating IPs**: Public IPs for internet access
- **Pricing**: Free (pay for bandwidth)

**Load Balancers**:
- **Layer 4 (TCP/UDP)**: Transport layer load balancing
- **Layer 7 (HTTP/HTTPS)**: Application layer with path/host routing
- **Health Checks**: Automated health monitoring
- **SSL/TLS Termination**: Offload SSL encryption
- **Pricing**: ~₽1,000/mo per LB

**VPN**:
- **Site-to-Site VPN**: Connect VK Cloud to on-premises data centers
- **IPsec**: Standard VPN protocol
- **Redundancy**: HA VPN gateways
- **Pricing**: ~₽3,000/mo per tunnel

**Direct Connect**:
- **Dedicated Connection**: Private, high-bandwidth link to VK Cloud
- **Bandwidth Options**: 1 Gbps, 10 Gbps
- **Low Latency**: Bypass public internet
- **Pricing**: ~₽50,000/mo (1 Gbps)

**Bandwidth Pricing**:
- **Ingress (Inbound)**: FREE ✅
- **Egress (Outbound)**: ~₽1/GB ✅ (AWS: ~₽8/GB = 8x cheaper)

**AWS Equivalent**: VPC, ELB, VPN Gateway, Direct Connect
**Azure Equivalent**: Virtual Network, Load Balancer, VPN Gateway, ExpressRoute
**GCP Equivalent**: VPC, Cloud Load Balancing, Cloud VPN, Cloud Interconnect

---

### 2. Private Cloud (Частное облако)

**Описание**: Dedicated single-tenant infrastructure for customers requiring enhanced isolation, compliance, or performance.

**Key Features**:
- **Dedicated Hardware**: Physical servers dedicated to single customer
- **Customization**: Tailored hardware configurations (CPU, RAM, storage)
- **Network Isolation**: Private VLANs, no shared networking
- **Compliance**: Meets strict regulatory requirements (finance, healthcare)
- **Hybrid Connectivity**: Seamless integration with VK Public Cloud
- **Dedicated Support**: Enhanced SLAs and dedicated support team

**Use Cases**:
- Regulated industries (banking, healthcare, government)
- High-performance workloads (databases, analytics)
- Sensitive data requiring physical isolation
- Predictable performance (no noisy neighbor)
- Hybrid cloud architectures

**Deployment Options**:
- **VK-Managed**: VK Cloud operates infrastructure in VK data centers
- **Customer Data Center**: VK Cloud deploys infrastructure in customer facility
- **Hybrid**: Combination of VK-managed and customer-managed

**Pricing**: Custom (depends on hardware configuration and commitment)

**AWS Equivalent**: AWS Outposts, Dedicated Hosts
**Azure Equivalent**: Azure Stack, Dedicated Host
**GCP Equivalent**: Anthos on-premises

---

### 3. VK S3 (Object Storage)

**Описание**: S3-compatible object storage для unstructured data (files, backups, media, data lakes).

**Key Features**:
- **S3-Compatible API**: Drop-in replacement for Amazon S3 (use AWS SDKs/tools)
- **Unlimited Scale**: Petabyte-scale storage
- **Durability**: 99.999999999% (11 nines) durability with erasure coding
- **Availability**: 99.95% availability SLA

**Storage Classes**:

| Storage Class | Access Pattern | Availability | Pricing (примерно) | Use Case |
|---------------|----------------|--------------|---------------------|----------|
| **Hot** | Frequent | 99.95% | ~₽1.50/GB/mo | Active data, data lakes, web content |
| **Cold** | Infrequent | 99.9% | ~₽0.50/GB/mo | Backups, archives (accessed monthly) |
| **Glacier** | Archive | 99% | ~₽0.20/GB/mo | Long-term archives (accessed yearly) |

**Features**:
- **Versioning**: Keep multiple versions of objects
- **Lifecycle Policies**: Auto-transition objects between storage classes
- **Server-Side Encryption**: AES-256 encryption at rest
- **Access Control**: Bucket policies, ACLs, IAM integration
- **CDN Integration**: Distribute content globally with low latency
- **Event Notifications**: Trigger actions on object changes (Kafka integration)
- **Multipart Upload**: Upload large files (>5GB) in parallel
- **Cross-Region Replication**: Replicate data across regions for DR

**Bandwidth Pricing**:
- **Egress**: ~₽1/GB ✅ (AWS S3: ~₽8/GB = 8x cheaper)
- **Ingress**: FREE

**API Compatibility**:
- ✅ AWS S3 API (PutObject, GetObject, ListBuckets, etc.)
- ✅ AWS CLI (`aws s3 ...` commands work directly)
- ✅ AWS SDKs (Boto3, AWS SDK for Java, etc.)
- ✅ Third-party tools (s3cmd, rclone, Cyberduck)

**Use Cases**:
- Data lakes (store raw data for analytics)
- Backup and disaster recovery
- Media storage (images, videos, documents)
- Log aggregation and archival
- Static website hosting
- ML dataset storage

**AWS Equivalent**: Amazon S3
**Azure Equivalent**: Azure Blob Storage
**GCP Equivalent**: Google Cloud Storage

---

### 4. VK Kubernetes (Managed Kubernetes)

**Описание**: Fully managed Kubernetes service для deploying, managing, and scaling containerized applications.

**Key Features**:
- **Free Control Plane**: ✅ $0/mo (AWS EKS: $73/mo per cluster)
- **Managed Masters**: VK Cloud manages Kubernetes masters (API server, etcd, scheduler)
- **Auto-Upgrades**: Automated Kubernetes version upgrades
- **Multi-Cluster**: Manage multiple K8s clusters from single dashboard
- **CNCF Certified**: 100% upstream Kubernetes (no vendor-specific modifications)

**Node Pools (Worker Nodes)**:
- **Flexible Configurations**: Choose any VM instance type (general purpose, CPU-optimized, GPU)
- **Auto-Scaling**: Horizontal Pod Autoscaler (HPA) and Cluster Autoscaler
- **Heterogeneous Nodes**: Mix instance types in same cluster (CPU + GPU nodes)
- **Node Pools**: Logical groups of nodes with same configuration

**Networking**:
- **CNI Plugin**: Calico for network policies
- **Load Balancers**: Automatic LoadBalancer provisioning for Services
- **Ingress Controllers**: NGINX Ingress, Traefik
- **Network Policies**: Micro-segmentation between pods

**Storage**:
- **Persistent Volumes**: Backed by VK Cloud Block Storage
- **Storage Classes**: SSD, HDD, NVMe options
- **Dynamic Provisioning**: Automatic PV creation
- **CSI Driver**: Container Storage Interface support

**Add-ons & Integrations**:
- **Monitoring**: Prometheus + Grafana (pre-installed)
- **Logging**: ELK stack (Elasticsearch, Logstash, Kibana)
- **Registry**: Integration with VK Container Registry
- **Helm**: Helm chart deployments
- **GitOps**: ArgoCD, Flux for CI/CD

**Pricing**:
- **Control Plane**: FREE ✅
- **Worker Nodes**: Standard VM pricing (e.g., gp.medium: ~₽5,000/mo per node)
- **Load Balancers**: ~₽1,000/mo per LB
- **Persistent Volumes**: Block storage pricing (~₽5/GB/mo for SSD)

**Use Cases**:
- Microservices architectures
- Containerized applications (Docker)
- CI/CD pipelines
- Batch processing and data pipelines
- ML model serving (inference)
- Hybrid cloud (portable across clouds)

**AWS Equivalent**: Amazon EKS
**Azure Equivalent**: Azure Kubernetes Service (AKS)
**GCP Equivalent**: Google Kubernetes Engine (GKE)

---

### 5. VK Data Platform (Managed Data Services)

**Описание**: Managed database and data processing services для analytics, transactional workloads, and event streaming.

#### ClickHouse (Analytical Database)

**Описание**: Columnar OLAP database для real-time analytics (analytical queries on massive datasets).

**Key Features**:
- **Real-Time Analytics**: Subsecond queries on billions of rows
- **Columnar Storage**: 100x faster than row-based databases for analytics
- **Compression**: 10x data compression (save storage costs)
- **Distributed**: Scale horizontally with sharding
- **SQL Interface**: Standard SQL queries
- **Integrations**: Kafka, S3, PostgreSQL, MySQL connectors

**Cluster Configurations**:

| Cluster Size | Nodes | Storage | Pricing (примерно) | Use Case |
|--------------|-------|---------|---------------------|----------|
| **Small** | 3 nodes | 1 TB each | ~₽30,000/mo | Startups, dev/test |
| **Medium** | 6 nodes | 2 TB each | ~₽100,000/mo | Medium-scale analytics |
| **Large** | 12+ nodes | 5 TB each | ~₽300,000/mo | Enterprise analytics |

**Performance**:
- **Queries/Second**: 1000s of analytical queries per second
- **Latency**: p95 < 1 second for complex aggregations
- **Throughput**: 100M+ rows/second ingestion

**Use Cases**:
- Real-time analytics dashboards
- Data warehousing (replace Greenplum, AWS Redshift)
- Log analytics (replace Elasticsearch for analytics)
- Time-series data (IoT, metrics, events)
- Business intelligence (Tableau, Power BI integration)

**Competitors**:
- **AWS Redshift**: ClickHouse is 10-100x faster, 50% lower cost
- **Google BigQuery**: ClickHouse comparable performance, 40% lower cost
- **Snowflake**: ClickHouse similar performance, 60% lower cost

**AWS Equivalent**: Amazon Redshift
**Azure Equivalent**: Azure Synapse Analytics
**GCP Equivalent**: Google BigQuery

#### PostgreSQL (Relational Database)

**Описание**: Managed PostgreSQL для transactional workloads (OLTP).

**Key Features**:
- **High Availability**: Multi-AZ with automatic failover
- **Automated Backups**: Daily backups with point-in-time recovery (PITR)
- **Read Replicas**: Scale read workloads horizontally
- **Monitoring**: Built-in Prometheus metrics and Grafana dashboards
- **Auto-Scaling Storage**: Automatically expand storage

**Configurations**:

| Configuration | vCPU | RAM | Storage | Pricing (примерно) | Use Case |
|---------------|------|-----|---------|---------------------|----------|
| **Small** | 2 | 4 GB | 100 GB | ~₽8,000/mo | Small apps, dev/test |
| **Medium** | 4 | 16 GB | 500 GB | ~₽25,000/mo | Production apps |
| **Large** | 8 | 64 GB | 2 TB | ~₽80,000/mo | Large-scale apps |

**PostgreSQL Versions**: 12, 13, 14, 15, 16 (latest)

**Use Cases**:
- Transactional applications (e-commerce, SaaS)
- Content management systems (CMS)
- ERP, CRM systems
- Geospatial applications (PostGIS extension)

**AWS Equivalent**: Amazon RDS for PostgreSQL
**Azure Equivalent**: Azure Database for PostgreSQL
**GCP Equivalent**: Cloud SQL for PostgreSQL

#### MongoDB (NoSQL Document Database)

**Описание**: Managed MongoDB для document-based data storage.

**Key Features**:
- **Document Model**: Flexible schema for JSON-like documents
- **Replication**: Multi-node replica sets for HA
- **Sharding**: Horizontal scaling for massive datasets
- **Automated Backups**: Daily backups with restore

**Use Cases**:
- Content management (catalogs, user profiles)
- Mobile/web applications (flexible schema)
- IoT data storage
- Real-time analytics

**AWS Equivalent**: Amazon DocumentDB
**Azure Equivalent**: Azure Cosmos DB (MongoDB API)
**GCP Equivalent**: MongoDB Atlas (third-party on GCP)

#### Redis (In-Memory Cache)

**Описание**: Managed Redis для caching and session storage.

**Key Features**:
- **In-Memory**: Microsecond latency
- **Persistence Options**: AOF (append-only file), RDB (snapshots)
- **High Availability**: Redis Sentinel for automatic failover
- **Data Structures**: Strings, hashes, lists, sets, sorted sets, bitmaps

**Use Cases**:
- Application caching (reduce database load)
- Session storage (web apps)
- Leaderboards and counters
- Real-time messaging (Pub/Sub)

**AWS Equivalent**: Amazon ElastiCache for Redis
**Azure Equivalent**: Azure Cache for Redis
**GCP Equivalent**: Memorystore for Redis

#### Apache Kafka (Event Streaming Platform)

**Описание**: Managed Kafka для event streaming and message queuing.

**Key Features**:
- **High Throughput**: Millions of events/second
- **Durability**: Replicated, persistent event log
- **Scalability**: Add brokers to scale horizontally
- **Retention**: Configurable event retention (hours to forever)

**Use Cases**:
- Real-time data pipelines (ETL)
- Event-driven architectures (microservices)
- Log aggregation
- Stream processing (Kafka Streams, Flink)

**AWS Equivalent**: Amazon MSK (Managed Streaming for Kafka)
**Azure Equivalent**: Azure Event Hubs (Kafka-compatible)
**GCP Equivalent**: Confluent Cloud on GCP

#### Tarantool (In-Memory Database)

**Описание**: In-memory database с Lua scripting и ACID transactions.

**Key Features**:
- **In-Memory + Persistent**: Data in RAM with disk persistence
- **ACID Transactions**: Full ACID compliance
- **Lua Scripting**: Stored procedures in Lua
- **Replication**: Master-slave and multi-master replication

**Use Cases**:
- High-performance transactional workloads
- Real-time applications (gaming, fintech)
- Caching with complex logic
- Geospatial applications

---

### 6. VK Dev Platform (Developer Tools)

**Описание**: Managed development and CI/CD tools.

#### GitLab (Source Control & CI/CD)

**Key Features**:
- **Git Repositories**: Unlimited private repositories
- **CI/CD Pipelines**: GitLab CI for automated testing and deployment
- **Container Registry**: Private Docker registry
- **Issue Tracking**: Project management and bug tracking
- **Code Review**: Merge requests with code review

**Pricing**: ~₽5,000/mo per user (примерно)

**Use Cases**:
- Source control (Git)
- CI/CD automation
- DevOps workflows
- Container image management

**AWS Equivalent**: AWS CodeCommit + CodePipeline + ECR
**Azure Equivalent**: Azure DevOps + Azure Container Registry
**GCP Equivalent**: Cloud Source Repositories + Cloud Build + Artifact Registry

#### Container Registry

**Key Features**:
- **Docker/OCI Images**: Store and manage container images
- **Private Registry**: Secure, private image storage
- **Integration**: Works with VK Kubernetes, GitLab CI
- **Vulnerability Scanning**: Scan images for security vulnerabilities

---

### 7. Bare Metal (Dedicated Servers)

**Описание**: Physical servers without virtualization overhead for maximum performance.

**Server Configurations**:

| Type | CPU | RAM | Storage | Pricing (примерно) | Use Case |
|------|-----|-----|---------|---------------------|----------|
| **CPU-Optimized** | Dual Xeon (32 cores) | 128 GB | 2 TB NVMe | ~₽30,000/mo | Databases, HPC |
| **GPU-Optimized** | Dual Xeon + 8x NVIDIA A100 | 256 GB | 4 TB NVMe | ~₽500,000/mo | ML training, rendering |
| **Storage-Optimized** | Dual Xeon | 64 GB | 20 TB HDD | ~₽40,000/mo | Data warehouses, big data |

**Key Features**:
- **Full Control**: Root access, custom OS, kernel tuning
- **No Virtualization Overhead**: Maximum performance
- **Custom Networking**: VLAN, bonding, SR-IOV
- **Dedicated Resources**: No noisy neighbors

**Use Cases**:
- High-performance databases (PostgreSQL, MySQL, Oracle)
- ML model training (GPUs required)
- HPC workloads (scientific computing)
- Latency-sensitive applications

**AWS Equivalent**: AWS Bare Metal (i3.metal, c5.metal)
**Azure Equivalent**: Azure Dedicated Host
**GCP Equivalent**: Sole-tenant nodes

---

### 8. DBaaS (Database as a Service)

Unified managed database offering covering all database types mentioned above:
- PostgreSQL
- MySQL (if available)
- MongoDB
- Redis
- ClickHouse
- Tarantool

**Unified Features Across All DBaaS**:
- **High Availability**: Multi-AZ deployment with automatic failover
- **Automated Backups**: Daily backups with point-in-time recovery
- **Monitoring**: Prometheus + Grafana dashboards
- **Scaling**: Vertical (resize instance) and horizontal (read replicas, sharding)
- **Security**: Encryption at rest and in transit, network isolation
- **Patch Management**: Automated security and version updates

---

## Service Comparison Matrix

### VK Cloud vs. AWS

| VK Cloud Service | AWS Equivalent | Key Difference |
|------------------|----------------|----------------|
| VM Instances | EC2 | Similar features, 20-30% lower cost |
| Block Storage | EBS | Similar performance, lower cost |
| VK S3 | Amazon S3 | S3-compatible API, 8x cheaper egress |
| VK Kubernetes | EKS | FREE control plane (EKS: $73/mo) |
| ClickHouse | Redshift | 10-100x faster, 50% lower cost |
| PostgreSQL DBaaS | RDS PostgreSQL | Similar features, competitive pricing |
| MongoDB DBaaS | DocumentDB | Standard MongoDB vs. AWS fork |
| Redis DBaaS | ElastiCache | Similar features |
| Kafka | MSK | Similar features |
| Load Balancer | ELB | Similar features |
| VPN | VPN Gateway | Similar features |

**VK Cloud Advantages**:
- ✅ Free Kubernetes control plane (save $876/year per cluster)
- ✅ 8x cheaper egress (massive savings for data-intensive apps)
- ✅ Data sovereignty (152-FZ compliance)
- ✅ No sanctions risk
- ✅ Local support (Russian language, Moscow timezone)

**AWS Advantages**:
- More global regions (25+ vs. Russia-focused)
- Broader service portfolio (200+ services vs. ~30)
- Larger ecosystem (ISVs, SIs, training)

---

## Product Roadmap (Future Services)

**Expected in 2024-2025**:
- **Serverless Functions**: AWS Lambda equivalent
- **Managed MySQL**: DBaaS for MySQL
- **Managed Elasticsearch**: For search and log analytics
- **GPU-as-a-Service**: On-demand GPU instances for ML
- **API Gateway**: Managed API gateway for microservices
- **Service Mesh**: Istio/Envoy managed service mesh

**Request from Sales**: If customer needs service not yet available, escalate to product team for roadmap visibility.

---

## Key Principles for Solution Design

1. **Open Standards First**: Prioritize Kubernetes, S3, PostgreSQL—avoid proprietary lock-in
2. **Managed Services Over DIY**: Use DBaaS, Kubernetes vs. self-hosted (reduce ops burden)
3. **Cost Optimization**: Leverage free K8s control plane, cheap egress, reserved instances
4. **Hybrid When Needed**: Private Cloud for sensitive data + Public Cloud for scalability
5. **Data Sovereignty**: Ensure all data stays in Russia for 152-FZ compliance
6. **Multi-AZ HA**: Always design for high availability (multi-AZ databases, load balancers)
7. **Security by Design**: Encryption, network isolation, least privilege
8. **Cloud-Native Patterns**: Immutable infrastructure, declarative config, auto-scaling

---

## References

- **VK Cloud Documentation**: https://mcs.mail.ru/docs/ (official docs)
- **Pricing Calculator**: https://mcs.mail.ru/app/services/infra/ (estimate costs)
- **API Reference**: https://mcs.mail.ru/docs/ru/api (API docs for automation)
- **S3 API Compatibility**: https://mcs.mail.ru/docs/ru/base/s3/s3-api (S3 compatibility matrix)
- **Kubernetes Docs**: https://mcs.mail.ru/docs/ru/base/k8s/ (VK Kubernetes guide)

For latest pricing, features, and roadmap—contact VK Cloud product team or reference official documentation.
