### 1. 安装wayfire及相关软件
```
# 在wayfire下foot无法输入中文，终端替换成Sakura
sudo apt install wayfire swaybg swayidle swaylock fcitx5 fcitx5-rime rime-data-wubi thunar xarchiver pulseaudio blueman thunar-archive-plugin fonts-noto-cjk sakura wofi seatd xwayland git brightnessctl firefox-esr mako-notifier gsettings-desktop-schemas
```

### 2. 启动wayfire
```
# 编辑 ~/.profile加入以下内容即可：

if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  exec wayfire
fi
```

### 3. wayfire
```
cp /usr/share/wayfire/examples/wayfire.ini ~/.config/wayfire.ini
```

### 4. 输入法环境变量设置

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

### 5. 设置终端(foot)字体大小
```
cp -r /etc/foot/ ~/.config/foot/
vi ~/.config/foot/foot.ini

# 也可以直接在/etc/foot/foot.ini中修改
font=monospace:size=12
```

### 6. 配置文件修改

```
[input]
# 键入时禁用触摸板
disable_touchpad_while_typing = true

使用鼠标时禁用触摸板
disable_touchpad_while_mouse = true

[output]
scale = 1.250000

[core]
plugins = session_lock

[autostart]
autostart_wf_shell = false

# 状态栏
bar = waybar

# 桌面背景
background = swaybg -i '/home/poo/图片/2.jpg'

# 输入法
ime = fcitx5

# 蓝牙
bluetooth = blueman-applet

# 启动终端
# https://github.com/DanteAlighierin/foot
binding_terminal = <super> KEY_ENTER
command_terminal = foot

# 启动启动器
# https://hg.sr.ht/~scoopta/wofi
binding_launcher = <super> <shift> KEY_ENTER
command_launcher = wofi -S drun -I -G -p "请输入程序名称"

# 屏幕截图
# https://wayland.emersion.fr/grim/
# https://wayland.emersion.fr/slurp/
# https://github.com/bugaevc/wl-clipboard
binding_screenshot = KEY_PRINT
command_screenshot = grim - | wl-copy
binding_screenshot_interactive = <super> <shift> KEY_S
command_screenshot_interactive = grim -g "$(slurp)" - | wl-copy

# 音量控制
# https://github.com/pulseaudio
repeatable_binding_volume_up = KEY_VOLUMEUP
command_volume_up = pactl set-sink-volume @DEFAULT_SINK@ +5%
repeatable_binding_volume_down = KEY_VOLUMEDOWN
command_volume_down = pactl set-sink-volume @DEFAULT_SINK@ -5%
binding_mute = KEY_MUTE
command_mute = pactl set-sink-mute @DEFAULT_SINK@ toggle

# 屏幕亮度
# https://github.com/Hummer12007/brightnessctl
repeatable_binding_light_up = KEY_BRIGHTNESSUP
command_light_up = brightnessctl set 5%+
repeatable_binding_light_down = KEY_BRIGHTNESSDOWN
command_light_down = brightnessctl set 5%-
```

### 7. 其他

**禁止 `wofi` 多开**

```
#!/bin/bash

if pgrep -x "wofi" > /dev/null; then
    echo "Wofi is already running."
else
    wofi -S drun -I -G -p "请输入程序名称"
fi
```
**`gtk` 程序添加最大化和最小化按钮**

```
gsettings-desktop-schemas  # 这装这个软件

gsettings set org.gnome.desktop.wm.preferences button-layout ":minimize,maximize,close"  # 添加最大化和最小化按钮
gsettings set org.gnome.desktop.interface gtk-theme "主题名称"  # 设置主题
gsettings set org.gnome.desktop.interface icon-theme "图标主题名称"  # 设置图标
```
