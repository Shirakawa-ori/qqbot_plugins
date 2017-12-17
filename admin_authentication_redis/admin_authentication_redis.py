# -*- coding: utf-8 -*-
import redis
import sys,os
import ConfigParser

class get_config():
    def __init__(self):
        self.dict = {}

    def get_redis_config(self,config):
        self.dict['redis_host'] = config.get("redis", "redis_host")
        self.dict['redis_port'] = config.get("redis", "redis_port")
        self.dict['redis_db'] = config.get("redis", "redis_db")
        return self.dict
 
def conn_Redis_authentication(contact):
    conFile = '/root/.qqbot-tmp/plugins/config.ini'
    config = ConfigParser.ConfigParser()
    config.readfp(open(conFile))
    get_conf = get_config()
    redis_config = get_conf.get_redis_config(config)

    redis_host = redis_config['redis_host']
    redis_port = redis_config['redis_port']
    redis_db = redis_config['redis_db']
    rs = redis.StrictRedis(host=redis_host,port=redis_port,db=redis_db)
    
    #SADD adminlist *********
    
    adminlist = rs.smembers ('adminlist')
    for admin in adminlist :
        if str(contact.qq) == str(admin):
            return 1
    return 0

def onQQMessage(bot, contact, member, content):
    if content == 'whoami':
        if conn_Redis_authentication(contact):
            bot.SendTo(contact,'admin')
        else :
            bot.SendTo(contact,'other')
