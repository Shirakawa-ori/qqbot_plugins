# qqbot_plugins

----------
## 完成的几个qqbot插件 ##

 1. tianqi
    群内@bot就返回天气信息了，API是用的阿里的

 2. admin_authentication_redis
    管理员用户鉴权（不一定是管理员，换成别的角色也可以），需要用到redis（pip install redis），配置文件单独存放（引用需要绝对路径，不然会报错），私聊whoai即可返回限权信息（admin或other）。

 3. IOT_Light
    IOT方面的插件，控制IO电平（这里应用就是开关灯了），群内@bot使用。qqbot收到指令后把指令传给服务端，服务端这里用的是树莓派，下接Arduino，串口通信控制电平。
