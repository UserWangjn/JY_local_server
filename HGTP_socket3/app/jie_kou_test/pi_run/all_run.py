    # Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\pi_run\all_run.py
# Compiled at: 2019-04-15 17:05:08
import sys, os
sys.path.append(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]))
from ..json_pi_pei.begin_excel import reead_excel
from .pi_run import *

class run(object):

    def __init__(self, path, run_time, *ip):
        self.suite = []
        path = [ os.path.normpath(i) for i in path ]
        self.all_bianliang = {}
        if len(ip) != 0:
            self.ip = ip[0]
            self.server_ip = ip[1]
        self.time = run_time
        self.u = reead_excel(path)
        self.all_bianliang['before_case_detail'] = self.u.all_case
        if len(ip) == 3:
            run_id = ip[2]
            self.simple_result = pi_run(path[0], run_time, self.ip, self.server_ip, self.all_bianliang, run_id).flask_result
        else:
            for i in self.u.path:
                if isinstance(i, bytes):
                    i = i.decode('utf-8')
                pi_run(i, run_time, self.ip, self.server_ip, self.all_bianliang)


if __name__ == '__main__':
    z = []
    z.append('C:\\所写系统\\无时间限制正常程序\\lr_test\\第二套环境\\HGTP\\get接口')
    z.append('C:\\所写系统\\无时间限制正常程序\\lr_test\\测试环境\\HGTP\\post接口')
    run(z, 'C:\\work\\lenove_jie_kou')