import pymysql  
import  pymysql.cursors  
import logging
import logging.config
from telegram import Message
from corn_data import db_config
# 连接数据库  
connection = db_config.connection

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
    print(' 成功删除', cursor.rowcount, '条数据') 
    connection.commit()

def doTransaction(sqlAndData):
    for sql , data in sqlAndData.items():
        cursor.execute(sql%data)
    print('事物成功') 
    connection.commit()

# 关闭连接  
def close():
    print('开始关闭数据库连接') 
    cursor.close()  
    connection.close() 
    print('关闭数据库连接成功')