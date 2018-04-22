# qqbot_plugins
---------

本项目是基于qqbot的插件，需要配合qqbot使用。</br>
qqbot github 地址： <https://github.com/pandolia/qqbot>

----------
## 完成的几个qqbot插件 ##

 1. tianqi</br>
    群内@bot就返回天气信息了，API是用的阿里的

 2. admin_authentication_redis</br>
    由于接口改变，已挂</br>
    管理员用户鉴权（不一定是管理员，换成别的角色也可以），需要用到redis（pip install redis），配置文件单独存放（引用需要绝对路径，不然会报错），私聊whoai即可返回限权信息（admin或other）。

 3. IOT_Light</br>
    IOT方面的插件，控制IO电平（这里应用就是开关灯了），群内@bot使用。qqbot收到指令后把指令传给服务端，服务端这里用的是树莓派，下接Arduino，串口通信控制电平。

4.bilibili_TAGupdate_track.py</br>
b站关键词搜索更新，当初为了追踪新投稿用的，群内艾特触发，也用到了redis.

5.coc.py</br>
coc跑团用机器人。
