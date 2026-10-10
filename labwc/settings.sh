#!/bin/bash

showdesktop() {
    echo "<txt></txt><txtclick>wtype -M logo -k d</txtclick>"
    echo "<css>.genmon_valuebutton {min-width:2px;border-left:1px solid #bbb;margin-left:2px}</css>"
    echo "<tool>最小化所有打开的窗口并显示桌面</tool>"
}

light() {
    light=$(brightnessctl get | awk '{print $1/192}')
    notify-send -t 2000 -h string:x-canonical-private-synchronous:brightness -h int:value:$light -i display-brightness "$light% 亮度"
}

network() {
    rssi=$(iwctl station wlan0 show | grep AverageRSSI | awk '{print $2}')
    if [ $(iwctl station wlan0 show | grep -F State | awk '{print $2}') = "connected" ];then
        if [ $rssi -ge -60 ];then
            echo "<icon>network-wireless-signal-excellent</icon>"
        elif [ $rssi -lt -61 ] && [ $rssi -ge -70 ];then
            echo "<icon>network-wireless-signal-good</icon>"
        elif [ $rssi -lt -71 ] && [ $rssi -ge -80 ];then
            echo "<icon>network-wireless-signal-ok</icon>"
        else
            echo "<icon>network-wireless-signal-weak</icon>"
        fi
        echo "<tool>网络连接正常 $(iwctl station wlan0 show | grep 'Connected network' | awk -F' ' '{print $3}')</tool>"
    else
	    echo "<icon>network-wireless-offline</icon>"
	    echo "<tool>网络连接失败</tool>"
    fi
    echo "<css>.genmon_image {margin-right:2px;margin-left:2px}</css>"
    echo "<iconclick>wtype -M logo -k n</iconclick>"
}

volume() {
    volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')
    if [[ $(wpctl status| grep 'USB Audio Device 模拟立体声') =~ "MUTED" ]] || [ $volume -eq 0 ];then
        echo "<icon>audio-volume-muted</icon>"
    elif [ $volume -ge 1 ] && [ $volume -le 33 ];then
        echo "<icon>audio-volume-low</icon>"
    elif [ $volume -ge 34 ] && [ $volume -le 66 ];then
        echo "<icon>audio-volume-medium</icon>"
    else
        echo "<icon>audio-volume-high</icon>"
    fi
    echo "<tool>音量：$volume%</tool>"
    echo "<iconclick>wtype -M logo -k v</iconclick>"
    echo "<css>.genmon_image {margin-right:2px;margin-left:2px}</css>"
}

system() {
    echo "<icon>debian-logo</icon><iconclick>wtype -M alt -k f3</iconclick>"
    echo "<tool>所有应用程序</tool>"
}

touchpad() {
    if grep -q "<sendEventsMode>no</sendEventsMode>$" ~/.config/labwc/rc.xml; then
        sed -i "s/<sendEventsMode>no<\/sendEventsMode>/<sendEventsMode>yes<\/sendEventsMode>/" ~/.config/labwc/rc.xml
        labwc -r
    else
        sed -i "s/<sendEventsMode>yes<\/sendEventsMode>/<sendEventsMode>no<\/sendEventsMode>/" ~/.config/labwc/rc.xml
        labwc -r
    fi

    if grep -q "<sendEventsMode>no</sendEventsMode>$" ~/.config/labwc/rc.xml;then
        notify-send -t 2000 -h string:x-canonical-private-synchronous:touchpad "触摸板已关闭"
    else
        notify-send -t 2000 -h string:x-canonical-private-synchronous:touchpad "触摸板已启用"
    fi
}

volume-notify() {
    xfce4-panel --plugin-event=genmon-10:refresh:bool:true
    volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')
    if [[ $(wpctl status| grep 'USB Audio Device 模拟立体声') =~ "MUTED" ]] || [ $volume -eq 0 ];then
        notify-send -t 2000 -h string:x-canonical-private-synchronous:volume -h int:value:$volume -i display-volume "$volume% 静音"
    else
        notify-send -t 2000 -h string:x-canonical-private-synchronous:volume -h int:value:$volume -i display-volume "$volume% 音量"
    fi
}

change-swaybg() {
    sed -i "/^swaybg -i/c\\swaybg -i \"$2\" >/dev/null 2>&1 &" ~/.config/labwc/autostart
    pkill swaybg
    swaybg -i "$2"
}

if [ "$1" = "showdesktop" ]; then
    showdesktop
elif [ "$1" = "light" ]; then
    light
elif [ "$1" = "network" ]; then
    network
elif [ "$1" = "volume" ]; then
    volume
elif [ "$1" = "system" ]; then
    system
elif [ "$1" = "touchpad" ]; then
    touchpad
elif [ "$1" = "volume-notify" ]; then
    volume-notify
elif [ "$1" = "change-swaybg" ]; then
    change-swaybg "$1" "$2"
fi
