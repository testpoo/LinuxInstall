### 1. 安装Sway及相关软件
```
sudo apt install fcitx5 fcitx5-rime rime-data-wubi thunar xarchiver pipewire-audio blueman thunar-archive-plugin fonts-noto-cjk sway swaybg swayidle swaylock foot wofi seatd xwayland grim git brightnessctl wl-clipboard slurp upower chromium chromium-l10n

# wl-clipboard 剪切板
# slurp 截图选框
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
# 编辑 ~/.profile加入以下内容即可：

if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  exec sway
fi
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

font=monospace:size=12
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

### 9. Chromium支持wayland并支持fcitx5

```
# 目前Chromium已经自动支持wayland和fcitx5，不再需要下面的语句，仅做留存
--ozone-platform=wayland --enable-wayland-ime --wayland-text-input-version=3 --gtk-version=4
```

### 10.  其他

```
# 修改微信文档目录，修改文件/home/poo/.xwechat/config/51a1fffea11325a1e4104c6b3de47af7.ini中使用以下内容
Appdata:.xwechat

# 若 polkit 未安装在您的系统上，并且您想使用 seatd 来替代，请将您添加到 seat 用户组并启用/启动 seatd.service，然后重新登录。
sudo usermod -aG seat poo
