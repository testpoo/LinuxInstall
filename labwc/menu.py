#!/usr/bin/env python3
# coding=utf-8

import os,configparser,math,sys

def items(label, icon, exec):
    print('<item label="' + label + '" icon="' + icon + '">')
    print('<action name="Execute" command="' + exec + '" />')
    print('</item>')

def menus(app_lists, num, i, cols):
    for app in app_lists[0:num]:
        items(app[0], app[2], app[1])
    if cols > i and len(app_lists) >= num:
        i += 1
        print('<menu id="more" icon="application-sql" label="更多程序">')
        menus(app_lists[num:], num, i)
        if i != 0:
            print('<separator />')
            for i in range(len(logouts)):
                items("☰☲☱☴☵☶☳☷", "application-sql", "")
        print('</menu>')

def apps():
    exclude = [
      'Foot Server',
      'Foot Client',
      '批量重命名',
      'Thunar 首选项',
      '可移动驱动器和介质'
    ]

    file_path = '/usr/share/applications/'
    file_names = os.listdir(file_path)

    app_lists = []

    for name in file_names:
        config = configparser.RawConfigParser()
        config.read(file_path + name, encoding='utf-8')
        if not config.has_section('Desktop Entry'):
            continue
        if config.get('Desktop Entry','Type') != "Application" or config.get('Desktop Entry','NoDisplay', fallback='false') != 'false' or 'LABWC' not in config.get('Desktop Entry','OnlyShowIn', fallback='LABWC').split(';'):
            continue
        if config.has_option('Desktop Entry','Name[zh_CN]'):
            Name = config.get('Desktop Entry','Name[zh_CN]')
        elif config.has_option('Desktop Entry','Name[zh]'):
            Name = config.get('Desktop Entry','Name[zh]')
        elif config.has_option('Desktop Entry','Name'):
            Name = config.get('Desktop Entry','Name')
        else:
            continue
        if config.has_option('Desktop Entry','Exec'):
            Exec = config.get('Desktop Entry','Exec').split('%')[0]
        else:
            continue
        if config.has_option('Desktop Entry','Icon'):
            Icon = config.get('Desktop Entry','Icon')
        else:
            continue
        if Name not in exclude:
            app_lists.append([Name,Exec,Icon])
    return sorted(app_lists)

def applications():
    logouts = [
      {
        "Name": "锁屏",
        "Exec": "swaylock -c 0F4C81",
        "Icon": "system-lock-screen"
        },
#  {
#    "Name": "挂起",
#    "Exec": "systemctl suspend",
#    "Icon": "system-suspend"
#  },
#  {
#    "Name": "休眼",
#    "Exec": "systemctl hibernate",
#    "Icon": "system-suspend-hibernate"
#  },
        {
        "Name": "重载",
        "Exec": "labwc -r",
        "Icon": "sync-synchronizing"
        },
        {
        "Name": "退出",
        "Exec": "labwc -e",
        "Icon": "system-log-out"
        },
        {
        "Name": "重启",
        "Exec": "systemctl reboot",
        "Icon": "system-reboot"
        },
        {
        "Name": "关机",
        "Exec": "systemctl poweroff -i",
        "Icon": "system-shutdown"
        }
    ]

    num= 28
    i = 0
    app_lists = apps()

    print('<openbox_pipe_menu>')
    menus(app_lists, num, i, math.ceil(len(app_lists)/num))
    print('<separator />')
    print('<menu id="logout" label="从这里登出" icon="system-log-out">')
    for app in logouts:
        items(app["Name"], app["Icon"], app["Exec"])
    print('</menu>')
    print('</openbox_pipe_menu>')

def volume():
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
        items(device[2], device[0], "wpctl set-default " + device[1])
    print('</openbox_pipe_menu>')

def network():
    new_knowpass = []
    knowpass = os.popen("iwctl known-networks list").read()
    for know in knowpass.replace('[0m','').split('\n')[4:]:
        if know.split() != []:
            new_knowpass.append(know.split()[0])
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
        items(choice_ssid[1], choice_ssid[2], "iwctl station wlan0 disconnect")
    print('<separator label="可用 WLAN" />')
    for ssid in new_ssids:
        if ssid[1] in new_knowpass:
            items(ssid[1], ssid[2], "iwctl station wlan0 connect " + ssid[1])
        else:
            items(ssid[1], ssid[2], "~/.config/labwc/network-input.py " + ssid[1])
    print('<item label="更新列表" icon="system-software-update">')
    exec = "sh -c 'iwctl station wlan0 scan;wtype -M logo -k n'"
    print('<action name="Execute" command="' + exec + '" />')
    print('</item>')
    print('<menu id="logout" label="清除密碼" icon="edit-clear">')
    for ssid in new_ssids:
        if ssid[1] in new_knowpass:
            items(ssid[1], ssid[2], "iwctl known-networks " + ssid[1] + " forget")
    print('</menu>')
    print('</openbox_pipe_menu>')

if sys.argv[1] == "applications":
    applications()
elif sys.argv[1] == "volume":
    volume()
elif sys.argv[1] == "network":
    network()