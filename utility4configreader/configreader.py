# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''

from os import path
from sys import path as syspath
from configparser import ConfigParser

class ConfigReader(ConfigParser):
    ''' 
    读取配置文件,并转换数据格式 

    '''

    CONFIG_NAME = 'config.ini'

    def __init__(self, config_name=None) -> None:
        '''
        读取配置文件，默认为 CONFIG_NAME 变量定义的文件
        '''

        #调用父类的三种方法，最新不用传递self了？
        #super(ConfigReader,self).__init__()
        #ConfigParser.__init__(self)
        super().__init__()
        
        if not config_name:
            config_name = ConfigReader.CONFIG_NAME
        self.read(path.join(syspath[0], config_name), encoding='utf_8')
        return None


    def getdict(self, section) -> dict:
        '''
        将items()方法得到的元组列表，转换为字典
        
        '''
        _items = self.items(section)
        _dict = { }
        for key, value in _items:
            _dict[key] = value
        return _dict
