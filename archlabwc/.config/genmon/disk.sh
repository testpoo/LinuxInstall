#!/bin/bash

# 磁盘
diskUsage=$(df -h | grep -F "/dev/sda2" | awk '{print $3}')

echo "<txt>$diskUsage
磁盘</txt>"
echo "<tool>磁盘</tool>"
echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"