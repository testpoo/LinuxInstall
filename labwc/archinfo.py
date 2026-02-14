#!/usr/bin/env python3
# coding=utf-8

import os

infoa = "用户名：" + os.popen("whoami").read().replace('\n','')
infob = "Shell：" + os.popen("echo -e $SHELL").read().replace('\n','')
infoc = "运行时间：" + os.popen("uptime -p |awk -F' ' '{print $2,$3,$4,$5}'").read().replace('\n','')
infod = "包数量：" + os.popen("pacman -Q|awk 'END {print NR}'").read().replace('\n','')
infoe = "分辨率：" + os.popen("cat /sys/class/drm/card1-eDP-1/modes").read().replace('\n','')
infof = "磁盘：" + os.popen("cat /proc/partitions |grep -w 'sda' | awk -F' ' '{print $3}' |awk '{printf \"%.1f\",$1/1024/1024}'").read().replace('\n','') + "GB"
infog = "设备名称：" + os.popen("uname -n").read().replace('\n','')
infoh = "操作系统名称：" + os.popen("hostnamectl|grep 'Static hostname'| awk -F ': ' '{print $2}'").read().replace('\n','')
infoi = "操作系统类型：" + os.popen("uname -m").read().replace('\n','')
infoj = "发型版: " + os.popen("hostnamectl|grep 'Operating System'| awk -F ': ' '{print $2}'").read().replace('\n','')
infok = "发型版版本：" + os.popen("cat /etc/os-release |grep 'BUILD_ID' |awk -F'=' '{print $2}'").read().replace('\n','')
infol = "内核版本：" + os.popen("uname -r").read().replace('\n','')
infom = "处理器：" + os.popen("cat /proc/cpuinfo |grep 'model name' |head -n 1 |awk -F': ' '{print $2}'").read() + os.popen("cat /proc/cpuinfo |grep 'physical id'|uniq |wc -l").read().replace('\n','') +"C " + os.popen("grep 'core id' /proc/cpuinfo | sort -u |wc -l").read().replace('\n','') + "核 " + os.popen("grep 'processor' /proc/cpuinfo |wc -l").read().replace('\n','') + "线程"
infon = "内存：" + os.popen("cat /proc/meminfo |grep 'MemTotal' |cut -f2 -d:|awk -F' ' '{print int($1)}' |awk '{printf \"%.1f\",$1/1024/1024}'").read().replace('\n','') + "GB"
infoo = "GPU：" + os.popen("lspci |grep -i vga | awk -F' VGA compatible controller: ' '{print $2}'").read().replace('\n','')
infop = "主板：" + os.popen("cat /sys/devices/virtual/dmi/id/board_vendor").read().replace('\n','') + os.popen("cat /sys/devices/virtual/dmi/id/board_name").read().replace('\n','')
infoq = "网卡：" + os.popen("lspci |grep -i 'Network controller' |awk -F'Co., Ltd. ' '{print $2}'").read().replace('\n','')
infor = "声卡：" + os.popen("lspci |grep -i audio |awk -F': ' '{print $2}'").read().replace('\n','')

print('<openbox_pipe_menu>')
print('<separator label="Arch系统信息" />')
for app in [infoa,infob,infoc,infod,infoe,infof,infog,infoh,infoi,infoj,infok,infol,infom,infon,infoo,infop,infoq,infor]:
    print('<item label="' + app + '" icon="distributor-logo-archlinux" />')
print('</openbox_pipe_menu>')