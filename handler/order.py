
import telegram
from service import service
import dataList
from restrict import restrict
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler





#menu_reg='/orderB 安心油条 茶叶蛋 菜馅包子'
menu_reg='/orderB A5 加辣'

#点单命令
@restrict.RateLimited(1)
@restrict.cutoffRestricted
def order(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    
    datas = service.userOrder(updates.message)
    if datas:
        if len(datas) < 2 and 'WRONG_NOT_ALLINCLUE' in datas:
            bot.send_message(chat_id=chat_id, text='订单有误，每个名称要准确（参照菜单上的），间隔都是一个空格哦，\n参考格式：'+menu_reg)
            return
        if len(datas) < 2 and 'WRONG_NO_PARAMS' in datas:
            bot.send_message(chat_id=chat_id, text='啥也没点啊老哥，参考格式：'+menu_reg)
            return
        if datas[4]==0:
            state = '未付钱'
        elif datas[4]==1:
            state = '已付钱'
        elif datas[4]==2:
            state = '废弃订单'
        bot.send_message(chat_id=chat_id, text="单号               订单信息     创建时间            状态  费用\n"+datas[0]+'\n'+datas[1]+' ['+str(datas[2])+'] '+str(datas[3])+' '+state+' '+str(datas[5])+'p')
    else:
        bot.send_message(chat_id=chat_id, text='订单有误，每个名称要准确（参照菜单上的），间隔都是一个空格哦。参考格式：'+menu_reg)
   
handler = CommandHandler('orderB', order)