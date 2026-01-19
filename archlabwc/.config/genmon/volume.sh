#!/bin/bash

# 声音
volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')"%"
if [ $(wpctl status| grep '57.'|awk -F ' ' '{print $8}') = "MUTED]" ];then volume="🔇"$volume;else volume="🔊"$volume;fi

echo "<txt>$volume</txt>"
echo "<tool>声音</tool>"