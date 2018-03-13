import telegram
import sys
import os
from telegram import KeyboardButton,ReplyKeyboardMarkup,InlineQueryResultArticle, InputTextMessageContent,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import Updater,MessageHandler, Filters,CommandHandler,InlineQueryHandler,RegexHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

from functools import wraps
from service import service
import dataList
from restrict import restrict
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    datefmt="%A, %D %B %Y %H:%M:%S",
                    filename='log/myBot.log',
                    filemode='w')
# # 缓存的电报组管理员检查
# # 如果您想限制某些机器人功能给组管理员，
# # 您必须测试用户是否为该组中的管理员。
# # 然而，这需要额外的API请求，这就是为什么在特定时间缓存这些信息是有意义的，特别是如果您的bot非常繁忙。
# # @MWT(timeout=2)
# # def get_admin_ids(bot, chat_id):
# #     """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
# #     return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]



# start_handler = CommandHandler('help', star)
# dispatcher.add_handler(start_handler)

# #菜单命令
# @restrict.RateLimited(0.5)
# def menu(bot,updates):
#     chat_id = updates.message.chat_id
#     print(chat_id)
#     bot.send_message(chat_id=chat_id, text="下面是菜单")
#     bot.send_photo(chat_id=chat_id, photo=open('img/YXK.jpg','rb'))

# menu_handler = CommandHandler('menu', menu)
# dispatcher.add_handler(menu_handler)

# # def echo(bot, updates):
# #     chat_id = updates.message.chat_id
# #     bot.send_photo(chat_id=chat_id, photo='https://cache8.shzunliansy.com/app/telegram/breakfast.jpg')
# #     bot.send_message(chat_id=chat_id, text="updates.message.text")
    
# # echo_handler = MessageHandler(Filters.text, echo)
# # dispatcher.add_handler(echo_handler)

# #caps没加成功
# # args = [ '确定','取消','万能键']
# # print (args)
# # def caps(bot, updates, args):
# #     text_caps = ' '.join(args).upper()
# #     print(text_caps)
# #     bot.send_message(chat_id=updates.message.chat_id, text=text_caps)

# # caps_handler = CommandHandler('caps', caps, pass_args=True)
# # dispatcher.add_handler(caps_handler)

# #内联模式启动 没成功 到时候再测试
# # def inline_caps(bot, updates):
# #     query = updates.inline_query.query
# #     if not query:
# #          return
# #     results = list()
# #     results.append(
# #         InlineQueryResultArticle(
# #             id=query.upper(),
# #             title='Caps',
# #             input_message_content=InputTextMessageContent(query.upper())
# #         )
# #     )
# #     bot.answer_inline_query(updates.inline_query.id, results)

# # inline_caps_handler = InlineQueryHandler(inline_caps)
# # dispatcher.add_handler(inline_caps_handler)

# # button_list = [
#     # KeyboardButton(text="/food#酱爆鸡扒",callback_data=None),
#     # KeyboardButton(text="/food#深海八爪鱼",callback_data=None),
#     # KeyboardButton(text="/drink#神农山泉",callback_data=None),
#     # ]
#     # reply_markup = ReplyKeyboardMarkup(build_menu(button_list, n_cols=2))
#     # bot.send_message(chat_id = chat_id, text="奶爸服务", reply_markup=reply_markup)
#     #自定义按钮
#     # custom_keyboard = [['/food#酱爆鸡扒', '/food#深海八爪鱼'], 
#     #                ['/drink#神农山泉', '/drink#哇哈哈']]
#     # reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
#     # bot.send_message(chat_id=chat_id, 
#     #               text="奶爸服务", 
#     #               reply_markup=reply_markup)






# #服务命令
# @restrict.RateLimited(1)
# @restrict.restricted
# def doService(bot,updates):
#     chat_id = updates.message.chat_id
#     print(chat_id)
#     # button_list = [
#     # InlineKeyboardButton(text="col1"),
#     # InlineKeyboardButton(text="col2"),
#     # InlineKeyboardButton(text="row 2"),
#     # ]
#     # reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))
#     # bot.send_message(chat_id = chat_id, text="A two-column menu", reply_markup=reply_markup)
#     #自定义按钮
#     custom_keyboard = [['/order -点饭', '娱乐'], 
#                    ['东莞一条龙', '学习'],
#                    ['/delB -取消']]
#     reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
#     bot.send_message(chat_id=chat_id, 
#                   text="奶爸服务", 
#                   reply_markup=reply_markup)


# service_handler = CommandHandler('service', doService)
# dispatcher.add_handler(service_handler)

# #清除按钮
# @restrict.RateLimited(1)
# @restrict.restricted
# def close(bot,updates):
#     chat_id = updates.message.chat_id
#     service.closeConnection()
#     bot.send_message(chat_id=chat_id, text="数据库关闭成功奶爸再次为你服务~")

# close_handler = CommandHandler('close', close)
# dispatcher.add_handler(close_handler)


# #关闭所有自定义按钮
# @restrict.restricted
# def delB(bot,updates):
#     chat_id = updates.message.chat_id
#     reply_markup = telegram.ReplyKeyboardRemove()
#     bot.send_message(chat_id=chat_id, text="清除按钮成功奶爸再次为你服务~\n /menu -点饭", reply_markup=reply_markup)

# delB_handler = CommandHandler('delB', delB)
# dispatcher.add_handler(delB_handler)



from handler.unknow import unknown_handler
from handler.exception import error_callback
from handler import *
import handler


def autoLoadHandlers(dispatcher):
    if handler == None or handler.__all__ == None or len(handler.__all__) == 0:
        logging.info('handles is null')
    else:
        for handle in handler.__all__:
            dispatcher.add_handler(eval(handle+'.handler'))
        dispatcher.add_handler(unknown_handler)#未知命令反馈
        dispatcher.add_error_handler(error_callback)#错误命令反馈

def dispatcher_start(updater):
    dispatcher = updater.dispatcher
    autoLoadHandlers(dispatcher)
    updater.start_polling()

def main():
    from corn_data import bot
    updater =  Updater(token=bot.token)
    try : 
        dispatcher_start(updater)
    except :
        logging.info("Unexpected error:get somethingWrong")
        dispatcher_start(updater)

if __name__ == '__main__':
    main()
