# -*- coding:utf_8 -*-

'''
The MIT License (MIT) 
zhujidong 2021 Copyright(c), WITHOUT WARRANTY OF ANY KIND.

'''


# *** 上级目录在 sys.path 中才能够找到包
from utility4configreader.configreader import ConfigReader
#from ssl import SSLError

from email.policy import default
from email.parser import BytesParser
from email.utils import parseaddr
from imaplib import IMAP4_SSL
#from imaplib.IMAP4 import error as imapError #任何错误都将引发该异常。


class ImapHelper(object):

    def __init__(self, *config:str) -> None:
        '''
        登录imap收件服务器，将句柄赋值给实例变量self.imap
        设置实例变量存储由with语句（在__exit__中传递过来）返回的执行信息
        '''

        self.config = config
        _dict = ConfigReader(*self.config).getdict('mail')

        self.imap = IMAP4_SSL(_dict['imaphost'], _dict['imapport'])
        self.imap.login(_dict['username'], _dict['password'])
        _tag = self.imap._new_tag() 
        self.imap.send(_tag + b' ID ("name" "zbot" "version" "1.0" "vendor" "J.D.zhu")\r\n')
        ''' 
        网易服务器要求客户端发送一个ID命令，否则认为是不安全的。
        *imap求每条命令前有一个标签，以便异步响应，所以调用imap._new_tag()生成；
        *要以\r\n结尾，否则一直等待结束；这个通信是字节串，所以用 “ b ” 
        '''
        self.exc_type = None
        self.exc_value = None
        self.exc_tb = None
        self.error = None #错误信息

        
    def __enter__(self) -> object:
        '''
        *此方法只会被 with...as 语句块调用, 为as提供一个值
        :return: 本类的实例对像
        '''
        return self


    def __exit__(self, exc_type, exc_value, exc_tb):
        '''
        with...as语句块是否正常结束后，会调用此方法，如果语句块没有异常，三个参数值是None
        '''
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_tb = exc_tb
        self.imap.close()
        self.imap.logout()


    def get_mails(self, parts='BODY[HEADER]', criterion='(UNSEEN)', last=0) -> list:
        '''
        读取收件箱的邮件内容，返回邮件列表
        
        :param:
            parts:str, 给IMAP4.fetch()默认为读取邮件头部信息'BODY[HEADER]'
                    BODY[]相当于RFC822，返回的是全部邮件内容
            criterion:str,给IMAP4.search()的参数. 默认为未读邮件'(UNSEEN)'
            last:读取最后（最新）收到的几个邮件。如果缺省或者大于邮件数量，则读取全部邮件
        :return:
            bmails: 邮件内容的列表,内容是未经解析的字节串。 []空表示没有相关邮件
        '''   

        #选择邮箱,默认参数是INBOX,返回: ( 状态，[b'邮件数量'] ) 
        self.imap.select()
        #response是一个列表；第一个元素是‘空格分隔的邮件号’
        _, resp = self.imap.search(None, criterion) 
        numbers = resp[0].split()
        #取最新的几个邮件ID
        if last>0 and last<len(numbers):
            numbers = numbers[-(last):]
    
        bmails = []
        #以新旧顺序先读取字节串
        for number in reversed(numbers):
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

    
    def trans_addr(self, _from:str) -> tuple:
        '''
        将邮件中from发件人信息字符串转换为 ('username', 'useraddr@abc.com') 的元组
        '''
        return parseaddr(_from)



from email.message import EmailMessage
from email.headerregistry import Address
from smtplib import SMTP_SSL
#from smtplib import SMTPException #OSError 的子类，它是本模块提供的所有其他异常的基类。


class SmtpHelper(object):

    def __init__(self, *config) -> None:
        '''
        登录SMTP服务器，将句柄赋值给实例变量self.smtp
        设置实例变量存储由with语句（在__exit__中传递过来）返回的执行信息
        '''

        self.config = config
        _dict = ConfigReader(*self.config).getdict('mail')

        self.smtp = SMTP_SSL(_dict['smtphost'], _dict['smtpport'])
        self.smtp.login(_dict['username'], _dict['password'])

        self.username = _dict['username']
        self.exc_type = None
        self.exc_value = None
        self.exc_tb = None
        self.error = None #错误信息

         
    def __enter__(self) -> object:
        '''
        *此方法只会被 with...as 语句块调用，为as提供一个值
        :return: 本类的实例对像
        '''
        return self


    def __exit__(self, exc_type, exc_value, exc_tb):
        '''
        with...as语句块不管是否正常结束，都会调用此方法，如果语句块没有异常，三个参数值是None
        '''
        self.exc_type = exc_type
        self.exc_value = exc_value
        self.exc_tb = exc_tb
        self.smtp.quit()
        return None


    def send_mail(self, to_addr:str or list, message:str, title:str) -> str:
        ''' 
        发送信息给收件人
        :param:
            to_addr:收件人地址。一个地址的字符串，或者是地址列表。
            message:邮件内容，字符串。
            title：邮件标题
        :return:

        '''   
        msg = EmailMessage()
        msg['Subject'] = title 
        msg['From'] = Address(self.username, addr_spec = self.username) 
        msg['To'] = to_addr 
        msg.set_content(message)
        self.smtp.sendmail(self.username, to_addr, msg.as_string())
        
        return None
