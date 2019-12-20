# -*- coding: utf-8 -*-
# import urllib,urllib2
import execjs
from bs4 import BeautifulSoup
import os
import re
import json
import requests
import time
import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse
import hashlib
import sys
#好房后台加密
def haofang_server(config):
    url=config.get('login','url')
    name = config.get('login', 'name')
    password = config.get('login', 'password')

def get_js():
    print(99999999999999999999999999999999)
    print(os.path.join(os.path.split(os.path.realpath(__file__))[0],"messagehash.js"))
    f = open(os.path.join(os.path.split(os.path.realpath(__file__))[0],"messagehash.js"), 'r') # 打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr+line
        line = f.readline()
    return htmlstr
def get_des_psswd():
    jsstr = get_js()
    ctx = execjs.compile(jsstr) #加载JS文件
    return (ctx.call('encryptAes', '111111aA', "qhcjr01234567890"))

def haofang_login(name,password,url):
    response = requests.get(url=url)
    cookies = response.cookies.get_dict()['JSESSIONID_COOKIE']
    print(cookies)
    headers={'Cookie':'JSESSIONID_COOKIE='+cookies}
    url=url.split('user/')[0]+'user/login'
    parm={'username': name,'password': password,'ismulpwd': 'chenGnag1'}
    password=get_des_psswd()
    req = urllib.request.Request(url=url, data=urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=headers)
    res = urllib.request.urlopen(req)
    print(res.read())
    return headers