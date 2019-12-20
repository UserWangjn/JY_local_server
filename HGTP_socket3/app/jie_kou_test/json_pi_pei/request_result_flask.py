# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\Users\sunzhen\Desktop\web flask\HGTP_socket3\app\jie_kou_test\json_pi_pei\request_result_flask.py
# Compiled at: 2019-04-12 11:25:12
import traceback
import sys, urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, json
sys.path.append('../../')

class request_flask(object):

    def __init__(self, name, data, time, ip, server_ip, server_port=8080):#, *simple_run):
        print(name, data, time, ip, server_ip, server_port)
        self.name = name
        self.data = data
        self.server_ip = server_ip
        url = 'http://' + server_ip + ':' + str(server_port) + '/piliang_run_result'
        test_data = urllib.parse.urlencode({'jeikou_name': name.encode('utf-8'), 'result': data.encode('utf-8'), 'time': time.encode('utf-8'), 'ip': ip.encode('utf-8'), 'path': 'server'}).encode(encoding='utf-8')
        req = urllib.request.Request(url=url, data=test_data)
        res_data = urllib.request.urlopen(req).read()
        try:
            res_data = json.loads(res_data)
        except Exception as err:
            print(traceback.format_exc())
            print(err)
            res_data = {'res_data': res_data}