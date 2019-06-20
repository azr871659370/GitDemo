#coding = utf8

from socket import *
import sys
import getpass



def main():#网络连接由用户手动输入
    if len(sys.argv)<3:#判断用户输入的ip地址及端口号是否小于3如果小于则执行如下操作
        print('argv is error')#打印一句提示，表示错误信息
        return#返回函数调用，结束函数

    HOST = sys.argv[1]#将用户输入的信息第一位用变量HOST绑定起来
    PORT = int(sys.argv[2])#将用户输入的信息第二位整数类型用变量PORT绑定起来
    s = socket()#创建套接字
    try:#添加异常捕获机制
        s.connect((HOST,PORT))#以输入的ip地址及端口号向服务器发起连接请求
    except Exception as e:#异常保护机制及异常重命名
        print(e)#打印异常报告
        return#返回函数调用

    while True:#创建一个死循环显示第一显示界面
        print('''
        ===========Welcome==========
        ->1.注册    2.登录     3.退出
        ============================
        ''')#以上为第一显示界面的显示内容
        try:#异常捕获机制
            cmd = int(input('输入选项:'))#用户自主选择要操作的内容
        except Exception as e:#异常保护机制及异常重命名
            print('命令错误')#打印异常报告
            continue

        if cmd not in [1,2,3]:#判断用户的输入是否超出范围
            print('没有该选项')#如果超出选择范围则打印此段代码
            continue
        elif cmd ==1:#判断用户的输入选择如果为1则执行下列函数
            do_register(s)#调用注册函数以便完成注册功能的实现

        elif cmd ==2:#判断用户的输入选择如果为2则执行下列函数
            do_login(s)#调用登录函数以便完成注册功能的实现

        elif cmd ==3:#判断用户的输入选择我如果为3则执行下列代码
            s.send(b'E')#向客户端发送结束的标识符
            sys.exit('谢谢使用')#结束程序前的温馨提示


#注册函数
def do_register(s):#注册函数，参数为套接字地址
    while True:#创建一个死循环,用来循环用户的输入
        name = input('User')#用来接收用户输入的账户名，用变量name来绑定
        passwd = getpass.getpass()#调用模块使用户的密码输入变得隐藏起来
        passwd1 = getpass.getpass('Again')#调用模块使用户的密码输入第二次,以便验证准确性

        if(' ' in name) or (' ' in passwd):#判断用户输入的账号密码当中是否有空格的存在,若有空格则执行如下代码的操作
            print('用户名或密码不能有空格')#打印一个警告提示信息
            continue

        if passwd != passwd1:#判断用户输入的第一次密码是否跟第二次输入的密码相同，如果不相同则执行如下代码
            print('两次密码不一致')#打印警告提示符,
            continue

        msg = 'R %s %s'%(name,passwd)#将用户输入的用户名及密码分位邦洞，并加首部标识符R，用msg变量来绑定
        s.send(msg.encode())#将准备就绪的msg变量通过套接字发送给服务器
        
        data = s.recv(128).decode()#接收客户端回发过来的消息以1024大小接收
        if data == 'OK':#判断服务器返回来的内容，如果为ok则执行以下操作
            print('注册成功')#打印操作成功的提示信息
        elif data == 'EXISTS':#如果服务器发来的消息为操作失败的标识符则执行如下代码段
            print('该用户已存在')#打印操作失败的标识符
        else:
            print('注册失败')#同上述代码作用同效,错误信息的提示语句
        return


def do_login(s):#登录函数，参数为套接字的地址
    name = input('User')#输入登录的账户
    passwd = getpass.getpass()#隐藏输入密码模块方法
    msg = "L %s %s"%(name,passwd)#给账户跟密码的首部添加L用以服务器的识别
    s.send(msg.encode())#将准备就绪的账户密码变量名发送给s服务器
    data = s.recv(128).decode()#接收客户端发来的消息，用变量data来绑定
    if data == 'OK':#判断客户端发来的消息内容标识符，如果为ok则如下代码段
        print('登录成功')#打印操作成功的提示语句
        login(s,name)#调用第二界面函数，用以显示第二界面的显示
    elif data =='EXISTS':#判断客户端发来的消息如果为错误标识符则执行如下操作
        print('用户名不存在')#打印错误信息的提示语句
    else:
        print('登录失败')#同上述代码同效，错误信息提示语句


def login(s,name):#第二界面的函数调用，参数为套接字地址及用户名
    while True:#创建一个死循环用来循环显示第二显示界面
        print('''
        =========查询界面=========
        1.查词   2.历史记录  3.注销
        ========================
        ''')#以上为第二界面的显示内容

        try:#异常捕获机制
            cmd = int(input('输入选项:'))#用来接收用户的选择输入，以整数为基准
        except Exception as e:#用来判断是否输入错误，如果错误则执行如下操作
            print('命令错误')#打印一个错误信息提示语句
            continue
        if cmd not in [1,2,3]:#判断用户的选择是否超出范围，如果超出范围则执行如下代码的执行
            print('没有该选项')#打印一句超出范围后的错误信息提示语句
            continue
        elif cmd==1:#判断用户的选择是否为1如果为1则执行如下代码
            do_query(s,name)#调用查询单词的函数，用来实现单词的查询功能
        elif cmd==2:#用来判断用户输入的选择是否2如果为2则执行如下代码
            do_hist(s,name)#历史记录的函数调用，用来实现用户的查询历史记录的功能实现
        elif cmd==3:#用来判断用户的选择是否为3如果为3则执行如下函数
            return#返回函数调用，结束函数运行


def do_query(s,name):#单词查询函数，参数为套接字地址及用户名
    while True:#创建一个死循环用来循环接收用户输入的单词名字
        word = input('单词:')#用来循环接收用户输入的单词名字
        if word == '##':#判断用户的驶输入是否为##如果是，则执行如下代码的操作
            break#结束函数的运行，返回调用
        msg = 'Q %s %s'%(name,word)#将用户的用户名及密码分位存储，并加以首部标识符,用变量msg绑定
        s.send(msg.encode())#将准备就绪的msg函数通过套接字地址发送到服务器
        data = s.recv(1024).decode()#接收服务器回发过来的消息，以1024的大小来接收
        if data == 'FALL':#判断服务器回来过来的内容是否为错误标识符,如果是则执行如下代码操作
            print('没有找到该单词')#打印依据错误信息的提示信息

        else:#上述代码的相反结果
            print(data)#打印操作成功的内容即查询到的单词及单词解释


def do_hist(s,name):#历史记录函数，参数为套接字地址及用户名
    msg = 'H %s'%name#将用户名分位存储，并加以首部标识符,用变量msg来绑定
    s.send(msg.encode())#将准备就绪的msg变量通过套接字发送到服务器
    data = s.recv(1024).decode()#接收服务器回发的消息内容，以1024的大小来接收
    if data == 'OK':#判断服务器返回来的消息内容标识符是否为ok如果是则执行如下代码
        while True:#创建一个死循环用来循环接收服务器的回发消息
            data = s.recv(1024).decode()#接收服务器的回发消息
            if data == '##':#判断服务器的回发消息内容是否为##如果是则则执行如下代码
                break#返回函数调用，结束函数的运行
            else:#上述代码的反向执行
                print(data)#打印接收到的服务器回发来的消息内容
    else:
        print('没有历史记录')#打印错误消息提醒




if __name__ == '__main__':#调用main函数以执行整个程序
    main()#调用main函数（整个程序的导火索!!）


















