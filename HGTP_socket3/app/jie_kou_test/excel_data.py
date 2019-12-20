#处理excel表格中的特殊数据
import sys
import random
import requests
import json
from selenium import webdriver
import time
import chardet
import unittest
import demjson
import urllib.request, urllib.parse, urllib.error
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
#from  creat_dang import *
import unittest
import xlrd
import json
import urllib.request, urllib.error, urllib.parse
import os
import logging
import datetime
import configparser
from app.jie_kou_test.json_pi_pei.excel_data import  *
import re
from flask import current_app
from app.jie_kou_test.sing_data.pymql import BANKS
import cx_Oracle

class excel_data_exe(object):
    # 处理excel表格中的特殊数据,带#的为要运行的代码数据，必须有一个返回值
    def han_shu(self,data):
        print(data)
        print(__name__)
        print('===============================')
        if type(data)==list:
            for k,i in enumerate(data):
                if type(i)==dict:
                    for z,u in i.items():
                        if "##" in u:
                            self.b = 'self.a='
                            exec (self.b + u.split('##')[1])
                            data[k][z]=self.b
            return data
        else:
            self.b = 'self.a='
            exec (self.b + data.split('##')[1])
            return self.a
#传入的参数是json字典，返回self.data
class change(object):
    def __init__(self,data):
        self.data=data
        if type(data)==dict:
            for k in list(data.keys()):
                 if type(data[k]) not in [dict,list]  and type(data[k])  in [str,str]:
                     self.data[k]=self.change_data(self.data[k])
                 else:
                     change(self.data[k])
        elif type(data)==list:
            for k,i in enumerate(data):
                if type(i) not in [dict,list]  and type(i)  in [str,str]:
                    self.change_data(i)
                else:
                    change(i)
    def change_data(self,simple_data):
        self.simple_data=simple_data
        pattern = r"(\[.*?\]\[.*?\])"
        guid = re.findall(pattern, self.simple_data, re.M)
        if len(guid)>0:
            for i in guid:
                self.simple_data=self.simple_data.replace(i,'7')
        return  self.simple_data
def save_data_config(excel_data,path,old_config,*result):
    error_statu=False
    if len(result)!=0:
        if type(result[0]) in [dict,list]:
            result_json=result[0]
        else:
            try:
                result_json=json.loads(result[0])
            except:
                error_statu=True
    db_path=os.path.join(os.path.dirname(path),'db.txt')
    cf = configparser.ConfigParser()
    cf.read(db_path)
    for i in current_app.config.get('CLEAR_DB_DATA'):
        if i in cf.options('data'):
            cf.remove_option('data', i)
    if 'data' not in cf.sections():
        cf.add_section('data')
    if 'data' not in old_config.sections():
        old_config.add_section('data')
    if 'save_data' in list(excel_data.keys()) and excel_data['save_data'].strip()!='':
        all_save=excel_data['save_data'].split(',')
        for k, i in enumerate(all_save):
            rs = re.findall(re.compile(r'=[[]"(.*?)["]]', re.S), i)
            if rs[0]=='request':
                data_key=re.findall(re.compile(r'(.*?)=', re.S), i)[0]
                try:
                    k = re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i)[-1]
                    data_value = excel_data[k]
                except KeyError:
                    raise Exception("找不到需要保存的参数:"+re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i)[-1])
                cf.set('data',data_key, data_value)
                old_config.set('data', data_key, data_value)
                if 'idcardno' == data_key:
                    h, t = 5, 3
                    val = data_value[:h] + ('**' * ((len(data_value)-h -t) // 2)).replace('  ', ' ').strip() + data_value[-t:]
                    cf.set('data', 'maskedCredNum', val)
                    old_config.set('data', 'maskedCredNum', val)
                if 'bankcard' == data_key:
                    bcd = BANKS[data_value[:6]][1]
                    cf.set('data', 'bankcode', bcd)
                    old_config.set('data', 'bankcode', bcd)

            elif 'db' in rs[0]:
                data_key=re.findall(re.compile(r'(.*?)=', re.S), i)[0]
                data_value=re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i)
                for k, i in enumerate(data_value):
                    data_value[k] = '[' + i + ']'
                data_value=''.join(data_value)
                data_value=change_data_db(old_config,data_value).simple_data
                cf.set('data',data_key,data_value)
                old_config.set('data',data_key,data_value)
            elif rs[0]=='result':
                if not error_statu:
                    data_key = re.findall(re.compile(r'(.*?)=', re.S), i)[0]
                    try:
                        data_value=eval('result_json'+i.split('["result"]')[-1])
                    except:
                        data_value = json.dumps({'接口地址': path, '错误信息': "常量保存错误"})
                    cf.set('data', data_key, data_value)
                    old_config.set('data', data_key, data_value)
                    if 'ecifId' == data_key:
                        cf.set('data', 'platformuserno', 'HFJYJF' + data_value + '2')
                        old_config.set('data', 'platformuserno', 'HFJYJF' + data_value + '2')
                        dbtype = old_config.get('db_oracle_core', 'type')
                        dbconn = old_config.get('db_oracle_core', 'conn')
                        if 'oracle' == dbtype:
                            db = cx_Oracle.connect(dbconn)
                            cursor = db.cursor()
                            sql = old_config.get('sql', 'account_no')
                            param = sql[sql.find('['): sql.rfind(']') + 1]
                            sec, opt, t = param[1:-1].split('][')
                            sql = sql.replace(param, old_config.get(sec, opt))
                            try:
                                res = cursor.execute(sql).fetchall()[0][0]
                                cf.set('data', 'jyacctid', res)
                                old_config.set('data', 'jyacctid', res)
                            except Exception as err:
                                print(err)
                                raise Exception("数据库中无对应记录：" + sql)
                            cursor.close()
                            db.close()
                else:
                    data_value=json.dumps({'接口地址':path,'错误信息':"常量保存错误"})
                    cf.set('data', data_key, data_value)
                    old_config.set('data', data_key, data_value)
            elif rs[0]=='result_split':
                data_key= re.findall(re.compile(r'(.*?)=', re.S), i)[0]
                data_path= re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i+']')
                if ';' in data_path[-1]:
                    data_path = re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i + ']')[1:-1]
                else:
                    data_path = re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i + ']')[1:]
                get_result_json = result_json
                for z in data_path:
                    if ';' in z:
                        break
                    if isinstance(get_result_json, dict):
                        if z in get_result_json:
                           get_result_json = get_result_json[z]
                        else:
                            raise Exception("保存变量路径错误" + json.dumps(result_json), "错误接口：" + path)

                if isinstance(get_result_json, bytes):
                    get_result_json = get_result_json.decode('utf-8')

                if not isinstance(get_result_json, str):
                    raise Exception("保存变量路径过短")

                begin_str = i.split('[')[-1].split(';')[0].strip().replace('\\', '')
                over_str = i.split('[')[-1].split(';')[-1].split(']')[0].strip().replace('\\', '')
                if not error_statu:
                    # data_key = re.findall(re.compile(r'(.*?)=', re.S), i)[0]
                    # begin_str=re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i)[-1].split(',')[0].split('"')[0]
                    # try:
                    #    over_str=re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i)[-1].split(',')[1].split('"')[-1]
                    # except:
                    #     pass
                    try:
                        data_value=get_result_json.split(begin_str)[-1].split(over_str)[0]
                    except:
                        data_value = json.dumps({'接口地址': path, '错误信息': "常量保存错误"})
                    cf.set('data', data_key, data_value)
                    try:
                       old_config.set('data', data_key, data_value)
                    except:
                        pass
                else:
                    data_value=json.dumps({'接口地址':path,'错误信息':"常量保存错误"})
                    cf.set('data', data_key, data_value)
                    old_config.set('data', data_key, data_value)
    cf.write(open(db_path, 'w'))
#测试中
def save_data_normal(path,sec,op,va):
    db_path = os.path.join(os.path.dirname(path), 'db.txt')
    cf = configparser.ConfigParser()
    cf.read(db_path)
    if  sec not in cf.sections():
        cf.add_section(sec)
    cf.set(sec,op,va)
    cf.write(open(db_path, 'w'))
#执信登陆，返回登陆后的session
def zhixin_login(name,password,url,secret_pic):
    url = 'https://testwww.zhixininvest.com/official/zxUser/login'
    response = requests.get(url)
    cookies = response.cookies.get_dict()
    u = 'SESSION=' + cookies['SESSION']
    parm = {'phone': name.strip(),
            'password': password,
            'imgCode': secret_pic}
    url = url.split('/official/zxUser/login')[0]+'/official/zxUser/submit/login'
    header = {}
    header['Cookie'] = u
    header['Content-Type'] = 'application/x-www-form-urlencoded'
    k = requests.post(url, data=parm, headers=header)
    return u

#保存参数化sql
def save_sql_config(excel_data, path, old_config, *result):
    error_statu = False
    if len(result) != 0:
        if type(result[0]) in [dict, list]:
            result_json = result[0]
        else:
            try:
                result_json = json.loads(result[0])
            except:
                error_statu = True
    db_path = os.path.join(os.path.dirname(path), 'db.txt')
    cf = configparser.ConfigParser()
    cf.read(db_path)
    [cf.remove_option('data', i) for i in current_app.config.get('CLEAR_DB_DATA') if
     i in cf.options('data')]
    if 'data' not in cf.sections():
        cf.add_section('data')
    if 'data' not in old_config.sections():
        old_config.add_section('data')
    if 'save_data' in list(excel_data.keys()) and excel_data['save_data'].strip() != '':
        for i in excel_data['save_data'].split(','):
            if re.findall(re.compile(r'=[[]"(.*?)["]]', re.S), i)[0] == 'request':
                data_key = re.findall(re.compile(r'(.*?)=', re.S), i)[0]
                data_value = excel_data[re.findall(re.compile(r'[[]"(.*?)["]]', re.S), i)[-1]]
                cf.set('data', data_key, data_value)
                old_config.set('data', data_key, data_value)
            elif re.findall(re.compile(r'=[[]"(.*?)["]]', re.S), i)[0] == 'result':
                if not error_statu:
                    data_key = re.findall(re.compile(r'(.*?)=', re.S), i)[0]
                    try:
                        data_value = eval('result_json' + i.split('["result"]')[-1])
                    except:
                        data_value = json.dumps({'接口地址': path, '错误信息': "常量保存错误"})
                    cf.set('data', data_key, data_value)
                    try:
                        old_config.set('data', data_key, data_value)
                    except:
                        pass
                else:
                    data_value = json.dumps({'接口地址': path, '错误信息': "常量保存错误"})
                    cf.set('data', data_key, data_value)
                    old_config.set('data', data_key, data_value)
    cf.write(open(db_path, 'w'))








