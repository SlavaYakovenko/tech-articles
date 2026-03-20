# ============================================================
# Mode B: Ethernet WAN (ether1 подключен к кабелю отеля)
# ============================================================
# Использование:
#   /system/script/run mode-b
# ============================================================

:log info "mode-b: switching to Ethernet WAN"

# Отключить DHCP на wlan1
/ip/dhcp-client/disable [find interface=wlan1]

# Переключить wlan1 в AP режим (нужен как мастер для wlan2)
/interface/wireless/set wlan1 mode=ap-bridge

# Убрать wlan1 из WAN list
/interface/list/member/remove [find interface=wlan1 list=WAN]

# Включить DHCP на ether1
/ip/dhcp-client/enable [find interface=ether1]

:delay 3s
:put ">>> Mode B активирован (Ethernet WAN)"
:put ">>> Подключите кабель к ETH1"
:put ">>> Статус DHCP:"
/ip/dhcp-client/print
