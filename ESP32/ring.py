#
from machine import Pin, PWM
import time


def ringTone(pwm):
  for i in range(1, 11):  # 10 次迴圈 (1~10)
    pwm.freq(1000)        # 設定頻率為 1KHz
    pwm.duty(512)         # 設定工作週期為 50%
    time.sleep_ms(50)     # 持續時間 50 毫秒
    pwm.freq(500)         # 設定頻率為 500Hz
    time.sleep_ms(50)     # 持續時間 50 毫秒


while True:
  pwm = PWM(Pin(23))
  ringTone(pwm)
  pwm.deinit()
  time.sleep(2)
