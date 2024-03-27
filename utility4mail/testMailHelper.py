# -*- coding:utf_8 -*-


import time

def imap_test():
    with ImapHelper() as imap:
        today = time.strftime('%d-%b-%Y')
        #today = "15-Mar-2024"
        wht = imap.get_mails('BODY[HEADER]', F'(SINCE "{today}")')
    
    for w in wht:
        t = imap.trans_header(w)
        print(type(t))
        print(t['Subject'])
        print(t.get('Date'))


def smtp_test():
    with SmtpHelper() as smtp:
        smtp.send_mail('66461627@qq.com', '两个收人，就是个列表就可以邮件\n不用tostring行不', '两个收件人')


if __name__ == '__main__':
    
    from os import path as ospath
    from sys import path as syspath
    #将上级目录加入sys.path, 才能找到同级目录内的包
    syspath.append(ospath.dirname(ospath.dirname(__file__)))
    from mailhelper import ImapHelper, SmtpHelper
    
    #imap_test()
    smtp_test()