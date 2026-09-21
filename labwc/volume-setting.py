#!/usr/bin/env python3
# coding=utf-8

import os

devices = os.popen("wpctl status | awk '/Sinks:/{f=1;next} /Sources:/{f=0} f'").read().split('\n')
devices = [device for device in devices if device not in (' │  ','')]
ndevices = []
for device in devices:
    device = device.split("[vol:")[0].split()
    if device[1] != '*':
        device =['',device[1].replace(".","")," ".join(device[2:])]
    else:
        device =[device[1],device[2].replace(".","")," ".join(device[3:])]
    ndevices.append(device)

for device in ndevices:
    print(str(ndevices.index(device)) + "：" + device[2] + " " + device[0])
num = input("请选择声卡序号：")
card_id = ndevices[int(num)][1]
result = os.system("wpctl set-default " + card_id)
if result == 0:
    print("设置声卡成功...")
else:
    print("设置声卡失败...")
input("按回车关闭...")