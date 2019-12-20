# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
import sys
sys.path.append("../../")
import unittest
import os
import inspect
from new import classobj
import HTMLTestRunner
import time
import copy
class make_suite(object):
    def get_current_function_name(self):
        return inspect.stack()[1][3]
    #生成测试套件
    #第一个参数为接口名字，第二个参数为列表，第一个为接口行id 和comment连接，第二个为错误信息字典。
    def __init__(self,name,data):
        self.name=name
        self.data=data
        #exec ('%s= classobj("a", (unittest.TestCase, ), { "test_u":self.run})' % self.name)
        exec ('%s= classobj("%s", (unittest.TestCase, ), { })'  %  (self.name,self.name))
        self.suite = unittest.TestSuite()
        for i in data:
            #print  self.name+str(i[0])
            #setattr(eval(self.name),self.name+str(i[0]),self.run)
            setattr(eval(self.name), str(self.name +'_'+ str(int(i[0]))), self.run)

            # 将测试用例加入到测试容器中
            self.suite.addTest(eval('%s("%s")' %   (self.name,self.name+'_'+str(int(i[0])))))
    #方法函数
    def run(self):
             for k,i in enumerate(self.data):
                 u=self.data.pop(k)
                 if len(u[1])!=0:
                     for i in u[1]:
                         assert False
                 else:
                        assert True

#运行函数
class make_html(object):
    #参数是测试套件的列表，每一个套件是一个接口的测试用例集合,第二个参数为html文件存放地址
    def __init__(self,a,b):
        # 获取当前时间，这样便于下面的使用。
        now = time.strftime("%Y-%m-%M-%H_%M_%S", time.localtime(time.time()))
        # 打开一个文件，将result写入此file中
        fp = open(os.path.join(b,'result.html'), 'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='test result', description='result:')
        for i in a:
             runner.run(i )
        fp.close()
if __name__=='__main__':
    h=make_suite('dafaf',[[1,['错误信息是什么']]])
    make_html([h.suite],r'C:\work\lenove_jie_kou\Interface_automation\lenovo_jie_kou')

