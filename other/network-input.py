#!/usr/bin/env python3
import gi,sys,os

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class InputPopup(Gtk.Window):
    def __init__(self):
        super().__init__(title="请输入WIFI密码")
        self.set_default_size(300, 100)
        self.set_resizable(False)
        # 窗口居中
        self.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)

        # 输入框
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("请输入WIFI密码...")
        self.entry.connect("activate", self.on_submit) # 回车提交
        vbox.pack_start(self.entry, False, False, 0)

        # 按钮行
        btn_box = Gtk.Box(spacing=10)
        btn_ok = Gtk.Button(label="确定")
        btn_ok.connect("clicked", self.on_submit)
        btn_cancel = Gtk.Button(label="取消")
        btn_cancel.connect("clicked", self.on_cancel)

        btn_box.pack_start(btn_ok, True, True, 0)
        btn_box.pack_start(btn_cancel, True, True, 0)
        vbox.pack_start(btn_box, False, False, 0)

        self.add(vbox)
        self.result = None

        # ESC关闭窗口
        self.connect("key-press-event", self.on_key_press)
        # 窗口显示后自动聚焦输入框
        self.connect("show", self.on_window_shown)

    def on_window_shown(self, widget):
        self.entry.grab_focus()

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.result = None
            Gtk.main_quit()
            return True
        return False

    def on_submit(self, widget):
        self.result = self.entry.get_text().strip()
        Gtk.main_quit()

    def on_cancel(self, widget):
        self.result = None
        Gtk.main_quit()

def main():
    win = InputPopup()
    win.show_all()
    Gtk.main()
    if win.result is not None:
        passwd = win.result
    else:
        passwd = ""
    os.system("iwctl --passphrase " + passwd + " station wlan0 connect " + sys.argv[1])

if __name__ == "__main__":
    main()
