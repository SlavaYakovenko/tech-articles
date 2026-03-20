# Connecting at a new hotel

Connect to the router: via cable into ETH2/3/4 or via WiFi `YOUR_SSID`
Open a terminal: `ssh admin@192.168.13.1`

> ℹ️ Each command is entered as a single line and executed by pressing Enter.

---

## Mode A — Hotel WiFi

### 1. Find the hotel SSID
```
/interface/wireless/scan wlan1 duration=5
```

### 2. Run the switching script

**Password-protected WiFi (WPA2):**
```
:global ssid "HOTEL_SSID"
:global password "HOTEL_PASSWORD"
/system/script/run mode-a
```

**Open WiFi (no password):**
```
:global ssid "HOTEL_SSID"
/system/script/run mode-a
```

### 3. Verify the connection
```
/ip/dhcp-client/print
```
Wait for `bound` status. Then:
```
/ping 8.8.8.8 count=4
```

---

## Mode B — Cable from hotel

Plug the cable into **ETH1**, then:
```
/system/script/run mode-b
```
`bound` status on `ether1` — ready.

---

## If DHCP lease is not obtained (Mode A)

```
/ip/dhcp-client/renew [find interface=wlan1]
```
Wait 15 seconds and check again.
