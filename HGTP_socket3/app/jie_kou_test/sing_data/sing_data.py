import execjs
from bs4 import BeautifulSoup
import os
import re
import json
import requests
import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse
import hashlib
#第一个参数是单点登录的地址，第二个参数是用户名，第三个参数是密码
def second(url,name,password):
    conn1 = requests.session()
    response = conn1.get(url)
    res = response.text
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    first_id = cookies['JSESSIONID_COOKIE']
    protocol, s1 = urllib.parse.splittype(url)
    host, s2 = urllib.parse.splithost(s1)
    url = 'http://'+host+'/loan/user/login'
    headers = {'Content-Type': 'application/x-www-form-urlencoded,Cookie', 'JSESSIONID_COOKIE': first_id}
    param = {'username': name, 'password': password}
    response = requests.post(url, param)
    id = response.url.split('JSESSIONID=')[-1]
    header = {'Cookie': 'JSESSIONID_COOKIE=' + id}
def web_token(public_config):
    url = public_config.get('login', 'url')
    if 'service='  in url:
        name = public_config.get('login', 'name')
        password = public_config.get('login', 'password')
        return ceshizhong(url,name,password)
    else:
        name = public_config.get('login', 'name')
        password = public_config.get('login', 'password')
        header=second(url, name, password)
        return second(url, name, password)
def ceshizhong(url,name,password):
    #url = "http://172.18.101.98/cas/login?source=S001&service=http://172.18.100.212:8080/loan/user/caslogin"
    conn1 = requests.session()
    response=conn1.get(url)
    res=response.text
    cookies = requests.utils.dict_from_cookiejar(response.cookies)
    first_id = cookies['JSESSIONID']
    data,headers,new_url=login_request_data(res,name,password)
    url=get_host(url)+new_url
    #发送登录请求
    response=requests.post(url, data)
    second_id=response.url.split('JSESSIONID=')[-1]
    headers={
        'Cookie': 'JSESSIONID = '+first_id+'; '+'JSESSIONID_COOKIE ='+second_id
    }
    return  headers
def get_host(url):
    protocol, s1 = urllib.parse.splittype(url)
    host, s2 = urllib.parse.splithost(s1)
    return 'http://'+host
#第一个参数为调用url返回的text信息，第二个为用户名,第三个为密码
def login_request_data(res,name,password):
    html = BeautifulSoup(res, 'html.parser')
    jypwdtoken = html.find(attrs={'name': 'jypwdtoken'}).get('value')
    lt = html.find(attrs={'name': 'lt'}).get('value')
    execution = html.find(attrs={'name': 'execution'}).get('value')
    sessionid = html.find(attrs={'name': 'sessionid'}).get('value')
    key = re.findall(r'var key = "(.*)"', res)[0]
    new_url = html.find(attrs={'id': 'loginForm'}).get('action')
    paths = os.path.dirname(__file__)
    js2 = os.path.join(paths, 'rc4.js')
    b = execjs.compile(open(js2).read())
    keys = b.call('encryptAes', key, password)
    data = {
        'requestSystem': "http://dk.jieyuechina.com/loan",
        'jypwdtoken': jypwdtoken,
        'password': keys,
        'ptt': 123456,
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'browertype': '',
        'ratio': '',
        'useros': '',
        'sessionid': sessionid,
        'username': name,
    }
    headers = {"Connection": "keep-alive",
               "Host": "172.18.101.98",
               "Content-Length": "302",
               "Cache-Control": "max-age=0",
               "Origin": "http://172.18.101.98",
               "Upgrade-Insecure-Requests": "1",
               "Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
               "Referer": "http://172.18.101.98/cas/login?source=S001&service=http://172.18.100.212:8080/loan/user/caslogin",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Cookie": "JSESSIONID=" + sessionid}
    return [data,headers,new_url]
def test(header):
    url='http://172.18.100.212:8080/loan/lbTIntoInfo/checkIntoCanEdit?intoId=120153854739'
    data={'intoId': 120153854739}
    headers=header
    req = urllib.request.Request(url, json.dumps(data), headers)
    response = urllib.request.urlopen(req)
    return response.read()
#后台加密登录
def houtai_jiami(user,password,url):
    m = hashlib.md5()
    m.update(password)
    toke=m.hexdigest()
    parm = {'phone': user, 'pwd':toke, 'flag': "", 'type': 1}
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    req = urllib.request.Request(url=url, data=json.dumps(parm), headers=header_dict)
    res = urllib.request.urlopen(req)
    res = res.read()
    return json.loads(res)['data']['token']
#严雪泪 ，后台加密，返回接口解密
def all_jiami(req,jiami_url):
    header = {}
    header['Content-Type'] = 'application/json'
    request = urllib.request.Request(jiami_url, req, headers=header)
    # print r.text
    return  urllib.request.urlopen(request, timeout=20).read()
#严雪泪 ，返回接口解密
def all_jiemi(respons,jeimi_url):
    header = {}
    header['Content-Type'] = 'application/json'
    request = urllib.request.Request(jeimi_url, respons, headers=header)
    # print r.text
    return  urllib.request.urlopen(request, timeout=20).read()

if __name__=='__main__':
    name='10025186'
    password='Cs654321'
    url = "http://172.18.101.98/cas/login?source=S001&service=http://172.18.100.212:8080/loan/user/caslogin"
    header=ceshizhong(url,name,password)
    print(header)
    print(test(header))
