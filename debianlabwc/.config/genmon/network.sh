#!/bin/bash

# 网络
if [ $(iwctl station wlan0 show | grep -F State | awk '{print $2}') = "connected" ];then
    echo "<txt>ON
网络</txt>"
    echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"
    echo "<tool>网络正常</tool>"
else
	echo "<txt>OFF
网络</txt>"
	echo "<css>.genmon_value {background:#E0E0E0;color:#FF0000;font-size:11px;min-width:35px;margin-left:1px}</css>"
	echo "<tool>网络关闭</tool>"
fi