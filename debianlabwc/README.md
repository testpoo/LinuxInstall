### 1. 安装labwc及相关软件
```
sudo apt install labwc swaybg swayidle swaylock wlr-randr fcitx5 fcitx5-rime rime-data-wubi thunar thunar-archive-plugin xfce4-terminal xfce4-appfinder xfce4-panel xfce4-genmon-plugin xarchiver pipewire-audio blueman fonts-noto-cjk git brightnessctl wlopm mako-notifier firefox-esr webext-ublock-origin-firefox firefox-esr-l10n-zh-cn upower grim slurp wl-clipboard wtype iwd ristretto libglib2.0-bin amberol libreoffice libreoffice-l10n-zh-cn libreoffice-gtk3

sudo apt autoremove --purge wpasupplicant
```
### 2. 启动labwc
```
# 编辑 ~/.profile加入以下内容即可：

if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  exec labwc
fi
```
### 3. iwd无法联网

```
sudo nano /etc/iwd/main.conf

[General]
EnableNetworkConfiguration=true

sudo systemctl enable iwd.service --now

sudo nano /etc/resolv.conf

nameserver 223.5.5.5
nameserver 119.29.29.29

systemctl restart iwd
```
### 4. 其他

```
# 启动pipewire
systemctl --user status pipewire
systemctl --user start pipewire

# 通过wtype关联labwc root-menu，通过xfce启动器实现
名称：程序菜单  命令：wtype -M logo -k s

# 强制xfce4-panel所有插件以内部方式运行
xfconf-query -c xfce4-panel -p /force-all-internal -t bool -s true --create

xfce4-genmon-plugin稳定版是4.1.1, 4.2以后才支持<css>标签，目前只支持gtk.css中书写， 所以强制在稳定版本中安装4.3
```