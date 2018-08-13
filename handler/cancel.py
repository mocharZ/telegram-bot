import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler



#取消订单命令
@restrict.RateLimited(1)
@restrict.cutoffRestricted
def cancel(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    dataCode = service.cancelOrder(updates.message)
    if dataCode  :
        if dataCode==6002:
            bot.send_message(chat_id=chat_id, text='取消订单有误，参考格式：/cancelB 1519781265240jo')
            return
        elif dataCode==666:
            bot.send_message(chat_id=chat_id, text='只能取消未付钱状态的单')
            return
        else:
            bot.send_message(chat_id=chat_id, text='奶爸有点忙处理不过来啊~~')
            return
    bot.send_message(chat_id=chat_id, text='取消订单成功')
    
handler = CommandHandler('cancelB', cancel)