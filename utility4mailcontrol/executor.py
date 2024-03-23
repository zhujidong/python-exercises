# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''

import subprocess as subp

class Executor(object):
    """
    在linux系统上执行mail发来的在配置文件字典中列出的命令

    """

    def __init__(self, cmd_dict={}):
        self.cmd_dict = cmd_dict

    def exec_cmd(self, orders):
        for order in orders:
            if order in self.cmd_dict.keys():
                cmds = self.cmd_dict[order]
                rs = subp.run(cmds.split(), capture_output=True, encoding='UTF-8')
                print('\r\n------the return .stdout-------\r\n',rs.stdout)
            else:
                print(order,'命令不存在')

        
        