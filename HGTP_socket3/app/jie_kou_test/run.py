import sys
import threading
import traceback
sys.path.append("../../")
from selenium import webdriver
from .sing_data.sing_data import *
import time
import chardet
import unittest
from .json_pi_pei.request_result_flask  import *
from .json_pi_pei.json_pi_pei  import *
from .json_pi_pei.request_run import *
import demjson
import urllib.request, urllib.parse, urllib.error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
#from  creat_dang import *
import unittest
import configparser
import xlrd
import json
import urllib.request, urllib.error, urllib.parse
import os
import logging
import socket
import copy
#from header import *
from .just_run.just_run import just_run
from .just_run.change_request_before import *
from .excel_data import *
#发送获取目录请求
class mulu(object):
    def __init__(self):
        # 启动socket server
        while True:

            time.sleep(2)
            url = 'http://127.0.0.1:5021/get_mulu'
            data=urllib.parse.urlencode({'statu':'调试'})
            #倒数第二个个为接口配置信息，最后一个为目录信息
            request = urllib.request.Request(url)
            request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
            response = urllib.request.urlopen(request, data)
            mulu=json.loads(response.read())['mulu']
            if len(mulu)>0 and mulu!='':
                if os.path.isdir(mulu):
                    run(mulu)
            else:
                pass

class run(object):
    def __init__(self,path):
        print(__name__)
        print('--------------------------------------------')
        #self.h = webdriver.Chrome()
        self.url=''
        #self.h.get('http://127.0.0.1:5021/ceshi')
        #self.send = confi(path,self.h)
        self.send = confi(path)
        self.data = xlrd.open_workbook(self.send.excel_path)
        self.table = self.data.sheets()[0]
        self.key=self.table.row_values(0)
        self.data0 = [self.table.row_values(i) for i in range(1,self.table.nrows)]
        #self.creat_json(open(self.dir[1]).read())
        num=0
        while True:
            #判断后台有没有设定的要运行的目录信息
            if num==0 or num==1:
                url = 'http://127.0.0.1:5021/get_mulu'
                data = urllib.parse.urlencode({'statu': '调试'})
                # 倒数第二个个为接口配置信息，最后一个为目录信息
                request = urllib.request.Request(url)
                request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
                response = urllib.request.urlopen(request, data)
                response = urllib.request.urlopen(request)
                mulu = json.loads(response.read())['mulu']
                num=0
            if  mulu!=path and mulu.strip()!='':
                    break
            num += 1
            #到此为止
            time.sleep(2)
            try:
               self.data = xlrd.open_workbook(self.send.excel_path)
            except IOError as e:
                print(traceback.format_exc())
                time.sleep(1)
                self.data = xlrd.open_workbook(self.send.excel_path)
            self.table = self.data.sheets()[0]
            self.data=[self.table.row_values(i) for i in range(1,self.table.nrows)]
            self.change={}
            if self.data0!=self.data:
                for k,i in enumerate(self.data):
                    #增加数据行
                    if len(self.data)!=len(self.data0):
                        self.data0 = self.data
                        #判断是否包含url字段
                        self.data  = dict(list(zip(self.key, self.data[-1])))
                        self.yongli_name=self.data['Comment']
                        #判断是否包含before_request,若包含则替换
                        if 'before_request' in list(self.data.keys()):
                            k=change_request_before()
                            self.data =k.use(self.data)
                        if 'url' in list(self.data.keys()) and self.data['url'].strip() != '':
                            self.send.config_path.get('config','public_url')
                            self.url = self.send.config_path.get('config','public_url').strip()+self.data.pop('url')
                        for k, i in enumerate(self.data.keys()):
                          if type(i) == float:
                            self.data[int(i)] = self.data.pop(i)
                    # 判断是否有包含#的字段若果则执行python代码
                        for i in self.data:
                            data_s = str(self.data[i])
                            if '##' in data_s:
                                self.s = excel_data_exe()
                                param = None
                                if ('(' in data_s) and data_s.endswith(')'):
                                    param = self.data.get(data_s[data_s.find('(')+1: data_s.find(')')])
                                self.data[i] = self.s.han_shu(self.data[i], param)
                    # 生成json字符串
                        self.data = json.loads(change(self.send.config_path, i).self.data)
                        self.data['result'] = change(self.send.config_path, self.data['result'], self.data).data
                        self.send.all_send(self.data,self.url)
                        break
                    #修改数据行值
                    elif self.data[k]!=self.data0[k]:
                        self.data0 = self.data
                        #获取改变了信息的行信息字典形式
                        self.data=dict(list(zip(self.key,self.data[k])))
                        if 'before_request' in list(self.data.keys()):
                            k=change_request_before()
                            self.data = k.use(self.data)
                        # 判断是否包含url字段
                        if 'url' in list(self.data.keys()) and str(self.data['url']).strip() != '':
                            self.url = self.data.pop('url')
                        #调用查询价格单接口
                        #self.query_data=self.query.just_reque(self.data)
                        #self.s=json.loads(self.query_data)['result']['data'][0]['barcode']
                        #self.data['apiSign']=self.s
                        #读取excel有可能将数字键变为flaot，因此要将float键变成str整形
                        for k, i in enumerate(self.data.keys()):
                            if type(i) == float:
                                self.data[int(i)] = self.data.pop(i)
                        # 判断是否有包含#的字段若果则执行python代码
                        for i in self.data:
                            data_s = str(self.data[i])
                            if '##' in data_s:
                                self.s = excel_data_exe()
                                param = None
                                if ('(' in data_s) and data_s.endswith(')'):
                                    param = self.data.get(data_s[data_s.find('(')+1: data_s.find(')')])
                                self.data[i] = self.s.han_shu(self.data[i], param)
                        #生成json字符串
                        self.send.all_send(self.data,self.url)
                        break

class confi(object):
    #第一个参数为文件夹路径，第二个参数为需要执行js的网页句柄
    def __init__(self,*path_h):
        #self.log=log()
        # 查找文件夹内各种配置文件路径，表格名和文件夹名相同，json.txt为json模板名，config为接口参数，第一个为url，第二个为头key，第三个为头value
        # 获取最后的目录名
        if len(path_h)==2:
            self.h=path_h[1]
            self.path=path_h[0]
        else:
            self.path = path_h[0]
        excel_name = os.path.basename(self.path)
        for dir, b, file in os.walk(self.path):
            # 返回表格路径
            for z in file:
                if excel_name in z:
                    self.excel_path = os.path.join(self.path, z)
                elif 'json' == z.split('.')[0]:
                    self.json_path = os.path.join(self.path, z)
                elif 'configparse' == z.split('.')[0] :
                    self.config_path = configparser.ConfigParser()
                    self.config_data = self.config_path.read(os.path.join(self.path, z))
                            # 读取公共配置文件
                    public_config_path = os.path.join(os.path.dirname(self.path), 'config.txt')
                    if os.path.isfile(public_config_path):
                         public_config = configparser.ConfigParser()
                         public_config.read(public_config_path)
                         private_config_path = os.path.join(self.path, 'configparse.txt')
                         private_config = configparser.ConfigParser()
                         private_config.read(private_config_path)
                         if os.path.isfile(os.path.join(os.path.dirname(self.path), 'db.txt')):
                             db_config_path = os.path.join(os.path.dirname(self.path), 'db.txt')
                             db_config = configparser.ConfigParser()
                             db_config.read(db_config_path)
                             for i in db_config.sections():
                                 self.config_path.add_section(i)
                                 for k in db_config.options(i):
                                     try:
                                         self.config_path.set(i, k, db_config.get(i, k))
                                     except Exception as err:
                                         print(traceback.format_exc())
                                         print(err)
                                 [self.config_path.set(i, k, db_config.get(i, k)) for k in db_config.options(i)]
                         if self.config_path.get('sign', 'sign_type').strip() == 'web':
                             if 'login' not in self.config_path.sections():
                                 self.config_path.add_section('login')
                             if 'login' in private_config.sections() and all(
                                             k in private_config.options('login') for k in
                                             public_config.options('login')):
                                 [public_config.set('login', z, private_config.get('login', z)) for z in
                                  private_config.options('login')]
                             [self.config_path.set('login', z, public_config.get('login', z)) for z in
                              public_config.options('login')]
                             headers_dict = web_token(self.config_path)
                             self.config_path.set('login', 'headers_dict', json.dumps(headers_dict))
                             self.config_path.add_section('login_value')
                             hash = hashlib.md5()
                             # 登录url，登录用户，登录没密码，去掉前后空格后的相加的字符串
                             code = self.config_path.get('login', 'url').strip() + self.config_path.get('login',
                                                                                                        'name').strip() + self.config_path.get(
                                 'login', 'password').strip()
                             hash.update(code)
                             self.config_path.set('login_value', str(hash.hexdigest()), json.dumps(headers_dict))
                             head_key = private_config.get('config', 'head_key').split('.')
                             head_value = private_config.get('config', 'head_value').split('.')[:len(head_key)]
                             header_older = json.dumps(dict(list(zip(head_key, head_value))))
                             self.config_path.set('login', 'headers_old', header_older)
                         if self.config_path.get('sign', 'sign_type').strip() == 'app':
                             header_dict = {
                                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                                 "Content-Type": "application/json"}
                             self.config_path.add_section('app_head')
                             self.config_path.set('app_head', 'app_head', json.dumps(header_dict))
                         elif self.config_path.get('sign', 'sign_type').strip() == 'Backstage_web':
                                 if 'login' not in self.config_path.sections():
                                     self.config_path.add_section('login')
                                 self.config_path.set('login', 'url', public_config.get('login', 'url'))
                                 self.config_path.set('login', 'name', public_config.get('login', 'name'))
                                 self.config_path.set('login', 'password', public_config.get('login', 'password'))
                                 if 'token'  not in  self.config_path.options('login'):
                                     token = houtai_jiami(self.config_path.get('login', 'name').strip(), self.config_path.get('login', 'password').strip(), self.config_path.get('login', 'url').strip())
                                     self.config_path.set('login', 'token', token)
                                 # save_data_normal(self.path, 'data', 'token', token)
                         elif self.config_path.get('sign', 'sign_type').strip() == 'hkci':
                             if 'login' not in self.config_path.sections():
                                 self.config_path.add_section('login')
                             self.config_path.set('login', 'login_url', public_config.get('login', 'login_url'))
                             self.config_path.set('login', 'server_host', public_config.get('login', 'server_host'))
                             self.config_path.set('login', 'phone', public_config.get('login', 'phone'))
                             self.config_path.set('login', 'ling_pai', public_config.get('login', 'ling_pai'))
                             self.config_path.set('login', 'dian_pu', public_config.get('login', 'dian_pu'))
                             if 'huasheng_headertoken' in self.config_path.options('login'):
                                 if self.config_path.get('login', 'phone') == self.all_bianliang[
                                     'phone'] and self.config_path.get('login', 'ling_pai') == self.all_bianliang[
                                     'ling_pai'] and self.config_path.get('login', 'dian_pu') == self.all_bianliang[
                                     'dian_pu']:
                                     self.config_path.set('login', 'huasheng_headertoken', self.config_path.get('login',''))
                             else:
                                 get_mendian_detail_url = self.config_path.get('login', 'server_host') + '/hk-peanut-car/api/place/getLoginPlaceInfo'
                                 db_detail = [db_config.get('db_mysql_login', 'host'),
                                              db_config.get('db_mysql_login', 'port'),
                                              db_config.get('db_mysql_login', 'user'),
                                              db_config.get('db_mysql_login', 'password'),
                                              db_config.get('db_mysql_login', 'db')]
                                 huasheng_headertoken = hs_login(self.config_path.get('login', 'server_host'),
                                                                 db_detail,
                                                                 self.config_path.get('login', 'login_url'),
                                                                 self.config_path.get('login', 'phone'),
                                                                 self.config_path.get('login', 'dian_pu'),
                                                                 self.config_path.get('login', 'ling_pai'))
                                 self.config_path.set('login', 'huasheng_headertoken',
                                                      huasheng_headertoken)
                             save_data_normal(self.path, 'data', 'huasheng_headertoken',
                                              self.config_path.get('login','huasheng_headertoken'))
                         if public_config.get('url', 'public_url').strip() != '':
                                    self.config_path.set('config','public_url', public_config.get('url', 'public_url').strip())
                                    url =  public_config.get('url', 'public_url').strip()+self.config_path.get('config', 'private_url')
                                    self.config_path.set('config', 'url', url)
                         if 'sign' in public_config.sections():
                             if 'api_key' in public_config.options('sign') and 'secretKey' in public_config.options('sign'):
                                 self.config_path.set('sign', 'api_key', public_config.get('sign', 'api_key'))
                                 self.config_path.set('sign', 'secretKey', public_config.get('sign', 'secretKey'))
        # 返回值第一个为表格路径，第二个为json路径，第三个为配置文件句柄
        self.jiekou_detail =[self.excel_path, self.json_path, self.config_path]
        self.port=request_run(json.loads(open(self.json_path).read()),self.config_path,'null')
    #f发送调用的实验用的接口，参数第一个为请求数据
    def  just_reque(self,data):
        v = json.loads(open(self.json_path).read())
        #判断json字符串在excel表格中是否有数值:
        if 'json' in list(self.data.keys())  and self.data['json']!='':
            self.req=self.data['json']
        else:
           self.req = self.creat_json(v,data)
        self.resulte = self.reque(self.req, self.config_path)
        try:
            json.dumps(json.loads(self.resulte))
        except Exception as err:
            print(traceback.format_exc())
            print(err)
            self.resulte={"result":str(self.resulte)}
            self.resulte=json.dumps(self.resulte)
        return self.resulte
    #发送数据到前段及后台方法,第二个为要发送的数据字典,第三个为数据中的rul
    def all_send(self,data,url):
        self.url=url
        self.comment=data['Comment']
        if 'json' in list(data.keys()) and data['json']!='' :
            self.req=data['json']
        elif open(self.json_path).read().strip()!='':
          v = json.loads(open(self.json_path).read())
          self.req=self.creat_json(v,data)
        elif open(self.json_path).read().strip()=='':
            self.req=''
        self.resulte=self.reque(self.req,self.config_path)
        self.request_url=self.resulte['request_url']
        self.resulte=self.resulte['result']
        #如果输入参数没有json则为excel 中使用url 字段发送get请求
        if str(self.req).strip()=='':
            self.req=json.dumps({"url": self.url})
        self.config_path.set('config','req',json.dumps(self.req))
        self.config_path.set('config', 'respons',json.dumps(self.resulte))
        if type(self.resulte)=='dict':
            self.assert_result = assert_run(self.config_path).walk_find(data['result'],json.dumps(self.resulte))
        else:
            self.assert_result = assert_run(self.config_path).walk_find(data['result'], self.resulte)
        self.send({'request':self.req,'resulte':self.resulte,'comment':self.comment,'assert':self.assert_result,'request_url':self.request_url})
        self.read_log()
    #读取json模板信息，并与传入参数匹配生成json字符串，第一个为模板路径，第二个要生成json的数据信息,返回匹配后的json字符串
    def creat_json(self,v,data):
        #判断是否有id_data模块，若有则改成id
        if 'id'  in list(data.keys()):
            data.pop('id')
        if 'id_data' in list(data.keys()):
            data['id']=data.pop('id_data')
        j=data
        #将data中的值用before_request返回的字典中的值替换
        j=data
        #判断是否有重复json
        #判断哪个键包含有二级参数
        if type(v) == dict:
            #判断是否为实数，且小数点后面为全部为0
            for k in list(j.keys()):
                if type(j[k])==float and int(j[k])==j[k]:
                    j[k]=int(j[k])
            for k in list(v.keys()):
                # print  "第一次dict%s" % str(k)
                if type(v[k]) != dict and type(v[k]) != list:
                    if k not in j:
                        v.pop(k)
                        continue
                    if type(j[k]) not in [dict,float,int,int,list] and j[k].strip()=='':
                        v.pop(k)
                    else:
                       self.s = self.change(v[k], j[k])
                       v[k] = self.s
                elif type(v[k]) == list:
                    for z in v[k]:
                        self.creat_json(z, j)
                elif type(v[k]) == dict:
                    self.creat_json(v[k], j)
        return json.dumps(v)
    def change(self, a, b):
        if type(a) == int:
            try:
                b = int(str(b).split('.')[0])
            except Exception as err:
                print(traceback.format_exc())
                print(err)
        elif type(a) == float:
            try:
                if str(b).split('.')[-1]=='0':
                      b = float(str(b).split('.')[0])
                else:
                    b=float(b)
            except Exception as err:
                print(traceback.format_exc())
                print(err)
        else:
            try:
                float(b)
            except Exception as err:
                print(traceback.format_exc())
                print(err)
                if type(b)==int:
                    b = str(b)
                else:
                    b=b
            b=str(b)
        return b
    #f发送调用的实验用的接口，参数第一个为请求数据，第二个为列表形式：第一个为url,第二个为头，第三个为头值
    def  reque(self,data,config):
        req=dict(config.items('config'))
        if req['head_key'].strip()!='':
            if req['method']=='post':
                if self.url != '':
                   self.respons=self.port.post(data, config,self.url)
                else:
                    self.respons = self.port.post(data, config)
            elif req['method']=='get':
                if self.url != '':
                    self.respons = self.port.get(data, config, self.url)
                else:
                    self.respons =self.port.get(data, config)
            elif req['method']=='delete':
                if self.url != '':
                    self.respons= self.port.delete(data, config, self.url)
                    if  self.respons['respons'].strip()=='':
                        self.respons['respons']={}
                    else:
                     self.respons = self.respons
                else:
                  self.respons = self.port.delete(data, config)
            return {"result":self.respons['respons'],"request_url":self.respons['url']}

             # if self.url != '':
             #    req['url'] = self.url
             # if data.strip()=='':
             #     parm={"param":"nullß"}
             # else:
             #    parm=json.loads(data)
             # try:
             #    r=requests.get(url=req['url'], params=parm,headers=head_vk,verify=False)
             # except Exception,e:
             #     respons=json.dumps({'error_detail':str(e)})
             # else:
             #     respons=r.text
             # req_data=urllib.urlencode(json.loads(data))
             # if '?' not in req['url']:
             #     req['url']=req['url']+'?'+req_data
             # print 88888888888888888888888888888888888888
             # print req['url']
             # request = urllib2.Request(req['url'])
             # for k,i in head_vk.iteritems():
             #    request.add_header(k,i)
             # try :
             #   response  = urllib2.urlopen(request)
             # except urllib2.URLError, e:
             #     return json.dumps({"open_error": str(e.reason)})
             # x=response.read()
             #return respons
        else :
            #判断表格中是否有url字符按
            sign = dict(config.items('sign'))
            if self.url!='':
                sign['url']=self.url.split(req['url'].split(sign['url'])[0])[-1]
                req['url']=self.url
                self.data=''
            elif req['method']=='get':
                public_url=req['url'].split(sign['url'])[0]
                req['url'] = req['url']+'?'+ urllib.parse.urlencode(eval(data))
                sign['url']= sign['url']+'?'+ urllib.parse.urlencode(eval(data))
            if data.strip()!='':
                data=json.dumps(json.loads(data))
            head=make_head(sign['url'],sign['app_key'],data,self.config_path.get('config','method'),self.config_path)
            #判断是post还是get请求,如果json文件中是空值，则发送get请求
            if req['method']=='get':
                response = requests.get(url=req['url'],headers=head,params=json.loads(data),verify=False)
            else:
              response = requests.post(url=req['url'], data=data, headers=head,verify=False)
            self.request_url=req['url']
            return  response.text
    #执行js将json数据传送到页面上
    def send_js(self,req,pon):
       if req.strip()!='':
          req=json.dumps(json.loads(req))
       self.log.wri("发送到前端的js请求 %s" % req)
       if req.strip()!='':
          req=json.dumps(json.loads(json.dumps(demjson.decode(req)), parse_int=int), indent=4, sort_keys=False,
                  ensure_ascii=False).replace('"','\\"').replace('\n','\\n').replace('\\\\','\\')
       """
       #利用webdriver向页面填充json字符串
       self.h.execute_script('$("#1").html("%s")'  % req)
       pon = json.dumps(json.loads(json.dumps(demjson.decode(pon)), parse_int=int), indent=4, sort_keys=False,
                        ensure_ascii=False).replace('"', '\\"').replace('\n', '\\n')
       self.h.execute_script('$("#2").html("%s")' % pon)
       self.h.execute_script('$("#yun1").html("%s")' % os.path.basename(self.path))
       """
    #调用发送数据的接口
    def send(self,b):
        #发送服务器信息\
        #url = 'http://127.0.0.1:5021/linux_config'
        #倒数第二个个为接口配置信息，最后一个为目录信息
        #request = urllib2.Request(url)
        #request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
        data={}
        data['config']=dict(self.config_path.items('config'))
        data['name'] = os.path.basename(self.path)
        data['comment']=b['comment']
        data['request']=b['request']
        data['resulte']=b['resulte']
        data['assert'] = b['assert']
        data['request_url']=b['request_url']
        self.run_result=data
        #response = urllib2.urlopen(request, urllib.urlencode(data))
        #发送接口信息
        # url='http://127.0.0.1:5021/jiaobenshuru'
        #request = urllib2.Request(url)
        #request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
        #response = urllib2.urlopen(request, urllib.urlencode(data))
    #读取日志
    def read_log(self):
        #发送服务器信息
        url = 'http://127.0.0.1:5021/read_logs'
        request = urllib.request.Request(url)
        request.add_header('content-TYPE', 'application/x-www-form-urlencoded')
        data={"name":os.path.basename(self.path)}
        try:
           response = urllib.request.urlopen(request,urllib.parse.urlencode(data))
           x=response.read().split('\n')
        except Exception as err:
            print(traceback.format_exc())
            print(err)
        return 11
class log(object):
    def __init__(self):
        self.logger = logging.getLogger('mylogger')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(r'C:\log.txt')
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    def wri(self,data):
        self.logger.info(data)

#启动其他程序线程
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
         #os.path.join(os.path.dirname(sys.argv[0]), 'app', 'jie_kou_test', 'run.py')
         os.system('python    '+os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0])))+'/run.py')
if __name__=='__main__':
    #支付
    #run(r'C:\work\lr_test\paymax_list')
    #退款
    #run(r'C:\work\lr_test\paymax_refund')
    #查询退款
    #run(r'C:\work\lr_test\paymax_check_refund')
    #查询订单
    #run(r'C:\work\lr_test\paymax_check_list')
    #批量代付
   # run(r'C:\work\lr_test\daifu\paymax_daifu')
    #example
    #run(os.path.join(os.getcwd(), 'example'))
    #代付查询
   # run(r'C:\work\lr_test\daifu\paymax_daifu_query')
    #退票回盘文件下载
    #run(r'C:\work\lr_test\daifu\paymax_daifu_returndownload')
    #普通回盘文件下载
    #run(r'C:\work\lr_test\daifu\paymax_daifu_download')
    #代扣流程
    #run(r'C:\work\lr_test\daikou\paymax_daikou')
    #查询实时代扣
    #run(r'C:\work\lr_test\daikou\paymax_daishou')
    #实时代付文件下载
    #run(r'C:\work\lr_test\daikou\paymax_daishou_download')
    #卡前置运行
    #run(r'C:\work\lr_test\card_before\card_before_pay')
    # 卡前置发送验证码
   # run(r'C:\work\lr_test\card_before\card_before_send_ms')
    # 银行卡绑定查询
    #run(r'C:\work\lr_test\card_before\card_bank_list')
    # 银行卡解绑
    #run(r'C:\work\lr_test\card_before\card_bank_card_unbind')
    # 支付确认
   #run(r'C:\work\lr_test\card_before\card_before_conform')
    # 发送退款
    # run(r'C:\work\lr_test\card_before\card_before_refunds')
    # 发送退款查询
    #run(r'C:\work\lr_test\card_before\card_bank_check_refunds')
    # 卡前置收银台支付
    #run(r'C:\work\lr_test\支付\拉卡拉PC网关支付')
    # 查询支付
    MyThread().run()
    mulu()
    #run(r'C:\所写系统\无时间限制正常程序\lr_test\第二套环境\HGTP\get接口')
    # 卡前置收银台发送验证码
    #run(r'C:\work\lr_test\卡前置收银台\卡前置收银台_发送验证码')
    #卡前置收银台绑卡查询
   # run(r'C:\work\lr_test\卡前置收银台\卡前置收银台_绑卡查询')
    # 卡前置收银台支付查询
    #run(r'C:\work\lr_test\卡前置收银台\卡前置收银台_下单查询')
     #create_stock(r'E:\httt_stock_last_jiaoben\getSto#ckDetail')
    # create_stock(r'E:\httt_stock_last_jiaoben\getStockAuditList')
   # create_stock(r'E:\httt_stock_last_jiaoben\stockAudit')
     #create_stock(r'E:\httt_stock_last_jiaoben\queryGoodsList')
    # create_stock(r'E:\httt_stock_last_jiaoben\getStockManageList')
    # create_stock(r'E:\httt_stock_last_jiaoben\acceptCISResult')
     #create_stock(r'E:\httt_stock_last_jiaoben\autoOnlineDataCheck')