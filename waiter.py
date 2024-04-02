# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''



from utility4configreader.configreader import ConfigReader
from utility4controlBYmail.executor import Executor

_config = 'config.ini'
_, info = Executor(_config).exec_cmd()
print(info)

#以上检查邮件执行命令后退出。改由systemd 的：
# my-mcc.service 单元注册为系统任务（非自动启动）。
# my-mcc.timer 单元控制计划时行