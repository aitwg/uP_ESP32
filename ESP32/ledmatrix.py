# max7219 demo for ESP32
# Reference code for ESP32
# 2020/05/04 v0.1
# https://github.com/mcauser/micropython-max7219

import max7219
import time
from machine import Pin, SPI

messages = ['P', 'I', 'X', 'E', 'L']

spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(4), mosi=Pin(2))
ss = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, ss, 1)
display.brightness(0)

while True:
  for item in messages:
    display.fill(0)
    display.text(item, 0, 0, 1)
    display.show()
    time.sleep(1)
