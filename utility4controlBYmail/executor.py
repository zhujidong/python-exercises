# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''

import time
import subprocess as subp

# *** 上级目录在 sys.path 中才能够找到包
from utility4configreader.configreader import ConfigReader
from utility4mail.mailhelper import ImapHelper, SmtpHelper

class Executor(object):
    """
    在主机上系统上执行mail发来的在配置文件字典中列出的命令

    """

    def __init__(self, *config):
        
        _cfg = ConfigReader(*config)
        self.cmd_dict = _cfg.getdict('cmdlist') #命令列表,只能发此列表中的别名
        self.master = _cfg.get('default', 'master') #可以发布命令的邮件地址

        self.last_cmd = '' #最后一次邮件的命令
        self.last_time = 0 #最后一次邮件的时间戳 

    def exec_cmd(self):
        '''
        执行命令(必须是命令列表之中的)
        '''

        orders = _get_orders()
        for order in orders:
            if order in self.cmd_dict.keys():
                cmds = self.cmd_dict[order]
                rs = subp.run(cmds.split(), capture_output=True, encoding='UTF-8')
                print('\r\n------the return .stdout-------\r\n',rs.stdout)
                print('\r\n------the return .stderror-------\r\n',rs.stderr)
            else:
                print(order,'命令不存在')

    def _get_orders(self) -> dict:
        '''
        读取 master 邮件头中的命令信息
        返回 [(标题, 发件人地址, 时间戳),]
        '''
        
        orders = []
        with ImapHelper('..','utility4mail','config.ini') as imap: #测试完这个配置文件放到一个主配置中,不再些放配置文件地址
            #读取今天最新的5个邮件
            #today = time.strftime('%d-%b-%Y')
            today = "15-Mar-2024"
            bheads = imap.get_mails('BODY[HEADER]', F'(SINCE "{today}")', 5)
            for bhd in bheads:
                hd = imap.trans_header(bhd) #解析邮件头
                s = hd.get('Subject')
                f = imap.trans_addr(hd.get('From'))[1] #只要邮件地址
                t = hd.get('Date')
                _struct = time.strptime(t, "%a, %d %b %Y %H:%M:%S +0800")
                t =time.mktime(_struct) #转为时间戳
                orders.append((s, f, t))
        return  orders