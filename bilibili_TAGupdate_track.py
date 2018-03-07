#-*- coding:utf-8 -*- - 
#!/usr/bin/python

import commands
import re
import urllib2
import sys
import redis
import time
import random

url= "https://search.bilibili.com/all?keyword=Wota%E8%89%BA&page=1&order=pubdate"
redis_host = 'localhost'
redis_port = '6379'
redis_db = '1'
rs = redis.StrictRedis(host=redis_host,port=redis_port,db=redis_db)

def redis_ins(atdict,bot, contact):
    if atdict == 'nope' :
        bot.SendTo(contact, '获取更新失败，凉了')
    else:
        flag_updata = 0
        rs.delete('Cache_list')
        for avideo in atdict: 
            if rs.exists(avideo):
                print avideo,atdict[avideo]+ ' exists'
            else :
                rs.set(avideo,atdict[avideo])
                print avideo,atdict[avideo]+ ' NEW'
                time.sleep(random.uniform(0, 6))
                cmd = 'TAG:WOTA艺\n发现新投稿：'+avideo+'\n标题：'+atdict[avideo]
                bot.SendTo(contact, cmd)
                flag_updata = 1
                rs.sadd('Cache_list',avideo)
        time.sleep(random.uniform(0, 6))
        if flag_updata :
            bot.SendTo(contact, '获取更新完毕,技能冷却半小时。')
            locktime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            rs.set ('lock',locktime)
            rs.expire ('lock',1800)
        else :
            bot.SendTo(contact, '暂无更新，技能冷却十五分钟')
            locktime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            rs.set ('lock',locktime)
            rs.expire ('lock',900)


def get_data_list2dict(filename):
    cmd = "cat "+ filename +" | tr '[:cntrl:]' '\\n' | grep '<a href=\"//www.bilibili.com/video/' "
    (status, output) = commands.getstatusoutput( cmd )
    #print output
    link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')" ,output)
    video = []
    for url in link_list:
        url = url.lstrip('//www.bilibili.com/video/')
        url = url.split('?')
        video.append(url[0])
    title_list = re.findall(r"(?<=title=\").+?(?=\")|(?<=title=\').+?(?=\')" ,output)
    atdict = dict(zip(video,title_list))
    return atdict

def get_html(url):
    send_headers = {
     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
    }

    try :
        req = urllib2.Request(url,headers=send_headers)
        r = urllib2.urlopen(req)
        html = r.read()        #返回网页内容
        receive_header = r.info()     #返回的报头信息
    except:
        html = 0
        receive_header = 0

    #print receive_header
    #print html
    
    filename = "temp.html"
    if html != 0 :
        f=file(filename,"w")
        f.write(html)
        f.close()
        return get_data_list2dict(filename)
    else :
        return 'nope'

def Cache_output(bot, contact):
    time.sleep(random.uniform(0, 3))
    bot.SendTo(contact, '读取前次缓存')
    Cache_list = rs.smembers ('Cache_list')
    for avideo in Cache_list:
        title = rs.get(avideo)
        cmd = 'TAG:WOTA艺\n投稿：'+avideo+'\n标题：'+title
        bot.SendTo(contact, cmd)
        time.sleep(random.uniform(0, 3))
    bot.SendTo(contact, '读取完毕')


def onQQMessage(bot, contact, member, content):
    if '[@ME]  投稿更新' in content:
        if rs.exists('lock'):
            lock_ttl = rs.ttl('lock')
            lock_time = rs.get('lock')
            bot.SendTo(contact, '___技能正在冷却___\n上次使用时间：'+str(lock_time)+'\nCD还有'+str(lock_ttl)+'秒')
            print 'lock_query'
            Cache_output(bot, contact)           

        else :
            redis_ins(get_html(url),bot, contact)
