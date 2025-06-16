### 1. 安装labwc及相关软件
```
sudo apt install labwc swaybg swayidle swaylock kanshi fcitx5 fcitx5-rime rime-data-wubi thunar xarchiver pulseaudio blueman thunar-archive-plugin fonts-noto-cjk foot wofi seatd xwayland git brightnessctl firefox-esr wlopm mako-notifier
```
### 2. 启动labwc
```
# 编辑 ~/.profile加入以下内容即可：

if [ -z "$DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
  exec labwc
fi
```
### 3. labwc
```
mkdir -p ~/.config/labwc
cp /usr/share/doc/labwc/* ~/.config/labwc/
```
#### 3.1. 输入法环境变量设置
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
#### 3.2. 添加快捷键rc.xml
```
    <!--自定义-->
    <keybind key="W-s">
      <action name="Execute" command="wofi --show=drun --lines=6 --allow-images --prompt='请输入软件名称'" />
    </keybind>
    <keybind key="XF86AudioRaiseVolume">
      <action name="Execute" command="pactl set-sink-volume @DEFAULT_SINK@ +5%" />
    </keybind>
    <keybind key="XF86AudioLowerVolume">
      <action name="Execute" command="pactl set-sink-volume @DEFAULT_SINK@ -5%" />
    </keybind>
    <keybind key="XF86AudioMute">
      <action name="Execute" command="pactl set-sink-mute @DEFAULT_SINK@ toggle" />
    </keybind>
    <keybind key="XF86AudioMicMute">
      <action name="Execute" command="pactl set-source-mute @DEFAULT_SOURCE@ toggle" />
    </keybind>
    <keybind key="XF86MonBrightnessDown">
      <action name="Execute" command="brightnessctl set 5%-" />
    </keybind>
    <keybind key="XF86MonBrightnessUp">
      <action name="Execute" command="brightnessctl set 5%+" />
    </keybind>
    <keybind key="W-s">
      <action name="Execute" command="wofi --show=drun -I --gtk-dark -x 0 -y 324 -W 300 -H 600 -p '请输入软件名称'" />
    </keybind>
    <keybind key="W-q">
      <action name="Execute" command="firefox-esr" />
    </keybind>
    <keybind key="W-e">
      <action name="Execute" command="thunar" />
    </keybind>
```    
#### 3.3 开机启动设置
```
nano autostart

# 背景设置
swaybg -i '/home/poo/图片/3.jpg' >/dev/null 2>&1 &

fcitx5 >/dev/null 2>&1 &
blueman-applet >/dev/null 2>&1 &
```
### 4. 设置终端(foot)字体大小
```
cp -r /etc/foot/ ~/.config/foot/
vi ~/.config/foot/foot.ini

font=monospace:size=12
```
### 5. 设置kanshi
```
mkdir -p ~/.config/kanshi
nano config

# 缩放1.25
profile nomad {
    output eDP-1 enable scale 1.25
}
```