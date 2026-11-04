#!/usr/bin/env python3
import os,sys,gi,threading
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class WifiAuthDialog(Gtk.Window):
    def __init__(self, ssid="MyWiFi"):
        super().__init__(title=f"连接无线网络 {sys.argv[1]}")
        self.set_border_width(10)
        self.set_default_size(300, 100)
        self.set_resizable(False)
        self.set_icon_name("network-wireless")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        hbox_pw = Gtk.Box(spacing=0)
        # ========== 重点：密码框下方的红色提示Label ==========
        self.label_err = Gtk.Label()
        self.label_err.set_markup('<span color="#228822">请输入无线网络' + sys.argv[1] + '的密码</span>')
        self.label_err.set_halign(Gtk.Align.START)
        vbox.pack_start(self.label_err, False, False, 0)

        # 密码行 + 眼睛按钮
        self.entry_pw = Gtk.Entry()
        self.entry_pw.set_placeholder_text("请输入密码...")
        self.entry_pw.set_visibility(False)
        self.btn_eye = Gtk.Button(label="👁")
        self.btn_eye.connect("clicked", self.toggle_visible)
        hbox_pw.pack_start(self.entry_pw, True, True, 0)
        hbox_pw.pack_start(self.btn_eye, False, False, 1)
        vbox.pack_start(hbox_pw, False, False, 0)
        self.entry_pw.connect("activate", self.on_connect)

        # 按钮行
        btn_conn = Gtk.Button(label="连接")
        btn_conn.connect("clicked", self.on_connect)
        vbox.pack_start(btn_conn, False, False, 0)

    def toggle_visible(self, btn):
        vis = self.entry_pw.get_visibility()
        self.entry_pw.set_visibility(not vis)

    def set_error(self, txt):
        self.label_err.set_markup(f'<span color="#dd2222">{txt}</span>')

    def on_connect(self, btn):
        self.set_error('<span color="#228822">连接中...</span>')
        passwd = self.entry_pw.get_text()
        # 后台线程函数
        def connect_wifi():
            text = os.popen("iwctl --passphrase " + passwd + " station wlan0 connect " + sys.argv[1]).read().strip()
            # 回到GTK主线程更新UI
            def update_ui():
                if text == '\x1b[0;91mOperation failed\n\x1b[0m':
                    self.set_error("网络连接失败")
                elif text == '\x1b[0;91mArgument format is invalid\n\x1b[0m':
                    self.set_error("密码格式错误")
                elif text == '':
                    self.label_err.set_markup("网络连接成功")
            GLib.idle_add(update_ui)
        # 启动线程，不阻塞UI
        t = threading.Thread(target=connect_wifi, daemon=True)
        t.start()

        self.entry_pw.grab_focus()
        self.entry_pw.select_region(0, -1)
        return

win = WifiAuthDialog("TestWiFi")
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
