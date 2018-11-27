#!/bin/sh
ampy -p /dev/ttyUSB0 put $HOME/ampy/ampy_esp_8266_switch_light/boot.py  /boot.py
ampy -p /dev/ttyUSB0 put $HOME/ampy/ampy_esp_8266_switch_light/HTTPsServer.py  /main.py

echo "All files was copied successful"
