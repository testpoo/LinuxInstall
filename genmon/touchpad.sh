#!/bin/bash

# 触摸板
if grep -q '<sendEventsMode>disabledOnExternalMouse<\/sendEventsMode>$' ~/.config/labwc/rc.xml;then
    echo "<txt>OFF
触控</txt>"
    echo "<css>.genmon_value {background:#E0E0E0;color:#FF0000;font-size:11px;min-width:35px;}</css>"
    echo "<tool>触摸板已关闭</tool>"
else
	echo "<txt>ON
触控</txt>"
	echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;}</css>"
	echo "<tool>触摸板已启用</tool>"
fi