# -*- coding:utf_8 -*-

import os
import sys
from configparser import ConfigParser

import time
import random
from schedule import Schedule


def read_config():
    '''
    测试计划的格式
    '''
    config = ConfigParser()
    config.read( os.path.join(sys.path[0], "config.ini"), encoding='utf_8')
    my_schedule = config.items("my_schedule")
    print("从配置文件读出的计划格式是:\r\n", my_schedule)
    '''
        计划的格式是如下的元组列表,含义见 config.ini
        [('6,7', '09:00, 14:00, 17:00'), 
         ('1,5', '08:30, 10:30, 13:30, 15:30, 17:30, 20:00'), 
         ('3', '3600, 06:00, 22:00') ]
    '''
    return my_schedule


def sche_time():
    '''
    测试生成计划下次运行时间
    '''
    interval, nextdatetime =  Schedule.get_interval(read_config())
    print("\r\n测试调用方法生成下次计划运行时间：")
    print("下次计划间隔：", interval)
    print("下次计划时间：", time.strftime("%m月%d日%H:%M", nextdatetime))



'''
测试计划任任务执行
'''
def task1(arg):
    rs = random.randint(0, 1)
    print("这是task1，首次传入的参数:",arg)
    print("任务将返回：",rs)
    #根据返回值判断任务执行是否失败，决定是否重试
    return rs

def task2(arg):
    rs = random.randint(0, 1)
    print("\r\n这是任务二，首次传入的参数:",arg)
    print("任务将返回：",rs)
    return rs

def sche():
    sche = Schedule()
    sche.reg_thread('task-one', task1, ('OK',), ([('5', '20, 01:00, 20:00'),]), (1,10),run_now=False)
    sche.reg_thread('任务二', task2, ('二',), ([('5', '60, 01:00, 20:00'),]), (0,),True)

    while True:
        print ("输入q退出")
        print ("输入任务名字取消任务")
        str = input()
        if str=='q':
            sche.close_threads()
            break
        else:
            rs = sche.cancel_thread(str)
            print(rs)


if __name__ == '__main__':

    #read_config()

    #sche_time()

    sche()
    
