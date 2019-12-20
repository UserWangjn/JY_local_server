#! /usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0],'app'))
from app import app
import threading
import sys
import os
from gevent import monkey
from gevent.pywsgi import WSGIServer
from app.jie_kou_test.run import *
if __name__ == '__main__':
     app.run(host='0.0.0.0',port=5041,debug=True)
     # monkey.patch_all()
     # WSGIServer(('0.0.0.0', 5038), app).serve_forever()
     # app.config.update(debug=False, threaded=True)
     # server = WSGIServer(('0.0.0.0', 5022), app)
     # server.serve_forever()
     # monkey.patch_all()
     # WSGIServer(('0.0.0.0', 5039), app).serve_forever()

