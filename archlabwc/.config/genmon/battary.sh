#!/bin/bash

# 电量
battery=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "percentage" | awk -F ':' '{print $2,$4}' | sed 's/ //g')
time=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "time to empty" | awk -F ':' '{print $2,$4}' | sed 's/ //g') 
# battery="⚡️"$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "state\|percentage\|time to empty" | awk -F ':' '{print $2,$4}' | sed 's/ //g') 

echo "<txt>$battery
电量</txt>"
echo "<tool>电量$time</tool>"
if [ $battery -le 20 ];then
    echo "<css>.genmon_value {background:#E0E0E0;color:#FF0000;font-size:11px;min-width:35px;margin-left:1px}</css>"
else
	echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"
fi