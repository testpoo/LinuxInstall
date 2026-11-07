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
        self.height = 32

        # 启用 layer-shell
        GtkLayerShell.init_for_window(self)
        # 锚定到屏幕顶部+左右铺满
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        # 层 top
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        # 开启 exclusive zone，labwc自动预留空间
        GtkLayerShell.set_exclusive_zone(self, self.height)
        # 设置边距
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 0)
        # GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.ON_DEMAND)

        self.set_default_size(-1, self.height)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_name("hbox")
        self.add(hbox)

        # 程序按钮/菜单
        self.root_btn = Gtk.Button()
        self.root_btn.set_relief(Gtk.ReliefStyle.NONE)
        self.root_btn.set_tooltip_text("所有程序")
        icon = Gtk.Image.new_from_icon_name("distributor-logo-archlinux", Gtk.IconSize.BUTTON)
        icon.set_pixel_size(self.height)
        self.root_btn.set_image(icon)
        hbox.pack_start(self.root_btn, False, False, 0)
        self.root_btn.connect("clicked", self.on_root_clicked)

        self.left_label = Gtk.Label()
        hbox.pack_start(self.left_label, True, True, 0)

        # 窗口列表
        self.window_btn = Gtk.Button()
        self.window_btn.set_relief(Gtk.ReliefStyle.NONE)
        icon = Gtk.Image.new_from_icon_name("org.xfce.panel.windowmenu", Gtk.IconSize.BUTTON)
        icon.set_pixel_size(self.height)
        self.window_btn.set_image(icon)
        hbox.pack_start(self.window_btn, False, False, 0)
        self.window_btn.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)
        self.window_btn.connect("enter-notify-event", self.on_window_clicked)

        # 右分隔符
        self.right_label = Gtk.Label()
        hbox.pack_start(self.right_label, True, True, 0)

        # 时间按钮
        self.time_btn = Gtk.Button()
        self.time_btn.set_relief(Gtk.ReliefStyle.NONE)
        self.time_btn.set_name("time_btn")
        hbox.pack_start(self.time_btn, False, False, 0)
        self.time_btn.connect("clicked", self.on_date_clicked)
        GLib.timeout_add(1000, self.update_time)

        # 工具按钮/菜单
        self.tools_btn = Gtk.Button()
        self.tools_btn.set_relief(Gtk.ReliefStyle.NONE)
        self.tools_btn.set_tooltip_text("工具")
        icon = Gtk.Image.new_from_icon_name("shutdown", Gtk.IconSize.BUTTON)
        icon.set_pixel_size(self.height)
        self.tools_btn.set_image(icon)
        hbox.pack_end(self.tools_btn, False, False, 0)
        self.tools_btn.connect("clicked", self.on_tools_clicked)

        # CSS
        css = f"""
        * {{
            background-color: #f6f5f4;
            color: #222222;
            font-size: 14px;
        }}
        #hbox {{
            border-top: 1px solid #D5D0CC;
        }}
        button {{
            border: none;
            border-image: none;
            box-shadow: none;
            outline: none;
            background: transparent;
            padding: 0px 2px
        }}
        button:hover {{
            border: none;
            border-image: none;
            box-shadow: none;
            background: transparent;
        }}
        button:focus {{
            outline: none;
            border: none;
            border-image: none;
        }}
        button:active {{
            border: none;
            border-image: none;
            box-shadow: none;
        }}
        #time_btn label {{
            font-size: 10px;
            font-weight: bold;
        }}
        tooltip,
        tooltip *,
        tooltip box,
        tooltip label {{
            background-color: #1a1a1a;
        }}
        tooltip label {{
            color: #fff;
            font-weight: bold;
        }}
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
        self.time_btn.set_label(datetime.now().strftime("       %R\n%Y/%m/%d"))
        self.time_btn.set_tooltip_text(os.popen("date +'%A %F %H:%M 第%V周'").read().strip())
        return True

    def on_date_clicked(self, _button):
        os.system("/opt/xflunar/xflunar.py")

    def on_root_clicked(self, _button):
        os.system("wtype -M logo -k 1")
        return False

    def on_tools_clicked(self, _button):
        os.system("wtype -M logo -k 2")
        return False

    def on_window_clicked(self, widget, event):
        if event.detail != Gdk.NotifyType.INFERIOR:
            os.system("wtype -M logo -k 3")
        return False

if __name__ == "__main__":
    win = LabwcBar()
    Gtk.main()
