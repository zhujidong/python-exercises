# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''

from os import path as ospath
from sys import path as syspath
from configparser import ConfigParser

class ConfigReader(ConfigParser):
    ''' 
    读取配置文件,并转换数据格式 

    '''

    _CONFIG = 'config.ini'

    def __init__(self, *config:str) -> None:
        '''
        读取配置文件，默认为 CONFIG_NAME 变量定义的文件
        
        :param:
        config:配置文件的路径和名称,从sys.path[0]之后开始如： 'path1','path2','filename'
            默认为当前（程序启动）目录下的 config.ini
        '''

        #调用父类的三种方法，最新不用传递self了？
        #super(ConfigReader,self).__init__()
        #ConfigParser.__init__(self)
        super().__init__()
        
        if not config:
            config = (ConfigReader._CONFIG,)
        
        self.read(ospath.join(syspath[0], *config), encoding='utf_8')
        return None


    def getdict(self, section) -> dict:
        '''
        将section段的内容读取为字典
        '''
        _items = self.items(section)
        _dict = { }
        for key, value in _items:
            _dict[key] = value
        return _dict
