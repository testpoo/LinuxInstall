### 1. 安装labwc及相关软件
```
sudo apt install labwc swaybg swayidle swaylock wlr-randr fcitx5 fcitx5-rime rime-data-wubi thunar gvfs xarchiver pipewire-audio blueman thunar-archive-plugin fonts-noto-cjk foot xfce4-appfinder seatd xwayland git brightnessctl firefox-esr wlopm mako-notifier libglib2.0-bin waybar webext-ublock-origin-firefox firefox-esr-l10n-zh-cn --no-install-recommends
```
### 2. 启动labwc
```
# 编辑 ~/.profile加入以下内容即可：

if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  exec labwc
fi
```

#### 3. 输入法环境变量设置

启用fcitx输入需要配置环境变量：
```
nano ~/.config/labwc/environment

XIM="fcitx"
#GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
XMODIFIERS="@im=fcitx"
INPUT_METHOD=fcitx
SDL_IM_MODULE=fcitx
GLFW_IM_MODULE=fcitx
```

### 4. 其它
```
sudo chmod 666 /sys/class/backlight/intel_backlight/brightness
```