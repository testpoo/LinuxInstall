#!/usr/bin/env python3
# coding=utf-8

import os

os.system("iwctl station wlan0 scan")
ssids = os.popen("iwctl station wlan0 get-networks").read()
new_ssids = []
choice_ssid = ''
ssid_icons = ['network-wireless-signal-weak','network-wireless-signal-ok','network-wireless-signal-good','network-wireless-signal-excellent']
for ssid in ssids.replace('[0m','').split('\n')[4:]:
    new_ssid = ssid.split()
    if len(new_ssid) > 3:
        choice_ssid = ['*',new_ssid[1],ssid_icons[int(len(new_ssid[3].split('\x1b[1;90m')[0]) - 1)]]
    elif new_ssid != []:
        new_ssid = ['',new_ssid[0],ssid_icons[int(len(new_ssid[2].split('\x1b[1;90m')[0]) - 1)]]
        new_ssids.append(new_ssid)
print('<openbox_pipe_menu>')
if choice_ssid != '':
    print('<separator label="已连接 WLAN" />')
    print('<item label="' + ' ' + choice_ssid[1] + '" icon="' + choice_ssid[2] + '">')
    print('<action name="Execute" command="iwctl station wlan0 disconnect" />')
    print('</item>')
print('<separator label="可用 WLAN" />')
for new_ssid in new_ssids:
    print('<item label="' + ' ' + new_ssid[1] + '" icon="' + new_ssid[2] + '">')
    exec = "iwctl station wlan0 connect " + new_ssid[1]
    print('<action name="Execute" command="' + exec + '" />')
    print('</item>')
print('</openbox_pipe_menu>')
# exec = "sh -c 'INPUT=$(~/network-input.py);iwctl --passphrase $INPUT station wlan0 connect " + choice_ssid[1] + "'"