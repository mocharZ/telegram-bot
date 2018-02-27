import pymysql  
import pymysql.cursors  
import logging
import logging.config
from telegram import Message
import dao
import time
import datetime
import dataList

# 查询余额数据
def getBalance(message):
    print("开始查询余额")
    sql_1 = "select * from telegram_user where tel_id = %.2f"
    
    # for key , value in params.items():
    #     if key == 'from':
    #         for inKey , inValue in params[key].items():
    #                 if inKey == 'id':
    #                         print(params[key][inKey])
    args=[]
    data = (message.from_user.id)
    rows=dao.select(sql_1 , data)  
    print("数量： "+str(rows['count']))  
    if rows['count'] == 0:
        sql_2 = "insert into telegram_user(firstName,tel_id,balance) value('%s',%.2f, %.2f)"
        data_2 = (message.from_user.first_name,message.from_user.id,0)
        dao.insert(sql_2,data_2)
        return getBalance(message)
    elif rows['count'] == 1:
        
        for row in rows['rows']:  
            print("id:",str(row[0]),'userName',str(row[1]),'balance',str(row[3]))  
            args.append("大神："+str(row[2]))
            args.append('\n余额：'+str(row[3]))
            args.append('\n编号：'+str(row[0]))
        
        # sql_2 = 'insert into telegram_user(userName,balance) value("joey",2000)'  
        # cout_2=cursor.execute(sql_2)  
        # print("数量： "+str(cout_2))  
    closeConnection()
    return args

#初始化用户订单
def userOrder(message):
    try:
        print('开始产生用户订单')
        #事物字典
        DsqlAndData = {}

        sql_1 = "insert into telegram_order_list(order_username,order_no,tel_id,order_info,createTime,updateTime,state,payments) value ('%s','%s',%d,'%s','%s','%s',%d,%d)"
        #生成订单数据
        order_username = message.from_user.first_name
        order_no = str(int(time.time()*1000))+message.from_user.first_name[0]+message.from_user.first_name[1]
        tel_id = message.from_user.id
        order_info = handleOrderInfo(message.text)
        state = 0
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payments = calPay(message.text)
        if "SUCCESS" != payments['code']:
            return [payments['code']]
        data_1 = (order_username,order_no,tel_id,order_info,dt,dt,state,payments['value'])
        # print(order_username+' '+order_no+' '+str(tel_id)+' '+' '.join(order_info)+''+str(dt))
        #用户表扣费
        sql_2 = 'update telegram_user set balance = balance - %d where tel_id = %d'
        data_2 = (payments['value'],tel_id)
        DsqlAndData = {
            sql_1 : data_1,
            sql_2 : data_2
        }
        #事物结算
        dao.doTransaction(DsqlAndData)
        return [order_username,order_no,order_info,dt,state]
    except Exception as e :
        logging.error(e)
        dao.connection.rollback
    finally:
        closeConnection()
    
#本人订单集合
def getOrderListSelf(message):
    try:
        print('获取用户自己的订单集合')
        sql_1 = 'select order_username,order_no,order_info,createTime,state,payments from telegram_order_list where tel_id = %d'
        data_1 = (message.from_user.id)
        rows = dao.select(sql_1,data_1)
        print("数量： "+str(rows['count'])) 
        # argsv = [] 
        if rows['count'] > 0:
            strs = ''
            for row in rows['rows']:  
                print('order_username:',str(row[0])," order_no:",str(row[1]),'order_info',str(row[2]),'createTime',str(row[3]),'state',str(row[4]),'payments',str(row[5]))  
                # args = []
                # args.append(str(row[0]))
                # args.append(str(row[1]))
                # args.append(str(row[2]))
                # args.append(str(row[3]))
                # args.append(str(row[4]))
                if row[4]==0:
                    state = '执行中'
                elif row[4]==1:
                    state = '执行完毕'
                elif row[4]==2:
                    state = '废弃'
                strs = strs+str(row[0]+':\n '+row[1])+str(row[2])+' '+str(row[3])+' '+state+' '+str(row[5])+'p'+'\n'
                # argsv.append(args)
            return strs
    
    except Exception as e:
        logging.error(e)
        dao.connection.rollback
    finally:
        closeConnection()

#获取当天订单数据
def getOrderListIntraday(message):
    try:
        print('获取当天的订单数据')
        sql_1 ="select order_username,order_no,order_info,createTime,state,payments from telegram_order_list where createTime > '%s' and createTime < '%s'"
        today = datetime.datetime.today()
        today = datetime.datetime(today.year,today.month,today.day,0,0,0)
        tommorrow = datetime.datetime(today.year,today.month,today.day+1,0,0,0)
        data_1 = (today,tommorrow)
        rows = dao.select(sql_1,data_1)
        print("数量： "+str(rows['count'])) 
        # argsv = [] 
        if rows['count'] > 0:
            strs = ''
            for row in rows['rows']:  
                print('order_username:',str(row[0])," order_no:",str(row[1]),'order_info',str(row[2]),'createTime',str(row[3]),'state',str(row[4]),'payments',str(row[5]))  
                # args = []
                # args.append(str(row[0]))
                # args.append(str(row[1]))
                # args.append(str(row[2]))
                # args.append(str(row[3]))
                # args.append(str(row[4]))
                if row[4]==0:
                    state = '执行中'
                elif row[4]==1:
                    state = '执行完毕'
                elif row[4]==2:
                    state = '废弃'
                strs = strs+str(row[0]+':\n '+row[1])+str(row[2])+' '+str(row[3])+' '+state+' '+str(row[5])+'p'+'\n'
                # argsv.append(args)
            return strs
    
    except Exception as e:
        logging.error(e)
        dao.connection.rollback
    finally:
        closeConnection()

#处理订单信息
def handleOrderInfo(info):
    info = info.split(" ")
    del info[0]
    strs=''
    for estr in info:
        strs = strs +" "+estr 
    return strs

#计算每次订单所需金钱
def calPay(message):
    info = message.text.split(' ')
    del info[0]
    pay = 0
    for compare in info:
        if compare not in dataList.LIST_OF_MNEU_ORDER_SINGLE.keys():
                return {'code': 'WRONG_NOT_ALLINCLUE' , 'value': 0}
        for key ,value in dataList.LIST_OF_MNEU_ORDER_SINGLE.items():
            if compare == key:
                pay += value
    return {'code': 'SUCCESS' ,'value': pay}


def closeConnection():
    dao.close

