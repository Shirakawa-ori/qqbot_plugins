# -*- coding: UTF-8 -*- 
import redis
import random
from random import choice
import time
import base64

#Tool fun

def enbase64(s):
    #转base64
    return base64.encodestring(s)

def debase64(s):
    #base64转回来
    return base64.decodestring(s)

def conn_redis(redis_host = 'localhost',redis_port = '6379',redis_db = '15'):
    return redis.StrictRedis(host=redis_host,port=redis_port,db=redis_db) 

def rsflushdb(db):
    rs = conn_redis(redis_db = db)
    return str(rs.flushdb())

def getname(rs,name):
    rsname = name
    if rs.exists(rsname):
        return str(rs.get(rsname))
    else :
        return ''

#gen ran
def ran(min,max):
    i = 0
    ranlist = []
    ranumber = random.randint(min,max)
    while(i < 1):
        ranlist.append(ranumber)
        i = i+1
    return choice(ranlist)

#ran2 for !coc
def ran2():
    seed = random.randint(0,100)
    if seed < 80:
        return ran(6,14)
    elif seed > 90:
        return ran(3,6)
    else :
        return ran(15,16)

def ranlist(min,max,listlen):
    i = 0
    retlist = []
    while (i<listlen):
        #retlist.append(ran(min,max))
        retlist.append(ran2())
        i = i+1
    return retlist
    #return [ran(min,max),ran(min,max),ran(min,max),ran(min,max),ran(min,max),ran(min,max),ran(min,max),ran(min,max)]

def smsretList(listlen):
    i = 0
    smslist = []
    while(i < listlen):
        smslist.append(ranlist(3,16,9))
        i = i+1
    return smslist

def retrsname(name):
    try:
        rs1 = conn_redis(redis_db = '1')
        rsname = getname(rs1,enbase64(name))
        if rsname != '':
            name = debase64(rsname)
        else :
            pass
        return name
    except Exception,e:
        print e
        return name

#procedure fun
def rd(content,member):
    rs1 = conn_redis(redis_db = '1')
    num = int(content[3:])
    try:
        name = retrsname(member.name)
    except Exception,e:
        name = '暗投'
    sms =  name +' 投掷: ' + '1'+'d'+ str(num) +' = '+ str(ran(1,num))
    return sms

def coc(content,member):
    name = retrsname(member.name)
    if content[4:] == '':
        loopnum = 1
    else:
        loopnum = int(content[4:])
    if loopnum > 5:
        loopnum = 5
    else :
        pass
    valtemp = '''
* %s 投掷COC 6版 属性 : 
力量  %s 敏捷  %s 体质 %s 外表 %s 意志 %s 智力 %s 体型 %s 教育 %s 资产 %s 
'''
    sms = ''
    for i in smsretList(loopnum):
        smsone = valtemp % (name, str(i[0]), str(i[1]), str(i[2]), str(ran(3,16)), str(i[4]), str(i[5]), str(i[6]), str(i[7]), str(ran(3,10)))
        sms = sms+smsone
    return sms
    
def remapName(content,member):
    try:
        rs1 = conn_redis(redis_db = '1')
        if '%%' in content:
            newname = str(content[5:].split('%%')[0])
            if len(newname) <= 30:
                oldname = member.name
                rs1.set(enbase64(oldname),enbase64(newname))
                return oldname + ' ,设置了新名字: '+ newname
            else :
                return member.name + '名字必须小于30个字符(九个汉字)'
        else :
            return member.name + ' ,必须要以%%为结束符'
    except Exception,e:
        errsms = '嘤嘤嘤 error: ' + str(e)
        return errsms
    finally:
        pass

def myname(content,member):
    try:
        
        name = member.name
        rsname = getname(rs1,enbase64(name))
        if rsname != '':
            return name + ' ,设置的名字是: '+ debase64(rsname)
        else :
            return name + ' ,没有设置名字'
    except Exception,e:
        errsms = '嘤嘤嘤 error: ' + str(e)
        return errsms
    finally:
        pass

def mindmax(content,member):
        mm = str(content[2:])
        minmax = mm.split('d')
        min = int(minmax[0])
        max = min * int(minmax[1])
        try:
            name = retrsname(member.name)
        except Exception,e:
            name = '暗投'
        sms = name +' 投掷: ' + str(min) +'d'+ str(minmax[1]) + ' = ' + str(ran(min,max))
        return sms

#MesEnter fun
def onQQMessage(bot, contact, member, content):
    #rs = conn_redis(redis_db = '0')
    if '.rd' in content :
        bot.SendTo(contact,rd(content,member))
    elif '!coc' in content :
        bot.SendTo(contact,coc(content,member))
    elif './rsn' in content :
        bot.SendTo(contact,remapName(content,member))
    elif './myname' in content:
        bot.SendTo(contact,myname(content,member)) 
    elif './flushdb' == content:
        bot.SendTo(contact,rsflushdb(0))
    elif '.*'in content:
        if 'd' in content:
            bot.SendTo(contact,str(mindmax(content,member)))
    elif './help' == content:
        bot.SendTo(contact,'.rd(int|no max) or !coc(int|max 5) or ./rns(len 30)%% or ./myname')
