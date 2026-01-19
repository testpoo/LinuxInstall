#!/bin/bash

# 磁盘
diskUsage="💾"$(df -h | grep -F "/dev/sda2" | awk '{print $3}')

echo "<txt>$diskUsage</txt>"
echo "<tool>磁盘</tool>"