'''
name:Azr
modules:pymysql
This is a dict project for AID
'''

from socket import *
import pymysql
import os
import sys
from threading import Thread
import time



#定义需要的全局变量
DICT_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8000
ADDR = (HOST,PORT)

#处理僵尸进程
def zombie():
    os.wait()





#网络搭建
def main():
    #创建数据库连接
    db = pymysql.connect('localhost','root','123456','dict')

    s = socket(AF_INET,SOCK_STREAM)#创建套接字
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)#设置套接字的端口重用
    s.bind(ADDR)#绑定套接字的地址
    s.listen(5)#设置套接字的监听队列

    while True:#创建一个死循环用来循环接收客户端的连接请求
        try:#创建一个异常捕获机制
            c,addr = s.accept()#等待客户端发起链接、接收客户端的链接请求
            print('Connect from',addr)#处于待连接状态时的提示语句
        
        except KeyboardInterrupt:#异常捕获机制
           s.close()#如果上述异常成立则关闭s套接字
           sys.exit('服务器退出')#继上述代码执行完毕之后执行服务器的正常退出操作(不会以报错的状态退出!!)
        except Exception as e:#异常捕获机制
            print(e)#如上述异常成立则打印上述异常的异常内容
            continue#跳过该异常继续正常执行代码

        #创建子进程
        pid = os.fork()
        if pid == 0:#调用fork方法创建子进程的返回值若是为0则表示成功创建子进程
            s.close()#垃圾回收机制,如果子进程成功创建则关闭无用的套接字以节省资源
            do_child(c,db)#子进程调用及复制父进程的函数用以调用跟父进程同步执行
        else:#若子进程返回值非0时则为父进程代码段！
            c.close()#垃圾回收机制,关闭无用的套接字，用以节省资源的消耗
            t = Thread(target = zombie())#调用函数，用以防止僵尸进程的产生
            t.setDaemon(True)#设置上述代码的必要属性
            t.start()#启动调用防止僵尸进程的函数
            continue#python3函数

#父子进程同时调用的函数，负责整个程序的功能实现及代码执行
def do_child(c,db):
    while True:#创建死循环
        data = c.recv(1024).decode()#接收客户端发起的请求
        print(c.getpeername(),':',data)#打印发起请求者的IP地址端口号及用户名密码
        if (not data) or data[0]== 'E':#识别用户的操作、如首部识别符为E则表示退出!此时程序结束！
            c.close()#如果上述代码条件成立则关闭套接字、程序运行结束
            sys.exit('谢谢使用')#结束程序时的温馨提示
        elif data[0] == 'R':#识别首部识别符,如果为R则表示注册
            do_register(c,db,data)#若上述代码条件成立则调用注册函数开始执行
        elif data[0] =='L':#识别首部标识符，如果为L则表示登录
            do_login(c,db,data)#若上述代码条件成立则调用登录函数开始执行
        elif data[0] =='Q':#识别首部标识符，如果为Q则表示单词的查询
            do_query(c,db,data)#若上述代码条件成立则调用查询函数开始执行
        elif data[0] =='H':#识别首部标识符,如果为H则调用历史记录查询函数
            do_hist(c,db,data)#如果上述代码条件成立，则调用历史记录查询函数开始执行


#注册函数
def do_register(c,db,data):#注册函数->参数为套接字地址，数据库的链接，客户端发来的账户密码消息
    l = data.split(' ')#切割操作:将用户发来的消息以空格进行切割
    name = l[1]#继切割操作之后将切割内容的第一位赋值给name
    passwd = l[2]#继切割操作之后将切割内容给的第二位赋值给passwd
    cursor = db.cursor()#创建数据库游标对象
    sql = "select * from user where name='%s'"%name#进行数据库的指定查询操作,以sql变量用以绑定
    cursor.execute(sql)#将上述的sql语句进行执行
    r = cursor.fetchone()#将执行结果赋值给r变量用以绑定

    if r != None:#执行r变量的判断操作，若为None(空值)则执行下列操作
        c.send(b'EXISTS')#继上述代码执行结果之后的执行，向客户端发送一个操作结果执行完毕后的信息
        return

    
    sql = "insert into user (name,passwd) value('%s','%s')"%(name,passwd)#插入指定数据库的操作，用以sql变量进行绑定
    try:#异常捕获机制
        cursor.execute(sql)#执行上述sql语句的执行
        db.commit()#提交事件执行后的结果
        c.send(b'OK')#向客户端发送一个事件执行后的结果
    except:#异常捕获机制
        db.rollback()#若上述代码成立则执行此出代码|功能:事务回滚
        c.send(b'FALL')#向客户端发送事件执行后的结果

#登录函数
def do_login(c,db,data):#登录函数参数为客户端套接字地址及数据库链接，客户端的账户密码
    l=data.split(' ')#收到客户端发来的账户及密码、以空格分割
    name = l[1]#将切割的第一位赋值给name
    passwd = l[2]#将切割的第二位赋值给passwd
    cursor = db.cursor()#创建数据库的游标对象

    #执行数据库的指定查询进行判断
    sql = "select * from user where name='%s' and passwd='%s'"%(name,passwd)
    
    #查找用户
    cursor.execute(sql)#执行上述sql语句的执行操作
    r = cursor.fetchone()#将上述操作的结果赋值给r变量进行绑定
    if r == None:#判断r变量是否为空如果为空返回给客户端一个信息标识符
        c.send(b'EXISTS')#向客户端发送失败标识符
    else:
        c.send(b'OK')#否则向客户端发送成功标识符


def do_query(c,db,data):#查询单词的函数
    l = data.split(' ')#将客户端发来的消息以空格分割，赋值给变量l
    name = l[1]#将切割后的第一位赋值给name
    word = l[2]#将切割后的第二位赋值给word
    cursor = db.cursor()#创建数据库的游标对象

    def insert_history():#内嵌函数省去传参（查询记录的存储机制）
        tm = time.ctime()#将转换的时间格式赋值给tm
        sql = "insert into hist (name,word,time) values ('%s','%s','%s')"%(name,word,tm)
        #编写数据库的指定插入操作赋值给sql
        
        try:#异常捕获机制
            cursor.execute(sql)#执行sql语句
            db.commit()#将sql语句的执行结果提交
        except:
            db.rollback()#失败后的事务回滚
    
    #使用单词本查找
    try:#异常捕获机制
        f = open(DICT_TEXT)#打开词典文本，参数为词典的地址全局变量
    except:#如果出现异常则执行如下函数
        c.send(b'FALL')#如果上述操作失败将向客户端发送一个打开文件失败的标识符
        return
    for line in f:#遍历打开的词典文件,每一行记录以line绑定
        tmp = line.split(' ')[0]#将将遍历到的词典内容以空格切割[0]为标识单词名，用于tmp变量进行绑定
        if tmp > word:#判断如果tmp小于客户端输入的单词名则执行如下操作
            c.send(b'FALL')#向客户端发送FALL标识符
            f.close()#关闭词典文件
            return
        elif tmp == word:#如果tmp等于客户端输的单词名称则执行如下操作
            c.send(line.encode())#将匹配到单词及单词注释发送回客户端
            insert_history()#调用历史记录函数用以记录
            f.close()#关闭词典文件
            return
    c.send(b'FALL')#向客户端发送FALL标识符
    f.close()#for循环结束后关闭词典文件




def do_hist(c,db,data):#查询历史记录的函数
    l = data.split(' ')#将客户端发来的消息用空格切割，用变量l绑定
    name = l[1]#将切割后的第一位赋值于name变量绑定
    cursor = db.cursor()#创建数据库游标对象
    sql = "select * from hist where name='%s'"%name#创建数据库的指定查询操作，用以sql变量绑定
    cursor.execute(sql)#将上述的sql语句执行
    r = cursor.fetchall()#将上述的sql语句执行后的结果用r进行绑定
    if not r:#判断r是否为空，如果为空则执行如下代码
        c.send(b'FALL')#向客户端发送FALL的标识符
        return
    else:#否则执行如下代码
        c.send(b'OK')#向客户端发送ok标识符
        time.sleep(0.1)#设置程序睡眠机制，每隔0.1秒执行一次，以防止tcp的粘包特性
    for i in r:#循环遍历r
        msg = '%s %s %s'%(i[1],i[2],i[3])#将遍历出来的结果分位绑定，用变量msg绑定
        c.send(msg.encode())#将准备就绪的变量发送给客户端
        time.sleep(0.1)#每隔0.1秒发送一次，防止产生粘包
    c.send(b'##')#向客户端发送结束标识符





if __name__ == '__main__':
    main()#调用main函数开始执行代码(导火索！！)

    