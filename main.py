import telegram
import sys
import os
from telegram import KeyboardButton,ReplyKeyboardMarkup,InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)
from util import build_menu
import logging
from functools import wraps
from mwt import MWT
from myFilter import RateLimited
import exception
import service
import dataList

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    datefmt="%A, %D %B %Y %H:%M:%S",
                    filename='log/myBot.log',
                    filemode='w')
#初始数据
bot = telegram.Bot(token="508830944:AAGdJMj2B8BSJ7tlV0oisa4ty2_9dMI386k")
updates = bot.get_updates()
updater = Updater(token='508830944:AAGdJMj2B8BSJ7tlV0oisa4ty2_9dMI386k')
dispatcher = updater.dispatcher

#限制对处理程序的访问（装饰器）
#这个装饰器允许你限制一个处理程序的访问权限，仅限于user_ids指定的LIST_OF_ADMINS。
def restricted(func):
    @wraps(func)
    def wrapped(bot, updates, *args, **kwargs):

        user_id = updates.effective_user.id
        if user_id not in dataList.LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            updates.message.reply_text(text="不好意思你无权限访问")
            return
        return func(bot, updates, *args, **kwargs)
    return wrapped

#截单限制
def cutoffRestricted(func):
    @wraps(func)
    def wrapped(bot, updates, *args, **kwargs):

        state = service.getOrderCutOff()
        print('是否截单：'+str(state))
        if state != 1:
            updates.message.reply_text(text="截单啦大神！~")
            return
        return func(bot, updates, *args, **kwargs)
    return wrapped

# 缓存的电报组管理员检查
# 如果您想限制某些机器人功能给组管理员，
# 您必须测试用户是否为该组中的管理员。
# 然而，这需要额外的API请求，这就是为什么在特定时间缓存这些信息是有意义的，特别是如果您的bot非常繁忙。
# @MWT(timeout=2)
# def get_admin_ids(bot, chat_id):
#     """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
#     return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


# menu_reg='/orderB 安心油条 茶叶蛋 菜馅包子'
menu_reg='/orderB A5 加辣'

#start命令
@RateLimited(2)
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


start_handler = CommandHandler('help', star)
dispatcher.add_handler(start_handler)

#菜单命令
@RateLimited(0.5)
def menu(bot,updates):
    chat_id = updates.message.chat_id
    print(chat_id)
    bot.send_message(chat_id=chat_id, text="下面是菜单")
    bot.send_photo(chat_id=chat_id, photo=open('img/YXK.jpg','rb'))

menu_handler = CommandHandler('menu', menu)
dispatcher.add_handler(menu_handler)

# def echo(bot, updates):
#     chat_id = updates.message.chat_id
#     bot.send_photo(chat_id=chat_id, photo='https://cache8.shzunliansy.com/app/telegram/breakfast.jpg')
#     bot.send_message(chat_id=chat_id, text="updates.message.text")
    
# echo_handler = MessageHandler(Filters.text, echo)
# dispatcher.add_handler(echo_handler)

#caps没加成功
# args = [ '确定','取消','万能键']
# print (args)
# def caps(bot, updates, args):
#     text_caps = ' '.join(args).upper()
#     print(text_caps)
#     bot.send_message(chat_id=updates.message.chat_id, text=text_caps)

# caps_handler = CommandHandler('caps', caps, pass_args=True)
# dispatcher.add_handler(caps_handler)

#内联模式启动 没成功 到时候再测试
# def inline_caps(bot, updates):
#     query = updates.inline_query.query
#     if not query:
#          return
#     results = list()
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     bot.answer_inline_query(updates.inline_query.id, results)

# inline_caps_handler = InlineQueryHandler(inline_caps)
# dispatcher.add_handler(inline_caps_handler)

# button_list = [
    # KeyboardButton(text="/food#酱爆鸡扒",callback_data=None),
    # KeyboardButton(text="/food#深海八爪鱼",callback_data=None),
    # KeyboardButton(text="/drink#神农山泉",callback_data=None),
    # ]
    # reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2))
    # bot.send_message(chat_id = chat_id, text="奶爸服务", reply_markup=reply_markup)
    #自定义按钮
    # custom_keyboard = [['/food#酱爆鸡扒', '/food#深海八爪鱼'], 
    #                ['/drink#神农山泉', '/drink#哇哈哈']]
    # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    # bot.send_message(chat_id=chat_id, 
    #               text="奶爸服务", 
    #               reply_markup=reply_markup)

#点单命令
@RateLimited(1)
@cutoffRestricted
def order(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    
    datas = service.userOrder(updates.message)
    if datas:
        if len(datas) < 2 and 'WRONG_NOT_ALLINCLUE' in datas:
            bot.send_message(chat_id=chat_id, text='订单有误，每个名称要准确（参照菜单上的），间隔都是一个空格哦，\n参考格式：/orderB 安心油条 茶叶蛋 菜馅包子')
            return
        if len(datas) < 2 and 'WRONG_NO_PARAMS' in datas:
            bot.send_message(chat_id=chat_id, text='啥也没点啊老哥，参考格式：/orderB 安心油条 茶叶蛋 菜馅包子')
            return
        if datas[4]==0:
            state = '未付钱'
        elif datas[4]==1:
            state = '已付钱'
        elif datas[4]==2:
            state = '废弃订单'
        bot.send_message(chat_id=chat_id, text="单号               订单信息     创建时间            状态  费用\n"+datas[0]+'\n'+datas[1]+' ['+str(datas[2])+'] '+str(datas[3])+' '+state+' '+str(datas[5])+'p')
    else:
        bot.send_message(chat_id=chat_id, text='订单有误，每个名称要准确（参照菜单上的），间隔都是一个空格哦。参考格式：/orderB 安心油条 茶叶蛋 菜馅包子')
   
order_handler = CommandHandler('orderB', order)
dispatcher.add_handler(order_handler)

#取消订单命令
@RateLimited(1)
@cutoffRestricted
def cancel(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    dataCode = service.cancelOrder(updates.message)
    if dataCode  :
        if dataCode==6002:
            bot.send_message(chat_id=chat_id, text='取消订单有误，参考格式：/cancelB 1519781265240jo')
            return
        else:
            bot.send_message(chat_id=chat_id, text='奶爸有点忙处理不过来啊~~')
            return
    bot.send_message(chat_id=chat_id, text='取消订单成功')
cancel_handler = CommandHandler('cancelB', cancel)
dispatcher.add_handler(cancel_handler)

#余额命令
@RateLimited(0.5)
def balance(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    logging.error(updates.message)
    datas=service.getBalance(updates.message)
    bot.send_message(chat_id=chat_id, text=datas[0]+datas[1]+datas[2])
    
    # bot.send_message(chat_id=chat_id, text=updates.user.get_chat_administrators+' '+updates.user.get_admin_ids)
    # bot.send_message(chat_id=chat_id, text='?2')

balance_handler = CommandHandler('balanceB', balance)
dispatcher.add_handler(balance_handler)

#用户自己订单信息
@RateLimited(0.5)
def orderList(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    datas = service.getOrderListSelf(updates.message)
    if datas:
        bot.send_message(chat_id=chat_id, text='单号           订单信息    创建时间    状态 费用\n'+datas)
    else:
        bot.send_message(chat_id=chat_id, text='老铁你就一次也没点过早餐啊~')

orderList_handler = CommandHandler('GOLB', orderList)
dispatcher.add_handler(orderList_handler)

#当天开车订单信息
@RateLimited(0.5)
def orderListInterday(bot,updates):
    chat_id = updates.message.chat_id
    print(chat_id)
    datas = service.getOrderListIntraday(updates.message)
    if datas:
        bot.send_message(chat_id=chat_id, text=datas)
    else:
        bot.send_message(chat_id=chat_id, text='今天没人点餐？不可能吧？')

orderListInterday_handler = CommandHandler('LL', orderListInterday)
dispatcher.add_handler(orderListInterday_handler)

#截单并显示当天订单信息
@RateLimited(0.5)
@restricted
def Cut_Off_Time(bot,updates):
    chat_id = updates.message.chat_id
    print(chat_id)
    datas = service.cutOffTime(updates.message)
    if datas:
        bot.send_message(chat_id=chat_id, text=datas)
    else:
        bot.send_message(chat_id=chat_id, text='今天没人点餐？不可能吧？')

Cut_off_Time_handler = CommandHandler('cutOffTime', Cut_Off_Time)
dispatcher.add_handler(Cut_off_Time_handler)

#存款
@RateLimited(1)
@restricted
def doposit(bot,updates):
    chat_id = updates.effective_user.id
    print(chat_id)
    datas = service.deposit(updates.message)
    print(datas['tel_id'])
    bot.send_message(chat_id=datas['tel_id'], text=datas['info']+datas['data'][0]+datas['data'][1]+datas['data'][2])

doposit_handler = CommandHandler('depositB', doposit)
dispatcher.add_handler(doposit_handler)


#服务命令
@RateLimited(1)
@restricted
def doService(bot,updates):
    chat_id = updates.message.chat_id
    print(chat_id)
    # button_list = [
    # InlineKeyboardButton(text="col1"),
    # InlineKeyboardButton(text="col2"),
    # InlineKeyboardButton(text="row 2"),
    # ]
    # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
    # bot.send_message(chat_id = chat_id, text="A two-column menu", reply_markup=reply_markup)
    #自定义按钮
    custom_keyboard = [['/order -点饭', '娱乐'], 
                   ['东莞一条龙', '学习'],
                   ['/delB -取消']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id=chat_id, 
                  text="奶爸服务", 
                  reply_markup=reply_markup)


service_handler = CommandHandler('service', doService)
dispatcher.add_handler(service_handler)

#清除按钮
@RateLimited(1)
@restricted
def close(bot,updates):
    chat_id = updates.message.chat_id
    service.closeConnection()
    bot.send_message(chat_id=chat_id, text="数据库关闭成功奶爸再次为你服务~")

close_handler = CommandHandler('close', close)
dispatcher.add_handler(close_handler)


#关闭所有自定义按钮
@restricted
def delB(bot,updates):
    chat_id = updates.message.chat_id
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(chat_id=chat_id, text="清除按钮成功奶爸再次为你服务~\n /menu -点饭", reply_markup=reply_markup)

delB_handler = CommandHandler('delB', delB)
dispatcher.add_handler(delB_handler)


#未知命令反馈
def unknown(bot, updates):
     bot.send_message(chat_id=updates.message.chat_id, text="欢迎使用超级奶爸机器人早餐服务~")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#错误回调
dispatcher.add_error_handler(exception.error_callback)



updater.start_polling()