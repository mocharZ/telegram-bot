import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler


#未知命令反馈
def unknown(bot, updates):
     bot.send_message(chat_id=updates.message.chat_id, text="欢迎使用超级奶爸机器人早餐服务~")

unknown_handler = MessageHandler(Filters.command, unknown)