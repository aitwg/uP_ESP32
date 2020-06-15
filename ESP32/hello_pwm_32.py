from machine import Pin
from machine import PWM
import time

PWM2 = 23


pwm23 = PWM(Pin(23))
pwm23.freq()
pwm23.duty()

index = 1
while True:
    pwm23.freq(50)
    pwm23.duty(128*(index%8))
    index += 1
    time.sleep(0.3)
