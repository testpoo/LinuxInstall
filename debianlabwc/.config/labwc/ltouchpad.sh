#!/bin/bash

if grep -q '<sendEventsMode>disabledOnExternalMouse</sendEventsMode>$' ~/.config/labwc/rc.xml; then
    sed -i 's/<sendEventsMode>disabledOnExternalMouse<\/sendEventsMode>/<sendEventsMode>yes<\/sendEventsMode>/' ~/.config/labwc/rc.xml
    labwc -r
else
    sed -i 's/<sendEventsMode>yes<\/sendEventsMode>/<sendEventsMode>disabledOnExternalMouse<\/sendEventsMode>/' ~/.config/labwc/rc.xml
    labwc -r
fi
