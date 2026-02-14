### 1. Arch下的Labwc和Sway

#### 1.1. 安装Labwc/Sway及相关软件

- arch下安装labwc及相关软件

```
sudo pacman -S chromium thunar gvfs xarchiver thunar-archive-plugin xfce4-panel xfce4-genmon-plugin foot fcitx5 fcitx5-rime rime-wubi git blueman wl-clipboard ristretto libreoffice-fresh libreoffice-fresh-zh-cn man-db 7zip swaybg swayidle swaylock wlr-randr brightnessctl wlopm mako upower grim slurp wtype

# 可选:cmus mp3插件, Motrix需要, 微信需要, 图标
cmus libmad fuse xcb-util-image tela-circle-icon-theme-blue

sudo pacman -Rns alacritty htop smartmontools vim wget wireless_tools wpa_supplicant lightdm lightdm-gtk-greeter
```
- arch下安装sway及相关软件

```
sudo pacman -S thunar chromium gvfs fcitx5 fcitx5-rime xarchiver git upower blueman thunar-archive-plugin wl-clipboard rime-wubi ristretto libreoffice-fresh man-db 7zip xfce4-appfinder libreoffice-fresh-zh-cn

sudo pacman -Rns lightdm lightdm-gtk-greeter htop smartmontools vim waybar wget wireless_tools wpa_supplicant pavucontrol wmenu
```

#### 1.2. 启动Labwc/Sway

```
# 编辑 ~/.bash_profile加入以下内容即可：

[ "$(tty)" = "/dev/tty1" ] && exec labwc

[ "$(tty)" = "/dev/tty1" ] && exec sway
```

#### 1.3.设置 Fcitx5 初始配置

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

#### 1.4.添加Arch Linux CN 软件仓库源

```
# 在/etc/pacman.conf文件最后面添加
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch

# 然后安装archlinuxcn-keyring
pacman -Sy archlinuxcn-keyring
```

#### 1.5. iwd无法联网

```
sudo nano /etc/iwd/main.conf

[General]
EnableNetworkConfiguration=true

sudo systemctl enable iwd.service --now
sudo systemctl enable systemd-resolved.service --now
systemctl restart iwd
```

#### 1.6. 其他

```
# 若 polkit 未安装在您的系统上，并且您想使用 seatd 来替代，请将您添加到 seat 用户组并启用/启动 seatd.service，然后重新登录。
sudo systemctl enable seatd --now
sudo usermod -aG seat poo

# 通过wtype关联labwc root-menu，通过xfce启动器实现
名称：Arch程序菜单  命令：wtype -M logo -k s

# 强制xfce4-panel所有插件以内部方式运行
xfconf-query -c xfce4-panel -p /force-all-internal -t bool -s true --create

# 安装Motrix appimage包，需要安装依赖 fuse；安装微信appimage包，需要安装依赖xcb-util-image。

# libreoffice 护眼色：C7EDCC

# 解决 Chromium 浏览器卡顿缓慢的问题（在抖音和B站放视频页面卡住），禁用GPU加速：
1. 打开 Chromium 浏览器，进入“设置 → 系统”，将 使用图形加速功能 的选项关闭掉，重启浏览器。如果设置后卡顿已有明显改善，那么就此搞定，不然继续第二步。
2. 在地址栏上输入：chrome://flags/ 回车，在顶部搜索栏中搜索“gpu”，列表中找到：“GPU rasterization”(GPU 渲染) 以及 “Accelerated 2D canvas”(2D 图形加速) 两项，将它们都设为“Disabled”禁用即可。点击右下角的“ReLaunch”重启浏览器。

# 查字体
fc-match
fc-match -a | grep Mono  # 等线字体

# libreoffice问题
# libreoffice打开提示错误，加载libswlo.so失败，使用下面的命令查找缺失的程序，然后安装
ldd /usr/lib/libreoffice/program/libswlo.so | grep "not found"
```

### 2. Debian下的Labwc、Sway和Wayfire

#### 2.1. 安装Sway/Labwc/Wayfire及相关软件

- Debian下安装sway及相关软件

```
sudo apt install fcitx5 fcitx5-rime rime-data-wubi thunar xarchiver pipewire-audio blueman thunar-archive-plugin fonts-noto-cjk sway swaybg swayidle swaylock foot wofi xwayland grim git brightnessctl wl-clipboard slurp upower webext-ublock-origin-firefox firefox-esr firefox-esr-l10n-zh-cn libglib2.0-bin iwd

# wl-clipboard 剪切板
# slurp 截图选框

sudo apt autoremove --purge wpasupplicant
```

- Debian下安装labwc及相关软件

```
sudo apt install labwc swaybg swayidle swaylock wlr-randr fcitx5 fcitx5-rime rime-data-wubi thunar thunar-archive-plugin xfce4-terminal xfce4-appfinder xfce4-panel xfce4-genmon-plugin xarchiver pipewire-audio blueman fonts-noto-cjk git brightnessctl wlopm mako-notifier upower grim slurp wl-clipboard wtype iwd ristretto libglib2.0-bin amberol firefox-esr firefox-esr-l10n-zh-cn webext-ublock-origin-firefox libreoffice libreoffice-l10n-zh-cn libreoffice-gtk3

sudo apt autoremove --purge wpasupplicant
```

- Debian下安装wayfire及相关软件

```
sudo apt install wayfire swaybg swayidle swaylock fcitx5 fcitx5-rime rime-data-wubi thunar xarchiver pipewire-audio blueman thunar-archive-plugin fonts-noto-cjk xfce4-terminal xfce4-appfinder seatd xwayland git brightnessctl firefox-esr webext-ublock-origin-firefox firefox-esr-l10n-zh-cn mako-notifier grim wl-clipboard slurp libglib2.0-bin waybar chromium chromium-l10n
```

#### 2.2. 启动Sway

```
# 编辑 ~/.profile加入以下内容即可：

if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  exec sway
fi

if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  exec labwc
fi

if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  exec wayfire
fi
```
#### 2.3. iwd无法联网

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

#### 2.4. 其他

```
# 启动pipewire
systemctl --user status pipewire
systemctl --user start pipewire

# 通过wtype关联labwc root-menu，通过xfce启动器实现
名称：程序菜单  命令：wtype -M logo -k p

# 强制xfce4-panel所有插件以内部方式运行
xfconf-query -c xfce4-panel -p /force-all-internal -t bool -s true --create

# gtk程序添加最大化和最小化按钮，需要安装libglib2.0-bin
gsettings set org.gnome.desktop.wm.preferences button-layout ":minimize,maximize,close"  # 添加最大化和最小化按钮
gsettings set org.gnome.desktop.interface gtk-theme "主题名称"  # 设置主题
gsettings set org.gnome.desktop.interface icon-theme "图标主题名称"  # 设置图标

# xfce4-genmon-plugin稳定版是4.1.1, 4.2以后才支持<css>标签，目前只支持gtk.css中书写， 所以强制在稳定版本中安装4.3
```

### 3. Fcitx5相关设置

#### 3.1. 输入法环境变量设置

启用fcitx输入需要配置环境变量：
```
nano /etc/environment

XIM="fcitx"
#GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS="@im=fcitx"
INPUT_METHOD=fcitx
SDL_IM_MODULE=fcitx
GLFW_IM_MODULE=fcitx
```

#### 3.2 安装fcitx5后配置

```
nano ~/.local/share/fcitx5/rime/default.custom.yaml
patch:
  schema_list:
    - schema: wubi_pinyin
    - schema: luna_pinyin_simp
    - schema: wubi86
```

#### 3.3. Chromium支持wayland并支持fcitx5

```
# 目前Chromium已经自动支持wayland和fcitx5，不再需要下面的语句，仅做留存
--ozone-platform=wayland --enable-wayland-ime --wayland-text-input-version=3 --gtk-version=4
```