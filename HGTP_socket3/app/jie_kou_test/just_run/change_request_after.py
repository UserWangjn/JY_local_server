# -*- coding: utf-8 -*-
# uncompyle6 version 3.3.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.7.3 (default, Jun 24 2019, 04:54:02) 
# [GCC 9.1.0]
# Embedded file name: C:\jieyuelianhe\old_all_server\test_local\HGTP_socket3\app\jie_kou_test\just_run\change_request_after.py
# Compiled at: 2018-08-06 13:46:00
__author__ = 'SUNZHEN519'
import sys
sys.path.append('../../')
from selenium import webdriver
import time as timee, chardet, unittest, demjson, urllib.request, urllib.parse, urllib.error, random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import unittest, xlrd, configparser, json, urllib.request, urllib.error, urllib.parse, os, logging
from header import *
from app.just_run import *
from excel_data import *
from json_pi_pei.request_result_flask import *
from json_pi_pei.json_pi_pei import *
from json_pi_pei.request_run import *
from assert_run.assert_run import *

class change_request_after(object):

    def use(self, data):
        if 'after_request' in list(data.keys()) and str(data['after_request']).strip() != '':
            pass