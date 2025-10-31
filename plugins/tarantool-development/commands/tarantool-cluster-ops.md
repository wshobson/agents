# Tarantool Cluster Setup & Operations

Setup and operate production Tarantool clusters with high availability and disaster recovery:

[Extended thinking: This command covers complete cluster setup from single-instance to multi-region distributed clusters using both Cartridge and vshard. It includes topology design, replication configuration, backup/restore procedures, monitoring, and operational procedures for production environments.]

## Language Support

All outputs adapt to the input language:
- **Russian input** → **Russian response**
- **English input** → **English response**
- **Mixed input** → Response in the language of the primary content
- **Technical terms, code, and system names** maintain their original form

This command works seamlessly in both languages.

## Configuration Options

### Cluster Type
- **single-instance**: Single Tarantool instance (development)
- **replicated**: Master-slave or master-master replication
- **cartridge**: Multi-role cluster with Cartridge
- **sharded**: Distributed cluster with vshard
- **multi-region**: Multi-region cluster with replication

### Cloud Provider
- **on-premises**: Self-managed infrastructure
- **aws**: Amazon AWS (EC2, RDS Aurora)
- **azure**: Microsoft Azure
- **gcp**: Google Cloud Platform
- **kubernetes**: Kubernetes with Operator

### HA Strategy
- **passive-failover**: Manual failover (no automation)
- **active-failover**: Automatic failover (Cartridge)
- **distributed-ha**: HA across multiple regions

## Phase 1: Planning & Design

1. **Capacity Planning**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Plan Tarantool cluster capacity for: $ARGUMENTS. Estimate storage needs, throughput requirements, memory footprint. Design for growth. Plan for redundancy and failover."
   - Expected output: Capacity plan with hardware requirements

2. **Cluster Architecture**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Design cluster architecture for: $ARGUMENTS. Type: $CLUSTER_TYPE. Cloud: $CLOUD_PROVIDER. Design topology with master/slave or shard replicas. Plan for $HA_STRATEGY. Include network topology and security."
   - Expected output: Cluster architecture with topology diagrams

3. **Backup & Recovery Strategy**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Design backup and recovery for: $ARGUMENTS. Plan RTO and RPO targets. Design backup procedures (snapshots, WAL archival). Plan for point-in-time recovery. Document recovery procedures."
   - Expected output: Backup strategy with recovery procedures

## Phase 2: Implementation

4. **Cluster Configuration**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Configure Tarantool cluster for: $ARGUMENTS. Create configuration files. Setup replication for topology: [include design]. Configure vshard if sharding. Setup WAL and durability settings."
   - Expected output: Complete cluster configuration

5. **Replication Setup**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Setup replication for: $ARGUMENTS. Configure replication topology. Setup replicas. Verify replication working. Document replication monitoring."
   - Expected output: Replication configuration and verification

6. **Container & Orchestration**
   - Use Task tool with subagent_type="kubernetes-operations::kubernetes-architect"
   - Prompt: "Setup Tarantool containers for: $ARGUMENTS. If cloud: $CLOUD_PROVIDER. Create Docker images. Setup Kubernetes Operator if needed. Configure persistent volumes for data."
   - Expected output: Container configuration and orchestration setup

7. **Monitoring & Observability**
   - Use Task tool with subagent_type="observability-monitoring::observability-engineer"
   - Prompt: "Setup monitoring for Tarantool cluster: $ARGUMENTS. Configure Prometheus metrics collection. Setup Grafana dashboards. Configure alerting for replication lag, memory usage, failover events. Create runbooks."
   - Expected output: Monitoring configuration and dashboards

## Phase 3: Validation & Operations

8. **Disaster Recovery Testing**
   - Use Task tool with subagent_type="tarantool-development::tarantool-architect"
   - Prompt: "Plan disaster recovery testing for: $ARGUMENTS. Create DR test procedures. Test node failures, network partitions, data corruption. Document RTO/RPO verification. Create recovery runbooks."
   - Expected output: DR testing procedures and runbooks

9. **Operational Documentation**
   - Use Task tool with subagent_type="documentation-generation::docs-architect"
   - Prompt: "Generate operational documentation for: $ARGUMENTS. Create cluster setup guide, operational procedures, troubleshooting guide, backup/recovery guide, scaling procedures, monitoring guide."
   - Expected output: Complete operational documentation

10. **Deployment Automation**
    - Use Task tool with subagent_type="cicd-automation::deployment-engineer"
    - Prompt: "Create deployment automation for: $ARGUMENTS. Setup cluster deployment scripts. Create configuration management. Automate backup scheduling. Setup rolling updates for zero-downtime maintenance."
    - Expected output: Deployment automation and scripts

## Execution Parameters

### Required
- **--cluster-name**: Cluster name and environment
- **--cluster-type**: Type of cluster (single-instance|replicated|cartridge|sharded|multi-region)
- **--environment**: Environment (development|staging|production)

### Optional
- **--cloud-provider**: Cloud platform (on-premises|aws|azure|gcp|kubernetes) - default: on-premises
- **--ha-strategy**: HA approach (passive-failover|active-failover|distributed-ha) - default: active-failover
- **--backup-retention-days**: Backup retention period - default: 30
- **--enable-sharding**: Enable vshard (true|false) - default: false
- **--replication-mode**: Replication (master-slave|master-master) - default: master-slave
- **--shard-count**: Number of shards (if sharding) - default: 3

## Success Criteria

- Cluster deployed and operational
- Replication configured and verified
- Backups automated and tested
- Monitoring and alerting operational
- Failover tested and working
- Documentation complete
- Team trained on operations

## Example Clusters

1. **Single-Instance Development**
   - One Tarantool instance
   - Memtx storage
   - No replication

2. **Replicated Production**
   - Master + 2 replicas
   - Automated failover
   - Continuous backups

3. **Multi-Region Cluster**
   - Sharding with vshard
   - Multi-master replication
   - Automatic rebalancing

Tarantool cluster setup for: $ARGUMENTS
