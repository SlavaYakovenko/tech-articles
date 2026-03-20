# MikroTik hAP lite — Travel Router: Complete Setup Guide

**Hardware:** MikroTik hAP lite, RouterOS 7.x
**Goal:** travel router with two operating modes

---

## Architecture

```
                   MODE B (cable)
                   ether1 ──── [Hotel/Office LAN]
                       │
[MikroTik hAP lite]   NAT
                       │
              bridge (192.168.13.1/24)
              ├── ether2 / ether3 / ether4
              └── wlan2 (AP: YOUR_SSID, WPA2)
                       │
                [Your devices]
                 192.168.13.x


                   MODE A (WiFi repeater)
              wlan1 (station) ──── [Hotel WiFi]
                       │
[MikroTik hAP lite]   NAT
                       │
              bridge (192.168.13.1/24)
              ├── ether2 / ether3 / ether4
              └── wlan2 (AP: YOUR_SSID, WPA2)
                       │
                [Your devices]
                 192.168.13.x
```

**Key parameters:**
| Parameter | Value |
|-----------|-------|
| Router management | http://192.168.13.1 |
| LAN subnet | 192.168.13.0/24 |
| DHCP pool | 192.168.13.10 – 192.168.13.254 |
| Personal WiFi network | YOUR_SSID (WPA2) |
| WiFi client mode | station (NOT station-pseudobridge!) |

> ⚠️ **MikroTik Terminal:** each command is entered as a single line. Multi-line input via copy-paste does not work in SSH.

---

## Part 1 — Initial Setup (done once)

### Step 1 — Factory Reset

**Hardware reset (recommended):**
1. Power off the router
2. Press and hold the `Reset` button (small button on the back)
3. While holding the button, power on the router
4. Hold for ~5 seconds until the LED blinks rapidly
5. Release

The router will boot with the MikroTik default configuration. IP: `192.168.88.1`

> ⚠️ Do not use WebFig → System → Reset with the "No Default Configuration" flag — the router will become unreachable without Winbox.

---

### Step 2 — Change IP to 192.168.13.1

1. Connect via cable to ETH2/3/4 (not ETH1)
2. Open http://192.168.88.1 → log in as `admin` (password is empty)
3. **WebFig → Quick Set**
4. Change `IP Address` from `192.168.88.1` to `192.168.13.1` and set the subnet mask
5. Click Apply

Reconnect to http://192.168.13.1

---

### Step 3 — Change admin password

Via WebFig: **System → Users → admin → Password**

Or via SSH/Terminal:
```
/user/set admin password="YOUR_PASSWORD"
```

---

### Step 4 — Verify basic LAN configuration

The MikroTik default configuration already contains what is needed. Verify:

```
/interface/bridge/port/print
/ip/address/print
/ip/dhcp-server/print
/ip/pool/print
```

Expected result:
- `bridge` contains: `ether2`, `ether3`, `ether4`, `wlan1`
- IP on bridge: `192.168.13.1/24`
- DHCP server on `bridge`, pool: `192.168.13.10-192.168.13.254`

---

### Step 5 — Configure personal WiFi network (SSID + WPA2)

```
/interface/wireless/security-profiles/set [find name=default] mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key="YOUR_WIFI_PASSWORD"
```

```
/interface/wireless/set wlan1 ssid="YOUR_SSID" disabled=no
```

---

### Step 6 — Create VirtualAP (wlan2) for Mode A

In Mode A, `wlan1` becomes a client (station), so a separate virtual AP is needed to serve WiFi to clients.

```
/interface/wireless/add master-interface=wlan1 name=wlan2 ssid="YOUR_SSID" security-profile=default mode=ap-bridge disabled=no
```

---

### Step 7 — Reconfigure bridge: wlan1 → wlan2

```
/interface/bridge/port/remove [find interface=wlan1]
```
```
/interface/bridge/port/add bridge=bridge interface=wlan2
```

Verify:
```
/interface/bridge/port/print
```
Bridge should contain: `ether2`, `ether3`, `ether4`, `wlan2`

---

### Step 8 — Firewall: allow DHCP on WAN interfaces

```
/ip/firewall/filter/add chain=input protocol=udp dst-port=68 in-interface-list=WAN action=accept place-before=5 comment="allow DHCP client on WAN"
```

---

### Step 9 — Create security profile for hotel WiFi

```
/interface/wireless/security-profiles/add name=hotel mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key=""
```

---

### Step 10 — Initial activation of Mode A

```
/interface/wireless/set wlan1 mode=station ssid="HOTEL_SSID" security-profile=hotel bridge-mode=enabled
```
```
/ip/dhcp-client/add interface=wlan1 add-default-route=yes use-peer-dns=yes disabled=no
```
```
/interface/list/member/add list=WAN interface=wlan1
```

> ⚠️ Use `mode=station`, NOT `mode=station-pseudobridge`. Pseudobridge causes DHCP issues with some APs (TP-Link Mesh, Xiaomi).

---

### Step 11 — Install mode-switching scripts

Scripts are installed once. Each command is a single line:

**mode-b (Ethernet WAN):**
```
/system/script/add name=mode-b source="/ip/dhcp-client/disable [find interface=wlan1]\n/interface/wireless/set wlan1 mode=ap-bridge\n/interface/list/member/remove [find interface=wlan1 list=WAN]\n/ip/dhcp-client/enable [find interface=ether1]\n:delay 3s\n:put \"Mode B activated\"\n/ip/dhcp-client/print"
```

**mode-a (WiFi repeater):**
```
/system/script/add name=mode-a source=":global ssid\n:global password\n:if ([:len \$ssid] = 0) do={ :error \"Set :global ssid first\" }\n:if ([:len \$password] > 0) do={ /interface/wireless/security-profiles/set [find name=hotel] mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key=\$password } else={ /interface/wireless/security-profiles/set [find name=hotel] mode=none }\n/ip/dhcp-client/disable [find interface=ether1]\n/interface/wireless/set wlan1 mode=station ssid=\$ssid security-profile=hotel\n/ip/dhcp-client/enable [find interface=wlan1]\n:if ([:len [/interface/list/member/find interface=wlan1 list=WAN]] = 0) do={ /interface/list/member/add list=WAN interface=wlan1 }\n:set ssid \"\"\n:set password \"\"\n:delay 3s\n:put \"Mode A activated\"\n/ip/dhcp-client/print"
```

Verify:
```
/system/script/print
```

---

### Step 12 — Firewall: brute force protection and router stealth

**ICMP from LAN only** (router does not respond to pings from the hotel network):
```
/ip/firewall/filter/set [find comment="defconf: accept ICMP"] in-interface-list=LAN
```

**SSH brute force protection** (5 attempts in 2 min → 1-hour block). Each command is a separate line:
```
/ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new action=add-src-to-address-list address-list=ssh-stage1 address-list-timeout=2m comment="ssh-bf: stage1"
```
```
/ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new src-address-list=ssh-stage1 action=add-src-to-address-list address-list=ssh-stage2 address-list-timeout=2m comment="ssh-bf: stage2"
```
```
/ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new src-address-list=ssh-stage2 action=add-src-to-address-list address-list=ssh-stage3 address-list-timeout=2m comment="ssh-bf: stage3"
```
```
/ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new src-address-list=ssh-stage3 action=add-src-to-address-list address-list=ssh-stage4 address-list-timeout=2m comment="ssh-bf: stage4"
```
```
/ip/firewall/filter/add chain=input protocol=tcp dst-port=22 connection-state=new src-address-list=ssh-stage4 action=add-src-to-address-list address-list=ssh-blacklist address-list-timeout=1h comment="ssh-bf: blacklist"
```
```
/ip/firewall/filter/add chain=input protocol=tcp dst-port=22 src-address-list=ssh-blacklist action=drop comment="ssh-bf: drop blacklisted"
```

Move stage1 to the first position:
```
/ip/firewall/filter/move [find comment="ssh-bf: stage1"] destination=1
```

Verify:
```
/ip/firewall/filter/print
```

---

## Part 2 — Daily use at a hotel

See [HOTEL-CONNECT.en.md](HOTEL-CONNECT.en.md)

---

## Important notes

### ⚠️ station vs station-pseudobridge
Use `mode=station`, NOT `mode=station-pseudobridge`.

`station-pseudobridge` is designed for transparent L2 bridging when clients need to be in the same subnet as the hotel. In our case NAT is used, so `station` is the correct choice. `station-pseudobridge` causes DHCP issues with some APs (TP-Link, Xiaomi Mesh).

### ℹ️ Captive Portal (hotels with browser-based authentication)
Works without any additional configuration. After connecting to the hotel WiFi, open a browser on any device — the login page will appear automatically.

### ℹ️ Router management
- WebFig: http://192.168.13.1
- SSH: `ssh admin@192.168.13.1`
- Connect via ETH2/3/4 or via WiFi YOUR_SSID

---

## Diagnostics

| Problem | Command |
|---------|---------|
| No DHCP from hotel | `/ip/dhcp-client/print` |
| WiFi does not see networks | `/interface/wireless/scan wlan1 duration=5` |
| No association with AP | `/interface/wireless/registration-table/print` |
| No internet | `/ping 8.8.8.8 count=4` |
| Check NAT | `/ip/firewall/nat/print` |
| Check routes | `/ip/route/print` |
| Sniff DHCP packets | `/tool/sniffer/quick interface=wlan1 port=67,68 duration=10` |
