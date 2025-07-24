#!/bin/bash

# Tailscale Setup Commands for Raspberry Pi
# Save this file as: mesh-vpn-raspberry-pi/assets/tailscale-commands.sh

echo "=== Tailscale Installation and Setup ==="

# Update system packages
echo "Updating system packages..."
sudo apt update

# Install Tailscale
echo "Installing Tailscale..."
sudo apt install tailscale

# Launch Tailscale (will provide authorization URL)
echo "Starting Tailscale (follow the authorization link)..."
sudo tailscale up

echo ""
echo "=== Useful Tailscale Commands ==="

# Check Tailscale status
echo "Check status:"
echo "tailscale status"

# Show assigned IP addresses
echo ""
echo "Show IP addresses:"
echo "tailscale ip"

# Test connectivity to another node
echo ""
echo "Test connection to specific node:"
echo "tailscale ping [node-name-or-ip]"

# Show network map
echo ""
echo "Show network topology:"
echo "tailscale netmap"

# Logout from Tailscale
echo ""
echo "Logout (if needed):"
echo "sudo tailscale logout"

# Show help
echo ""
echo "Get help:"
echo "tailscale help"

echo ""
echo "=== Post-Setup Verification ==="
echo "1. Run 'tailscale status' to see connected devices"
echo "2. Note the Tailscale IP (100.x.x.x) assigned to your Pi"
echo "3. Test SSH connection using the Tailscale IP"
echo "4. Verify bidirectional connectivity"