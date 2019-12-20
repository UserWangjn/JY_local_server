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
import configparser
# 获取所有section，返回值
def linux_log_reserver (func):
    def linux_log_reserver():
        linux_mulu=os.path.join(request.form['gen_mulu'],request.form['huanjing'],request.form['yewu'])
        cf = configparser.ConfigParser()
        if not os.path.isfile(os.path.join(linux_mulu,'linux_log.txt')):
            open(os.path.join(linux_mulu,'linux_log.txt'),'w').close()
            cf.read(os.path.join(linux_mulu,'linux_log.txt'))
            for i in ['linux','split_detail','mulu']:
                 cf.add_section(i)
            [cf.set('linux',i,request.form[i]) for i in ['ip','port','name','password']]
            cf.set('mulu','log_mulu',request.form['log_mulu'])
            cf.set('split_detail', 'log_begin_split', request.form['log_begin_split'])
            cf.set('split_detail', 'log_done_split', request.form['log_done_split'])
            cf.write(open(os.path.join(linux_mulu,'linux_log.txt'), "w"))
            res=jsonify(statu='success')
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    return linux_log_reserver




def read_linux_log(func):
    def read_linux_log():
        func()
        linux_mulu = os.path.join(request.form['gen_mulu'], request.form['huanjing'], request.form['yewu'])
        cf = configparser.ConfigParser()
        if os.path.isfile(os.path.join(linux_mulu,'linux_log.txt')):
            linux_log_detail={}
            cf.read(os.path.join(linux_mulu,'linux_log.txt'))
            for i in ['linux', 'split_detail', 'mulu']:
                linux_log_detail[i]={}
                if i in cf.sections():
                    for z in cf.options(i):
                        linux_log_detail[i][z]=cf.get(i,z)
            res = jsonify(statu='success',linux_log_detail=linux_log_detail)
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
        else:
            res = jsonify(statu='success',linux_log_detail="none")
            res.headers['Access-Control-Allow-Origin'] = '*'
            return res
    return read_linux_log