from tempfile import mktemp
import traceback
from app import app
from flask import send_from_directory,send_file,Response
import socket
import paramiko
import os
import demjson
import json
import configparser
import urllib.request, urllib.error, urllib.parse
import re
import  chardet
import time
import sqlite3
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap

from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import json
import xlwt
def create_file(func):
    def ceshiaa():
        func()
        jiekou_path=os.path.join(request.form['gen_mulu'],request.form['huanjing'],request.form['yewu'],request.form['jiekou_name'])
        jiekou_name=request.form['jiekou_name']
        if request.form['json_data'].replace('<br>','').strip()!='':
            try:
                json_data=list(request.form['json_data'])
                for k,i in enumerate(json_data):
                    if ord(i)==160:
                        json_data[k]=' '
                jiekou_moban=json.loads(''.join(json_data).replace('<br>',''))
            except Exception as err:
                print(traceback.format_exc())
                print(err)
                error_statu='json格式错误'
                resp = jsonify(statu=error_statu)
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp
        else:
            jiekou_moban={}
        if os.path.exists(jiekou_path):
            error_statu='接口目录已经存在'
        else:
            os.makedirs(jiekou_path)
            #创建excel表格
            file = xlwt.Workbook()
            table = file.add_sheet('Sheet1')
            table.write(0, 0, 'id')
            table.write(0, 1, 'Comment')
            #往excel表格中添加请求参数
            jiekou_canshu=[]
            k=0
            for k,i in enumerate(canshu(jiekou_canshu,jiekou_moban)):
                table.write(0, k+2, i[0])
                table.write(1, k + 2, i[1])
            #添加result列表
            table.write(0, k + 3, 'result')
            table.write(1, 0, 1)
            table.write(1, 1, 'test')
            file.save(os.path.join(jiekou_path, jiekou_name + '.xls'))
            #创建json配置文件
            json_file=open(os.path.join(jiekou_path, 'json.txt'),'w')
            json_file.write(json.dumps(jiekou_moban,indent=4))
            json_file.close()
            error_statu='success'
            #创建configparse.txt 配置文件
            open(os.path.join(jiekou_path, 'configparse.txt'),'w').close()
            config = configparser.SafeConfigParser()
            config.read(os.path.join(jiekou_path, 'configparse.txt'))
            config.add_section('config')
            config.add_section('sign')
            config.set('config', 'private_url', request.form['request_url'])
            config.set('config', 'method', request.form['method'])
            config.set('config', 'head_key', 'Content-type')
            config.set('config', 'request_type', request.form['request_type'])
            config.set('config', 'head_value', 'application/x-www-form-urlencoded')
            config.set('sign', 'sign_type', request.form['sign_type'])
            # if request.form['sign_type']=='Backstage_web':
            #     if 'login' not  in config.sections():
            #         config.add_sections('login')
            #     config.set('login','url',request.form['login_url'])
            #     config.set('login', 'name', request.form['user'])
            #     config.set('login', 'password', request.form['password'])
            config.write(open(os.path.join(jiekou_path, 'configparse.txt'),'w'))
        resp=jsonify(statu=error_statu)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return ceshiaa

#返回json请求模板中所有的参数列表,第一个为要添加的list变量，第二个为字典
def canshu(canshu_list,request_moban):
     for i in request_moban:
         if type(request_moban[i]) not in [list,dict]:
             canshu_list.append([i,request_moban[i]])
         elif type(request_moban[i])==dict:
             canshu(canshu_list,request_moban[i])
         elif type(request_moban[i])==list:
             canshu_list.append([i, json.dumps(request_moban[i],indent=4)])
             request_moban[i] = 'change_json'
     return canshu_list
def read_config(func):
    def cefeaefe():
        func()
        if request.form['type']=='publick_config':
                jiekou_path = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'],'config.txt')
        if request.form['type']=='db_config':
            jiekou_path = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'], 'db.txt')
        if request.form['type']=='private_config':
            jiekou_path = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'],request.form['jiekou'] ,'configparse.txt')
            json_path=os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'],request.form['jiekou'] ,'json.txt')
            try:
                file_config=open(jiekou_path, 'r+')
            except Exception as err:
                print(traceback.format_exc())
                print(err)
                print(jiekou_path)
            data_config = file_config.read().replace('\n', '<br/>').replace('\r', '<br/>')
            file_json=open(json_path, 'r+')
            # try:
            #data_json = json.dumps(json.loads(file_json.read().replace('\n', '<br/>').replace('\r', '<br/>').decode('gb2312')),sort_keys=True, indent=4).replace('\n', '<br/>').replace('\r', '<br/>')
            data_json = file_json.read().replace('\n', '<br/>').replace('\r', '<br/>').decode('gb2312')
            # except:
            #     data_json=u'json 格式错误未能读取'
            jiekou_path = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'])
            #jiekou_list = [i.encode('gb2312') for i in os.listdir(jiekou_path)]
            jiekou_list =[i for i in os.listdir(jiekou_path) if i not in 'db.txt,config.txt']
            resp = jsonify(data_json=data_json,data_config=data_config.decode('gb2312'),jiekou_list=jiekou_list)
            file_json.close()
            file_config.close()
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        if not os.path.isfile(jiekou_path):
            open(jiekou_path, 'w').close()
        file = open(jiekou_path, 'r+')
        data = file.read().replace('\n', '<br/>').replace('\r', '<br/>')
        file.close()
        resp = jsonify(data=data.decode('gb2312'))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return cefeaefe


def save_conifg(func):
    def afadadfa():
        func()
        if request.form['type']=='publick_config':
                jiekou_path = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'],'config.txt')
        if request.form['type']=='db_config':
            jiekou_path = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'], 'db.txt')
        if request.form['type']=='private_config':
            jiekou_path = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'],request.form['jiekou'] ,'configparse.txt')
            json_path=os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'],request.form['jiekou'] ,'json.txt')
            file_config=open(jiekou_path, 'w')
            file_config.write(request.form['config_data'].replace('<div>', '\n').replace('</div>', '').replace('<br>','\n').replace('amp;',''))
            file_config.close()
            file_json=open(json_path, 'w')
            file_json.write(request.form['json_data'].replace('<div>', '\n').replace('</div>', '').replace('<br>','\n').replace('amp;',''))
            file_json.close()
            resp = jsonify(statu='success')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        file=open(jiekou_path,'w')
        file.write(request.form['json_data'].replace('<div>','\n').replace('</div>','').replace('<br>','\n').replace('amp;',''))
        file.close()
        resp = jsonify(statu='success')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return afadadfa

#打开excel
def open_excel(func):
    def afafeqer():
        func()
        jiekou_path = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'],
                                   request.form['jiekou_name'],request.form['jiekou_name']+'.xls')
        os.system(jiekou_path)
        resp = jsonify(statu='success')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return afafeqer
#当select改变时，根绝环境名，返回所有的业务及接口名字
def open_all_jiekou(func):
    def changeaeer():
        func()
        jiekou_path = os.path.join(request.form['mulu'], request.form['huanjing'])
        yewu_list=os.listdir(jiekou_path)
        resp = jsonify(all_yewu=yewu_list,statu='success')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return changeaeer

#根据环境及业务获取所有接口列表信息
def get_yewu_jiekou(func):
    def get_yewu_jiekou():
        func()
        resp = jsonify(statu='success')
        jiekou_path = os.path.join(request.form['mulu'], request.form['huanjing'],request.form['yewu'])
        yewu_list=[i for i in os.listdir(jiekou_path)  if 'txt'  not in i ]
        resp = jsonify(all_jiekou=yewu_list)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return get_yewu_jiekou