import pymysql  
import  pymysql.cursors  

connection = pymysql.connect(host='localhost',  
                             user='root',  
                             password='asdvhn82',  
                             db='mysql',  
                             port=3306,  
                             charset='utf8')#注意是utf8不是utf-8  
try:  
    with connection.cursor() as cursor:  
        sql_1 = "select * from telegram_user where userName = 'joey'"
        cout_1=cursor.execute(sql_1)  
        print("数量： "+str(cout_1))  
        for row in cursor.fetchall():  
            print("id:",str(row[0]),'userName',str(row[1]),'balance',str(row[2]))  
          
        # sql_2 = 'insert into telegram_user(userName,balance) value("joey",2000)'  
        # cout_2=cursor.execute(sql_2)  
        # print("数量： "+str(cout_2))  
        connection.commit()  
finally:  
    connection.close()  