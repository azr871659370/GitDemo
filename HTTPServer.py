#coding=utf-8
'''
aid httpsrver v3.0
'''

from socket import *
import sys 
from threading import Thread 
#导入配置文件
from settings import *
import re
import time 

#和WebFrame通信
def connect_frame(METHOD,PATH_INFO):
    s = socket()
    try:
        s.connect(frame_address) #连接框架服务器地址
    except Exception as e:
        print("Connect error",e)
        return
    s.send(METHOD.encode())
    time.sleep(0.1)
    s.send(PATH_INFO.encode())
    response = s.recv(4096).decode()
    if not response:
        response = '404'
    s.close()
    return response 
    
#封装httpserver类
class HTTPServer(object):
    def __init__(self,address):
        self.address = address 
        self.create_socket()
        self.bind(address)

    #创建套接字
    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(\
        SOL_SOCKET,SO_REUSEADDR,1)

    #绑定地址
    def bind(self,address):
        self.ip = address[0]
        self.port = address[1]
        self.sockfd.bind(address)
    
    #启动服务器
    def serve_forever(self):
        self.sockfd.listen(10)
        print("Listen the port %d..."%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            print("Connect from",addr)
            handle_client = Thread(target=self.handle,\
            args = (connfd,))
            handle_client.setDaemon(True)
            handle_client.start()
    
    #处理具体的客户端请求
    def handle(self,connfd):
        #接收浏览器发来的http请求
        request = connfd.recv(4096)
        if not request:
            connfd.close()
            return 
        request_lines = request.splitlines()
        #获取请求行
        request_line=request_lines[0].decode('utf-8')
        print(request_line)

        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
            print(env)
        except:
            response_headlers="HTTP/1.1 500 SERVER ERROR\r\n"
            response_headlers+='\r\n'
            response_body = "Server Error"
            response=response_headlers + response_body
            connfd.send(response.encode())
            connfd.close()
            return
        
        response = connect_frame(**env)

        if response == '404':
            response_headlers="HTTP/1.1 404 Not Found\r\n"
            response_headlers+='\r\n'
            response_body = "====Sorry,not found the page==="
        else:
            response_headlers="HTTP/1.1 200 OK\r\n"
            response_headlers+='\r\n'
            response_body = response

        response=response_headlers+response_body
        connfd.send(response.encode())
        connfd.close()

        



if __name__=="__main__":
    httpd = HTTPServer(ADDR)
    httpd.serve_forever() #启动ＨＴＴＰ服务

