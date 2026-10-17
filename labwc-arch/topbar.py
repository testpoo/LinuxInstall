#!/usr/bin/env python3

import gi,os
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GLib, GtkLayerShell
from datetime import datetime

class LabwcLayerBar(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("labwc-layer-bar")
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

        self.set_default_size(-1, 28)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(hbox)

        # Left root menu
        self.left_evbox = Gtk.EventBox()
        left_label = Gtk.Label(label="🖥️")
        self.left_evbox.add(left_label)
        self.left_evbox.set_visible_window(False)
        self.left_evbox.connect("enter-notify-event", self.on_enter_root)
        hbox.pack_start(self.left_evbox, False, False, 10)
        self.root_timeout_id = None

        self.left_label = Gtk.Label()
        hbox.pack_start(self.left_label, True, True, 0)

        # Middle list menu
        self.list_evbox = Gtk.EventBox()
        list_label = Gtk.Label(label="☰")
        self.list_evbox.add(list_label)
        self.list_evbox.set_visible_window(False)
        self.list_evbox.connect("enter-notify-event", self.on_enter_list)
        hbox.pack_start(self.list_evbox, False, False, 0)
        self.root_timeout_id = None

        # Middle datetime
        self.mid_btn = Gtk.Button()
        self.mid_btn.set_relief(Gtk.ReliefStyle.NONE)
        hbox.pack_start(self.mid_btn, False, False, 0)
        self.mid_btn.connect("clicked", self.on_button_clicked)
        GLib.timeout_add(1000, self.update_time)

        self.right_label = Gtk.Label()
        hbox.pack_start(self.right_label, True, True, 0)

        # Right client menu
        self.right_evbox = Gtk.EventBox()
        right_label = Gtk.Label(label="🛠️")
        self.right_evbox.add(right_label)
        self.right_evbox.set_visible_window(False)
        self.right_evbox.connect("enter-notify-event", self.on_enter_client)
        hbox.pack_end(self.right_evbox, False, False, 10)
        self.client_timeout_id = None

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
        self.mid_btn.set_label(datetime.now().strftime("%m/%d %R"))
        return True

    def on_button_clicked(self, _button):
        os.system("/opt/xflunar/xflunar.py")

    def _spawn_labwc_menu(self, cmd):
        GLib.spawn_command_line_async(cmd)

    def on_enter_root(self, widget, event):
        if event.type != Gdk.EventType.ENTER_NOTIFY:
            return False
#        if self.root_timeout_id is not None:
#            GLib.source_remove(self.root_timeout_id)
        self.root_timeout_id = GLib.timeout_add(250, self._spawn_labwc_menu, "wtype -M logo -k s")
        return False

    def on_enter_client(self, widget, event):
        if event.type != Gdk.EventType.ENTER_NOTIFY:
            return False
#        if self.client_timeout_id is not None:
#            GLib.source_remove(self.client_timeout_id)
        self.client_timeout_id = GLib.timeout_add(250, self._spawn_labwc_menu, "wtype -M logo -k z")
        return False

    def on_enter_list(self, widget, event):
        if event.type != Gdk.EventType.ENTER_NOTIFY:
            return False
#        if self.client_timeout_id is not None:
#            GLib.source_remove(self.client_timeout_id)
        self.client_timeout_id = GLib.timeout_add(250, self._spawn_labwc_menu, "wtype -M alt -k f3")
        return False

if __name__ == "__main__":
    win = LabwcLayerBar()
    Gtk.main()
