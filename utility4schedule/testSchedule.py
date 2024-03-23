# -*- coding:utf_8 -*-

import time
import random

from os import path as ospath
from sys import path as syspath
#将系统查找路径加入到第2人位置。第1个保持为调用python解释器即程序启动路径
syspath.insert(1, ospath.dirname(ospath.dirname(__file__)))

from utility4configreader.configreader import ConfigReader
from schedule import Schedule


def read_config():
    '''
    计划任务的所需的配置文件格式
    '''
    cfg = ConfigReader() #为空默认是程序启动目录下config.ini
    my_schedule = cfg.getschedule("scheduleA")
    print("从配置文件读出的计划格式是:\r\n", my_schedule)

    return my_schedule


def sche_time():
    '''
    测试生成计划下次运行时间
    '''
    interval, nextdatetime =  Schedule._get_interval(read_config())
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
    sche.reg_thread('taskone', task1, ('OK',), ([('6', '60, 01:00, 22:00'),]), (1,10),run_now=False)
    sche.reg_thread('二', task2, ('二',), ([('6', '80, 01:00, 21:00'),]), (0,),True)

    while True:
        str = input()
        if str=='q':
            sche.close_threads()
            break
        elif str=="p":
            print ("输入任务名字暂停任务：")
            str = input()
            rs = sche.pause_thread(str)
            print(rs)

        elif str=="a":
            print ("输入任务名字重启任务：")
            str = input()
            rs = sche.restart_thread(str)
            print(rs)

        elif str=="r":
            print ("输入任务名字立即运行任务：")
            str = input()
            rs = sche.run_thread(str)
            print(rs)

        elif str=="l":
            sche.list_threads()
            


read_config()
#sche_time()
#sche()
    
