#!/bin/bash

echo "<icon>wine</icon><iconclick>wtype -M win p -m win</iconclick>"
echo "<tool>系统: $(uname -s)
用户名: $(whoami)
Shell: $SHELL
运行时间: $(uptime -p |awk -F' ' '{print $2,$3,$4,$5}')
包数量: $(pacman -Q|awk 'END {print NR}')
分辨率: $(cat /sys/class/drm/card1-eDP-1/modes)
磁盘: $(cat /proc/partitions |grep -w "sda" | awk -F' ' '{print $3}' |awk '{printf "%.1f",$1/1024/1024}')GB
设备: $(uname -n)
操作系统名称: $(hostnamectl|grep 'Operating System'| awk -F ': ' '{print $2}')
操作系统类型: $(uname -m)
发型版: $(uname -o)
核心版本: $(uname -r)
处理器: $(cat /proc/cpuinfo |grep "model name" |cut -f2 -d: |head -n 1 |cut -c 2-) $(cat /proc/cpuinfo |grep "physical id"|uniq |wc -l)C $(grep 'core id' /proc/cpuinfo | sort -u |wc -l)核 $(grep 'processor' /proc/cpuinfo |wc -l)线程
内存: $(cat /proc/meminfo |grep "MemTotal" |cut -f2 -d:|awk -F' ' '{print int($1)}' |awk '{printf "%.1f",$1/1024/1024}')GB
GPU: $(lspci |grep -i vga | awk -F'00:02.0 VGA compatible controller: ' '{print $2}')
主板: $(cat /sys/devices/virtual/dmi/id/board_vendor) $(cat /sys/devices/virtual/dmi/id/board_name)</tool>"