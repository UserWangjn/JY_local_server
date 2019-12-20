import chardet
import hashlib
import requests
import sys
import time
import traceback
sys.path.append("../../")
import copy
import urllib.request, urllib.error, urllib.parse, urllib.error
#from ..sing_data.gdaxMain import CoinbaseExchangeAuth
from app.jie_kou_test.sing_data.sing_data import *
from app.jie_kou_test.sing_data.sing_xiangqian import hengfeng_w_sing
from app.jie_kou_test.json_pi_pei.excel_data import *
from app.jie_kou_test.json_pi_pei.json_pi_pei import *
#from ....header import make_head

import json
class request_run(object):
    def __init__(self,json_moban,path,mu_lu):
        self.json_moban=json_moban
        self.path=path
        if 'run_interval' in self.path.options('sign'):
            try:
                time.sleep(float(self.path.get('sign','run_interval')))
            except Exception as err:
                print(traceback.format_exc())
                print(err)
        self.url=self.path.get('config','url')
        self.config=dict(self.path.items('config'))
        self.sign=dict(self.path.items('sign'))
#        self.public_url=self.url.split(self.path.get('sign','url'))[0]
        #从配置文件替换数据
    #paymax post请求
    def post_run(self,data,*url):
        self.data = data
        if len(url)!=0:
            self.sign_url=url[0].split(self.public_url)[-1]
            self.url=url[0]
            head = make_head(self.sign_url, self.sign['app_key'], data, self.config['method'], self.path)
        else:
            head = make_head(self.path.get('sign','url'), self.sign['app_key'], data, self.config['method'], self.path)
        try:
            response = requests.post(url=self.url, data=self.data, headers=head,verify=False)
        except Exception as err:
            print(traceback.format_exc())
            print(err)
            response = requests.post(url=self.url, data=self.data, headers=head,verify=False)
        return response
    #paymax  get 请求
    def get_run(self,data,*url):
        #生成全部self.url
        if str(data).strip()!='':
           if len(url)!=0:
               url = url[0] + '?' + urllib.parse.urlencode(eval(data)).encode(encoding='utf-8')
           else:
                 url = self.url+'?'+urllib.parse.urlencode(eval(data)).encode(encoding='utf-8')
        else:
            if len(url) == 0:
                url = self.url + '?' + urllib.parse.urlencode(eval(data)).encode(encoding='utf-8')
            else:
                url=url[0]
        self.sign_url=url.split(self.config['url'].split(self.sign['url'])[0])[-1]
        head = make_head(self.sign_url, self.sign['app_key'], data, self.config['method'],self.path)
        response = requests.get(url=url, headers=head,verify=False)
        return response
    #普通post请求
    def post(self, data, config, *url):
        data = json.loads(change_data_db(config, data).data)
        json_change(copy.deepcopy(self.json_moban), data)
        if isinstance(data, dict):
            data = json.dumps(data)
        #data = creat_json(copy.deepcopy(self.json_moban), data)
        if 'sign_type' not in dict(self.path.items('sign')) or self.path.get('sign', 'sign_type')=='web_nosign':
            head_data={config.get('config', 'head_key'):config.get('config', 'head_value')}
            parm = json.loads(data)
            parm['api_key']=config.get('sign', 'api_key')
            parm['sign']=buildMySign(parm,config.get('sign', 'secretKey'))
            parm['api_key']=config.get('sign', 'api_key')
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons = requests.post(url=all_url, data=parm, headers=head_data,verify=False).text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type')=='v3':
            auth=CoinbaseExchangeAuth(config.get('sign', 'api_key'), config.get('sign', 'secretKey'),self.path.get('sign', 'password'))
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            respons = requests.post(url=all_url, json=parm, auth=auth).text
        if self.path.get('sign', 'sign_type')=='Backstage_web':
            parm = json.loads(data)
#            #logger.debug(str(self.path.get('login','token')))
            header={'Authorization':self.path.get('login','token'),'Content-type':'application/json'}
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type'  in self.path.options('config') and self.path.get('config','request_type').strip()=='form_data':
                    header['Content-Type'] = 'application/x-www-form-urlencoded'
                    request = urllib.request.Request(all_url, urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                    respons = urllib.request.urlopen(request, timeout=60).read()
                else:
                    request = urllib.request.Request(all_url,json.dumps(parm), headers=header)
                    respons = urllib.request.urlopen(request,timeout=60).read()
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type')=='zhixin':
            parm = json.loads(data)
            header={'Cookie':self.path.get('login','token')}
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type'  in self.path.options('config') and self.path.get('config','request_type').strip()=='form_data':
                    respons = urllib.request.Request(url=all_url, data=urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                    respons = urllib.request.urlopen(respons)
                    respons = respons.read()
                else:
                    respons = urllib.request.Request(url=all_url, data=json.dumps(parm), headers=header)
                    respons = urllib.request.urlopen(respons)
                    respons = respons.read()
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type')=='hexin':
            data={'json':data}
            parm = data
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            header={}
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            try:
                if 'request_type'  in self.path.options('config') and self.path.get('config','request_type').strip()=='form_data':
                    respons=requests.post(all_url,data=parm,headers=header)
                    respons = respons.text
                else:
                    respons = urllib.request.Request(url=all_url, data=json.dumps(parm), headers=header)
                    respons = urllib.request.urlopen(respons)
                    respons = respons.read()
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type')=='haofang_server':
            parm = json.loads(data)
            header=json.loads(self.path.get('login','haofang_headertoken'))
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type'  in self.path.options('config') and self.path.get('config','request_type').strip()=='form_data':
                    respons = urllib.request.Request(url=all_url, data=urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                    respons = urllib.request.urlopen(respons)
                    respons = respons.read()
                else:
                    respons = urllib.request.Request(url=all_url, data=json.dumps(parm), headers=header)
                    respons = urllib.request.urlopen(respons)
                    respons = respons.read()
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})

        if self.path.get('sign', 'sign_type')=='hkci':
            parm = json.loads(data)
            header=json.loads(self.path.get('login','huasheng_headertoken'))
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type'  in self.path.options('config') and self.path.get('config','request_type').strip()=='form_data':
                    respons=requests.post(all_url,data=data,headers=header)
                    # respons = urllib2.Request(url=all_url, data=urllib.urlencode(parm), headers=header)
                    # respons = urllib2.urlopen(respons)
                    # respons = respons.read()
                    respons=respons.text
                else:
                    respons = requests.post(all_url, json=json.loads(data), headers=header)
                    respons = respons.text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})

        if self.path.get('sign', 'sign_type')=='web':
            parm = json.loads(data)
            # parm.pop('symbol')
            if self.path.has_option('sign', 'login') and self.path.get('sign', 'login') == 'false':
                header = {}
            else:
                hash = hashlib.md5()
                # 登录url，登录用户，登录没密码，去掉前后空格后的相加的字符串
                code = self.path.get('login', 'url').strip() + self.path.get('login','name').strip() + self.path.get('login', 'password').strip()
                hash.update(code)
                code =str(hash.hexdigest())
                header=json.loads([self.path.get('login_value',i) for i in self.path.options('login_value') if code==i][0])
            if len(url) != 0:
                if 'http://' in url[0] or 'https://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                if 'request_type' in self.path.options('config') and self.path.get('config','request_type')=='json':
                    respons = requests.post(all_url, data=json.dumps(parm), headers=header).text
                else:
                            header['authorization']='UzAwMQ=='
                            request = urllib.request.Request(all_url, urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                            respons = urllib.request.urlopen(request,timeout=60).read()
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type')=='app':
            parm = json.loads(data)
            #parm.pop('symbol')
            header={}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(list(zip(head_key, head_key)))
                header['Content-Type'] = "application/json"
            else:
                header_dict = {"Content-Type": "application/json"}
            header['Content-Type'] = 'application/json'
            if 'head_data'  in self.path.sections():
                for k,i in json.loads(self.path.get('head_data','head_data')).items():
                    header[k]=i
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                if  'request_type'  in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    header['Content-Type']='application/x-www-form-urlencoded'
                    request = urllib.request.Request(all_url, urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                else:
                    d = json.dumps(parm).encode(encoding='utf-8')
                    request = urllib.request.Request(all_url, data=d, headers=header)
                respons = urllib.request.urlopen(request, timeout=60).read()
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                respons = json.dumps({"error_detail": str(e)})
            #logger.debug("接口返回信息" + str(respons))
        if self.path.get('sign', 'sign_type') in ('app', 'xiang_qian'):
            parm = json.loads(data)
            header={}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(list(zip(head_key, head_key)))
                header['Content-Type'] = "application/json"
            else:
                header_dict = {"Content-Type": "application/json"}
            header['Content-Type'] = 'application/json'
            if 'head_data'  in self.path.sections():
                for k,i in json.loads(self.path.get('head_data','head_data')).items():
                    header[k]=i
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]

            else:
                all_url=self.url

            if '][' in all_url:
                datapart = all_url[all_url.find('['):all_url.rfind(']')+1]
                section, key, datatype = datapart[1:-1].split('][')

            for k in parm:
                if not isinstance(parm[k], str):
                    parm[k] = parm[k].decode(chardet.detect(parm[k])['encoding'])
            en_de_aes=AESCipher('Jy_ApP_0!9i+90&#')
            parm={"aesRequest":en_de_aes.encrypt(data).decode('utf-8')}
            header['appType']='ios'
            try:
                if 'request_type'  in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    header['Content-Type'] = 'application/x-www-form-urlencoded'
                    request = urllib.request.Request(all_url, urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                else:
                    request = urllib.request.Request(all_url, data=json.dumps(parm).encode(encoding='utf-8'), headers=header)
                resp = urllib.request.urlopen(request, timeout=60).read().decode('utf-8')
                d = json.loads(resp)
                aes = d['aesResponse']
                respons = en_de_aes.decrypt(aes)
            except Exception as e:
                print(traceback.format_exc())
                print(e)
                respons = json.dumps({"error_detail": str(e)})
            #logger.debug("接口返回信息" + str(respons))
        if self.path.get('sign', 'sign_type') in ('hengfeng_w', 'extra', 'json_param', 'json_extra'):
            parm = json.loads(data)
            #parm.pop('symbol')
            header={}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(list(zip(head_key, head_key)))
                if not('Content-Type' in header):
                    header['Content-Type'] = "application/json"
            else:
                header['Content-Type'] = 'application/json'
            if 'head_data'  in self.path.sections():
                for k,i in json.loads(self.path.get('head_data','head_data')).items():
                    header[k]=i
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url

            if ('sign' in parm) or ("reqData" in parm) or ('respData' in parm):
                try:
                    if 'reqData' in parm:
                        hf = hengfeng_w_sing(parm['reqData'])
                        parm['sign']=hf.sign_return(key='reqData')
                        parm['reqData'] = json.dumps(parm['reqData'])
                    if 'respData' in parm:
                        hf = hengfeng_w_sing(parm['respData'])
                        parm['sign'] = hf.sign_return(key='respData')
#                        parm['respData'] = json.dumps(parm['respData'])
                except Exception as err:
                   print(traceback.format_exc(err))
                   print(err)
                   raise Exception('请求体需要包在reqData里')
#            for k in parm:
#                if not isinstance(parm[k], (str, dict)):
#                    parm[k] = parm[k].decode(chardet.detect(parm[k])['encoding'])
            try:
                if  'request_type'  in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    if self.path.get('sign', 'sign_type') in ('extra', 'json_param', 'json_extra'):
                        header = {'Content-Type': self.path.get('config', 'head_value')}
#                        header = {'Content-Type': 'application/json'}
                        if self.path.get('sign', 'sign_type') == 'json_param':
                            parm = {'json': json.dumps(parm)}
#                            header = {'Content-Type': 'application/x-www-form-urlencoded'}
                        if self.path.get('sign', 'sign_type') == 'json_extra':
                            parm = json.dumps(parm)
                        res = requests.post(url=all_url, data=parm, headers=header)
                        if self.path.get('sign', 'sign_type') == 'json_extra':
                            j = json.loads(res.text)
                        respons = {'retCode': res.status_code, 'text': res.text}
                    else:
                        header['Content-Type'] = 'application/x-www-form-urlencoded'
                        request = urllib.request.Request(all_url, urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                        r = urllib.request.urlopen(request, timeout=60)
                        respons = r.read().decode('utf-8')
                else:
#                    request = urllib.request.Request(all_url, data=json.dumps(parm), headers=header)
#                    respons = urllib.request.urlopen(request, timeout=60).read()
                    resp = requests.post(url=all_url, data=parm, headers=header)
                    respons = resp.text
            except Exception as e:
                print(e)
                respons = json.dumps({"error_detail": str(traceback.format_exc())})

            #logger.debug("接口返回信息" + str(respons))
        if self.path.get('sign', 'sign_type')=='jy_appServer':
            #parm = json.loads(data)
            #parm.pop('symbol')
            parm=all_jiami(data,self.path.get('sign_url', 'encode_url'))
            #header['Content-Type']='application/x-www-form-urlencoded'
            header={}
            header['Content-Type'] = 'application/json'
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                if  'request_type'  in self.path.options('config') and self.path.get('config', 'request_type').strip() == 'form_data':
                    header['Content-Type']='application/x-www-form-urlencoded'
                    request = urllib.request.Request(all_url, urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                    respons = urllib.request.urlopen(request, timeout=60).read()
                else:
                    respons = urllib.request.Request(url=all_url, data=urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                    respons = urllib.request.urlopen(request, timeout=60).read()
                    respons=all_jiemi(respons,self.path.get('sign_url', 'decode_url'))
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})

        config.set('config', 'req', json.dumps(parm))
        try:
            config.set('config','respons', respons)
        except Exception as err:
            print(traceback.format_exc())
            print(err)
        return {'respons': respons, 'url': all_url}
    #普通delete请求
    def delete(self,data,config,*url):
        data=change_data_db(config, data).data
        json_change(copy.deepcopy(self.json_moban),json.loads(data))
        #data = creat_json(copy.deepcopy(self.json_moban), data)
        if 'sign_type' not in  list(dict(self.path.items('sign')).keys()) or config.get('sign', 'sign_type')=='v1':
            head_data=dict(list(zip(config.get('config', 'head_key'),config.get('config', 'head_value'))))
            parm = json.loads(data)
            parm['sign']=buildMySign(parm,config.get('sign', 'secretKey'))
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons = requests.delete(url=all_url, params=parm, headers=head_data,verify=False).text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if config.get('sign', 'sign_type')=='v3':
            auth=CoinbaseExchangeAuth(config.get('sign', 'api_key'), config.get('sign', 'secretKey'),self.path.get('sign', 'password'))
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                respons = requests.delete(url=all_url, json=parm, auth=auth).text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if config.get('sign', 'sign_type')=='Backstage_web':
            parm = json.loads(data)
            if self.path.has_option('sign','login') and  self.path.get('sign', 'login')=='false':
                header={}
            else:
                code = self.path.get('login', 'url').strip() + self.path.get('login',
                                                                             'name').strip() + self.path.get(
                    'login', 'password').strip()
                hash.update(code)
                code = str(hash.hexdigest())
                header = json.loads([self.path.get('login_value', i) for i in self.path.options('login_value') if code == i][0])
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                respons = requests.delete(url=all_url, json=parm,  headers = header).text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if config.get('sign', 'sign_type')=='web':
            parm = json.loads(data)
            if self.path.has_option('sign','login') and  self.path.get('sign', 'login')=='false':
                header={}
            else:
                code = self.path.get('login', 'url').strip() + self.path.get('login',
                                                                             'name').strip() + self.path.get(
                    'login', 'password').strip()
                hash.update(code)
                code = str(hash.hexdigest())
                header = json.loads([self.path.get('login_value', i) for i in self.path.options('login_value') if code == i][0])
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                respons = requests.delete(url=all_url, json=parm,  headers = header).text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type')=='app':
            parm = json.loads(data)
            #parm.pop('symbol')
            header=json.loads(self.path.get('app_head','app_head'))
            #header['Content-Type']='application/x-www-form-urlencoded'
            header['Content-Type'] = 'application/json'
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                request = urllib.request.Request(all_url, data=urllib.parse.urlencode(parm).encode(encoding='utf-8'), headers=header)
                respons = urllib.request.urlopen(request,timeout=60).read()
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        return {"respons": respons, 'url': all_url}
    #普通get 请求
    def get(self,data,congig,*url):
        data=change_data_db(self.path, data).data
        json_change(copy.deepcopy(self.json_moban), json.loads(data))
        #data = creat_json(copy.deepcopy(self.json_moban), data)
        if  'sign_type' not in  list(dict(self.path.items('sign')).keys()) or  self.path.get('sign', 'sign_type') == 'v1':
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://' in url[0]:
                    all_url = url[0]
                else:
                    all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url = self.url
            try:
                respons=requests.get(url=all_url, params=parm, headers=dict(list(zip(self.path.get('config','head_key'),self.path.get('config','head_value')))),verify=False).text
            except Exception as e:
                respons=json.dumps({"error_detail":str(e)})
        if self.path.get('sign', 'sign_type')=='v3':
            auth=CoinbaseExchangeAuth(self.path.get('sign', 'api_key'), self.path.get('sign', 'secretKey'),self.path.get('sign', 'password'))
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                if len(parm) ==0:
                    respons = requests.get(url=all_url,  auth=auth).text
                else:
                   respons = requests.get(url=all_url, params=parm, auth=auth).text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type')=='web':
            if self.path.has_option('sign','login') and  self.path.get('sign', 'login')=='false':
                header={}
            else:
                code = self.path.get('login', 'url').strip() + self.path.get('login',
                                                                             'name').strip() + self.path.get(
                    'login', 'password').strip()
                hash.update(code)
                code = str(hash.hexdigest())
                header =json.loads( [self.path.get('login_value', i) for i in self.path.options('login_value') if code == i][0])
            parm = json.loads(data)
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                if len(parm) ==0:
                    respons = requests.get(url=all_url,   headers = header).text
                else:
                   respons = requests.get(url=all_url, params=parm,  headers = header).text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type')=='app':
            parm = json.loads(data)
            #parm.pop('symbol')
            header={}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(list(zip(head_key, head_key)))
                header['Content-Type'] = "application/json"
            else:
                header_dict = {"Content-Type": "application/json"}
            #header['Content-Type']='application/x-www-form-urlencoded'
            header['Content-Type'] = 'application/json'
            if 'head_data'  in self.path.sections():
                for k,i in json.loads(self.path.get('head_data','head_data')).iteritmes():
                    header[k]=i
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                request = requests.get(all_url, params=parm, headers=header,timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
            #logger.debug("接口返回信息" + str(respons))
        if self.path.get('sign', 'sign_type')=='xiang_qian':
            parm = json.loads(data)
            #parm.pop('symbol')
            header={}
            head_key = self.path.get('config', 'head_key').split(',')
            head_value = self.path.get('config', 'head_value').split(',')
            if len(head_key) == len(head_value):
                head = dict(list(zip(head_key, head_key)))
                header['Content-Type'] = "application/json"
            else:
                header_dict = {"Content-Type": "application/json"}
            #header['Content-Type']='application/x-www-form-urlencoded'
            header['Content-Type'] = 'application/json'
            if 'head_data'  in self.path.sections():
                for k,i in json.loads(self.path.get('head_data','head_data')).iteritmes():
                    header[k]=i
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            xiangqian_sign = AESCipher('Jy_ApP_0!9i+90&#')
            parm={"aesRequest":xiangqian_sign.encrypt(json.dumps(parm))}
            try:
                request = requests.get(all_url, params=parm, headers=header,timeout=5)
                respons = xiangqian_sign.decrypt(json.loads(request.text)['aesResponse'])
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
            #logger.debug("接口返回信息" + str(respons))
        if self.path.get('sign', 'sign_type') == 'Backstage_web':
            parm = json.loads(data)
            #parm.pop('symbol')
            header=json.loads(self.path.get('app_head','app_head'))
            #header['Content-Type']='application/x-www-form-urlencoded'
            header = {'Authorization': self.path.get('login','token'), 'Content-type': 'application/json'}
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                request = requests.get(all_url, params=parm, headers=header,timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type') == 'zhixin':
            parm = json.loads(data)
            #parm.pop('symbol')
            header=json.loads(self.path.get('app_head','app_head'))
            #header['Content-Type']='application/x-www-form-urlencoded'
            header = {'Authorization': self.path.get('login','token'), 'Content-type': 'application/json'}
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                request = requests.get(all_url, params=parm, headers=header,timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type') == 'hkci':
            parm = json.loads(data)
            #parm.pop('symbol')
            header = json.loads(self.path.get('login', 'huasheng_headertoken'))
            #header['Content-Type']='application/x-www-form-urlencoded'
            header = {'Authorization': self.path.get('login','token'), 'Content-type': 'application/json'}
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                request = requests.get(all_url, params=parm, headers=header,timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        if self.path.get('sign', 'sign_type') == 'haofang_server':
            parm = json.loads(data)
            #parm.pop('symbol')
            #header['Content-Type']='application/x-www-form-urlencoded'
            header=json.loads(self.path.get('login','haofang_headertoken'))
            if len(url) != 0:
                if 'http://'  in url[0]  or 'https://'  in url[0]:
                    all_url=url[0]
                else:
                  all_url = self.path.get('config', 'public_url') + url[0]
            else:
                all_url=self.url
            try:
                request = requests.get(all_url, params=parm, headers=header,timeout=5)
                respons = request.text
            except Exception as e:
                respons = json.dumps({"error_detail": str(e)})
        return {"respons": respons, 'url': all_url}

