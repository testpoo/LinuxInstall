### 1. 安装Sway及相关软件
```
sudo apt install fcitx5 fcitx5-rime rime-data-wubi thunar xarchiver pipewire-audio blueman thunar-archive-plugin fonts-noto-cjk sway swaybg swayidle swaylock foot wofi seatd xwayland grim git brightnessctl wl-clipboard slurp upower webext-ublock-origin-firefox firefox-esr firefox-esr-l10n-zh-cn libglib2.0-bin

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

### 4. Chromium支持wayland并支持fcitx5

```
# 目前Chromium已经自动支持wayland和fcitx5，不再需要下面的语句，仅做留存
--ozone-platform=wayland --enable-wayland-ime --wayland-text-input-version=3 --gtk-version=4
```

### 5. 其他

```
# 修改微信文档目录，修改文件/home/poo/.xwechat/config/51a1fffea11325a1e4104c6b3de47af7.ini中使用以下内容
Appdata:.xwechat

# 若 polkit 未安装在您的系统上，并且您想使用 seatd 来替代，请将您添加到 seat 用户组并启用/启动 seatd.service，然后重新登录。
sudo usermod -aG seat poo
