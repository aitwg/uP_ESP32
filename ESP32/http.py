# ESP32 - http.py
# 2020/04/11 v0.5
# 2020/04/24 v0.6 added PWM support for ESP32

try:
  import usocket as socket
except:
  import socket
import time
from machine import Pin
from machine import PWM

IN1 = 32  #
IN2 = 33  #
IN3 = 25  #
IN4 = 26  #

ENA = 22   # D1
ENB = 23  # D2

# init p_IN1~p_IN4
print("init p_IN1~p_IN4")
p_IN1 = Pin(IN1, Pin.OUT)
p_IN2 = Pin(IN2, Pin.OUT)
p_IN3 = Pin(IN3, Pin.OUT)
p_IN4 = Pin(IN4, Pin.OUT)

p_ENA = Pin(ENA)
p_ENB = Pin(ENB)
PWM_ENA = PWM(p_ENA)
PWM_ENB = PWM(p_ENB)
PWM_ENA.freq(50)
PWM_ENB.freq(50)


def m_Forward():
  p_IN1.on()
  p_IN2.off()
  p_IN3.on()
  p_IN4.off()
  PWM_ENA.duty(30)
  PWM_ENB.duty(30)


def m_Backward():
  p_IN1.off()
  p_IN2.on()
  p_IN3.off()
  p_IN4.on()
  PWM_ENA.duty(150)
  PWM_ENB.duty(150)


def m_Left():
  p_IN1.off()
  p_IN2.off()
  p_IN3.on()
  p_IN4.off()
  PWM_ENA.duty(60)
  PWM_ENB.duty(60)


def m_Right():
  p_IN1.off()
  p_IN2.off()
  p_IN3.off()
  p_IN4.on()
  PWM_ENA.duty(120)
  PWM_ENB.duty(120)


def m_Stop():
  p_IN1.off()
  p_IN2.off()
  p_IN3.off()
  p_IN4.off()
  PWM_ENA.duty(0)
  PWM_ENB.duty(0)


def web_page():
  print("reading index_moto.html")
  file = open("index_moto.html", "r")
  page = file.read()
  file.close()
  return page


#servo = GPIO12/D12/MISO
#servo = machine.PWM(machine.Pin(12), freq=50)

# init socket
print("bind socket 80 and start listening")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  moto_f = request.find('/?moto=f')
  moto_b = request.find('/?moto=b')
  moto_s = request.find('/?moto=s')
  moto_l = request.find('/?moto=l')
  moto_r = request.find('/?moto=r')

  moto_state = "Stop"

  if moto_f == 6:
    print('moto f')
    m_Forward()
    moto_state = "Forward"

  if moto_b == 6:
    print('moto b')
    m_Backward()
    moto_state = "Backward"

  if moto_s == 6:
    print('moto s')
    m_Stop()
    moto_state = "Stop"

  if moto_l == 6:
    print('moto l')
    m_Left()
    moto_state = "Left"

  if moto_r == 6:
    print('moto r')
    m_Right()
    moto_state = "Right"

  response = web_page()

  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
