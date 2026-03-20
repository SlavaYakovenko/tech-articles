# ============================================================
# Mode A: WiFi Repeater (wlan1 подключается к WiFi отеля)
# ============================================================
# Использование:
#   :global ssid "SSID_ОТЕЛЯ"
#   :global password "ПАРОЛЬ"       # не нужно для открытых сетей
#   /system/script/run mode-a
# ============================================================

:global ssid
:global password

# Проверка что SSID задан
:if ([:len $ssid] = 0) do={
  :error "Укажите SSID: :global ssid \"HOTEL_SSID\""
}

:log info ("mode-a: switching to WiFi repeater, SSID=" . $ssid)

# Настроить security profile
:if ([:len $password] > 0) do={
  /interface/wireless/security-profiles/set [find name=hotel] \
    mode=dynamic-keys \
    authentication-types=wpa2-psk \
    wpa2-pre-shared-key=$password
} else={
  /interface/wireless/security-profiles/set [find name=hotel] mode=none
}

# Отключить DHCP на ether1
/ip/dhcp-client/disable [find interface=ether1]

# Переключить wlan1 в station mode
/interface/wireless/set wlan1 mode=station ssid=$ssid security-profile=hotel

# Включить DHCP на wlan1
/ip/dhcp-client/enable [find interface=wlan1]

# Добавить wlan1 в WAN list (если ещё нет)
:if ([:len [/interface/list/member/find interface=wlan1 list=WAN]] = 0) do={
  /interface/list/member/add list=WAN interface=wlan1
}

# Очистить глобальные переменные
:set ssid ""
:set password ""

:delay 3s
:put ">>> Mode A активирован (WiFi repeater)"
:put ">>> Статус DHCP:"
/ip/dhcp-client/print
