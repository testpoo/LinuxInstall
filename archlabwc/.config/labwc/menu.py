#!/usr/bin/env python3
# coding=utf-8

import os,configparser

cats = {
  "Office": [
    "办公",
    "applications-office"
  ],
  "Development": [
    "开发",
    "applications-development"
  ],
  "Graphics": [
    "图形",
    "applications-graphics"
  ],
  "Network": [
    "网络",
    "applications-network"
  ],
  "Education": [
    "教育",
    "applications-education"
  ],
  "Science": [
    "科学",
    "applications-science"
  ],
  "Games": [
    "游戏",
    "applications-games"
  ],
  "System": [
    "系统",
    "applications-system"
  ],
  "Utility": [
    "附件",
    "applications-utilities"
  ],
  "Settings": [
    "设置",
    "applications-system-orange"
  ],
  "AudioVideo": [
    "多媒体",
    "applications-multimedia"
  ],
  "others":[
    "其他",
    "applications-other"
  ]
}

logouts = [
  {
    "Name": "锁屏",
    "Exec": "swaylock -f -i /home/poo/图片/background.png -c 015000",
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
    "Icon": "systemback"
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

file_path = '/usr/share/applications/'
file_names = os.listdir(file_path)

app_lists = []
app_dicts = {}

for name in file_names:
    config = configparser.RawConfigParser()
    config.read(file_path + name, encoding='utf-8')
    #sections = config.sections()
    if not config.has_section('Desktop Entry'):
        continue
    if config.get('Desktop Entry','Type') != "Application" or config.get('Desktop Entry','NoDisplay', fallback='false') != 'false' or config.get('Desktop Entry','OnlyShowIn', fallback='LABWC') != 'LABWC':
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
        Categories = config.get('Desktop Entry','Categories').split(';')[:-1]
        for cat in Categories:
            if cat in cats:
                Category = cat
                break
            else:
                Category = "others"
    else:
        continue
    app_lists.append([Name,Exec,Icon,Category])

app_lists.sort()
for app in app_lists:
    if app[3] in app_dicts:
        app_dicts[app[3]] = app_dicts[app[3]] + [app]
    else:
        app_dicts[app[3]] = [app]

app_dicts = dict(sorted(app_dicts.items(), key=lambda item: item[0]))

print('<openbox_pipe_menu>')
for key in app_dicts:
    print('<menu id="' + key + '" icon="' + cats[key][1] + '" label="' + cats[key][0] + '">')
    for app in app_dicts[key]:
        print('<item label="' + app[0] + '" icon="' + app[2] + '">')
        print('<action name="Execute" command="' + app[1] + '" />')
        print('</item>')
    print('</menu>')
print('  <separator />')
for app in logouts:
    print('<item label="' + app["Name"] + '" icon="' + app["Icon"] + '">')
    print('<action name="Execute" command="' + app["Exec"] + '" />')
    print('</item>')
print('</openbox_pipe_menu>')