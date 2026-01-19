#!/bin/bash

# 亮度
light="🔆"$(brightnessctl get | awk '{print $1/192"%"}')

echo "<txt>$light</txt>"
echo "<tool>亮度</tool>"