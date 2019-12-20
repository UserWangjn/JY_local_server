# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\json_pi_pei\begin_excel.py
# Compiled at: 2019-05-05 14:07:59
__author__ = 'SUNZHEN519'
import sys
sys.path.append('../../')
import json, xlrd, os

class reead_excel(object):

    def __init__(self, path):
        self.path = path
        self.all_case = {}
        self.all_yewuliu = []
        self.gen_mulu = os.path.dirname(os.path.dirname(path[0]))
        self.read_case()
        self.yewuliu()
        self.jiekou_paixu()
        for k in self.all_case:
            for i in self.all_case[k]:
                self.all_case[k][i] = ''

    def jiekou_paixu(self):
        self.all_yewuliu.sort()
        for k, i in enumerate(self.path):
            if not i.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
                self._num = k
                break

        for i in self.all_yewuliu:
            if len(i) > 0 and i[0].strip() != '':
                self._this_path = os.path.join(self.gen_mulu, i[0].split('$')[0].split('/')[0], i[0].split('$')[0].split('/')[1])
                self._this_path = os.path.normpath(self._this_path)
                self.path.remove(self._this_path)
                self.path.insert(self._num, self._this_path)

    def read_case(self):
        for i in self.path:
            i = os.path.normpath(i)
            excle_path = os.path.join(i, os.path.basename(i) + '.xls')
            if not os.path.isfile(excle_path):
                continue
            self._workbook = xlrd.open_workbook(os.path.join(i, os.path.basename(i) + '.xls'))
            sheet2 = self._workbook.sheet_by_index(0)
            self._all_id = [ int(key) for key in sheet2.col_values(0)[1:] if '#' not in str(key) and str(key).strip() != '' ]
            if 'before_request' in sheet2.row_values(0):
                self.all_case[i] = dict(list(zip(self._all_id, sheet2.col_values(sheet2.row_values(0).index('before_request'))[1:])))
                self.all_case[i]['before_request'] = True
            else:
                self.all_case[i] = {}
                self.all_case[i]['before_request'] = False
                for z in self._all_id:
                    self.all_case[i][int(z)] = ''

    def yewuliu(self):
        for path, detail in list(self.all_case.items()):
            if detail['before_request'] == False:
                detail.pop('before_request')
                continue
            else:
                detail.pop('before_request')
                self._yewu = []
                for case_id, before_detail in list(detail.items()):
                    self._statu = 0
                    if before_detail.strip() != '':
                        this_before_str = os.path.basename(os.path.dirname(path)) + '/' + os.path.basename(path) + '$' + str(case_id)
                        for before_str in self.all_yewuliu:
                            for before_str_simple in before_str:
                                if this_before_str in before_str_simple:
                                    self._statu = 1
                                    break

                        if self._statu == 1:
                            continue
                        if before_detail.strip() != '':
                            self._yewu.append(os.path.basename(os.path.dirname(path)) + '/' + os.path.basename(path) + '$' + str(case_id))
                            self.find_jiekou(before_detail, self._yewu)

                if len(self.all_yewuliu) == 0:
                    self.all_yewuliu.append(self._yewu)
                else:
                    for i in self.all_yewuliu:
                        if ('#').join(self._yewu) in ('#').join(i):
                            break
                        if i == self._yewu:
                            break
                        else:
                            self.all_yewuliu.append(self._yewu)
                            break

    def find_jiekou(self, before_detail, yewu_append):
        self._part_path, self._par_id = before_detail.split('$')
        yewu_append.append(before_detail)
        before_path = os.path.normpath(os.path.join(self.gen_mulu, self._part_path))
        if before_path in list(self.all_case.keys()) and int(self._par_id) in list(self.all_case[before_path].keys()):
            if self.all_case[before_path][int(self._par_id)].strip() != '':
                self.find_jiekou(self.all_case[before_path][int(self._par_id)].strip(), yewu_append)


if __name__ == '__main__':
    a = []
    a.append(('C:\\Users\\sunzhen\\Desktop\\新建文件夹3\\杨雪峰\\示例demo\\测试环境\\App_server\\正常登录').decode('utf-8'))
    a.append(('C:\\Users\\sunzhen\\Desktop\\新建文件夹3\\杨雪峰\\示例demo\\测试环境\\App_server\\金额期限申请').decode('utf-8'))
    a.append(('C:\\Users\\sunzhen\\Desktop\\新建文件夹3\\杨雪峰\\示例demo\\测试环境\\App_server\\用户注册').decode('utf-8'))
    a.append(('C:\\Users\\sunzhen\\Desktop\\新建文件夹3\\杨雪峰\\示例demo\\测试环境\\App_server\\邀请码验证').decode('utf-8'))
    reead_excel(a)