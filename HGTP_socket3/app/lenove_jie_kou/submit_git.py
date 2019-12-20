from app import app
from flask import send_from_directory,send_file,Response
import os
import json
import re
import  chardet
import time
import sqlite3
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import demjson
import zipfile,os
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib.request, urllib.error, urllib.parse
import requests
import traceback
def  submit_git(func):
    def submit_git1():
        #验证别人是否在提交中
        request_get= requests.post("http://"+request.form['ip']+":5025/get_sumint_statu")
        if json.loads(request_get.text)['statu']!="success":
            resp = jsonify(statu='fail', detail="传送中，请稍后再试")
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        #压缩文件
        mulu=request.form['mulu']
        for dirpath, dirnames, filenames in os.walk(mulu):
            for file in filenames:
                if os.path.splitext(os.path.join(dirpath, file))[-1] not in ['.xls','.txt']:
                    resp = jsonify(statu='fail', detail="目录包含非接口文件："+os.path.join(dirpath, file))
                    resp.headers['Access-Control-Allow-Origin'] = '*'
                    return resp
        shengcheng_mulu=os.path.join(os.path.dirname(mulu),'git_submit_mulu.zip')
        zip_ya(mulu,shengcheng_mulu)
        if  not os.path.isdir(mulu):
            resp = jsonify(statu='no file')
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        register_openers()
        datagen, headers = multipart_encode({"image1": open(shengcheng_mulu, "rb")})
        headers['mulu']=mulu
        headers['git_address']=request.form['git_address']
        request_server = urllib.request.Request("http://"+request.form['ip']+":5025/get_file_git", datagen, headers)
        result_send= json.loads(urllib.request.urlopen(request_server,timeout=300).read())
        if result_send['statu']=="success":
             resp = jsonify(statu='success',file_path=os.path.join(os.path.dirname(mulu), 'git_submit_mulu.zip'))
        else:
            resp = jsonify(statu='fail',detail=result_send["ouput_detail"],file_path=os.path.join(os.path.dirname(mulu), 'git_submit_mulu.zip'))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return submit_git1
#把整个文件夹内的文件打包成zip文件（包括压缩路径下的字文件夹的文件）
# 第一个参数是要压缩的文件目录，第二个参数是生成的zip文件保存的目录
def zip_ya(startdir,file_news):
    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
    z.close()
def banben_data(func):
    def banben_data():
        func()
        resp = jsonify(statu=float(current_app.config.get('BANBEN_NUM')))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return banben_data
#上传文件成功后，回调函数，删除文件
def delete_local_file_save(func):
    def delete_local_file_save():
        func()
        time.sleep(1)
        try:
           os.remove(request.form['file_path'])
        except Exception as err:
            print(traceback.format_exc())
            print(err)

        resp = jsonify(statu="success")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return delete_local_file_save
if __name__=='__main__':
    get_files_path = r'C:\Users\sunzhen\Desktop\test\222'
    set_files_path = r"test.zip" #存放的压缩文件地址(注意:不能与上述压缩文件夹一样)
    zip_ya(get_files_path,set_files_path)