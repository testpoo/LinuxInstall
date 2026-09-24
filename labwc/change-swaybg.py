#!/usr/bin/env python3
# coding=utf-8

import os,time,sys

os.system("sed -i '/^swaybg -i/c\swaybg -i " + sys.argv[1] + " >/dev/null 2>&1 &' ~/.config/labwc/autostart")
os.system("pkill swaybg")
os.system("swaybg -i " + sys.argv[1])