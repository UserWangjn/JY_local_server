# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
#批量运行结果页面
from tempfile import mktemp
from assert_run import  *
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
from functools import wraps
#不是自动打开的页面，可以查看调试信息
def piliangjiekou_result(func):
  @wraps(func)
  def ceshi():
    func()
    ip = request.remote_addr
    if ip=='127.0.0.1':
        ip='192.168.137.1'
    if request.method == "GET":
        s_assert=assert_run()
        #根据ip地址读取测试数据
        g.cu.execute('select * from  jiekou_result where ip=?', (ip,))
        data = g.cu.fetchall()
        tim=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(data[-1][-2])))
        all=[]
        if len(data)!=0:
             for i in data:
                 name=i[0]
                 detail=[]
                 statu=0
                 count=len(json.loads(i[2]))
                 fail=0
                 succ=0
                 for k,z in json.loads(i[2]).items():
                     result= json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(z['respons']))), parse_int=int), indent=4,
                                    sort_keys=False,
                                    ensure_ascii=False)
                     id=int(k)
                     case_assert=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(json.loads(z['case_assert'])))), parse_int=int), indent=4,
                                    sort_keys=False,
                                    ensure_ascii=False)
                     comment=z['case_name']
                     req=z['req']
                     req = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(req))), parse_int=int), indent=4,
                                    sort_keys=False,
                                    ensure_ascii=False)
                     if z['assert_result']==False:
                         statu=1
                         fail+=1
                         detail.append(["failCase",id,comment,case_assert,result,req])
                     else:
                         succ+=1
                         detail.append(["passCase", id, comment, case_assert,result,req])
                 detail=sorted(detail,key=lambda x:x[1])
                 if statu==1:
                         all.append([name,"failClass",[count,succ,fail,count],detail])
                 elif statu==0:
                         all.append([name,"passClass", [count, succ, fail, count], detail])
        #z中元素第一个接口名字，第二个接口的count，第三个用例状态，最后一个列表d第一个为用例状态，第二个用例id，第三个用例comment，第四个用例的接口数据
        return render_template('/hualala/jiekou_test/test_result.html',z=all,time=tim)
  return ceshi
##接收接口测试返回过来的批量接口数据，并存入数据库中
def jiekou_result(func):
    def resultee():
        func()
        #接口名和接口运行数据的列表
        data=request.form['data']
        time=request.form['time']
        ip=request.form['ip']
        #将获取的数据存入数据库jiekoui_test表中
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        #删除原有数据根据ip地址
        cu.execute('delete  from jiekou_result where ip=? and time!=?',[ip,str(time)])
        db.commit()
        for k,i in eval(data).items():
            cu.executemany('INSERT INTO  jiekou_result(name,ip,data,time) VALUES (?,?,?,?,null)', [(k,ip,str(i),str(time))])
            db.commit()
        #cu.executemany('INSERT INTO  jiekou_result(name,ip,data,time) VALUES (?,?,?,?)', [(1,2,3,time.time())])
        db.close()
        return jsonify(a='1')
    return resultee