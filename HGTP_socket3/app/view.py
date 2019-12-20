# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\view.py
# Compiled at: 2019-04-16 15:55:35
from tempfile import mktemp
from flask import send_from_directory, send_file, Response
import socket, paramiko, os, json, urllib.request, urllib.error, urllib.parse, re, chardet
import traceback
from .jie_kou import *
from functools import wraps
import time, threading, sqlite3
from flask import render_template, flash, redirect, request, g, Response, stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash, jsonify
import datetime, json
from . import app
import unittest
bootstrap = Bootstrap(app)
from app import UPLOAD_FOLDER

@app.before_request
def before_request():
    pass
#    if time.time() > 1560650805:
#        return jsonify(statu='success')


@app.route('/mulu_detail', methods=['POST', 'GET'])
def mulu_detail():
    path = str(request.form['mulu']).strip()
    current_app.config['mulu'] = path
    select_huanjing = ''
    yewu_name = {}
    if not os.path.isdir(os.path.join(path, request.form['huanjing'].strip())):
        return jsonify(statu='no dir')
    if request.form['huanjing'].strip() == '' or not os.path.isdir(os.path.join(path, request.form['huanjing'].strip())):
        huanjing = [ os.path.join(path, i) for i in os.listdir(path) if i.strip() != '' and 'git' not in i and 'DS_Store' not in i
                   ]
    else:
        huanjing = [
         os.path.join(path, request.form['huanjing'].strip())]
    if select_huanjing.strip() != '':
        for i in huanjing:
            if select_huanjing == os.path.basename(i):
                select_jing = i

    else:
        select_jing = huanjing[0]
    for filename in os.listdir(select_jing):
        if filename.strip() != '' and '.git' not in filename and '__init__' not in filename and 'DS_Store' not in filename:
            value = []
            if os.path.isfile(os.path.join(select_jing, filename)):
                return jsonify(error_detail='请选择上级目录')
            try:
                for z in os.listdir(os.path.join(select_jing, filename)):
                    if os.path.isdir(os.path.join(select_jing, filename, z)):
                        value.append(z)

            except:
                pass

            yewu_name[filename] = [ i for i in os.listdir(os.path.join(select_jing, filename)) if os.path.isdir(os.path.join(select_jing, filename, i)) and 'data_config' not in i ]

    huanjing_list = [ i for i in os.listdir(path) if i.strip() != '' and 'git' not in i and 'DS_Store' not in i
                    ]
    huanjing_list.remove(os.path.basename(select_jing))
    all_data = {}
    all_data['yewu_name'] = yewu_name
    all_data['select_huanjing'] = os.path.basename(select_jing)
    all_data['huanjing'] = huanjing_list
    all_data = json.dumps(all_data)
    return jsonify(data=all_data)


from .jie_kou_test.pi_run import all_run

@app.route('/piliang_run', methods=['POST', 'GET'])
def piliang_run():
    data = json.loads(request.form['data'])
    data['all_jiekou'] = [ os.path.join(data['gen_mulu'], i) for i in data['all_jiekou'] if i.strip() != '' ]
    server_ip = request.remote_addr
    time_interval = current_app.config.get('RUN_INTERVAL')
    MyThread_jiekou(data['all_jiekou'], data['run_time'], data['ip_dizhi'], server_ip).run()
    return jsonify(a=2)


class MyThread_jiekou(threading.Thread):

    def __init__(self, all_jiekou, run_time, ip, server_ip):
        self.all_jiekou = all_jiekou
        self.run_time = run_time
        self.ip = ip
        self.server_ip = server_ip
        threading.Thread.__init__(self)

    def run(self):
        all_run.run(self.all_jiekou, self.run_time, self.ip, self.server_ip)
        url = 'http://' + self.server_ip + ':8080/piliang_run_over'
        test_data = urllib.parse.urlencode({'statu': 'over', 'path': 'server', 'ip': self.ip}).encode(encoding='utf-8')
        req = urllib.request.Request(url=url, data=test_data)
        try:
            res_data = json.loads(urllib.request.urlopen(req).read())
            print(__name__)
            print(res_data)
            print('==================================')
        except Exception as err:
            print(err)

@app.route('/ceshi', methods=['POST', 'GET'])
def ceshi():
    return render_template('/jie_kou_ping_tai/result_error.html')


@app.route('/jiankong_mulu', methods=['POST', 'GET'])
def jiankong_mulu():
    current_app.config['jiankong_mulu'] = request.form['mulu']
    return jsonify(statu='success')


@app.route('/get_mulu', methods=['POST', 'GET'])
def get_mulu():
    try:
        current_app.config['jiankong_mulu']
    except Exception as err:
        print(traceback.format_exc())
        print(err)
        current_app.config['jiankong_mulu'] = ''

    return jsonify(mulu=current_app.config['jiankong_mulu'])


from .lenove_jie_kou.jiekou_list import *

@app.route('/jiaobenshuru', methods=['POST'])
@jiaobenshuru
def jiaoben_shuru():
    pass


@app.route('/ceshi_post', methods=['POST', 'GET'])
def ceshi_post():
    return jsonify(a='SUCCESS')


@app.route('/linux_config', methods=['POST'])
def linux_config():
    return jsonify(a=111)


from .lenove_jie_kou.jiekou_list import *

@app.route('/shishitiaoshi', methods=['GET', 'POST'])
@shishitiaoshi_new
def shishitiaoshi():
    pass


from .lenove_jie_kou.jiekou_list import delete_shsihitiaoshi

@app.route('/delete_shsihitiaoshi', methods=['GET', 'POST'])
@delete_shsihitiaoshi
def delete_shsihitiaoshi():
    pass


@app.before_request
def before_request():
    pass


from .lenove_jie_kou.creat_jielou_file import create_file

@app.route('/creat_file', methods=['POST', 'GET'])
@create_file
def creat_file():
    pass


from .lenove_jie_kou.creat_jielou_file import read_config

@app.route('/read_config', methods=['POST', 'GET'])
@read_config
def read_config():
    pass


from .lenove_jie_kou.creat_jielou_file import save_conifg

@app.route('/save_conifg', methods=['POST', 'GET'])
@save_conifg
def save_conifg():
    pass


from .lenove_jie_kou.creat_jielou_file import open_excel

@app.route('/open_excel', methods=['POST'])
@open_excel
def open_excel():
    pass


from .lenove_jie_kou.creat_jielou_file import open_all_jiekou

@app.route('/get_all_jiekou', methods=['POST'])
@open_all_jiekou
def open_all_jiekou():
    pass


from .lenove_jie_kou.creat_jielou_file import get_yewu_jiekou

@app.route('/get_yewu_jiekou', methods=['POST'])
@get_yewu_jiekou
def get_yewu_jiekou():
    pass


@app.route('/clear_tisohi', methods=['POST'])
def clear_tisohi():
    db = sqlite3.connect(current_app.config.get('JIE_KOU'))
    cu = db.cursor()
    cu.execute('delete  from  jie_kou_test WHERE num=? and ip=?', (
     'run', request.remote_addr))
    db.commit()
    db.close()
    resp = jsonify(statu='scuess')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


from .lenove_jie_kou.shishitiaoshi import *

@app.route('/creat_result_json', methods=['POST'])
@create_result_json
def creat_result_json():
    pass


from .lenove_jie_kou.submit_git import submit_git

@app.route('/set_local_file_save', methods=['POST'])
@submit_git
def submit_git():
    pass


from .lenove_jie_kou.submit_git import delete_local_file_save

@app.route('/delete_local_file_save', methods=['POST'])
@delete_local_file_save
def delete_local_file_save():
    pass


@app.route('/<name>', methods=['POST', 'GET'])
def submit_git(name):
    return jsonify(name=name)


from .lenove_jie_kou.submit_git import banben_data

@app.route('/banben_data', methods=['POST', 'GET'])
@banben_data
def banben_data():
    pass


from .lenove_jie_kou.raad_log import raad_log_file

@app.route('/raad_log_file', methods=['POST'])
@raad_log_file
def raad_log_file():
    pass


from .lenove_jie_kou.raad_log import log_peizhi_submit

@app.route('/log_peizhi_submit', methods=['POST', 'GET'])
@log_peizhi_submit
def log_peizhi_submit():
    pass


import random

@app.route('/test_run', methods=['POST', 'GET'])
def test_run():
    detail = ''
    if 'runing_type' in list(session.keys()) and session['runing_type'] == 'runing':
        if 'run_detail' in list(session.keys()) and session['runing_type'].strip() != '':
            detail = session['runing_type'].split('$%')[0]
            if len(session['runing_type'].split('$%')[0]) > 1:
                session['runing_type'] = ('$%').join(session['runing_type'].split('$%')[1:])
            else:
                session['runing_type'] = ''
    resp = jsonify(detail=detail)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


from .jieyue_ui.ui_run import get_case_detail

@app.route('/get_case_detail', methods=['GET', 'POST'])
@get_case_detail
def get_case_detail():
    pass


from .jieyue_ui.ui_run import run_log

@app.route('/run_log', methods=['GET', 'POST'])
@run_log
def run_log():
    pass


from .jieyue_ui.ui_run import run_ui_simple

@app.route('/run_simple', methods=['GET', 'POST'])
@run_ui_simple
def run_ui_simple():
    pass


from .jieyue_ui.ui_run import run_statu_ui

@app.route('/run_statu_ui', methods=['GET', 'POST'])
@run_statu_ui
def run_statu_ui():
    pass


from .jieyue_ui.ui_run import ui_run_result

@app.route('/ui_run_result', methods=['GET', 'POST'])
@ui_run_result
def ui_run_result():
    pass


from .lenove_jie_kou.linux_log import linux_log_reserver

@app.route('/linux_log_reserver', methods=['GET', 'POST'])
@linux_log_reserver
def linux_log_reserver():
    pass


from .lenove_jie_kou.linux_log import read_linux_log

@app.route('/read_linux_log', methods=['GET', 'POST'])
@read_linux_log
def read_linux_log():
    pass