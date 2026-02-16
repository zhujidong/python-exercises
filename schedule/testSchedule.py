# -*- coding:utf_8 -*-

import time
import random
from schedule import Schedule


def read_config():
    '''
    计划任务的所需的配置文件格式
    '''

    tom = TOMLReader()['scheduleB']
    print("从tom配置文件读出的计划格式是:\r\n", tom)
    return tom


def trans():
    tom = read_config()
    ttom = Schedule._trans_schedule(tom)

    print("tom:\n",ttom)
    return ttom

def sche_time():
    '''
    测试生成计划下次运行时间
    '''
    ttom = trans()
    interval, nextdatetime =  Schedule._get_interval(ttom)
    print("\r\n测试调用方法生成下次计划运行时间：")
    print("下次计划间隔：", interval)
    print("下次计划时间：", time.strftime("%m月%d日%H:%M", nextdatetime))



'''
测试计划任任务执行
'''
def task1(p):
    rs = random.randint(0, 1)
    print("这是task1，传入的参数:", p)
    print("任务将返回：",rs)
    #根据返回值判断任务执行是否失败，决定是否重试
    if rs==1:
        err = '随机失败'
    else:
        err = '随机成功'

    return rs, err

def task2(kw1=None,kw2='默认'):
    rs = random.randint(0, 1)
    print(F"\r\n这里任务二，位置参数kw1:～{kw1}， 关键字参数kw2：～{kw2}")
    print("任务将返回：",rs)
    if rs==1:
        err = '任务二随机失败'
    else:
        err = '任务二随机成功'

    return rs, err

def sche():
    sche = Schedule()
    s1 = {'retry': [0, 2], 'run': True, '1,2,3,4,5,6,7': ['16:45', '16:47', '21:04']}
    s2 = {'retry': [0, 0], 'run': False, '1,2,3,4,5,6,7': [8, '16:40', '23:55']}

    sche.reg_thread('taskone', task1, ['传入位置参数'],{}, s1)
    #sche.reg_thread('二', task2, ["以位置传入参数"], {'kw2':'位置传关键字'}, s2)

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
            

if __name__ == '__main__':

    from os import path as ospath
    from sys import path as syspath
    #将最先调用python解释器的脚本,即启动程序所在目录的上级目录,加入到系统查找路径
    syspath.append(ospath.dirname(ospath.dirname(__file__)))
    from configreader.tomlreader import TOMLReader

    #read_config()
    
    #trans()

    #sche_time()
    
    sche()
    
