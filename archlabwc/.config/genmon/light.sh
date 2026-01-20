#!/bin/bash

# 亮度
light=$(brightnessctl get | awk '{print $1/192"%"}')

echo "<txt>$light
亮度</txt>"
echo "<tool>亮度</tool>"
echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"