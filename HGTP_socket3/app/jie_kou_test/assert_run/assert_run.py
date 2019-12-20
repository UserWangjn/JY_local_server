# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\assert_run\assert_run.py
# Compiled at: 2019-05-13 16:50:35
import traceback
import sys, os
sys.path.append('../../')
import json, demjson, chardet, time
from app.jie_kou_test.json_pi_pei.excel_data import *

class assert_run(object):

    def __init__(self, config):
        self.config = config
        self.all_statu = True

    def walk_find(self, v, j):
        if type(v) not in [list, dict] and v.strip() == '':
            return True
        if '&&' in v:
            s = hanshu_assert(v, self.config)
            return hanshu_assert(v, self.config)
        v = change_data_db(self.config, v).data
        try:
            v = json.loads(v)
        except Exception as err:
            print(traceback.format_exc())
            print(err)
            return False
        else:
            if self.all_statu == False:
                return False
            if type(v) not in [list, dict] and v.split('respons')[0].strip() == '' and v.strip() != '':
                chang_du = int(v.split('*')[(-1)])
                if type(eval(v.replace('respons', 'j').split('*')[0])) in [list, dict]:
                    result_len = len(eval(v.replace('respons', 'j').split('*')[0]))
                else:
                    result_len = len(json.loads(eval(v.replace('respons', 'j').split('*')[0])))
                return result_len == chang_du
            if type(v) not in [dict, list]:
                try:
                    v = json.loads(v)

                except Exception as err:
                    print(traceback.format_exc())
                    print(err)
                    return False

            if type(j) not in [dict, list]:
                if j == None and v != None:
                    return False
                if j.strip() == '':
                    if v != '':
                        return False
                else:
                    j = json.loads(j)
            if len(j) == 0 and len(v) != 0:
                return False

        if type(v) == list:
            if type(j) != list or len(j) < len(v):
                return False
            if len(v) > len(j):
                return False
            statu = 0
            for num, ceshi in enumerate(v):
                if type(ceshi) not in [int, float] and 'len*' in ceshi:
                    chang_du = ceshi.split('len*')[(-1)]
                    if len(j[num]) != int(chang_du):
                        return False
                if type(ceshi) in [dict, list]:
                    if type(j) == list:
                        for num_j, i_data in enumerate(j):
                            if self.walk_find(ceshi, j[num_j]) != False:
                                statu = 1

                elif ceshi == '*str':
                    if type(j[num]) not in [str, str]:
                        return False
                elif ceshi == '*int':
                    if type(j[num]) not in [int, int]:
                        return False
                elif type(ceshi) in [str, str] and ceshi.startswith('in:'):
                    if ceshi.split('in:')[(-1)] not in j[k]:
                        return False
                elif ceshi == '*float':
                    if type(j[num]) != float:
                        return False
                elif ceshi == '*bool':
                    if type(j[num]) != bool:
                        return False
                elif ceshi != j[num]:
                    try:
                        if float(ceshi) != float(j[num]):
                            return False
                    except Exception as err:
                        print(traceback.format_exc())
                        print(err)
                        return False

            if statu == 0:
                return False
        if type(v) == dict:
            for k, i in v.items():
                if type(j) != dict or k not in list(j.keys()):
                    return False
                if type(i) != dict and type(i) != list:
                    if i in [True, False]:
                        if k not in list(j.keys()):
                            return False
                        if i != j[k]:
                            return False
                    if i == None:
                        if j[k] != None:
                            return False
                    if type(i) not in [int, float, bool, int] and i != None and 'len*' in i:
                        chang_du = i.split('len*')[(-1)]
                        if len(j[k]) != int(chang_du):
                            return False
                    if i == '*':
                        try:
                            assert k in list(j.keys())

                        except Exception as err:
                            print(traceback.format_exc())
                            print(err)

                            return False

                    elif i == '*int':
                        try:
                            assert type(j[k]) in [int, int]
                        except Exception as err:
                            print(traceback.format_exc())
                            print(err)

                            return False

                    elif i == '*long':
                        try:
                            assert type(j[k]) in [int, int]
                        except Exception as err:
                            print(traceback.format_exc())
                            print(err)

                            return False

                    elif type(i) in [str, str] and i.startswith('in:'):
                        if i.split('in:')[(-1)] not in j[k]:
                            return False
                    elif i == '*float':
                        try:
                            assert type(j[k]) == float
                        except Exception as err:
                            print(traceback.format_exc())
                            print(err)

                            return False

                    elif i == '*str':
                        try:
                            assert type(j[k]) == str
                        except Exception as err:
                            print(traceback.format_exc())
                            print(err)

                            return False

                    elif i != j[k] and 'len*' not in str(i):
                        try:
                            if float(i) != float(j[k]):
                                return False
                        except Exception as err:
                            print(traceback.format_exc())
                            print(err)

                            return False

                if type(i) == dict:
                    if k not in list(j.keys()):
                        return False
                    if self.walk_find(i, j[k]) == False:
                        return False
                if type(i) == list:
                    if self.walk_find(i, j[k]) == False:
                        return False

        return self.all_statu


def hanshu_assert(assert_data, config):
    mulu = os.path.dirname(config.get('config', 'mulu'))
    req = config.get('config', 'req')
    respons = config.get('config', 'respons')
    if os.path.join(mulu, 'data_config') in sys.path:
        sys.path.remove(os.path.join(mulu, 'data_config'))
    sys.path.append(os.path.join(mulu, 'data_config'))
    imp_str = 'import %s' % assert_data.split('&&')[(-1)].split('.')[0]
    try:
        exec('del %s' % assert_data.split('&&')[(-1)].split('.')[0])
    except Exception as err:
            print(traceback.format_exc())
            print(err)

    exec(imp_str)
    return eval(assert_data.split('&&')[(-1)].split('.')[0] + '.' + assert_data.split('&&')[(-1)].split('.')[(-1)].replace('"', '') + '(req,respons)')


if __name__ == '__main__':
    a = {1: 2, 
       3: [{1: 1}], 5: 1}
    b = {3: [{1: 4}], 1: 3, 5: {3: 2}, 6: 7}
    u = assert_run()
    u.walk_find(a, b)
    for i in u.wrong:
        pass