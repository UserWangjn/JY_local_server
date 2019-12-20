#处理excel表格中的特殊数据
import sys
import re
import requests
# import cx_Oracle
import json
import datetime
from selenium import webdriver
import time
import chardet
import unittest
import demjson
import pymysql
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
import random
import pymysql
from excel_data import  *

# def before_after_sql(sql_detail,config):
#     for i in  sql_detail.split(','):
#         pattern = r"[[](.*?)[]]"
#         i = re.findall(pattern, sql_detail, re.M)
#         if len(i)==2 :
#             db = pymysql.connect(
#                 host=config.get(i[0], 'host'),
#                 port=int(config.get(i[0], 'port')),
#                 user=config.get(i[0], 'user'),
#                 password=config.get(i[0], 'password'),
#                 db=config.get(i[0], 'db')
#             )
#             cursor = db.cursor()
#             for z in i[1].split(','):
#                 if "=" in z:
#                     reslut=z.split('=')[-1]
#                     cursor.execute(config.get('sql', z.split('=')[0].strip()))
#                     shiji=cursor.fetchall()
#                     if len(shiji)>0 and str(shiji[0][0])==str(reslut):
#                         pass
#                     else:
#                         return {"statu":'error','detail':u"结果返回不对","sql":config.get('sql', z.split('=')[0].strip())}
#                 else:
#                     try:
#                        cursor.execute(config.get('sql',z))
#                     except:
#                         pass
#                 db.commit()
#             db.close()
#             return  {"statu":"success"}
def before_after_sql(sql_detail,config):
    type_re = r"(\[.*?\]\[.*?\]\[.*?\])"
    for i in  sql_detail.split(','):
        if len(re.findall(type_re, i, re.M))==0:
              i=i+'[none]'
              s=change_data_db(config,i)
        elif len(re.findall(type_re, i, re.M))>0:
            s = change_data_db(config, i)
        assert_str=s.simple_data.replace('[none]','')
        statu=0
        for i in ['==','<','>','>=','<=','!=']:
            if  i in assert_str:
                assert_str=i.join(["'"+str(i).strip()+"'" for i in assert_str.split(i)])
                statu=1
                break
        #logger.debug(assert_str)
        if  statu==1:
            if not   eval(assert_str):
                ex = Exception("sql断言失败%s" % s.simple_data.replace('[none]',''))
                raise ex
    return  {"statu":"success"}