#!/bin/bash

# 声音
volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')"%"
temp=$(wpctl status| grep '内置音频 模拟立体声')
if [[ $temp =~ "MUTED" ]];then volume="🔇"$volume;else volume="🔊"$volume;fi

echo "<txt>$volume</txt>"
echo "<tool>声音</tool>"