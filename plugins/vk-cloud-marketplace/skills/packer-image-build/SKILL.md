---
name: packer-image-build
description: Build VM images for VK Cloud marketplace using Packer with Ansible provisioning. Use when creating VM images, automating image builds, or preparing images for marketplace deployment.
---

# Packer Image Build for VK Cloud Marketplace

## When to Use This Skill

- Building VM images for VK Cloud marketplace
- Automating image creation with Packer
- Provisioning images with Ansible during build
- Ensuring images meet VK Cloud requirements
- Creating reproducible image builds
- Setting up CI/CD for image building

## Core Concepts

### Packer Overview

Packer is an open-source tool for creating identical machine images for multiple platforms from a single source configuration. For VK Cloud marketplace, Packer automates:

- VM creation with proper base OS
- Ansible provisioning during build
- Image export with correct metadata
- Reproducible builds for CI/CD

**Build Process Flow:**
```
1. Packer reads configuration (.images.yaml, .pkr.hcl)
2. Creates temporary VM from base image
3. Runs Ansible provisioner (provision.yml)
4. Captures VM snapshot as new image
5. Exports image with metadata
6. Cleans up temporary resources
```

### Image Metadata Configuration (.images.yaml)

The `.images.yaml` file defines OpenStack-compatible metadata for the image:

```yaml
xaas-service-name:
  # Image OpenStack metadata
  metadata:
    os_admin_user: 'ubuntu'           # Default admin username
    os_distro: ubuntu2404             # Distribution identifier
    os_version: '24'                  # OS version as string
    os_type: 'linux'                  # Always 'linux' for Linux
    mcs_name: xaas-service-name       # VK Cloud marketplace name
    mcs_os_type: 'linux'              # Always 'linux'
    mcs_os_distro: 'ubuntu'           # Distribution for marketplace
    mcs_os_version: '24'              # Version for marketplace
    hw_qemu_guest_agent: 'yes'        # Required for VK Cloud
    os_require_quiesce: 'yes'         # Required for snapshots
    team: 'xaas'                      # Team identifier
    sid: 'hidden'                     # Service ID or 'hidden'

  # Packer build overrides (optional)
  build_override:
    disk_size: 50G                    # Override default disk size
```

**Common Distributions:**
- Ubuntu: `ubuntu2404`, `ubuntu2204`, `ubuntu2004`
- AlmaLinux: `almalinux9`, `almalinux8`
- CentOS: `centos8`, `centos7`

**Required Metadata Fields:**
- `os_admin_user`: Must match the admin user in base image
- `hw_qemu_guest_agent`: Must be 'yes' for VK Cloud compatibility
- `os_require_quiesce`: Must be 'yes' for proper snapshot support
- `mcs_*` fields: Define how image appears in VK Cloud marketplace

### Packer HCL Configuration

The Packer HCL file (e.g., `xaas-service.pkr.hcl`) defines the build process:

```hcl
build {
  source "qemu.ubuntu-24" {
    name = "xaas-service-name"
  }

  provisioner "ansible" {
    playbook_file = "./playbook/provision.yml"
    user          = "ubuntu"
    sftp_command  = "/usr/libexec/openssh/sftp-server -e"
    use_proxy     = false
    ansible_env_vars = [
      "ANSIBLE_CONFIG=./playbook/ansible.cfg"
    ]
  }
}
```

**Build Block:**
- `source`: References base image source (e.g., `qemu.ubuntu-24`)
- `name`: Image name (matches `.images.yaml` key)

**Ansible Provisioner:**
- `playbook_file`: Path to provision playbook (relative to HCL file)
- `user`: Admin user for SSH (must match `os_admin_user`)
- `sftp_command`: SFTP server command for file transfer
- `use_proxy`: Disable proxy for local builds
- `ansible_env_vars`: Set Ansible configuration file path

**Available Base Sources:**
- `qemu.ubuntu-24`: Ubuntu 24.04 LTS
- `qemu.ubuntu-22`: Ubuntu 22.04 LTS
- `qemu.almalinux-91`: AlmaLinux 9.1
- `qemu.almalinux-8`: AlmaLinux 8

## Image Requirements

### Required Software Packages

Every VK Cloud marketplace image must include:

1. **Cloud-init**
   - Essential for VM initialization
   - Handles user-data processing
   - Configures SSH keys and networking
   - Manages first-boot scripts

2. **Curl**
   - Required for agent download
   - Used in Cloud-init scripts
   - Essential for bootstrap process

3. **Systemd**
   - Service management
   - Agent lifecycle control
   - Auto-start configuration

4. **Qemu-guest-agent**
   - Enables password setting via VK Cloud UI
   - Provides VM information to hypervisor
   - Required for proper VM management

5. **SSH Server (OpenSSH)**
   - Remote access capability
   - Must auto-start on boot
   - Key-based authentication support

6. **VirtIO Drivers**
   - `virtio-net`: Network interface
   - `virtio-blk`: Block storage
   - `virtiofs`: File system access
   - Usually included in modern kernels

### OS Configuration Requirements

**Security and Cleanup:**
- No default passwords or hardcoded credentials
- All unused ports closed
- Firewall disabled (marketplace handles security)
- Bash command history cleared
- No development tools in production images
- Remove sensitive data and personal information

**System Configuration:**
- SSH server enabled and auto-start on boot
- Linux kernel configured to log to console
- No embedded immutable MAC addresses
- Full KVM virtualization support
- VK Cloud SDN compatibility
- Services auto-start after soft and hard reboots

## Ansible Provisioning Integration

### Playbook Organization

Packer runs the **provision.yml** playbook during image build:

```yaml
---
- name: Provision Image
  hosts: default              # Packer sets up 'default' host
  gather_facts: false
  become: true               # Run with root privileges

  tasks:
    - import_role:
        name: provision_roles/vm_init

    - import_role:
        name: common_roles/variables

    - import_role:
        name: provision_roles/docker

    - import_role:
        name: provision_roles/monitoring

    - import_role:
        name: provision_roles/backup

    - import_role:
        name: provision_roles/myapp
```

**Playbook Characteristics:**
- `hosts: default`: Packer creates temporary VM as 'default'
- `become: true`: Root access for package installation
- `gather_facts: false`: Skip fact gathering for speed
- Roles executed in order during image build

### Common Provision Roles

**vm_init Role:**
```yaml
# provision_roles/vm_init/tasks/main.yml
---
- name: Update package cache
  apt:
    update_cache: yes
  when: ansible_os_family == "Debian"

- name: Install required packages
  apt:
    name:
      - cloud-init
      - curl
      - systemd
      - qemu-guest-agent
      - openssh-server
      - ca-certificates
    state: present

- name: Enable SSH service
  systemd:
    name: ssh
    enabled: yes
    state: started

- name: Enable Qemu guest agent
  systemd:
    name: qemu-guest-agent
    enabled: yes
    state: started

- name: Disable firewall
  systemd:
    name: ufw
    enabled: no
    state: stopped
  ignore_errors: yes

- name: Clear bash history
  shell: history -c && rm -f /root/.bash_history /home/*/.bash_history
```

**monitoring Role:**
```yaml
# provision_roles/monitoring/tasks/main.yml
---
- name: Install Telegraf
  apt:
    deb: https://dl.influxdata.com/telegraf/releases/telegraf_1.28.2-1_amd64.deb

- name: Create Telegraf config directory
  file:
    path: /etc/telegraf/telegraf.d
    state: directory
    owner: telegraf
    group: telegraf
    mode: '0755'

- name: Install Telegraf base config
  copy:
    src: telegraf.conf
    dest: /etc/telegraf/telegraf.conf
    owner: telegraf
    group: telegraf

- name: Disable Telegraf (starts at runtime)
  systemd:
    name: telegraf
    enabled: no
```

**backup Role:**
```yaml
# provision_roles/backup/tasks/main.yml
---
- name: Install backup tools
  apt:
    name:
      - restic
      - rclone
    state: present

- name: Create backup scripts directory
  file:
    path: /opt/backup
    state: directory
    mode: '0755'

- name: Copy backup scripts
  copy:
    src: "{{ item }}"
    dest: /opt/backup/
    mode: '0755'
  with_fileglob:
    - files/backup_*.sh
```

### Ansible Configuration

**ansible.cfg Example:**
```ini
[defaults]
host_key_checking = False
retry_files_enabled = False
roles_path = ./common_roles:./provision_roles:./service_roles
stdout_callback = yaml
bin_ansible_callbacks = True

[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
```

## Building Images

### Local Build Process

```bash
# 1. Prepare directory structure
cd image/
ls -la
# Should see: .images.yaml, xaas-service.pkr.hcl, playbook/

# 2. Validate Packer configuration
packer validate xaas-service.pkr.hcl

# 3. Initialize Packer (download plugins if needed)
packer init xaas-service.pkr.hcl

# 4. Build image
packer build xaas-service.pkr.hcl

# Build output shows:
# - VM creation
# - Ansible provisioning progress
# - Image export
# - Cleanup
```

**Build Options:**
```bash
# Debug mode (verbose output)
PACKER_LOG=1 packer build xaas-service.pkr.hcl

# Force rebuild (ignore cache)
packer build -force xaas-service.pkr.hcl

# Parallel builds disabled (sequential)
packer build -parallel-builds=1 xaas-service.pkr.hcl

# Set variables
packer build -var 'disk_size=100G' xaas-service.pkr.hcl
```

### CI/CD Integration

**GitLab CI Example:**
```yaml
# .gitlab-ci.yml
stages:
  - validate
  - build
  - upload

validate:packer:
  stage: validate
  image: hashicorp/packer:latest
  script:
    - cd image/
    - packer validate xaas-service.pkr.hcl

build:image:
  stage: build
  image: hashicorp/packer:latest
  script:
    - cd image/
    - packer build xaas-service.pkr.hcl
  artifacts:
    paths:
      - image/output/
    expire_in: 1 week
  only:
    - main
    - tags

upload:vkcloud:
  stage: upload
  script:
    - # Upload image to VK Cloud
    - # Requires VK Cloud credentials
  only:
    - tags
```

## Testing Images

### Local Testing with QEMU

```bash
# After Packer build completes
cd output/

# Boot image with QEMU
qemu-system-x86_64 \
  -m 2048 \
  -smp 2 \
  -drive file=xaas-service.qcow2,format=qcow2 \
  -net nic,model=virtio \
  -net user,hostfwd=tcp::2222-:22 \
  -display none \
  -daemonize

# SSH into VM
ssh -p 2222 ubuntu@localhost

# Verify required packages
which cloud-init curl systemd qemu-ga

# Check services
systemctl status ssh
systemctl status qemu-guest-agent

# Verify no credentials
cat /etc/shadow | grep -v '!'

# Shutdown
shutdown -h now
```

### Image Validation Checklist

Before uploading to VK Cloud:

- [ ] Cloud-init installed and configured
- [ ] Curl available in PATH
- [ ] Systemd is init system
- [ ] Qemu-guest-agent running
- [ ] SSH server enabled and auto-starts
- [ ] VirtIO drivers loaded
- [ ] No default passwords set
- [ ] No hardcoded credentials
- [ ] Firewall disabled
- [ ] Bash history cleared
- [ ] Image size reasonable (<50GB recommended)
- [ ] All required services auto-start
- [ ] Image boots successfully

## Advanced Patterns

### Multi-OS Support

Build images for multiple distributions:

```hcl
# multi-os.pkr.hcl
build {
  source "qemu.ubuntu-24" {
    name = "xaas-service-ubuntu24"
  }

  source "qemu.almalinux-91" {
    name = "xaas-service-almalinux9"
  }

  provisioner "ansible" {
    playbook_file = "./playbook/provision.yml"
    user          = "{{ build.User }}"
    sftp_command  = "/usr/libexec/openssh/sftp-server -e"
    use_proxy     = false
    extra_arguments = [
      "--extra-vars",
      "os_family={{ build.OsFamily }}"
    ]
  }
}
```

### Custom Disk Size

```yaml
# .images.yaml with custom disk size
xaas-large-service:
  metadata:
    os_admin_user: 'ubuntu'
    os_distro: ubuntu2404
    # ... other metadata ...

  build_override:
    disk_size: 100G    # Increase from default 10G
    memory: 4096       # Increase RAM for build
```

### Post-Processors

```hcl
build {
  source "qemu.ubuntu-24" {
    name = "xaas-service"
  }

  provisioner "ansible" {
    playbook_file = "./playbook/provision.yml"
    # ... provisioner config ...
  }

  post-processor "compress" {
    output = "output/xaas-service.tar.gz"
  }

  post-processor "checksum" {
    checksum_types = ["sha256"]
    output         = "output/xaas-service.sha256"
  }
}
```

## Troubleshooting

### Common Issues

**Issue: Ansible connection timeout**
```
Error: timeout waiting for SSH
Solution:
1. Verify SSH server installed in base image
2. Check firewall not blocking port 22
3. Ensure correct os_admin_user in .images.yaml
4. Add boot_wait to allow VM to start
```

**Issue: Qemu-guest-agent not found**
```
Error: qemu-ga: command not found
Solution:
1. Install qemu-guest-agent package
2. Enable service in provision playbook:
   systemctl enable qemu-guest-agent
3. Verify package name for your OS distribution
```

**Issue: Image too large**
```
Warning: Image exceeds recommended size
Solution:
1. Remove unnecessary packages
2. Clean package cache: apt clean
3. Remove logs: rm -rf /var/log/*
4. Zero free space: dd if=/dev/zero of=/zero; rm /zero
5. Use smaller base distribution (Alpine, minimal)
```

**Issue: Packer build hangs during Ansible**
```
Error: Provisioner stuck at task
Solution:
1. Enable Ansible debug: ANSIBLE_DEBUG=1
2. Check task requires interaction (disable)
3. Increase timeout in playbook
4. Verify network connectivity from VM
```

## Best Practices

### Image Security

1. **Minimal Attack Surface**
   - Install only required packages
   - Remove development tools
   - Disable unnecessary services

2. **No Secrets in Image**
   - No hardcoded passwords
   - No API keys or tokens
   - No SSH private keys
   - Use runtime configuration

3. **Regular Updates**
   - Rebuild images regularly
   - Update base OS packages
   - Patch security vulnerabilities
   - Document image versions

### Build Optimization

1. **Layer Caching**
   - Order Ansible tasks by change frequency
   - Separate package installation from configuration
   - Use Ansible handlers for service restarts

2. **Build Speed**
   - Disable fact gathering when not needed
   - Use Ansible pipelining
   - Parallel package installations
   - Local package mirrors

3. **Reproducibility**
   - Pin package versions
   - Use version control for configurations
   - Document build dependencies
   - Tag image builds with versions

### Documentation

Document in your repository:
- Base OS and version
- Installed packages and versions
- Build requirements
- Testing procedures
- Known issues and workarounds
- Changelog between image versions

## References

See `references/` directory for:
- Complete `.images.yaml` examples
- Packer HCL templates
- Ansible provision playbooks
- Build scripts
- Testing procedures

See `assets/` directory for:
- Build process diagrams
- Image structure documentation
- Troubleshooting guides
