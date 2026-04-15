# Tech Articles Repository

A collection of technical articles covering networking, IoT, microboards, and development topics.

## Repository Structure

```
tech-articles/
├── README.md
├── pandas-apply-benchmarks/
├── mesh-vpn-raspberry-pi/
├── mesh-vpn-raspberry-pi-part2/
├── mesh-vpn-raspberry-pi-part3/
├── mikrotik-travel-router/
└── [future-articles]/
```

## Articles

### 🔗 [ADR in the AI Epoch](./adr-in-the-ai-epoch/README.md)
Exploring the role of Architecture Decision Records (ADRs) when AI agents are part of the development team. A guide on how to integrate ADRs into AI-driven workflows to prevent memory loss and maintain architectural consistency.

**Topics covered:**
- Architecture Decision Records (ADRs)
- AI agent collaboration
- Knowledge persistence in LLMs
- Project planning with Claude Code

### 🔗 [MikroTik as a Travel Router](./mikrotik-travel-router/README.md)
A practical guide to configuring a MikroTik hAP lite as a travel router for hotels and public networks. Covers two operating modes — WiFi repeater and direct LAN connection — with one-command switching via RouterOS scripts.

**Topics covered:**
- Network isolation and security on public networks
- WiFi repeater mode with virtual AP
- Ethernet WAN mode with automatic DHCP
- RouterOS scripting for mode switching
- Firewall hardening for untrusted environments

### 🔗 [Pandas: Direct Column Calculation vs Masked One](./pandas-apply-benchmarks/README.md)
Performance analysis of two approaches for processing JSON data in pandas DataFrames. A comprehensive benchmark comparing direct apply vs masked filtering approaches with practical recommendations for different scenarios.

**Topics covered:**
- Pandas performance optimization
- JSON parsing strategies
- Boolean indexing mechanics
- Benchmark methodology
- Real-world performance implications

### 🔗 [Mesh VPN for Raspberry Pi](./mesh-vpn-raspberry-pi/README.md)
A practical guide to setting up Tailscale mesh VPN for remote access to Raspberry Pi and other microboards without additional infrastructure. Perfect for developers working with IoT projects and home labs.

**Topics covered:**
- Solving NAT traversal issues
- Tailscale installation and setup
- Mesh networking fundamentals
- Remote access to microboards

### 🔗 [Mesh VPN for Raspberry Pi :: Part 2](./mesh-vpn-raspberry-pi-part2/README.md)
Advanced Tailscale configuration for accessing your entire home network remotely through subnet routing. Learn how to reach any device on your home network from anywhere in the world.

**Topics covered:**
- Subnet routing configuration
- IP forwarding setup
- Multi-location network planning
- Global device access strategies
- Network topology best practices

### 🔗 [Mesh VPN for Raspberry Pi :: Part 3](./mesh-vpn-raspberry-pi-part3/README.md)
Using Tailscale exit nodes to control your public IP address and route internet traffic through specific devices in your mesh network. Perfect for accessing geo-restricted content and securing connections on untrusted networks.

**Topics covered:**
- Exit node configuration
- Public IP address control
- Geographic content access
- Secure internet routing
- Mobile device setup

---

## Series Overview

### **Mesh VPN for Raspberry Pi Series**
A comprehensive guide to building secure, scalable remote access solutions:

1. **Part 1**: Basic mesh VPN setup with device-to-device connectivity
2. **Part 2**: Subnet routing for full network access
3. **Part 3**: Exit nodes for controlled internet access
4. **Part 4**: *(Coming soon)* Advanced security and ACL configuration

### **Data Processing Performance Series**
Practical performance analysis for common data processing scenarios:

1. **Pandas JSON Processing**: Direct apply vs masked filtering comparison

## About

This repository contains technical articles aimed at developers, IoT enthusiasts, data engineers, and programmers interested in practical solutions for common networking, data processing, and development challenges.

## Contributing

Feel free to suggest improvements or report issues through GitHub issues.

## License

All content is provided for educational purposes.