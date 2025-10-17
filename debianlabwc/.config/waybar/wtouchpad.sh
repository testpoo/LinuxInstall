#!/bin/bash

if grep -q '<sendEventsMode>disabledOnExternalMouse<\/sendEventsMode>$' ~/.config/labwc/rc.xml;then
	echo '关'
else
	echo '开'
fi