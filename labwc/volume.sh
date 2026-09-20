#!/bin/bash

# 声音
volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')
if [[ $(wpctl status| grep 'USB Audio Device 模拟立体声') =~ "MUTED" ]] || [ $volume -eq 0 ];then
    echo "<icon>audio-volume-muted-symbolic</icon><txt> </txt>"
elif [ $volume -ge 1 ] && [ $volume -le 33 ];then
    echo "<icon>audio-volume-low-symbolic</icon><txt> </txt>"
elif [ $volume -ge 34 ] && [ $volume -le 66 ];then
    echo "<icon>audio-volume-medium-symbolic</icon><txt> </txt>"
else
    echo "<icon>audio-volume-high-symbolic</icon><txt> </txt>"
fi
echo "<tool>音量：$volume%</tool>"
