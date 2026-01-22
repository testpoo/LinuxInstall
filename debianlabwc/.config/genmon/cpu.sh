#!/bin/bash

# CPU
cpuUsage=$(top -b -n1 | grep -F "Cpu" | awk '{printf "%d", 100-$8}')"%"

echo "<txt>$cpuUsage
CPU</txt>"
echo "<tool>CPU占用$cpuUsage</tool>"
echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"