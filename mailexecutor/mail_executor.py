# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2024 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''



import os
import sys
import time

import shlex
import subprocess

import traceback
from subprocess import SubprocessError
from imaplib import IMAP4
from smtplib import SMTPException

#sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from mailhelper.mailhelper import ImapHelper, SmtpHelper
from configreader.tomlreader import TOMLReader


class MailExecutor(object):
    """
    在主机上系统上执行mail发来的（在邮件标题中）命令

    """

    CONFIG = TOMLReader()['mailexecutor']

    def __init__(self, config:dict={}):
        '''
        初始化实例属性存储配置信息；初始化实例属性存储临时文件名。

        config:dict，一般是从配置文件中读取的字典，其中主要成员如下，其它见config.toml：
            tempfile：值为一个临时文件名，只是用文件的时间记录上次处理邮件的时间
            master：dict，只接收这些邮件地址发来的命令
            cmdlist：dict,只有字典中的命令才能被执行
            mailhelper：dict,供邮件服务使用
        '''

        if config == {}:
            self.config = MailExecutor.CONFIG
        else:
            self.config = config

        #临时文件，只是取它的更时间用，每次调用本方法会，都会写一下此文件，更新其时间
        self.tempfile = os.path.join(sys.path[0], self.config['tempfile'])


    def fetch_mails(self) -> list:
        '''
        读取最新的6封邮件的头信息，将符合条件的命令邮件标题，拆分成命令列表

        :return:
            commands:list 命令列表。没找到符合条件地返回空
                *最近发的（即最后发送的）在列表的前面
        '''
       
        i = 0
        commands = []

        """虽然time的altzone、daylight、tzname、timezone常量在加载时确定，但tzset()等作用，
        可能会不正常。建议用localtime()生成的结构化时间的tm_zone和tm_gmtoff属性 """
        now_stamp = time.time()
        now_struct = time.localtime(now_stamp)

        """上次检查邮件命令的时间戳（临时文件的时间戳）: 当调用本方法，就会写一下临时文件，表示这个时
        间点的之前的邮件命令都被执行过（不管成功与否），只有大于此时间的邮件，才会再次被返回 """
        try:
            last_stamp = os.path.getmtime(self.tempfile)
        except:
            last_stamp = 0

        #抓取今天0点之后，最后收到的6个邮件的头部（＊注意：这之中不一定全是管理员发的命令）
        with ImapHelper(self.config['mailhelper']) as imap:
            now_str = time.strftime('%d-%b-%Y', now_struct) #same "15-Mar-2024"
            mail_headers = imap.get_mails('BODY[HEADER]', F'(SINCE "{now_str}")', 6)
                
        #找到管理员发送、设置的时间内（各种原因时间太久没执行也做废）没有执行过的命令
        for mail_header in mail_headers:
            header = imap.parse_header(mail_header) #解析邮件头
            mail_subject = header.get('Subject','').replace(' ','').lower()
            mail_from = header.get('From').addresses[0].addr_spec #只要邮件地址
            mail_date = header.get('Date')

            #将邮件日期(时间字符串)转为结构化时间，再转为时间戳，
            mail_struct = time.strptime(mail_date, "%a, %d %b %Y %H:%M:%S %z")
            mail_stamp = time.mktime(mail_struct)
            #当前时区比邮件时区多了多少？给其加上，转为当前时区时间戳
            mail_stamp += (now_struct.tm_gmtoff - mail_struct.tm_gmtoff)
            
            #符合条件的命令邮件 
            if( mail_from in self.config['master'].values()  #管理员列表中的
                and now_stamp - mail_stamp < self.config['recent_time']  #没有超时
                and mail_stamp > last_stamp  #没有执行过
                and mail_subject #有主题
            ):
                #较早发的邮件插在前面先执行，较晚（最近发的）在后面，后执行
                commands = mail_subject.split(self.config['separator']) + commands
                i += 1
                if i == self.config['latest_mail']: #只要执行最后的几个邮件命令
                    break
        #写一下文件，更新时间戳，记录本次执行的时间
        with open(self.tempfile, 'w') as f:
            pass
        return commands


    def execute_commands(self, commands:list=[]) -> list[subprocess.CompletedProcess]:
        '''
        执行命令(必须是命令列表之中的),返回结果
        
        :param:
            commands:命令列表
                ＊此命令不是真正的命令，而是配置文件cmdlist段中定义的变量，
                实际命令可以写在一个字符串中，也可以是命令和参数的列表。
        :return:
            results：列表，元素是subprocess.run() 的返回的对像。或者字符串。
        '''

        results = []
        for cmd in commands:
            
            #将命令和参数分开
            cmd_h = cmd.split(' ',1)[0]
            args = cmd.removeprefix(cmd_h)
            
            if cmd_h in self.config['cmdlist'].keys():
                cmd_str = self.config['cmdlist'][cmd_h]

                #没参数但命令串中有参数；有参数但命令串没参数
                if (args=='' and '{args}' in cmd_str) \
                or (args!='' and '{args}' not in cmd_str):
                    results.append(F"\n{cmd}》\n参数数量错误\n\n")
                else:
                    #合法的命令，但有参数的要处理一下
                    if args!='':
                        cmd_str = cmd_str.format(args=args)
                                
                    rs = subprocess.run(
                        shlex.split(cmd_str), 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        encoding='UTF-8',
                        timeout=30
                    )
                    results.append(rs)
            elif cmd=='help':
                results.append('\n－－－ list －－－\n')
                for v in self.config['cmdhelp'].values():
                    results.append(F"{v}\n\n")
            else:
                results.append(F"\n{cmd}》\n命令不存在\n\n")
        return results


    def send_results(self, results:list, recipient:dict={}):
        '''
        将命令执行结果通过邮件发送
        
        :param:
            results:命令执行结果列表，元素是subprocess.CompletedProcess或字符串
            recipient:收件人字典，名字为键，地址为值。
                ＊默认发送给所以有权执行邮件命令邮件地址
        :return:

        '''
        if recipient=={}:
            recipient = self.config['master']
        
        msg = ''
        for rs in results:
            if type(rs)==str:
                msg += rs
            else:
                msg += F"\n》{' '.join(rs.args)}》\n{'执行成功:' if rs.returncode==0 else '执行失败:'}\n"
                msg += rs.stdout + rs.stderr + '\n'

        with SmtpHelper(self.config['mailhelper']) as smtp: 
            smtp.send_mail( recipient, '邮件命令执行结果', msg )


    def run(self):
        err=''
        try:
            print('检查邮件，看是否有需要执行的命令...')
            commands = self.fetch_mails()
            if commands:
                print('正在执行，结果将通过邮件发送...')            
                results = self.execute_commands(commands)
                self.send_results(results)
            else:
                print('没有要执行的命令')
        except SubprocessError:
            err = F"》执行命令子进程错误:{traceback.format_exc()}"
        except IMAP4.error:
            err = F"》收件服务出错:{traceback.format_exc()}"
        except SMTPException:
            err = F"》发件服务出错:{traceback.format_exc()}"
        except Exception:
            err = F"》罕见错误:{traceback.format_exc()}"
        finally:
            print(err)

if __name__ == '__main__':
    MailExecutor().run()