# LED demo for ESP8266
from machine import Pin
import time

led_no = [15, 13, 14, 12]


def switch_off():
  for led in leds:
    led.off()


leds = list()
for i in range(len(led_no)):
  led = Pin(led_no[i], Pin.OUT)
  leds.append(led)

while True:
  for led in leds:
    switch_off()
    led.on()
    time.sleep(1)
