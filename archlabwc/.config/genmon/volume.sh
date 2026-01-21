#!/bin/bash

# 声音
volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')"%"
if [[ $(wpctl status| grep '内置音频 模拟立体声') =~ "MUTED" ]];then
    echo "<txt>$volume
静音</txt>"
    echo "<css>.genmon_value {background:#E0E0E0;color:#FF0000;font-size:11px;min-width:35px;margin-left:1px}</css>"
else
    echo "<txt>$volume
声音</txt>"
    echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"
fi
echo "<tool>声音</tool>"
