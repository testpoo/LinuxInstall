#!/bin/bash

if grep -q '^disable_touchpad_while_mouse = true' ~/.config/wayfire.ini; then
    sed -i 's/disable_touchpad_while_mouse = true/disable_touchpad_while_mouse = false/' ~/.config/wayfire.ini
else
    sed -i 's/disable_touchpad_while_mouse = false/disable_touchpad_while_mouse = true/' ~/.config/wayfire.ini
fi