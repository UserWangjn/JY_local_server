import sys
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
#去除公共部分的url
def make_head(url,key,body,method,config):
    #SignConfig.PAYRIGHT_SECRET_KEY=key
    sign_key={}
    if 'app_key' in config.options("sign"):
        if config.get('sign', 'app_key').strip() != '':
            sign_key['app_key']=config.get('sign', 'app_key')
            SignConfig.PAYRIGHT_APP_KEY = config.get('sign', 'app_key')
    if 'sectet_key' in config.options("sign"):
        if config.get('sign','sectet_key').strip()!='':
            sign_key['sectet_key'] = config.get('sign', 'sectet_key')
            SignConfig.PAYRIGHT_SECRET_KEY=config.get('sign','sectet_key').strip()
    header = setHeader(sign_key=sign_key)
    if 'private_key' in config.options("sign"):
        if config.get('sign', 'private_key').strip() != '':
            sign_key['private_key'] = config.get('sign', 'private_key')
            private_key=config.get('sign', 'private_key')
        else:
            private_key=''
#组装header
    if method.strip()=='post':
       sign_data = to_sign_data(header=header, method='post', uri=url, body=body,sign_key=sign_key)
       print("sing_data的值为")
       print(sign_data)
       request_header = {'Host': header['Host'],
                  "Content-Type": "application/json;charset=utf-8",
                  'Authorization': header['Authorization'],
                  'nonce': header['nonce'],
                  'timestamp': header['timestamp'],
                  'sign': sign_data}
    elif method.strip()=='get':
            # 签名数据
            sign_data = to_sign_data(header=header, method='get', uri=url,body='',sign_key=sign_key)
            # 组装HTTP Header
            request_header = {'Host': header['Host'],
                              "Content-Type": "application/json;charset=utf-8",
                              'Authorization': header['Authorization'],
                              'nonce': header['nonce'],
                              'timestamp': header['timestamp'],
                              'sign': sign_data}

    return request_header
