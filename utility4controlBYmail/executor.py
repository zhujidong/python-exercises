# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''


import time
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

        self.last_cmds = '' #最后一次邮件的命令
        self.last_time = 0 #最后一次邮件的时间戳 


    def exec_cmd(self):
        '''
        执行命令(必须是命令列表之中的)

        :return:
            rcode:int，命令退出状态码，0正常，-N 被信息N中断
            rmsg:str, subprocess.run（）返回对像的字符值，包括 args,sdout（错误信息stderr也被定向到stdout了）
        '''

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
                
                #多个命令，只记录最后一条的执行时间
                self.last_time = time.time()
                self.last_cmds = cmds
            else:
                rmsg += F'{cmd}命令不存在\n'
            time.sleep(13)

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

        #找到最新的，管理员发送的，半小时内的，大于最后执行时间的（即没有执行过此命令）
        for bhd in bheads:
            hd = imap.trans_header(bhd) #解析邮件头
            s = hd.get('Subject')
            f = imap.trans_addr(hd.get('From'))[1] #只要邮件地址
            t = hd.get('Date')
            _struct = time.strptime(t, "%a, %d %b %Y %H:%M:%S +0800")
            t =time.mktime(_struct) #转为时间戳
            
            # 是管理员发送的； 距今半小时内的；大于最后次执行命令的时间； 
            if f==self.master and (now-t)<1800 and t>self.last_time:
                #将多个命令拆分为列表
                orders = s.replace(' ','').split("#")
                break
        return  orders