#!/usr/bin/env python3
import gi,os
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GtkLayerShell

class LabwcBar(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("labwcbar")
        self.set_decorated(False)

        # 高度改为 5
        self.height = 5

        GtkLayerShell.init_for_window(self)

        # 顶部居中，不左右拉伸
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)

        # 修复：补上self参数
        GtkLayerShell.set_exclusive_zone(self, 0)

        self.set_default_size(-1, self.height)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        hbox.set_name("hbox")
        self.add(hbox)

        # 小圆点按钮 ●，移除所有set_tooltip_text
        self.root_btn = Gtk.Button(label="▬▬▬")
        self.root_btn.set_relief(Gtk.ReliefStyle.NONE)
        hbox.pack_start(self.root_btn, False, False, 0)
        self.root_btn.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)
        self.root_btn.connect("enter-notify-event", self.on_root_clicked)

        self.window_btn = Gtk.Button(label="▬▬▬")
        self.window_btn.set_relief(Gtk.ReliefStyle.NONE)
        self.window_btn.set_margin_start(20)
        self.window_btn.set_margin_end(20)
        hbox.pack_start(self.window_btn, False, False, 0)
        self.window_btn.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)
        self.window_btn.connect("enter-notify-event", self.on_window_clicked)

        self.tools_btn = Gtk.Button(label="▬▬▬")
        self.tools_btn.set_relief(Gtk.ReliefStyle.NONE)
        hbox.pack_start(self.tools_btn, False, False, 0)
        self.tools_btn.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)
        self.tools_btn.connect("enter-notify-event", self.on_tools_clicked)

        # 背景透明，删除全部tooltip css
        css = """
        * {
            background-color: transparent;
            color: #222222;
            font-size: 5px;
        }

        #hbox {
            background-color: transparent;
            border-radius: 0px;
            padding: 0px;
        }

        window {
            background-color: transparent;
        }

        button {
            border: none;
            border-image: none;
            box-shadow: none;
            outline: none;
            background: transparent;
            padding: 0px;
            margin: 0px;
            min-height: 0px;
            min-width: 0px;
        }

        button:hover {
            background-color: rgba(180, 180, 180, 0.35);
        }

        button:focus {
            outline: none;
        }

        button:active {
            background-color: rgba(160, 160, 160, 0.5);
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

    def on_root_clicked(self, widget, event):
        if event.detail != Gdk.NotifyType.INFERIOR:
            os.system("wtype -M logo -k 1")
        return False

    def on_tools_clicked(self, widget, event):
        if event.detail != Gdk.NotifyType.INFERIOR:
            os.system("wtype -M logo -k 2")
        return False

    def on_window_clicked(self, widget, event):
        if event.detail != Gdk.NotifyType.INFERIOR:
            os.system("wtype -M logo -k 3")
        return False

if __name__ == "__main__":
    win = LabwcBar()
    Gtk.main()
