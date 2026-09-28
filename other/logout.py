import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import subprocess
import getpass

class PowerMenu(Gtk.Window):
    def __init__(self):
        super().__init__(title="注销")
        self.set_default_size(300, 300)
        self.set_resizable(False)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        username = getpass.getuser()

        # 主垂直容器
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_vbox.set_margin_top(10)
        main_vbox.set_margin_bottom(10)
        main_vbox.set_margin_start(10)
        main_vbox.set_margin_end(10)
        self.add(main_vbox)

        # ========= 顶部：注销用户 + 当前用户名 =========
        label_top = Gtk.Label(label=f"注销 {username}")
        label_top.set_markup(f"<big>注销 <b>{username}</b></big>")
        label_top.set_halign(Gtk.Align.CENTER)
        main_vbox.pack_start(label_top, False, False, 0)

        # ========= 第一行功能按钮：锁屏、重载、退出 =========
        row1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        btn_lock = self.make_icon_text_button("system-lock-screen", "锁屏")
        btn_lock.connect("clicked", self.on_lock)

        btn_reload = self.make_icon_text_button("sync-synchronizing", "重载")
        btn_reload.connect("clicked", self.on_reload)

        btn_exit = self.make_icon_text_button("system-log-out", "退出")
        btn_exit.connect("clicked", self.on_exit)

        row1.pack_start(btn_lock, True, True, 0)
        row1.pack_start(btn_reload, True, True, 0)
        row1.pack_start(btn_exit, True, True, 0)

        # ========= 第二行功能按钮：重启、关机 =========
        row2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        btn_reboot = self.make_icon_text_button("system-reboot", "重启")
        btn_reboot.connect("clicked", self.on_reboot)

        btn_shutdown = self.make_icon_text_button("system-shutdown", "关机")
        btn_shutdown.connect("clicked", self.on_shutdown)

        row2.pack_start(btn_reboot, True, True, 0)
        row2.pack_start(btn_shutdown, True, True, 0)

        # ========= 底部取消按钮 =========
        row_cancel = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_cancel = Gtk.Button(label="取消")
        btn_cancel.set_size_request(120, 50)
        btn_cancel.connect("clicked", self.on_cancel)
        row_cancel.pack_start(btn_cancel, False, False, 0)
        row_cancel.set_halign(Gtk.Align.CENTER)

        # 全部行加入主容器
        main_vbox.pack_start(row1, True, True, 0)
        main_vbox.pack_start(row2, True, True, 0)
        main_vbox.pack_start(row_cancel, False, False, 0)

        self.connect("delete-event", self.on_close)

    def make_icon_text_button(self, icon_name, text):
        """创建按钮：图标在上，文字在图标下方"""
        button = Gtk.Button()
        # 垂直盒子：图标 + 文字
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)

        image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DIALOG)
        label = Gtk.Label(label=text)
        label.set_markup("<big>%s</big>" % text)

        vbox.pack_start(image, True, True, 0)
        vbox.pack_start(label, False, False, 0)
        button.add(vbox)
        return button

    # 按钮回调
    def on_lock(self, widget):
        subprocess.Popen(["swaylock", "-c 0F4C81"])
        Gtk.main_quit()

    def on_reload(self, widget):
        subprocess.Popen(["labwc", "-r"])
        Gtk.main_quit()

    def on_exit(self, widget):
        subprocess.Popen(["swaymsg", "-e"])
        Gtk.main_quit()

    def on_reboot(self, widget):
        subprocess.Popen(["systemctl", "reboot"])
        Gtk.main_quit()

    def on_shutdown(self, widget):
        subprocess.Popen(["systemctl", "poweroff"])
        Gtk.main_quit()

    def on_cancel(self, widget):
        Gtk.main_quit()

    def on_close(self, widget, event):
        Gtk.main_quit()
        return False


if __name__ == "__main__":
    win = PowerMenu()
    win.show_all()
    Gtk.main()
