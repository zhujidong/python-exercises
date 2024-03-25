# -*- coding:utf_8 -*-


import time

def imap_test():
    with ImapHelper() as imap:
        #today = time.strftime('%d-%b-%Y')
        today = "15-Mar-2024"
        wht = imap.get_mails('BODY[HEADER]', F'(SINCE "{today}")')
    
    for w in wht:
        t = imap.trans_header(w)
        print(t.get('Subject'))
        print(t.get('Date'))


def smtp_test():
    with SmtpHelper() as smtp:
        print('smtp ok')


if __name__ == '__main__':
    
    from os import path as ospath
    from sys import path as syspath
    #将上级目录加入sys.path, 才能找到同级目录内的包
    syspath.append(ospath.dirname(ospath.dirname(__file__)))
    from mailhelper import ImapHelper, SmtpHelper
    
    #imap_test()
    #master_order()    smtp_test()