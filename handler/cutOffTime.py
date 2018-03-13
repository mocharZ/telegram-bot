import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler


#截单并显示当天订单信息
@restrict.RateLimited(0.5)
@restrict.restricted
def Cut_Off_Time(bot,updates):
    chat_id = updates.message.chat_id
    print(chat_id)
    datas = service.cutOffTime(updates.message)
    if datas:
        bot.send_message(chat_id=chat_id, text=datas)
    else:
        bot.send_message(chat_id=chat_id, text='今天没人点餐？不可能吧？')

handler = CommandHandler('cutOffTime', Cut_Off_Time)