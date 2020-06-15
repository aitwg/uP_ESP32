# 2020/05/04 I2C LCD v0.1
from machine import I2C, Pin
from esp8266_i2c_lcd import I2cLcd

# i2c=I2C(scl=Pin(5),sda=Pin(4),freq=400000)                #指定 I2C 介面之 GPIO 與傳輸速率
# ESP32 SCL=GPIP22, SDA=GPIO21
i2c=I2C(scl=Pin(22),sda=Pin(21),freq=400000)
lcd=I2cLcd(i2c, 0x27, 2, 16)                                #指定 I2C Slave 設備位址與顯示器之列數, 行數
                                                            #0x27 or 0x3F
lcd.putstr("Hello World!\nIt's working!")                   #顯示字串
lcd.move_to(0,1)                                            #移到游標至第二列第一行位置 (跳行)
lcd.putstr("It's working!")    