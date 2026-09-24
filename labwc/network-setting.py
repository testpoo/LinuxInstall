#!/usr/bin/env python3
# coding=utf-8

import os

new_knowpass = []
knowpass = os.popen("iwctl known-networks list").read()
for know in knowpass.replace('[0m','').split('\n')[4:]:
    if know.split() != []:
        new_knowpass.append(know.split()[0])
# os.system("iwctl station wlan0 scan")
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
for ssid in new_ssids:
    print('<item label="' + ' ' + ssid[1] + '" icon="' + ssid[2] + '">')
    if ssid[1] in new_knowpass:
        print('<action name="Execute" command="iwctl station wlan0 connect ' + ssid[1] + '" />')
    else:
        print('<action name="Execute" command="~/.config/labwc/network-input.py ' + ssid[1] + '" />')
    print('</item>')
print('<item label="更新列表" icon="system-software-update">')
exec = "sh -c 'iwctl station wlan0 scan;wtype -M logo -k n'"
print('<action name="Execute" command="' + exec + '" />')
print('</item>')
print('<menu id="logout" label="清除密碼" icon="edit-clear">')
for ssid in new_ssids: 
    if ssid[1] in new_knowpass:    
        print('<item label="' + ssid[1] + '" icon="' + ssid[2] + '">')
        print('<action name="Execute" command="iwctl known-networks ' + ssid[1] + ' forget" />')
        print('</item>')
print('</menu>')
print('</openbox_pipe_menu>')