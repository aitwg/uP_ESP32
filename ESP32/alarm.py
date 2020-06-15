from machine import Pin, PWM
import time


def alarmClockBeep(pwm):
  for i in range(1, 5):  # 4 次迴圈 (1~4)
    pwm.freq(1000)  # 設定頻率為 1KHz
    pwm.duty(512)  # 設定工作週期為 50%
    time.sleep_ms(100)  # 持續時間 0.1 秒
    pwm.deinit()  # 停止發聲
    time.sleep_ms(200)  # 持續時間 0.2 秒
  time.sleep_ms(800)


pwm23 = PWM(Pin(23))

while True:
  alarmClockBeep(pwm23)
