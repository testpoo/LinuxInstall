#!/usr/bin/env python3

import gi,os
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GLib, GtkLayerShell
from datetime import datetime
from collections import Counter

class LabwcBar(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("labwcbar")
        self.set_decorated(False)

        # 启用 layer-shell
        GtkLayerShell.init_for_window(self)
        # 锚定到屏幕顶部+左右铺满
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        # 层 top
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        # 开启 exclusive zone，labwc自动预留空间
        GtkLayerShell.set_exclusive_zone(self, 24)
        # 设置边距
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 0)
        GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.ON_DEMAND)

        self.set_default_size(-1, 28)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(hbox)

        # Left root menu
        self.root_btn = Gtk.Button()
        self.root_btn.set_relief(Gtk.ReliefStyle.NONE)
        self.root_btn.set_tooltip_text("所有程序")
        icon = Gtk.Image.new_from_icon_name("debian-logo-symbolic", Gtk.IconSize.BUTTON)
        self.root_btn.set_image(icon)
        hbox.pack_start(self.root_btn, False, False, 0)
        self.root_btn.connect("clicked", self.on_root_clicked)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("搜索程序...")
        self.entry.set_has_frame(False)
        hbox.pack_start(self.entry, False, False, 0)
        self.entry.set_width_chars(14)

        self.left_label = Gtk.Label()
        hbox.pack_start(self.left_label, True, True, 0)

        # Middle list menu
        self.list_box = Gtk.Box()
        hbox.pack_start(self.list_box, False, False, 0)

        self.right_label = Gtk.Label()
        hbox.pack_start(self.right_label, True, True, 0)

        # Right datetime
        self.time_btn = Gtk.Button()
        self.time_btn.set_relief(Gtk.ReliefStyle.NONE)
        hbox.pack_start(self.time_btn, False, False, 0)
        self.time_btn.connect("clicked", self.on_date_clicked)
        GLib.timeout_add(1000, self.update_time)

        # Right tools menu
        self.tools_btn = Gtk.Button()
        self.tools_btn.set_relief(Gtk.ReliefStyle.NONE)
        self.tools_btn.set_tooltip_text("工具")
        icon = Gtk.Image.new_from_icon_name("system-shutdown-panel-restart", Gtk.IconSize.BUTTON)
        self.tools_btn.set_image(icon)
        hbox.pack_end(self.tools_btn, False, False, 0)
        self.tools_btn.connect("clicked", self.on_tools_clicked)

        self.entry.connect("activate", self.on_search_enter)
        GLib.timeout_add(500, self.update_tasks)

        # CSS
        css = """
        * {
            background-color: #1a1a1a;
            color: #f0f0f0;
            font-size:14px;
        }
        GtkLabel {
            padding: 2px 4px;
        }
        EventBox:hover GtkLabel {
            background-color:#333333;
        }
        button {
            border: none;
            border-image: none;
            box-shadow: none;
            outline: none;
            background: transparent;
            padding: 0px 4px
        }
        button:hover {
            border: none;
            border-image: none;
            box-shadow: none;
            background: transparent;
        }
        button:focus {
            outline: none;
            border: none;
            border-image: none;
        }
        button:active {
            border: none;
            border-image: none;
            box-shadow: none;
        }
        entry {
            background-color: #555555;
            color: #ffffff;
            border: none;
            border-radius: 0px;
            min-height: 24px;
            padding:0 6px;
            box-shadow: none;
        }
        entry:focus {
            outline: none;
        }
        entry selection {
            background-color: #444444;
            color: #ffffff;
        }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.show_all()

    def update_time(self):
        self.time_btn.set_label(datetime.now().strftime("%Y/%m/%d %R"))
        return True

    def on_date_clicked(self, _button):
        os.system("/opt/xflunar/xflunar.py")

    def on_root_clicked(self, _button):
        os.system("wtype -M logo -k 1")

    def on_tools_clicked(self, _button):
        os.system("wtype -M logo -k 2")

    def on_window_clicked(self, _button, appid, title):
        os.system("wlrctl toplevel focus app_id:" + appid + " title:'" + title + "'")

    def get_icon(self, app):
        temp = app.split(":", maxsplit=1)
        icon = os.popen("grep -m 1 'Icon=' /usr/share/applications/" + temp[0].lower().replace(".py","") + ".desktop").read().strip().split("=")
        name_zh_cn = os.popen("grep -m 1 'Name\\[zh_CN\\]' /usr/share/applications/" + temp[0].lower().replace(".py","") + ".desktop").read().strip()
        name_zh = os.popen("grep -m 1 'Name\\[zh_CN\\]' /usr/share/applications/" + temp[0].lower().replace(".py","") + ".desktop").read().strip()
        name = os.popen("grep -m 1 'Name' /usr/share/applications/" + temp[0].lower().replace(".py","") + ".desktop").read().strip()
        if name_zh_cn != "":
            name = name_zh_cn.split("=")[1]
        elif name_zh != "":
            name = name_zh.split("=")[1]
        else:
            name = name.split("=")[1]
        list = [name, icon[1], temp[1]]
        return list

    def add_button(self, app):
        self.btn = Gtk.Button()
        self.btn.set_relief(Gtk.ReliefStyle.NONE)
        #self.btn.set_label(app.split(": ")[0])
        self.btn.set_tooltip_text(self.get_icon(app)[0] + ": " + self.get_icon(app)[2])
        self.btn.win_data = app
        icon = Gtk.Image.new_from_icon_name(self.get_icon(app)[1], Gtk.IconSize.BUTTON)
        self.btn.set_image(icon)
        self.list_box.pack_start(self.btn, False, False, 0)
        self.btn.connect("clicked", self.on_window_clicked, app.split(": ")[0], app.split(": ")[1])

    def update_tasks(self):
        wins_text = [(child, child.win_data) for child in self.list_box.get_children()]
        apps = os.popen("wlrctl window list").read().split("\n")[:-1]
        counter_apps = Counter(apps)
        counter_wins = Counter([app[1] for app in wins_text])

        for app in wins_text:
            if app[1] not in apps:
                self.list_box.remove(app[0])
            else:
                num = int(counter_wins[app[1]]) - int(counter_apps[app[1]])
                for i in range(num):
                    self.list_box.remove(app[0])

        for app, value in counter_apps.items():
            if app not in [app[1] for app in wins_text]:
                for i in range(value):
                    self.add_button(app)
            else:
                num = int(counter_apps[app]) - int(counter_wins[app])
                for i in range(num):
                    self.add_button(app)
        self.list_box.show_all()
        return True  # 返回True，定时器持续执行

    def on_search_enter(self, entry):
        """输入内容"""
        text = entry.get_text().strip()
        if not text:
            return
        with open("/tmp/tmp.txt", "w", encoding="utf-8") as f:
            f.write(text)
        os.system("wtype -M logo -k 3")
        entry.set_text("")

if __name__ == "__main__":
    win = LabwcBar()
    Gtk.main()
