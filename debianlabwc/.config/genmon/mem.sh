#!/bin/bash

# 内存
mem_used_persent=$(free -m | grep -F "内存" | awk '{printf "%.1f",$3/1024}')"G"

echo "<txt>$mem_used_persent
内存</txt>"
echo "<tool>内存占用$mem_used_persent</tool>"
echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"