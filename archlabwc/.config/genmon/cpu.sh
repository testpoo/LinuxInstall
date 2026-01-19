#!/bin/bash

# CPU
cpuUsage="©️"$(top -b -n1 | grep -F "Cpu" | awk '{printf "%d", 100-$8}')"%"

echo "<txt>$cpuUsage</txt>"
echo "<tool>CPU</tool>"