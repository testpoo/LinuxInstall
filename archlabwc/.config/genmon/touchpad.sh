#!/bin/bash

# 触摸板
touchpad="🖱️"$(if grep -q '<sendEventsMode>disabledOnExternalMouse<\/sendEventsMode>$' ~/.config/labwc/rc.xml;then echo '关';else echo '开';fi)

echo "<txt>$touchpad</txt>"
echo "<tool>触摸板</tool>"