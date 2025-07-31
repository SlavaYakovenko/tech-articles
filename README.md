# Tech Articles Repository

A collection of technical articles covering networking, IoT, microboards, and development topics.

## Repository Structure

```
tech-articles/
├── README.md                           # This file
├── mesh-vpn-raspberry-pi/
│   ├── README.md                      # Part 1: Basic Tailscale setup
│   ├── images/
│   │   ├── raspberripi-tailscale-network-diagram-1.png
│   │   ├── raspberripi-tailscale-network-diagram-2.png
│   │   └── raspberripi-tailscale-network-diagram-3.png
│   └── assets/
│       └── tailscale-commands.sh
├── mesh-vpn-raspberry-pi-part2/
│   ├── README.md                      # Part 2: Subnet routing
│   ├── images/
│   │   ├── raspberripi-tailscale-network-diagram-4.png
│   │   └── raspberripi-tailscale-network-diagram-5.png
│   └── assets/
│       └── subnet-routing-commands.sh
└── [future-articles]/
    ├── README.md
    └── images/
```

## Articles

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

---

## Series Overview

The **Mesh VPN for Raspberry Pi** series provides a comprehensive guide to building secure, scalable remote access solutions:

1. **Part 1**: Basic mesh VPN setup with device-to-device connectivity
2. **Part 2**: Subnet routing for full network access
3. **Part 3**: *(Coming soon)* Exit nodes and advanced security

## About

This repository contains technical articles aimed at developers, IoT enthusiasts, and programmers interested in practical solutions for common networking and development challenges.

## Contributing

Feel free to suggest improvements or report issues through GitHub issues.

## License

All content is provided for educational purposes.