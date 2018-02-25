import telegram
import sys,os
import time
from telegram.ext import Updater
from mwt import MWT
#初始数据
# bot = telegram.Bot(token="508830944:AAGdJMj2B8BSJ7tlV0oisa4ty2_9dMI386k")
# updates = bot.get_updates()
# updater = Updater(token='508830944:AAGdJMj2B8BSJ7tlV0oisa4ty2_9dMI386k')
# dispatcher = updater.dispatcher


# class InitData :


@MWT()
def z(a,b):
    return a + b

@MWT(timeout=5)
def x(a,b):
    return a + b

z(1,2)
x(1,3)

print (MWT()._caches)
#>>> {<function 'z'>: {(1, 2): (3, 1099276281.092)},<function 'x'> : {(1, 3): (4, 1099276281.092)}}

time.sleep(3)
MWT().collect()
print (MWT()._caches)
#>>> {<function 'z'>: {},<function 'x'> : {(1, 3): (4, 1099276281.092)}}








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
