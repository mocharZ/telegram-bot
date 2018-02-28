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
        sql_1 = "select * from telegram_user where tel_id = %.2f"
        data_1 = (message.from_user.id)
        rows=dao.select(sql_1 , data_1)  
        print("数量： "+str(rows['count']))  
        if rows['count'] == 0:
            sql_2 = "insert into telegram_user(firstName,tel_id,balance,createTime) value('%s',%.2f, %.2f,'%s')"
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data_2 = (message.from_user.first_name,message.from_user.id,0,dt)
            dao.insert(sql_2,data_2)
        elif rows['count'] == 1:
            #事物字典
            DsqlAndData = {}

            sql_3 = "insert into telegram_order_list(order_username,order_no,tel_id,order_info,createTime,updateTime,state,payments) value ('%s','%s',%d,'%s','%s','%s',%d,%d)"
            #生成订单数据
            order_username = message.from_user.first_name
            order_no = str(int(time.time()*1000))+message.from_user.first_name[0]+message.from_user.first_name[1]
            tel_id = message.from_user.id
            order_info = handleOrderInfo(message.text)
            if order_info.strip() == '':
                return ['WRONG_NO_PARAMS']
            state = 0
            dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            payments = calPay(message)
            if "SUCCESS" != payments['code']:
                return [payments['code']]
            data_3 = (order_username,order_no,tel_id,order_info,dt,dt,state,payments['value'])
            # print(order_username+' '+order_no+' '+str(tel_id)+' '+' '.join(order_info)+''+str(dt))
            #用户表扣费
            sql_4 = 'update telegram_user set balance = balance - %d where tel_id = %d'
            data_4 = (payments['value'],tel_id)
            DsqlAndData = {
                sql_3 : data_3,
                sql_4 : data_4
            }
            #事物结算
            dao.doTransaction(DsqlAndData)
            return [order_username,order_no,order_info,dt,state,payments['value']]
    except Exception as e :
        logging.error(e)
        dao.connection.rollback
    finally:
        closeConnection()
#取消订单
def cancelOrder(message):
    try:
        print('用户取消订单')
        #清除订单数据
        sql_1 = "delete from telegram_order_list where order_no = '%s'"

        order_info = handleOrderInfo(message.text)
        if not order_info :
            return dataList.LIST_OF_STANTS["WRONG_PARAM"]
        print(order_info)
        data_1 = (order_info.strip())
        # print(order_username+' '+order_no+' '+str(tel_id)+' '+' '.join(order_info)+''+str(dt))
        #事物结算
        dao.delete(sql_1,data_1)
    except Exception as e :
        logging.error(e)
        dao.connection.rollback
        return 666
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
                    state = '未付钱'
                elif row[4]==1:
                    state = '已付钱'
                elif row[4]==2:
                    state = '废弃订单'
                strs = strs+str(row[0]+':\n'+row[1])+' ['+str(row[2])+'] '+str(row[3])+' '+state+' '+str(row[5])+'p'+'\n'
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
        tommorrow = today + datetime.timedelta(days=1)
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
                strs = strs+str(row[0]+':\n '+row[1])+'['+str(row[2])+'] '+str(row[3])+' '+state+' '+str(row[5])+'p'+'\n'
                # argsv.append(args)
            return strs
    
    except Exception as e:
        logging.error(e)
        dao.connection.rollback
    finally:
        closeConnection()

#存钱给用户
def deposit(message):
    try:
        print('开始给用户存钱')

        #金额字段增钱
        sql_1 = "update telegram_user set balance = balance + %d , updateTime = '%s' where id = %d "
        
        order_info = handleDepositInfo(message.text)
        if not order_info:
            raise RuntimeError('user parameter error')
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_1=(int(order_info[1]),dt,int(order_info[0]))
        dao.update(sql_1,data_1)

    except Exception as e :
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

#处理存钱参数数据
def handleDepositInfo(info):
    info = info.split(" ")
    del info[0]
    if len(info) == 1 :
        strs = info[0].split('#')
        if len(strs) == 2:
            return strs

#计算每次订单所需金钱
def calPay(message):
    info = message.text.split(' ')
    del info[0]
    print(str(info))
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

