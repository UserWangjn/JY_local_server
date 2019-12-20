import os
SECRET_KEY = 'you-will-never-guess'
BASE = os.path.abspath(os.path.dirname(__file__))
DB_BASE = os.path.join(BASE, '..', '..', 'db')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(DB_BASE, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE, 'db_repository')
#脚本存储路径
JIAO_DIZHI=r'C:\s_ben'
#运行模板文件存放路径名为mulu44.py
MOBANDIZHI=r'C:\web flask\mulu44.py'
GENMULU=r'C:\web flask'
SOCKET=8022
#生成结果文件html的地址
JIEGUO=r'C:\web flaskapp\templates\\'
#数据库example地址
DB_DIZHI=os.path.join(DB_BASE,'example.db')
CSRF_ENABLED = True
#生成结果文件存放目录
RESULT=r'C:\web flask\app\templates\result'
PERMANENT_SESSION_LIFETIME=600
LOG=os.path.join(BASE, 'log.txt')
#接口url
JIE_KOU_URL=r'C:\work\lr_test'
LOCUST_FILE=r'C:\all_new\locust_file'
#哗啦啦运行脚本存放地方
ALLRUN_FILE=r'C:\all_new\run_mulu'
#接口运行数据库
JIE_KOU=os.path.join(DB_BASE,'jiekou.db')
#本机ip地址
BENJI_IP=('192.168.18.129',8065)
#批量运行脚本的时候，设置的运行间隔时间
RUN_INTERVAL=2.1
#版本号
BANBEN_NUM=3
#每跑完一次，都需要清除的db.txt里面的项目
CLEAR_DB_DATA = ['login_name', 'login_password', 'login_secret', 'token']
#ui 运行数据库
UI_DB=os.path.join(DB_BASE,'ui_test.db')