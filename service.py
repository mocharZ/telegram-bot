import pymysql  
import pymysql.cursors  
import logging
import logging.config
from telegram import Message
import dao
import time
import datetime


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
        sql_1 = "insert into telegram_order_list(order_username,order_no,tel_id,order_info,createTime,updateTime,state,payments) value ('%s','%s',%d,'%s','%s','%s',%d,%d)"
        #生成订单数据
        order_username = message.from_user.first_name
        order_no = str(int(time.time()*1000))+message.from_user.first_name[0]+message.from_user.first_name[1]
        tel_id = message.from_user.id
        order_info = handleOrderInfo(message.text)
        state = 0
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        payments = 0
        data_1 = (order_username,order_no,tel_id,order_info,dt,dt,state,payments)
        # print(order_username+' '+order_no+' '+str(tel_id)+' '+' '.join(order_info)+''+str(dt))
        dao.insert(sql_1,data_1)
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
        sql_1 = 'select order_no,order_info,createTime,state,payments from telegram_order_list where tel_id = %d'
        data_1 = (message.from_user.id)
        rows = dao.select(sql_1,data_1)
        print("数量： "+str(rows['count'])) 
        # argsv = [] 
        if rows['count'] > 0:
            strs = ''
            for row in rows['rows']:  
                print("order_no:",str(row[0]),'order_info',str(row[1]),'createTime',str(row[2]),'state',str(row[3]),'payments',str(row[4]))  
                # args = []
                # args.append(str(row[0]))
                # args.append(str(row[1]))
                # args.append(str(row[2]))
                # args.append(str(row[3]))
                # args.append(str(row[4]))
                if row[3]==0:
                    state = '执行中'
                elif row[3]==1:
                    state = '执行完毕'
                elif row[3]==2:
                    state = '废弃'
                strs = strs+str(row[0])+str(row[1])+' '+str(row[2])+' '+state+' '+str(row[4])+'p'+'\n'
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
def closeConnection():
    dao.close

