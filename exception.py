#错误回调
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

import telegram
import sys
import os
from telegram.ext import Updater
import logging
import logging.config
def error_callback(bot, updates, error):
    if updates:
        try:
            raise error
        except Unauthorized:
            updates.message.reply_text("如果出现这段话说明您还没激活机器人，请私聊此机器人，点击start按钮激活机器人服务~~")
        except BadRequest:
            updates.message.reply_text("奶爸受伤了，正在修复~")
        except TimedOut:
            updates.message.reply_text("等一会等一会~奶爸有点忙！")
        except NetworkError:
            updates.message.reply_text("奶爸不在工作岗位~")
        except ChatMigrated :
            updates.message.reply_text("聊天已迁移")
        except TelegramError:
            updates.message.reply_text("纸飞机崩啦！")
