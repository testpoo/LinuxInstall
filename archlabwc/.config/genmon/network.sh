#!/bin/bash

# 网络
if [ $(iwctl station wlan0 show | grep -F State | awk '{print $2}')="connected" ];then network="ON";else network="OFF";fi

echo "<txt>$network
网络</txt>"
echo "<tool>网络</tool>"
echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"