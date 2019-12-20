# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
#根据列表执行运行文件
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import os
import time
import shutil
import sqlite3
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask import current_app
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import json
import demjson
import datetime
from functools import wraps
def change_config(func):
    def change():
        if request.method=='GET':
            yewu_name,jiekou_name=request.args.get('path').split('#')
            huanjing = [os.path.join(current_app.config.get('JIE_KOU_URL'), i.decode('gb2312')) for i in
                        os.listdir(current_app.config.get('JIE_KOU_URL'))
                        if i.strip() != '' and 'git' not in i]
            if 'jie_kou_huan_jing' in list(session.keys()):
                pass
            else:
                session['jie_kou_huan_jing'] = huanjing[0]
            path=os.path.join(session['jie_kou_huan_jing'],yewu_name,jiekou_name,'configparse.txt')
            text=open(path).read()
            if text.strip()!='':
                text.decode('gb2312')
            return jsonify(a=text.decode('gb2312'))
        elif request.method=='POST':
            all_path=[i for i in request.form['path_class'].split('$') if i.strip()!='']
            for k,i in enumerate(all_path):
                yewu_name, jiekou_name = i.split('#')
                path = os.path.join(session['jie_kou_huan_jing'], yewu_name, jiekou_name)
                all_path[k]=path
            for k,i in  enumerate(all_path):
                for parent, dirnames, filenames in os.walk(i):
                    for filename in filenames:
                             if filename=='configparse.txt':
                                 path=os.path.join(parent,'configparse.txt')
                                 now = datetime.datetime.now()
                                 file=str(time.time())+'.txt'
                                 shutil.copy(os.path.join(parent,'configparse.txt'),os.path.join(parent,file))
                                 open(path, 'w').write(request.form['text_data'].encode('gb2312'))
            return jsonify(result='success')
    return change