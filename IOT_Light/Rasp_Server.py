#-*- coding:utf-8 -*- -

'''
树莓派服务端，接收到socket后，通过串口控制Arduino
'''

import socket  
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
address = ('127.0.0.1', 31500)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()  
s.bind(address)  
s.listen(5)  

def serial_Arduino(words):
    print ser.isOpen()
    s = ser.write(words)
    time.sleep(0.1)

try:
    while (1):
        ss, addr = s.accept()  
        print 'got connected from',addr  
        ra = ss.recv(512)
        ss.send(ra)
        ss.close()
        serial_Arduino(ra)
except :
    print 'GG myfriend'
finally:
    print 'Colse'
    s.close()
    ser.close()
    exit(0)
