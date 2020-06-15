# ESP32 - main.py
# 2020/04/11 v0.5
import time
from machine import Pin

IN1 = 32  #
IN2 = 33  #
IN3 = 25  #
IN4 = 26  #

# init p_IN1~p_IN4
print("init p_IN1~p_IN4")
p_IN1 = Pin(IN1, Pin.OUT)
p_IN2 = Pin(IN2, Pin.OUT)
p_IN3 = Pin(IN3, Pin.OUT)
p_IN4 = Pin(IN4, Pin.OUT)


def m_Forward():
  p_IN1.on()
  p_IN2.off()
  p_IN3.on()
  p_IN4.off()


def m_Backward():
  p_IN1.off()
  p_IN2.on()
  p_IN3.off()
  p_IN4.on()


def m_Left():
  p_IN1.off()
  p_IN2.off()
  p_IN3.on()
  p_IN4.off()


def m_Right():
  p_IN1.off()
  p_IN2.off()
  p_IN3.off()
  p_IN4.on()


def m_Stop():
  p_IN1.off()
  p_IN2.off()
  p_IN3.off()
  p_IN4.off()


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
