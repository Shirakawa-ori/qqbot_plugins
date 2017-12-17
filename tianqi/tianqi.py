#-*- coding:utf-8 -*- - 

'''
@bot 天气
群内@的方式获取天气，用的阿里的API
'''

import urllib, urllib2,sys,json
reload(sys)
sys.setdefaultencoding( "utf-8" )

def Requestjson(url):
    appcode = '*********************************'
    //自己的appCode
    
    request = urllib2.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    response = urllib2.urlopen(request)
    try:
        dicjson = json.loads(response.read())
        return dicjson
    except:
        print 'getjson ERROR'
        return '0'

def gettianqi(city='北京'):
    host = 'http://jisutqybmf.market.alicloudapi.com'
    path = '/weather/query'
    method = 'GET'
    querys = 'city=' + city
    bodys = {}
    url = host + path + '?' + querys
    
    dicjson = Requestjson(url)

    if dicjson == '0':
        return '获取天气失败'
    else :
        pass

    city = str(dicjson['result'] ['city'])
    temphigh = str(dicjson['result'] ['temphigh'])
    templow = str(dicjson['result'] ['templow'])
    tmp = str(dicjson['result'] ['temp'])
    winddirect = str(dicjson['result'] ['winddirect'])
    windpower = str(dicjson['result'] ['windpower'])
    pm25 = str(dicjson['result'] ['aqi'] ['pm2_5'])
    updatetime = str(dicjson['result'] ['updatetime'])

    winddirect = winddirect[:-3]
    windpower = str(windpower)[:-3]

    mnx = templow+'~'+temphigh

    return '，查询的城市'+city+'，今日气温为'+mnx+'度，当前气温为'+tmp+'度，风向为'+winddirect+'风，风力'+windpower+'级，PM2.5指数为'+pm25+'μg/m?。更新时间：'+ updatetime

def onQQMessage(bot, contact, member, content):
    if '[@ME]  天气' in content:
        try :
            sms = str (gettianqi())
        except :
            sms =  ',哭哭，出错了。'
        bot.SendTo(contact, member.name+sms)

#print gettianqi()
