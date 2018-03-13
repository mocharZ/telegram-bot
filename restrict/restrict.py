
from functools import wraps
import dataList
from service import service
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

import time
#接口请求频率限制
def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

# @RateLimited(1)  # 2 per second at most
# def PrintNumber(num):
#     print (num)

# if __name__ == "__main__":
#     print ("This should print 1,2,3... at about 2 per second.")
#     for i in range(1,100):
#         PrintNumber(i)