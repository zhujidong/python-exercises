# -*- coding:utf_8 -*-

import os
import sys
from configparser import ConfigParser

import time
from schedule import Schedule

'''
测试计划的格式
'''
config = ConfigParser()
config.read( os.path.join(sys.path[0], "config.ini"), encoding='utf_8')
my_schedule = config.items("my_schedule")
print("从配置文件读出计划格式是:\r\n", my_schedule)
'''
    计划的格式是如下的元组列表,含义见 config.ini
    [('6,7', '09:00, 14:00, 17:00'), 
     ('1,5', '08:30, 10:30, 13:30, 15:30, 17:30, 20:00'), 
     ('3', '3600, 06:00, 22:00') ]
'''


'''
修改配置文件，测试下次计划时间
'''
interval, nextdatetime =  Schedule.get_interval(my_schedule)
print("下次计划间隔：", interval)
print("下次计划时间：", time.strftime("%m月%d日%H:%M", nextdatetime))


'''
测试计划任任务执行
'''
def print_time(cur_time)
