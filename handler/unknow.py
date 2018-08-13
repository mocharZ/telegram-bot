import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler


#未知命令反馈
def unknown(bot, updates):
     bot.send_message(chat_id=updates.message.chat_id, text="超级奶爸机器人提醒：你的命令有误~")

unknown_handler = MessageHandler(Filters.command, unknown)