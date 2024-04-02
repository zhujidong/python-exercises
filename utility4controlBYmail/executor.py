# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''



import time
from os import path as ospath
from sys import path as syspath
import subprocess as subp
# subp.SubprocessError  #subprocess 所有异常类的基类

# *** 上级目录在 sys.path 中才能够找到包
from utility4configreader.configreader import ConfigReader
from utility4mail.mailhelper import ImapHelper, SmtpHelper


class Executor(object):
    """
    在主机上系统上执行mail发来的在配置文件字典中列出的命令
    """

    def __init__(self, *config):
        '''
        可以给给出读取配置文件的路径
        '''
        self.config = config
        _cfg = ConfigReader(*self.config)
        self.cmd_dict = _cfg.getdict('executor_cmdlist') #命令列表,只能发此列表中的别名
        self.master = _cfg.get('executor', 'master') #可以发布命令的邮件地址
        self.tmpfile = ospath.join(syspath[0], _cfg.get('executor', 'tmpfile_name'))

    def exec_cmd(self, cmds=None):
        '''
        执行命令(必须是命令列表之中的)
        
        :param:
            cmds:列表，元素需是命令列表中定义好的。缺省调用self._get_orders()从邮件中读取

        :return:
            rcode:int，命令退出状态码，0正常，-N 被信息N中断
            rmsg:str, subprocess.run（）返回对像的字符值，包括 args,sdout（错误信息stderr也被定向到stdout了）
        '''

        if not cmds:
            cmds = self._get_orders()
        rcode = 0
        rmsg = ''
        for cmd in cmds:
            #此命令在列表之中
            if cmd in self.cmd_dict.keys():
                cmd = self.cmd_dict[cmd]
                cmd_l = cmd.split()  #shlex.split() 复杂的也许需要此方法序列化
                rs = subp.run(cmd_l, stdout=subp.PIPE, stderr=subp.STDOUT, encoding='UTF-8')
                if rs.returncode!=0:
                    rcode = rs.returncode
                rmsg += 'args: ' + ' '.join(rs.args) + '\n'
                rmsg += 'code: ' + str(rs.returncode) + '\n'
                rmsg += 'stdout: ' + rs.stdout +'\n\n'
            else:
                rmsg += F'{cmd}命令不存在\n'
            time.sleep(7)

        if not rmsg:
            rmsg ='当前没有需要执行的命令'
        else:
            with SmtpHelper(*self.config) as smtp: 
                smtp.send_mail( self.master, rmsg, '#'.join(cmds)+'执行结果')
 
        return rcode, rmsg


    def _get_orders(self) -> dict:
        '''
        读取最新的5封邮件的头信息，将符合条件的命令邮件标题，拆分成命令列表

        :return:
            orders:list 命令列表。没找到符合条件地返回空
        '''
       
        orders = []
        now = time.time()

        #读取今天最新的五封邮件头部
        with ImapHelper(*self.config) as imap:
            today = time.strftime('%d-%b-%Y')
            #today = "15-Mar-2024"
            bheads = imap.get_mails('BODY[HEADER]', F'(SINCE "{today}")', 5)
        
        #读读临时文件时间，此文件创建之后的邮件才是没被执行的新邮件
        try:
            last_runtime = ospath.getmtime(self.tmpfile)
        except:
            last_runtime = 0

        #找到最新的，管理员发送的，半小时内的，大于最后执行时间的（即没有执行过此命令）
        for bhd in bheads:
            hd = imap.trans_header(bhd) #解析邮件头
            s = hd.get('Subject')
            f = imap.trans_addr(hd.get('From'))[1] #只要邮件地址
            t = hd.get('Date')
            _struct = time.strptime(t, "%a, %d %b %Y %H:%M:%S +0800")
            t =time.mktime(_struct) #转为时间戳
            
            # 是管理员发送的； 距今半小时内的；大于上次读取的邮件时间； 
            if f==self.master and (now-t)<1800 and t>last_runtime:
                #创建此文件只为记录创建它时的的这个时间，此时间前的最新邮件将被执行
                with open(self.tmpfile, 'w') as f:
                    pass
                #将多个命令拆分为列表，传给执行函数
                orders = s.replace(' ','').split("#")
                break
        return  orders