#!/usr/bin/env python3
# coding=utf-8

import os

os.system("iwctl station wlan0 scan")
print(os.popen("iwctl station wlan0 get-networks").read())
network = input("请输入网络SSID：")
result = os.system("iwctl station wlan0 connect " + network)
if result == 0:
    print("网络连接成功...")
else:
    print("网络连接失败...")
input("按回车关闭...")