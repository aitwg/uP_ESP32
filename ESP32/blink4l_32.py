from machine import Pin
import time

p15 = Pin(32, Pin.OUT)
p14 = Pin(33, Pin.OUT)
p13 = Pin(25, Pin.OUT)
p12 = Pin(26, Pin.OUT)

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
