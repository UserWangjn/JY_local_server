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
import paramiko
#不是自动打开的页面，可以查看调试信息
def wirte_logs(func):
  def ceshi():
      linux = g.cu.execute(
          'select linux from jie_kou_test where name="%s" and ip="%s"' % (request.form['name'], ip)).fetchall()[0][0]
      linux = eval(linux)
      hostname = linux['ip']
      username = linux['username']
      password = linux['password']
      s = paramiko.SSHClient()
      s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      s.connect(hostname, 22, username, password, timeout=5)
      s.close()
      return 111
  return  ceshi
