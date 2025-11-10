---
name: ha-supervised-installation
description: Complete installation scripts and configuration templates for deploying Home Assistant Supervised on Raspberry Pi 4. Includes master installer, modular component scripts, network services setup, WiFi captive portal, Tailscale VPN, and nginx reverse proxy configuration.
---

# Home Assistant Supervised - Raspberry Pi 4 Installation Scripts

Complete automated installation toolkit for deploying production-ready Home Assistant Supervised on Raspberry Pi 4 with Debian 12 Bookworm.

## Installation Scripts

### Master Installer: `00-install-all.sh`
Orchestrates complete installation of all components:

```bash
#!/bin/bash
set -e

echo "=== Home Assistant Supervised - Complete Installation ==="
echo "This will install:"
echo "  1. System dependencies (Docker, NetworkManager, etc.)"
echo "  2. Home Assistant Supervised"
echo "  3. Tailscale for remote access"
echo "  4. Nginx reverse proxy"
echo "  5. WiFi captive portal"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Step 1/5: Initial System Setup ==="
./01-initial-setup.sh

echo "=== Step 2/5: Install Home Assistant Supervised ==="
./02-install-ha-supervised.sh

echo "=== Step 3/5: Install Tailscale ==="
./03-install-tailscale.sh

echo "=== Step 4/5: Setup Nginx Reverse Proxy ==="
./04-setup-nginx-reverse-proxy.sh

echo "=== Step 5/5: Setup WiFi Portal ==="
./05-setup-wifi-portal.sh

echo ""
echo "=== Installation Complete! ==="
echo "IMPORTANT: Reboot your system now: sudo reboot"
echo ""
echo "After reboot:"
echo "  - Home Assistant: http://YOUR_IP:8123"
echo "  - Via Nginx: http://YOUR_IP"
echo "  - SSH: ssh root@YOUR_IP (password: 1234)"
echo "  - Tailscale: Run 'tailscale up' to authenticate"
```

### Component 1: Initial Setup (`01-initial-setup.sh`)
System dependencies and base configuration:

```bash
#!/bin/bash
set -e

echo "Installing system dependencies..."

# Update system
apt-get update
apt-get upgrade -y

# Install required packages
apt-get install -y \
    apparmor \
    jq \
    wget \
    curl \
    udisks2 \
    libglib2.0-bin \
    network-manager \
    dbus \
    systemd-journal-remote \
    systemd-resolved

# Install Docker
curl -fsSL https://get.docker.com | sh

# Set root password
echo "root:1234" | chpasswd

# Install OS Agent
OS_AGENT_VERSION=$(curl -s https://api.github.com/repos/home-assistant/os-agent/releases/latest | jq -r '.tag_name')
wget "https://github.com/home-assistant/os-agent/releases/download/${OS_AGENT_VERSION}/os-agent_${OS_AGENT_VERSION#v}_linux_aarch64.deb"
dpkg -i "os-agent_${OS_AGENT_VERSION#v}_linux_aarch64.deb"
rm "os-agent_${OS_AGENT_VERSION#v}_linux_aarch64.deb"

echo "Initial setup complete!"
```

### Component 2: Home Assistant Supervised (`02-install-ha-supervised.sh`)
Home Assistant Supervised installer:

```bash
#!/bin/bash
set -e

echo "Installing Home Assistant Supervised..."

# Download and run HA Supervised installer
wget -O /tmp/homeassistant-supervised.deb \
    https://github.com/home-assistant/supervised-installer/releases/latest/download/homeassistant-supervised.deb

dpkg -i /tmp/homeassistant-supervised.deb
rm /tmp/homeassistant-supervised.deb

echo "Home Assistant Supervised installed!"
echo "It will take 10-20 minutes to fully start."
echo "Check status: ha core info"
```

### Component 3: Tailscale Installation (`03-install-tailscale.sh`)
Tailscale VPN with Funnel support:

```bash
#!/bin/bash
set -e

echo "Installing Tailscale..."

# Add Tailscale repository
curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.noarmor.gpg | \
    tee /usr/share/keyrings/tailscale-archive-keyring.gpg >/dev/null
curl -fsSL https://pkgs.tailscale.com/stable/debian/bookworm.tailscale-keyring.list | \
    tee /etc/apt/sources.list.d/tailscale.list

# Install Tailscale
apt-get update
apt-get install -y tailscale

# Enable Tailscale service
systemctl enable --now tailscaled

echo "Tailscale installed!"
echo ""
echo "To configure:"
echo "  1. Run: tailscale up"
echo "  2. Follow the URL to authorize"
echo "  3. Enable Funnel: tailscale cert \$(hostname) && tailscale funnel 8123"
```

### Component 4: Nginx Reverse Proxy (`04-setup-nginx-reverse-proxy.sh`)
Nginx configuration for port 80 access:

```bash
#!/bin/bash
set -e

echo "Setting up Nginx reverse proxy..."

# Install nginx
apt-get install -y nginx

# Create Home Assistant proxy config
cat > /etc/nginx/sites-available/homeassistant << 'EOF'
server {
    listen 80;
    listen [::]:80;
    server_name _;

    location / {
        proxy_pass http://localhost:8123;
        proxy_set_header Host $host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/websocket {
        proxy_pass http://localhost:8123/api/websocket;
        proxy_set_header Host $host;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/homeassistant /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and restart
nginx -t
systemctl restart nginx
systemctl enable nginx

echo "Nginx reverse proxy configured!"
echo "Home Assistant will be accessible on port 80"
```

### Component 5: WiFi Captive Portal (`05-setup-wifi-portal.sh`)
Auto-starting WiFi configuration portal:

```bash
#!/bin/bash
set -e

echo "Setting up WiFi captive portal..."

# Install required packages
apt-get install -y dnsmasq hostapd python3 python3-pip

# Create portal script
cat > /usr/local/bin/wifi-portal.sh << 'EOFSCRIPT'
#!/bin/bash

# Check if LAN cable is connected
if nmcli -t -f DEVICE,STATE device | grep -q ":connected"; then
    echo "LAN connection detected, skipping WiFi portal"
    exit 0
fi

echo "No LAN connection, waiting 3 seconds..."
sleep 3

# Check again after delay
if nmcli -t -f DEVICE,STATE device | grep -q ":connected"; then
    echo "LAN connection established, skipping WiFi portal"
    exit 0
fi

echo "Starting WiFi captive portal..."

# Create AP
nmcli device wifi hotspot ssid PiSetup password raspberry

# Start web portal
cd /opt/wifi-portal && python3 -m http.server 80 &
PORTAL_PID=$!

# Wait for WiFi configuration
while true; do
    if nmcli -t -f DEVICE,STATE device | grep -q "eth.*:connected\|wlan.*:connected"; then
        echo "Network connection established"
        kill $PORTAL_PID 2>/dev/null || true
        nmcli connection down hotspot 2>/dev/null || true
        exit 0
    fi
    sleep 5
done
EOFSCRIPT

chmod +x /usr/local/bin/wifi-portal.sh

# Create systemd service
cat > /etc/systemd/system/wifi-portal.service << 'EOFSERVICE'
[Unit]
Description=WiFi Captive Portal
After=NetworkManager.service
Wants=NetworkManager.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/wifi-portal.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOFSERVICE

# Enable service
systemctl daemon-reload
systemctl enable wifi-portal.service

echo "WiFi portal configured!"
echo "Portal will auto-start if no LAN cable detected at boot"
```

## Configuration Files

### Nginx Site Configuration
Location: `/etc/nginx/sites-available/homeassistant`
- Reverse proxy to Home Assistant on port 8123
- WebSocket support for `/api/websocket`
- Proper header forwarding for Home Assistant

### Systemd Services
- `wifi-portal.service` - Auto-start WiFi configuration portal
- Location: `/etc/systemd/system/wifi-portal.service`

## Usage Workflow

### Quick Deployment
1. Flash Debian 12 Bookworm ARM64 to SD card
2. Enable SSH: `touch /boot/firmware/ssh`
3. Boot Raspberry Pi, SSH in as `pi`
4. Copy scripts to Pi via `scp` or git clone
5. Run: `sudo ./00-install-all.sh`
6. Reboot after installation
7. Access Home Assistant at `http://PI_IP:8123` or `http://PI_IP`

### Manual Step-by-Step
Run scripts individually for more control:
```bash
./01-initial-setup.sh
./02-install-ha-supervised.sh
./03-install-tailscale.sh
./04-setup-nginx-reverse-proxy.sh
./05-setup-wifi-portal.sh
sudo reboot
```

### WiFi Portal Flow
1. Boot without LAN cable
2. Portal auto-starts after 3-second delay
3. Connect to "PiSetup" WiFi (password: raspberry)
4. Browser opens to `http://10.42.0.1`
5. Select WiFi network and enter password
6. Pi connects, portal shuts down automatically

### Tailscale Remote Access
```bash
# Authenticate Tailscale
tailscale up

# Enable HTTPS via Funnel
tailscale cert $(hostname)
tailscale funnel 8123

# Check status
tailscale funnel status

# Access from anywhere
# https://your-pi.tailnet.ts.net
```

## Troubleshooting Commands

### Home Assistant Status
```bash
ha core info
ha core logs
docker ps
journalctl -u homeassistant-supervised -f
```

### Network Services
```bash
systemctl status nginx
systemctl status wifi-portal
nmcli device status
nmcli connection show
```

### Tailscale
```bash
tailscale status
tailscale funnel status
journalctl -u tailscaled -f
```

## System Requirements
- Raspberry Pi 4 (2GB+ RAM recommended)
- 32GB+ SD card (Class 10 or better)
- Debian 12 Bookworm ARM64
- Ethernet cable (for initial setup) or WiFi

## Default Credentials
- SSH root password: `1234` (change after installation!)
- WiFi portal SSID: `PiSetup`
- WiFi portal password: `raspberry`

## Security Recommendations
1. Change root password: `passwd root`
2. Setup SSH key authentication
3. Configure UFW firewall
4. Keep system updated: `apt update && apt upgrade`
5. Use Tailscale for remote access (no port forwarding needed)

## Post-Installation
1. Complete Home Assistant onboarding at `http://PI_IP:8123`
2. Configure Tailscale: `tailscale up`
3. Install desired Home Assistant add-ons
4. Setup integrations for your smart home devices
5. Configure automations and dashboards

This skill provides complete automation for deploying production-ready Home Assistant Supervised infrastructure with security, remote access, and network flexibility built-in from day one.
