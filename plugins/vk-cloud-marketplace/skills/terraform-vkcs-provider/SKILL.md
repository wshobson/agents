---
name: terraform-vkcs-provider
description: Complete guide to VK Cloud Terraform provider (vkcs) for infrastructure as code. Use when creating Terraform configurations, managing VK Cloud resources, or building marketplace deployment manifests.
---

# Terraform VK Cloud Provider (vkcs)

## When to Use This Skill

- Writing Terraform configurations for VK Cloud infrastructure
- Creating deployment manifests for marketplace applications
- Managing compute, network, storage, and database resources
- Implementing infrastructure as code for VK Cloud
- Troubleshooting Terraform provider issues
- Understanding VKCS resource types and their relationships

## Core Concepts

### Provider Overview

The VK Cloud Terraform provider (`vk-cs/vkcs`) enables declarative infrastructure management for VK Cloud platform using Terraform.

**Key Facts:**
- **Provider Source**: `vk-cs/vkcs`
- **Minimum Terraform Version**: 1.1.5+
- **Latest Version**: Available on [Terraform Registry](https://registry.terraform.io/providers/vk-cs/vkcs/latest)
- **GitHub Repository**: https://github.com/vk-cs/terraform-provider-vkcs
- **SDN Support**: Both Neutron and Sprut

### Provider Configuration

**Basic Configuration:**
```hcl
terraform {
  required_providers {
    vkcs = {
      source  = "vk-cs/vkcs"
      version = "~> 0.8.0"
    }
  }
  required_version = ">= 1.1.5"
}

provider "vkcs" {
  username   = var.username
  password   = var.password
  project_id = var.project_id
  region     = "RegionOne"
}
```

**Authentication Methods:**

1. **Via Configuration File** (recommended for marketplace):
   - Download from VK Cloud portal: Project → Terraform tab → "Download VKCS provider file"
   - Contains pre-filled `username`, `password`, `project_id`

2. **Environment Variables**:
   ```bash
   export OS_USERNAME="user@example.com"
   export OS_PASSWORD="password"
   export OS_PROJECT_ID="project-id"
   export OS_REGION_NAME="RegionOne"
   ```

3. **Direct in Provider Block** (not recommended for production):
   ```hcl
   provider "vkcs" {
     username   = "user@example.com"
     password   = "sensitive_password"
     project_id = "abc123"
   }
   ```

**Provider Arguments:**
- `username` (required): VK Cloud account email
- `password` (required): Account password or application credential
- `project_id` (required): Project UUID from VK Cloud portal
- `region` (optional): Default "RegionOne"
- `auth_url` (optional): Custom authentication endpoint

## Resource Categories

### Compute Resources

#### vkcs_compute_instance

Creates and manages virtual machines.

**Basic VM Example:**
```hcl
resource "vkcs_compute_instance" "basic" {
  name              = "vm-tf-example"
  flavor_id         = "your-flavor-id"
  availability_zone = "GZ1"

  block_device {
    source_type      = "image"
    uuid             = "image-uuid"
    destination_type = "volume"
    volume_type      = "ceph-ssd"
    volume_size      = 10
    boot_index       = 0
    delete_on_termination = true
  }

  network {
    uuid = "network-uuid"
  }

  security_group_ids = ["security-group-uuid"]
}
```

**VM with Cloud-Init:**
```hcl
resource "vkcs_compute_instance" "with_cloud_init" {
  name              = "vm-cloud-init"
  flavor_id         = var.flavor_id
  availability_zone = "GZ1"

  block_device {
    source_type           = "image"
    uuid                  = var.image_id
    destination_type      = "volume"
    volume_type           = "ceph-ssd"
    volume_size           = 20
    boot_index            = 0
    delete_on_termination = false  # Preserve volume
  }

  network {
    port = vkcs_networking_port.instance_port.id
  }

  user_data = <<-EOT
    #cloud-config
    package_update: true
    packages:
      - docker
      - docker-compose
    runcmd:
      - systemctl enable docker
      - systemctl start docker
  EOT

  config_drive = true  # Required for personality

  personality {
    file    = "/etc/app/config.yml"
    content = file("${path.module}/config.yml")
  }

  key_pair = vkcs_compute_keypair.admin.name

  metadata = {
    sid      = "xaas"
    product  = "myapp"
    instance = var.instance_uuid
  }

  stop_before_destroy = true
}
```

**Key Arguments:**
- `name` (required): Instance identifier
- `flavor_id` (required): VM size specification
- `availability_zone` (required): Zone (e.g., "GZ1", "MS1", "ME1")
- `block_device`: Boot and data volumes
  - `source_type`: "image", "volume", or "blank"
  - `uuid`: Source image or volume ID
  - `destination_type`: "volume" (default), "local"
  - `volume_type`: "ceph-ssd", "high-iops", "ko1-high-iops"
  - `volume_size`: Size in GB
  - `boot_index`: 0 for boot volume, >0 for data volumes
  - `delete_on_termination`: true to delete with instance
- `network`: Network connections via `uuid`, `name`, or `port`
- `security_group_ids`: List of security group UUIDs
- `user_data`: Cloud-init configuration (base64 encoded automatically)
- `key_pair`: SSH key pair name
- `metadata`: Custom key-value tags
- `stop_before_destroy`: Graceful shutdown (recommended)

**Attributes:**
- `id`: Instance UUID
- `access_ip_v4` / `access_ip_v6`: Primary IP addresses
- `all_metadata`: Complete metadata map

#### vkcs_compute_keypair

Manages SSH key pairs.

```hcl
resource "vkcs_compute_keypair" "admin" {
  name       = "admin-key"
  public_key = file("~/.ssh/id_rsa.pub")
}

# Or generate new keypair
resource "vkcs_compute_keypair" "generated" {
  name = "generated-key"
}

output "private_key" {
  value     = vkcs_compute_keypair.generated.private_key
  sensitive = true
}
```

#### vkcs_compute_floatingip_associate

Associates floating IP with instance.

```hcl
resource "vkcs_compute_floatingip_associate" "fip" {
  floating_ip = vkcs_networking_floatingip.public.address
  instance_id = vkcs_compute_instance.vm.id
}
```

### Storage Resources

#### vkcs_blockstorage_volume

Creates block storage volumes.

**Empty Volume:**
```hcl
resource "vkcs_blockstorage_volume" "data" {
  name              = "data-volume"
  description       = "Data storage"
  size              = 100  # GB
  volume_type       = "ceph-ssd"
  availability_zone = "GZ1"

  metadata = {
    sid      = "xaas"
    product  = "myapp"
    instance = var.instance_uuid
  }
}
```

**Bootable Volume from Image:**
```hcl
resource "vkcs_blockstorage_volume" "boot" {
  name              = "boot-volume"
  size              = 20
  volume_type       = "ceph-ssd"
  image_id          = data.vkcs_images_image.ubuntu.id
  availability_zone = "GZ1"
}
```

**Volume from Snapshot:**
```hcl
resource "vkcs_blockstorage_volume" "from_snapshot" {
  name              = "restored-volume"
  snapshot_id       = vkcs_blockstorage_snapshot.backup.id
  size              = 50
  volume_type       = "ceph-ssd"
  availability_zone = "GZ1"
}
```

**Key Arguments:**
- `name`: Volume name
- `size` (required): Size in GB
- `volume_type` (required): "ceph-ssd", "high-iops", "ko1-high-iops"
- `availability_zone` (required): Zone
- `image_id`: Create bootable volume from image
- `snapshot_id`: Restore from snapshot
- `source_vol_id`: Clone existing volume
- `metadata`: Custom tags

**Note**: `image_id`, `snapshot_id`, and `source_vol_id` are mutually exclusive.

#### vkcs_compute_volume_attach

Attaches volume to instance.

```hcl
resource "vkcs_compute_volume_attach" "attached" {
  instance_id = vkcs_compute_instance.vm.id
  volume_id   = vkcs_blockstorage_volume.data.id
  device      = "/dev/vdb"  # Optional
}
```

#### vkcs_blockstorage_snapshot

Creates volume snapshots.

```hcl
resource "vkcs_blockstorage_snapshot" "backup" {
  name        = "volume-snapshot"
  description = "Backup before upgrade"
  volume_id   = vkcs_blockstorage_volume.data.id
  force       = false  # true allows snapshot of attached volume
}
```

### Networking Resources

#### vkcs_networking_network

Creates virtual networks.

```hcl
resource "vkcs_networking_network" "app" {
  name           = "app-network"
  admin_state_up = true
  sdn            = "neutron"  # or "sprut"

  tags = ["app", "production"]
}
```

**Arguments:**
- `name`: Network name
- `admin_state_up`: Enable network (default true)
- `sdn`: "neutron" or "sprut" (defaults to project SDN)
- `port_security_enabled`: Enable port security
- `tags`: Network labels

#### vkcs_networking_subnet

Creates subnets within networks.

```hcl
resource "vkcs_networking_subnet" "app" {
  name       = "app-subnet"
  network_id = vkcs_networking_network.app.id
  cidr       = "192.168.1.0/24"

  allocation_pool {
    start = "192.168.1.10"
    end   = "192.168.1.250"
  }

  dns_nameservers = ["8.8.8.8", "8.8.4.4"]

  tags = ["app"]
}
```

**Key Arguments:**
- `network_id` (required): Parent network UUID
- `cidr` (required): Subnet CIDR (e.g., "192.168.1.0/24")
- `ip_version`: 4 or 6 (default 4)
- `allocation_pool`: IP range for DHCP
  - `start`: First IP
  - `end`: Last IP
- `dns_nameservers`: List of DNS servers
- `enable_dhcp`: Enable DHCP (default true)
- `gateway_ip`: Gateway address (auto-assigned if omitted)

#### vkcs_networking_port

Creates network ports with fixed IPs.

```hcl
resource "vkcs_networking_port" "app_port" {
  name       = "app-port"
  network_id = vkcs_networking_network.app.id
  admin_state_up = true

  fixed_ip {
    subnet_id  = vkcs_networking_subnet.app.id
    ip_address = "192.168.1.100"  # Optional: specific IP
  }

  security_group_ids = [
    vkcs_networking_secgroup.app.id,
    vkcs_networking_secgroup.common.id
  ]

  full_security_groups_control = true

  tags = ["app", "database"]
}
```

**Key Arguments:**
- `network_id` (required): Network UUID
- `fixed_ip`: Subnet and optional IP address
  - `subnet_id` (required): Subnet UUID
  - `ip_address` (optional): Specific IP (DHCP if omitted)
- `security_group_ids`: Security group UUIDs
- `full_security_groups_control`: Set true for consistent SG management
- `admin_state_up`: Port enabled state
- `port_security_enabled`: Enable port security
- `no_fixed_ip`: Create port without fixed IP
- `allowed_address_pairs`: Additional IP/MAC pairs
- `tags`: Port labels

**Attributes:**
- `all_fixed_ips`: All assigned IPs
- `mac_address`: Port MAC address

#### vkcs_networking_router

Creates routers for network connectivity.

```hcl
resource "vkcs_networking_router" "router" {
  name                = "app-router"
  admin_state_up      = true
  external_network_id = data.vkcs_networking_network.extnet.id
  sdn                 = "neutron"
}
```

**Arguments:**
- `name`: Router identifier
- `external_network_id`: External network for internet access
- `sdn`: "neutron" or "sprut"
- `admin_state_up`: Enable router

#### vkcs_networking_router_interface

Connects subnet to router.

```hcl
resource "vkcs_networking_router_interface" "app" {
  router_id = vkcs_networking_router.router.id
  subnet_id = vkcs_networking_subnet.app.id
}
```

#### vkcs_networking_secgroup

Creates security groups.

```hcl
resource "vkcs_networking_secgroup" "app" {
  name                 = "app-security-group"
  description          = "Security group for app servers"
  delete_default_rules = true  # Remove default egress rules
  sdn                  = "neutron"

  tags = ["app"]
}
```

**Arguments:**
- `name` (required): Security group name
- `description`: Human-readable description
- `delete_default_rules`: Remove default egress rules (default false)
- `sdn`: "neutron" or "sprut"
- `tags`: Labels

**Default Rules**: VK Cloud automatically creates IPv4 and IPv6 egress rules. Set `delete_default_rules = true` to manage all rules explicitly via Terraform.

#### vkcs_networking_secgroup_rule

Defines security group rules.

```hcl
# Allow SSH
resource "vkcs_networking_secgroup_rule" "ssh" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = vkcs_networking_secgroup.app.id
  description       = "Allow SSH from anywhere"
}

# Allow HTTP
resource "vkcs_networking_secgroup_rule" "http" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 80
  port_range_max    = 80
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = vkcs_networking_secgroup.app.id
  description       = "Allow HTTP"
}

# Allow HTTPS
resource "vkcs_networking_secgroup_rule" "https" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 443
  port_range_max    = 443
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = vkcs_networking_secgroup.app.id
  description       = "Allow HTTPS"
}

# Allow all egress
resource "vkcs_networking_secgroup_rule" "egress_v4" {
  direction         = "egress"
  ethertype         = "IPv4"
  security_group_id = vkcs_networking_secgroup.app.id
  description       = "Allow all IPv4 egress"
}

# Allow from another security group
resource "vkcs_networking_secgroup_rule" "from_lb" {
  direction              = "ingress"
  ethertype              = "IPv4"
  protocol               = "tcp"
  port_range_min         = 8080
  port_range_max         = 8080
  remote_group_id        = vkcs_networking_secgroup.lb.id
  security_group_id      = vkcs_networking_secgroup.app.id
  description            = "Allow from load balancer"
}
```

**Key Arguments:**
- `security_group_id` (required): Parent security group UUID
- `direction` (required): "ingress" or "egress"
- `ethertype` (required): "IPv4" or "IPv6"
- `protocol`: "tcp", "udp", "icmp", or number
- `port_range_min`: Starting port (1-65535)
- `port_range_max`: Ending port (1-65535)
- `remote_ip_prefix`: Source/destination CIDR (e.g., "0.0.0.0/0")
- `remote_group_id`: Allow traffic from another security group
- `description`: Rule description

**Pattern: Using Count for Multiple Ports:**
```hcl
variable "allowed_ports" {
  default = [22, 80, 443, 8080]
}

resource "vkcs_networking_secgroup_rule" "ingress_ports" {
  count             = length(var.allowed_ports)
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = var.allowed_ports[count.index]
  port_range_max    = var.allowed_ports[count.index]
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = vkcs_networking_secgroup.app.id
  description       = "Allow port ${var.allowed_ports[count.index]}"
}
```

#### vkcs_networking_floatingip

Allocates floating (public) IPs.

```hcl
resource "vkcs_networking_floatingip" "public" {
  pool        = "ext-net"  # or "internet" for Sprut SDN
  description = "Public IP for app server"
}
```

**Arguments:**
- `pool` (required): External network pool name
  - Neutron SDN: "ext-net"
  - Sprut SDN: "internet"
- `description`: Human-readable description
- `port_id`: Associate with specific port
- `fixed_ip`: Port's fixed IP (when port has multiple IPs)
- `subnet_ids`: Preferred external subnets

**Attributes:**
- `address`: Allocated public IP
- `id`: Floating IP UUID

**Determining Pool Based on SDN:**
```hcl
resource "vkcs_networking_floatingip" "adaptive" {
  pool = data.vkcs_networking_subnet.app.sdn == "neutron" ? "ext-net" : "internet"
}
```

#### vkcs_networking_floatingip_associate

Associates floating IP with port or instance.

```hcl
resource "vkcs_networking_floatingip_associate" "app" {
  floating_ip = vkcs_networking_floatingip.public.address
  port_id     = vkcs_networking_port.app_port.id
}
```

### Data Sources

Data sources query existing VK Cloud resources.

#### vkcs_networking_network

```hcl
data "vkcs_networking_network" "extnet" {
  name = "ext-net"
}
```

#### vkcs_networking_subnet

```hcl
data "vkcs_networking_subnet" "app" {
  subnet_id = var.subnet_id
}

output "subnet_cidr" {
  value = data.vkcs_networking_subnet.app.cidr
}

output "subnet_sdn" {
  value = data.vkcs_networking_subnet.app.sdn
}
```

#### vkcs_compute_flavor

```hcl
data "vkcs_compute_flavor" "basic" {
  name = "Basic-1-2-20"
}

# Filter by specs
data "vkcs_compute_flavor" "min_specs" {
  min_ram   = 2048
  min_vcpus = 2
  min_disk  = 20
}
```

#### vkcs_images_image

```hcl
data "vkcs_images_image" "ubuntu" {
  name        = "Ubuntu-22.04-202312"
  most_recent = true
}

output "image_id" {
  value = data.vkcs_images_image.ubuntu.id
}
```

## Common Patterns

### Pattern 1: Basic Single-VM Deployment

```hcl
# Data sources
data "vkcs_networking_network" "extnet" {
  name = "ext-net"
}

data "vkcs_images_image" "ubuntu" {
  name        = "Ubuntu-22.04"
  most_recent = true
}

# Network
resource "vkcs_networking_network" "app" {
  name = "app-network"
}

resource "vkcs_networking_subnet" "app" {
  name       = "app-subnet"
  network_id = vkcs_networking_network.app.id
  cidr       = "192.168.1.0/24"
}

resource "vkcs_networking_router" "router" {
  name                = "app-router"
  external_network_id = data.vkcs_networking_network.extnet.id
}

resource "vkcs_networking_router_interface" "app" {
  router_id = vkcs_networking_router.router.id
  subnet_id = vkcs_networking_subnet.app.id
}

# Security
resource "vkcs_networking_secgroup" "app" {
  name = "app-sg"
}

resource "vkcs_networking_secgroup_rule" "ssh" {
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = 22
  port_range_max    = 22
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = vkcs_networking_secgroup.app.id
}

# Compute
resource "vkcs_blockstorage_volume" "boot" {
  name              = "boot-volume"
  size              = 20
  volume_type       = "ceph-ssd"
  image_id          = data.vkcs_images_image.ubuntu.id
  availability_zone = "GZ1"
}

resource "vkcs_compute_instance" "vm" {
  name              = "app-server"
  flavor_id         = "flavor-uuid"
  availability_zone = "GZ1"

  block_device {
    source_type      = "volume"
    uuid             = vkcs_blockstorage_volume.boot.id
    destination_type = "volume"
    boot_index       = 0
  }

  network {
    uuid = vkcs_networking_network.app.id
  }

  security_group_ids = [vkcs_networking_secgroup.app.id]
}

# Public IP
resource "vkcs_networking_floatingip" "public" {
  pool = "ext-net"
}

resource "vkcs_compute_floatingip_associate" "fip" {
  floating_ip = vkcs_networking_floatingip.public.address
  instance_id = vkcs_compute_instance.vm.id
}

output "public_ip" {
  value = vkcs_networking_floatingip.public.address
}
```

### Pattern 2: Marketplace Application Deployment

```hcl
# Variables
variable "instance_uuid" {
  type    = string
  default = "uuid-from-marketplace"
}

variable "email" {
  type    = string
  default = "user@example.com"
}

variable "ds-subnet" {
  type = string
}

variable "ds-flavor" {
  type = string
}

variable "ds-az" {
  type    = string
  default = "GZ1"
}

variable "image_uuid" {
  type = string
}

# Locals
locals {
  short_name = substr(var.instance_uuid, 0, 8)
  hosts_name = "${local.short_name}-myapp"
}

# Data sources
data "vkcs_networking_subnet" "subnet" {
  subnet_id = var.ds-subnet
}

# Network port
resource "vkcs_networking_port" "port" {
  name               = "${local.short_name}-myapp"
  admin_state_up     = true
  network_id         = data.vkcs_networking_subnet.subnet.network_id
  security_group_ids = [vkcs_networking_secgroup.secgroup.id]
  sdn                = data.vkcs_networking_subnet.subnet.sdn

  fixed_ip {
    subnet_id = var.ds-subnet
  }
}

# Security group
resource "vkcs_networking_secgroup" "secgroup" {
  name                 = "${local.short_name}-myapp"
  sdn                  = data.vkcs_networking_subnet.subnet.sdn
  delete_default_rules = true
}

resource "vkcs_networking_secgroup_rule" "ingress" {
  count             = length([22, 80, 443])
  direction         = "ingress"
  ethertype         = "IPv4"
  protocol          = "tcp"
  port_range_min    = [22, 80, 443][count.index]
  port_range_max    = [22, 80, 443][count.index]
  remote_ip_prefix  = "0.0.0.0/0"
  security_group_id = vkcs_networking_secgroup.secgroup.id
  description       = "Allow port ${[22, 80, 443][count.index]}"
}

resource "vkcs_networking_secgroup_rule" "egress" {
  direction         = "egress"
  ethertype         = "IPv4"
  security_group_id = vkcs_networking_secgroup.secgroup.id
}

# Boot volume
resource "vkcs_blockstorage_volume" "boot" {
  name              = "${local.short_name}-myapp"
  metadata          = { "sid" : "xaas", "product" : "myapp", "instance" : var.instance_uuid }
  image_id          = var.image_uuid
  volume_type       = "ceph-ssd"
  size              = 20
  availability_zone = var.ds-az
}

# VM instance
resource "vkcs_compute_instance" "compute" {
  name              = local.hosts_name
  flavor_id         = var.ds-flavor
  availability_zone = var.ds-az
  metadata          = { "sid" : "xaas", "product" : "myapp", "instance" : var.instance_uuid }

  block_device {
    source_type      = "volume"
    uuid             = vkcs_blockstorage_volume.boot.id
    destination_type = "volume"
    boot_index       = 0
  }

  network {
    port = vkcs_networking_port.port.id
  }

  stop_before_destroy = true

  timeouts {
    create = "10m"
  }
}

# Floating IP
resource "vkcs_networking_floatingip" "fip" {
  pool = data.vkcs_networking_subnet.subnet.sdn == "neutron" ? "ext-net" : "internet"
}

resource "vkcs_compute_floatingip_associate" "fip" {
  floating_ip = vkcs_networking_floatingip.fip.address
  instance_id = vkcs_compute_instance.compute.id
}

# Outputs
output "internal_ip" {
  description = "Internal IP address"
  value       = vkcs_compute_instance.compute.access_ip_v4
}

output "external_ip" {
  description = "Public IP address"
  value       = vkcs_networking_floatingip.fip.address
}
```

### Pattern 3: Using Variables for Datasource Parameters

```hcl
# parameters/ds-az.yaml
actions:
  - create
schema:
  description: Availability Zone
  type: string
  datasource:
    type: availability_zone

# parameters/ds-flavor.yaml
actions:
  - create
schema:
  description: VM Flavor
  type: string
  datasource:
    type: flavor
    filter:
      vcpus:
        minimum: 1
      ram:
        minimum: 1024

# parameters/ds-subnet.yaml
actions:
  - create
schema:
  description: Subnet
  type: string
  datasource:
    type: subnet

# deploy.tf
variable "ds-az" { type = string }
variable "ds-flavor" { type = string }
variable "ds-subnet" { type = string }

data "vkcs_networking_subnet" "subnet" {
  subnet_id = var.ds-subnet
}

resource "vkcs_compute_instance" "vm" {
  availability_zone = var.ds-az
  flavor_id         = var.ds-flavor
  network {
    uuid = data.vkcs_networking_subnet.subnet.network_id
  }
  # ...
}
```

## Best Practices

### Resource Naming

Use consistent naming with prefixes:
```hcl
locals {
  prefix = "${var.project}-${var.environment}"
}

resource "vkcs_networking_network" "app" {
  name = "${local.prefix}-network"
}

resource "vkcs_compute_instance" "vm" {
  name = "${local.prefix}-vm-${count.index + 1}"
}
```

### Security Groups

1. **Always set `delete_default_rules = true`** when managing all rules via Terraform
2. **Use `full_security_groups_control = true`** for ports
3. **Add descriptions to all rules** for documentation

### Metadata Tags

Add consistent metadata for resource tracking:
```hcl
metadata = {
  sid      = "xaas"
  product  = var.product_name
  instance = var.instance_uuid
  managed_by = "terraform"
}
```

### Volume Management

1. **Create volumes separately** from instances for persistence
2. **Set `delete_on_termination = false`** for data volumes
3. **Use `stop_before_destroy = true`** for instances with volumes

### Timeouts

Add timeouts for long-running operations:
```hcl
resource "vkcs_compute_instance" "vm" {
  # ...
  timeouts {
    create = "15m"
    update = "10m"
    delete = "10m"
  }
}
```

### Dependencies

Use explicit `depends_on` when needed:
```hcl
resource "vkcs_compute_instance" "vm" {
  # ...
  depends_on = [
    vkcs_networking_router_interface.app
  ]
}
```

## Troubleshooting

### Common Issues

**Issue: "The subnet could not be found"**
```
Solution:
1. Verify subnet exists: data source query
2. Check subnet_id format (UUID)
3. Ensure router interface created first
4. Add explicit depends_on
```

**Issue: "No valid host was found"**
```
Solution:
1. Check flavor availability in zone
2. Verify sufficient quota
3. Try different availability zone
4. Check flavor_id is valid UUID
```

**Issue: "Port already has a floating IP"**
```
Solution:
1. Use vkcs_compute_floatingip_associate instead of vkcs_networking_floatingip_associate for instances
2. Dissociate existing floating IP first
3. Check if floating IP already assigned
```

**Issue: "Security group rules conflict"**
```
Solution:
1. Set delete_default_rules = true on security group
2. Ensure full_security_groups_control = true on ports
3. Define all egress rules explicitly
```

**Issue: SDN mismatch**
```
Solution:
1. Query subnet SDN: data.vkcs_networking_subnet.subnet.sdn
2. Use correct pool for floating IPs:
   - Neutron: "ext-net"
   - Sprut: "internet"
3. Set sdn explicitly on resources
```

## State Management

### Import Existing Resources

```bash
# Import network
terraform import vkcs_networking_network.app <network-uuid>

# Import instance
terraform import vkcs_compute_instance.vm <instance-uuid>

# Import volume
terraform import vkcs_blockstorage_volume.data <volume-uuid>

# Import security group
terraform import vkcs_networking_secgroup.app <secgroup-uuid>
```

### Remote State

Store state securely:
```hcl
terraform {
  backend "s3" {
    bucket   = "terraform-state"
    key      = "vkcloud/terraform.tfstate"
    endpoint = "https://s3.storage.cloud.vk.com"
    region   = "ru-msk"
  }
}
```

## References

- **Official Documentation**: https://registry.terraform.io/providers/vk-cs/vkcs/latest/docs
- **GitHub Repository**: https://github.com/vk-cs/terraform-provider-vkcs
- **VK Cloud Portal**: https://mcs.mail.ru/app/
- **Terraform Provider Download**: VK Cloud Portal → Project → Terraform tab

See `references/` directory for:
- Complete deployment examples
- Provider configuration templates
- Resource combinations
- Migration guides

See `assets/` directory for:
- Resource relationship diagrams
- Network topology examples
- Security group patterns
