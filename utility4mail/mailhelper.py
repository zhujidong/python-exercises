# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''

#import time
#import random

import os
import sys
from configparser import ConfigParser

#import smtplib
#from email.message import EmailMessage
#from email.headerregistry import Address
#from ssl import SSLError


import imaplib
from email.policy import default
from email.parser import BytesParser

class ImapHelper(object):

    def __init__(self) -> None:

        config = ConfigParser()
        config.read( os.path.join(sys.path[0], "mail.ini"), encoding='utf_8')
        self.username = config['mail']['username']
        self.password = config['mail']['password']
        self.imaphost = config['mail']['imaphost']
        self.imapport = config['mail']['imapport']
        
        self.imap = None        
        self.exc_type = None
        self.exc_value = None
        self.exc_tb = None

    def __enter__(self) -> object:
        """ 
        登录imap收件服务，将句柄赋值给实例变量self.imap 
        *此方法只会被 with...as 语句块调用

        :return: 本类的实例对像
        """
        
        self.imap = imaplib.IMAP4_SSL(self.imaphost, self.imapport)
        self.imap.login(self.username, self.password)
        ''' 
        网易服务器要求客户端发送一个ID命令，否则认为是不安全的。
        *imap求每条命令前有一个标签，以便异步响应，所以调用imap._new_tag()生成；
        *要以\r\n结尾，否则一直等待结束；这个通信是字节串，所以用 “ b ” 
        '''
        tag = self.imap._new_tag() 
        self.imap.send(tag + b' ID ("name" "zbot" "version" "1.0" "vendor" "J.D.zhu")\r\n')
        return self


    def __exit__(self, exc_type, exc_value, exc_tb):
        """ 
        with...as语句块结束后，会调用此方法，如果语句块没有异常，三个参数值是None
        """
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_tb = exc_tb
        self.imap.logout()


    def get_mails(self, parts='BODY[HEADER]', criterion='(UNSEEN)') -> list:
        '''
        读取收件箱的邮件内容
        :param:
            parts:str, 给IMAP4.fetch()默认为读取邮件头部信息'BODY[HEADER]'
                    BODY[ ]相当于RFC822，返回的是全部邮件内容
            criterion:str,给IMAP4.search()的参数. 默认为未读邮件'(UNSEEN)'
        :return:
            list: 邮件内容的列表, []空表示没有相关邮件
        '''   

        #选择邮箱,默认参数是INBOX,返回: ( 状态，[b'邮件数量'] ) 
        self.imap.select()
        #response是一个列表；第一个元素是‘空格分隔的邮件号’
        _, resp = self.imap.search(None, criterion) 
        numbers = resp[0].split() 

        bmails = []
        for number in numbers:
            status, response = self.imap.fetch(number, parts) 
            bmails.append(response[0][1])
        return bmails            


    def trans_header(self, bmail):
        '''
        转换头部信息
        :param:
            bmail:字节串,应该是标准的头部或全部信息
        :return:
            EmailMessage消息对像
        '''
        return BytesParser(policy=default).parsebytes(bmail, headersonly=True)



class MailHelper(object):
    
    def __init__(self) -> None:

        config = ConfigParser()
        config.read( os.path.join(sys.path[0], "mail.ini"), encoding='utf_8')

        self.username = config['mail']['username']
        self.password = config['mail']['password']
        self.smtphost = config['mail']['smtphost']
        self.smtpport = config['mail']['smtpport']
        self.imaphost = config['mail']['imaphost']
        self.imapport = config['mail']['imapport']

        self.imap = None
        self.smtp = None


    def _login_imap(self):
        """ 
        登录imap收件服务，将句柄赋值给实例变量。 
        
        :return:
            失败返回-1, 成功返回邮件的数量
        """
        
        self.imap = imaplib.IMAP4_SSL(self.imaphost, self.imapport)
        self.imap.login(self.username, self.password)
        tag = self.imap._new_tag() 
        self.imap.send(tag + b' ID ("name" "zbot" "version" "1.0" "vendor" "J.D.zhu")\r\n')
        ''' 
            网易服务器要求客户端发送一个ID命令，否则认为是不安全的。
            #imap求每条命令前有一个标签，以便异步响应，所以调用imap._new_tag()生成；
            #要以\r\n结尾，否则一直等待结束；这个通信是字节串，所以用 “ b ” 
        '''


        #self.imap.select()[1][0].decode() #默认参数是INBOX,返回: ( 状态，[b'邮件数量'] ) 

        return self.imap.select()


    def _login_smtp(self):
        '''
        登录smtp发件服务器，将句柄赋值给实例变量

        '''   
        self.smtp = smtplib.SMTP_SSL(self.smtphost, self.smtpport)
        self.smtp.login(self.username, self.password)
        return None


    def __del__(self):
        self.imap.logout()
        self.smtp = None



    def send_notice(self, fields, notice:list, name_email:list, max_size=0) -> int:
        '''
        发送一条通知内容给接收人
            
        :param:
            fields: Field类实例，属性名为字段名，值对应内容元组的索引
            notice：通知信息元组
            name_email：(收信人名称，email地址）的列表
            max_size：允许附件大小，0为使用配置文件中设置的大小
        :return:
            int:发送成功的通知id
        '''
        msg = EmailMessage()
        msg['Subject'] = notice[fields.title]
        msg['From'] = Address(str(notice[fields.noticeid])+' -'+self.sender, addr_spec = self.username) 
        receivers = []
        header_to = []
        for rece in name_email:
            receivers.append(rece[1]) 
            header_to.append( Address(rece[0], addr_spec=rece[1]) )
        msg['To'] = header_to
        
        #纯文本邮件正文 
        text = "很遗憾，您的客户端不支持HTML格式邮件，无法查看。"
        msg.set_content(text)
               
        #html格式邮件正文
        htmls =[]
        htmls.append(self.html_top)
        htmls.append(
            F'''<table><tr><th>ID: </th><th>{notice[fields.noticeid]}</th></tr>
            <tr><td>时间:</td><td>{notice[fields.pubdate]}</td></tr>
            <tr><td>标题:</td><td>{notice[fields.title]}</td></tr>
            <tr><td>部门:</td><td>{notice[fields.department]}</td></tr>
            <tr><td>发/审:</td><td>{notice[fields.pubname]} / {notice[fields.reviewer]}</td></tr>
            <tr><td>接收:</td><td>{notice[fields.receiver]}</td></tr>
            <tr><td>正文:</td><td>{notice[fields.content] if notice[fields.content]!='null' else '[ 无正文 ]'}</td></tr>
            <tr><td>附件:</td><td>{('应有'+str(notice[fields.amount])+'个，名称如下') if notice[fields.amount]>0 else ''}</td></tr>
            <tr><td></td><td>{notice[fields.attname] if notice[fields.attname] else '[ 无附件 ]'}</td></tr></table><br/>'''
        )
        htmls.append(self.html_bottom)
        msg.add_alternative(' '.join(htmls), subtype="html") 

        #有附件，则添加附件
        if notice[fields.amount] > 0:
            am = Attachment(notice[fields.pubdate], notice[fields.noticeid])
            try:            
                filename_list = am.get_filename(max_size)
                for filename in filename_list:
                    base_name = am.base_name(filename)
                    flag = filename[-8:]
                    if flag == '-OVF.txt':
                        base_name = '文件过大-' + base_name
                        am_content = '此附件过大，无法通过邮件发送'.encode()
                    elif flag == '-ZRO.txt':
                        base_name = '文件为空-' + base_name
                        am_content = '此附件为空，可能是下载时出错'.encode()
                    else:
                        with open(filename,'rb') as f:
                            am_content = f.read()
                    msg.add_attachment( 
                        am_content, maintype = 'application', subtype = 'octet-stream', 
                        filename = base_name
                    )
            except FileNotFoundError:
                msg.add_attachment( 
                    '附件丢失或未下载。可以发送xxx命令重新下载并发送给你。'.encode(),
                    maintype = 'application', subtype = 'octet-stream', 
                    filename = '附件丢失或未下载.txt'
                )
        #endif 添加附件完成

        self._login_smtp()
        self.smtp.sendmail(self.username, receivers, msg.as_string())
        
        try:
            self.smtp.quit()
        except (SSLError, smtplib.SMTPServerDisconnected):
            self.smtp.close()
        except:
            self.smtp = None

        return notice[fields.noticeid]


    def send_msg(self, content:list[list], name_email:list[tuple], title:str) -> str:
        ''' 
        发送信息给收件人
        :param:
            msg:list[list], 发送的信息，会被放在表格中发送
            name_email：(name,email）组成的元组列表
        :return:
            str: ’‘（null）表示成功，否则是错误信息
        '''   
        msg = EmailMessage()
        msg['Subject'] = title 
        msg['From'] = Address(self.sender, addr_spec = self.username) 
        receivers = [] #收件人email列表
        header_to = [] #邮件内容中构造的收件人信息
        for rece in name_email:
            receivers.append(rece[1]) 
            header_to.append( Address(rece[0], addr_spec=rece[1]) )
        msg['To'] = header_to 
        
        #纯文本邮件正文 
        text = "很遗憾，您的客户端不支持HTML格式邮件，无法查看。"
        msg.set_content(text)
               
        #html格式邮件正文
        htmls =[]
        htmls.append(self.html_top)
        htmls.append('<table>')
        for line in content:
            tr = '<tr>'
            for td in line:
                tr += F'<td>{td}</td>'
            tr += '</tr>'
            htmls.append(tr)
        htmls.append('</table>')
        htmls.append(self.html_bottom)
        msg.add_alternative(' '.join(htmls), subtype="html") 

        info = ''
        try:
            self._login_smtp()
            self.smtp.sendmail( self.username, receivers, msg.as_string() )
        except smtplib.SMTPException:
            info = '邮件发送失败（发件服务器问题）。'
        except:
            info = '邮件发送失败（未知原因）。'
        finally:
            try:
                self.smtp.quit()
            except (SSLError, smtplib.SMTPServerDisconnected):
                self.smtp.close()
            except:
                self.smtp = None
        return info