# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\just_run\just_run.py
# Compiled at: 2019-05-22 18:22:29
import sys
import importlib
sys.path.append('../../')
importlib.reload(sys)
from selenium import webdriver
import time as timee, chardet
from ..sing_data.haofang_server import haofang_login
import unittest, demjson, urllib.request, urllib.parse, urllib.error, random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, configparser, json, urllib.request, urllib.error, urllib.parse, os, logging, hashlib
from header import *
from ..excel_data import *
from ..json_pi_pei.excel_data import *
from ..json_pi_pei.request_result_flask import *
from ..json_pi_pei.json_pi_pei import *
from ..json_pi_pei.request_run import *
from ..assert_run.assert_run import *
from ..json_pi_pei.before_after_sql import before_after_sql

class just_run(object):

    def __init__(self, path, id, data, before_req, config_path, all_bianliang):
        self.all_bianliang = all_bianliang
        self.path = path
        self.all_config_path = config_path
        excel_name = os.path.basename(self.path)
        for dir, b, file in os.walk(self.path):
            for z in file:
                if excel_name in z:
                    self.excel_path = os.path.join(self.path, z)
                elif 'json' == z.split('.')[0]:
                    self.json_path = os.path.join(self.path, z)
                elif 'configparse' == z.split('.')[0]:
                    self.config_path = configparser.ConfigParser()
                    self.config_data = self.config_path.read(os.path.join(self.path, z))
                    db_config_path = os.path.join(os.path.dirname(self.path), 'db.txt')
                    content = open(db_config_path).read()
                    content = re.sub('\\xfe\\xff', '', content)
                    content = re.sub('\\xff\\xfe', '', content)
                    content = re.sub('\\xef\\xbb\\xbf', '', content)
                    with open(db_config_path, 'w') as f:
                        f.write(content)
                    db_config = configparser.ConfigParser()
                    db_config.read(db_config_path)
                    if os.path.isfile(os.path.join(os.path.dirname(self.path), 'db.txt')) and self.config_path.get('sign', 'sign_type').strip() == 'zhixin':
                        for i in db_config.sections():
                            self.config_path.add_section(i)
                            [ self.config_path.set(i, k, db_config.get(i, k)) for k in db_config.options(i) ]

                    if os.path.isfile(os.path.join(os.path.dirname(self.path), 'config.txt')):
                        public_config_path = os.path.join(os.path.dirname(self.path), 'config.txt')
                        private_config_path = os.path.join(self.path, 'configparse.txt')
                        self.private_config = configparser.ConfigParser()
                        public_config = configparser.ConfigParser()
                        public_config.read(public_config_path)
                        self.private_config.read(private_config_path)
                        if os.path.isfile(public_config_path):
                            if self.config_path.get('sign', 'sign_type').strip() == 'web':
                                if 'login' not in self.config_path.sections():
                                    self.config_path.add_section('login')
                                if 'login' in self.private_config.sections() and all(k in self.private_config.options('login') for k in public_config.options('login')) and not all(self.config_path.get('login', i) == self.private_config.get('login', i) for i in self.private_config.options('login')):
                                    [ public_config.set('login', z, self.private_config.get('login', z)) for z in self.private_config.options('login') ]
                                [ self.config_path.set('login', z, public_config.get('login', z)) for z in public_config.options('login')
                                ]
                                if all(k in self.config_path.options('login') for k in ['url', 'name', 'password']):
                                    hash = hashlib.md5()
                                    code = self.config_path.get('login', 'url').strip() + self.config_path.get('login', 'name').strip() + self.config_path.get('login', 'password').strip()
                                    hash.update(code)
                                    code = str(hash.hexdigest())
                                    if code not in self.all_config_path.options('login_value'):
                                        headers_dict = web_token(public_config)
                                        self.all_config_path.set('login_value', code, json.dumps(headers_dict))
                                self.config_path.add_section('login_value')
                                [ self.config_path.set('login_value', i, self.all_config_path.get('login_value', i)) for i in self.all_config_path.options('login_value') ]
                                self.config_path.set('login', 'headers_dict', config_path.get('login', 'headers_dict'))
                                head_key = self.private_config.get('config', 'head_key').split('.')
                                head_value = self.private_config.get('config', 'head_value').split('.')[:len(head_key)]
                                header_older = json.dumps(dict(list(zip(head_key, head_value))))
                                self.config_path.set('login', 'headers_old', header_older)
                            else:
                                if self.config_path.get('sign', 'sign_type').strip() == 'Backstage_web':
                                    if 'login' not in self.config_path.sections():
                                        self.config_path.add_section('login')
                                    self.config_path.set('login', 'url', public_config.get('login', 'url'))
                                    self.config_path.set('login', 'name', public_config.get('login', 'name'))
                                    self.config_path.set('login', 'password', public_config.get('login', 'password'))
                                    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko', 
                                       'Content-Type': 'application/json'}
                                    self.config_path.add_section('app_head')
                                    self.config_path.set('app_head', 'app_head', json.dumps(header_dict))
                                    if 'token' not in self.config_path.options('login'):
                                        token = houtai_jiami(self.config_path.get('login', 'name').strip(), self.config_path.get('login', 'password').strip(), self.config_path.get('login', 'url').strip())
                                        self.config_path.set('login', 'token', token)
                                    else:
                                        token = self.config_path.get('login', 'token')
                                    save_data_normal(self.path, 'data', 'token', token)
                                else:
                                    if self.config_path.get('sign', 'sign_type').strip() == 'jy_appServer':
                                        if 'sign_url' in public_config.sections() and 'sign_url' not in self.config_path.sections():
                                            self.config_path.add_section('sign_url')
                                            self.config_path.set('sign_url', 'encode_url', public_config.get('sign_url', 'encode_url'))
                                            self.config_path.set('sign_url', 'decode_url', public_config.get('sign_url', 'decode_url'))
                                    else:
                                        if self.config_path.get('sign', 'sign_type').strip() == 'hkci':
                                            if 'login' not in self.config_path.sections():
                                                self.config_path.add_section('login')
                                            self.config_path.set('login', 'login_url', public_config.get('login', 'login_url'))
                                            self.config_path.set('login', 'server_host', public_config.get('login', 'server_host'))
                                            self.config_path.set('login', 'phone', public_config.get('login', 'phone'))
                                            self.config_path.set('login', 'ling_pai', public_config.get('login', 'ling_pai'))
                                            self.config_path.set('login', 'dian_pu', public_config.get('login', 'dian_pu'))
                                            if 'huasheng_headertoken' in list(self.all_bianliang.keys()):
                                                if self.config_path.get('login', 'phone') == self.all_bianliang['phone'] and self.config_path.get('login', 'ling_pai') == self.all_bianliang['ling_pai'] and self.config_path.get('login', 'dian_pu') == self.all_bianliang['dian_pu']:
                                                    self.config_path.set('login', 'huasheng_headertoken', self.all_bianliang['huasheng_headertoken'])
                                            else:
                                                self.all_bianliang['phone'] = self.config_path.get('login', 'phone')
                                                self.all_bianliang['ling_pai'] = self.config_path.get('login', 'ling_pai')
                                                self.all_bianliang['dian_pu'] = self.config_path.get('login', 'dian_pu')
                                                get_mendian_detail_url = self.config_path.get('login', 'server_host') + '/hk-peanut-car/api/place/getLoginPlaceInfo'
                                                db_detail = [db_config.get('db_mysql_login', 'host'), db_config.get('db_mysql_login', 'port'),
                                                 db_config.get('db_mysql_login', 'user'), db_config.get('db_mysql_login', 'password'), db_config.get('db_mysql_login', 'db')]
                                                huasheng_headertoken = hs_login(self.config_path.get('login', 'server_host'), db_detail, self.config_path.get('login', 'login_url'), self.config_path.get('login', 'phone'), self.config_path.get('login', 'dian_pu'), self.config_path.get('login', 'ling_pai'))
                                                self.all_bianliang['huasheng_headertoken'] = huasheng_headertoken
                                                self.config_path.set('login', 'huasheng_headertoken', self.all_bianliang['huasheng_headertoken'])
                                            save_data_normal(self.path, 'data', 'huasheng_headertoken', self.all_bianliang['huasheng_headertoken'])
                                        else:
                                            if self.config_path.get('sign', 'sign_type').strip() == 'zhixin':
                                                if 'login' not in self.config_path.sections():
                                                    self.config_path.add_section('login')
                                                self.config_path.set('login', 'url', public_config.get('login', 'url'))
                                                self.config_path.set('login', 'name', public_config.get('login', 'name'))
                                                self.config_path.set('login', 'password', public_config.get('login', 'password'))
                                                self.config_path.set('login', 'secret', public_config.get('login', 'secret'))
                                                if 'login_name' in db_config.options('data'):
                                                    self.config_path.set('login', 'name', db_config.get('data', 'login_name'))
                                                if 'login_password' in db_config.options('data'):
                                                    self.config_path.set('login', 'password', db_config.get('data', 'login_password'))
                                                if 'login_secret' in db_config.options('data'):
                                                    self.config_path.set('login', 'secret', db_config.get('data', 'login_secret'))
                                                if 'login_token' in list(self.all_bianliang.keys()) and 'login' in self.config_path.sections():
                                                    if self.config_path.get('login', 'name') == self.all_bianliang['name'] and self.config_path.get('login', 'password') == self.all_bianliang['password']:
                                                        self.config_path.set('login', 'token', self.all_bianliang['login_token'])
                                                header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko', 
                                                   'Content-Type': 'application/json'}
                                                self.config_path.add_section('app_head')
                                                self.config_path.set('app_head', 'app_head', json.dumps(header_dict))
                                                if 'token' not in self.config_path.options('login'):
                                                    token = zhixin_login(self.config_path.get('login', 'name').strip(), self.config_path.get('login', 'password').strip(), self.config_path.get('login', 'url').strip())
                                                    self.config_path.set('login', 'token', token)
                                                else:
                                                    token = self.config_path.get('login', 'token')
                                                save_data_normal(self.path, 'data', 'token', token)
                                            else:
                                                if self.config_path.get('sign', 'sign_type').strip() in ('app', 'xiang_qian'):
                                                    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko', 'Content-Type': 'application/json'}
                                                    self.config_path.add_section('app_head')
                                                    self.config_path.set('app_head', 'app_head', json.dumps(header_dict))
                                                else:
                                                    if self.config_path.get('sign', 'sign_type').strip() == 'haofang_server':
                                                        if 'login' not in self.config_path.sections():
                                                            self.config_path.add_section('login')
                                                        self.config_path.set('login', 'url', public_config.get('login', 'url'))
                                                        self.config_path.set('login', 'name', public_config.get('login', 'name'))
                                                        self.config_path.set('login', 'password', public_config.get('login', 'password'))
                                                        if 'haofang_headertoken' in list(self.all_bianliang.keys()):
                                                            if self.config_path.get('login', 'name') == self.all_bianliang['name'] and self.config_path.get('login', 'password') == self.all_bianliang['password']:
                                                                self.config_path.set('login', 'haofang_headertoken', self.all_bianliang['haofang_headertoken'])
                                                            else:
                                                                self.all_bianliang['name'] = self.config_path.get('login', 'name')
                                                                self.all_bianliang['password'] = self.config_path.get('login', 'password')
                                                                haofang_headertoken = json.dumps(haofang_login(self.config_path.get('login', 'name').strip(), self.config_path.get('login', 'password').strip(), self.config_path.get('login', 'url').strip()))
                                                                self.all_bianliang['haofang_headertoken'] = haofang_headertoken
                                                                self.config_path.set('login', 'haofang_headertoken', self.all_bianliang['haofang_headertoken'])
                                                        else:
                                                            self.all_bianliang['name'] = self.config_path.get('login', 'name')
                                                            self.all_bianliang['password'] = self.config_path.get('login', 'password')
                                                            haofang_headertoken = json.dumps(haofang_login(self.config_path.get('login', 'name').strip(), self.config_path.get('login', 'password').strip(), self.config_path.get('login', 'url').strip()))
                                                            self.all_bianliang['haofang_headertoken'] = haofang_headertoken
                                                            self.config_path.set('login', 'haofang_headertoken', self.all_bianliang['haofang_headertoken'])
                                                        save_data_normal(self.path, 'data', 'haofang_headertoken', self.all_bianliang['haofang_headertoken'])
                            if public_config.get('url', 'public_url').strip() != '':
                                url = self.config_path.get('config', 'private_url')
                                self.config_path.set('config', 'public_url', public_config.get('url', 'public_url').strip())
                                self.config_path.set('config', 'url', public_config.get('url', 'public_url').strip() + url.strip())

        if 'run_interval' in self.all_config_path.options('sign') and 'run_interval' not in self.config_path.options('sign'):
            self.config_path.set('sign', 'run_interval', self.all_config_path.get('sign', 'run_interval'))
        if os.path.isfile(os.path.join(os.path.dirname(self.path), 'db.txt')) and self.config_path.get('sign', 'sign_type').strip() != 'zhixin':
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
            if str(int(str(self.table.row_values(i)[k]).split('#')[(-1)].split('.')[0])).strip() == str(id).strip():
                self.data = dict(list(zip(self.key, self.table.row_values(i))))
                break

        if 'head_data' in self.key and self.data['head_data'].strip() != '':
            request_header = change_data_db(self.config_path, self.data['head_data'], i).data
            self.config_path.add_section('head_data')
            self.config_path.set('head_data', 'head_data', request_header)
        for z in self.data:
            try:
                if str(z)[0] != '0' and int(z) == float(z):
                    z = str(int(z))
            except Exception as err:
                print(traceback.format_exc())
                print(err)

        kknum = 0
        for z in self.data:
            kknum += 1
            if kknum == 1:
                pass
            try:
                if str(self.data[z])[0] != '0' and int(self.data[z]) == float(self.data[z]):
                    self.data[z] = str(int(self.data[z]))
            except Exception as err:
                print(traceback.format_exc())
                print(err)
            if '##' in str(self.data[z]):
                data_s = str(self.data[z])
                self.s = excel_data_exe()
                param = None
                if ('(' in data_s) and data_s.endswith(')'):
                    param = self.data.get(data_s[data_s.find('(') + 1: data_s.find(')')])
                self.data[z] = self.s.han_shu(self.data[z], param)

            elif '{{' in str(self.data[z]) and '}}' in str(self.data[z]):
                self.kk = [
                 self.data[z].split('{{')[0], self.data[z].split('}}')[(-1)]]
                self.idd = self.data[z].split('{{')[(-1)].split('}}')[0]
                try:
                    self.data[z] = self.kk[0] + str(eval('data' + self.idd)) + self.kk[(-1)]
                except Exception as e:
                    self.data = {'err_detail': str(e), 'message': '获取不到前置接口返回值'}
                    break

            elif '((' in str(self.data[z]) and '))' in str(self.data[z]):
                self.kk = [
                 self.data[z].split('((')[0], self.data[z].split('))')[(-1)]]
                self.idd = self.data[z].split('((')[(-1)].split('))')[0]
                self.data[z] = self.kk[0] + str(eval('before_req' + self.idd)) + self.kk[(-1)]

        self.full_data = copy.deepcopy(self.data)
        self.url = {}
        self.di = {}
        if open(self.json_path).read().strip() != '':
            j = json.loads(open(self.json_path).read())
        else:
            j = ''
        self.data = change_data_db(self.config_path, self.data).data
        if isinstance(self.data, str):
            self.data = json.loads(self.data)
        change_json_data(j, self.data)
        self.data = change(self.config_path, self.data)
        if 'id_data' in self.data:
            self.data['id'] = self.data.pop('id_data')
        if 'url' in list(self.data.keys()) and self.data['url'].strip() != '':
            if os.path.isfile(os.path.join(os.path.dirname(self.path), 'config.txt')) and public_config.get('url', 'public_url').strip() != '':
                url = self.config_path.get('config', 'url')
                if 'http' not in self.data['url']:
                    self.data['url'] = public_config.get('url', 'public_url').strip() + self.data['url']
            self.url = str(self.data['url'])
        if 'json' in list(self.data.keys()) and str(self.data['json']).strip() != '':
            self.req = self.data['json']
        else:
            self.req = self.data
        if 'before_sql' in list(self.data.keys()) and self.data['before_sql'] != '':
            before_after_sql(self.data['before_sql'], self.config_path)
            self.data.pop('before_sql')
        after_sql = ''
        if 'after_sql' in list(self.data.keys()) and self.data['after_sql'] != '':
            after_sql = self.data.pop('after_sql')
        self.req = creat_json(copy.deepcopy(j), self.req)
        port = request_run(j, self.config_path, self.path)
        self.config_path.set('config', 'mulu_path', self.path)
        if self.url != {}:
            if self.config_path.get('config', 'method') == 'post':
                if self.config_path.get('config', 'head_key').strip() == '':
                    self.respons = json.loads(port.post(self.req, self.url)['respons'])
                else:
                    self.respons_this = port.post(self.req, self.config_path, self.url)['respons']
                    try:
                        self.respons = json.loads(self.respons_this)
                    except Exception as err:
                        print(traceback.format_exc())
                        print(err)
                        self.respons = {'result': self.respons_this}

            elif self.config_path.get('config', 'method') == 'get':
                if self.config_path.get('config', 'head_key').strip() == '':
                    self.respons = json.loads(port.get('', self.url)['respons'])
                else:
                    self.respons = port.get(self.req, self.config_path, self.url)['respons']
                    try:
                        self.respons = json.loads(self.respons)
                    except Exception as err:
                        print(traceback.format_exc())
                        print(err)
                        self.respons = {'result': self.respons}

            elif self.config_path.get('config', 'method') == 'delete':
                self.respons = port.delete(self.req, self.config_path, self.url)['respons']
                try:
                    self.respons = json.loads(self.respons)

                except Exception as err:
                    print(traceback.format_exc())
                    print(err)
                    self.respons = {'result': self.respons}

        else:
            if self.config_path.get('config', 'method') == 'post':
                self.respons = port.post(self.req, self.config_path)['respons']
                if self.respons.strip() == '':
                    self.respons = {'detai': '接口返回值为空'}
            else:
                if self.config_path.get('config', 'method') == 'get':
                    self.respons = json.loads(port.get(self.req, self.config_path)['respons'])
                else:
                    if self.config_path.get('config', 'method') == 'delete':
                        try:
                            self.respons = json.loads(port.delete(self.req, self.config_path)['respons'])
                        except Exception as err:
                            print(traceback.format_exc())
                            print(err)
                            self.respons = {'result': port.delete(self.req, self.config_path)['respons']}

        if after_sql != '':
            before_after_sql(after_sql, self.config_path)
        if 'save_data' in list(self.data.keys()):
            save_data_config(self.data, self.path, self.all_config_path, self.respons)
        self.assert_run = assert_run(self.config_path)
        self.assert_result = self.assert_run.walk_find(self.data['result'], self.respons)
        if self.assert_result == False:
            raise Exception('错误接口名' + self.path + str(self.respons))
        self.path = path.replace('\\', '/')
        if self.path in list(self.all_bianliang['before_case_detail'].keys()) and len(self.all_bianliang['before_case_detail'][self.path][int(id)]) == 0:
            self.all_bianliang['before_case_detail'][self.path][int(id)] = {}
            self.all_bianliang['before_case_detail'][self.path][int(id)]['request'] = json.loads(self.req)
            try:
                self.all_bianliang['before_case_detail'][self.path][int(id)]['result'] = json.loads(self.respons)
            except Exception as err:
                print(traceback.format_exc())
                print(err)
                self.all_bianliang['before_case_detail'][self.path][int(id)]['result'] = self.respons


if __name__ == '__main__':
    x = just_run('C:\\Users\\wo\\Desktop\\\ufefflr_test的副本\\okex系统\\http接口v3新版\\下单交易', 1)
    print(x.respons)
    for k, u in x.respons.items():
        print(u)