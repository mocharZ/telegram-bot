import telegram
import sys,os
import time
import paramiko
from telegram.ext import Updater
from mwt import MWT
import datetime
#初始数据
# bot = telegram.Bot(token="508830944:AAGdJMj2B8BSJ7tlV0oisa4ty2_9dMI386k")
# updates = bot.get_updates()
# updater = Updater(token='508830944:AAGdJMj2B8BSJ7tlV0oisa4ty2_9dMI386k')
# dispatcher = updater.dispatcher


# class InitData :


# @MWT()
# def z(a,b):
#     return a + b

# @MWT(timeout=5)
# def x(a,b):
#     return a + b

# z(1,2)
# x(1,3)

# print (MWT()._caches)
#>>> {<function 'z'>: {(1, 2): (3, 1099276281.092)},<function 'x'> : {(1, 3): (4, 1099276281.092)}}

# time.sleep(3)
# MWT().collect()
# print (MWT()._caches)
#>>> {<function 'z'>: {},<function 'x'> : {(1, 3): (4, 1099276281.092)}}

args = {'message_id': 682, 
        'date': 1519638094, 
        'chat': {'id': 356974645, 'type': 'private', 'username': 'Joey_Zhang', 'first_name': 'Joey', 'last_name': 'Zhang'}, 
        'text': '/balance joey', 
        'entities': [{'type': 'bot_command', 'offset': 0, 'length': 8}], 
        'caption_entities': [], 
        'photo': [], 
        'new_chat_members': [], 
        'new_chat_photo': [], 
        'delete_chat_photo': False, 
        'group_chat_created': False, 
        'supergroup_chat_created': False, 
        'channel_chat_created': False, 
        'from': {'id': 356974645, 'first_name': 'Joey', 'is_bot': False, 'last_name': 'Zhang', 'username': 'Joey_Zhang', 'language_code': 'zh-CN'},
        'new_chat_member': None}

# for key , value in args.items():
#     if key == 'from':
#         for inKey , inValue in args[key].items():
#                 if inKey == 'id':
#                         print(args[key][inKey])
#                 elif inKey == 'username':
#                         print(args[key][inKey])


# print( str(int(time.time()*1000))+str(int(time.clock()*1000000)))

print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
# strs = '/order 油条 鸡蛋 豆浆'.split(' ')
# del strs[0]
# print(' '.join(strs))

import time  
  

today = datetime.datetime.today()
datetime.datetime(today.year,today.month,today.day,0,0,0)
print(str(datetime.datetime(today.year,today.month,today.day,0,0,0)))

today = datetime.datetime.today()
today = datetime.datetime(today.year,today.month,today.day,0,0,0) 
tommorrow = today + datetime.timedelta(days=1)
print(str(tommorrow))
# print(bot.get_me())

#获取用户发送到bot的信息
# updates = bot.get_updates()
# print([u.message.text for u in updates])
# print([u.message.photo for u in updates if u.message.photo])

# chat_id = updates.message.chat_id
#发送消息
# bot.send_message(chat_id=356974645, text="长得帅有错？")
#回复用户
# updates[-1].message.reply_text("竦轻躯以鹤立，若将飞而未翔")

# bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)
# bot.send_message(chat_id=chat_id, 
#                 text="*bold* _italic_ `fixed width font` [link](http://google.com).", 
#                 parse_mode=telegram.ParseMode.MARKDOWN)

# bot.send_photo(chat_id=chat_id, photo=open('img/commonReply.jpg', 'rb'))
# bot.send_photo(chat_id=356974645, photo='http://ww2.sinaimg.cn/mw1024/7453fb7agw1elnshmn5d7g20dw07pb29.gif')

