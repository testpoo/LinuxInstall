#!/bin/bash

# 内存
mem_used_persent="Ⓜ️"$(free -m | grep -F "内存" | awk '{printf "%.1f",$3/1024}')"G"

echo "<txt>$mem_used_persent</txt>"
echo "<tool>内存</tool>"