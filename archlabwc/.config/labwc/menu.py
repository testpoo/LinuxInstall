#!/usr/bin/env python3
# coding=utf-8

import os,configparser,math

del_files = {
    'org.gnupg.pinentry-qt5.desktop',
    'bssh.desktop',
    'org.gnupg.pinentry-qt.desktop',
    'bvnc.desktop',
    'avahi-discover.desktop',
    'fcitx5-wayland-launcher.desktop',
    'footclient.desktop',
    'foot-server.desktop'
}

logouts = [
  {
    "Name": " 锁屏    ",
    "Exec": "swaylock -f -i /home/poo/图片/background.png -c 015000",
    "Icon": "system-lock-screen"
  },
#  {
#    "Name": " 挂起    ",
#    "Exec": "systemctl suspend",
#    "Icon": "system-suspend"
#  },
#  {
#    "Name": " 休眼    ",
#    "Exec": "systemctl hibernate",
#    "Icon": "system-suspend-hibernate"
#  },
  {
    "Name": " 重载    ",
    "Exec": "labwc -r",
    "Icon": "systemback"
  },
  {
    "Name": " 退出    ",
    "Exec": "labwc -e",
    "Icon": "system-log-out"
  },
  {
    "Name": " 重启    ",
    "Exec": "systemctl reboot",
    "Icon": "system-reboot"
  },
  {
    "Name": " 关机    ",
    "Exec": "systemctl poweroff -i",
    "Icon": "system-shutdown"
  }
]

file_path = '/usr/share/applications/'
file_names = os.listdir(file_path)
file_names = set(file_names) - del_files

app_lists = []
num = 30

for name in file_names:
    config = configparser.RawConfigParser()
    config.read(file_path + name, encoding='utf-8')
    sections = config.sections()
    if config.has_option('Desktop Entry','Name[zh_CN]'):
        Name = config.get('Desktop Entry','Name[zh_CN]')
    elif config.has_option('Desktop Entry','Name[zh]'):
        Name = config.get('Desktop Entry','Name[zh]')
    elif config.has_option('Desktop Entry','Name'):
        Name = config.get('Desktop Entry','Name')
    else:
        continue
    if config.has_option('Desktop Entry','Exec'):
        Exec = config.get('Desktop Entry','Exec').replace('%F','').replace('%f','').replace('%U','')
    else:
        continue
    if config.has_option('Desktop Entry','Icon'):
        Icon = config.get('Desktop Entry','Icon')
    else:
        continue
    app_lists.append([Name,Exec,Icon])

app_lists.sort()
app_rows = math.ceil(len(app_lists)/num)

print('<openbox_pipe_menu>')
for i in range(app_rows):
    print('<menu id="' + str(i + 1) + '" icon="application-sql" label="程序">')
    for app in app_lists[i*num:(i+1)*num]:
        print('<item label="' + app[0] + '" icon="' + app[2] + '">')
        print('<action name="Execute" command="' + app[1] + '" />')
        print('</item>')
    print('</menu>')
print('<separator />')
for app in logouts:
    print('<item label="' + app["Name"] + '" icon="' + app["Icon"] + '">')
    print('<action name="Execute" command="' + app["Exec"] + '" />')
    print('</item>')
print('</openbox_pipe_menu>')