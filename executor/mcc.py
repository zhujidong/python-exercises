# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2024 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''


if __name__ == '__main__':
    from os import path as ospath
    from sys import path as syspath
    #将当前目录的上级目录加入到sys.path
    syspath.insert(1, ospath.dirname(ospath.dirname(__file__)))

    from configreader.tomlreader import TOMLReader
    from executor import Executor

    _, info = Executor(TOMLReader()['executor']).exec_cmd()
    print(info)

    # my-mcc.service 单元注将本脚本注册为系统任务（非自动启动）。
    # my-mcc.timer 单元控制计划时行