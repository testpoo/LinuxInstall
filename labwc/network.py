#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi,os
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib

class SimpleWifiWin(Gtk.Window):
    def __init__(self):
        super().__init__(title="WiFi工具")
        self.set_default_size(300, 520)
        self.expanded_ssid = None
        self.set_resizable(False)
        self.set_icon_name("network-wireless")
        self.known_ssids = []      # 已经保存密码的ssid
        self.connected_ssid = None # 当前正在连接的ssid
        self.scanning = False
        self.connecting_ssid = None  # 正在连接的ssid
        self.last_status = {}        # ssid: (status_text, is_error)

        main_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        main_v.set_margin_top(0)
        main_v.set_margin_start(0)
        main_v.set_margin_end(0)
        main_v.set_margin_bottom(0)
        self.add(main_v)

        sw = Gtk.ScrolledWindow()
        sw.set_vexpand(True)
        main_v.pack_start(sw, expand=True, fill=True, padding=0)
        self.list_v = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        sw.add(self.list_v)

        self.render_list()

        self.btn_scan = Gtk.Button(label="扫描")
        self.btn_scan.set_size_request(120, -1)
        self.btn_scan.connect("clicked", self.on_scan)
        self.btn_scan.set_margin_start(5)
        self.btn_scan.set_margin_end(5)
        self.btn_scan.set_margin_bottom(5)
        main_v.pack_end(self.btn_scan, expand=False, fill=False, padding=0)

        # css：hover增加padding，行点击区域变大
        css_provider = Gtk.CssProvider()
        css = """
        .wifi-row-hover {
            background-color: #e6e6e6;
            padding:5px 4px;
        }
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def load_known_networks(self):
        self.known_ssids.clear()
        knowpass = os.popen("iwctl known-networks list").read()
        for know in knowpass.replace('\x1b[0m','').split('\n')[4:]:
            parts = know.split()
            if parts:
                self.known_ssids.append(parts[0])

    def load_connected_ssid(self):
        self.connected_ssid = None
        out = os.popen("iwctl station wlan0 show").read()
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Connected network"):
                content = line[len("Connected network"):].strip()
                if content:
                    self.connected_ssid = content
                break

    def render_list(self):
        self.load_known_networks()
        self.load_connected_ssid()
        wifi_list = []
        ssid_icons = ['network-wireless-signal-weak','network-wireless-signal-ok','network-wireless-signal-good','network-wireless-signal-excellent']
        ssids = os.popen("iwctl station wlan0 get-networks").read().strip()
        if ssids == "No station on device: 'wlan0'":
            choice_ssid = ['*',"网络断开","network-wireless-offline"]
        else:
            for ssid in ssids.replace('\x1b[0m','').split('\n')[4:]:
                new_ssid = ssid.split()
                if len(new_ssid) > 3:
                    choice_ssid = ['*',new_ssid[1],ssid_icons[int(len(new_ssid[3].split('\x1b[1;90m')[0]) - 1)]]
                    wifi_list.append(choice_ssid)
                elif new_ssid != []:
                    new_ssid = ['',new_ssid[0],ssid_icons[int(len(new_ssid[2].split('\x1b[1;90m')[0]) - 1)]]
                    wifi_list.append(new_ssid)

        for c in self.list_v.get_children():
            self.list_v.remove(c)

        for wifi in wifi_list:
            ssid = wifi[1]
            row_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            # 关键：设置上下margin，**增大每一行的高度**
            row_h.set_margin_top(5)
            row_h.set_margin_bottom(5)
            row_h.set_margin_start(10)

            icon = Gtk.Image.new_from_icon_name(wifi[2], Gtk.IconSize.MENU)

            base_text = ssid
            status_mark = ""
            if ssid == self.connected_ssid:
                status_mark = f"<span foreground='#88c070'>  ✔已连接</span>"
            elif ssid == self.connecting_ssid:
                status_mark = "  <span>连接中…</span>"
            elif ssid in self.last_status:
                txt, is_err = self.last_status[ssid]
                if is_err:
                    status_mark = f"  <span foreground='#ed4040'>{txt}</span>"
                else:
                    status_mark = f"  <span>{txt}</span>"

            markup = f"{base_text}{status_mark}"
            ssid_lbl = Gtk.Label()
            ssid_lbl.set_markup(markup)
            ssid_lbl.set_xalign(0)

            row_h.pack_start(icon, expand=False, fill=False, padding=0)
            row_h.pack_start(ssid_lbl, expand=True, fill=True, padding=0)

            evt = Gtk.EventBox()
            evt.add(row_h)
            evt.ssid = ssid
            evt.connect("button-press-event", self.on_row_click)
            evt.connect("enter-notify-event", self.on_row_enter)
            evt.connect("leave-notify-event", self.on_row_leave)
            self.list_v.pack_start(evt, expand=False, fill=False, padding=0)

            if self.expanded_ssid == ssid and ssid not in self.known_ssids:
                pass_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                pass_h.set_margin_top(4)
                entry = Gtk.Entry()
                entry.set_placeholder_text("输入密码，回车")
                entry.set_visibility(False)
                entry.ssid = ssid
                entry.connect("activate", self.on_pass_enter)
                pass_h.pack_start(entry, expand=True, fill=True, padding=0)
                self.list_v.pack_start(pass_h, expand=False, fill=False, padding=0)

        self.list_v.show_all()

    def on_row_enter(self, widget, event):
        widget.get_style_context().add_class("wifi-row-hover")

    def on_row_leave(self, widget, event):
        widget.get_style_context().remove_class("wifi-row-hover")

    def clear_all_status(self):
        self.last_status.clear()

    def on_row_click(self, evtbox, event):
        ssid = evtbox.ssid
        if ssid == self.connected_ssid or ssid == self.connecting_ssid:
            return
        self.clear_all_status()
        if ssid in self.known_ssids:
            self.do_connect(ssid, "")
            return
        if self.expanded_ssid == ssid:
            self.expanded_ssid = None
        else:
            self.expanded_ssid = ssid
        self.render_list()

    def on_pass_enter(self, entry):
        ssid = entry.ssid
        self.clear_all_status()
        self.do_connect(ssid, entry.get_text())

    def do_connect(self, ssid, pwd):
        self.expanded_ssid = None
        self.connecting_ssid = ssid
        self.render_list()

        if ssid in self.known_ssids:
            text = os.popen("iwctl station wlan0 connect " + ssid).read().strip()
        else:
            text = os.popen("iwctl --passphrase " + pwd + " station wlan0 connect " + ssid).read().strip()

        if text == '\x1b[0;91mOperation failed\n\x1b[0m':
            if ssid in self.known_ssids:
                os.popen(f"iwctl known-networks \"{ssid}\" forget")
            self.last_status[ssid] = ("连接失败", True)
        elif text == '\x1b[0;91mArgument format is invalid\n\x1b[0m':
            self.last_status[ssid] = ("密码格式错误", True)
        elif text == '':
            self.last_status[ssid] = ("连接成功", False)

        self.connecting_ssid = None
        GLib.timeout_add(1500, self._after_connect_refresh)
        return

    def _after_connect_refresh(self):
        self.render_list()
        return False

    def on_scan(self, btn):
        if self.scanning:
            return
        self.clear_all_status()
        self.scanning = True
        self.btn_scan.set_label("扫描中…")
        os.system("iwctl station wlan0 scan")
        GLib.timeout_add(2000, self._scan_finish)

    def _scan_finish(self):
        self.scanning = False
        self.btn_scan.set_label("扫描")
        self.render_list()
        return False

def main():
    win = SimpleWifiWin()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
