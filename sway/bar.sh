#!/bin/bash

# 捕获 USR1 信号
trap 'update_swaybar' SIGUSR1

# 启用JSON协议头
echo '{"version":1,"click_events":false}'
echo '[' # 开始JSON数组
echo '[]' # 初始化空数组

# 主循环生成状态信息
while true; do
  # 获取动态数据
  # 时间
  now_time=$(date '+%A %F %H:%M 第%V周')

  # 电量
  battary="电量:"$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "percentage\|time to empty" | awk -F ':' '{print $2,$4}' | sed 's/ //g') 
  # battary="ϟ "$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep -i "state\|percentage\|time to empty" | awk -F ':' '{print $2,$4}' | sed 's/ //g') 

  # 亮度
  light="亮度:"$(brightnessctl get | awk '{print $1/192"%"}')

  # 声音
  volume=$(wpctl get-volume @DEFAULT_AUDIO_SINK@ | awk -F ': ' '{print $2*100}')"%"
  if [[ $(wpctl status| grep '内置音频 模拟立体声') =~ "MUTED" ]];then volume="静音:"$volume;else volume="声音:"$volume;fi

  # CPU
  cpuUsage="CPU:"$(top -b -n1 | grep -F "Cpu" | awk '{printf "%d", 100-$8}')"%"

  # 内存
  mem_used_persent="内存:"$(free -m | grep -F "内存" | awk '{printf "%.1f",$3/1024}')"G"

  # 磁盘
  diskUsage="磁盘:"$(df -h | grep -F "/dev/sda2" | awk '{print $3}')

  # 网络
  if [ $(iwctl station wlan0 show | grep -F State | awk '{print $2}')="connected" ];then network="网络:连";else network="网络:断";fi

  # 触摸板
  touchpad="触控:"$(swaymsg -t get_inputs | python3 -c "import os,sys,json; print([li for li in json.load(sys.stdin) if li['identifier'] == '2362:597:SYNA3602:00_093A:0255_Touchpad'][0]['libinput']['send_events'])" | awk '{if ($0 == "enabled"){print "开"} else {print "关"}}')

  if [[ $touchpad =~ "触控:关" ]];then tcolor="#FF0000";else tcolor="#ffffff";fi
  if [[ $network =~ "网络:断" ]];then ncolor="#FF0000";else ncolor="#ffffff";fi
  if [[ $volume =~ "静音:" ]];then vcolor="#FF0000";else vcolor="#ffffff";fi

  # 构造带点击标识的JSON块
  JSON_BLOCKS=$(cat <<EOF
,[
  {"full_text":"$cpuUsage","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"#ffffff"},
  {"full_text":"$mem_used_persent","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"#ffffff"},
  {"full_text":"$diskUsage","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"#ffffff"},
  {"full_text":"$touchpad","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"$tcolor"},
  {"full_text":"$light","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"#ffffff"},
  {"full_text":"$volume","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"$vcolor"},
  {"full_text":"$network","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"$ncolor"},
  {"full_text":"$battary","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"#ffffff"},
  {"full_text":"$now_time","border":"#111111aa","border_left": 1,"border_right":1,"align":"center","background":"#111111aa","separator":false,"separator_block_width":2,"color":"#ffffff"}
]
EOF
  )

  echo "$JSON_BLOCKS"  
  sleep 5 &
  wait $!
done
