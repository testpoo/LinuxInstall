#!/bin/bash

# 磁盘
diskUsage=$(df -P|grep '/dev/sda'|awk '{sum+=$3} END {print sum/1024/1024}'| awk '{printf "%.1f",$1}')G
diskUsage1=$(df -h | grep -F "/dev/sda1" | awk '{print $3}')
diskUsage2=$(df -h | grep -F "/dev/sda2" | awk '{print $3}')
diskUsage3=$(df -h | grep -F "/dev/sda3" | awk '{print $3}')

echo "<txt>$diskUsage
磁盘</txt>"
echo "<tool>/boot   $diskUsage1
/           $diskUsage2
/home $diskUsage3</tool>"
echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"