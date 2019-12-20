# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
#批量运行结果页面
from tempfile import mktemp
from flask import send_from_directory,send_file,Response
import socket
import os
import time
import sqlite3
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask import current_app
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import json
import demjson
from functools import wraps
import os
import sys
import requests
import urllib.request, urllib.error, urllib.parse,urllib.request,urllib.parse,urllib.error
url='http://172.18.100.141:9081/loan/user/toLoginReal'
conn1 = requests.session()
response = conn1.get(url)
res = response.text
cookies = requests.utils.dict_from_cookiejar(response.cookies)
first_id = cookies['JSESSIONID_COOKIE']
print(first_id)
url='http://172.18.100.141:9081/loan/user/login'
headers={'Content-Type': 'application/x-www-form-urlencoded,Cookie','JSESSIONID_COOKIE':first_id}
param={'username': 11043779,'password': 111111}
response=requests.post(url, param)
id=  response.url.split('JSESSIONID=')[-1]



header={'Cookie': 'JSESSIONID_COOKIE='+id}
all_url='http://172.18.100.141:9081/loan/lbTIntoInfo/intoInitCheck'
data={'cardType': 1,
'cardId': 372928198510260038,
'prodType': '01',
'prodCode': 'PTL160600126',
'customerManager': '10026859',
'custName': '孙振',
'mainOrSub': '1'
        }
request = urllib.request.Request(all_url, urllib.parse.urlencode(data), headers=header)
print((urllib.request.urlopen(request).read()))
