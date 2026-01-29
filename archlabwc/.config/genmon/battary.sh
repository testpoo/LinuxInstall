#!/bin/bash

# 电量
percentage=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "percentage" | awk -F ':' '{print $2,$4}' | sed 's/ //g')
time_to_empty=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "time to empty" | awk -F ':' '{print $2,$4}' | sed 's/ //g') 
time_to_full=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "time to full" | awk -F ':' '{print $2,$4}' | sed 's/ //g') 
# battery="⚡️"$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "state\|percentage\|time to empty" | awk -F ':' '{print $2,$4}' | sed 's/ //g') 
state=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "state" | awk -F ':' '{print $2,$4}' | sed 's/ //g')

if [[ $state = "charging" && $percentage = "100%" ]];then
	echo "<txt>$percentage
电量</txt>"
    echo "<tool>电量已充满</tool>"
elif [[ $state = "charging" && ${percentage:0:-1} -le 100 ]];then
	echo "<txt>$percentage
充电</txt>"
    echo "<tool>电量剩余$percentage，将在$time_to_full后充满</tool>"
elif [[ $state = "discharging" ]];then
	echo "<txt>$percentage
放电</txt>"
    echo "<tool>电量剩余$percentage，还可使用$time_to_empty</tool>"
fi

if [[ ${percentage:0:-1} -ge 20 ]];then
    echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;margin-left:1px}</css>"
else
    echo "<css>.genmon_value {background:#E0E0E0;color:#FF0000;font-size:11px;min-width:35px;margin-left:1px}</css>"
fi