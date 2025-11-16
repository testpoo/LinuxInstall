### 1. 安装Sway及相关软件
```
# 通过arch安装sway

sudo pacman -S thunar chromium gvfs fcitx5 fcitx5-rime xarchiver git upower blueman thunar-archive-plugin wl-clipboard rime-wubi ristretto libreoffice-fresh man-db 7zip xfce4-appfinder libreoffice-fresh-zh-cn

sudo pacman -Rns lightdm lightdm-gtk-greeter htop smartmontools vim waybar wget wireless_tools wpa_supplicant pavucontrol wmenu
```

### 2. 输入法环境变量设置

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

### 3. 启动Sway

```
# 编辑 ~/.bash_profile加入以下内容即可：

[ "$(tty)" = "/dev/tty1" ] && exec sway
```

### 4. 配置sway

```
mkdir -p ~/.config/sway
cp /etc/sway/config ~/.config/sway/

# 编辑~/.config/sway
```

### 5. 修改程序启动器

```
# 注释掉$menu行，改为以下内容：
set $menu set $menu xfce4-appfinder
```

### 6. 设置终端(foot)字体大小

```
cp -r /etc/foot/ ~/.config/foot/
vi ~/.config/foot/foot.ini

font=FreeMono:size=12
```

### 7. 设置分辨率和缩放

```
swaymsg -t get_outputs
output eDP-1 resolution 1920x1200 position 0,0 scale 1.25
```

### 8. 设置触摸板

```
swaymsg -t get_inputs
input "2362:597:SYNA3602:00_093A:0255_Touchpad" {
    dwt enabled
    tap enabled
    natural_scroll enabled
    middle_emulation enabled
    events enabled
}
```

### 9.设置 Fcitx5 初始配置

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

#### 9.1 安装fcitx5后配置

```
nano ~/.local/share/fcitx5/rime/default.custom.yaml
patch:
  schema_list:
    - schema: wubi_pinyin
    - schema: luna_pinyin_simp
    - schema: wubi86
```

### 9.添加Arch Linux CN 软件仓库源

```
# 在/etc/pacman.conf文件最后面添加
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch

# 然后安装archlinuxcn-keyring
pacman -Sy archlinuxcn-keyring
```

### 10. Arch Wifi慢

- 查看网卡型号：`lspci| grep Net`，本机的型号是RTL8821CE

- 查看驱动：`lsmod | grep 8821`

- 切换驱动：`modprobe rtw88_8821ce`


### 11. iwd无法联网

```
sudo nano /etc/iwd/main.conf

[General]
EnableNetworkConfiguration=true

sudo systemctl enable iwd.service --now
sudo systemctl enable systemd-resolved.service --now
systemctl restart iwd
```

### 12.  其他

```
# 修改微信文档目录，修改文件/home/poo/.xwechat/config/51a1fffea11325a1e4104c6b3de47af7.ini中使用以下内容
Appdata:.xwechat

# 若 polkit 未安装在您的系统上，并且您想使用 seatd 来替代，请将您添加到 seat 用户组并启用/启动 seatd.service，然后重新登录。
sudo usermod -aG seat poo

# 安装Motrix appimage包，需要安装依赖 fuse；安装微信appimage包，需要安装依赖xcb-util-image。

# 查字体
fc-match
fc-match -a | grep Mono  # 等线字体
```
