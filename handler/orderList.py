import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler


#用户自己订单信息
@restrict.RateLimited(0.5)
def orderList(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    datas = service.getOrderListSelf(updates.message)
    if datas:
        bot.send_message(chat_id=chat_id, text='单号           订单信息    创建时间    状态 费用\n'+datas)
    else:
        bot.send_message(chat_id=chat_id, text='老铁你就一次也没点过早餐啊~')

handler = CommandHandler('GOLB', orderList)