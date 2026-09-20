#!/bin/bash

# 触摸板
if grep -q '<sendEventsMode>no<\/sendEventsMode>$' ~/.config/labwc/rc.xml;then
    notify-send -t 2000 -h string:x-canonical-private-synchronous:touchpad "触摸板已关闭"
else
	notify-send -t 2000 -h string:x-canonical-private-synchronous:touchpad "触摸板已启用"
fi