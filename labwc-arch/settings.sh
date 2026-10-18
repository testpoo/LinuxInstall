#!/bin/bash

light() {
    light=$(brightnessctl get | awk '{print $1/192}')
    notify-send -t 2000 -h string:x-canonical-private-synchronous:brightness -h int:value:$light -i display-brightness "$light% 亮度"
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

if [ "$1" = "light" ]; then
    light
elif [ "$1" = "touchpad" ]; then
    touchpad
elif [ "$1" = "volume-notify" ]; then
    volume-notify
elif [ "$1" = "change-swaybg" ]; then
    change-swaybg "$1" "$2"
fi
