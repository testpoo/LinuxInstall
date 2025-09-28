#!/usr/bin/env python3
# coding=utf-8

import os,json

if [input for input in json.load(os.popen("swaymsg -t get_inputs")) if input['identifier'] == '2362:597:SYNA3602:00_093A:0255_Touchpad'][0]['libinput']['send_events'] == "enabled":
    os.system("swaymsg input \"2362:597:SYNA3602:00_093A:0255_Touchpad\" events disabled")
else:
    os.system("swaymsg input \"2362:597:SYNA3602:00_093A:0255_Touchpad\" events enabled")
