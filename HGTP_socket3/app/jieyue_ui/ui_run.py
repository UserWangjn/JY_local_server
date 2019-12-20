from . import old_htmr
from tempfile import mktemp
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
# import old_htmr
import unittest
from concurrent.futures import ThreadPoolExecutor
def run_ui_simple(func):
    def run_simpleee():
        func()
        current_app.config['run_done_num']=0
        current_app.config['success_num'] = 0
        current_app.config['fail_num'] = 0
        current_app.config['error_num'] = 0
        db = sqlite3.connect(current_app.config.get('UI_DB'))
        cu = db.cursor()
        type_run=request.form['type']
        if type_run=='class_run_case_all':
                class_name = request.form['class_name']
                cu.execute('delete from run_type where type=? and run_name=? ',
                           (type_run,str(class_name)))
                db.commit()
                cu.execute('insert into run_type values (null,?,?,?,?,?)',
                           (type_run,str(time.time()),'','run',str(class_name)))
                db.commit()
                row_id = cu.execute('select id from run_type where type=? and run_name=?',(type_run,
                                    str(class_name))).fetchall()[-1][0]
                current_app.config['ui_now_run_id']=row_id
                db.close()
                executor = ThreadPoolExecutor(2)
                mulu = request.form['mulu']
                mulu = os.path.normpath(request.form['mulu'])
                session['run_statu'] = 'running'
                run_bing = executor.submit(test_test, class_name, mulu,current_app.config.get('UI_DB'),type_run,row_id)
        elif type_run=='def_run':
            def_name=request.form['def_name']
            class_name=request.form['class_name']
            cu.execute('delete from run_type where type=? and run_name=? ',
                       (type_run, str(def_name)+'$'+str(class_name)))
            db.commit()
            cu.execute('insert into run_type values (null,?,?,?,?,?) ',
                       (type_run, str(time.time()), '', 'run', str(def_name).strip()+'$'+str(class_name).strip()))
            db.commit()
            row_id=cu.execute('select id from run_type where type=? and run_name=?',(type_run,str(def_name).strip()+'$'+str(class_name).strip())).fetchall()[-1][0]
            current_app.config['ui_now_run_id'] = row_id
            db.close()
            executor = ThreadPoolExecutor(2)
            mulu = request.form['mulu']
            mulu = os.path.normpath(request.form['mulu'])
            session['run_statu'] = 'running'
            run_bing = executor.submit(test_test, [class_name,def_name], mulu, current_app.config.get('UI_DB'),type_run,row_id)
        elif type_run=='run_all':
            class_list = json.loads(request.form['class_list'])
            def_list=[i.split('&') for i in json.loads(request.form['def_list']) if i.split('&')[-1] not in class_list]
            fangfa_detail={"class_list":class_list,"def_list":def_list}
            db_detail=cu.execute('select don_or_run from run_type where type="%s"' % type_run).fetchall()
            if len(db_detail)==0:
                cu.execute('insert into run_type values (null,?,?,?,?,?)',
                           (type_run, str(time.time()), '', 'run', json.dumps(fangfa_detail)))
            else :
                if db_detail[0][0]=='done':
                         cu.executemany('update  run_type  set start_time=?,done_time=?,don_or_run=?,run_name=? where type=? ',
                                   [(str(time.time()),'','run',json.dumps(fangfa_detail),type_run)])
            row_id=cu.execute('select id from run_type where type="%s"' % type_run).fetchall()[0][0]
            cu.execute('delete from run_detail where suite_id="%s"' % (str(row_id)))
            current_app.config['ui_now_run_id'] = row_id
            db.commit()
            db.close()
            executor = ThreadPoolExecutor(2)
            mulu = request.form['mulu']
            mulu =os.path.normpath(request.form['mulu'])
            session['run_statu'] = 'running'
            run_bing = executor.submit(test_test, fangfa_detail, mulu, current_app.config.get('UI_DB'),type_run,row_id)
        resp = jsonify(statu="success")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return run_simpleee

def test_test(class_name,mulu,db_mulu,type_run,row_id):
    db = sqlite3.connect(db_mulu)
    cu = db.cursor()
    discover = unittest.defaultTestLoader.discover(mulu, pattern='*.py')
    u = {}
    retu = {}
    suite = unittest.TestSuite()
    for i in discover:
        for z in i:
            for b in z:
                class_name_new = str(b).split('(')[-1].split(')')[0].strip()
                def_name = str(b).split('(')[0]=str(b).split('(')[0]
                if type_run=='class_run_case_all':
                        if class_name_new == class_name:
                             suite.addTest(b)
                elif type_run=='def_run':
                        if def_name==class_name[1]  and  class_name_new==class_name[0]:
                            suite.addTest(b)
                if type_run=='run_all':
                    statu=0
                    for i in class_name['class_list']:
                        if class_name_new==i:
                            statu=1
                            suite.addTest(b)
                    if statu==0:
                        for i in class_name['def_list']:
                            if def_name == i[0] and class_name_new==i[1]:
                                suite.addTest(b)
    runner = old_htmr.HTMLTestRunner(title='Report_title', description='Report_description', verbosity=2,db_mulu=db_mulu,row_id=row_id)
    resutlt = runner.run(suite)

    # filename = r"C:\jieyuelianhe\old_all_server\ui_test/xxx.html"
    # f = file(filename, 'wb')
    # runner = HTMLTestRunner.HTMLTestRunner(title='Report_title', description='Report_description', verbosity=2)
    # resutlt = runner.run(suite)



    # runner = unittest.TextTestRunner()
    # runner.run(suite)
    cu.execute('UPDATE run_type SET don_or_run=?,done_time=? where id=?',
               ('done',str(time.time()),row_id))
    db.commit()
    db.close()
def run_statu_ui(func):
    def run_statu_ui():
        func()
        db = sqlite3.connect(current_app.config.get('UI_DB'))
        cu = db.cursor()
        detail=cu.execute('select type,run_name,don_or_run from  run_type ').fetchall()
        statu='all_done'
        for i in detail:
            if i[2]=='done':
                pass
            else:
                statu='is_runing'
        if statu=='all_done':
            resp = jsonify(data={})
        else:
           resp=jsonify(data=detail)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return run_statu_ui
def get_case_detail(func):
    def get_case_detail():
        func()
        mulu=request.form['mulu']
        if mulu.strip()=='':
                resp = jsonify(ceshi='不能为空')
                resp.headers['Access-Control-Allow-Origin'] = '*'
                return resp
        else:
            mulu = os.path.normpath(request.form['mulu'])
        db = sqlite3.connect(current_app.config.get('UI_DB'))
        cu = db.cursor()
        cu.execute('delete from run_type where type!="all_run"')
        cu.execute('delete from run_detail')
        db.commit()
        discover = unittest.defaultTestLoader.discover(mulu, pattern='*.py')
        u = {}
        retu = {}
        suite = unittest.TestSuite()
        statu_num_all_case=0
        try:
            for i in discover:
                for z in i:
                    for b in z:
                        statu_num_all_case += 1
                        suite.addTest(b)
                        fangfa_doc = b.shortDescription()
                        class_name = str(b).split('(')[-1].split(')')[0].strip()
                        class_doc = b.__doc__
                        def_name = str(b).split('(')[0]
                        def_doc = b.shortDescription()
                        if class_name not in list(u.keys()):
                            u[class_name] = [{"class_name": class_name, "class_doc": class_doc, "class_suit": z}, {def_name:
                                {
                                    "def_doc": def_doc,
                                    "def_suit": b}}]
                            retu[class_name] = [{"class_name": class_name, "class_doc": class_doc}, {def_name: def_doc}]
                        else:
                            def_detail = {"def_doc": def_doc, "def_suit": b}
                            u[class_name][-1][def_name] = def_detail
                            retu[class_name][-1][def_name] = def_doc
        except Exception as e:
            resp = jsonify(ceshi='导入脚本代码有误', mulu=mulu,type='error')
            session['mulu_detail'] = mulu
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            resp = jsonify(ceshi=retu, mulu=mulu,type='success')
            session['mulu_detail'] = mulu
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    return get_case_detail
def test_all(func):
    def test_all():
        func()
        return jsonify(ajdjiaeja='22222')
    return test_all


def run_log(func):
    def run_log():
        func()
        db = sqlite3.connect(current_app.config.get('UI_DB'))
        cu = db.cursor()
        if  'log_begin_length' not in list(session.keys()):
            session['log_begin_length']=24
        begin_desc='========================================================================\n'
        short_desc='------------------------------------------------------------------------\n'
        if 'success_num' not in list(current_app.config.keys()):
            current_app.config['success_num'] = 0
            current_app.config['fail_num'] = 0
            current_app.config['error_num'] = 0
        if 'ui_now_run_id'  in list(current_app.config.keys()):
            run_detail=cu.execute('select * from run_detail where suite_id="%s" order by end_time asc' % current_app.config['ui_now_run_id']).fetchall()
            if 'run_done_num' not in list(current_app.config.keys()):
                current_app.config['run_done_num']=str(len(run_detail))
                if len(run_detail)!=0:
                    return_desc = ''
                    for i in range(len(run_detail)):
                        if run_detail[0 - 1 - i][6]=='success':
                            current_app.config['success_num']+=1
                        elif run_detail[0 - 1 - i][6]=='fail':
                            current_app.config['fail_num']+=1
                        elif run_detail[0 - 1 - i][6]=='error':
                            current_app.config['error_num']+=1
                        this_desc=begin_desc+run_detail[0 - 1 - i][6].upper()+'       '+run_detail[0 - 1 - i][5]+'('+run_detail[0 - 1 - i][5]+')'+'\n'+short_desc+run_detail[0 - 1 - i][7]
                        return_desc =return_desc+ this_desc
            elif  'run_done_num' in list(current_app.config.keys()) and len(run_detail)>int(current_app.config['run_done_num']):
                return_desc=''
                for i in range(len(run_detail)-int(current_app.config['run_done_num'])):
                    if run_detail[0 - 1 - i][6] == 'success':
                        current_app.config['success_num'] += 1
                    elif run_detail[0 - 1 - i][6] == 'fail':
                        current_app.config['fail_num'] += 1
                    elif run_detail[0 - 1 - i][6] == 'error':
                        current_app.config['error_num'] += 1
                    this_desc = begin_desc + run_detail[0 - 1 - i][6].upper() + '       ' + run_detail[0 - 1 - i][
                        5] + '(' + run_detail[0 - 1 - i][5] + ')' + '\n' + short_desc + run_detail[0 - 1 - i][7]
                    return_desc = return_desc + this_desc
                current_app.config['run_done_num'] = len(run_detail)
            else:
                return_desc=''
        else:
            return_desc = 'no_run'
        if session['log_begin_length']>0:
            if return_desc.count('\n')<session['log_begin_length']:
                return_desc+'\n'*(session['log_begin_length']-return_desc.count('\n'))
                session['log_begin_length']=session['log_begin_length']-return_desc.count('\n')
        resp = jsonify(return_desc=return_desc.replace('\n','<br>').strip(),success_num=current_app.config['success_num'],
                       fail_num=current_app.config['fail_num'],error_num=current_app.config['error_num'])
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return run_log


#获取运行结果信息
def ui_run_result(func):
    def ui_run_result():
        func()
        result_type=request.args.get('type')
        ui_type=request.form['type']
        db = sqlite3.connect(current_app.config.get('UI_DB'))
        cu = db.cursor()
        if result_type=='run_all':
            row_id=cu.execute('select id from run_type where type="%s"' %(ui_type)).fetchall()
            time_detial=cu.execute('select start_time,done_time from run_type where type="%s"' %(ui_type)).fetchall()[0]
            begin_time=time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(float(time_detial[0])))
            taken_time=int(float(time_detial[1]))-int(float(time_detial[0]))
            if len(row_id)==0:
                resp=jsonify(result_detail='未运行case')
            else:
                row_id=row_id[0][0]
                result_detail=cu.execute('select * from run_detail where suite_id="%s"' %(row_id)).fetchall()
                sort_detail={}
                for i in result_detail:
                    if i[5]  not in list(sort_detail.keys()):
                        sort_detail[i[5]]=[i]
                    else:
                        sort_detail[i[5]].append(i)
                for i in sort_detail:
                    if len(sort_detail[i])==0:
                        sort_detail.pop(i)
                resp = jsonify(result_detail=sort_detail,begin_time=str(begin_time),taken_time=str(taken_time))
        elif result_type=='class_all':
            class_name=request.args.get('class_name')
            row_id=cu.execute('select id from run_type where type="class_run_case_all"  and run_name="%s"' %(class_name)).fetchall()
            time_detial=cu.execute('select start_time,done_time from run_type where type="class_run_case_all"  and  run_name="%s" ' %(class_name)).fetchall()[0]
            begin_time=time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(float(time_detial[0])))
            taken_time=int(float(time_detial[1]))-int(float(time_detial[0]))
            if len(row_id)==0:
                resp=jsonify(result_detail='未运行case')
            else:
                row_id=row_id[0][0]
                result_detail=cu.execute('select * from run_detail where suite_id="%s"' %(row_id)).fetchall()
                sort_detail={}
                for i in result_detail:
                    if i[5]  not in list(sort_detail.keys()):
                        sort_detail[i[5]]=[i]
                    else:
                        sort_detail[i[5]].append(i)
                for i in sort_detail:
                    if len(sort_detail[i])==0:
                        sort_detail.pop(i)
                resp = jsonify(result_detail=sort_detail,begin_time=str(begin_time),taken_time=str(taken_time))
        elif result_type=='def_run':
            class_name=request.args.get('class_name')
            def_name=request.args.get('def_name')
            run_name=def_name.strip()+'$'+class_name.strip()
            row_id=cu.execute('select id from run_type where type="def_run"  and run_name="%s"' %(run_name)).fetchall()
            time_detial=cu.execute('select start_time,done_time from run_type where type="def_run"  and  run_name="%s" ' %(run_name)).fetchall()[0]
            begin_time=time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(float(time_detial[0])))
            taken_time=int(float(time_detial[1]))-int(float(time_detial[0]))
            if len(row_id)==0:
                resp=jsonify(result_detail='未运行case')
            else:
                row_id=row_id[0][0]
                result_detail=cu.execute('select * from run_detail where suite_id="%s"' %(row_id)).fetchall()
                sort_detail={}
                for i in result_detail:
                    if i[5]  not in list(sort_detail.keys()):
                        sort_detail[i[5]]=[i]
                    else:
                        sort_detail[i[5]].append(i)
                for i in sort_detail:
                    if len(sort_detail[i])==0:
                        sort_detail.pop(i)
                resp = jsonify(result_detail=sort_detail,begin_time=str(begin_time),taken_time=str(taken_time))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return ui_run_result