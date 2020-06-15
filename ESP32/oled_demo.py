# Complete project details at https://RandomNerdTutorials.com

from machine import Pin, I2C
import ssdoled
from time import sleep

# ESP32 Pin assignment 
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
# i2c.scan()

# ESP8266 Pin assignment
#i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssdoled.SSD1306_I2C(oled_width, oled_height, i2c)

    #oled.fill(0)
oled.text('Hello, World 1!', 0, 0)
oled.text('Hello, World 2!', 0, 10)
oled.text('Hello, World 3!', 0, 20)    

oled.show()
sleep(3)