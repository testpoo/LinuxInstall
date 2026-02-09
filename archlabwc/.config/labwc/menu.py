#!/usr/bin/env python3
# coding=utf-8

import os,configparser,math

logouts = [
  {
    "Name": "锁屏",
    "Exec": "swaylock -f -i /home/poo/图片/background.png -c 015000",
    "Icon": "system-lock-screen",
    "shortcut": "Win+L"
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
    "Icon": "systemback",
    "shortcut": "Win+Shift+C"
  },
  {
    "Name": "退出",
    "Exec": "labwc -e",
    "Icon": "system-log-out",
    "shortcut": "Win+Shift+E"
  },
  {
    "Name": "重启",
    "Exec": "systemctl reboot",
    "Icon": "system-reboot",
    "shortcut": "Win+Shift+R"
  },
  {
    "Name": "关机",
    "Exec": "systemctl poweroff -i",
    "Icon": "system-shutdown",
    "shortcut": "Win+Shift+P"
  }
]

exclude = [
  'Avahi Zeroconf 浏览器',
  'Avahi SSH 服务器的浏览器',
  'Avahi VNC 服务器的浏览器',
  'Foot Server',
  'Foot Client'
]

file_path = '/usr/share/applications/'
file_names = os.listdir(file_path)

app_lists = []
num= 28
i = 0

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

app_lists.sort()
cols = math.ceil(len(app_lists)/num)

def items(label, icon, exec):
    print('<item label="' + label + '" icon="' + icon + '">')
    print('<action name="Execute" command="' + exec + '" />')
    print('</item>')

def menus(app_lists, num, i):
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

print('<openbox_pipe_menu>')
menus(app_lists, num, i)
print('<separator />')
for app in logouts:
    items(app["Name"] + "｜" + app["shortcut"], app["Icon"], app["Exec"])
print('</openbox_pipe_menu>')