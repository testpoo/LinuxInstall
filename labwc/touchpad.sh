#!/bin/bash

if grep -q "<sendEventsMode>no</sendEventsMode>$" ~/.config/labwc/rc.xml; then
	sed -i "s/<sendEventsMode>no<\/sendEventsMode>/<sendEventsMode>yes<\/sendEventsMode>/" ~/.config/labwc/rc.xml
	labwc -r
else
	sed -i "s/<sendEventsMode>yes<\/sendEventsMode>/<sendEventsMode>no<\/sendEventsMode>/" ~/.config/labwc/rc.xml
	labwc -r
fi

# 触摸板
if grep -q '<sendEventsMode>no<\/sendEventsMode>$' ~/.config/labwc/rc.xml;then
    notify-send -t 2000 -h string:x-canonical-private-synchronous:touchpad "触摸板已关闭"
else
	notify-send -t 2000 -h string:x-canonical-private-synchronous:touchpad "触摸板已启用"
fi