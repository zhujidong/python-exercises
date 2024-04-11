# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2024 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''



import time
from os import path as ospath
from sys import path as syspath
import subprocess as subp
# subp.SubprocessError  #subprocess 所有异常类的基类

# ***mailhelper需在 sys.path 中才能查找到
from mailhelper.mailhelper import ImapHelper, SmtpHelper


class Executor(object):
    """
    在主机上系统上执行mail发来的在配置文件字典中列出的命令
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
        self.tempfile = ospath.join(syspath[0], config['tempfile'])
        ''' 当 self._get_orders()从邮箱取得一个新的命令时，就会重新生成些临时文件，借以记录这条命令被执行的时间。
            当再次从邮箱中读取新的命令时，会和这个得时文件的生成时间来比较，只有比这个临时文件晚的邮件，才是新发来的命令。
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
       
        orders = []
        now_stamp = time.time() #当前时间戳
        local_struct = time.localtime(now_stamp)
        ''' 当前时间结构，虽然time的altzone、daylight、tzname、timezone常量在加载时确定，
            但tzset()等作用，可以会不正常，建议用localtime()的tm_zone和tm_gmtoff属性
        '''
        try:
            #时间文件的时间戳，应该是个本地化时间吧
            last_time = ospath.getmtime(self.tempfile)
        except:
            last_time = 0

        #读取今天最新的五封邮件头部
        with ImapHelper(self.config['mailhelper']) as imap:
            today = time.strftime('%d-%b-%Y', local_struct)
            #today = "15-Mar-2024"
            bheads = imap.get_mails('BODY[HEADER]', F'(SINCE "{today}")', 5)
                
        #找到最新的，管理员发送的，半小时内的，大于最后执行时间的（即没有执行过此命令）
        for bhd in bheads:
            hd = imap.parse_header(bhd) #解析邮件头
            s = hd.get('Subject')
            f = hd.get('From').addresses[0].addr_spec #只要邮件地址
            t = hd.get('Date')

            #将邮件日期时间字符串，转为时间戳
            hd_struct = time.strptime(t, "%a, %d %b %Y %H:%M:%S %z")
            t_stamp = time.mktime(hd_struct)
            #当前时区比邮件时区多了多少？给其加上，转为当前时区时间戳
            t_stamp += (local_struct.tm_gmtoff-hd_struct.tm_gmtoff)
            
            # 是管理员发送的； 距今半小时内的；大于上次读取的邮件时间； 
            if f in self.config['master'].values() \
            and (now_stamp-t_stamp)<1800 and t_stamp>last_time:
                with open(self.tempfile, 'w') as f:
                    #创建或重写文件，只为用文件时间记录邮件被处理的时间。
                    pass
            
                orders = s.replace(' ','').lower().split("=")
                break #只要最新的一个邮件
        return  orders