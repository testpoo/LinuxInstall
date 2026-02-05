#!/usr/bin/env python3
# coding=utf-8

import os,configparser

del_cats = {
    'X-XFCE',
    'HardwareSettings',
    'X-XFCE-SettingsDialog',
    'GTK',
    'Qt',
    'TerminalEmulator',
    'DesktopSettings',
    'X-XFCE-PersonalSettings',
    'WordProcessor',
    'X-Red-Hat-Base',
    'WebBrowser',
    'X-Xfce-Toplevel',
    'GNOME',
    'X-SuSE-Core-Office',
    '2DGraphics',
    'Database',
    'FlowChart',
    'VectorGraphics',
    'FileTools',
    'FileManager',
    'Spreadsheet',
    'Archiving',
    'Compression',
    'Presentation',
    'Core',
    'XFCE',
    'Math',
    'Viewer',
    'Printing',
    'TextEditor',
    'Filesystem'
}

cats_zh = {
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
    "settings"
  ],
  "AudioVideo": [
    "多媒体",
    "audio"
  ],
  "Logout":[
    "退出",
    "gnome-logout"
  ]
}

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
cat_lists = []
app_dicts = {}

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
    if config.has_option('Desktop Entry','Categories'):
        Categories = config.get('Desktop Entry','Categories').split(';')[:-1]
    else:
        continue
    app_lists.append({"Name":Name,"Exec":Exec,"Icon":Icon,"Categories":Categories})
    cat_lists.extend(Categories)

cats = list(set(cat_lists) - del_cats)

for app in app_lists:
    for cat in cats:
        if cat in app['Categories']:
            if cat in app_dicts:
                app_dicts[cat] = app_dicts[cat] + [app]
            else:
                app_dicts[cat] = [app]

app_dicts = dict(sorted(app_dicts.items(), key=lambda item: item[0]))
app_dicts['Logout'] = logouts
print('<openbox_pipe_menu>')
for key in app_dicts:
    if key in cats_zh:
        print('<menu id="' + key + '" icon="' + cats_zh[key][1] + '" label="' + cats_zh[key][0] + '">')
    else:
        print('<menu id="' + key + '" label="' + key + '">')
    for app in app_dicts[key]:
        print('<item label="' + app["Name"] + '" icon="' + app["Icon"] + '">')
        print('<action name="Execute" command="' + app["Exec"] + '" />')
        print('</item>')
    print('</menu>')
print('</openbox_pipe_menu>')