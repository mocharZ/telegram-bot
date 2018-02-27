import pymysql  
import  pymysql.cursors  
import logging
import logging.config
# 连接数据库  
connection = pymysql.connect(host='localhost',  
                             user='root',  
                             password='asdvhn82',  
                             db='mysql',  
                             port=3306,  
                             charset='utf8')#注意是utf8不是utf-8  

# 获取游标  
cursor = connection.cursor() 

# 查询余额数据
def getBalanceByUserName(name):
    sql_1 = "select * from telegram_user where userName = '%s'"
    data = (name)
    cout_1=cursor.execute(sql_1 % data)  
    print("数量： "+str(cout_1))  
    args=[]
    for row in cursor.fetchall():  
        print("id:",str(row[0]),'userName',str(row[1]),'balance',str(row[2]))  
        args.append(str(row[1]))
        args.append('余额：'+str(row[2]))
    # sql_2 = 'insert into telegram_user(userName,balance) value("joey",2000)'  
    # cout_2=cursor.execute(sql_2)  
    # print("数量： "+str(cout_2))  
    connection.commit()
    return args

# 查询余额数据
def getBalance(**params):
    print("开始查询余额")
    sql_1 = "select * from telegram_user where tel_id = %.2f"

    for key , value in params.items():
        if key == 'from':
            for inKey , inValue in params[key].items():
                    if inKey == 'id':
                            print(params[key][inKey])

    data = (params[key][inKey])
    cout_1=cursor.execute(sql_1 % data)  
    print("数量： "+str(cout_1))  
    args=[]
    for row in cursor.fetchall():  
        print("id:",str(row[0]),'userName',str(row[1]),'balance',str(row[2]))  
        args.append(str(row[1]))
        args.append('余额：'+str(row[2]))
    # sql_2 = 'insert into telegram_user(userName,balance) value("joey",2000)'  
    # cout_2=cursor.execute(sql_2)  
    # print("数量： "+str(cout_2))  
    connection.commit()
    return args

def insert(name,money):
    sql = "insert into telegram_user(userName,balance) value('%s', %.2f)"  
    data = (name,money)
    cursor.execute(sql % data)  
    print(name+' 成功插入', cursor.rowcount, '条数据') 
    connection.commit()

def update(name,money):
    sql = "update telegram_user set balance =%.2f where userName = '%s')"  
    data = (money,name)
    cursor.execute(sql%data)  
    print(name+' 成功修改', cursor.rowcount, '条数据') 
    connection.commit()

def delete(name):
    sql= "delete from telegram_user where userName = '%s' "
    data = (name)
    cursor.execute(sql % data)
    print(name+' 成功删除', cursor.rowcount, '条数据') 
    connection.commit()

# 关闭连接  
def close():
    print('开始关闭数据库连接') 
    cursor.close()  
    connection.close() 
    print('关闭数据库连接成功')