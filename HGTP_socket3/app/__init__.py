from flask import Flask, request, redirect, url_for
from werkzeug import *
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config.from_object('fileconfig')
db = SQLAlchemy(app)
UPLOAD_FOLDER = 'static/Uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from app import view

import logging
import logging.handlers
logger = logging.getLogger()
fh = logging.handlers.TimedRotatingFileHandler('run.log', "D", 1, 10)
fh.setFormatter(logging.Formatter('%(asctime)s %(filename)s_%(lineno)d: [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)
