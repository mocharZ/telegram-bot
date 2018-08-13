import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler


menu_reg='/orderB 安心油条 茶叶蛋 菜馅包子'
# menu_reg='/orderB B5'
# menu_reg='/orderB B1 A套餐 B套餐'
# menu_reg='/orderB 猪肉圆葱馅饼 肉三鲜水饺 疙瘩汤'
#start命令
@restrict.RateLimited(2)
def star(bot,updates):
    chat_id = updates.message.chat_id
    print(chat_id)
    user_id = updates.effective_user.id
    if user_id in dataList.LIST_OF_ADMINS:
        service.orderOpen()
    # if updates.message.from_user.id in get_admin_ids(bot, chat_id):
    #     # admin only
    #     bot.send_message(chat_id=chat_id, text="频率没问题 ")
    # else:
    #     bot.send_message(chat_id=chat_id, text="太快了宝贝")
    bot.send_message(chat_id=chat_id, text="快撑不住了嘛？！让奶爸奶你一口\n/menu - 早餐菜单\n\n点餐格式："+menu_reg+"\n\n/balanceB - 余额\n/GOLB 自己历史订单 \n/cancelB 取消订单(格式:/cancelB 1519781265240jo)\n/LL 查询今天全部订单信息")
    
    # bot.send_photo(chat_id=chat_id, photo='https://cache8.shzunliansy.com/app/telegram/breakfast.jpg')

handler = CommandHandler('help', star)