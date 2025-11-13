# Complete Terraform Manifest Example for VK Cloud Marketplace
# Service: Grafana with monitoring, backups, and auto-recovery
# Based on official VK Cloud documentation

# ============================================================================
# VARIABLES
# ============================================================================

# Special variables (provided by deployment system)
variable "instance_uuid" {
  type        = string
  default     = "4a57a965-3c83-436c-80e2-428e421538cc"
  description = "Deployment ID for ivkcs resources"
}

variable "email" {
  type        = string
  default     = "user@example.com"
  description = "User email for notifications and certificates"
}

# External variables (user-configurable from tariff plan options)
variable "grafana_placement" {
  type        = string
  default     = "internal"
  description = "Placement: internal or external IP"
}

variable "backup_style" {
  type        = string
  default     = "s3"
  description = "Backup method: s3 or none"
}

# Infrastructure variables
variable "ds-az" {
  type        = string
  default     = "GZ1"
  description = "Availability zone"
}

variable "ds-flavor" {
  type        = string
  default     = "a493b27d-170d-48eb-a24b-99e9b325f988"
  description = "VM flavor UUID"
}

variable "ds-subnet" {
  type        = string
  default     = "cd4224ac-0527-4291-a8e0-afae0cee02ed"
  description = "Subnet UUID"
}

# Storage variables
variable "root_type" {
  type        = string
  default     = "ceph-ssd"
  description = "Root disk type"
}

variable "root_size" {
  type        = number
  default     = 10
  description = "Root disk size in GB"
}

variable "data_type" {
  type        = string
  default     = "ceph-ssd"
  description = "Data disk type"
}

variable "data_size" {
  type        = number
  default     = 1
  description = "Data disk size in GB"
}

# Image variable
variable "image_uuid" {
  type        = string
  default     = "8c7a6443-bb79-4f04-884a-14231f0ba6cb"
  description = "Service image UUID"
}

# Security group ports
variable "ports" {
  type        = list(number)
  default     = [22, 80, 443]
  description = "Ports for security group rules"
}

# Locals for computed values
locals {
  short_name     = substr(var.instance_uuid, 0, 8)
  hosts_name     = "${local.short_name}-grafana"
  grafana_domain = var.grafana_placement == "external" ? "${ivkcs_dns.grafana[0].name}.${ivkcs_dns.grafana[0].domain}" : vkcs_compute_instance.grafana.access_ip_v4
  grafana_root_url = var.grafana_placement == "external" ? "https://${local.grafana_domain}" : "http://${local.grafana_domain}"
}

# ============================================================================
# DATA SOURCES
# ============================================================================

# Get subnet information
data "vkcs_networking_subnet" "subnet" {
  subnet_id = var.ds-subnet
}

# Example: Validate flavor exists
# data "vkcs_compute_flavor" "compute" {
#   flavor_id = var.ds-flavor
# }

# ============================================================================
# S3 BACKUP (ivkcs provider)
# ============================================================================

# Create S3 bucket for backups
resource "ivkcs_s3" "s3_backup" {
  count = var.backup_style == "s3" ? 1 : 0
  name  = "${local.hosts_name}-backup"
}

# ============================================================================
# SECURITY GROUP
# ============================================================================

# Create security group
resource "vkcs_networking_secgroup" "secgroup" {
  name = "${local.short_name}-grafana"
  sdn  = data.vkcs_networking_subnet.subnet.sdn
}

# Create security group rules for each port
resource "vkcs_networking_secgroup_rule" "rules" {
  count             = length(var.ports)
  direction         = "ingress"
  port_range_max    = element(var.ports, count.index)
  port_range_min    = element(var.ports, count.index)
  protocol          = "tcp"
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = vkcs_networking_secgroup.secgroup.id
  description       = "rule_tcp_${element(var.ports, count.index)}"
}

# ============================================================================
# NETWORK
# ============================================================================

# Attach IP to port
resource "vkcs_networking_port" "ports" {
  name               = "${local.short_name}-grafana"
  admin_state_up     = "true"
  network_id         = data.vkcs_networking_subnet.subnet.network_id
  sdn                = data.vkcs_networking_subnet.subnet.sdn
  security_group_ids = [vkcs_networking_secgroup.secgroup.id]

  fixed_ip {
    subnet_id = var.ds-subnet
  }
}

# ============================================================================
# SSH KEYPAIR (ivkcs provider)
# ============================================================================

# Auto-generate SSH key pair
resource "ivkcs_ssh_keypair" "keypair" {}

# ============================================================================
# CLOUD-INIT CONFIGURATION (ivkcs provider)
# ============================================================================

# Generate cloud-config for agent initialization
resource "ivkcs_user_data" "user_data" {
  uuid      = var.instance_uuid
  hosts     = [local.hosts_name]
  target_os = "almalinux9"  # or ubuntu2204, debian11, etc.

  ssh_authorized_keys = [
    ivkcs_ssh_keypair.keypair.public_key,
  ]
}

# ============================================================================
# VOLUMES
# ============================================================================

# Create boot volume from image
resource "vkcs_blockstorage_volume" "boot" {
  name              = "${local.short_name}-grafana-boot"
  metadata          = { "sid" : "xaas", "product" : "grafana" }
  image_id          = var.image_uuid
  volume_type       = var.root_type
  size              = var.root_size
  availability_zone = var.ds-az
}

# Create data volume
resource "vkcs_blockstorage_volume" "grafana_data" {
  name              = "${local.short_name}-grafana-data"
  metadata          = { "sid" : "xaas", "product" : "grafana" }
  size              = var.data_size
  availability_zone = var.ds-az
  volume_type       = var.data_type
}

# ============================================================================
# COMPUTE INSTANCE
# ============================================================================

# Create VM instance
resource "vkcs_compute_instance" "grafana" {
  name              = local.hosts_name
  flavor_id         = var.ds-flavor
  security_groups   = [vkcs_networking_secgroup.secgroup.name]
  availability_zone = var.ds-az
  metadata          = { "sid" : "xaas", "product" : "grafana" }

  # Boot from volume
  block_device {
    source_type      = "volume"
    destination_type = "volume"
    boot_index       = 0
    uuid             = vkcs_blockstorage_volume.boot.id
  }

  # Apply cloud-config for agent installation
  user_data = ivkcs_user_data.user_data.user_data[0]

  # Attach network port
  network {
    port = vkcs_networking_port.ports.id
  }

  # Graceful shutdown before destroy
  stop_before_destroy = true

  # Timeout for instance creation
  timeouts {
    create = "10m"
  }
}

# Attach data volume to instance
resource "vkcs_compute_volume_attach" "attached" {
  instance_id = vkcs_compute_instance.grafana.id
  volume_id   = vkcs_blockstorage_volume.grafana_data.id
}

# ============================================================================
# EXTERNAL IP AND DNS (conditional)
# ============================================================================

# Allocate floating IP if external placement
resource "vkcs_networking_floatingip" "fips" {
  count = var.grafana_placement == "external" ? 1 : 0
  pool  = data.vkcs_networking_subnet.subnet.sdn == "neutron" ? "ext-net" : "internet"
}

# Associate floating IP with instance
resource "vkcs_compute_floatingip_associate" "fip" {
  count       = length(vkcs_networking_floatingip.fips)
  floating_ip = vkcs_networking_floatingip.fips[count.index].address
  instance_id = vkcs_compute_instance.grafana.id
}

# Create DNS A-record in VK Cloud DNS (ivkcs provider)
resource "ivkcs_dns" "grafana" {
  count  = length(vkcs_networking_floatingip.fips)
  name   = "grafana-${local.short_name}"
  domain = "xaas.msk.vkcs.cloud"
  ip     = vkcs_networking_floatingip.fips[count.index].address
}

# ============================================================================
# AGENT SCRIPT EXECUTION (ivkcs provider)
# ============================================================================

# Startup script configuration
locals {
  start = <<-EOT
#!/bin/bash
ansible-playbook start.yml \
  --extra-vars "lego_enabled=${var.grafana_placement == "external" ? "true" : "false"}" \
  --extra-vars "lego_email=${var.email}" \
  --extra-vars "backup_enabled=${var.backup_style == "s3" ? "true" : "false"}" \
  --extra-vars "backup_access_token=${try(ivkcs_s3.s3_backup[0].access, "n/a")}" \
  --extra-vars "backup_secret_token=${try(ivkcs_s3.s3_backup[0].secret, "n/a")}" \
  --extra-vars "backup_bucket_name=${try(ivkcs_s3.s3_backup[0].name, "n/a")}_bucket" \
  --extra-vars "grafana_domain=${local.grafana_domain}" \
  --extra-vars "grafana_root_url=${local.grafana_root_url}"
EOT
}

# Execute startup script via agent
resource "ivkcs_agent_exec" "start" {
  hosts = [local.hosts_name]
  name  = "start_grafana"
  uuid  = var.instance_uuid

  # Multi-step execution
  step {
    index   = 1
    type    = "bash"  # or "python"
    content = local.start
    options {
      timeout  = "20m"      # Execution timeout
      cwd      = "/opt/playbooks"  # Working directory
      attempts = 1         # Retry attempts
    }
  }

  # Wait for instance and volume
  depends_on = [
    vkcs_compute_instance.grafana,
    vkcs_compute_volume_attach.attached,
  ]
}

# ============================================================================
# HEALTH CHECK AND MONITORING (ivkcs provider)
# ============================================================================

# Configure health monitoring
resource "ivkcs_agent_check" "health" {
  hosts = [local.hosts_name]
  uuid  = var.instance_uuid

  # HTTP health check configuration
  http_health {
    method     = "GET"
    protocol   = var.grafana_placement == "internal" ? "http" : "https"
    host       = local.grafana_domain
    path       = "/api/health"
    http_codes = [200]  # Expected HTTP codes
    period     = "30s"  # Check interval
  }

  timeouts {
    create = "5m"
  }

  # Wait for startup script completion
  depends_on = [
    ivkcs_agent_exec.start,
  ]
}

# ============================================================================
# OUTPUTS
# ============================================================================

# Output private SSH key (sensitive)
output "keypair" {
  value     = ivkcs_ssh_keypair.keypair.private_key
  sensitive = true
  description = "SSH private key for instance access"
}

# Output Grafana URL
output "grafana_url" {
  value = local.grafana_root_url
  description = "Grafana web interface URL"
}

# Output S3 backup bucket ID
output "s3_backup" {
  value = try(ivkcs_s3.s3_backup[0].id, "n/a")
  description = "S3 backup bucket ID"
}

# ============================================================================
# ADDITIONAL ivkcs PROVIDER EXAMPLES
# ============================================================================

# Example: VM reboot during deployment
# resource "ivkcs_compute_instance_reboot" "reboot" {
#   instance_id = vkcs_compute_instance.grafana.id
#   depends_on = [ivkcs_agent_exec.start]
# }

# Example: Get script execution result
# data "ivkcs_agent_script_result" "result" {
#   uuid = var.instance_uuid
#   host = local.hosts_name
#   name = "start_grafana"
# }

# Example: Monitoring user
# resource "ivkcs_monitoring_user" "monitor" {
#   uuid = var.instance_uuid
#   hosts = [local.hosts_name]
#   username = "monitoring"
#   password = random_password.monitor.result
# }

# Example: Multi-step agent execution
# resource "ivkcs_agent_exec" "multi_step" {
#   hosts = [local.hosts_name]
#   name  = "complex_setup"
#   uuid  = var.instance_uuid
#
#   step {
#     index = 1
#     type  = "bash"
#     content = "echo 'Step 1'"
#     options {
#       timeout = "5m"
#       cwd = "/tmp"
#     }
#   }
#
#   step {
#     index = 2
#     type  = "python"
#     content = "print('Step 2')"
#     options {
#       timeout = "10m"
#       attempts = 3
#     }
#   }
# }
