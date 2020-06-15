#myapp.py
import time, ntptime, dht
from machine import I2C, Pin, ADC
from esp8266_i2c_lcd import I2cLcd

def fill_zero(n):
    if n<10:
        return '0' + str(n)
    else:
        return str(n)

def fill_blank(n):        
    if n<10:
        return ' ' + str(n)
    else:
        return str(n)

#
#i2c=I2C(scl=Pin(5),sda=Pin(4),freq=400000)
# ESP32 SCL=GPIP22, SDA=GPIO21
i2c=I2C(scl=Pin(22),sda=Pin(21),freq=400000)
lcd=I2cLcd(i2c, 0x27, 2, 16)
lcd.custom_char(0, bytearray([0x1C,0x14,0x1C,0x00,0x00,0x00,0x00,0x00]))  

##DHTPIN=Pin(16, Pin.IN)
DHTPIN=Pin(14, Pin.IN)
# LEDPIN=Pin(14, Pin.OUT)
# d=dht.DHT11(DHTPIN)
d=dht.DHT22(DHTPIN)
##adc=ADC(0)

week={0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

try:
    ntptime.settime()
except:
    pass
n=0
while True:
    d.measure()              
    t=d.temperature()
    h=d.humidity()
    
    utc_epoch=time.mktime(time.localtime())
    Y,M,D,H,m,S,W,DY=time.localtime(utc_epoch + 28800)
    YMD='%s-%s-%s' % (str(Y),fill_zero(M),fill_zero(D))  
    Hm='%s:%s' % (fill_zero(H),fill_zero(m))
    T='%s%s' % (fill_blank(t),chr(0))
    H='%sH' % (fill_blank(h))
    lcd.move_to(0, 0)
    lcd.putstr(YMD)
    lcd.move_to(11, 0)  
    lcd.putstr(Hm)    
    lcd.move_to(0, 1)
    lcd.putstr(week[W])
    lcd.move_to(5, 1)    
    lcd.putstr(T)
    lcd.move_to(9, 1)
    lcd.putstr(H)
    time.sleep(1)  
    n=n+1
    if n >= 3600:
        try:
            ntptime.settime()
        except:
            pass
        n=0