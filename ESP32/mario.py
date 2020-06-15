from machine import Pin, PWM
import time


def mario(pwm):
    pwm.freq(659)  # E5
    pwm.duty(512)
    time.sleep_ms(150)
    pwm.deinit()
    time.sleep_ms(150)
    pwm.freq(659)  # E5
    pwm.duty(512)
    time.sleep_ms(150)
    pwm.deinit()
    time.sleep_ms(150)
    pwm.freq(659)  # E5
    pwm.duty(512)
    time.sleep_ms(150)
    pwm.deinit()
    time.sleep_ms(150)
    time.sleep_ms(150)
    pwm.freq(523)  # C5
    pwm.duty(512)
    time.sleep_ms(150)
    pwm.deinit()
    time.sleep_ms(150)
    pwm.freq(659)  # E5
    pwm.duty(512)
    time.sleep_ms(150)
    pwm.deinit()
    time.sleep_ms(150)
    time.sleep_ms(150)
    pwm.freq(784)  # G5
    pwm.duty(512)
    time.sleep_ms(150)


while True:
    pwm23 = PWM(Pin(23))
    mario(pwm23)
    pwm23.deinit()
    time.sleep(3)
