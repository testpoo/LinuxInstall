#!/bin/bash

# 网络
rssi=$(iwctl station wlan0 show | grep AverageRSSI | awk '{print $2}')
if [ $(iwctl station wlan0 show | grep -F State | awk '{print $2}') = "connected" ];then
    if [ $rssi -ge -60 ];then
        echo "<icon>network-wireless-signal-excellent</icon>"
    elif [ $rssi -lt -61 ] && [ $rssi -ge -70 ];then
        echo "<icon>network-wireless-signal-good</icon>"
    elif [ $rssi -lt -71 ] && [ $rssi -ge -80 ];then
        echo "<icon>network-wireless-signal-ok</icon>"
    else
        echo "<icon>network-wireless-signal-weak</icon>"
    fi
    echo "<tool>网络连接正常 $(iwctl station wlan0 show | grep 'Connected network' | awk -F' ' '{print $3}')</tool>"
else
	echo "<icon>network-wireless-offline</icon>"
	echo "<tool>网络连接失败</tool>"
fi
echo "<css>.genmon_image {margin-right:2px;margin-left:2px}</css>"
echo "<iconclick>wtype -M logo -k n</iconclick>"