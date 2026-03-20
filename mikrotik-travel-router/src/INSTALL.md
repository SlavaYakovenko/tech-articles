# Установка скриптов на роутер

Выполните один раз через `ssh admin@192.168.13.1`

> ⚠️ Каждая команда — одна строка целиком. Не вставляйте многострочно.

## Установка mode-b (Ethernet WAN)

```
/system/script/add name=mode-b source="/ip/dhcp-client/disable [find interface=wlan1]\n/interface/wireless/set wlan1 mode=ap-bridge\n/interface/list/member/remove [find interface=wlan1 list=WAN]\n/ip/dhcp-client/enable [find interface=ether1]\n:delay 3s\n:put \"Mode B activated\"\n/ip/dhcp-client/print"
```

## Установка mode-a (WiFi repeater)

```
/system/script/add name=mode-a source=":global ssid\n:global password\n:if ([:len \$ssid] = 0) do={ :error \"Set :global ssid first\" }\n:if ([:len \$password] > 0) do={ /interface/wireless/security-profiles/set [find name=hotel] mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key=\$password } else={ /interface/wireless/security-profiles/set [find name=hotel] mode=none }\n/ip/dhcp-client/disable [find interface=ether1]\n/interface/wireless/set wlan1 mode=station ssid=\$ssid security-profile=hotel\n/ip/dhcp-client/enable [find interface=wlan1]\n:if ([:len [/interface/list/member/find interface=wlan1 list=WAN]] = 0) do={ /interface/list/member/add list=WAN interface=wlan1 }\n:set ssid \"\"\n:set password \"\"\n:delay 3s\n:put \"Mode A activated\"\n/ip/dhcp-client/print"
```

## Проверка установки

```
/system/script/print
```

---

## Использование

### Режим A — WiFi отеля с паролем (WPA2)
```
:global ssid "SSID_ОТЕЛЯ"
:global password "ПАРОЛЬ_ОТЕЛЯ"
/system/script/run mode-a
```

### Режим A — открытый WiFi (без пароля)
```
:global ssid "SSID_ОТЕЛЯ"
/system/script/run mode-a
```

### Режим B — кабель в ETH1
```
/system/script/run mode-b
```
