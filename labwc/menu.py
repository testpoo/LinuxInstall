#!/usr/bin/env python3
# coding=utf-8

import os,configparser,math,sys
from collections import defaultdict
from itertools import chain

def items(label, icon, exec):
    print('<item label="' + label + '" icon="' + icon + '">')
    print('<action name="Execute" command="' + exec + '" />')
    print('</item>')

def menus(app_dicts, cat, icon, cat_zh):
    print('<menu id="apps" label="' + cat_zh + '" icon="' + icon + '">')
    seen = set()
    app_lists = []
    for sub in app_dicts[cat]:
        key = tuple(sub)
        if key not in seen:
            seen.add(key)
            app_lists.append(sub)
    for app in app_lists:
        items(app[0], app[2], app[1])
    print('</menu>')

def apps():
    exclude = [
      'Foot Server',
      'Foot Client',
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
        if config.has_option('Desktop Entry','Categories'):
            Categories = config.get('Desktop Entry','Categories')
        else:
            continue
        if Name not in exclude:
            app_lists.append([Name,Exec,Icon,Categories])
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

    CATEGORIES = [
        ('Settings', ['Settings','Screensaver'], 'preferences-desktop', '设置'), 
        ('Accessories', ['Accessibility','Core','Legacy','Utility'], 'applications-accessories', '实用工具'), 
        ('Development', ['Development'], 'applications-development', '开发'), 
        ('Education', ['Education'], 'applications-education', '教育'), 
        ('Games', ['Game'], 'applications-games', '游戏'), 
        ('Graphics', ['Graphics'], 'applications-graphics', '图形图像'), 
        ('Multimedia', ['Audio','Video','AudioVideo'], 'applications-multimedia', '多媒体'), 
        ('Network', ['Network'], 'applications-internet', '网络'), 
        ('Office', ['Office'], 'applications-office', '办公'), 
        ('Science', ['Science'], 'applications-science', '科学'), 
        ('System', ['Emulator','System'], 'applications-system', '系统工具'), 
        ('Other', ['Other'], 'applications-other', '其它')
    ]

    abouts = [
        "系统：" + os.popen("uname -s").read(),
        "用户名：" + os.popen("whoami").read(),
        "Shell：" + os.popen("echo $SHELL").read(),
        "运行时间：" + os.popen("uptime -p |awk -F' ' '{print $2,$3,$4,$5}' |sed -e 's/ hours, /时/g' -e 's/ minutes/分/g' -e 's/ hour, /时/g' -e 's/ minute/分/g'").read(),
        "包数量：" + os.popen("dpkg -l |wc -l").read(),
        "分辨率：" + os.popen("wlr-randr |awk '/Modes:/{getline; print}' |awk -F' ' '{print $1}'").read(),
        "磁盘：" + os.popen("cat /proc/partitions |grep -w 'sda' | awk -F' ' '{print $3}' |awk '{printf \"%.1f\",$1/1024/1024}'").read() + "GB",
        "设备名称：" + os.popen("hostname").read(),
        "操作系统名称：" + os.popen("lsb_release -si").read(),
        "操作系统类型：" + os.popen("uname -m |sed -e 's/_/__/g'").read(),
        "发型版：" + os.popen("lsb_release -sd").read(),
        "发型版版本：" + os.popen("cat /etc/os-release |grep VERSION_CODENAME |awk -F'=' '{print $2}'").read(),
        "内核版本：" + os.popen("uname -r").read(),
        "处理器：" + os.popen("cat /proc/cpuinfo |grep 'model name' |head -n 1 |awk -F ': ' '{print $2}'").read() + os.popen("cat /proc/cpuinfo |grep 'physical id'|uniq |wc -l").read().strip() + "C "  + os.popen("grep 'core id' /proc/cpuinfo | sort -u |wc -l").read().strip() + "核 "  + os.popen("grep 'processor' /proc/cpuinfo |wc -l").read().strip() + "线程",
        "内存：" + os.popen("cat /proc/meminfo |grep 'MemTotal' |cut -f2 -d:|awk -F' ' '{print int($1)}' |awk '{printf \"%.1f\",$1/1024/1024}'").read() + "GB",
        "GPU：" + os.popen("lspci |grep -i vga |awk -F ': ' '{print $2}'").read(),
        "主板：" + os.popen("cat /sys/devices/virtual/dmi/id/board_vendor").read() + os.popen("cat /sys/devices/virtual/dmi/id/board_name").read(),
        "网卡：" + os.popen("lspci |grep -i 'Network controller' |awk -F'Co., Ltd. ' '{print $2}'").read(),
        "声卡：" + os.popen("lspci |grep -i audio |awk -F': ' '{print $2}'").read(),
    ]

    app_lists = apps()
    app_lists.sort()
    app_dicts = defaultdict(list)

    for app in app_lists:
        for cat in CATEGORIES:
            intersection = set(cat[1]) & set(app[3].split(";"))
            others = set(list(chain.from_iterable([cat[1] for cat in CATEGORIES if cat[2] != ['Other']]))) & set(app[3].split(";"))
            if intersection != ():
                for key in intersection:
                    if key in cat[1]:
                        app_dicts[cat[0]].append(app[:-1])
            elif others == ():
                app_dicts['Other'].append(app[:-1])

    print('<openbox_pipe_menu>')
    items("运行程序...", "org.xfce.appfinder", "~/.config/labwc/appfinder.py")
    print('<separator />')
    items("终端模拟器", "org.xfce.terminalemulator", "exo-open --launch TerminalEmulator")
    items("文件管理器", "org.xfce.filemanager", "exo-open --launch FileManager")
    items("网络浏览器", "org.xfce.webbrowser", "exo-open --launch WebBrowser")
    print('<separator />')
    for cat in CATEGORIES:
        if cat[0] in app_dicts:
            menus(app_dicts, cat[0], cat[2], cat[3])
    print('<separator />')
    print('<menu id="about" label="关于Debian" icon="org.xfce.about">')
    print('<separator label="关于Debian" />')
    for about in abouts:
        items(about, "debian-logo", "")
    print('</menu>')
    print('<menu id="logout" label="注销" icon="system-log-out">')
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
