# coding:UTF-8
# @Date:2018/7/12
# @Author:cxj

import random, datetime

'''
排列顺序从左至右依次为：六位数字地址码，八位数字出生日期码，三位数字顺序码和一位校验码:
1、地址码 
表示编码对象常住户口所在县(市、旗、区)的行政区域划分代码，按GB/T2260的规定执行。
2、出生日期码 
表示编码对象出生的年、月、日，按GB/T7408的规定执行，年、月、日代码之间不用分隔符。 
3、顺序码 
表示在同一地址码所标识的区域范围内，对同年、同月、同日出生的人编定的顺序号，顺序码的奇数分配给男性，偶数分配给女性。 
4、校验码计算步骤
    (1)十七位数字本体码加权求和公式 
    S = Sum(Ai * Wi), i = 0, ... , 16 ，先对前17位数字的权求和 
    Ai:表示第i位置上的身份证号码数字值(0~9) 
    Wi:7 9 10 5 8 4 2 1 6 3 7 9 10 5 8 4 2 （表示第i位置上的加权因子）
    (2)计算模 
    Y = mod(S, 11)
    (3)根据模，查找得到对应的校验码 
    Y: 0 1 2 3 4 5 6 7 8 9 10 
    校验码: 1 0 X 9 8 7 6 5 4 3 2
'''


def getCheckBit(num17):
    """
    获取身份证最后一位，即校验码
    :param num17: 身份证前17位字符串
    :return: 身份证最后一位
    """
    Wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    checkCode = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    zipWiNum17 = list(zip(list(num17), Wi))
    S = sum(int(i) * j for i, j in zipWiNum17)
    Y = S % 11
    return checkCode[Y]


def getAddrCode():
    """
    获取身份证前6位，即地址码
    :return: 身份证前6位
    """
    addrIndex = random.randint(0, len(addr) - 1)
    return addr[addrIndex]


def getBirthday(start="1900-01-01", end="2000-12-30"):
    """
    获取身份证7到14位，即出生年月日
    :param start: 出生日期合理的起始时间
    :param end: 出生日期合理的结束时间
    :return: 份证7到14位
    """
    days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
    birthday = datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days))
    return datetime.datetime.strftime(birthday, "%Y%m%d")


def getRandomIdCard(sex=1):
    """
    获取随机身份证
    :param sex: 性别，默认为男
    :return: 返回一个随机身份证
    """
    idNumber, addrName = getAddrCode()
    idCode = str(idNumber) + getBirthday()
    for i in range(2):
        idCode += str(random.randint(0, 9))
    idCode += str(random.randrange(sex, 9, 2))
    idCode += getCheckBit(idCode)
    return idCode

addr = [(110000, '北京市'),
(110100, '市辖区'),
(110101, '东城区'),
(110102, '西城区'),
(110103, '崇文区'),
(110104, '宣武区'),
(110105, '朝阳区'),
(110106, '丰台区'),
(110107, '石景山区'),
(110108, '海淀区'),
(110109, '门头沟区'),
(110111, '房山区'),
(110112, '通州区'),
(110113, '顺义区'),
(110114, '昌平区'),
(110115, '大兴区'),
(110116, '怀柔区'),
(110117, '平谷区'),
(110200, '县'),
(110228, '密云县'),
(110229, '延庆县'),
(120000, '天津市'),
(120100, '市辖区'),
(120101, '和平区'),
(120102, '河东区'),
(120103, '河西区'),
(120104, '南开区'),
(120105, '河北区'),
(120106, '红桥区'),
(120107, '塘沽区'),
(120108, '汉沽区'),
(120109, '大港区'),
(120110, '东丽区'),
(120111, '西青区'),
(120112, '津南区'),
(120113, '北辰区'),
(120114, '武清区'),
(120115, '宝坻区'),
(120200, '市辖县'),
(120221, '宁河县'),
(120223, '静海县'),
(120225, '蓟县'),
(130000, '河北省')]

if __name__ == "__main__":
    print((getRandomIdCard()))
