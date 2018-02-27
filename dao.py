import pymysql  
import  pymysql.cursors  
import logging
import logging.config
from telegram import Message
# 连接数据库  
connection = pymysql.connect(host='localhost',  
                             user='root',  
                             password='asdvhn82',  
                             db='mysql',  
                             port=3306,  
                             charset='utf8')#注意是utf8不是utf-8  

# 获取游标  
cursor = connection.cursor() 


def select(sql,data):
    cout_1 = cursor.execute(sql % data)  

    return {'count':cout_1,'rows':cursor.fetchall()}
 
def insert(sql,data):
    cursor.execute(sql % data)  
    print('成功插入', cursor.rowcount, '条数据') 
    connection.commit()

def update(sql,data):
    cursor.execute(sql%data)  
    print(' 成功修改', cursor.rowcount, '条数据') 
    connection.commit()

def delete(sql,data):
    cursor.execute(sql%data)  
    print(' 成功修改', cursor.rowcount, '条数据') 
    connection.commit()


def updateTe(name,money):
    sql = "update telegram_user set balance =%.2f where userName = '%s')"  
    data = (money,name)
    cursor.execute(sql%data)  
    print(name+' 成功修改', cursor.rowcount, '条数据') 
    connection.commit()

def deleteTe(name):
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