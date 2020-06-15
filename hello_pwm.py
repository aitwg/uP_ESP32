from machine import Pin
from machine import PWM

# GPIO Table for ESP8266 NodeMCU
# 2020/04/12
IN1 = 14  # D5/SCLK/GPIO14
IN2 = 12  # D6/MISO/GPIO12
IN3 = 13  # D7/MOSI/GPIO13
IN4 = 15  # D8/CS/GPIO15
ENA = 5   # D1
ENB = 4   # D2

pwm4 = PWM(Pin(4))
pwm4.freq()
pwm4.duty()
pwm5 = PWM(Pin(5))
pwm5.freq()
pwm5.duty()

pwm4.freq(50)
pwm5.freq(50)
pwm4.duty(30)
pwm5.duty(30)
