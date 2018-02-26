#错误回调
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

import telegram
import sys
import os
from telegram.ext import Updater

def error_callback(bot, updates, error):
  
    chat_id = updates.message.chat_id
    print(chat_id)
    try:
        raise error
    except Unauthorized:
        updates.message.reply_text("神杖的权利已经不在你的手里！")
    except BadRequest:
        updates.message.reply_text("奶爸受伤了，正在修复~")
    except TimedOut:
        updates.message.reply_text("等一会等一会~奶爸有点忙！")
    except NetworkError:
        updates.message.reply_text("奶爸不在工作岗位~")
    except ChatMigrated as e:
        updates.message.reply_text("聊天已迁移")
        chat_id = e.new_chat_id
    except TelegramError:
        updates.message.reply_text("纸飞机崩啦！")
