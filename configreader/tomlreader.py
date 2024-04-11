# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2024 Copyright(c), WITHOUT WARRANTY OF ANY KIND.
'''


import tomllib
from os import path as ospath
from sys import path as syspath


class TOMLReader(object):
    ''' 
    读取toml类型配置文件,生成字典容器
    '''
    
    _CONFIG_NAME = 'config.toml'

    def __init__(self, *config:str):
        '''
        读取配置文件，将字典数据存入 self._data
        
        :param:
        config:str:配置文件，缺省是__main__所在目录下的config.toml
            以路径和名称多个字符串参数形式给出，从sys.path[0]之后的开始，如： 'path1','path2','filename'
        '''
        
        #配置文件生成的字典
        self._data = {}

        if not config:
            config = (TOMLReader._CONFIG_NAME,)
        config = ospath.join(syspath[0], *config)
        with open(config, "rb") as f:
            self._data = tomllib.load(f)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key:str):
        '''
        字典类的子类，使本类的实例可以像字典或列表方式返回数据
        '''
        return self._data[key]
    
    def __setitem__(self, key:str, value:any):
        '''
        虽然数据应该从toml中读取的，有时也许需要从其它配置文件中读取，放入同一个容器
        ***键名重复，之前的数据会被覆盖
        '''
        self._data[key] = value

    def get(self, key):
        return self._data[key]

    def items(self):
        return self._data.items()

