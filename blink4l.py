from machine import Pin
import time

# GPIO Table for ESP8266 NodeMCU
# 2020/04/12
IN1 = 14  # D5/SCLK/GPIO14
IN2 = 12  # D6/MISO/GPIO12
IN3 = 13  # D7/MOSI/GPIO13
IN4 = 15  # D8/CS/GPIO15
ENA = 5   # D1
ENB = 4   # D2


p15 = Pin(15, Pin.OUT)
p14 = Pin(14, Pin.OUT)
p13 = Pin(13, Pin.OUT)
p12 = Pin(12, Pin.OUT)

while True:
    p15.on()
    time.sleep(1)
    p13.on()
    time.sleep(1)
    p14.on()
    time.sleep(1)
    p12.on()
    time.sleep(1)
    p15.off()
    time.sleep(1)
    p13.off()
    time.sleep(1)
    p14.off()
    time.sleep(1)
    p12.off()
    time.sleep(1)