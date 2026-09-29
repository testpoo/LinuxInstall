#!/usr/bin/env python3
# coding=utf-8

import gi,os,subprocess,configparser
gi.require_version("Gtk", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

ICON_SIZE = 32

def load_icon(icon_str):
    """统一加载图标：支持绝对文件路径 / 主题图标名称，失败返回默认pixbuf"""
    fallback = Gtk.IconTheme.get_default().load_icon("application-x-executable", ICON_SIZE, 0)
    if not icon_str:
        return fallback
    # 如果是文件路径
    if os.path.isabs(icon_str):
        if os.path.exists(icon_str):
            try:
                return GdkPixbuf.Pixbuf.new_from_file_at_scale(icon_str, ICON_SIZE, ICON_SIZE, True)
            except Exception:
                return fallback
        else:
            return fallback
    # 主题图标名
    theme = Gtk.IconTheme.get_default()
    try:
        p = theme.load_icon(icon_str, ICON_SIZE, Gtk.IconLookupFlags.USE_BUILTIN)
        if p:
            return p
    except Exception:
        pass
    return fallback


def scan_desktop_entries():
    app_lists = []
    exclude = [
      'Foot Server',
      'Foot Client',
      '批量重命名',
      'Thunar 首选项',
      '可移动驱动器和介质'
    ]
    file_path = '/usr/share/applications/'
    file_names = os.listdir(file_path)
    for name in file_names:
        config = configparser.RawConfigParser()
        config.read(file_path + name, encoding='utf-8')
        if not config.has_section('Desktop Entry'):
            continue
        if config.get('Desktop Entry','Type') != "Application" or config.get('Desktop Entry','NoDisplay', fallback='false') != 'false' or 'LABWC' not in config.get('Desktop Entry','OnlyShowIn', fallback='LABWC').split(';'):
            continue
        if config.has_option('Desktop Entry','Name[zh_CN]'):
            Name = config.get('Desktop Entry','Name[zh_CN]')
        elif config.has_option('Desktop Entry','Name[zh]'):
            Name = config.get('Desktop Entry','Name[zh]')
        elif config.has_option('Desktop Entry','Name'):
            Name = config.get('Desktop Entry','Name')
        else:
            continue
        if config.has_option('Desktop Entry','Exec'):
            Exec = config.get('Desktop Entry','Exec').split('%')[0]
        else:
            continue
        if config.has_option('Desktop Entry','Icon'):
            Icon = config.get('Desktop Entry','Icon')
        else:
            continue
        if Name not in exclude:
            app_lists.append({"name":Name,"exec":Exec,"icon":Icon})
    return app_lists

def filter_apps(apps, query):
    q = query.lower()
    return [a for a in apps if q in a["name"].lower()]

class WofiLike(Gtk.Window):
    def __init__(self):
        super().__init__(title="AppFinder")
        self.set_default_size(500, 400)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_border_width(10)
        self.all_apps = scan_desktop_entries()
        self.matched_apps = self.all_apps.copy()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)
        # 搜索框
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("查询程序...")
        self.search_entry.connect("changed", self.on_search_changed)
        vbox.pack_start(self.search_entry, False, True, 0)

        # ListStore: 0=GdkPixbuf对象，1=显示名称
        self.list_store = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        self.tree_view = Gtk.TreeView(model=self.list_store)
        self.tree_view.set_headers_visible(False)

        # 图标列
        cell_pix = Gtk.CellRendererPixbuf()
        col_icon = Gtk.TreeViewColumn()
        col_icon.pack_start(cell_pix, False)
        col_icon.add_attribute(cell_pix, "pixbuf", 0)
        self.tree_view.append_column(col_icon)

        # 文字列
        cell_text = Gtk.CellRendererText()
        col_text = Gtk.TreeViewColumn()
        col_text.pack_start(cell_text, True)
        col_text.add_attribute(cell_text, "text", 1)
        self.tree_view.append_column(col_text)

        self.tree_view.connect("row-activated", self.on_row_activate)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.tree_view)
        vbox.pack_start(scrolled, True, True, 0)
        self.selection = self.tree_view.get_selection()
        self.update_list()
        self.connect("key-press-event", self.on_window_key)

    def update_list(self):
        self.list_store.clear()
        for app in self.matched_apps:
            pix = load_icon(app["icon"])
            self.list_store.append([pix, app["name"]])
        if self.matched_apps:
            self.selection.select_path(Gtk.TreePath.new_from_indices([0]))

    def on_search_changed(self, entry):
        query = entry.get_text()
        self.matched_apps = filter_apps(self.all_apps, query)
        self.update_list()

    def on_window_key(self, widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()
            return True
        if event.keyval == Gdk.KEY_Down and self.search_entry.has_focus():
            self.tree_view.grab_focus()
            return True
        return False

    def on_row_activate(self, treeview, path, column):
        idx = path.get_indices()[0]
        app = self.matched_apps[idx]
        cmd = app["exec"]
        for ph in ["%U", "%u", "%i", "%d", "%c", "%k"]:
            cmd = cmd.replace(ph, "")
        cmd = cmd.strip()
        subprocess.Popen(cmd, shell=True, start_new_session=True)
        self.destroy()

if __name__ == "__main__":
    win = WofiLike()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.search_entry.grab_focus()
    Gtk.main()
