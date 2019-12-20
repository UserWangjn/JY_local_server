#根据列表执行运行文件
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import os
import time
import traceback
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
from  jie_kou_test.pi_run.pi_run  import *
from  jie_kou_test.pi_run import all_run

import configparser

sys.path.append(r'C:\exec\jie_kou_test')
#不是自动打开的页面，可以查看调试信息
def jiekou_list_show(func):
  def jiekou_list_showee():
      func()
      if request.method == 'GET':
          #从数据库中获取目录信息
          db = sqlite3.connect(current_app.config.get('JIE_KOU'))
          cu = db.cursor()
          if  'gen_mulu' not in session:
              gen_mulu=cu.execute('select  mulu from jiekou_mulu where ip=? and statu=?',(request.remote_addr, '批量')).fetchall()
              if len(gen_mulu)>0:
                  gen_mulu=gen_mulu[0][0]
              else:
                  gen_mulu=''
          else:
              gen_mulu=session['gen_mulu']
          db.close()
          # 业务文件名
          if request.remote_addr + 'all_url' in session:
              re_all_mulu=session[request.remote_addr + 'all_url']
          else:
              re_all_mulu=""
          if gen_mulu!='':
              yewu_name = {}
              #需要跳转的环境
              huanjing=[os.path.join(current_app.config.get('JIE_KOU_URL'),i.decode('gb2312'))for i in os.listdir(current_app.config.get('JIE_KOU_URL'))
                        if i.strip()!='' and 'git' not in i]
              if 'value' in  list(request.args.keys()):
                  for i in huanjing:
                      if request.args.get('value')==os.path.basename(i):
                              session['jie_kou_huan_jing']=i
              else:
                  if 'jie_kou_huan_jing' in list(session.keys()):
                      pass
                  else:
                      try:
                         value = os.listdir(os.path.join(session['jie_kou_huan_jing'], filename))
                      except Exception as err:
                          print(traceback.format_exc())
                          print(err)

                      yewu_name[filename] = [i for i in os.listdir(os.path.join(session['jie_kou_huan_jing'], filename)) if '__init__' not in i and '.git' not in i]
              huanjing_list =[i.decode('gb2312') for i in os.listdir(current_app.config.get('JIE_KOU_URL')) if
                   i.strip() != '' and 'git' not in i]
              huanjing_list.remove(os.path.basename(session['jie_kou_huan_jing']))
          else:
              yewu_name=''
              select_huanjing=''
              huanjing=''
              huanjing_list=''
          return render_template('/hualala/pages/jiekou_list.html', yewu_name=yewu_name,select_huanjing=os.path.basename(session['jie_kou_huan_jing']),
                                 huanjing=huanjing_list,all_mulu=re_all_mulu,gen_mulu=gen_mulu
                                 )
  return jiekou_list_showee
def jiekou_result_run(func):
    def result_run():
        func()
        if request.method=="POST":
            all_url=[]
            ip=request.remote_addr
            huanjing = [os.path.join(current_app.config.get('JIE_KOU_URL'), i.decode('gb2312')) for i in
                        os.listdir(current_app.config.get('JIE_KOU_URL'))
                        if i.strip() != '' and 'git' not in i]
            if 'jie_kou_huan_jing' in list(session.keys()):
                pass
            else:
                session['jie_kou_huan_jing'] = huanjing[0]
            url=session['jie_kou_huan_jing']
            all_req=[z.split('#')  for z in request.form['ame'].split(',') if z.strip()!='']
            for i in all_req:
                             all_url.append(os.path.join(os.path.join(url, i[0]),i[1]))
            all_run.run(all_url, r'C:\work\lenove_jie_kou',ip)
            error='1'
            """
            try:
                all_run.run(all_url, r'C:\work\lenove_jie_kou')
            except Exception,e:
                error=e
                """
            return jsonify(a=str(error))
    return result_run

#脚本输入测试信息
import chardet
def jiaobenshuru(func):
    def zz():
        if request.method=='POST':
            ip=request.remote_addr
            db = sqlite3.connect(current_app.config.get('JIE_KOU'))
            cu = db.cursor()
            current_app.config[request.remote_addr+'last_change']=request.form
            name = request.form['name']
            data=json.dumps(request.form)
            if len(cu.execute('select * from  jie_kou_test WHERE num=? and ip=?', ('run',request.remote_addr)).fetchall())==0:
                cu.execute('insert into jie_kou_test values (?,?,?,?,?,?,?,?) ', ('run', name, 'null',data,'null', request.remote_addr,'null',str(time.time())))
            else:
                cu.execute('UPDATE jie_kou_test SET name=?,data=? WHERE num=? and ip=?', (name, data,'run',request.remote_addr))
            db.commit()
            return jsonify(da=1)
    return zz
#接口url 插入数据库
def url_insert(func):
    def hk():
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        if len(cu.execute('select * from jiekou_mulu where ip=? and statu=?',(request.remote_addr,request.args.get('statu'))).fetchall())>0:
            cu.execute('update jiekou_mulu set mulu=?,update_time=? where ip=? and statu=?',(request.args.get('mulu'),str(time.time()),request.remote_addr,request.args.get('statu')))
        else:
          cu.executemany('INSERT INTO jiekou_mulu VALUES (null,?,?,?,?)',
                       [(request.args.get('statu'), request.args.get('mulu'),request.remote_addr, str(time.time()))])
        db.commit()
        db.close()
        session['调试']=request.args.get('mulu')
        return jsonify(statu="success")
    return hk
#本地server 获取要监控的目录地址
def get_mulua(func):
    @wraps(func)
    def hk():
        if '调试' in session:
            mulu=session['调试']
        else:
            db = sqlite3.connect(current_app.config.get('JIE_KOU'))
            cu = db.cursor()
            mulu=cu.execute('select mulu from jiekou_mulu where ip=? and statu=?',(request.remote_addr,request.form['statu'])).fetchall()
            db.close()
        return jsonify(mulu=mulu)
    return hk
#返回调试首页
import xlrd
import sys
sys.path.append(os.path.dirname(os.path.dirname(sys.argv[0])))
from app.jie_kou_test.run import *
def shishitiaoshi(func):
    @wraps(func)
    def aa():
        try:
            current_app.config['jiankong_mulu']
        except Exception as err:
            print(traceback.format_exc())
            print(err)

            current_app.config['jiankong_mulu'] = ''
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        path=current_app.config['jiankong_mulu']
        error_code='null'
        #验证配置文件是否出现格式错误
        error_statu=''
        if current_app.config['jiankong_mulu'].strip()!='':
             gen_mulu=os.path.dirname(current_app.config['jiankong_mulu'])
             #读取db配置文件
             conf = configparser.ConfigParser()
             if os.path.isfile(os.path.join(gen_mulu,'db.txt')):
                 try:
                     conf.read(os.path.join(gen_mulu,'db.txt'))
                 except Exception as err:
                     print(traceback.format_exc())
                     print(err)
                     error_statu='db.txt配置错误'
             if not os.path.isfile(os.path.join(gen_mulu,'config.txt')):
                 error_statu = error_statu+'#'+'config.txt公共配置文件不存在'
             if os.path.isfile(os.path.join(gen_mulu,'config.txt')):
                 try:
                     conf.read(os.path.join(gen_mulu,'config.txt'))
                 except Exception as err:
                     print(traceback.format_exc())
                     print(err)
                     error_statu=error_statu+'#'+'config.txt公共配置文件错误'
             if not os.path.isfile(os.path.join(current_app.config['jiankong_mulu'],'configparse.txt')):
                 error_statu = error_statu+'#'+'configparse.txt接口配置文件不存在'
             if os.path.isfile(os.path.join(gen_mulu,'configparse.txt')):
                 try:
                     conf.read(os.path.join(gen_mulu,'configparse.txt'))
                 except Exception as err:
                     print(traceback.format_exc())
                     print(err)
                     error_statu=error_statu+'#'+'config.txt接口配置文件错误'
             if not os.path.isfile(os.path.join(current_app.config['jiankong_mulu'],'json.txt')):
                 error_statu = error_statu+'#'+'json.txt接口模板文件不存在'
             if os.path.isfile(os.path.join(current_app.config['jiankong_mulu'],'json.txt')):
                 json_data=open(os.path.join(current_app.config['jiankong_mulu'],'json.txt'),'r+')
                 data=json_data.read()#z.decode('gb2312')
                 if data.strip()!='':
                     json.loads(data)
                     try:
                         json.loads(data)
                     except Exception as err:
                         print(traceback.format_exc())
                         print(err)
                         error_statu = error_statu + '#' + 'json.txt接口模板json解析错误'
        if error_statu!='':
            resp = jsonify(error_statu=error_statu)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        if  path != '':
            if os.path.isdir(path):
                path = path
                # self.h = webdriver.Chrome()
                time.sleep(3)
                url = ''
                # self.h.get('http://127.0.0.1:5021/ceshi')
                # self.send = confi(path,self.h)
                excel_name = os.path.basename(path)
                for dir, b, file in os.walk(path):
                    # 返回表格路径
                    for z in file:
                        if excel_name in z:
                            excel_path = os.path.join(path, z)
                try:
                   data = xlrd.open_workbook(excel_path)
                except Exception as err:
                    print(traceback.format_exc())
                    print(err)

                table = data.sheets()[0]
                key = table.row_values(0)
                data = [table.row_values(i) for i in range(1, table.nrows)]
                try:
                    current_app.config['excel_data_last']
                except Exception as err:
                    print(traceback.format_exc())
                    print(err)
                    current_app.config['excel_data_last']=data
                # self.creat_json(open(self.dir[1]).read())
                change = {}
                if data != current_app.config['excel_data_last']:
                    send = confi(path, session)
                    session['tiaoshi_error_statu']=''
                    # 增加数据行
                    if len(data) != len(current_app.config['excel_data_last']):
                        current_app.config['excel_data_last'] = data
                        # 判断是否包含url字段
                        data = dict(list(zip(key, data[-1])))
                        yongli_name = data['Comment']
                        if data['result'].strip() == '':
                            data['result'] = '{}'
                        #判断断言json是否正确
                        # 判断是否包含before_request,若包含则替换
                        try:
                            json.loads(data['result'])
                        except Exception as err:
                            print(traceback.format_exc())
                            print(err)

                            error_statu='断言json解析错误'
                            resp = jsonify(error_statu=error_statu)
                            resp.headers['Access-Control-Allow-Origin'] = '*'
                            return resp
                        # 调用前置接口返回的是最近的前置接口返回的json字符串
                        if 'global_data' in list(data.keys()) and data['global_data'].strip() != '':
                            set_global_data().set_global_data(data, send.config_path, path,
                                                              {})
                        if 'before_request' in list(data.keys()):
                            try:
                                k = change_request_before()
                                k.use(data,path,send.config_path)
                            except Exception as err:
                                print(traceback.format_exc())
                                print(err)

                                error_statu = '前置接口运行错误'
                                session['tiaoshi_error_statu']=error_statu
                                resp = jsonify(error_statu=error_statu)
                                resp.headers['Access-Control-Allow-Origin'] = '*'
                                return resp
                        for k, i in enumerate(data.keys()):
                            try:
                                if int(i) == float(i):
                                    data[k] = str(int(i))

                            except Exception as err:
                                print(traceback.format_exc())
                                print(err)

                            if type(i) == float:
                                data[int(i)] = data.pop(i)
                                # 判断是否有包含#的字段若果则执行python代码
                        for i in data:
                            if '##' in str(data[i]):
                                s = excel_data_exe()
                                data[i] = s.han_shu(data[i])
                                # 生成json字符串
                        if 'url' in list(data.keys()) and data['url'].strip() != '':
                            url = send.config_path.get('config','public_url')+data['url']

                        change_json_data(json.loads(open(send.json_path).read()), data)
                        if  data['result']!='':
                            result_data=json.loads(excel_data.change_data_db(send.config_path, data.pop('result')).data)
                        else:
                            result_data=''
                        data = json.loads(excel_data.change_data_db(send.config_path, data).data)
                        data['result'] = result_data
                        send.all_send(data, url)
                    # 修改数据行值
                    else:
                        for k, i in enumerate(data):
                            if data[k] != current_app.config['excel_data_last'][k]:
                                current_app.config['excel_data_last'] = data
                                # 获取改变了信息的行信息字典形式
                                data = dict(list(zip(key, data[k])))
                                if data['result'].strip() == '':
                                    data['result'] = '{}'
                                try:
                                    json.loads(data['result'])
                                except Exception as err:
                                    print(traceback.format_exc())
                                    print(err)
                                    error_statu = '断言json解析错误'
                                    session['tiaoshi_error_statu'] = error_statu
                                    resp = jsonify(error_statu=error_statu)
                                    resp.headers['Access-Control-Allow-Origin'] = '*'
                                    return resp
                                # 调用前置接口返回的是最近的前置接口返回的json字符串
                                if 'global_data' in list(data.keys()) and data['global_data'].strip() != '':
                                    set_global_data().set_global_data(data, send.config_path, path, {})
                                if 'before_request' in list(data.keys()):
                                    k = change_request_before()
                                    k.use(data, path,send.config_path)
                                # 判断是否包含url字段
                                # 调用查询价格单接口
                                # self.query_data=self.query.just_reque(self.data)
                                # self.s=json.loads(self.query_data)['result']['data'][0]['barcode']
                                # self.data['apiSign']=self.s
                                # 读取excel有可能将数字键变为flaot，因此要将float键变成str整形
                                for k, i in enumerate(data.keys()):
                                    try:
                                        if int(i) == float(i):
                                            data[k] = str(int(i))

                                    except Exception as err:
                                        print(traceback.format_exc())
                                        print(err)

                                    if type(i) == float:
                                        data[int(i)] = data.pop(i)
                                #判断是否可以转为float如果可以，判断小叔掉后面是否都是0如果是则删除小数点后面的
                                # 判断是否有包含#的字段若果则执行python代码
                                for i in data:
                                    if type(data[i]) not in [float,int,bool]  and  '##' in data[i]:
                                        s = excel_data_exe()
                                        data[i] = s.han_shu(data[i])
                                # 生成json字符串,里面有调用其他接口，将数据存入数据库
                                if 'url' in list(data.keys()) and data['url'].strip() != '':
                                    url = send.config_path.get('config', 'public_url') + data['url']
                                change_json_data(json.loads(open(send.json_path).read().decode('GB2312')), data)
                                if data['result'] != '':
                                    result_data = json.loads(
                                        excel_data.change_data_db(send.config_path, data.pop('result')).data)
                                data = json.loads(excel_data.change_data_db(send.config_path, data).data)
                                data['result'] = result_data
                                send.all_send(data, url)
                                break
                    save_data_config(data, path, send.config_path, data['result'])
                    name = send.run_result['name']
                    if len(cu.execute('select * from  jie_kou_test WHERE num=? and ip=?', ('run', request.remote_addr)).fetchall()) == 0:
                        cu.execute('insert into jie_kou_test values (?,?,?,?,?,?,?,?) ', ('run', name, 'null', json.dumps(send.run_result), 'null', request.remote_addr, 'null', str(time.time())))
                    else:
                        cu.execute('UPDATE jie_kou_test SET name=?,data=? WHERE num=? and ip=?',
                                   (name, json.dumps(send.run_result), 'run', request.remote_addr))

        db.commit()
        if 'ip_data'  in request.args:
            request_ip=request.args.get('ip_data')
        else:
            request_ip=request.remote_addr
        if len(cu.execute('select * from jie_kou_test where num=? and ip=?',("run",request_ip)).fetchall())==0:
            data=json.dumps({'comment':'null','resulte':'null','name':'null','assert':'null','request':'null'})
        else:
            data=cu.execute('select * from jie_kou_test where num=? and ip=?',("run",request_ip)).fetchall()[0][3]
                        #data=current_app.config[request.remote_addr+'last_change']
        data=json.loads(data)
        db.close()
        case_name=data['comment']
        if len(data['request'])==0:
            shuru=str(data['request'])
        else:
           shuru=json.dumps(json.loads(json.dumps(demjson.decode(data['request'])), parse_int=int), indent=4, sort_keys=False,
                                   ensure_ascii=False)
        if len(data['resulte'])==0:
            shuchu=str(data['resulte'])
        else:
            shuchu=json.dumps(json.loads(json.dumps(demjson.decode(data['resulte'])), parse_int=int), indent=4, sort_keys=False,
                                   ensure_ascii=False)
        jiekou_name=data['name']
        result_statu=str(data['assert'])
        if 'request_url'  not in list(data.keys()):
            request_url=""
        else:
            request_url=data['request_url']
        simple_assert=create_result_json(shuchu)
        if 'tiaoshi_error_statu' not in list(session.keys()) or  session['tiaoshi_error_statu']=='':
           resp=jsonify(error_statu=error_statu,case_name=case_name,shuru=shuru,shuchu=shuchu,jiekou_name=jiekou_name,result_statu=result_statu,request_url=request_url,simple_assert=simple_assert)
        else:
            resp= jsonify(error_statu=session['tiaoshi_error_statu'])
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return aa

#实时调试，new
def shishitiaoshi_new(func):
    @wraps(func)
    def aa():
        try:
            current_app.config['jiankong_mulu']

        except Exception as err:
            print(traceback.format_exc())
            print(err)

            current_app.config['jiankong_mulu'] = ''
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        path=current_app.config['jiankong_mulu']
        error_code='null'
        #验证配置文件是否出现格式错误
        error_statu=''
        if current_app.config['jiankong_mulu'].strip()!='':
             gen_mulu=os.path.dirname(current_app.config['jiankong_mulu'])
             #读取db配置文件
             conf = configparser.ConfigParser()
             if os.path.isfile(os.path.join(gen_mulu,'db.txt')):
                     try:
                         conf.read(os.path.join(gen_mulu,'db.txt'))
                     except:
                        error_statu='db.txt配置错误'
             if not os.path.isfile(os.path.join(gen_mulu,'config.txt')):
                 error_statu = error_statu+'#'+'config.txt公共配置文件不存在'
             if os.path.isfile(os.path.join(gen_mulu,'config.txt')):
                     try:
                         conf.read(os.path.join(gen_mulu,'config.txt'))
                     except:
                        error_statu=error_statu+'#'+'config.txt公共配置文件错误'
             if not os.path.isfile(os.path.join(current_app.config['jiankong_mulu'],'configparse.txt')):
                 error_statu = error_statu+'#'+'configparse.txt接口配置文件不存在'
             if os.path.isfile(os.path.join(gen_mulu,'configparse.txt')):
                     try:
                         conf.read(os.path.join(gen_mulu,'configparse.txt'))
                     except:
                        error_statu=error_statu+'#'+'config.txt接口配置文件错误'
             if not os.path.isfile(os.path.join(current_app.config['jiankong_mulu'],'json.txt')):
                 error_statu = error_statu+'#'+'json.txt接口模板文件不存在'
             if os.path.isfile(os.path.join(current_app.config['jiankong_mulu'],'json.txt')):
                     json_data=open(os.path.join(current_app.config['jiankong_mulu'],'json.txt'),'r+')
                     data=json_data.read()#.decode('gb2312')
                     if data.strip()!='':
                         json.loads(data)
                         try:
                             json.loads(data)
                         except:
                             error_statu = error_statu + '#' + 'json.txt接口模板json解析错误'
        if error_statu!='':
            resp = jsonify(error_statu=error_statu)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        if  path != '':
                if os.path.isdir(path):
                    path = path
                    # self.h = webdriver.Chrome()
                    time.sleep(3)
                    url = ''
                    # self.h.get('http://127.0.0.1:5021/ceshi')
                    # self.send = confi(path,self.h)
                    excel_name = os.path.basename(path)
                    for dir, b, file in os.walk(path):
                        # 返回表格路径
                        for z in file:
                            if excel_name in z:
                                excel_path = os.path.join(path, z)
                    try:
                       data = xlrd.open_workbook(excel_path)
                    except:
                        pass
                    table = data.sheets()[0]
                    key = table.row_values(0)
                    data = [table.row_values(i) for i in range(1, table.nrows)]
                    try:
                        current_app.config['excel_data_last']
                    except:
                         current_app.config['excel_data_last']=data
                    # self.creat_json(open(self.dir[1]).read())
                    change = {}
                    # print  77777777777777777777777
                    # s = all_run.run([current_app.config['jiankong_mulu']], time.time(), '127.0.0.1',
                    #                 '192.168.33.216', 1).simple_result
                    # print  99999999999999999999999999999999999999999999
                    # print s
                    if data != current_app.config['excel_data_last'] :
                       if  "'shishitiaoshi_statu'" not in list(current_app.config.keys()) or current_app.config[
                            'shishitiaoshi_statu'] != "running":
                                current_app.config['shishitiaoshi_statu']="running"
                                # # 增加数据行
                                # if len(data) != len(current_app.config['excel_data_last']):
                                #     current_app.config['excel_data_last'] = data
                                #     # 判断是否包含url字段
                                if len(data) != len(current_app.config['excel_data_last']):
                                           current_app.config['excel_data_last'] = data
                                           data = dict(list(zip(key, data[-1])))
                                           try:
                                               simple_result=all_run.run([current_app.config['jiankong_mulu']],time.time(),'127.0.0.1','127.0.0.1',int(data['id'])).simple_result
                                               #logger.debug(simple_result)
                                           except:
                                               simple_result = json.dumps({
                                                   "1": {
                                                       "req": None,
                                                       "case_assert": None,
                                                       "case_name": None,
                                                       "assert_result": None,
                                                       "respons": {
                                                           "运行出错": "运行出错,请排除错误重新修改excel表格数据"},
                                                       "req_url": None
                                                   }
                                               })

                                # 修改数据行值
                                else:
                                    for k, i in enumerate(data):
                                     if data[k] != current_app.config['excel_data_last'][k]:
                                        current_app.config['excel_data_last'] = data
                                        # 获取改变了信息的行信息字典形式
                                        data = dict(list(zip(key, data[k])))
                                        # if data['result'].strip() == '':
                                        #     data['result'] = '{}'
                                        # try:
                                        #     json.loads(data['result'])
                                        # except:
                                        #     error_statu = u'断言json解析错误'
                                        #     session['tiaoshi_error_statu'] = error_statu
                                        #     resp = jsonify(error_statu=error_statu)
                                        #     resp.headers['Access-Control-Allow-Origin'] = '*'
                                        #     return resp
                                        try:
                                            simple_result=all_run.run([current_app.config['jiankong_mulu']], time.time(), '127.0.0.1',
                                                                      '127.0.0.1', int(data['id'])).simple_result
                                        except:
                                            simple_result = json.dumps({
                                                "1": {
                                                    "req": None,
                                                    "case_assert": None,
                                                    "case_name": None,
                                                    "assert_result": None,
                                                    "respons": {
                                                        "运行出错": "运行出错,请排除错误重新修改excel表格数据"},
                                                    "req_url": None
                                                }
                                            })
                                        break
                                current_app.config['shishitiaoshi_statu'] = "done"
                                simple_result=list(json.loads(simple_result).values())[0]
                                name = os.path.basename(path)
                                simple_result={'comment': simple_result['case_name'], 'resulte': simple_result['respons'], 'name': name, 'assert': simple_result['assert_result'],
                                 'request': simple_result['req'],'request_url':simple_result['req_url']}
                                if len(cu.execute('select * from  jie_kou_test WHERE num=? and ip=?',
                                                  ('run', request.remote_addr)).fetchall()) == 0:
                                    cu.execute('insert into jie_kou_test values (?,?,?,?,?,?,?,?) ',
                                               ('run', name, 'null', json.dumps(simple_result), 'null', request.remote_addr, 'null',
                                                str(time.time())))
                                else:
                                    cu.execute('UPDATE jie_kou_test SET name=?,data=? WHERE num=? and ip=?',
                                               (name, json.dumps(simple_result), 'run', request.remote_addr))

        db.commit()
        if 'ip_data'  in request.args:
            request_ip=request.args.get('ip_data')
        else:
            request_ip=request.remote_addr
        if len(cu.execute('select * from jie_kou_test where num=? and ip=?',("run",request_ip)).fetchall())==0:
                            data=json.dumps({'comment':'null','resulte':'null','name':'null','assert':'null','request':'null'})
        else:
                          data=cu.execute('select * from jie_kou_test where num=? and ip=?',("run",request_ip)).fetchall()[0][3]
                        #data=current_app.config[request.remote_addr+'last_change']
        data=json.loads(data)
        db.close()
        case_name=data['comment']
        if len(data['request'])==0:
            shuru=str(data['request'])
        else:
           shuru=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(data['request']))), parse_int=int), indent=4, sort_keys=False,
                                   ensure_ascii=False)
        if len(data['resulte'])==0:
            shuchu=str(data['resulte'])
        else:
            shuchu=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(data['resulte']))), parse_int=int), indent=4, sort_keys=False,
                                   ensure_ascii=False)
        jiekou_name=data['name']
        result_statu=str(data['assert'])
        if 'request_url'  not in list(data.keys()):
            request_url=""
        else:
            request_url=data['request_url']
        simple_assert=create_result_json(shuchu)
        if 'tiaoshi_error_statu' not in list(session.keys()) or  session['tiaoshi_error_statu']=='':
           resp=jsonify(error_statu=error_statu,case_name=case_name,shuru=shuru,shuchu=shuchu,jiekou_name=jiekou_name,result_statu=result_statu,request_url=request_url,simple_assert=simple_assert)
        else:
            resp= jsonify(error_statu=session['tiaoshi_error_statu'])
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return aa
#批量运行接口
def piliang_run(func):
    @wraps(func)
    def ceshipi():
        session['run_time'] = str(time.time())
        ip = request.remote_addr
        all_mulu=json.loads(request.form['all_jiekou_re'])['all_mulu']
        for k,i in enumerate(all_mulu):
            if request.remote_addr + 'all_url' in session:
                gen_mulu=session[request.remote_addr + 'all_url']
            else:
                gen_mulu=request.form['gen_mulu']
            all_mulu[k]=os.path.join(gen_mulu,request.form['huanjing'],i.split('#')[0],i.split('#')[1])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if ip == "127.0.0.1":
            ip = '192.168.137.1'
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        #把实时运行信息清空
        cu.execute('delete from jiekou_result where ip="%s"' % ip)
        db.commit()
        #把运行信息插入数据库
        for i in all_mulu:
             cu.executemany('INSERT INTO  jiekou_result values (?,?,?,?,null)', [(i,ip,'',session['run_time'])])
        db.commit()
        db.close()
        s.connect((ip, 8065))
        s.send('piliang_run')
        b = s.recv(1024)
        if b == 'ready to run':
            s.send(json.dumps({'all_jiekou':all_mulu,'huanjing':request.form['huanjing'],'run_time':session['run_time']}))
        return jsonify(data='success')
    return ceshipi

#获取后端发过来的本地批量运行的结果并存入数据库中
def  piliang_run_resulttt(func):
    @wraps(func)
    def piliang_run_result1():
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        data=request.form['result']
        time=request.form['time']
        name=request.form['jeikou_name']
        ip = request.remote_addr
        if ip == "127.0.0.1":
            ip = '192.168.137.1'
        name=[ i[0] for i in cu.execute('select name from jiekou_result  where ip="%s" and time="%s"'  % (ip,time)).fetchall() if os.path.basename(i[0])==name][0]
        cu.executemany('update  jiekou_result  set data=? where time=? and name=?',
                       [(data,time,name)])
        db.commit()
        db.close()
        return jsonify(statu='success')
    return piliang_run_result1

#从数据库中拉取数据，生成批量测试结果
def run_jiekou(func):
  def ceshi():
    func()
    ip = request.remote_addr
    if request.method == "GET":
        #根据ip地址读取测试数据
        g.cu.execute('select * from  jiekou_result where ip=?', (ip,))
        data = g.cu.fetchall()
        tim=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(data[-1][-1])))
        all=[]
        if len(data)!=0:
             for i in data:
                 name=i[0]
                 detail=[]
                 statu=0
                 count=len(eval(i[2]))
                 fail=0
                 succ=0
                 for k,z in eval(i[2]).items():
                     z=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(z))), parse_int=int), indent=4, sort_keys=False,
                  ensure_ascii=False)
                     result,id,comment,req=k.split('jo.in')
                     req=json.loads(req)
                     req = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(req))), parse_int=int), indent=4,
                                    sort_keys=False,
                                    ensure_ascii=False)
                     if s_assert.walk_find(json.loads(result),json.loads(z))==False:
                         statu=1
                         fail+=1
                         detail.append(["failCase",id.split('.')[0],comment,result,z,req])
                     else:
                         succ+=1
                         detail.append(["passCase", id.split('.')[0], comment, result,z,req])
                 detail=sorted(detail,key=lambda x:x[1])
                 if statu==1:
                         all.append([name,"failClass",[count,succ,fail,count],detail])
                 elif statu==0:
                         all.append([name,"passClass", [count, succ, fail, count], detail])

        #z中元素第一个接口名字，第二个接口的count，第三个用例状态，最后一个列表d第一个为用例状态，第二个用例id，第三个用例comment，第四个用例的接口数据
        return render_template('/result/test_result.html',z=all,time=tim)
  return ceshi

#返回接口批量运行页面
def jiekou_piliang(func):
    @wraps(func)
    def ceshizhong():
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        jiekou_db=sqlite3.connect(current_app.config.get('JIE_KOU'))
        jiekou_cu = jiekou_db.cursor()
        name = cu.execute(
            'select name from user where ip="%s" order by time desc limit 0,1' % request.remote_addr).fetchall()
        if len(name) == 0:
            return redirect(url_for('login_new'))
        else:
            name = name[0][0]
        if request.method == 'GET':
            git_detail = [list(i) for i in jiekou_cu.execute('select * from git_detail  ').fetchall()]
            for i in git_detail:
                i[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[3])))
            email_detail = [i[0] for i in
                            cu.execute('select address from email_address where user="%s"' % (name)).fetchall()]
            fajianren = [i[0] for i in db.execute('select email_user from fajianren where name="%s"' % name).fetchall()]
            dingshi_detail = [[i[1], i[2], i[4], i[6]] for i in cu.execute(
                'select * from dingshi_run where name="%s" order by update_time desc ' % (name)).fetchall()]
            jobs = [i[0] for i in db.execute('select job_name from jekins where name="%s"' % name).fetchall()]
            for k, i in enumerate(dingshi_detail):
                i.insert(0, i[0])
                i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
                if i[-2].strip() == '0':
                    i[-2] = 'ready'
                elif i[-2].strip() == '1':
                    i[-2] = 'running'
                elif i[-2].strip() == '2':
                    i[-2] = 'over'
            time_date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
            server_detail = [i[1] for i in cu.execute('select * from all_server where statu="1"').fetchall()]
            db.close()
            jiekou_db.commit()
            jiekou_db.close()
            return render_template('/hualala/pages/jiekou_page.html', git_detail=git_detail, email_detail=email_detail,
                                   time_date=time_date, dingshi_detail=dingshi_detail, fajianren=fajianren, jobs=jobs,
                                   server_detail=server_detail)
        else:
            git_url = request.form['git'].strip()
            git_beizhu = request.form['beizu'].strip()
            git_branch = request.form['branch'].strip()
            if git_url.strip() != '' and git_beizhu.strip() != '':
                jiekou_cu.executemany('INSERT INTO git_detail VALUES (?,?,?,?,?,?)',
                               [(git_url, git_beizhu, name, str(time.time()), '', git_branch)])
                db.commit()
                jiekou_db.commit()
                jiekou_db.close()
                db.close()
            return jsonify(a='1')
    return ceshizhong
def delete_shsihitiaoshi(func):
    def delete_shsihitiaoshi():
        func()
        jiekou_db=sqlite3.connect(current_app.config.get('JIE_KOU'))
        jiekou_cu = jiekou_db.cursor()
        jiekou_cu.execute('delete from  jie_kou_test')
        jiekou_db.commit()
        jiekou_db.close()
        return jsonify(statu='delete_success')
    return delete_shsihitiaoshi



#自动生成json断言

def create_result_json(json_data):
        if json_data!='null'  and json_data.strip()!='':
            json_data=json.loads(json_data)
            change_json=get_result_json('simple_json',json_data).json
            change_json=json.dumps(change_json,indent=4)
        else:
            change_json='null'
        return change_json
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