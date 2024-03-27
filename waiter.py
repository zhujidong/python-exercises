# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''



from utility4schedule.schedule import Schedule
from utility4configreader.configreader import ConfigReader
from utility4controlBYmail.executor import Executor


waiter = Executor().exec_cmd
table = ConfigReader().getschedule('executor_table')
sche = Schedule()
sche.reg_thread('waiter', waiter, (), table, (0,0),run_now=False)

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


