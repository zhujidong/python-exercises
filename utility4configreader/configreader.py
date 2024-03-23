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


    def getschedule(self, section) -> list[tuple]:
        '''
        为 Schedule() 提供的按周循环的计划任务表
        *含义及其在配置文件中的格式和见 utility$schedule.config.ini
        
        :return: 返回排好序的格式如下
        [   (1, ['600', '06:00', '22:00']), 
            (3, ['09:00', '14:00', '17:00']), 
            (7, ['08:30', '10:30', '13:30', '15:30', '17:30', '20:00']) ]
        
        '''
        _items = self.items(section)
        
        #整理成按星期排序的计划列表
        temp ={}
        for sche in _items:
            #转换成以星期几为键的字典，以消除重复的计划
            week = sche[0].replace(' ', '').split(',')
            table = sche[1].replace(' ', '').split(',')
            for w in week:
                temp[int(w)] = table
        
        #排序,生成,返回
        return sorted(temp.items(), key=lambda x:x[0])

