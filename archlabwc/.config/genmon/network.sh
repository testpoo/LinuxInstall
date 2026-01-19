#!/bin/bash

# 网络
if [ $(iwctl station wlan0 show | grep -F State | awk '{print $2}')="connected" ];then network="📶连接";else network="🌐断开";fi

echo "<txt>$network</txt>"
echo "<tool>网络</tool>"