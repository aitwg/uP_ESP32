# 2020/05/04 v0.3 demo code created.
# Complete project details at https://RandomNerdTutorials.com
# 
# https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py
# http://yhhuang1966.blogspot.com/2017/08/micropython-on-esp8266-ssd1306.html
# 2 I2C chips in the system
# 
from machine import Pin, I2C
import ssd1306
from time import sleep
import dht
import network
import time, ntptime
from esp8266_i2c_lcd import I2cLcd

import esp
esp.osdebug(None)
import gc
gc.collect()

# SSID & Password for your WiFi AP.
ssid = 'MEDIA_LINK'
password = '89124138af'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

try:
    ntptime.settime()
except:
    pass

# DHT22 Sensor at GPIO14.
sensor = dht.DHT22(Pin(14))
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

# ESP32 Pin assignment 
# ESP32 I2C SCL/GPIO22
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

# ESP8266 Pin assignment
#i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# ESP32 SCL=GPIP22, SDA=GPIO21
i2c_lcd=I2C(scl=Pin(22),sda=Pin(21),freq=400000)
lcd=I2cLcd(i2c_lcd, 0x27, 2, 16)                                #指定 I2C Slave 設備位址與顯示器之列數, 行數

while True:
    sleep(2)

    utc_epoch=time.mktime(time.localtime())
    Y,M,D,H,m,S,W,DY=time.localtime(utc_epoch + 28800)
    YMD='%s-%s-%s' % (str(Y),str(M),str(D))  
    Hm='%s:%s:%s' % (str(H),str(m),str(S))

    oled.fill(0)
    read_sensor()
    tempMsg = "Temp  = "+str(temp)
    humMsg  = "Humid = "+str(hum)
    print(tempMsg+" "+humMsg)
    print("\n")
    oled.text(tempMsg,0,0)
    oled.text(humMsg, 0, 10)
    oled.text(Hm, 0, 20)        
    oled.text(station.ifconfig()[0],0,30)
    oled.show()

    lcd.move_to(0,0)
    lcd.putstr("T/H  : " +str(temp) + "/" + str(hum))
    lcd.move_to(0,1)                                     
    lcd.putstr("Time : " + Hm)
    sleep(1)