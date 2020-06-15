# sample code
# https://atceiling.blogspot.com/2019/12/micropython05esp32micropython.html
#
try:
  import usocket as socket
except:
  import socket

import network
from machine import Pin
import dht

import esp
esp.osdebug(None)

import gc
gc.collect()
import time

# 需更換自己無線AP的SSID及密碼
ssid = 'MEDIA_LINK'
password = '89124138af'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

sensor = dht.DHT22(Pin(14))
#sensor = dht.DHT11(Pin(14))

temp = hum = 0

def read_sensor():
  global temp, hum
  try:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    if (isinstance(temp, float) and isinstance(hum, float)) or (isinstance(temp, int) and isinstance(hum, int)):
      msg = (b'{0:3.1f},{1:3.1f}'.format(temp, hum))

      # 轉換成華氏溫度
      #temp = temp * (9/5) + 32.0

      hum = round(hum, 2)
    else:
      return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')

while True:
    time.sleep(1)
    read_sensor()
    print("Temp = "+str(temp)+" "+"Humid ="+str(hum))
    print("\n")