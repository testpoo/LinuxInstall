#!/bin/bash

# 网络
if [ $(iwctl station wlan0 show | grep -F State | awk '{print $2}') = "connected" ];then
    echo "<icon>network-wireless</icon><txt> </txt>"
    echo "<tool>网络连接正常 $(iwctl station wlan0 show | grep 'Connected network' | awk -F' ' '{print $3}')</tool>"
else
	echo "<icon>network-wireless-offline</icon><txt> </txt>"
	echo "<tool>网络连接失败</tool>"
fi
echo "<css>.genmon_image {margin-right:2px;margin-left:2px}</css>"
echo "<iconclick>xfce4-terminal -e /home/poo/.config/labwc/network-setting.py</iconclick>"