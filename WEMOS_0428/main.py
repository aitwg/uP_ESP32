# 2020/04/12 v2 for WeMOS D1 ESP8266
# 1.use asyncio instead of socket
# 2.add PostAction with find .find() function
# 3.fixed issues while useing mobile browser
# 04/13 change index.html buffer size to 1024
# 04/13 update index.html to bootstraps buttons/table style.
# 04/28 Replace ENB with GPIO16/D2 due to D10 break

import uasyncio as asyncio
import uos
import pkg_resources
from machine import Pin
from machine import PWM

"""
#define Pins_WeMos_D1_h
static const uint8_t PIN_D0 = 3;            //RX
static const uint8_t PIN_D1 = 1;            //TX
static const uint8_t PIN_D2 = 16;
static const uint8_t PIN_D3_D15 = 5;        //SCL
static const uint8_t PIN_D4_D14 = 4;        //SDA
static const uint8_t PIN_D5_D13 = 14;       //SCK
static const uint8_t PIN_D6_D12 = 12;       //MISO
static const uint8_t PIN_D7_D11 = 13;       //MOSI
static const uint8_t PIN_D8 = 0;
static const uint8_t PIN_D9_LED = 2;        //LED
static const uint8_t PIN_D10 = 15;          //SS

static const uint8_t PIN_A0 = 17;

static const uint8_t PIN_RX = 3;
static const uint8_t PIN_TX = 1;
static const uint8_t PIN_SCL = 5;
static const uint8_t PIN_SDA = 4;
static const uint8_t PIN_SCK = 114;
static const uint8_t PIN_MISO = 12;
static const uint8_t PIN_MOSI = 13;
static const uint8_t PIN_SS = 15;
static const uint8_t PIN_LED = 2;
#endif
"""

# GPIO Table for WeMos D1
# 2020/04/12
# 04/18 update IN3 from GPIO13 to 12
IN1 = 4
# IN2 = 5     #D15
# 04/28 Switch to D2
# D2/GPIO16 is not allowed for PWM, so switch to GPIO
# use GPIO5 as PWM instead.
IN2 = 16  # D2
IN3 = 12
IN4 = 14

ENA = 13   # D7
# 04/28 changed to D2/GPIO5
# ENB = 15   # D10
# ENB = 16   #D2
ENB = 5  # D15

# init p_IN1~p_IN4
print("init p_IN1~p_IN4")
p_IN1 = Pin(IN1, Pin.OUT)
p_IN2 = Pin(IN2, Pin.OUT)
p_IN3 = Pin(IN3, Pin.OUT)
p_IN4 = Pin(IN4, Pin.OUT)

M_Speed = 400
M_Step = 50
M_Default = 400
M_Max = 900
M_Min = 200

PWM_ENA = PWM(Pin(ENA))
PWM_ENB = PWM(Pin(ENB))

#
PWM_ENA.freq(400)
PWM_ENA.duty(M_Speed)

#
PWM_ENB.freq(400)
PWM_ENB.duty(M_Speed)


def m_Backward():
    p_IN1.on()
    p_IN2.off()
    p_IN3.on()
    p_IN4.off()
    # PWM_ENA.duty(M_Speed)
    # PWM_ENB.duty(M_Speed)


def m_Forward():
    p_IN1.off()
    p_IN2.on()
    p_IN3.off()
    p_IN4.on()
    # PWM_ENA.duty(M_Speed)
    # PWM_ENB.duty(M_Speed)


def m_Right():
    p_IN1.off()
    p_IN2.off()
    p_IN3.on()
    p_IN4.off()
    # PWM_ENA.duty(M_Speed)
    # PWM_ENB.duty(M_Speed)


def m_Left():
    p_IN1.off()
    p_IN2.off()
    p_IN3.off()
    p_IN4.on()
    # PWM_ENA.duty(M_Speed)
    # PWM_ENB.duty(M_Speed)


def m_Stop():
    p_IN1.off()
    p_IN2.off()
    p_IN3.off()
    p_IN4.off()
    # PWM_ENA.duty(M_Speed)
    # PWM_ENB.duty(M_Speed)


def m_Fast():
    print("<m_Fast>")
    global M_Speed
    global M_Step
    l_Speed = PWM_ENA.duty()
    if (l_Speed < M_Max):
        l_Speed = l_Speed + M_Step
    PWM_ENA.duty(l_Speed)
    PWM_ENB.duty(l_Speed)
    M_Speed = l_Speed
    print("<Exit m_Fast>")


def m_Slow():
    print("<m_Slow>")
    global M_Speed
    global M_Step
    l_Speed = PWM_ENA.duty()
    if (l_Speed > M_Min):
        l_Speed = l_Speed - M_Step
    PWM_ENA.duty(l_Speed)
    PWM_ENB.duty(l_Speed)
    M_Speed = l_Speed
    print("<Exit m_Slow>")


def m_Default():
    global M_Speed
    global M_Step
    print("<m_Default>")
    l_Speed = M_Default
    PWM_ENA.duty(l_Speed)
    PWM_ENB.duty(l_Speed)
    M_Speed = l_Speed
    print("<Exit m_Default>")


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
    sp_f = request.find('?moto=sp1')
    sp_s = request.find('?moto=sp2')
    sp_d = request.find('?moto=sp0')

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

    if sp_f != -1:
        print('speed fast')
        m_Fast()

    if sp_s != -1:
        print('speed slow')
        m_Slow()

    if sp_d != -1:
        print('speed Default')
        m_Default()

    print("moto state =", moto_state)
    print("Speed =", M_Speed)


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
        # writer.awrite(web_page())
        print(file)
        if exists(file):
            mime_type, cacheable = get_mime_type(file)
            yield from writer.awrite("HTTP/1.0 200 OK\r\n")
            yield from writer.awrite("Content-Type: {}\r\n".format(mime_type))
            if cacheable:
                yield from writer.awrite("Cache-Control: max-age=86400\r\n")
            yield from writer.awrite("\r\n")

            f = open(file, "rb")
            Web_buffer = f.read(3000)
            f.close()

            # workaround to fix apps switch case file not close and read again.
            # only read 1024 byte for this apps
            # while buffer != b'':
            if Web_buffer != b'':
                yield from writer.awrite(Web_buffer)
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
