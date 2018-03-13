import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler



#当天开车订单信息
@restrict.RateLimited(0.5)
def orderListInterday(bot,updates):
    chat_id = updates.message.chat_id
    print(chat_id)
    datas = service.getOrderListIntraday(updates.message)
    if datas:
        bot.send_message(chat_id=chat_id, text=datas)
    else:
        bot.send_message(chat_id=chat_id, text='今天没人点餐？不可能吧？')

handler = CommandHandler('LL', orderListInterday)