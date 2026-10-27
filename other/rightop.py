#!/usr/bin/env python3

import gi,os
gi.require_version('Gtk', '3.0')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Gdk, GLib, GtkLayerShell

class LabwcLayerBar(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("labwc-layer-bar")
        self.set_decorated(False)

        # 启用 layer-shell
        GtkLayerShell.init_for_window(self)
        # 锚定到屏幕顶部+左右铺满
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
        GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.TOP, True)
        # 层 top
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
        # 开启 exclusive zone，labwc自动预留空间
        GtkLayerShell.set_exclusive_zone(self, 0)
        # 设置边距
        GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, 0)

        self.set_default_size(-1, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(hbox)

        # Right tools menu
        self.tools_evbox = Gtk.EventBox()
        tools_label = Gtk.Label(label="·")
        self.tools_evbox.add(tools_label)
        self.tools_evbox.set_visible_window(False)
        self.tools_evbox.connect("enter-notify-event", self.on_enter_tools)
        hbox.pack_end(self.tools_evbox, False, False, 0)
        self.tools_timeout_id = None

        # CSS
        css = """
        * {
            background-color: transparent;
            font-size:2px;
        }
        GtkLabel {
            padding: 0px 0px;
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

    def _spawn_labwc_menu(self, cmd):
        GLib.spawn_command_line_async(cmd)

    def on_enter_tools(self, widget, event):
        if event.type != Gdk.EventType.ENTER_NOTIFY:
            return False
        if self.tools_timeout_id is not None and GLib.MainContext.default().find_source_by_id(self.tools_timeout_id):
            GLib.source_remove(self.client_timeout_id)
        self.tools_timeout_id = GLib.timeout_add(250, self._spawn_labwc_menu, "wtype -M logo -k 2")
        return False

if __name__ == "__main__":
    win = LabwcLayerBar()
    Gtk.main()
