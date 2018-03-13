import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler
import logging

#余额命令
@restrict.RateLimited(0.5)
def balance(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    logging.error(updates.message)
    datas=service.getBalance(updates.message)
    bot.send_message(chat_id=chat_id, text=datas[0]+datas[1]+datas[2])
    
    # bot.send_message(chat_id=chat_id, text=updates.user.get_chat_administrators+' '+updates.user.get_admin_ids)
    # bot.send_message(chat_id=chat_id, text='?2')

handler = CommandHandler('balanceB', balance)