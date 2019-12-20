# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\just_run\change_request_before.py
# Compiled at: 2019-05-27 16:53:31
import sys
import importlib
sys.path.append('../../')
importlib.reload(sys)
from selenium import webdriver
import time as timee, chardet, unittest, demjson, urllib.request, urllib.parse, urllib.error, random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, configparser, json, urllib.request, urllib.error, urllib.parse, os, logging
from header import *
from ..just_run.just_run import  *
from ..json_pi_pei.excel_data import *
import copy
from ..json_pi_pei.request_result_flask import *
from ..json_pi_pei.json_pi_pei import *
from ..json_pi_pei.request_run import *
from ..assert_run.assert_run import *

class change_request_before(object):

    def __init__(self, all_bianliang):
        self.all_bianliang = all_bianliang

    def use(self, data, path, config_path):
        self.config_path = config_path
        self.path = os.path.dirname(path)
        if 'before_request' in list(data.keys()) and data['before_request'].strip() != '':
            self.all = []
            self.data = copy.deepcopy(data)
            self.all.append(data['before_request'])
            while 'before_request' in list(self.data.keys()) and self.data['before_request'].strip() != '':
                self.s = read_data(self.data['before_request'], self.path).data
                if 'before_request' in list(self.s.keys()) and self.s['before_request'].strip() != '':
                    self.all.append(self.s['before_request'])
                    self.data = self.s
                else:
                    break

            if '/' in self.all[(-1)]:
                self.s = just_run(os.path.join(os.path.dirname(self.path), self.all[(-1)].split('$')[0].strip()), self.all[(-1)].split('$')[1], data={}, before_req='', config_path=self.config_path, all_bianliang=self.all_bianliang)
            else:
                self.s = just_run(os.path.join(os.path.dirname(self.path), self.all[(-1)].split('$')[0].strip()), self.all[(-1)].split('$')[1], data={}, before_req='', config_path=self.config_path, all_bianliang=self.all_bianliang)
            if 'err_detail' in list(self.s.data.keys()):
                return self.s.data
            for i in list(reversed(self.all[:-1])):
                if not isinstance(self.s.respons, dict):
                    try:
                        json.loads(self.s.respons)
                    except Exception as err:
                        print(traceback.format_exc())
                        print(err)
                        self.s.respons = json.dumps({})
                p1 = os.path.join(os.path.dirname(self.path), i.split('$')[0].strip())
                p2 = i.split('$')[1]
                p3 = self.s.respons
                if not isinstance(p3, dict):
                    p3 = json.loads(p3)
                self.s = just_run(p1, p2, p3, self.s.full_data, self.config_path, self.all_bianliang)
                if 'err_detail' in list(self.s.data.keys()):
                    return self.s.data

            for k, u in data.items():
                if type(self.s.respons) == str:
                    self.s.respons = json.loads(self.s.respons)
                if '{{' in str(u) and '}}' in str(u):
                    self.kk = [
                     u.split('{{')[0], u.split('}}')[(-1)]]
                    self.idd = u.split('{{')[(-1)].split('}}')[0]
                    self.change_statu = 0
                    if self.idd.split(']')[0].split('[')[(-1)] in ('"*str"', '"*int"',
                                                                   '"*float"'):
                        self.change_statu = self.idd.split(']')[0].split('[')[(-1)]
                        self.idd = self.idd.split(self.change_statu)[(-1)][1:]
                    if type(self.s.respons) not in [list, dict]:
                        self.before_result_last = json.loads(self.s.respons)
                    else:
                        self.before_result_last = self.s.respons
                    try:
                        self.change_before_data = eval('self.before_result_last' + self.idd)
                        if self.change_statu != 0:
                            if self.change_statu == '"*str"':
                                self.change_before_data = str(self.change_before_data)
                            elif self.change_statu == '"*float"':
                                self.change_before_data = float(self.change_before_data)
                            elif self.change_statu == '"*int"':
                                self.change_before_data = int(float(self.change_before_data))
                        if type(self.change_before_data) in [float, int, bool, int] or self.change_before_data == None:
                            data[k] = self.change_before_data
                        else:
                            data[k] = self.kk[0] + self.change_before_data + self.kk[(-1)]
                    except Exception as e:
                        data[k] = '前置接口获取不到该参数'

                elif '((' in str(str(u)) and '))' in str(str(u)):
                    data[k] = change_canshu(self.s.full_data, u)

            self.respons = self.s.respons
        else:
            self.respons = data
        return self.respons


def change_canshu(a, b):
    if type(b) == list:
        for k, i in enumerate(b):
            if type(i) == dict:
                for z in i:
                    i[z] = tihuan(a, i[z])

            else:
                b[k] = tihuan(a, b[k])

    else:
        if type(b) == dict:
            for i in b:
                b[i] = tihuan(a, b[i])

        else:
            b = tihuan(a, b)
    return b


def tihuan(a, b):
    if '((' in b and '))' in b:
        k = [
         b.split('((')[0], b.split('))')[(-1)]]
        idd = b.split('((')[(-1)].split('))')[0]
        return eval('a' + idd)
    return b


class read_data(object):

    def __init__(self, zhi, path):
        if '/' in zhi:
            self.path = os.path.join(os.path.dirname(path), zhi.split('$')[0].strip()).strip()
        else:
            self.path = os.path.join(path, zhi.split('$')[0]).strip()
        self.id = zhi.split('$')[(-1)]
        excel_name = os.path.basename(self.path)
        public_config_path = os.path.join(os.path.dirname(self.path), 'config.txt')
        if os.path.isfile(public_config_path):
            public_config = configparser.ConfigParser()
            public_config.read(public_config_path)
            public_config.read(public_config_path)
        for dir, b, file in os.walk(self.path):
            for z in file:
                if excel_name in z:
                    self.excel_path = os.path.join(self.path, z)
                elif 'json' == z.split('.')[0]:
                    self.json_path = os.path.join(self.path, z)
                elif 'configparse' == z.split('.')[0]:
                    self.config_path = configparser.ConfigParser()
                    self.config_data = self.config_path.read(os.path.join(self.path, z))

        if os.path.isfile(os.path.join(os.path.dirname(self.path), 'config.txt')):
            url = public_config.get('url', 'public_url').strip() + self.config_path.get('config', 'private_url')
            self.config_path.set('config', 'url', url)
        self.data = xlrd.open_workbook(self.excel_path)
        self.table = self.data.sheets()[0]
        self.key = self.table.row_values(0)
        for k, i in enumerate(self.key):
            if type(i) == float:
                self.key[k] = int(i)

        for k, i in enumerate(self.key):
            if str(i).strip() == 'id':
                self.k = k
                break

        for i in range(1, self.table.nrows):
            if str(int(str(self.table.row_values(i)[k]).split('#')[(-1)].split('.')[0])).strip() == str(self.id).strip():
                self.data = dict(list(zip(self.key, self.table.row_values(i))))
                break

        for i in list(self.data.keys()):
            data_s = str(self.data[i])
            if '##' in data_s:
                self.s = excel_data_exe()
                param = None
                if ('(' in data_s) and data_s.endswith(')'):
                    param = self.data.get(data_s[data_s.find('(') + 1: data_s.find(')')])
                self.data[i] = self.s.han_shu(self.data[i], param)
