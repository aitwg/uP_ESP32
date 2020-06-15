# 2020/04/12 v2
# 1.use asyncio instead of socket
# 2.add PostAction with find .find() function
# 3.fixed issues while useing mobile browser
# 04/13 change index.html buffer size to 1024
# 04/13 update index.html to bootstraps buttons/table style.
# 04/17 added ENA/ENB for PWN support.
# 04/23 PWM demo code update

import uasyncio as asyncio
import uos
import pkg_resources
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


webroot = 'wwwroot'
default = 'index.html'
moto_state = "Stop"


def PostAction(request):

    print('Content = %s' % request)
    # 2020/4/12 removed "/" in find string
    moto_f = request.find('?moto=f')
    moto_b = request.find('?moto=b')
    moto_s = request.find('?moto=s')
    moto_l = request.find('?moto=l')
    moto_r = request.find('?moto=r')

    global moto_state

    if moto_f != -1:
        print('moto f')
        m_Forward()
        moto_state = "Forward"

    if moto_b != -1:
        print('moto b')
        m_Backward()
        moto_state = "Backward"

    if moto_s != -1:
        print('moto s')
        m_Stop()
        moto_state = "Stop"

    if moto_l != -1:
        print('moto l')
        m_Left()
        moto_state = "Left"

    if moto_r != -1:
        print('moto r')
        m_Right()
        moto_state = "Right"
    print("moto state =", moto_state)
# Breaks an HTTP request into its parts and boils it down to a physical file (if possible)

# 2020/04/12 add try: to avoid except while andriod browser switch/power off


def decode_path(req):
    try:
        cmd, headers = req.decode("utf-8").split('\r\n', 1)
        parts = cmd.split(' ')
        method, path = parts[0], parts[1]
        # remove any query string
        query = ''
        r = path.find('?')
        if r > 0:
            query = path[r:]
            path = path[:r]
        # check for use of default document
        if path == '/':
            path = default
        else:
            path = path[1:]
        print(query)
        PostAction(query)
        print(path)
    except:
        return ""
    # return the physical path of the response file
    return webroot + '/' + path

# Looks up the content-type based on the file extension


def get_mime_type(file):
    if file.endswith(".html"):
        return "text/html", False
    if file.endswith(".css"):
        return "text/css", True
    if file.endswith(".js"):
        return "text/javascript", True
    if file.endswith(".png"):
        return "image/png", True
    if file.endswith(".gif"):
        return "image/gif", True
    if file.endswith(".jpeg") or file.endswith(".jpg"):
        return "image/jpeg", True
    return "text/plain", False

# Quick check if a file exists


def exists(file):
    try:
        s = uos.stat(file)
        return True
    except:
        return False


@asyncio.coroutine
def serve(reader, writer):
    try:
        file = decode_path((yield from reader.read()))
        print(file)
        if exists(file):
            mime_type, cacheable = get_mime_type(file)
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: {}\r\n".format(mime_type))
            if cacheable:
                yield from writer.awrite("Cache-Control: max-age=86400\r\n")
            yield from writer.awrite("\r\n")

            f = open(file, "rb")
            buffer = f.read(4096)   # 2020/04/13 enlarge buffer to 4096
            f.close()
            # replace % with moto_state
            #global moto_state
            # buffer = (str)buffer
            #buffer = buffer % moto_state

            # workaround to fix apps switch case file not close and read again.
            # only read 1024 byte for this apps
            # while buffer != b'':
            if buffer != b'':
                yield from writer.awrite(buffer)
                #buffer = f.read(512)
            # f.close()
        else:
            yield from writer.awrite("HTTP/1.0 404 NA\r\n\r\n")
    except:
        raise
    finally:
        yield from writer.aclose()


def start():
    import logging
    # logging.basicConfig(level=logging.ERROR)
    logging.basicConfig(level=logging.INFO)

    loop = asyncio.get_event_loop()
    loop.call_soon(asyncio.start_server(serve, "0.0.0.0", 80, 20))
    loop.run_forever()
    loop.close()


start()
