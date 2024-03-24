# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''


import subprocess as subp

# *** 上级目录在 sys.path 中才能够找到包
from utility4configreader.configreader import ConfigReader

class Executor(object):
    """
    在主机上系统上执行mail发来的在配置文件字典中列出的命令

    """

    def __init__(self):
        
        self.cmd_dict = ConfigReader().getdict('cmdlist')
        print(self.cmd_dict)
    def exec_cmd(self, orders):
        for order in orders:
            if order in self.cmd_dict.keys():
                cmds = self.cmd_dict[order]
                rs = subp.run(cmds.split(), capture_output=True, encoding='UTF-8')
                print('\r\n------the return .stdout-------\r\n',rs.stdout)
                print('\r\n------the return .stderror-------\r\n',rs.stderr)
            else:
                print(order,'命令不存在')

        
        