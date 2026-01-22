### 1. 安装labwc及相关软件
```
sudo apt install labwc swaybg swayidle swaylock wlr-randr fcitx5 fcitx5-rime rime-data-wubi thunar gvfs xarchiver pipewire-audio blueman thunar-archive-plugin fonts-noto-cjk xfce4-terminal xfce4-appfinder git brightnessctl wlopm mako-notifier libglib2.0-bin xfce4-panel libglib2.0-bin firefox-esr webext-ublock-origin-firefox firefox-esr-l10n-zh-cn upower grim slurp xfce4-genmon-plugin wtype iwd polkitd ristretto

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
systemctl --user status pipewire
systemctl --user start pipewire

xfce4-genmon-plugin稳定版是4.1.1, 4.2以后才支持<css>标签，目前只支持gtk.css中书写， 所以支持强制在稳定版本中安装4.3
```