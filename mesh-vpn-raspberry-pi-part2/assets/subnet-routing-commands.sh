#!/bin/bash

# Tailscale Subnet Routing Setup Commands
# Save this file as: mesh-vpn-raspberry-pi-part2/assets/subnet-routing-commands.sh

echo "=== Configuring IP Forwarding ==="

# Enable IPv4 forwarding
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf

# Enable IPv6 forwarding  
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.conf

# Apply changes
sudo sysctl -p /etc/sysctl.conf

echo ""
echo "=== Advertising Subnet Routes ==="

# Advertise home network subnet (adjust IP range as needed)
sudo tailscale up --advertise-routes=192.168.8.0/24

echo ""
echo "=== Verification Commands ==="

# Check Tailscale status
echo "Check routes status:"
echo "tailscale status"

# Test connectivity to home devices
echo ""
echo "Test connectivity to home devices:"
echo "ping 192.168.8.12  # Example: NAS"
echo "ping 192.168.8.11  # Example: IP Camera"

echo ""
echo "=== Next Steps ==="
echo "1. Go to https://login.tailscale.com/admin/machines"
echo "2. Find your Raspberry Pi in the machine list"
echo "3. Enable 'Subnet routes' for advertised networks"
echo "4. Test connectivity from remote location"
