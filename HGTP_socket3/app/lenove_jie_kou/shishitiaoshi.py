from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import paramiko
import os
import json
import urllib.request, urllib.error, urllib.parse
import re
import  chardet
import time
import shutil
import sqlite3
import smtplib
from email.mime.text import MIMEText
import urllib.request, urllib.error, urllib.parse
from tempfile import mktemp
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import current_app
from werkzeug.utils import secure_filename
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import datetime
import unittest
import functools
import demjson
def create_result_json(func):
    def create_result_json():
        func()
        if request.form['json_data']!='null'  and request.form['json_data'].strip()!='':
            json_data=json.loads(request.form['json_data'])
            change_json=get_result_json('simple_json',json_data).json
            change_json=json.dumps(change_json,indent=4)
        else:
            change_json='null'
        resp = jsonify(statu='scuess',result_json=change_json)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return create_result_json
class get_result_json(object):
    #第一个参数为，要生成的类型，第二个参数为，结果json字符串
    def __init__(self,type_statu,jsonn_result):
        if type(jsonn_result) not in [dict,list]:
           self.json=json.loads(jsonn_result)
        else:
            self.json=jsonn_result
        self.create(self.json)
    def create(self,json_data):
        if type(json_data) == list:
            for k,i in enumerate(json_data):
                if type(i)  in [dict,list]:
                     self.create(i)
                else:
                    json_data[k]=self.change_data(i)
        elif type(json_data) == dict:
            for i in json_data:
                if type(json_data[i])  in [dict,list]:
                     self.create(json_data[i])
                else:
                    json_data[i]=self.change_data(json_data[i])
    def change_data(self,a):
        if type(a)==int:
            return "*int"
        elif type(a)==int:
            return "*long"
        elif type(a)==str or type(a)==str:
            return "*str"
        elif type(a)==bool:
            return a