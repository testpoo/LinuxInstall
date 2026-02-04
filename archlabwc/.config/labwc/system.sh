#!/bin/bash

echo -e "系统：$(uname -s)
用户名：$(whoami)
Shell：$SHELL
运行时间：$(uptime -p |awk -F' ' '{print $2,$3,$4,$5}')
包数量：$(pacman -Q|awk 'END {print NR}')
分辨率：$(cat /sys/class/drm/card1-eDP-1/modes)
磁盘：$(cat /proc/partitions |grep -w "sda" | awk -F' ' '{print $3}' |awk '{printf "%.1f",$1/1024/1024}')GB
设备名称：$(uname -n)
操作系统名称：$(hostnamectl|grep 'Static hostname'| awk -F ': ' '{print $2}')
操作系统类型：$(uname -m)
发型版: $(hostnamectl|grep 'Operating System'| awk -F ': ' '{print $2}')
发型版版本：$(cat /etc/os-release |grep 'BUILD_ID' |awk -F'=' '{print $2}')
内核版本：$(uname -r)
处理器：$(cat /proc/cpuinfo |grep "model name" |head -n 1 |awk -F': ' '{print $2}') $(cat /proc/cpuinfo |grep "physical id"|uniq |wc -l)C $(grep 'core id' /proc/cpuinfo | sort -u |wc -l)核 $(grep 'processor' /proc/cpuinfo |wc -l)线程
内存：$(cat /proc/meminfo |grep "MemTotal" |cut -f2 -d:|awk -F' ' '{print int($1)}' |awk '{printf "%.1f",$1/1024/1024}')GB
GPU：$(lspci |grep -i vga | awk -F' VGA compatible controller: ' '{print $2}')
主板：$(cat /sys/devices/virtual/dmi/id/board_vendor) $(cat /sys/devices/virtual/dmi/id/board_name)
网卡：$(lspci |grep -i 'Network controller' |awk -F'Co., Ltd. ' '{print $2}')
声卡：$(lspci |grep -i audio |awk -F': ' '{print $2}')"
exec /bin/bash