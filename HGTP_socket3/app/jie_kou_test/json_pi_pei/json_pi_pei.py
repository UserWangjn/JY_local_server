import sys
import traceback
sys.path.append("../../")
import json
from app.jie_kou_test.json_pi_pei.excel_data import  *
#生成json
#第一个为模板json 第二个为请求字典
def creat_json(v,data):
    if type(data) not in [list,dict]:
        j=json.loads(data)
    else:
        j=data
    #判断是否有重复json
    #判断哪个键包含有二级参数
    if type(v) == dict:
        for k in list(v.keys()):
            if k=='id_canshu':
                k='id'
            if k=="result_data":
                k='result'
            if type(v[k]) != dict and type(v[k]) != list:
                if k not in j:
                    v.pop(k)
                    continue
                if type(j[k]) not in [float,int,int]  and j[k].strip()=='':
                    #v.pop(k)
                    continue
                s = change(v[k], j[k])
                v[k] = s
            elif type(v[k]) == list:
                for z in v[k]:
                    creat_json(z, j)
            elif type(v[k]) == dict:
                creat_json(v[k], j)
    return json.dumps(v)

def change(a, b):
    if b==0.0:
        b=0
    if b is None or isinstance(b, bool):
        pass
    elif isinstance(a, int):
        try:
            b = int(b)
        except Exception as err:
            print(traceback.format_exc())
            print(err)
    elif isinstance(a, float):
        try:
            if float(b)==int(b):
                b=int(b)
            else:
                b=float(b)
        except Exception as err:
            print(traceback.format_exc())
            print(err)

    elif type(a) == str:
        if isinstance(b, bytes):
            b = b.decode('utf-8')
        else:
            b=str(b)
    else:
        if isinstance(b, float):
            b = int(b)
    return b

#第一个为模板json 第二个为请求字典
def creat_json(v,data):
    if type(data) not in [list,dict]:
        j=json.loads(data)
    else:
        j=data
    if type(j) == dict:
        for k, i in j.items():
            if k == 'json_data':
                j['json'] = j.pop('json_data')
    #判断是否有重复json
    #判断哪个键包含有二级参数
    if type(v) == dict:
        for k in list(v.keys()):
            if  v[k]=='change_json':
                   v[k]=j[k]
            elif type(v[k]) != dict and type(v[k]) != list :
                if k not in j:
                    v.pop(k)
                    continue
                elif type(j[k]) not in [float,int,int] and j[k]!=None:
                    try:
                        j[k].strip() == 'data_empty'
                    except Exception as err:
                        print(traceback.format_exc())
                        print(err)
                    else:
                        if  j[k].strip() =='data_empty':
                             v[k]=''
                             continue
                        elif j[k]!=None and j[k].strip()=='':
                           v.pop(k)
                           continue
                s = change(v[k], j[k])
                v[k] = s
            elif type(v[k]) == list:
                for z in v[k]:
                    creat_json(z, j)
            elif type(v[k]) == dict:
                creat_json(v[k], j)
    return json.dumps(v)
#第一个为json模板，第二个为要转的json
def json_change(a, b):
    if isinstance(a, (dict,list)):
        if isinstance(a, list):
            for k,i in enumerate(a):
                if type(a[k]) in [list, dict]:
                    json_change(a[k], b[k])
                else:
                    if isinstance(a[k], int) and b[k] == int(b[k]):
                        b[k] = int[b[k]]
                    if isinstance(a[k], int):
                        b[k] = int(b[k])
                    elif isinstance(a[k], float):
                        b[k] = float(b[k])
                    elif isinstance(a[k], bool):
                        b[k] = bool(b[k])
                    elif isinstance(a[k], str) and  a[k]!='change_json':
                        b[k] = str(b[k])
        else:
            for k in a:
                if isinstance(b, dict):
                    if k in b:
                        if isinstance(a[k], (list,dict)):
                            json_change(a[k],b[k])
                        else:
                            if isinstance(b[k], float) and b[k]==int(b[k]):
                                b[k] = int(b[k])
                            if isinstance(a[k], int):
                                b[k] = int(b[k])
                            elif isinstance(a[k], float):
                                b[k] = float(b[k])
                            elif isinstance(a[k], bool):
                                b[k] = bool(b[k])
                            elif isinstance(a[k], str):
                                if a[k]!='change_json':
                                    b[k] = str(b[k])
                                elif a[k]!='empty_data':
                                    b[k] = ""
                    else:
                        b[k] = a[k]

#判断哪个字段为json字符串，若为直接修改修改参数值为字符串，第一个为json魔板，第二个为excel中的参数字典，不是将全部json
def change_json_data(v, excel_data):
    if v!='':
        if not isinstance(v, (list,dict)):
            try:
                v=json.loads(v)
            except Exception as err:
                print(traceback.format_exc())
                print(err)
        if isinstance(v, dict):
            for k in v:
                if not isinstance(v[k], str):
                    change_json_data(v[k],excel_data)
                else:
                    if v[k]=="change_json":
                        for u in excel_data:
                            if u==k:
                                try:
                                    excel_data[u]=json.loads(excel_data[u])
                                except Exception as err:
                                    print(traceback.format_exc())
                                    print(err)
                    if not k in excel_data:
                        excel_data[k] = v[k]

    return excel_data

