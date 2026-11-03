#!/bin/bash

light-notify() {
    light=$(brightnessctl get | awk '{print $1/192}')
    notify-send -t 2000 -h string:x-canonical-private-synchronous:brightness -h int:value:$light -i display-brightness "$light% 亮度"
}

touchpad-notify() {
    if grep -q "<sendEventsMode>no</sendEventsMode>$" ~/.config/labwc/rc.xml; then
        sed -i "s/<sendEventsMode>no<\/sendEventsMode>/<sendEventsMode>yes<\/sendEventsMode>/" ~/.config/labwc/rc.xml
        labwc -r
        notify-send -t 2000 -h string:x-canonical-private-synchronous:touchpad "触摸板已启用"
    else
        sed -i "s/<sendEventsMode>yes<\/sendEventsMode>/<sendEventsMode>no<\/sendEventsMode>/" ~/.config/labwc/rc.xml
        labwc -r
        notify-send -t 2000 -h string:x-canonical-private-synchronous:touchpad "触摸板已关闭"
    fi
}

volume-notify() {
    volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')
    if [[ $(wpctl get-volume @DEFAULT_AUDIO_SINK@) =~ "MUTED" ]] || [ $volume -eq 0 ];then
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

showdesktop() {
    echo "<txt></txt><txtclick>wtype -M logo -k d</txtclick>"
    echo "<css>.genmon_valuebutton {min-width:2px;border-left:1px solid #bbb;margin-left:2px}</css>"
    echo "<tool>最小化所有打开的窗口并显示桌面</tool>"
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
    echo "<iconclick>wtype -M logo -k 2</iconclick>"
}

volume() {
    volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')
    if [[ $(wpctl get-volume @DEFAULT_AUDIO_SINK@) =~ "MUTED" ]] || [ $volume -eq 0 ];then
        echo "<icon>audio-volume-muted</icon>"
    elif [ $volume -ge 1 ] && [ $volume -le 33 ];then
        echo "<icon>audio-volume-low</icon>"
    elif [ $volume -ge 34 ] && [ $volume -le 66 ];then
        echo "<icon>audio-volume-medium</icon>"
    else
        echo "<icon>audio-volume-high</icon>"
    fi
    echo "<tool>音量：$volume%</tool>"
    echo "<iconclick>wtype -M logo -k 4</iconclick>"
    echo "<css>.genmon_image {margin-right:2px;margin-left:2px}</css>"
}

system() {
    echo "<icon>debian-logo</icon><iconclick>wtype -M logo -k s</iconclick>"
    echo "<tool>系统：$(uname -s)
用户名：$(whoami)
Shell：$SHELL
运行时间：$(uptime -p |awk -F' ' '{print $2,$3,$4,$5}')
包数量：$(dpkg -l |wc -l)
分辨率：$(wlr-randr |awk '/Modes:/{getline; print}' |awk -F' ' '{print $1}')
磁盘：$(cat /proc/partitions |grep -w "sda" | awk -F' ' '{print $3}' |awk '{printf "%.1f",$1/1024/1024}')GB
设备名称：$(hostname)
操作系统名称：$(lsb_release -si)
操作系统类型：$(uname -m)
发型版：$(lsb_release -sd)
发型版版本：$(cat /etc/os-release |grep VERSION_CODENAME |awk -F'=' '{print $2}')
内核版本：$(uname -r)
处理器：$(cat /proc/cpuinfo |grep "model name" |head -n 1 |awk -F ': ' '{print $2}') $(cat /proc/cpuinfo |grep "physical id"|uniq |wc -l)C $(grep 'core id' /proc/cpuinfo | sort -u |wc -l)核 $(grep 'processor' /proc/cpuinfo |wc -l)线程
内存：$(cat /proc/meminfo |grep "MemTotal" |cut -f2 -d:|awk -F' ' '{print int($1)}' |awk '{printf "%.1f",$1/1024/1024}')GB
GPU：$(lspci |grep -i vga |awk -F ': ' '{print $2}')
主板：$(cat /sys/devices/virtual/dmi/id/board_vendor) $(cat /sys/devices/virtual/dmi/id/board_name)
网卡：$(lspci |grep -i 'Network controller' |awk -F'Co., Ltd. ' '{print $2}')
声卡：$(lspci |grep -i audio |awk -F': ' '{print $2}')</tool>"
}

light() {
    light=$(brightnessctl get | awk '{print $1/192}')
    echo "<icon>display-brightness-symbolic</icon>"
    echo "<tool>亮度：$light%</tool>"
    echo "<css>.genmon_image {margin-right:2px;margin-left:2px}</css>"
}

touchpad() {
    if grep -q "<sendEventsMode>no</sendEventsMode>$" ~/.config/labwc/rc.xml; then
        echo "<icon>touchpad-disabled-symbolic</icon>"
        echo "<tool>触摸板关闭</tool>"
    else
        echo "<icon>input-touchpad-symbolic</icon>"
        echo "<tool>触摸板打开</tool>"
    fi
    echo "<iconclick>sh -c '/home/poo/.config/labwc/settings.sh touchpad-notify;xfce4-panel --plugin-event=genmon-19:refresh:bool:true'</iconclick>"
    echo "<css>.genmon_image {margin-right:2px;margin-left:2px}</css>"
}

bluetooth() {
    if [[ $(bluetoothctl devices Connected) != "" ]] && [[ $(bluetoothctl show | grep 'Powered:' | awk -F': ' '{print $2}') = "yes" ]];then
        echo "<icon>bluetooth-active</icon>"
        echo "<tool>蓝牙已连接</tool>"
    elif [[ $(bluetoothctl devices Connected) = "" ]] && [[ $(bluetoothctl show | grep 'Powered:' | awk -F': ' '{print $2}') = "yes" ]];then
        echo "<icon>bluetooth</icon>"
        echo "<tool>蓝牙未连接</tool>"
    else
        echo "<icon>bluetooth-disabled</icon>"
        echo "<tool>蓝牙已关闭</tool>"
    fi
    echo "<iconclick>wtype -M logo -k 3</iconclick>"
    echo "<css>.genmon_image {margin-right:2px;margin-left:2px}</css>"
}

if [ "$1" = "light-notify" ]; then
    light-notify
elif [ "$1" = "touchpad-notify" ]; then
    touchpad-notify
elif [ "$1" = "volume-notify" ]; then
    volume-notify
elif [ "$1" = "change-swaybg" ]; then
    change-swaybg "$1" "$2"
elif [ "$1" = "showdesktop" ]; then
    showdesktop
elif [ "$1" = "network" ]; then
    network
elif [ "$1" = "volume" ]; then
    volume
elif [ "$1" = "light" ]; then
    light
elif [ "$1" = "touchpad" ]; then
    touchpad
elif [ "$1" = "bluetooth" ]; then
    bluetooth
fi
