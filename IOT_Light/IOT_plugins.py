#-*- coding:utf-8 -*- -

'''
实现开灯关灯（更改电平）
qqbot（客户端）→树莓派（服务端）→Arduino（下位机）

此为群内@响应，私聊稍微改改就是
此为plugins（客户端）
'''

import socket  

address = ('127.0.0.1', 31500)

def Arduino_C( on ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.connect(address)
    s.send(on)
    status = s.recv(512)
    s.close()
    return status

def onQQMessage(bot, contact, member, content):
    if '[@ME]  开灯' in content:
        try :
            smsA =',OK:' + Arduino_C('O') 
        except :
            smsA =  ',哭哭，出错了。'
        bot.SendTo(contact, member.name+smsA)
    if '[@ME]  关灯' in content:
        try :
            smsA =',OK:' + Arduino_C('N')
        except :
            smsA =  ',哭哭，出错了。'
        bot.SendTo(contact, member.name+smsA)
