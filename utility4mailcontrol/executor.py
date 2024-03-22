# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''

import os
import sys
from configparser import ConfigParser

import subprocess as subp

class executor(object):
    """
    在linux系统上执行mail发来的在配置文件字典中列出的命令

    """

    def __init__(self):
        config = ConfigParser()
        config.read( os.path.join(sys.path[0], "config.ini"), encoding='utf_8')
        items = config.items('cmd_dict')
        self.cmd_dict = {}
        for key, value in items:
            self.cmd_dict[key] = value

    def exec_cmd(self, orders):
        for order in orders:
            if order in self.cmd_dict.keys():
                cmds = self.cmd_dict[order]
                rs = subp.run(cmds.split(), capture_output=True, encoding='UTF-8')
                print('\r\n------the return .stdout-------\r\n',rs.stdout)
            else:
                print('命令不存在')



if __name__ == '__main__':

    executor().exec_cmd(['frpc2status',])

        
        