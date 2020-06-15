from machine import Pin

# GPIO Table for ESP8266 NodeMCU
# 2020/04/12
IN1 = 14  # D5/SCLK/GPIO14
IN2 = 12  # D6/MISO/GPIO12
IN3 = 13  # D7/MOSI/GPIO13
IN4 = 15  # D8/CS/GPIO15
ENA = 5   # D1
ENB = 4   # D2

p14 = Pin(14, Pin.OUT)
p14.on()
p14.value(1)
p14.value()
