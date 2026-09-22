#!/usr/bin/env python3
# coding=utf-8

import os

devices = os.popen("wpctl status | awk '/Sinks:/{f=1;next} /Sources:/{f=0} f'").read().split('\n')
devices = [device for device in devices if device not in (' │  ','')]
ndevices = []
for device in devices:
    device = device.split("[vol:")[0].split()
    if device[1] != '*':
        device =['',device[1].replace(".","")," ".join(device[2:])]
    else:
        device =['mail-unread-symbolic',device[2].replace(".","")," ".join(device[3:])]
    ndevices.append(device)
print('<openbox_pipe_menu>')
print('<separator label="默认声卡选择" />')
for device in ndevices:
    print('<item label="' + device[2] + '" icon="' + device[0] + '">')
    print('<action name="Execute" command="' + 'wpctl set-default ' + device[1] + '" />')
    print('</item>')
print('</openbox_pipe_menu>')