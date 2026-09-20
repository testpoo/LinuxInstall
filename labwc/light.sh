#!/bin/bash

light=$(brightnessctl get | awk '{print $1/192}')
notify-send -t 2000 -h string:x-canonical-private-synchronous:brightness -h int:value:$light -i display-brightness "$light% 亮度"