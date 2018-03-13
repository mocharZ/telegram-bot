import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler



#存款
@restrict.RateLimited(1)
@restrict.restricted
def doposit(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    datas = service.deposit(updates.message)
    print(datas['tel_id'])
    bot.send_message(chat_id=datas['tel_id'], text=datas['info']+datas['data'][0]+datas['data'][1]+datas['data'][2])

handler = CommandHandler('depositB', doposit)