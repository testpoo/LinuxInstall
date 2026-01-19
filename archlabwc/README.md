### 1. 安装Sway及相关软件
```
# 通过arch安装labwc

sudo pacman -S chromium thunar gvfs xarchiver thunar-archive-plugin fcitx5 fcitx5-rime git blueman wl-clipboard rime-wubi ristretto libreoffice-fresh man-db 7zip xfce4-appfinder libreoffice-fresh-zh-cn swaybg swayidle swaylock wlr-randr brightnessctl wlopm mako upower fuse xcb-util-image xfce4-terminal grim slurp xfce4-panel xfce4-genmon-plugin wtype

sudo pacman -Rns alacritty htop smartmontools vim wget wireless_tools wpa_supplicant lightdm lightdm-gtk-geeter
```

### 2. 启动Sway

```
# 编辑 ~/.bash_profile加入以下内容即可：

[ "$(tty)" = "/dev/tty1" ] && exec labwc
```

### 3.设置 Fcitx5 初始配置

配置 Group 直接启动 fcitx5 是只有西文键盘的，把下面的内容粘贴到 ~/.config/fcitx5/profile
```
[Groups/0]
# Group Name
Name=Default
# Layout
Default Layout=us
# Default Input Method
DefaultIM=rime

[Groups/0/Items/0]
# Name
Name=rime
# Layout
Layout=

[GroupOrder]
0=Default
```
DefaultIM=xx 为设置默认输入法，后面的Group中的Name为具体的输入法名字，按0，1，2……这样的编号排序，修改文件时，在要fcitx5关闭状态下，否则修改不生效。

### 4 安装fcitx5后配置

```
nano ~/.local/share/fcitx5/rime/default.custom.yaml
patch:
  schema_list:
    - schema: wubi_pinyin
    - schema: luna_pinyin_simp
    - schema: wubi86
```

### 5.添加Arch Linux CN 软件仓库源

```
# 在/etc/pacman.conf文件最后面添加
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch

# 然后安装archlinuxcn-keyring
pacman -Sy archlinuxcn-keyring
```

### 6. iwd无法联网

```
sudo nano /etc/iwd/main.conf

[General]
EnableNetworkConfiguration=true

sudo systemctl enable iwd.service --now
sudo systemctl enable systemd-resolved.service --now
systemctl restart iwd
```

### 7. 其他

```
# 若 polkit 未安装在您的系统上，并且您想使用 seatd 来替代，请将您添加到 seat 用户组并启用/启动 seatd.service，然后重新登录。
sudo systemctl enable seatd --now
sudo usermod -aG seat poo

# 通过wtype关联labwc root-menu，命令如下
echo "<icon>system-shutdown</icon><iconclick>wtype -M win p -m win</iconclick>"

# 强制xfce4-panel所有插件以内部方式运行
xfconf-query -c xfce4-panel -p /force-all-internal -t bool -s true --create

# 安装Motrix appimage包，需要安装依赖 fuse；安装微信appimage包，需要安装依赖xcb-util-image。

# libreoffice 护眼色：C7EDCC

# 查字体
fc-match
fc-match -a | grep Mono  # 等线字体
```