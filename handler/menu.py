import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler



#菜单命令
@restrict.RateLimited(0.5)
def menu(bot,updates):
    chat_id = updates.message.chat_id
    print(chat_id)
    bot.send_message(chat_id=chat_id, text="下面是菜单")
    # bot.send_photo(chat_id=chat_id, photo=open('img/mm.jpg','rb'))
    bot.send_photo(chat_id=chat_id, photo=open('img/feimaoBreakfast.jpg','rb'))
    # bot.send_photo(chat_id=chat_id, photo=open('img/JiuJiuRed.jpg','rb'))

handler = CommandHandler('menu', menu)