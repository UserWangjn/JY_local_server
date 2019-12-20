# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
#根据列表执行运行文件
from tempfile import mktemp
from app import app
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
import datetime
from functools import wraps
import sys
from app.jie_kou_test.json_pi_pei import  excel_data
import datetime
from jie_kou_test.just_run.save_global_data import set_global_data
import configparser
# 获取所有section，返回值
def raad_log_file (func):
    def raad_log_file():
        log_section=['name','mulu','ip','port','user','password','begin_str','finish_str']
        cf = configparser.ConfigParser()
        mulu=os.path.join(request.form['mulu'],request.form['huanjing'],request.form['yewu'],'linux.txt')
        if  not  os.path.isfile(mulu):
            open(mulu,'w').close()
            cf.read(mulu)
            cf.add_section('linux')
            [cf.set('linux',i,'') for i in log_section]
            cf.write(open(mulu,'w'))
            res=jsonify(statu='create_success')
        else:
           detail={}
           cf.read(mulu)
           if 'linux' not in cf.sections():
               cf.add_section('linux')
               [cf.set('linux', i, '') for i in log_section]
               cf.write(open(mulu, 'w'))
           for i in log_section:
               if i in cf.options('linux'):
                   detail[i]=cf.get('linux', i)
               else:
                   detail[i]=''
           res=jsonify(statu='read_success',detail=json.dumps(detail))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    return raad_log_file
#读取或写入配置文件

def log_peizhi_submit(func):
    def log_peizhi_submit():
        func()
        log_section=['name','mulu','ip','port','user','password','begin_str','finish_str']
        cf = configparser.ConfigParser()
        mulu = os.path.join(request.form['gen_mulu'], request.form['huangjing'], request.form['yewu'], 'linux.txt')
        if not os.path.isfile(mulu):
            open(mulu,'w').close()
            cf.read(mulu)
            cf.add_section('linux')
            [cf.set('linux',i,'') for i in log_section]
            cf.write(open(mulu,'w'))
            res=jsonify(statu='create_success')
        else:
            cf.read(mulu)
        log_section=['name','mulu','ip','port','user','password','begin_str','finish_str']
        for i in log_section:
            cf.set('linux',i,request.form[i])
        cf.write(open(mulu, 'w'))
        return jsonify(statu='success')
    return log_peizhi_submit