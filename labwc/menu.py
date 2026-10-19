#!/usr/bin/env python3
# coding=utf-8

import os,configparser,math,sys
from collections import defaultdict
from itertools import chain

logouts = [
    {
        "Name": "锁屏",
        "Exec": "swaylock -i ~/图片/lock.svg -c 0F4C81",
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
        "Icon": "retweet"
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

# labwc item
def items(label, icon, exec):
    print('<item label="' + label + '" icon="' + icon + '">')
    print('<action name="Execute" command="' + exec + '" />')
    print('</item>')

# labwc menu
def menus(app_dicts, cat, icon, cat_zh):
    print('<menu id="apps" label="' + cat_zh + '" icon="' + icon + '">')
    for app in app_dicts[cat]:
        items(app[0], app[2], app[1])
    print('</menu>')

# 所有程序
def apps():
    exclude = [
      'Foot Server',
      'Foot Client',
      'Avahi SSH 服务器的浏览器',
      'Avahi VNC 服务器的浏览器',
      'Avahi Zeroconf 浏览器',
      'Qt V4L2 test Utility',
      'Qt V4L2 video capture utility'
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

# 程序菜单
def applications():
    CATEGORIES = [
        ('Settings', ['Settings','Screensaver'], 'preferences-desktop', '设置'), 
        ('Accessories', ['Accessibility','Core','Legacy','Utility'], 'applications-accessories', '附件'), 
        ('Development', ['Development'], 'applications-development', '开发'), 
        ('Education', ['Education'], 'applications-education', '教育'), 
        ('Games', ['Game'], 'applications-games', '游戏'), 
        ('Graphics', ['Graphics'], 'applications-graphics', '图形'), 
        ('Multimedia', ['Audio','Video','AudioVideo'], 'applications-multimedia', '多媒体'), 
        ('Network', ['Network'], 'applications-internet', '网络'), 
        ('Office', ['Office'], 'applications-office', '办公'), 
        ('Science', ['Science'], 'applications-science', '科学'), 
        ('System', ['Emulator','System'], 'applications-system', '系统'), 
        ('Other', ['Other'], 'applications-other', '其它')
    ]

    abouts = [
        "系统：" + os.popen("uname -s").read().strip(),
        "用户名：" + os.popen("whoami").read().strip(),
        "Shell：" + os.popen("echo $SHELL").read().strip(),
        "运行时间：" + os.popen("uptime -p |awk -F' ' '{print $2,$3,$4,$5}' |sed -e 's/ hours, /时/g' -e 's/ minutes/分/g' -e 's/ hour, /时/g' -e 's/ minute/分/g'").read().strip(),
        "包数量：" + os.popen("pacman -Q | wc -l").read().strip(),
        "分辨率：" + os.popen("wlr-randr |awk '/Modes:/{getline; print}' |awk -F' ' '{print $1}'").read().strip(),
        "磁盘：" + os.popen("cat /proc/partitions |grep -w 'sda' | awk -F' ' '{print $3}' |awk '{printf \"%.1f\",$1/1024/1024}'").read().strip() + "GB",
        "设备名称：" + os.popen("hostnamectl|grep 'Static hostname'|awk -F': ' '{print $2}'").read().strip(),
        "操作系统名称：" + os.popen("hostnamectl|grep 'Operating System'|awk -F': ' '{print $2}'").read().strip(),
        "操作系统类型：" + os.popen("uname -m |sed -e 's/_/__/g'").read().strip(),
        "发型版：" + os.popen("cat /etc/os-release |grep ID |awk -F'=' '{print $2}'").read().strip(),
        "发型版版本：" + os.popen("cat /etc/os-release |grep BUILD_ID |awk -F'=' '{print $2}'").read().strip(),
        "内核版本：" + os.popen("uname -r").read().strip(),
        "处理器：" + os.popen("cat /proc/cpuinfo |grep 'model name' |head -n 1 |awk -F ': ' '{print $2}'").read().strip() + " " + os.popen("cat /proc/cpuinfo |grep 'physical id'|uniq |wc -l").read().strip() + "C "  + os.popen("grep 'core id' /proc/cpuinfo | sort -u |wc -l").read().strip() + "核 "  + os.popen("grep 'processor' /proc/cpuinfo |wc -l").read().strip() + "线程",
        "内存：" + os.popen("cat /proc/meminfo |grep 'MemTotal' |cut -f2 -d:|awk -F' ' '{print int($1)}' |awk '{printf \"%.1f\",$1/1024/1024}'").read().strip() + "GB",
        "GPU：" + os.popen("lspci |grep -i vga |awk -F ': ' '{print $2}'").read().strip(),
        "主板：" + os.popen("cat /sys/devices/virtual/dmi/id/board_vendor").read().strip() + " " + os.popen("cat /sys/devices/virtual/dmi/id/board_name").read().strip(),
        "网卡：" + os.popen("lspci |grep -i 'Network controller' |awk -F'Co., Ltd. ' '{print $2}'").read().strip(),
        "声卡：" + os.popen("lspci |grep -i audio |awk -F': ' '{print $2}'").read().strip(),
    ]

    app_lists = apps()
    app_lists.sort()
    app_dicts = defaultdict(list)

    for app in app_lists:
        for cat in CATEGORIES:
            intersection = set(cat[1]) & set(app[3].split(";"))
            others = set(list(chain.from_iterable([cat[1] for cat in CATEGORIES if cat[2] != ['Other']]))) & set(app[3].split(";"))
            if intersection:
                for key in intersection:
                    if key in cat[1] and app[:-1] not in app_dicts[cat[0]]:
                        app_dicts[cat[0]].append(app[:-1])
            elif 'WPS' in app[0] and app[:-1] not in app_dicts['Office']:
                app_dicts['Office'].append(app[:-1])
            elif 'WPS' not in app[0] and not others and app[:-1] not in app_dicts['Other']:
                app_dicts['Other'].append(app[:-1])

    print('<openbox_pipe_menu>')
    items("运行程序...", "system-search", "~/.config/labwc/appfinder.py")
    print('<separator />')
    items("终端模拟器", "org.xfce.terminalemulator", "foot")
    items("文件管理器", "org.xfce.filemanager", "exo-open --launch FileManager")
    items("网络浏览器", "org.xfce.webbrowser", "exo-open --launch WebBrowser")
    print('<separator />')
    for cat in CATEGORIES:
        if cat[0] in app_dicts:
            menus(app_dicts, cat[0], cat[2], cat[3])
    print('<separator />')
    print('<menu id="about" label="关于Arch" icon="gnome-about-logo">')
    print('<separator label="关于Arch" />')
    for about in abouts:
        items(about, "distributor-logo-archlinux", "")
    print('</menu>')
    print('<menu id="logout" label="注销" icon="system-log-out">')
    for app in logouts:
        items(app["Name"], app["Icon"], app["Exec"])
    print('</menu>')
    print('</openbox_pipe_menu>')

def tools():
    print('<openbox_pipe_menu>')
    # 输入法
    ime = os.popen("fcitx5-remote -n").read().strip()
    if ime == "rime":
        ime = "中州韵"
    IsAsciiMode = os.popen("busctl --user call org.fcitx.Fcitx5 /rime org.fcitx.Fcitx.Rime1 IsAsciiMode").read().strip()
    if ime == "":
        print('<menu id="tools" label="输入法" icon="input-keyboard">')
    elif IsAsciiMode == "b true":
        print('<menu id="tools" label="英文" icon="fcitx_rime_latin">')
    else:
        print('<menu id="tools" label="' + ime + '" icon="fcitx-rime">')
    items("重新启动", "system-reboot", "fcitx5 -r")
    items("输入法设置", "system-config-keyboard", "fcitx5-configtool")
    items("退出", "system-log-out", "pkill fcitx5")
    print('</menu>')

    # 蓝牙
    status = os.popen("systemctl is-active bluetooth").read().strip()
    bluetooth_device = os.popen("bluetoothctl devices Connected").read().strip()
    if status == "active" and bluetooth_device != '':
        items("激活|" + bluetooth_device.split(" ")[2], "network-bluetooth-activated", "foot bluetui")
    elif status == "active" and bluetooth_device == '':
        items("激活|未连接" + bluetooth_device, "bluetooth-symbolic", "foot bluetui")
    else:
        items("激活", "network-bluetooth-inactive", "foot bluetui")

    # 网络
    new_knowpass = []
    knowpass = os.popen("iwctl known-networks list").read()
    for know in knowpass.replace('[0m','').split('\n')[4:]:
        if know.split() != []:
            new_knowpass.append(know.split()[0])
    ssids = os.popen("iwctl station wlan0 get-networks").read()
    new_ssids = []
    ssid_icons = ['network-wireless-signal-weak','network-wireless-signal-ok','network-wireless-signal-good','network-wireless-signal-excellent']
    for ssid in ssids.replace('[0m','').split('\n')[4:]:
        new_ssid = ssid.split()
        if len(new_ssid) > 3:
            choice_ssid = ['*',new_ssid[1],ssid_icons[int(len(new_ssid[3].split('\x1b[1;90m')[0]) - 1)]]
        elif new_ssid != []:
            new_ssid = ['',new_ssid[0],ssid_icons[int(len(new_ssid[2].split('\x1b[1;90m')[0]) - 1)]]
            new_ssids.append(new_ssid)
    if choice_ssid == '':
        choice_ssid = ['*',"网络断开","network-wireless-offline"]
    print('<menu id="tools" label="' + choice_ssid[1] + '" icon="' + choice_ssid[2] + '">')
    for ssid in new_ssids:
        if ssid[1] in new_knowpass:
            items(ssid[1], ssid[2], "iwctl station wlan0 connect " + ssid[1])
        else:
            items(ssid[1], ssid[2], "foot -T '输入WIFI密码' -w 500x80 sh -c 'iwctl station wlan0 connect " + ssid[1] + ";read'")
    print('<item label="更新列表" icon="bqm-update">')
    print('<action name="Execute" command="iwctl station wlan0 scan" />')
    print('</item>')
    print('<separator label="清除密码" />')
    for ssid in new_knowpass:
        items(ssid, "editclear", "iwctl known-networks " + ssid + " forget")
    print('</menu>')

    # 声音
    volume = os.popen("wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}'").read().strip()
    if "MUTED" in os.popen("wpctl get-volume @DEFAULT_AUDIO_SINK@").read().strip() or volume == 0:
        volume_icon = "audio-volume-muted-symbolic"
    elif int(volume) >= 1 and int(volume) < 33:
        volume_icon = "audio-volume-low-symbolic"
    elif int(volume) >= 34 and int(volume) < 66:
        volume_icon = "audio-volume-medium-symbolic"
    else:
        volume_icon = "audio-volume-high-symbolic"
    devices = os.popen("wpctl status | awk '/Sinks:/{f=1;next} /Sources:/{f=0} f'").read().split('\n')
    devices = [device for device in devices if device not in (' │  ','')]
    ndevices = []
    for device in devices:
        device = device.split("[vol:")[0].split()
        if device[1] != '*':
            device =['',device[1].replace(".","")," ".join(device[2:])]
        else:
            device =['audio-card',device[2].replace(".","")," ".join(device[3:])]
        ndevices.append(device)
    print('<menu id="tools" label="' + volume + '% 声音" icon="' + volume_icon + '">')
    print('<separator label="默认声卡选择" />')
    for device in ndevices:
        items(device[2], device[0], "wpctl set-default " + device[1])
    print('</menu>')

    # 亮度
    light = os.popen("(brightnessctl get | awk '{print $1/192}')").read().strip()
    items(light + "% 亮度", "brightness-display-symbolic", "")

    # 截图
    items("截图", "accessories-screenshot-symbolic", "sh -c 'grim -g &quot;$(slurp)&quot; -s 1.25 - | wl-copy'")

    # 触摸板
    if os.system("grep -q '<sendEventsMode>no<\\/sendEventsMode>$' ~/.config/labwc/rc.xml") == 0:
        items("触摸板关闭", "touchpad-disabled-symbolic", "~/.config/labwc/settings.sh touchpad")
    else:
        items("触摸板打开", "touchpad-enabled-symbolic", "~/.config/labwc/settings.sh touchpad")

    # 显示桌面
    items("显示桌面", "desktop", "wtype -M logo -k d")

    print('<separator />')
    # 图片
    list = []
    target_dir = "/home/poo/图片"
    entries = os.listdir(target_dir)
    for name in entries:
        full_path = os.path.join(target_dir, name)
        if os.path.isfile(full_path): # 只取文件，排除文件夹
            list.append((name, full_path))
    print('<menu id="tools" label="设置背景" icon="cs-backgrounds-symbolic">')
    for li in list:
        items(li[0], "games-config-background", "~/.config/labwc/settings.sh change-swaybg " + li[1])
    print('</menu>')

    print('<separator />')
    # 时间
    idate = os.popen("date '+%Y/%m/%d'").read().strip()
    itime = os.popen("date '+%H:%M:%S'").read().strip()
    iweek = os.popen("date '+%V周|%A'").read().strip()
    for time in [("date",idate), ("view-calendar-time-spent",itime), ("view-calendar-week",iweek)]:
        items(time[1], time[0], "/opt/xflunar/xflunar.py")

    print('<separator />')
    # 注销
    for app in logouts:
        items(app["Name"], app["Icon"], app["Exec"])
    print('</openbox_pipe_menu>')

def window_list():
    apps = os.popen("wlrctl window list").read().split("\n")[:-1]
    return apps

def tilde(index):
    tilde_list = []
    apps = window_list()
    for app in apps:
        temp = app.split(":", maxsplit=1)
        tilde_list.append("wlrctl window focus app_id:" + temp[0].strip() + " title:'" + temp[1].strip() + "'")
    os.system(tilde_list[int(index)])

def appwindows():
    print('<openbox_pipe_menu>')
    apps = window_list()
    if apps:
        for app in apps:
            temp = app.split(":", maxsplit=1)
            icon = os.popen("grep -m 1 'Icon=' /usr/share/applications/" + temp[0].lower().replace(".py","") + ".desktop").read().strip().split("=")
            name_zh_cn = os.popen("grep -m 1 'Name\[zh_CN\]' /usr/share/applications/" + temp[0].lower().replace(".py","") + ".desktop").read().strip()
            name_zh = os.popen("grep -m 1 'Name\[zh_CN\]' /usr/share/applications/" + temp[0].lower().replace(".py","") + ".desktop").read().strip()
            name = os.popen("grep -m 1 'Name' /usr/share/applications/" + temp[0].lower().replace(".py","") + ".desktop").read().strip()
            if name_zh_cn != "":
                name = name_zh_cn.split("=")[1]
            elif name_zh != "":
                name = name_zh.split("=")[1]
            else:
                name = name.split("=")[1]
            items(name + "｜" + temp[1].strip(), icon[1], "/home/poo/.config/labwc/menu.py tilde " + str(apps.index(app)))
    else:
        items("没有窗口打开", "window", "")
    print('</openbox_pipe_menu>')

if sys.argv[1] == "applications":
    applications()
elif sys.argv[1] == "tools":
    tools()
elif sys.argv[1] == "appwindows":
    appwindows()
elif sys.argv[1] == "tilde":
    tilde(sys.argv[2])