# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2024 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''



import time
from os import path as ospath
from sys import path as syspath
import subprocess as subp
# subprocess 所有异常类的基类
#subp.SubprocessError  

# ***mailhelper需在 sys.path 中才能查找到
from mailhelper.mailhelper import ImapHelper, SmtpHelper


class Executor(object):
    """
    在主机上系统上执行mail发来的（在邮件标题中）命令

    """

    def __init__(self, config:dict):
        '''
        初始化实例属性存储配置信息；初始化实例属性存储临时文件名。

        config:dict，一般是从配置文件中读取的字典，其中主要成员如下，其它见config.toml：
            tempfile：值为一个临时文件名，只是用文件的时间记录上次处理邮件的时间
            master：dict，可以用来发送命令的邮箱
            cmdlist：dict,只有字典中的命令才能被执行
            mailhelper：dict,供邮件服务使用
        '''

        self.config = config
        self.tempfile = ospath.join(syspath[0], self.config['tempfile'])
        ''' 当 self._get_orders()从邮箱取得一个新的命令时，就会重新生成此临时文件，借以记录此次命令被执行的时间。
            当再次从邮箱中读取新的命令时，只有比这个临时文件的日期晚的邮件，才是新发来的命令。
        '''


    def exec_cmd(self, cmds=None):
        '''
        执行命令(必须是命令列表之中的)
        
        :param:
            cmds:列表，需是命令列表中定义好的。缺省调用self._get_orders()从邮件中读取

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
            if cmd in self.config['cmdlist'].keys():
                cmd = self.config['cmdlist'][cmd]
                split_cmd = cmd.split()  #shlex.split() 复杂的也许需要此方法序列化
                rs = subp.run(split_cmd, stdout=subp.PIPE, stderr=subp.STDOUT, encoding='UTF-8')
                if rs.returncode!=0:
                    rcode = rs.returncode
                rmsg += 'args: ' + ' '.join(rs.args) + '\n'
                rmsg += 'code: ' + str(rs.returncode) + '\n'
                rmsg += 'stdout: ' + rs.stdout +'\n\n'
            else:
                rmsg += F'{cmd}命令不存在\n'
            time.sleep(5)

        if not rmsg:
            rmsg ='当前没有需要执行的命令'
        else:
            with SmtpHelper(self.config['mailhelper']) as smtp: 
                #将执行结果发送给所有的管理员
                smtp.send_mail( self.config['master'], '#'.join(cmds)+'执行结果', rmsg )
 
        return rcode, rmsg


    def _get_orders(self) -> list:
        '''
        读取最新的5封邮件的头信息，将符合条件的命令邮件标题，拆分成命令列表

        :return:
            orders:list 命令列表。没找到符合条件地返回空
        '''
       
        i = 0
        orders = []

        #当前时间戳
        now_stamp = time.time()
        #当前时间结构化表示
        now_struct = time.localtime(now_stamp)
        ''' 虽然time的altzone、daylight、tzname、timezone常量在加载时确定，但tzset()等作用，可能会不正常。
            建议用localtime()生成的结构化时间的tm_zone和tm_gmtoff属性
        '''
        
        #上次执行邮命令的时间戳（临时文件的时间戳）
        try:
            last_stamp = ospath.getmtime(self.tempfile)
        except:
            last_stamp = 0

        #读取最新的六封邮件头部（防止垃圾邮件影响要多读几封）
        with ImapHelper(self.config['mailhelper']) as imap:
            #生成当前时间字符串，符合邮件服务器格式
            now_str = time.strftime('%d-%b-%Y', now_struct)
            #now_str = "15-Mar-2024"
            mail_headers = imap.get_mails('BODY[HEADER]', F'(SINCE "{now_str}")', 6)
                
        #找到管理员发送、设置的时间内、大于最后执行时间（即没有执行过）的命令
        for mail_header in mail_headers:
            header = imap.parse_header(mail_header) #解析邮件头
            mail_subject = header.get('Subject')
            mail_from = header.get('From').addresses[0].addr_spec #只要邮件地址
            mail_date = header.get('Date')

            #将邮件日期(时间字符串)转为结构化时间，再转为时间戳，
            mail_struct = time.strptime(mail_date, "%a, %d %b %Y %H:%M:%S %z")
            mail_stamp = time.mktime(mail_struct)
            #当前时区比邮件时区多了多少？给其加上，转为当前时区时间戳
            mail_stamp += (now_struct.tm_gmtoff - mail_struct.tm_gmtoff)
            
            #是管理员发送的; #最近时间内的；#大于上次执行的时间； 
            if ( mail_from in self.config['master'].values()
                and now_stamp - mail_stamp < self.config['recent_time']
                and mail_stamp > last_stamp
            ):
                #创建或重写文件，只为用文件时间记录邮件被处理的时间。
                with open(self.tempfile, 'w') as f:
                    pass
  
                _order = mail_subject.replace(' ','').lower().split(self.config['separator'])
                print(_order)
                if _order:
                    orders.extend(_order)
                    i += 1

                if i == self.config['latest_mail']:
                    break

        return  orders