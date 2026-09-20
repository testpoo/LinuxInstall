#!/bin/bash

# 声音
volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')
if [[ $(wpctl status| grep 'USB Audio Device 模拟立体声') =~ "MUTED" ]] || [ $volume -eq 0 ];then
    notify-send -t 2000 -h string:x-canonical-private-synchronous:brightness -h int:value:$volume -i display-volume "$volume% 静音"
else
    notify-send -t 2000 -h string:x-canonical-private-synchronous:brightness -h int:value:$volume -i display-volume "$volume% 音量"
fi