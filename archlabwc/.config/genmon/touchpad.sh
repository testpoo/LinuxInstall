#!/bin/bash

# 触摸板
touchpad=$(if grep -q '<sendEventsMode>disabledOnExternalMouse<\/sendEventsMode>$' ~/.config/labwc/rc.xml;then echo 'OFF';else echo 'ON';fi)

echo "<txt>$touchpad
触控</txt>"
echo "<tool>触摸板</tool>"
echo "<css>.genmon_value {background:#E0E0E0;color:#212121;font-size:11px;min-width:35px;}</css>"