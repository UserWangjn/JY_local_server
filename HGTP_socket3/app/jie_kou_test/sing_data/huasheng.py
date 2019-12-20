# -*- coding: utf-8 -*-
import requests
import json
import pymysql
import time
import urllib.request, urllib.parse, urllib.error
def  get_db_data(db_detail,sql):
    db = pymysql.connect(db_detail[0],db_detail[1],db_detail[2],db_detail[3])
    cursor = db.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    db.close()
    return cursor.fetchall()
#获取店铺详细信息
def huasheng_test(get_mendian_detail_url,mendian):
    data={"placeCode":""}
    r = requests.post(get_mendian_detail_url, json = data)
    data=json.loads(r.text)
    for i in data['responseBody']:
        if i['companyName']==mendian.decode('gb2312'):
            return i
    return "error"


# 获取验证码，查看是否过期，若是过期，则点击获取验证码，否则直接从数据库读取验证码
def get_yanzhengma(mendian_all_detail,db_detail, phone, mendian, lingpaai, get_mendian_detail_url):
    # db = pymysql.connect(
    #     host=db_detail[0],
    #     port=int(db_detail[1]),
    #     user=db_detail[2],
    #     password=db_detail[3],
    #     database=db_detail[4],
    #     charset='utf8'
    # )
    # # db = pymysql.connect(db_detail[0], db_detail[2], db_detail[3], db_detail[4])
    # cursor = db.cursor()
    # cursor.execute("SELECT * FROM t_sms_info  WHERE phone=%s  ORDER BY expire_time DESC LIMIT 0,1" % phone)
    # db.close()
    # data = cursor.fetchall()
    # if len(data)!=0:
    #    data=data[0]
    #    yanzhengma = data[8].decode('utf-8').split(u"：")[1].split(u'，')[0].strip()
    #    if int(time.mktime(data[6].timetuple())) < time.time() + 120:
    #         return yanzhengma
    url = "http://peanut.test.haikr.com/hk-peanut-car/api/user/sendMsg"
    data = {
        "sysCode": mendian.decode('gb2312'),
        "orgCode": mendian_all_detail["companyCode"],
        "addrProvince": mendian_all_detail["addrProvince"],
        "addrCounty": mendian_all_detail["addrCounty"],
        "addrCity": mendian_all_detail["addrCity"],
        "phoneNum": phone,
        "verfication": "",
        "password": lingpaai
    }
    k=requests.post(url,json=data)
    return '1111'
# 登录接口
def hs_login(server_host,db_detail,login_url, phone, mendian, lingpaai):
    get_mendian_detail_url = server_host+'/hk-peanut-car/api/place/getLoginPlaceInfo'
    mendian_all_detail = huasheng_test(get_mendian_detail_url, mendian)
    yan_zheng=get_yanzhengma(mendian_all_detail, db_detail, phone, mendian, lingpaai, get_mendian_detail_url)
    data = {
        "sysCode": mendian.decode('gb2312'),
        "orgCode":  mendian_all_detail["companyCode"],
        "addrProvince":  mendian_all_detail["addrProvince"],
        "addrCounty":  mendian_all_detail["addrCounty"],
        "addrCity":  mendian_all_detail["addrCity"],
        "phoneNum": phone,
        "verfication": yan_zheng,
        "password": lingpaai
    }
    requests.options(login_url)
    token={"Authorization":"Bearer "+json.loads(requests.post(login_url,json=data).text)['responseBody']['info']}
    return  json.dumps(token)
# def get_yanzhengma():
if __name__=="__main__":
    url="http://10.50.181.41/hkci/single"
    get_mendian_detail_url='http://10.50.181.42:9041'
    login_url="http://10.50.181.42:9041rt"
    phone="19992131026"
    dianpu="太原测试三"
    lingpai="19870217"
    db_detail=["10.50.181.45","hk_insurance_dev","hk_dev","hk_insurance"]
    sql="SELECT * FROM t_sms_info  WHERE phone=%s  ORDER BY expire_time DESC LIMIT 0,1"   %  phone
    # huasheng_test(get_mendian_detail_url,dianpu)
    token=hs_login(get_mendian_detail_url,db_detail,login_url,phone,dianpu,lingpai)
    data = {"customerINameOrLicenseNo": "345445", "orderStatus": "", "timeSlotMark": "", "pageNum": 1, "pageSize": "10",
            "orderStatusTxt": "订单状态", "timeSlotMarkTxt": "日期范围"}
    url = "http://10.50.181.42:9041/hk-peanut-car/weChat/car/getOrderList"

    k = requests.post(url, json=data, headers=token)
    print(k.text)




