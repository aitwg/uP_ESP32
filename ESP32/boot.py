# ESP32 - boot.py
# 2020/04/11 v0.5

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MEDIA_LINK'
password = '89124138af'

ap = network.WLAN(network.AP_IF)
ap.active(True)

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
import webrepl
webrepl.start()
