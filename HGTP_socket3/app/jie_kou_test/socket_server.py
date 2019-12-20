import socket   #socket模块
import subprocess   #执行系统命令模块
import os
import threading
import traceback
import sqlite3
import socket
import time
import os
import unittest
import jenkins
import HTMLTestRunner
import smtplib
import json
import stat
from email.mime.text import MIMEText
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
from app.pi_run import all_run
class socket_run(object):
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
        myname = socket.getfqdn(socket.gethostname())
        k = (socket.gethostbyname(myname), 8065)
        s.bind(k)
        s.listen(2)
        while True:
            conn, addr = s.accept()  # 接受TCP连接，并返回新的套接字与IP地址
            ub = MyThread(conn, addr)
            ub.start()
#获取目录后遍历目录，返回json文件信息
class bianli(object):
    def __init__(self,path,select_huanjing):
        self.path=str(path)
        self.select_huanjing=select_huanjing
        yewu_name = {}
        # 需要跳转的环境
        huanjing = [os.path.join(self.path, i) for i in
                    os.listdir(self.path)
                    if i.strip() != '' and 'git' not in i ]
        if self.select_huanjing.strip()!='':
            for i in huanjing:
                if self.select_huanjing == os.path.basename(i):
                    select_jing = i
        else:
                select_jing = huanjing[0]
        for filename in os.listdir(select_jing):
            if filename.strip() != '' and '.git' not in filename and '__init__' not in filename:
                # 每个业务名是key，下面的接口名文件夹名是value
                value=[]
                try:
                    for z in os.listdir(os.path.join(select_jing, filename)):
                        if os.path.isdir(os.path.join(select_jing, filename,z)):
                            value.append(z)
                except Exception as err:
                    print(traceback.format_exc())
                    print(err)

                yewu_name[filename] = [i for i in  os.listdir(os.path.join(select_jing, filename)) if os.path.isdir(os.path.join(select_jing, filename,i))]
        huanjing_list = [i for i in os.listdir(self.path) if
                         i.strip() != '' and 'git' not in i ]
        huanjing_list.remove(os.path.basename(select_jing))
        all_data={}
        all_data['yewu_name']=yewu_name
        all_data['select_huanjing']=os.path.basename(select_jing)
        all_data['huanjing']=huanjing_list
        self.all_data=json.dumps(all_data)
#批量运行类
class pilaing_run(object):
    def __init__(self):
        pass
class MyThread(threading.Thread):
    def __init__(self, conn,addr):
        self.conn=conn
        self.addr=addr
        threading.Thread.__init__(self)
    def run(self):
        self.data = self.conn.recv(1024)
        #返回目录接口信息
        if self.data=='jiekou_mulu':
            self.conn.send('please')
            self.data = self.conn.recv(1024)
            self.data=bianli(self.data,'').all_data
            self.conn.send(self.data)
        #接收批量运行请求
        elif self.data=='piliang_run':
            self.conn.send('ready to run')
            self.data = json.loads(self.conn.recv(1024))
            all_run.run(self.data['all_jiekou'], self.data['run_time'],r'C:\work\lenove_jie_kou')
            '''
            self.return_data={'result':self.result,'time':self.time}
            url = 'http://127.0.0.1:5021/piliang_run_result'
            request = urllib2.Request(url)
            request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
            response = urllib2.urlopen(request, urllib.urlencode(self.return_data))
            '''
        self.conn.close()
if __name__=='__main__':
    #bianli(u'C:\所写系统\无时间限制正常程序\lr_test',u'第二套环境')
    socket_run()
