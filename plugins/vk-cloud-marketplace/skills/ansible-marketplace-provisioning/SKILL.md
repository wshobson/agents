---
name: ansible-marketplace-provisioning
description: Ansible provisioning patterns for VK Cloud marketplace image-based applications. Use when structuring Ansible playbooks, creating provision/service roles, or integrating with Terraform deployment.
---

# Ansible Provisioning for VK Cloud Marketplace

## When to Use This Skill

- Structuring Ansible playbooks for marketplace applications
- Creating provision roles for image build-time configuration
- Developing service roles for runtime initialization
- Integrating Ansible with Terraform via ivkcs_agent_exec
- Passing runtime parameters from Terraform to Ansible
- Implementing monitoring and backup automation
- Handling conditional service configuration

## Core Concepts

### Dual Playbook Architecture

VK Cloud marketplace uses a two-phase Ansible approach:

**1. Build-Time Provisioning (provision.yml)**
- Runs during Packer image build
- Installs software and dependencies
- Configures OS and system settings
- Prepares application files
- Sets up infrastructure (monitoring, backup)
- Executed with root privileges
- Creates reusable image template

**2. Runtime Initialization (start.yml)**
- Runs during Terraform deployment via ivkcs_agent_exec
- Starts services with user configuration
- Applies runtime parameters from --extra-vars
- Configures application-specific settings
- Initializes monitoring with VK Cloud credentials
- Executed on localhost after VM boot
- Customizes deployed instance

### Playbook Organization Pattern

```
playbook/
├── ansible.cfg                    # Ansible configuration
├── provision.yml                  # Build-time playbook (Packer)
├── start.yml                      # Runtime playbook (Terraform)
├── vm_init.yml                    # First-boot initialization (optional)
├── common_roles/                  # Shared across playbooks
│   └── variables/
│       └── defaults/
│           └── main.yml           # Default variable values
├── provision_roles/               # Build-time roles
│   ├── vm_init/                   # OS requirements
│   ├── docker/                    # Docker installation
│   ├── monitoring/                # Telegraf setup
│   ├── backup/                    # Backup tools
│   ├── lego/                      # Let's Encrypt (optional)
│   └── myapp/                     # Application installation
├── service_roles/                 # Runtime roles
│   ├── docker/                    # Docker service start
│   ├── monitoring/                # Monitoring activation
│   ├── backup/                    # Backup service start
│   ├── lego/                      # Certificate generation
│   └── myapp/                     # Application start
└── files/                         # Static files and templates
    ├── configs/
    ├── scripts/
    └── templates/
```

## Provision Playbook (provision.yml)

### Structure and Purpose

The provision playbook prepares the VM image during Packer build:

```yaml
---
- name: Provision Image
  hosts: default              # Packer creates 'default' host
  gather_facts: false         # Skip for speed (enable if needed)
  become: true               # Run as root

  tasks:
    # 1. Initialize VM with required packages
    - import_role:
        name: provision_roles/vm_init

    # 2. Load common variables
    - import_role:
        name: common_roles/variables

    # 3. Install Docker (if needed)
    - import_role:
        name: provision_roles/docker

    # 4. Set up monitoring infrastructure
    - import_role:
        name: provision_roles/monitoring

    # 5. Install backup tools
    - import_role:
        name: provision_roles/backup

    # 6. Optional: Let's Encrypt automation
    - import_role:
        name: provision_roles/lego

    # 7. Install application
    - import_role:
        name: provision_roles/myapp
```

**Key Characteristics:**
- `hosts: default` - Packer target
- `become: true` - Root access required for installation
- `gather_facts: false` - Faster execution (enable if facts needed)
- Sequential role execution
- Idempotent tasks

### Common Provision Roles

**vm_init Role (Required)**

Installs VK Cloud mandatory packages:

```yaml
# provision_roles/vm_init/tasks/main.yml
---
- name: Update package cache
  apt:
    update_cache: yes
    cache_valid_time: 3600
  when: ansible_os_family == "Debian"

- name: Install VK Cloud required packages
  apt:
    name:
      - cloud-init       # VM initialization
      - curl             # Agent download
      - systemd          # Service management
      - qemu-guest-agent # VK Cloud integration
      - openssh-server   # Remote access
      - ca-certificates  # SSL support
      - python3          # Ansible/automation
    state: present

- name: Enable and start SSH
  systemd:
    name: ssh
    enabled: yes
    state: started

- name: Enable Qemu guest agent
  systemd:
    name: qemu-guest-agent
    enabled: yes
    state: started

- name: Disable firewall (VK Cloud handles security)
  systemd:
    name: ufw
    enabled: no
    state: stopped
  ignore_errors: yes

- name: Clear bash history
  shell: |
    history -c
    rm -f /root/.bash_history
    rm -f /home/*/.bash_history
  args:
    warn: false
```

**docker Role**

Installs Docker for containerized applications:

```yaml
# provision_roles/docker/tasks/main.yml
---
- name: Install Docker dependencies
  apt:
    name:
      - apt-transport-https
      - ca-certificates
      - gnupg
      - lsb-release
    state: present

- name: Add Docker GPG key
  apt_key:
    url: https://download.docker.com/linux/ubuntu/gpg
    state: present

- name: Add Docker repository
  apt_repository:
    repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
    state: present

- name: Install Docker
  apt:
    name:
      - docker-ce
      - docker-ce-cli
      - containerd.io
      - docker-compose-plugin
    state: present
    update_cache: yes

- name: Add default user to docker group
  user:
    name: "{{ ansible_user }}"
    groups: docker
    append: yes

- name: Disable Docker service (starts at runtime)
  systemd:
    name: docker
    enabled: no
```

**monitoring Role**

Sets up Telegraf for VK Cloud monitoring:

```yaml
# provision_roles/monitoring/tasks/main.yml
---
- name: Download Telegraf package
  get_url:
    url: https://dl.influxdata.com/telegraf/releases/telegraf_1.28.2-1_amd64.deb
    dest: /tmp/telegraf.deb

- name: Install Telegraf
  apt:
    deb: /tmp/telegraf.deb

- name: Create Telegraf config directory
  file:
    path: /etc/telegraf/telegraf.d
    state: directory
    owner: telegraf
    group: telegraf
    mode: '0755'

- name: Copy base Telegraf configuration
  copy:
    src: telegraf.conf
    dest: /etc/telegraf/telegraf.conf
    owner: telegraf
    group: telegraf
    mode: '0644'

- name: Disable Telegraf (configured at runtime)
  systemd:
    name: telegraf
    enabled: no

- name: Clean up download
  file:
    path: /tmp/telegraf.deb
    state: absent
```

**backup Role**

Prepares backup tools:

```yaml
# provision_roles/backup/tasks/main.yml
---
- name: Install backup tools
  apt:
    name:
      - restic    # Modern backup tool
      - rclone    # Cloud storage sync
      - cron      # Scheduled backups
    state: present

- name: Create backup directories
  file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  loop:
    - /opt/backup
    - /var/backups/app

- name: Copy backup scripts
  copy:
    src: "{{ item }}"
    dest: /opt/backup/
    mode: '0755'
  with_fileglob:
    - files/backup_*.sh

- name: Disable cron (configured at runtime)
  systemd:
    name: cron
    enabled: no
```

## Start Playbook (start.yml)

### Structure and Purpose

The start playbook initializes services during deployment:

```yaml
---
- name: Start services
  hosts: localhost
  connection: local
  gather_facts: false

  tasks:
    # 1. Load variables (includes defaults and runtime vars)
    - import_role:
        name: common_roles/variables

    # 2. Start Docker services
    - import_role:
        name: service_roles/docker

    # 3. Generate Let's Encrypt certificates
    - import_role:
        name: service_roles/lego
      when: lego_enabled|bool

    # 4. Start backup services
    - import_role:
        name: service_roles/backup
      when: backup_enabled|bool

    # 5. Start application
    - import_role:
        name: service_roles/myapp

    # 6. Initialize monitoring
    - import_role:
        name: service_roles/monitoring
      when: monitoring_output_user_id != ""

    # 7. Optional: Tracing
    - import_role:
        name: service_roles/tracing
      when: tracing_enabled|bool
```

**Key Characteristics:**
- `hosts: localhost` - Runs on deployed VM
- `connection: local` - No SSH needed
- Conditional role execution with `when:`
- Uses runtime variables from --extra-vars
- Idempotent service startup

### Common Service Roles

**docker Service Role**

Starts Docker and containers:

```yaml
# service_roles/docker/tasks/main.yml
---
- name: Start Docker service
  systemd:
    name: docker
    state: started
    enabled: yes

- name: Wait for Docker to be ready
  wait_for:
    path: /var/run/docker.sock
    timeout: 60

- name: Pull application image
  docker_image:
    name: "{{ app_image }}"
    tag: "{{ app_version }}"
    source: pull
```

**monitoring Service Role**

Configures and starts Telegraf with VK Cloud:

```yaml
# service_roles/monitoring/tasks/main.yml
---
- name: Create monitoring configuration
  template:
    src: monitoring.conf.j2
    dest: /etc/telegraf/telegraf.d/monitoring.conf
    owner: telegraf
    group: telegraf
    mode: '0644'

- name: Start Telegraf
  systemd:
    name: telegraf
    state: started
    enabled: yes

# Template file:
# monitoring.conf.j2
[[outputs.influxdb_v2]]
  urls = ["{{ monitoring_output_endpoint }}"]
  token = "{{ monitoring_output_user_id }}:{{ monitoring_output_password }}"
  organization = "{{ monitoring_output_project_id }}"
  bucket = "{{ monitoring_output_namespace }}"

[[inputs.cpu]]
  percpu = true
  totalcpu = true

[[inputs.disk]]
[[inputs.diskio]]
[[inputs.mem]]
[[inputs.net]]
[[inputs.system]]

[global_tags]
  instance_id = "{{ monitoring_tags_instance_id }}"
```

**myapp Service Role**

Starts application with configuration:

```yaml
# service_roles/myapp/tasks/main.yml
---
- name: Create app configuration from template
  template:
    src: app_config.yml.j2
    dest: /opt/app/config.yml
    mode: '0644'

- name: Start application containers
  docker_compose:
    project_src: /opt/app
    state: present
    pull: yes
  environment:
    PUBLIC_ADDRESS: "{{ public_address }}"
    ADMIN_EMAIL: "{{ admin_email }}"
    CUSTOM_OPTION: "{{ custom_option }}"
```

## Terraform Integration

### Executing start.yml with ivkcs_agent_exec

Terraform runs the start playbook during deployment:

```hcl
resource "ivkcs_agent_exec" "start" {
  hosts = [local.hosts_name]
  name  = "start_service"
  uuid  = var.instance_uuid

  step {
    index   = 1
    type    = "bash"
    content = <<-EOT
#!/bin/bash

ansible-playbook start.yml \
  --extra-vars "public_address=${vkcs_networking_floatingip.fips.address}" \
  --extra-vars "subnet_cidr=${data.vkcs_networking_subnet.subnet.cidr}" \
  --extra-vars "admin_email=${var.email}" \
  --extra-vars "lego_enabled=${var.lego_enabled}" \
  --extra-vars "backup_enabled=${var.backup_enabled}" \
  --extra-vars "monitoring_output_user_id=${data.ivkcs_monitoring_user.write.user_id}" \
  --extra-vars "monitoring_output_password=${data.ivkcs_monitoring_user.write.password}" \
  --extra-vars "monitoring_output_project_id=${data.ivkcs_monitoring_user.write.project_id}" \
  --extra-vars "monitoring_output_auth_url=${data.ivkcs_monitoring_user.write.auth_url}" \
  --extra-vars "monitoring_output_namespace=${data.ivkcs_monitoring_user.write.namespace}" \
  --extra-vars "monitoring_output_endpoint=${data.ivkcs_monitoring_user.write.endpoint}" \
  --extra-vars "monitoring_tags_instance_id=${vkcs_compute_instance.compute.id}" \
  --extra-vars "custom_option=${var.custom_option}"

EOT

    options {
      timeout  = "10m"
      cwd      = "/opt/playbooks"
      attempts = 1
    }
  }

  depends_on = [
    vkcs_compute_instance.compute,
    ivkcs_compute_instance_reboot.reboot
  ]
}
```

### Retrieving Outputs

Capture playbook outputs for Terraform:

```hcl
# Additional step to get output
resource "ivkcs_agent_exec" "start" {
  # ... previous step ...

  step {
    index   = 2
    type    = "bash"
    content = "cat /opt/app/credentials.txt"
    options {
      timeout  = "5s"
      attempts = 1
    }
  }
}

# Retrieve the result
data "ivkcs_agent_script_result" "credentials" {
  uuid  = var.instance_uuid
  host  = local.hosts_name
  group = ivkcs_agent_exec.start.name
  index = 2

  depends_on = [ivkcs_agent_exec.start]
}

# Output to user
output "credentials" {
  description = "Application credentials"
  value       = data.ivkcs_agent_script_result.credentials.result
  sensitive   = true
}
```

## Variable Management

### Common Variables Pattern

```yaml
# common_roles/variables/defaults/main.yml
---
# Feature flags (overridden by --extra-vars)
lego_enabled: false
backup_enabled: false
monitoring_enabled: true
tracing_enabled: false

# Default application settings
app_image: "myorg/myapp"
app_version: "latest"
app_port: 8080

# Monitoring defaults (populated by Terraform)
monitoring_output_user_id: ""
monitoring_output_password: ""
monitoring_output_project_id: ""
monitoring_output_auth_url: ""
monitoring_output_namespace: ""
monitoring_output_endpoint: ""
monitoring_tags_instance_id: ""

# Network defaults
public_address: ""
subnet_cidr: ""
admin_email: ""

# Service-specific defaults
custom_option: "default_value"
```

### Variable Priority

Ansible variable precedence (lowest to highest):

1. Role defaults (`common_roles/variables/defaults/main.yml`)
2. Playbook vars
3. --extra-vars from Terraform (highest priority)

## Advanced Patterns

### Conditional Execution

```yaml
# start.yml with complex conditionals
- name: Configure HTTPS
  import_role:
    name: service_roles/lego
  when:
    - lego_enabled|bool
    - public_address != ""
    - admin_email != ""

- name: Start backup service
  import_role:
    name: service_roles/backup
  when:
    - backup_enabled|bool
    - backup_s3_endpoint is defined

- name: Initialize monitoring
  import_role:
    name: service_roles/monitoring
  when:
    - monitoring_output_user_id != ""
    - monitoring_enabled|default(true)|bool
```

### Dynamic Configuration Templates

```yaml
# service_roles/myapp/tasks/main.yml
- name: Generate app configuration
  template:
    src: app_config.yml.j2
    dest: /opt/app/config.yml

# templates/app_config.yml.j2
---
server:
  host: {{ public_address }}
  port: {{ app_port }}

{% if lego_enabled %}
ssl:
  enabled: true
  cert: /etc/lego/certificates/{{ public_address }}.crt
  key: /etc/lego/certificates/{{ public_address }}.key
{% endif %}

{% if backup_enabled %}
backup:
  enabled: true
  schedule: "0 2 * * *"
  destination: s3://{{ backup_bucket }}
{% endif %}

monitoring:
  enabled: {{ monitoring_enabled|lower }}
{% if monitoring_enabled %}
  endpoint: {{ monitoring_output_endpoint }}
{% endif %}
```

### Multi-Step Deployment

```yaml
# start.yml with phases
- name: Phase 1 - Infrastructure
  import_role:
    name: service_roles/docker

- name: Phase 2 - Data layer
  import_role:
    name: service_roles/database

- name: Phase 3 - Application
  import_role:
    name: service_roles/myapp

- name: Phase 4 - Monitoring
  import_role:
    name: service_roles/monitoring
  when: monitoring_output_user_id != ""

- name: Phase 5 - Health check
  wait_for:
    host: localhost
    port: "{{ app_port }}"
    timeout: 60
```

### Error Handling

```yaml
# service_roles/myapp/tasks/main.yml
- name: Start application
  docker_compose:
    project_src: /opt/app
    state: present
  register: app_start
  retries: 3
  delay: 5
  until: app_start is succeeded

- name: Verify application health
  uri:
    url: "http://localhost:{{ app_port }}/health"
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 10
  delay: 3

- name: Log startup success
  lineinfile:
    path: /var/log/app/startup.log
    line: "{{ ansible_date_time.iso8601 }} - Application started successfully"
    create: yes
  when: health_check is succeeded

- name: Handle startup failure
  fail:
    msg: "Application failed to start - check logs at /var/log/app/"
  when: health_check is failed
```

## Best Practices

### Role Organization

1. **Separation of Concerns**
   - Provision roles: Install and configure
   - Service roles: Start and initialize
   - Common roles: Shared variables and utilities

2. **Role Naming**
   - Use descriptive names: `docker`, `monitoring`, `backup`
   - Match provision and service role names
   - Prefix with category if needed: `database_postgres`, `web_nginx`

3. **Task Organization**
   - Group related tasks in same file
   - Use handlers for service restarts
   - Implement proper error handling
   - Add task names for clarity

### Idempotency

Ensure tasks can be run multiple times safely:

```yaml
# ✅ GOOD - Idempotent
- name: Create app directory
  file:
    path: /opt/app
    state: directory

# ✅ GOOD - Idempotent with check
- name: Initialize database
  command: /opt/app/init-db.sh
  args:
    creates: /var/lib/app/db/initialized

# ❌ BAD - Not idempotent
- name: Append to config
  shell: echo "setting=value" >> /etc/app/config
```

### Variable Naming

Follow consistent naming conventions:

```yaml
# Feature flags
<feature>_enabled: bool

# Service configuration
<service>_<setting>: value

# Monitoring variables
monitoring_output_<field>: value
monitoring_tags_<tag>: value

# Network configuration
public_address: ip_or_hostname
subnet_cidr: cidr_notation
```

### Documentation

Document roles clearly:

```yaml
# provision_roles/myapp/README.md
# MyApp Provision Role

## Purpose
Installs MyApp application and dependencies during image build.

## Requirements
- Ubuntu 22.04 or later
- Docker installed

## Variables
- `app_version`: Application version to install (default: "1.0.0")
- `app_install_path`: Installation directory (default: "/opt/app")

## Tasks
1. Create application directory
2. Download application binaries
3. Install dependencies
4. Configure application defaults
5. Prepare data directories

## Files
- `files/app-v1.0.0.tar.gz`: Application binary
- `templates/app.conf.j2`: Configuration template
```

## Troubleshooting

### Common Issues

**Issue: Variable not found in template**
```
Error: 'monitoring_output_endpoint' is undefined
Solution:
1. Check variable passed via --extra-vars
2. Verify variable name matches exactly
3. Add default in common_roles/variables
4. Use |default('') filter in template
```

**Issue: Service fails to start**
```
Error: Service myapp failed to start
Solution:
1. Check service logs: journalctl -u myapp
2. Verify configuration file syntax
3. Check file permissions
4. Ensure dependencies started first
5. Validate environment variables
```

**Issue: Ansible playbook not found**
```
Error: Could not find start.yml
Solution:
1. Verify playbook copied to /opt/playbooks
2. Check cwd in ivkcs_agent_exec options
3. Use absolute path to playbook
4. Verify provision role copied playbooks
```

**Issue: Template rendering fails**
```
Error: Template error - filter 'bool' does not exist
Solution:
1. Update Ansible to 2.9+
2. Use alternative: {% if lego_enabled == true %}
3. Check Jinja2 version compatibility
```

## References

See `references/` directory for:
- Complete playbook examples (provision.yml, start.yml)
- Role templates with best practices
- Terraform integration examples
- Variable management patterns
- Testing procedures

See `assets/` directory for:
- Playbook execution flow diagrams
- Role dependency charts
- Variable precedence documentation
- Troubleshooting guides
