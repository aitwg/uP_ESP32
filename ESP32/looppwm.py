from machine import Pin, PWM
import time


PWM2 = 23


pwm23 = PWM(Pin(23))
pwm23.freq()
pwm23.duty()

while True:
    pwm23.freq(50)
    pwm23.duty(30)
    time.sleep(3)
    pwm23.duty(90)
    time.sleep(3)
    pwm23.duty(150)
    time.sleep(3)
    pwm23.duty(180)
    time.sleep(3)
    pwm23.duty(256)
    time.sleep(3)
    pwm23.duty(512)
    time.sleep(3)
    pwm23.duty(768)
    time.sleep(3)